#!/usr/bin/env python3
"""Q550 v18.50w: anchored equidistance-root trajectories using authentic v18.50v data.

Pure authenticated POSTPROCESSING; no new physical IVPs. Both seed families were
prepared independently; equal ξ denotes turn-relative evolution (not equal
absolute time). The zero of a difference between two anchored distances is
not, by itself, a material threshold or a physical equidistance manifold.
"""
from __future__ import annotations
import hashlib, io, json, platform, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import PchipInterpolator, CubicSpline
from scipy.optimize import brentq

ROOT=Path(__file__).resolve().parents[1]
V='q550_long_horizon_kappa_response_activation_threshold_v18_50v_bundle'
U='q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle'
PARENT=ROOT/'inputs'/(V+'_server_sendback.zip')
FIELDS={
 'projector_gap':'projector_gap_from_seed_anchor',
 'observer_gap':'observer_delta_from_seed_anchor',
 'rhs_gap':'rate_delta_from_seed_anchor',
 'state_gap':'state_delta_from_seed_anchor',
}

def digest(data):return hashlib.sha256(data).hexdigest()

def authenticate_zip(z,basename):
    bad=z.testzip()
    if bad:raise RuntimeError(f'{basename}: invalid ZIP member {bad}')
    sm=json.loads(z.read(f'{basename}/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(f'{basename}/SHA256SUMS_OUTPUT.json'))
    if sm['root']!=basename or om['root']!=basename:
        raise RuntimeError('Manifest root mismatch')
    for manifest,key in ((sm,'files'),(om,'file_sha256')):
        for rel,expected in manifest[key].items():
            if digest(z.read(f'{basename}/{rel}'))!=expected:
                raise RuntimeError('Parent source/output SHA256 mismatch: '+rel)
    return {'sources':len(sm['files']),'outputs':len(om['file_sha256'])}

def load_parents():
    with zipfile.ZipFile(PARENT) as z:
        auth=authenticate_zip(z,V)
        report=json.loads(z.read(f'{V}/results/report.json'))
        if report['version']!='v18.50v' or report['design']['new_10d_driven_ivps']!=44:
            raise RuntimeError('Wrong authentic v18.50v genealogy')
        ledger=pd.read_csv(io.BytesIO(z.read(f'{V}/results/long_horizon_kappa_response_ledger.csv')))
        ublob=z.read(f'{V}/inputs/{U}_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(ublob)) as zu:
        auth_u=authenticate_zip(zu,U)
        ureport=json.loads(zu.read(f'{U}/results/report.json'))
        uledger=pd.read_csv(io.BytesIO(zu.read(f'{U}/results/fixed_seed_kappa_dynamic_scan.csv')))
        if ureport['version']!='v18.50u':raise RuntimeError('Not v18.50u')
    return ledger,report,uledger,ureport,{'v':auth,'u':auth_u,'v_zip_sha256':digest(PARENT.read_bytes()),'u_zip_sha256':digest(ublob)}

def pivot(df,field,x_key='xi'):
    if not {'seed_family','offset_units',x_key,field}.issubset(df.columns):raise RuntimeError('Missing required ledger fields')
    offsets=np.sort(df.offset_units.unique())
    xis=np.sort(df[x_key].unique())
    aa=df[df.seed_family=='autonomous'].pivot(index='offset_units',columns=x_key,values=field).reindex(index=offsets,columns=xis)
    bb=df[df.seed_family=='original'].pivot(index='offset_units',columns=x_key,values=field).reindex(index=offsets,columns=xis)
    if aa.isnull().values.any() or bb.isnull().values.any():raise RuntimeError('Incomplete paired grid')
    return offsets,xis,aa.values.astype(float),bb.values.astype(float)

def find_bracket(x,f):
    changes=np.flatnonzero(f[:-1]*f[1:]<0)
    if len(changes)!=1: return None
    return int(changes[0])

def roots_for_field(df,field,method='pchip',drop_midpoint=False):
    offsets,xis,A,O=pivot(df,field)
    if drop_midpoint:
        keep=np.abs(offsets-.5)>1e-7
        offsets,A,O=offsets[keep],A[keep],O[keep]
    F=A-O
    roots=[];brackets=[];slopes=[]
    for j,xi in enumerate(xis):
        yy=F[:,j]
        idx=find_bracket(offsets,yy)
        if idx is None:
            roots.append(float('nan')); brackets.append((float('nan'),float('nan')));slopes.append(float('nan'));continue
        if method=='pchip': interpol=PchipInterpolator(offsets,yy)
        elif method=='cubic': interpol=CubicSpline(offsets,yy)
        elif method=='linear': interpol=None
        else:raise ValueError(method)
        if interpol is None:
            root=float(offsets[idx]-yy[idx]*(offsets[idx+1]-offsets[idx])/(yy[idx+1]-yy[idx]))
            slope=float((yy[idx+1]-yy[idx])/(offsets[idx+1]-offsets[idx]))
        else:
            root=float(brentq(interpol,float(offsets[idx]),float(offsets[idx+1]),xtol=1e-14))
            slope=float(interpol.derivative()(root))
        roots.append(root);brackets.append((float(offsets[idx]),float(offsets[idx+1])));slopes.append(slope)
    return offsets,xis,F,np.array(roots),np.array(brackets),np.array(slopes)

def implicit_velocity(offsets,xis,F,roots,slopes):
    # PCHIP on the raw signed gap in xi, THEN interpolate its partial derivative
    # across kappa to the root. The xi derivative is independent of the root's
    # motion, so this implements the implicit function theorem correctly.
    partial_xi=PchipInterpolator(xis,F.T,axis=0).derivative()(xis)
    speeds=np.full_like(roots,np.nan)
    for i,root in enumerate(roots):
        if np.isfinite(root) and abs(slopes[i])>1e-12:
            fx_t=float(PchipInterpolator(offsets,partial_xi[i])(root))
            speeds[i]=-fx_t/slopes[i]
    return speeds

def independent_u_check(u,v):
    stats=[]
    for xi in (0.,.001092):
        for field_u,field_v in [('projector_gap_full','projector_gap_from_seed_anchor'),
                                ('projector_gap_parameter_only','projector_gap_from_seed_anchor')]:
            _,xt,_,ru,_,_=roots_for_field(u,field_u)
            _,xv,_,rv,_,_=roots_for_field(v,field_v)
            iu=np.argmin(abs(xt-xi));iv=np.argmin(abs(xv-xi))
            if abs(xt[iu]-xi)>1e-12 or abs(xv[iv]-xi)>1e-12:raise RuntimeError('Missing overlapping phase')
            stats.append({'xi':xi,'u_measure':field_u,'v_measure':field_v,
                          'u_root_normalized':float(ru[iu]),'v_root_normalized':float(rv[iv]),
                          'root_difference_normalized':float(ru[iu]-rv[iv])})
    return stats

def write_plots(trace,profiles,out,delta):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,5.2))
    for f,caption in [('projector_gap','7D projector'),('observer_gap','structural observer'),
                       ('rhs_gap','driven RHS'),('state_gap','10D state')]:
        d=trace[trace.measure==f]
        ax.plot(d.xi,d.root_normalized,label=caption)
    ax.axhline(.5,ls='--',lw=1,label='arithmetic midpoint (reference)')
    ax.set(xlabel='Turn-relative evolution ξ',ylabel='κ equidistance crossing, normalized 0..1',
           title='v18.50w | A crossing exists, but its motion depends on the measured response')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(out/'moving_gate_observable_comparison.png',dpi=155);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5.2))
    for f,caption in [('projector_gap','7D projector'),('observer_gap','structural observer'),('rhs_gap','driven RHS')]:
        d=trace[trace.measure==f]
        ax.plot(d.xi,(d.root_normalized-d.root_normalized.iloc[0])*1e6,label=caption)
    ax.set(xlabel='Turn-relative evolution ξ',ylabel='Crossing displacement, parts per million of κ interval',
           title='v18.50w | Two directions of tooth motion, no imposed peak')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(out/'equidistance_gate_drift.png',dpi=155);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5.2))
    for x_target in (0.,.001092,.0125,.05):
        d=profiles[np.isclose(profiles.xi,x_target,atol=2e-13)]
        if len(d):
            ax.plot(d.offset_units,d.signed_gap,label=f'ξ={x_target:.6g}')
    ax.axhline(0,ls='--',lw=1)
    ax.axvspan(0,1,alpha=.09)
    ax.set(xlabel='Normalized κ offset',ylabel='D_auto − D_orig (projector operator norm)',
           title='v18.50w | Signed difference underlying the double V')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(out/'signed_anchor_gap_crossings.png',dpi=155);plt.close(fig)

def main():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    v,vr,u,ur,auth=load_parents()
    kappa_auto=float(vr['kappa']['autonomous']); delta=float(vr['kappa']['delta'])
    kappa_orig=float(vr['kappa']['original'])
    if not(delta>0 and abs(kappa_auto+delta-kappa_orig)<1e-14):raise RuntimeError('Bad endpoints')
    records=[];profile_rows=[];summaries={};metrics={}
    for name,field in FIELDS.items():
        x,xis,F,roots,brackets,slopes=roots_for_field(v,field)
        if len(xis)!=79:raise RuntimeError('Expected 79 long-horizon sections')
        # State gap is exactly zero in both reference families at ξ=0:
        # equidistance is completely non-unique there, and is NOT imputed.
        velocities=implicit_velocity(x,xis,F,roots,slopes)
        for j,xi in enumerate(xis):
            records.append({'measure':name,'xi':float(xi),
                'root_normalized':float(roots[j]),'root_kappa':float(kappa_auto+delta*roots[j]) if np.isfinite(roots[j]) else np.nan,
                'bracket_left_offset':brackets[j,0],'bracket_right_offset':brackets[j,1],
                'signed_gap_slope_dF_doffset':slopes[j],
                'implicit_dx_dxi':velocities[j],
                'implicit_dkappa_dxi':float(delta*velocities[j]) if np.isfinite(velocities[j]) else np.nan,
                'crossing_detected':int(np.isfinite(roots[j]))})
            if name=='projector_gap':
                for a,ff in zip(x,F[:,j]):
                    profile_rows.append({'xi':float(xi),'offset_units':float(a),
                                         'kappa':float(kappa_auto+a*delta),'signed_gap':float(ff)})
        valid=roots[np.isfinite(roots)]
        dif=np.diff(valid)
        summaries[name]={'n_sections':len(xis),'n_unique_roots':len(valid),
            'start_root':float(roots[0]),'end_root':float(roots[-1]),
            'drift_normalized':float(valid[-1]-valid[0]),
            'drift_absolute_kappa':float((valid[-1]-valid[0])*delta),
            'increasing_steps':int(np.sum(dif>0)), 'decreasing_steps':int(np.sum(dif<0)),
            'min_abs_dF_doffset':float(np.nanmin(abs(slopes)))}
        _,_,_,lin,_,_=roots_for_field(v,field,method='linear')
        _,_,_,cub,_,_=roots_for_field(v,field,method='cubic')
        _,_,_,no_mid,_,_=roots_for_field(v,field,drop_midpoint=True)
        metrics[name]={'max_abs_pchip_minus_linear':float(np.nanmax(abs(roots-lin))),
                       'max_abs_pchip_minus_cubic':float(np.nanmax(abs(roots-cub))),
                       'max_abs_pchip_minus_no_midpoint':float(np.nanmax(abs(roots-no_mid))),
                       'drift_pchip':float(valid[-1]-valid[0]),
                       'drift_linear':float(lin[np.isfinite(lin)][-1]-lin[np.isfinite(lin)][0]),
                       'drift_no_midpoint':float(no_mid[np.isfinite(no_mid)][-1]-no_mid[np.isfinite(no_mid)][0])}
    trace=pd.DataFrame(records);profiles=pd.DataFrame(profile_rows)
    u_checks=independent_u_check(u,v)
    trace.to_csv(out/'equidistance_gate_time_ledger.csv',index=False,float_format='%.17g')
    profiles.to_csv(out/'signed_projector_distance_profiles.csv',index=False,float_format='%.17g')
    pd.DataFrame(u_checks).to_csv(out/'u_v_short_window_comparison.csv',index=False,float_format='%.17g')
    write_plots(trace,profiles,out,delta)
    report={'version':'v18.50w','title':'Moving Equidistance Gate & Two-Reference Transport Audit',
      'classification':'ANCHORED_EQUIDISTANCE_CROSSING_DIAGNOSTIC_NOT_INTRINSIC_MATERIAL_GATE_OR_ACTIVATION_CERTIFICATE',
      'parent_authentication':auth,
      'design':{'no_new_physical_integrations':True,'parent_v_10D_ivps':44,
                'seed_preparations':'Distinct natural seeds; matching ξ is relative to each seed turn event',
                'observables':FIELDS,'kappa_auto':kappa_auto,'kappa_original':kappa_orig,
                'delta_kappa':delta,'phase_sections':79,'kappa_grid':22,
                'interpolation':'PCHIP roots of signed distance difference, with linear/cubic/no-midpoint controls',
                'root_speed':'implicit -partial_xi F/partial_kappa F, using time and parameter PCHIP'},
      'measurements':summaries,'interpolation_robustness':metrics,
      'u_independent_short_window_comparisons':u_checks,
      'critical_interpretation':[
        'Distance-to-reference zeroes are definitionally at their respective anchors, not discovered physical zeros.',
        'At least one equidistance crossing between anchors is expected by continuity when distance curves preserve the endpoint ordering.',
        'Different observable distances produce different crossing paths and even different signs of drift.',
        'Neither an oscillating boundary nor a material activator is established by these crossings.',
        'The root-speed is numerically tiny in absolute kappa and no guaranteed rigorous error bound is claimed.',
        'Postprocessing of the genuine v18.50v real-solver replay; no new Q550 integrations.'
      ],'environment':{'python':platform.python_version(),'numpy':np.__version__,
           'pandas':pd.__version__,'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('v18.50w COMPLETE',json.dumps({'parent':auth,'root_paths':summaries,'interpolation':metrics},indent=2),flush=True)
if __name__=='__main__':main()
