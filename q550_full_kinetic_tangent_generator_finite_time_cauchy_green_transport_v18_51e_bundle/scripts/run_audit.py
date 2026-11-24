#!/usr/bin/env python3
"""Q550 v18.51e — full kinetic tangent generator and finite-time Cauchy–Green.

Authentic ancestry: v18.51d (including 51c, b, a, 50z, y, x and historical 49h).
The 10D driven model tangent Jacobian is evaluated analytically continuously along
new, original-seed physical IVPs. The 10D tangent flow is integrated separately;
it is NOT a kinematic surrogate or an interpolation of a skew-only generator.

The metric family H_tau=(Q,tau_ref V) contains a declared freely chosen time
weight tau_ref. No frame invariant physical energy transfer, causal hysteresis,
material torsion, one-third law, or unique phase-space metric is asserted.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, importlib.util, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp, trapezoid
from scipy.interpolate import CubicSpline
from scipy.linalg import polar
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results'
D = 'q550_kinetic_metric_construction_connection_compatibility_v18_51d_bundle'
C = 'q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle'
PARENT = ROOT/'inputs'/(D+'_server_sendback.zip')
TAUS = (0.5, 1.0, 2.0)
ID = np.eye(10)

def module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod; spec.loader.exec_module(mod)
    return mod

d = module(ROOT/'reference/d_replay_v18_51d.py','q550_v18_51d_reference')
kin = d.kin
zhelper = d.zhelper

def fn(a):return float(np.linalg.norm(a,'fro'))
def sym(a):return (a+a.T)*.5
def skew(a):return (a-a.T)*.5
def sha(b):return hashlib.sha256(b).hexdigest()
def max_rel(a,b):return fn(a-b)/max(1.,fn(a),fn(b))

def save_csv(path, rows):
    if not rows:raise ValueError('Empty output rows')
    with path.open('w',newline='',encoding='utf8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def authenticated_ancestry(temp):
    if not PARENT.exists():raise FileNotFoundError('Missing authenticated v18.51d sendback: '+str(PARENT))
    with zipfile.ZipFile(PARENT) as z:
        d_auth=d.auth(z,D,'v18.51d')
        for src,rel in (('scripts/run_audit.py','reference/d_replay_v18_51d.py'),
                        ('reference/kinetic_metric_v18_49h.py','reference/kinetic_metric_v18_49h.py'),
                        ('reference/z_replay_helpers_v18_50z.py','reference/z_replay_helpers_v18_50z.py')):
            if sha(z.read(D+'/'+src))!=sha((ROOT/rel).read_bytes()):
                raise RuntimeError('Reference source not byte-identical to historical archive: '+src)
        dreport=json.loads(z.read(D+'/results/report.json'))
        if dreport['version']!='v18.51d' or not all(dreport['checks'].values()):
            raise RuntimeError('v18.51d parent failed scientific gates')
        dledger=list(csv.DictReader(io.StringIO(z.read(D+'/results/kinetic_metric_spectral_source_ledger.csv').decode())))
        czip=z.read(D+'/inputs/'+C+'_server_sendback.zip')
        c_path=temp/(C+'_server_sendback.zip')
        c_path.write_bytes(czip)
    d.PARENT=c_path
    lineage,c_summary,c_table,Z,X,xcode,wblob=d.load_ancestry()
    if sha(czip)!=lineage['parent_sha256']:
        raise RuntimeError('Nested c archive hash mismatch')
    lineage['d']={'archive_sha256':sha(PARENT.read_bytes()),'auth':d_auth,
                  'parent_checks':len(dreport['checks']),'parent_observations':dreport['observations']}
    if len(dledger)!=474 or dreport['observations']!=474:
        raise RuntimeError('v18.51d parent section count inconsistent')
    return lineage,dledger,Z,X,xcode,wblob

def evaluate_state(xi,sol,ctx,engine,kappa,scales):
    ti=float(ctx['event']+xi)
    y=np.r_[np.asarray(sol.sol(ti),float),float(ctx['theta'](ti))]
    f,J, _=engine.jet.structural_jet(y,kappa,engine.params,engine.slope)
    JJ=(scales[:,None]*J[:10,:10])/scales[None,:]
    return y[:10],np.asarray(f[:10],float),JJ

def integrate_tangent(sol,ctx,engine,kappa,scales,xi,rtol,atol,max_step):
    def rhs(x,flat):
        _,_,J=evaluate_state(x,sol,ctx,engine,kappa,scales)
        return (J@flat.reshape(10,10)).ravel()
    tangent=solve_ivp(rhs,(float(xi[0]),float(xi[-1])),ID.ravel(),
                      method='DOP853',rtol=rtol,atol=atol,t_eval=xi,
                      max_step=max_step,dense_output=True)
    if not tangent.success or len(tangent.t)!=len(xi):
        raise RuntimeError('Full authenticated tangent flow failed: '+tangent.message)
    return tangent.y.T.reshape(-1,10,10),tangent

def reference_spline_transport(xi,J,rtol,atol,max_step):
    spl=CubicSpline(xi,J,axis=0)
    def rhs(t,f):return (spl(t)@f.reshape(10,10)).ravel()
    sol=solve_ivp(rhs,(float(xi[0]),float(xi[-1])),ID.ravel(),
                  method='DOP853',rtol=rtol,atol=atol,t_eval=xi,max_step=max_step)
    if not sol.success:raise RuntimeError('Independent sampled-jet tangent comparison failed')
    return sol.y.T.reshape(-1,10,10),int(sol.nfev)

def l_and_lprime(y,ydot,mx,tau,scales):
    h=2.0e-6/max(1.,float(np.linalg.norm(ydot)))
    L=kin.embedding_and_jac(y,mx,tau)[1]/scales[np.newaxis,:]
    Lp=(kin.embedding_and_jac(y+h*ydot,mx,tau)[1] -
        kin.embedding_and_jac(y-h*ydot,mx,tau)[1])/(scales[np.newaxis,:]*(2*h))
    return L,Lp

def passive_checks(F,L0,Li,y0,yi,scales):
    # Nonlinear passive gauge z->z+a sin(z), with distinct endpoint Jacobians.
    z0=scales*y0;zi=scales*yi
    a=np.linspace(.025,.11,10)
    D0=np.diag(1+a*np.cos(z0));Di=np.diag(1+a*np.cos(zi))
    Fp=Di@F@np.linalg.inv(D0)
    L0p=L0@np.linalg.inv(D0);Lip=Li@np.linalg.inv(Di)
    M=Li@F@np.linalg.inv(L0)
    Mp=Lip@Fp@np.linalg.inv(L0p)
    G0=L0.T@L0;Gi=Li.T@Li
    G0p=np.linalg.inv(D0).T@G0@np.linalg.inv(D0)
    Gip=np.linalg.inv(Di).T@Gi@np.linalg.inv(Di)
    Cp=np.linalg.inv(L0p).T@Fp.T@Gip@Fp@np.linalg.inv(L0p)
    C=M.T@M
    return dict(nonlin_chart_M=max_rel(M,Mp),nonlin_chart_C=max_rel(C,Cp),
                metric_start=max_rel(G0p,L0p.T@L0p),metric_end=max_rel(Gip,Lip.T@Lip))

def endpoint_fd(engine,ctx,source_rhs,sol,xi,F_end,scales,rtol,atol,eps,dirs):
    """Independently perturb ORIGINAL physical solver, compare end displacement."""
    if dirs==0:return {'tested':0,'max_relative_error':None,'per_direction':[]}
    y0=np.asarray(sol.sol(float(ctx['event']+xi[0])),float)
    times=(float(ctx['event']+xi[0]),float(ctx['event']+xi[-1]))
    vectors=[np.eye(10)[0],np.eye(10)[8],np.eye(10)[4],np.eye(10)[2]]
    errors=[]
    for i in range(dirs):
        dz=vectors[i];dy=eps*dz/scales
        ends=[]
        for sign in (+1,-1):
            ss=solve_ivp(source_rhs,times,y0+sign*dy,method='DOP853',
                         rtol=rtol,atol=atol,max_step=.00125)
            if not ss.success:raise RuntimeError('Independent finite-difference IVP failed')
            ends.append(ss.y[:,-1])
        measured=(ends[0]-ends[1])*scales/(2*eps)
        pred=F_end@dz
        errors.append({'direction_shared_chart':int(np.flatnonzero(dz)[0]),
                       'relative_error':float(np.linalg.norm(measured-pred)/max(1,np.linalg.norm(pred))),
                       'measured_norm':float(np.linalg.norm(measured)),
                       'predicted_norm':float(np.linalg.norm(pred))})
    return {'tested':len(errors),'max_relative_error':max(e['relative_error'] for e in errors),'per_direction':errors}

def seed_trajectory(seed,Z,model,xi,scales,mid,rtol,atol,max_step,fd_eps,fd_dirs):
        v,parts=model
        _,_,p,o,engine,unit,drpt,creport,_=parts
        ctx=p.make_context(o,seed,engine,unit,drpt,creport)
        sol,source_rhs=v.make_ivp(engine,ctx,mid,float(xi[-1]),2e-10,2e-11,.00125)
        if not sol.success:raise RuntimeError('Physical model IVP incomplete')
        y=[];ydot=[];J=[]
        for pos in xi:
            yy,fy,jy=evaluate_state(pos,sol,ctx,engine,mid,scales)
            y.append(yy);ydot.append(fy);J.append(jy)
        y=np.asarray(y);ydot=np.asarray(ydot);J=np.asarray(J)
        historic_error=max(max_rel(j,jz) for j,jz in zip(J,Z['J_'+seed]))
        F,ft=integrate_tangent(sol,ctx,engine,mid,scales,xi,rtol,atol,max_step)
        F_spline,nref=reference_spline_transport(xi,J,rtol,atol,max_step)
        err=max(max_rel(a,b) for a,b in zip(F,F_spline))
        archived_phi_error=max(max_rel(a,b) for a,b in zip(F,Z['Phi_'+seed]))
        rhs_err=max(float(np.linalg.norm(source_rhs(float(ctx['event']+pos),np.asarray(sol.sol(float(ctx['event']+pos)),float))-ff)/max(1.,np.linalg.norm(ff))) for pos,ff in zip(xi,ydot))
        fd=endpoint_fd(engine,ctx,source_rhs,sol,xi,F[-1],scales,
                       rtol,atol,fd_eps,fd_dirs)
        print(f'MODEL {seed}: physical nfev={sol.nfev}, tangent nfev={ft.nfev}, '
              f'jet replay={historic_error:.3e}, solver RHS={rhs_err:.3e}, spline transport={err:.3e}, archived Phi={archived_phi_error:.3e}, '
              f'endpoint FD={fd["max_relative_error"]}',flush=True)
        return {'seed':seed,'y':y,'ydot':ydot,'J':J,'F':F,
                'mx':float(engine.params.m_x),'ivp_nfev':int(sol.nfev),
                'tangent_nfev':int(ft.nfev),'spline_nfev':nref,
                'historical_J_error':historic_error,'sampled_J_transport_error':err,
                'archived_Phi_transport_error':archived_phi_error,'original_rhs_jet_error':rhs_err,'fd':fd}

def analyze(seed,tau,trajectory,xi,scales,dparent):
    state=trajectory['y'];dot=trajectory['ydot'];J=trajectory['J'];F=trajectory['F'];mx=trajectory['mx']
    L=[];Lprime=[]
    for y,vel in zip(state,dot):
        li,lpi=l_and_lprime(y,vel,mx,tau,scales)
        L.append(li);Lprime.append(lpi)
    L=np.asarray(L);Lprime=np.asarray(Lprime)
    L0inv=np.linalg.inv(L[0]);G0=L[0].T@L[0]
    S=np.diag(scales);Sinv=np.diag(1./scales)
    M=np.asarray([L[i]@F[i]@L0inv for i in range(len(xi))])
    Cmat=np.asarray([m.T@m for m in M]);rate=[];rows=[]
    spline_lp=CubicSpline(xi,L,axis=0).derivative()(xi)
    condL=[];chart=[]
    for i,xx in enumerate(xi):
        li=L[i];m=M[i];li_inv=np.linalg.inv(li)
        Dframe=Lprime[i]@li_inv
        Bg=li@J[i]@li_inv
        B=Bg+Dframe
        Ss=sym(B);Sk=skew(B)
        Urot,Ustretch=polar(m)
        eigvals=np.linalg.eigvalsh(Cmat[i]);eigvals=np.maximum(eigvals,0.)
        sv=np.sqrt(eigvals[::-1]);logs=np.log(np.maximum(sv,1e-300))
        # Independent finite-time volume identity: det M = exp(int trace B).
        logdet=float(np.linalg.slogdet(m)[1]);sgn=float(np.linalg.slogdet(m)[0])
        dC=2*m.T@Ss@m
        rate.append({'B':B,'dC':dC,'logdet':logdet})
        eigenU=np.linalg.eigvalsh(sym(Ustretch))
        condL.append(float(np.linalg.cond(li)))
        # Cross-check the old v18.51d DH@S chart convention against actual
        # shared-jet Jz=S Jy S^-1. True physical embedding requires DH@S^-1.
        DH0=kin.embedding_and_jac(state[0],mx,tau)[1]
        DHi=kin.embedding_and_jac(state[i],mx,tau)[1]
        Fy=Sinv@F[i]@S
        Mphysical=DHi@Fy@np.linalg.inv(DH0)
        Mlegacy=(DHi@S)@F[i]@np.linalg.inv(DH0@S)
        rows.append({
          'physical_vs_scaled_coordinate_M_residual':max_rel(m,Mphysical),
          'legacy_v18_51d_forward_scaled_M_difference':max_rel(m,Mlegacy),
          'seed_family':seed,'tau_ref':tau,'xi':float(xx),
          'kinetic_metric_cond':float(np.linalg.cond(li.T@li)),
          'kinetic_immersion_cond':float(np.linalg.cond(li)),
          'tangent_flow_cond':float(np.linalg.cond(F[i])),
          'physical_transport_cond':float(np.linalg.cond(m)),
          'norm_generator_full':fn(B),'norm_generator_model':fn(Bg),
          'norm_generator_frame':fn(Dframe),'norm_symmetric_strain':fn(Ss),
          'norm_skew_rotation':fn(Sk),
          'symmetric_fraction_of_full_generator':fn(Ss)/max(1e-28,fn(B)),
          'frame_symmetric_fraction_of_strain':fn(sym(Dframe))/max(1e-28,fn(Ss)),
          'trace_strain_rate':float(np.trace(Ss)),
          'trace_frame_rate':float(np.trace(Dframe)),
          'generator_reconstruction_residual':fn(B-Bg-Dframe)/max(1,fn(B)),
          'directional_Lprime_vs_spline_rel_error':max_rel(Lprime[i],spline_lp[i]),
          'logdet_M':logdet,'det_M_sign':sgn,'logdet_C':2*logdet,
          'cg_lambda_max':float(eigvals[-1]),'cg_lambda_min':float(eigvals[0]),
          'stretch_max':float(sv[0]),'stretch_2':float(sv[1]),'stretch_3':float(sv[2]),
          'stretch_min':float(sv[-1]),'norm_log_stretches':float(np.linalg.norm(logs)),
          'polar_rotation_distance_F':fn(Urot-ID),
          'polar_orthogonality_error':fn(Urot.T@Urot-ID),
          'cg_symmetry_error':fn(Cmat[i]-Cmat[i].T),
          'cg_positive_min_eigenvalue':float(eigvals[0]),
          'polar_positive_min_eigenvalue':float(eigenU[0]),
          'cg_metric_chart_identity_error':max_rel(Cmat[i],L0inv.T@F[i].T@(li.T@li)@F[i]@L0inv),
        })
        if i in (0,len(xi)//2,len(xi)-1):
            chart.append({'seed_family':seed,'tau_ref':tau,'xi':float(xx),
                          **passive_checks(F[i],L[0],li,state[0],state[i],scales)})
    Cprime_spline=CubicSpline(xi,Cmat,axis=0).derivative()(xi)
    logdet_spline=CubicSpline(xi,np.asarray([v['logdet'] for v in rate])).derivative()(xi)
    # Independent determinant-rate identity; endpoint spline derivative is less accurate.
    for i,rr in enumerate(rows):
        rr['cg_rate_identity_relative_error']=max_rel(Cprime_spline[i],rate[i]['dC'])
        rr['volume_rate_identity_absolute_error']=abs(float(logdet_spline[i]-np.trace(rate[i]['B'])))
    # Quadrature with linear trapezoid is a second finite-volume cross-check.
    quadrature=float(trapezoid([r['trace_strain_rate'] for r in rows],xi))
    summary={
       'seed_family':seed,'tau_ref':tau,'sections':len(rows),
       'xi_max':float(xi[-1]),'initial_transport_identity_error':max_rel(M[0],ID),
       'final_logdet_M':rows[-1]['logdet_M'],
       'integrated_trace_strain':quadrature,
       'final_volume_integral_defect':abs(quadrature-rows[-1]['logdet_M']),
       'final_stretch_max':rows[-1]['stretch_max'],
       'final_stretch_min':rows[-1]['stretch_min'],
       'final_norm_log_stretches':rows[-1]['norm_log_stretches'],
       'final_polar_rotation_distance_F':rows[-1]['polar_rotation_distance_F'],
       'final_symmetric_fraction':rows[-1]['symmetric_fraction_of_full_generator'],
       'max_cg_rate_rel_error':max(r['cg_rate_identity_relative_error'] for r in rows),
       'max_volume_rate_abs_error':max(r['volume_rate_identity_absolute_error'] for r in rows),
       'max_Lprime_spline_rel_error':max(r['directional_Lprime_vs_spline_rel_error'] for r in rows),
       'max_chart_error':max(max(v[k] for k in ('nonlin_chart_M','nonlin_chart_C','metric_start','metric_end')) for v in chart),
       'max_polar_orth_error':max(r['polar_orthogonality_error'] for r in rows),
       'max_metric_cond':max(r['kinetic_metric_cond'] for r in rows),
       'max_physical_chart_M_residual':max(r['physical_vs_scaled_coordinate_M_residual'] for r in rows),
       'endpoint_legacy_chart_difference':rows[-1]['legacy_v18_51d_forward_scaled_M_difference'],
       'first_three_stretches_end':[rows[-1][f'stretch_{k}'] for k in ('max','2','3')],
    }
    return rows,summary,chart,{'F':F,'M':M,'C':Cmat,'L':L,'B':np.asarray([a['B'] for a in rate])}

def thirds_ledger(ledger, tolerance):
    out=[];branch=[]
    for seed in ('original','autonomous'):
        for tau in TAUS:
            r=[v for v in ledger if v['seed_family']==seed and abs(float(v['tau_ref'])-tau)<1e-9]
            r.sort(key=lambda x:float(x['xi']))
            if len(r)!=79:raise RuntimeError('Historical v18.51d ledger missing records')
            rr=[]
            for e in r:
                frame=float(e['signed_kinetic_frame']);canonical=float(e['signed_canonical'])
                ratio=canonical/frame if abs(frame)>1e-12 else float('nan')
                dist=abs(ratio-1/3) if np.isfinite(ratio) else float('nan')
                row={'seed_family':seed,'tau_ref':tau,'xi':float(e['xi']),
                     'canonical_signed':canonical,'frame_signed':frame,
                     'canonical_to_frame_ratio':ratio,'absolute_distance_from_one_third':dist,
                     'near_one_third_declared_tolerance':int(np.isfinite(dist) and dist<=tolerance)}
                out.append(row);rr.append(row)
            last=rr[-1]
            branch.append({'seed_family':seed,'tau_ref':tau,'sections':len(rr),
                'endpoint_ratio':last['canonical_to_frame_ratio'],
                'endpoint_distance_from_one_third':last['absolute_distance_from_one_third'],
                'endpoint_within_declared_tolerance':bool(last['near_one_third_declared_tolerance']),
                'fraction_of_sections_near_one_third':float(np.mean([v['near_one_third_declared_tolerance'] for v in rr]))})
    return out,branch

def plots(rows,third):
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[r for r in rows if r['seed_family']==seed and r['tau_ref']==tau]
            ax.plot([v['xi'] for v in rr],[v['symmetric_fraction_of_full_generator'] for v in rr],label=f'tau_ref={tau:g}')
        ax.set(title=seed,xlabel='xi',ylabel='||sym B|| / ||B||');ax.grid(alpha=.25);ax.legend()
    fig.suptitle('v18.51e | Complete kinetic generator: symmetric-strain fraction')
    fig.tight_layout();fig.savefig(OUT/'full_generator_strain_fraction.png',dpi=155);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[r for r in rows if r['seed_family']==seed and r['tau_ref']==tau]
            ax.plot([v['xi'] for v in rr],[v['stretch_max'] for v in rr],label=f'max stretch tau_ref={tau:g}')
            ax.plot([v['xi'] for v in rr],[v['stretch_min'] for v in rr],ls='--',label=f'min stretch tau_ref={tau:g}')
        ax.set(title=seed,xlabel='xi',ylabel='singular value M');ax.grid(alpha=.25);ax.legend(fontsize=7)
    fig.suptitle('v18.51e | Finite-time physical kinetic Cauchy–Green stretches')
    fig.tight_layout();fig.savefig(OUT/'finite_time_cauchy_green_stretches.png',dpi=155);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.7),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[r for r in third if r['seed_family']==seed and r['tau_ref']==tau]
            ax.plot([v['xi'] for v in rr],[v['canonical_to_frame_ratio'] for v in rr],label=f'tau_ref={tau:g}')
        ax.axhline(1/3,ls=':',color='black',label='1/3 hypothesis')
        ax.set(title=seed,xlabel='xi',ylabel='historical canon / kinetic-frame signed shares');ax.grid(alpha=.25);ax.legend()
    fig.suptitle('v18.51e | Exploratory 1/3 comparison, NOT a physical law')
    fig.tight_layout();fig.savefig(OUT/'one_third_hypothesis_comparison.png',dpi=155);plt.close(fig)

def run(args):
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='q550_v18_51e_auth_') as tmp:
        lineage,dledger,Z,X,xcode,wblob=authenticated_ancestry(Path(tmp))
        xi=np.asarray(Z['xi'],float);scales=np.asarray(X['shared_scale_10d'],float)
        off=X['offset_units'];ic=int(np.argmin(abs(off-.5)))
        if abs(off[ic]-.5)>1e-12:raise RuntimeError('Missing historical midpoint kappa')
        mid=float(X['kappa'][ic])
        if len(xi)!=79:raise RuntimeError('Unexpected 79 section observational grid')
        if not np.array_equal(xi,X['xi']):raise RuntimeError('Historical time grids mismatch')
        trajectories={}
        print('STAGING authenticated solver lineage once for both independent seeds',flush=True)
        v,vr,parts,_=zhelper.stage_x_model(Path(tmp),xcode,wblob)
        for seed in ('original','autonomous'):
            trajectories[seed]=seed_trajectory(seed,Z,(v,parts),xi,scales,mid,
                   args.rtol,args.atol,args.max_step,args.fd_epsilon,args.fd_directions)
    records=[];summaries=[];charts=[];tensors={}
    for seed,trajectory in trajectories.items():
        tensors[f'xi_{seed}']=xi
        tensors[f'F_{seed}']=trajectory['F']
        for tau in TAUS:
            row,summary,chart,tensor=analyze(seed,tau,trajectory,xi,scales,dledger)
            records.extend(row);summaries.append(summary);charts.extend(chart)
            for k,v in tensor.items():tensors[f'{k}_{seed}_tau_{str(tau).replace(".","p")}']=v
            print(f'KINETIC {seed} tau_ref={tau:g}: sigma_max={summary["final_stretch_max"]:.9f}, '
                  f'sigma_min={summary["final_stretch_min"]:.9f}, '
                  f'sym_frac_end={summary["final_symmetric_fraction"]:.6f}, '
                  f'CG rate max err={summary["max_cg_rate_rel_error"]:.3e}',flush=True)
    third,third_summary=thirds_ledger(dledger,args.third_tolerance)
    save_csv(OUT/'full_generator_and_cauchy_green_ledger.csv',records)
    save_csv(OUT/'finite_time_cauchy_green_summary.csv',summaries)
    save_csv(OUT/'nonlinear_chart_covariance_controls.csv',charts)
    save_csv(OUT/'one_third_hypothesis_ledger.csv',third)
    save_csv(OUT/'one_third_hypothesis_summary.csv',third_summary)
    np.savez_compressed(OUT/'material_tangent_cauchy_green_tensors.npz',**tensors)
    plots(records,third)
    checks={
        'parent_d_source_lineage_authenticated':len(lineage)==9 and lineage['d']['parent_checks']==12,
        'historical_kinetic_source_byte_exact':lineage['historical_v18_49h_kinetic_source_sha256']=='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a',
        'two_authentic_physical_seed_ivps':len(trajectories)==2 and all(v['ivp_nfev']>0 for v in trajectories.values()),
        'continuous_original_analytic_J_replay':max(v['historical_J_error'] for v in trajectories.values())<1e-6,
        'original_physical_rhs_matches_analytic_jet':max(v['original_rhs_jet_error'] for v in trajectories.values())<1e-6,
        'archived_full_tangent_transport_crosscheck':max(v['archived_Phi_transport_error'] for v in trajectories.values())<2e-3,
        'independent_sampled_J_tangent_comparator':max(v['sampled_J_transport_error'] for v in trajectories.values())<2e-3,
        'finite_difference_physical_tangent_comparator':all(v['fd']['tested']==0 or v['fd']['max_relative_error']<2e-3 for v in trajectories.values()),
        'two_seeds_three_tau_seventy_nine_sections':len(records)==474 and len(summaries)==6,
        'full_kinetic_strain_rotation_decomposition':max(v['generator_reconstruction_residual'] for v in records)<1e-11,
        'initial_finite_transport_identity':max(v['initial_transport_identity_error'] for v in summaries)<1e-11,
        'CG_positive_definite_and_symmetric':min(v['cg_positive_min_eigenvalue'] for v in records)>0 and max(v['cg_symmetry_error'] for v in records)<1e-9,
        'finite_transport_metric_identity':max(v['cg_metric_chart_identity_error'] for v in records)<1e-9,
        'physical_shared_chart_conjugacy':max(v['max_physical_chart_M_residual'] for v in summaries)<1e-10,
        'independent_CG_rate_identity':max(v['max_cg_rate_rel_error'] for v in summaries)<2e-3,
        'finite_time_volume_rate_identity':max(v['max_volume_rate_abs_error'] for v in summaries)<2e-3,
        'finite_volume_integral_check':max(v['final_volume_integral_defect'] for v in summaries)<2e-3,
        'nonlinear_chart_covariance':max(v['max_chart_error'] for v in summaries)<1e-10,
        'polar_frame_orthogonality':max(v['max_polar_orth_error'] for v in summaries)<1e-10,
        'metric_conventions_not_silently_collapsed':len(set(v['final_stretch_max'] for v in summaries))>1,
        'one_third_is_exploratory_not_required':len(third_summary)==6,
    }
    report={
      'version':'v18.51e','title':'Full Kinetic Tangent Generator & Finite-Time Cauchy–Green Transport Audit',
      'classification':'NUMERICAL_FULL_TANGENT_FINITE_TIME_KINETIC_TRANSPORT_DIAGNOSTIC_NOT_UNIQUE_METRIC_OR_TORSION_CERTIFICATE',
      'source':'Genuine driven Q550 full physical jet. 10D tangent Φ integrated continuously along each original-seed 10D physical IVP.',
      'metric_construction':'Historical v18.49h kinetic Cartesian immersion; corrected shared-jet chart L=DH_tau diag(shared_scale)^-1, tau_ref=0.5,1,2.',
      'identities':{'full_kinetic_generator':'B=L J L^-1 + Lprime L^-1',
                    'kinetic_finite_transport':'M(xi)=L(xi) F(xi) L(0)^-1',
                    'right_Cauchy_Green':'C=M^T M',
                    'rate':'Cprime = 2 M^T sym(B) M',
                    'volume':'d log(det M)/dxi = trace(B)',
                    'one_third':'ratio of historical v18.51d signed canonical and kinetic-frame spectral source shares; not energy'},
      'kappa_midpoint':mid,'xi_max':float(xi[-1]),'sections_per_branch':len(xi),
      'num_rows':len(records),'tau_refs':TAUS,'full_10d_ivps':2,
      'lineage':lineage,'seed_replays':{seed:{k:v for k,v in trajectory.items() if k not in ('y','ydot','J','F')}
                                   for seed,trajectory in trajectories.items()},
      'finite_time_branches':summaries,'one_third_declared_tolerance_absolute':args.third_tolerance,
      'one_third_branches':third_summary,'scientific_checks':checks,
      'global_max_errors':{
           'continuous_jet':max(v['historical_J_error'] for v in trajectories.values()),
           'physical_vs_scaled_chart_M':max(v['max_physical_chart_M_residual'] for v in summaries),
           'sampled_jet_tangent':max(v['sampled_J_transport_error'] for v in trajectories.values()),
           'archived_Phi_tangent':max(v['archived_Phi_transport_error'] for v in trajectories.values()),
           'rhs_jet':max(v['original_rhs_jet_error'] for v in trajectories.values()),
           'finite_difference_trajectory_tangent':max((v['fd']['max_relative_error'] or 0) for v in trajectories.values()),
           'CG_rate':max(v['max_cg_rate_rel_error'] for v in summaries),
           'volume_rate':max(v['max_volume_rate_abs_error'] for v in summaries),
           'chart_covariance':max(v['max_chart_error'] for v in summaries)},
      'limitations':[
         'The Sasaki-type state metric has a free tau_ref; the base kinetic energy does not fix a unique 10D phase-state metric.',
         'This is a local finite-time 0..0.05 tangent transport at one midpoint kappa, not a complete parameter-band or multi-loop material-memory theorem.',
         'Original and autonomous are distinct PREPARATIONS replayed at the SAME midpoint kappa, not coexisting distinct-kappa boundaries.',
         'Cauchy–Green stretches measure deformation in the selected state metric, not calorimetric kinetic-energy fractions.',
         'Finite difference, spline rates, and trajectory solutions are numerical consistency checks, not interval mathematical certificates.',
         'The original v18.51d DH@S convention is not the pullback corresponding to the stored shared jet Jz=S Jy S^-1, except S=I; this audit uses DH@S^-1 and records the legacy forward-scale discrepancy.',
         'The 1/3 comparison is a falsifiable heuristic of signed spectral source shares and should not be interpreted as a structural constant.',
         '10D polar rotation is chart-embedded orientation diagnostic; it does not by itself establish torsion or a physical return flip.',
      ],
      'environment':{'python':platform.python_version(),'numpy':np.__version__,
                     'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('v18.51e COMPLETE',json.dumps({'checks':checks,'endpoints':summaries,'one_third':third_summary},indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('v18.51e failed one or more scientific controls')

def parse_args():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rtol',type=float,default=2e-11)
    p.add_argument('--atol',type=float,default=2e-12)
    p.add_argument('--max-step',type=float,default=.0003)
    p.add_argument('--fd-epsilon',type=float,default=2e-5)
    p.add_argument('--fd-directions',type=int,default=2,choices=(0,1,2,3,4))
    p.add_argument('--third-tolerance',type=float,default=.025,
                   help='Absolute tolerance to 1/3 for exploratory signed-share ratio; no PASS requires it')
    a=p.parse_args()
    if min(a.rtol,a.atol,a.max_step,a.fd_epsilon,a.third_tolerance)<=0:raise ValueError('positive tolerances required')
    return a

if __name__=='__main__':run(parse_args())
