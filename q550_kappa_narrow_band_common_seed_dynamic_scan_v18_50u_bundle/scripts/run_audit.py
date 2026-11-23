#!/usr/bin/env python3
"""Q550 v18.50u — Narrow-kappa common-seed driven replay and projector response.

Authenticates the v18.50t server sendback and reconstructs its original Q550
solver, observer and turning seeds. Every parameter scan point has an actual
new driven 10D IVP initialized from one of two FIXED seeds. This is a
controlled-parameter experiment, not re-preparation of a natural orbit at each
kappa. Both the parameter-only and changed-state contributions to the exact
projector difference are separately stored in the same shared state chart.

No binary 'active band' is inferred from just two endpoints or from monotone
projector gaps. All source code comments, reports and metadata are in English.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
T='q550_paired_kappa_phase_aligned_edge_motion_projector_separation_v18_50t_bundle'
S='q550_principal_angle_conditioning_tangent_integrator_convergence_v18_50s_bundle'
R='q550_differential_kernel_invariance_analytic_tangent_generator_v18_50r_bundle'
PARENT=ROOT/'inputs'/(T+'_server_sendback.zip')
WINDOW=0.001092
OFFSET_LIST=np.array([-2.,-1.,-.5,0.,.125,.25,.375,.5,.625,.75,.875,1.,1.5,2.,3.])

def sha(b):return hashlib.sha256(b).hexdigest()

def projector_gap(P,Q):
    """Operator norm distance of orthogonal projectors in one shared chart."""
    return float(np.linalg.svd(P-Q,compute_uv=False)[0])

def local_peak_candidates(x,y,min_prominence=0.2):
    """Conservative, interior-only peaks; endpoints never count."""
    x=np.asarray(x,float);y=np.asarray(y,float)
    out=[]
    for i in range(1,len(y)-1):
        if not (y[i]>y[i-1] and y[i]>y[i+1]):continue
        prom=y[i]-max(np.min(y[:i]),np.min(y[i+1:]))
        if prom>=min_prominence:out.append((float(x[i]),float(y[i]),float(prom)))
    return out

def authenticate_t():
    with zipfile.ZipFile(PARENT) as z:
        if z.testzip() is not None:raise RuntimeError('Parent t ZIP CRC failure')
        sm=json.loads(z.read(T+'/SOURCE_MANIFEST.json'))
        om=json.loads(z.read(T+'/SHA256SUMS_OUTPUT.json'))
        if sm['root']!=T or om['root']!=T:raise RuntimeError('Unexpected parent roots')
        for manifest,key in ((sm,'files'),(om,'file_sha256')):
            for rel,h in manifest[key].items():
                if sha(z.read(T+'/'+rel))!=h:raise RuntimeError('Parent t drift: '+rel)
        report=json.loads(z.read(T+'/results/report.json'))
        code=z.read(T+'/scripts/run_audit.py')
        sblob=z.read(T+'/inputs/'+S+'_server_sendback.zip')
    if report['version']!='v18.50t':raise RuntimeError('Unexpected parent scientific report')
    if report['diagnostics']['full_pair_gap_slope_sign_changes']!=0:raise RuntimeError('Unexpected parent extrema')
    return ({'sha256':sha(PARENT.read_bytes()),'source_count':len(sm['files']),
             'result_count':len(om['file_sha256'])}, code, sblob, report)

def reconstruct_t(tmp,code,sblob):
    stage=tmp/T;(stage/'scripts').mkdir(parents=True);(stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(code)
    (stage/'inputs'/(S+'_server_sendback.zip')).write_bytes(sblob)
    spec=importlib.util.spec_from_file_location('v18_50u_authenticated_parent_t',stage/'scripts/run_audit.py')
    t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
    info,s_script,r_blob=t.authenticate_s()
    q,r,p,o,engine,unit,drpt,creport,events=t.dynamic_model_stage(tmp,s_script,r_blob)
    return t,q,p,o,engine,unit,drpt,creport,events

def kernel_at(t,q,engine,y,kappa,branch_scale,shared_scale,weights):
    d,B,J=t.physical_observer(q,engine,y,kappa,branch_scale,shared_scale,weights)
    P,K,s=t.basis_projector(q,B)
    return P,s

def variant_trajectory(engine,ctx,kappa,xi_end,rtol,atol,max_step):
    """New physical 10D IVP, but same reference seed, imposed clock and turn."""
    if kappa==ctx['kappa0']:
        return ctx['sol'],0,True,False
    a=engine.original_ramp.Design('v18_50u','beta:2:2',.24)
    event=ctx['event'];theta=ctx['theta']
    def ode(t,z):
        y=np.r_[z,theta(t)]
        return np.asarray(engine.physical.rhs_from_original(
            y,kappa,engine.params,engine.slope,engine.clock.cubic_clock_sign(t,a),
            engine.support,engine.audit)[:10],float)
    sol=solve_ivp(ode,(event,event+xi_end),np.asarray(ctx['seed'][:10]),
                  method='DOP853',rtol=rtol,atol=atol,max_step=max_step,dense_output=True)
    if not sol.success or abs(sol.t[-1]-(event+xi_end))>1e-10:
        raise RuntimeError(f'Non-complete kappa IVP k={kappa}: {sol.message}')
    return sol,int(sol.nfev),bool(sol.success),True

def calc_scan(t,q,engine,co,ca,drpt,points,xi_values,rtol,atol,max_step):
    common_scale=np.maximum.reduce((np.ones(10),co['scale'],ca['scale']))
    weights=np.asarray(drpt['common_metric_scale_4d'],float)
    rows=[]; nfev=0;new_ivps=0
    refs={'original':co,'autonomous':ca}
    for label,ctx in refs.items():
        baselines=[]
        for xi in xi_values:
            ti=ctx['event']+xi
            y=np.r_[np.asarray(ctx['sol'].sol(ti),float),ctx['theta'](ti)]
            P,s=kernel_at(t,q,engine,y,ctx['kappa0'],ctx['scale'],common_scale,weights)
            baselines.append((y,P))
        for offset,kappa in zip(OFFSET_LIST,points):
            sol,n,success,isnew=variant_trajectory(engine,ctx,float(kappa),float(xi_values[-1]),rtol,atol,max_step)
            nfev+=n;new_ivps+=int(isnew)
            print(f'SCAN {label} offset={offset:+.3f} kappa={kappa:.12f} nfev={n}',flush=True)
            for i,xi in enumerate(xi_values):
                y0,P0=baselines[i]
                t_event=ctx['event']+xi
                y=np.r_[np.asarray(sol.sol(t_event),float),ctx['theta'](t_event)]
                P,s=kernel_at(t,q,engine,y,kappa,ctx['scale'],common_scale,weights)
                Pparam,_=kernel_at(t,q,engine,y0,kappa,ctx['scale'],common_scale,weights)
                full=P-P0;dp=Pparam-P0;ds=P-Pparam
                closure=float(np.linalg.norm(full-dp-ds,'fro'))
                rows.append({'seed_family':label,'offset_units':offset,'kappa':kappa,'xi':xi,
                             'projector_gap_full':float(np.linalg.norm(full,ord=2)),
                             'projector_gap_parameter_only':float(np.linalg.norm(dp,ord=2)),
                             'projector_gap_state_only':float(np.linalg.norm(ds,ord=2)),
                             'projector_full_fro':float(np.linalg.norm(full,'fro')),
                             'projector_parameter_fro':float(np.linalg.norm(dp,'fro')),
                             'projector_state_fro':float(np.linalg.norm(ds,'fro')),
                             'operator_identity_residual':closure,
                             'physical_state_delta_l2':float(np.linalg.norm(y[:10]-y0[:10])),
                             'observer_s3':float(s[2]),
                             'observer_s4':float(s[3]),'new_integrations_for_this_kappa':int(isnew),
                             'integrator_success':int(success)})
    return pd.DataFrame(rows),{'new_parameter_ivps':new_ivps,'nfev_new_ivps':nfev,'shared_scale':common_scale.tolist(),
                               'observer_weights':weights.tolist()}

def sensitivity_table(df,step):
    """Secant projector-state sensitivity proxy using full finite parameter scan.

    We compute rate variation of the *projector gap relative to the anchor*;
    it is only a scalar indicator and not the norm of dP/dkappa. The latter
    would require the actual projector arrays at neighboring kappa. The gate
    decision here is explicitly noncertifying and requires further tests.
    """
    out=[]
    for (seed,xi),f in df.groupby(['seed_family','xi']):
        f=f.sort_values('kappa')
        kk=f.kappa.to_numpy();g=f.projector_gap_full.to_numpy();
        for i in range(len(f)-1):
            k_mid=.5*(kk[i]+kk[i+1]);sec=(g[i+1]-g[i])/(kk[i+1]-kk[i])
            out.append({'seed_family':seed,'xi':xi,'kappa_mid':k_mid,'offset_mid':(f.offset_units.iloc[i]+f.offset_units.iloc[i+1])/2,
                        'slope_of_anchor_gap':sec,'abs_slope_of_anchor_gap':abs(sec)})
    return pd.DataFrame(out)

def classify(df,slopes):
    """Evaluate whether a narrow interior amplification peak is actually found.

    A pass requires an interior peak in abs scalar response-gradient >=1.2x
    both outer (offset<-0.5 and offset>1.5) controls at the final section,
    separately for both fixed seeds. A scalar peak alone still is NOT an
    activation certificate: a true band would also need a physical response
    criterion, wider windows and repeats across starts.
    """
    checks={}
    xi_last=float(df.xi.max())
    for seed in ('original','autonomous'):
        s=slopes[(slopes.seed_family==seed)&np.isclose(slopes.xi,xi_last)].sort_values('kappa_mid')
        m=s.offset_mid.to_numpy();v=s.abs_slope_of_anchor_gap.to_numpy()
        lo=v[m<=-.5];hi=v[m>=1.5]
        candidates=local_peak_candidates(m,v,min_prominence=max(.2*max(float(lo.max()),float(hi.max())),1e-12))
        supported=[{'offset':x,'value':y,'prominence':p} for x,y,p in candidates if 0<x<1 and y>=1.2*max(float(lo.max()),float(hi.max()))]
        checks[seed]={'scalar_interior_contrast_candidates':supported,'flank_max':max(float(lo.max()),float(hi.max())),
                      'slope_min':float(v.min()),'slope_max':float(v.max())}
    return checks

def graphs(df,slopes,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    final=df[np.isclose(df.xi,float(df.xi.max()))]
    fig,ax=plt.subplots(figsize=(9,5))
    for seed in ('original','autonomous'):
        f=final[final.seed_family==seed].sort_values('offset_units')
        ax.plot(f.offset_units,f.projector_gap_full,'o-',label=f'{seed}: new driven IVP')
        ax.plot(f.offset_units,f.projector_gap_parameter_only,'--',alpha=.7,label=f'{seed}: instant parameter only')
    ax.axvspan(0,1,color='0.8',alpha=.3,label='Between the two historical kappas')
    ax.set(xlabel='Normalized parameter offset (κ - κ_auto)/Δκ',ylabel='Projector distance to seed anchor',
           title='v18.50u — Driven versus instantaneous kappa scan (same seed)')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'kappa_scan_dynamic_vs_instant.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    for seed in ('original','autonomous'):
        f=final[final.seed_family==seed].sort_values('offset_units')
        ax.plot(f.offset_units,f.projector_gap_state_only,'o-',label=f'{seed}: evolved-state contribution')
    ax.axvspan(0,1,color='0.8',alpha=.3)
    ax.set(xlabel='Normalized parameter offset',ylabel='State-only contribution, operator norm',
           title='v18.50u — Same starting state, different driven trajectories')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(out/'kappa_scan_state_response.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    end=float(slopes.xi.max());
    for seed in ('original','autonomous'):
        s=slopes[(slopes.seed_family==seed)&np.isclose(slopes.xi,end)].sort_values('offset_mid')
        ax.plot(s.offset_mid,s.abs_slope_of_anchor_gap,'o-',label=seed)
    ax.axvspan(0,1,color='0.8',alpha=.3)
    ax.set(xlabel='Segment midpoint offset',ylabel='Absolute slope of distance-to-anchor versus κ',
           title='v18.50u — Narrow-band peak screening (not an activation certificate)')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(out/'kappa_sensitivity_band_screen.png',dpi=145);plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--phase-points',type=int,default=17)
    ap.add_argument('--rtol',type=float,default=1e-11)
    ap.add_argument('--atol',type=float,default=1e-12)
    ap.add_argument('--max-step',type=float,default=WINDOW/32)
    ap.add_argument('--preflight-only',action='store_true')
    a=ap.parse_args()
    if a.phase_points<9 or a.phase_points>257:raise ValueError('Unexpected grid size')
    info,code,sblob,parent=authenticate_t()
    print('AUTHENTICATED parent t',info,flush=True)
    if a.preflight_only:return
    ka=float(parent['model_kappas']['autonomous']);ko=float(parent['model_kappas']['original']);delta=ko-ka
    if not delta>0:raise RuntimeError('Bad kappa order')
    kk=ka+OFFSET_LIST*delta
    xis=np.unique(np.r_[np.linspace(0,WINDOW,a.phase_points),.00105,.001059,.001068,.001075])
    out=ROOT/'results';out.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='v18_50u_genealogy_') as tmpdir:
        t,q,p,o,engine,unit,drpt,creport,events=reconstruct_t(Path(tmpdir),code,sblob)
        co=p.make_context(o,'original',engine,unit,drpt,creport)
        ca=p.make_context(o,'autonomous',engine,unit,drpt,creport)
        df,meta=calc_scan(t,q,engine,co,ca,drpt,kk,xis,a.rtol,a.atol,a.max_step)
    slopes=sensitivity_table(df,delta)
    verdict=classify(df,slopes)
    df.to_csv(out/'fixed_seed_kappa_dynamic_scan.csv',index=False,float_format='%.17g')
    slopes.to_csv(out/'kappa_secant_response_screen.csv',index=False,float_format='%.17g')
    graphs(df,slopes,out)
    report={'version':'v18.50u','title':'Narrow-κ0 Band & Fixed-Seed Driven Projector Scan',
       'classification':'CONTROLLED_COMMON_SEED_PARAMETER_SCAN_NOT_DYNAMIC_ACTIVATION_CERTIFICATE',
       'parent_t':info,'kappa':{'autonomous':ka,'original':ko,'delta':delta,'offsets':OFFSET_LIST.tolist(),'values':kk.tolist()},
       'design':{'common_drive_shape':'beta:2:2','ramp_xi':0.24,'relative_event_window':WINDOW,
                  'phase_samples':len(xis),'fixed_seed_families':2,'new_10d_driven_ivps':meta['new_parameter_ivps'],
                  'nfev_new_ivps':meta['nfev_new_ivps'],'rows':len(df),'parameter_secants':len(slopes),
                  'rtol':a.rtol,'atol':a.atol,'max_step':a.max_step},
       'chart':{'shared_scale':meta['shared_scale'],'observer_weights':meta['observer_weights']},
       'diagnostics':{'max_operator_decomposition_residual':float(df.operator_identity_residual.max()),
                      'min_third_observer_sv':float(df.observer_s3.min()),
                      'max_fourth_observer_sv':float(df.observer_s4.max()),
                      'any_failed_integrations':int((df.integrator_success==0).any()),
                      'band_contrast_checks':verdict},
       'limitations':['A parameter sweep over 15 values includes points outside the historic kappa interval; no full Q-range scan.',
          'Each parameter IVP uses one of two fixed natural seeds and the same imposed clock; no natural state re-preparation at every κ.',
          'Distance-to-anchor and its scalar secant can show trivial V-shapes even in a smooth family; these are not physical activation scores.',
          'The observer-kernel projector is evaluated in a shared declared 10D chart, not a uniquely derived material metric.',
          'No oscillation is certified from this short time window; no bandwidth of material activation is established.',
          'Finite parameter and time grids cannot exclude narrower or more transient features.'],
       'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('v18.50u COMPLETED',json.dumps(report['diagnostics'],indent=2),flush=True)

if __name__=='__main__':main()
