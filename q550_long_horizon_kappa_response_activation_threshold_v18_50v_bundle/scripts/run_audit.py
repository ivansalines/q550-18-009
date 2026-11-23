#!/usr/bin/env python3
"""Q550 v18.50v: long-horizon controlled-kappa response and passage ledger.

This audit uses genuine driven 10D integrations from two fixed inherited natural
turning seeds. A κ scan across/beyond the historic interval measures state,
RHS, structural-observer and 7D-nullspace-projector sensitivity on a shared
chart. It is designed to find *or reject* localized time-dependent parameter
response without making peak/edge assumptions. No material activation is
certified by a finite parameter scan or an observer-derived diagnostic.

All provenance is authenticated against the original server sendback v18.50u;
the nested genealogy is reconstructed in a temporary directory, not shipped
in the returned compact bundle. Python 3.13 recommended for historical code.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
U='q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle'
T='q550_paired_kappa_phase_aligned_edge_motion_projector_separation_v18_50t_bundle'
PARENT=ROOT/'inputs'/(U+'_server_sendback.zip')
# Five external controls left, thirteen within the historic interval, four right.
OFFSETS=np.r_[-2.,-1.5,-1.,-.75,-.5, np.linspace(0.,1.,13), 1.5,2.,2.5,3.]
DEFAULT_END=.05

def sha(b:bytes)->str:return hashlib.sha256(b).hexdigest()

def authenticate_u():
    with zipfile.ZipFile(PARENT) as z:
        bad=z.testzip()
        if bad is not None:raise RuntimeError('Parent u ZIP CRC failure at '+bad)
        sm=json.loads(z.read(U+'/SOURCE_MANIFEST.json'))
        om=json.loads(z.read(U+'/SHA256SUMS_OUTPUT.json'))
        if sm['root']!=U or om['root']!=U:raise RuntimeError('Unexpected source/output roots')
        for manifest,key in ((sm,'files'),(om,'file_sha256')):
            for rel,h in manifest[key].items():
                if sha(z.read(U+'/'+rel))!=h:raise RuntimeError('Parent u digest mismatch: '+rel)
        rpt=json.loads(z.read(U+'/results/report.json'))
        if rpt['version']!='v18.50u' or rpt['design']['new_10d_driven_ivps']!=28:
            raise RuntimeError('Wrong authenticated v18.50u parent')
        code=z.read(U+'/scripts/run_audit.py')
        tblob=z.read(U+'/inputs/'+T+'_server_sendback.zip')
    return {'sha256':sha(PARENT.read_bytes()),'source_files':len(sm['files']),
            'result_files':len(om['file_sha256'])},rpt,code,tblob

def stage_model(tmp,code,tblob):
    stage=tmp/U
    (stage/'scripts').mkdir(parents=True)
    (stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(code)
    (stage/'inputs'/(T+'_server_sendback.zip')).write_bytes(tblob)
    spec=importlib.util.spec_from_file_location('v18_50v_authenticated_parent_u',stage/'scripts/run_audit.py')
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    tinfo,tscript,sblob,treport=mod.authenticate_t()
    t,q,p,o,engine,unit,drpt,creport,events=mod.reconstruct_t(tmp,tscript,sblob)
    return t,q,p,o,engine,unit,drpt,creport,tinfo

def phase_grid(end:float)->np.ndarray:
    """Dense through historic gate, then medium and longer post-passage scales."""
    if end<.0125:raise ValueError('Horizon must reach at least 0.0125')
    grid=np.r_[np.linspace(0,.001092,17), [.00105,.001059,.001068,.001075],
               np.linspace(.001092,.0125,25),np.linspace(.0125,end,35)]
    return np.unique(np.clip(grid,0,end))

def analytic_observer(t,q,engine,state,kappa,ctx,shared_scale,weights):
    d,B,J=t.physical_observer(q,engine,state,kappa,ctx['scale'],shared_scale,weights)
    P,K,s=t.basis_projector(q,B)
    return d,P,s

def make_ivp(engine,ctx,kappa,end,rtol,atol,maxstep):
    des=engine.original_ramp.Design('v18_50v','beta:2:2',.24)
    event=float(ctx['event'])
    def rhs(t,z):
        y=np.r_[z,ctx['theta'](t)]
        return np.asarray(engine.physical.rhs_from_original(
            y,kappa,engine.params,engine.slope,engine.clock.cubic_clock_sign(t,des),
            engine.support,engine.audit)[:10],float)
    sol=solve_ivp(rhs,(event,event+end),np.asarray(ctx['seed'][:10],float),
                  method='DOP853',rtol=rtol,atol=atol,max_step=maxstep,dense_output=True)
    if not sol.success or abs(sol.t[-1]-(event+end))>1e-10:
        raise RuntimeError(f'Incomplete physical IVP κ={kappa}: '+sol.message)
    return sol,rhs

def measures_for_seed(t,q,engine,ctx,kappas,xis,shared_scale,weights,rtol,atol,maxstep):
    """Integrate ALL variants including the baseline over the extended window.

    The inherited short ctx.sol ends at ξ=.001092, so it MUST NOT be extrapolated.
    """
    nk,nx=len(kappas),len(xis)
    Z=np.zeros((nk,nx,10));F=np.zeros_like(Z)
    D=np.zeros((nk,nx,4));P=np.zeros((nk,nx,10,10));SV=np.zeros((nk,nx,2))
    nfev=0;integrations=[]
    for ik,k in enumerate(kappas):
        sol,rhs=make_ivp(engine,ctx,float(k),float(xis[-1]),rtol,atol,maxstep)
        nfev+=sol.nfev
        integrations.append({'seed_family':ctx['kind'],'kappa':float(k),'nfev':sol.nfev,
                             'steps':len(sol.t)-1,'success':int(sol.success),'t_final':float(sol.t[-1]),
                             'event_t':float(ctx['event'])})
        for j,xi in enumerate(xis):
            ti=float(ctx['event']+xi)
            z=np.asarray(sol.sol(ti),float)
            y=np.r_[z,ctx['theta'](ti)]
            Z[ik,j]=z;F[ik,j]=rhs(ti,z)
            d,Pij,s=analytic_observer(t,q,engine,y,float(k),ctx,shared_scale,weights)
            D[ik,j]=d;P[ik,j]=Pij;SV[ik,j]=s[2:4]
        print(f'INTEGRATION seed={ctx["kind"]} {ik+1}/{nk} offset={(k-kappas[5])/(kappas[17]-kappas[5]):+.4f} nfev={sol.nfev}',flush=True)
    return {'Z':Z,'F':F,'D':D,'P':P,'SV':SV,'nfev':nfev,'integrations':integrations}

def norm(x,axes):return np.linalg.norm(x,axis=axes)

def sensitivity_fields(dat,kappas,shared_scale):
    """Derivative w.r.t. parameter BEFORE taking norms: removes anchor V cusp."""
    dz=np.gradient(dat['Z'],kappas,axis=0,edge_order=2)
    dd=np.gradient(dat['D'],kappas,axis=0,edge_order=2)
    dP=np.gradient(dat['P'],kappas,axis=0,edge_order=2)
    dF=np.gradient(dat['F'],kappas,axis=0,edge_order=2)
    return {'state_gain':norm(dz*shared_scale[None,None,:],2),
            'observer_gain':norm(dd,2),
            'projector_gain':norm(dP,(2,3)),
            'rate_gain':norm(dF*shared_scale[None,None,:],2)}

def peak_candidates(kappas,gain,flank,inside_mask,contrast_threshold):
    """Only interior maxima against BOTH flank controls; no endpoint V peaks."""
    out=[]
    for i in range(1,len(kappas)-1):
        if not inside_mask[i] or not(gain[i]>gain[i-1] and gain[i]>gain[i+1]):continue
        flank_max=max(float(gain[flank[0]].max()),float(gain[flank[1]].max()))
        if flank_max<=0:continue
        contrast=float(gain[i]/flank_max)
        if contrast<contrast_threshold:continue
        out.append({'index':i,'kappa':float(kappas[i]),'gain':float(gain[i]),'flank_max':flank_max,'contrast':contrast})
    return out

def summarize_ridges(cases,kappas,xis,fields,threshold):
    flank=(np.where(OFFSETS<=-.5)[0],np.where(OFFSETS>=1.5)[0])
    inside=(OFFSETS>0)&(OFFSETS<1)
    records=[];raw_candidates=[]
    # Three independent curves in the same controlled scan.
    for seed in ('original','autonomous'):
        for measure in ('state_gain','observer_gain','projector_gain','rate_gain'):
            g=fields[seed][measure]
            for j,xi in enumerate(xis):
                found=peak_candidates(kappas,g[:,j],flank,inside,threshold)
                imax=int(np.argmax(g[:,j]));max_inside=int(np.argmax(g[inside,j]))
                indices=np.where(inside)[0];imiddle=int(indices[max_inside])
                records.append({'seed_family':seed,'measure':measure,'xi':float(xi),
                                'global_max_offset':float(OFFSETS[imax]),
                                'internal_max_offset':float(OFFSETS[imiddle]),
                                'max_inside_to_flank':float(g[imiddle,j]/max(g[flank[0],j].max(),g[flank[1],j].max(),1e-20)),
                                'qualified_internal_ridge':int(bool(found)),
                                'qualified_kappa_offset':float(OFFSETS[found[0]['index']]) if found else np.nan})
                for v in found:raw_candidates.append({'seed_family':seed,'measure':measure,'xi':float(xi),'offset':float(OFFSETS[v['index']]),'contrast':v['contrast']})
    record=pd.DataFrame(records);peaks=pd.DataFrame(raw_candidates,columns=['seed_family','measure','xi','offset','contrast'])
    # Persistence: local feature must appear at >=2 consecutive time sections
    # in >=2 measures; separate seed agreement required for model-wide claim.
    results={}
    for seed in ('original','autonomous'):
        checks={}
        for measure in ('state_gain','observer_gain','projector_gain','rate_gain'):
            rr=record[(record.seed_family==seed)&(record.measure==measure)].sort_values('xi')
            x=rr.qualified_internal_ridge.to_numpy(dtype=int)
            pairs=np.where((x[:-1]==1)&(x[1:]==1))[0]
            checks[measure]={'qualifying_times':int(x.sum()),'persistent_adjacent_times':int(len(pairs)),
                             'first_qualifying_xi':float(rr.iloc[np.where(x==1)[0][0]].xi) if x.any() else None}
        results[seed]=checks
    # Require two independent 10D dynamical sensitivities and a geometric
    # cross-check, not observer-only peaks. Adjacent time samples must have
    # κ maxima within one inner-grid interval for BOTH fixed seed families.
    robust_both=False
    for jj in range(len(xis)-1):
        for ki in np.where(inside)[0]:
            by_seed=[]
            for seed in ('original','autonomous'):
                strict=True
                for tim in (float(xis[jj]),float(xis[jj+1])):
                    sample=peaks[(peaks.seed_family==seed)&np.isclose(peaks.xi,tim,rtol=0,atol=1e-14)]
                    for typ in ('state_gain','rate_gain'):
                        if not ((sample.measure==typ)&(np.abs(sample.offset-OFFSETS[ki])<=1/12+1e-8)).any():
                            strict=False
                    if not ((sample.measure.isin(('observer_gain','projector_gain')))&
                            (np.abs(sample.offset-OFFSETS[ki])<=1/12+1e-8)).any():
                        strict=False
                by_seed.append(strict)
            if all(by_seed):robust_both=True
    return record,peaks,results,robust_both

def generate_plots(data,record,kappas,xis,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        arr=data[seed]['state_gain']
        im=ax.pcolormesh(OFFSETS,xis,arr.T,shading='auto',cmap='viridis')
        ax.axvspan(0,1,color='white',alpha=.1)
        ax.set(title=seed,xlabel='Normalized κ offset',ylabel='Turn-relative ξ')
        fig.colorbar(im,ax=ax,label='||∂κ z|| in shared chart')
    fig.suptitle('v18.50v — Actual driven state sensitivity: where is the moving response?')
    fig.tight_layout();fig.savefig(out/'state_sensitivity_kappa_time_map.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        for xi in [float(xis[np.argmin(abs(xis-x))]) for x in [.001092,.0125,.05]]:
            j=int(np.argmin(abs(xis-xi)))
            ax.plot(OFFSETS,data[seed]['state_gain'][:,j],'.-',label=f'ξ={xi:.5g}')
        ax.axvspan(0,1,color='0.7',alpha=.15)
        ax.set(title=seed,xlabel='Normalized κ offset',ylabel='||∂κ z||, common chart')
        ax.legend();ax.grid(alpha=.2)
    fig.suptitle('v18.50v — Parameter response across early, medium and long sections')
    fig.tight_layout();fig.savefig(out/'three_horizons_state_response.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        for name in ('state_gain','observer_gain','projector_gain'):
            arr=data[seed][name];sl=np.where((OFFSETS>0)&(OFFSETS<1))[0]
            outer=np.r_[np.where(OFFSETS<=-.5)[0],np.where(OFFSETS>=1.5)[0]]
            ratio=arr[sl].max(axis=0)/np.maximum(arr[outer].max(axis=0),1e-25)
            ax.plot(xis[1:],ratio[1:],label=name)
        ax.axhline(1.15,color='black',linestyle=':',lw=1,label='screen threshold')
        ax.set(title=seed,xlabel='Turn-relative ξ',ylabel='Internal maximum / strongest outer control')
        ax.set_xscale('symlog',linthresh=.001)
        ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('v18.50v — Internal contrast against controls: not an activation certificate')
    fig.tight_layout();fig.savefig(out/'internal_contrast_time_history.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        for name in ('state_gain','rate_gain'):
            arr=data[seed][name];middle=int(np.argmin(abs(OFFSETS-.5)))
            ax.plot(xis,arr[middle],label=name)
        ax.set(title=seed,xlabel='Turn-relative ξ',ylabel='Parameter-response norm')
        ax.grid(alpha=.2);ax.legend()
    fig.suptitle('v18.50v — Observe the entire passage; no binary peak required')
    fig.tight_layout();fig.savefig(out/'midband_response_passage.png',dpi=145);plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--end',type=float,default=DEFAULT_END)
    ap.add_argument('--rtol',type=float,default=2e-10)
    ap.add_argument('--atol',type=float,default=2e-11)
    ap.add_argument('--max-step',type=float,default=.00125)
    ap.add_argument('--contrast',type=float,default=1.15)
    ap.add_argument('--preflight-only',action='store_true')
    a=ap.parse_args()
    if not(.0125<=a.end<=.10):raise ValueError('Limit long horizon to [.0125,.10]')
    if not(1<a.contrast<=3):raise ValueError('Bad contrast')
    info,u_report,code,tblob=authenticate_u()
    print('AUTHENTICATED 50u',info,flush=True)
    if a.preflight_only:return
    kappas=float(u_report['kappa']['autonomous'])+OFFSETS*float(u_report['kappa']['delta'])
    xis=phase_grid(a.end)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    all_fields={};ledger=[];integrations=[];all_svs=[]
    with tempfile.TemporaryDirectory(prefix='v18_50v_gen_') as temp:
        t,q,p,o,engine,unit,drpt,creport,tinfo=stage_model(Path(temp),code,tblob)
        co=p.make_context(o,'original',engine,unit,drpt,creport)
        ca=p.make_context(o,'autonomous',engine,unit,drpt,creport)
        contexts={'original':co,'autonomous':ca}
        shared_scale=np.maximum.reduce((np.ones(10),co['scale'],ca['scale']))
        weights=np.asarray(drpt['common_metric_scale_4d'],float)
        for label,ctx in contexts.items():
            data=measures_for_seed(t,q,engine,ctx,kappas,xis,shared_scale,weights,a.rtol,a.atol,a.max_step)
            integrations+=data['integrations']
            fields=sensitivity_fields(data,kappas,shared_scale)
            all_fields[label]=fields
            anchor=int(np.argmin(abs(kappas-ctx['kappa0'])))
            for ik,k in enumerate(kappas):
                for j,xi in enumerate(xis):
                    state_dev=float(norm((data['Z'][ik,j]-data['Z'][anchor,j])*shared_scale,0))
                    rhs_dev=float(norm((data['F'][ik,j]-data['F'][anchor,j])*shared_scale,0))
                    observer_dev=float(norm(data['D'][ik,j]-data['D'][anchor,j],0))
                    proj_dev=float(norm(data['P'][ik,j]-data['P'][anchor,j],(0,1)))
                    row={'seed_family':label,'kappa':float(k),'offset_units':float(OFFSETS[ik]),
                         'xi':float(xi),'event_t':float(ctx['event']),
                         'stage':'early' if xi<=.001092+1e-12 else ('medium' if xi<=.0125+1e-12 else 'long'),
                         'state_delta_from_seed_anchor':state_dev,
                         'rate_delta_from_seed_anchor':rhs_dev,
                         'observer_delta_from_seed_anchor':observer_dev,
                         'projector_gap_from_seed_anchor':proj_dev,
                         **{key:float(fields[key][ik,j]) for key in fields},
                         'observer_strong_s3':float(data['SV'][ik,j,0]),
                         'observer_weak_s4':float(data['SV'][ik,j,1])}
                    ledger.append(row)
            print('FIELD COMPLETE seed',label,'rows so far',len(ledger),flush=True)
    df=pd.DataFrame(ledger)
    series,peaks,checks,robust=summarize_ridges(contexts,kappas,xis,all_fields,a.contrast)
    (out/'long_horizon_kappa_response_ledger.csv').write_text(df.to_csv(index=False,float_format='%.17g'))
    (out/'moving_tooth_ridge_watch.csv').write_text(series.to_csv(index=False,float_format='%.17g'))
    (out/'candidate_peak_events.csv').write_text(peaks.to_csv(index=False,float_format='%.17g'))
    (out/'integration_completion.csv').write_text(pd.DataFrame(integrations).to_csv(index=False,float_format='%.17g'))
    generate_plots(all_fields,series,kappas,xis,out)
    mid_index=int(np.argmin(abs(OFFSETS-.5)))
    watchpoints={}
    for seed in ('original','autonomous'):
        entries=[]
        for target in (.001092,.0125,.05):
            if target>xis[-1]+1e-14:continue
            jj=int(np.argmin(abs(xis-target)))
            f=all_fields[seed]
            gains=f['state_gain'][:,jj]
            in_band=gains[(OFFSETS>=0)&(OFFSETS<=1)]
            entries.append({'xi':float(xis[jj]),'center_state_gain':float(gains[mid_index]),
                  'center_rate_gain':float(f['rate_gain'][mid_index,jj]),
                  'center_observer_gain':float(f['observer_gain'][mid_index,jj]),
                  'center_projector_gain':float(f['projector_gain'][mid_index,jj]),
                  'in_band_state_gain_relative_spread':float(np.ptp(in_band)/max(float(in_band.mean()),1e-30))})
        watchpoints[seed]=entries
    report={'version':'v18.50v','title':'Long-Horizon κ0 Response & Activation-Threshold Audit',
      'classification':'CONTROLLED_DYNAMIC_PARAMETER_RESPONSE_DIAGNOSTIC_NOT_MATERIAL_ACTIVATION_CERTIFICATE',
      'parent_u':info,'parent_t':tinfo,'kappa':{'original':float(u_report['kappa']['original']),
       'autonomous':float(u_report['kappa']['autonomous']),'delta':float(u_report['kappa']['delta']),
       'offsets':OFFSETS.tolist(),'values':kappas.tolist()},
      'design':{'two_fixed_natural_seeds':True,'drive_shape':'beta:2:2','ramp_xi':.24,
        'extended_xi_end':float(xis[-1]),'phase_sections':len(xis),'parameter_points':len(kappas),
        'new_10d_driven_ivps':len(integrations),'rows':len(df),'integrator':'DOP853',
        'rtol':a.rtol,'atol':a.atol,'max_step':a.max_step,'independent_observables':
        ['10D state sensitivity','10D RHS sensitivity','normalized 4D structural observer','rank-three Jacobian 7D projector'],
        'common_chart':'elementwise max of seed scales and 1'},
      'diagnostics':{'complete_ivps':int(sum(x['success'] for x in integrations)),
        'nfev':int(sum(x['nfev'] for x in integrations)),
        'minimum_third_sv':float(df.observer_strong_s3.min()),
        'maximum_fourth_sv':float(df.observer_weak_s4.max()),
        'max_state_gain':float(df.state_gain.max()),
        'max_projector_gain':float(df.projector_gain.max()),
        'time_ridge_screen':checks,
        'multiple_seed_and_measure_persistence_screen':bool(robust),
        'candidate_rows':len(peaks),'watchpoints':watchpoints},
      'decision':{'outcome':('CONTROLLED_LOCALIZED_CONTRAST_CANDIDATE' if robust else
                             'NO_LOCALIZED_CONTRAST_DETECTED_WITHIN_WINDOW'),
       'conditional_interpretation':
       'No qualifying internal contrast is a negative finding only within sampled κ, ξ, chart and seeds.'
       if not robust else 'Localized internal response candidate requires further grid refinement, seed variation and physical-response validation.',
       'threshold_internal_to_outer':a.contrast,'threshold_requires':'Strict interior maximum, stronger than both outer controls, two consecutive times, both 10D dynamical measures, one geometric observer measure, both fixed seeds, κ alignment within one inner grid step',
       'cannot_establish':'material activation, physical edges, oscillator bandwidth, or response invariant to observer chart'},
      'limitations':['A fixed-seed driven κ scan is not a preparation of a natural orbit for each κ.',
       'The original turning section and drive clock are held fixed separately inside each seed family.',
       'The observer metric and shared state chart are declared, not physical kinetic-metric certificates.',
       'Finite ξ and κ grids cannot exclude unobserved narrow or later activation.',
       'A local maximum of an observer sensitivity is not a material activation threshold.',
       'The scalar nullspace projector has no intrinsic material stiffness or energy assigned.',
       'The moving-tooth ledger is recorded even if no qualifying ridge is present.'],
      'environment':{'python':platform.python_version(),'numpy':np.__version__,
                     'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('v18.50v COMPLETED',json.dumps(report['diagnostics'],indent=2),flush=True)

if __name__=='__main__':main()
