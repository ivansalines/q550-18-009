#!/usr/bin/env python3
"""v18.50z - model J10 versus observer-projector canonical transport.

All scientific source comments and output are in English.
The model jet and natural seeds come from the cryptographically authenticated
v18.50y -> x -> w -> v -> u -> t -> s -> r -> q ancestry. No response E is
used when constructing either connection. Full J10 includes shear/strain;
its orthogonal off-block K_J is a comparison convention, NOT a physical metric.
"""
from __future__ import annotations
import hashlib, io, importlib.util, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.linalg import polar

ROOT=Path(__file__).resolve().parents[1]
Y='q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle'
X='q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle'
W='q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle'
PARENT=ROOT/'inputs'/(Y+'_server_sendback.zip')


def digest(b):return hashlib.sha256(b).hexdigest()

def authenticate_one(z,root):
    assert z.testzip() is None,root+' failed CRC'
    sm=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
    assert sm['root']==root and om['root']==root
    for mp,key in ((sm,'files'),(om,'file_sha256')):
        for f,h in mp[key].items():
            if digest(z.read(root+'/'+f))!=h:raise RuntimeError(root+' SHA256 mismatch '+f)
    return {'source_files':len(sm['files']),'result_files':len(om['file_sha256'])}

def read_authenticated_data():
    with zipfile.ZipFile(PARENT) as z:
        ys=authenticate_one(z,Y)
        yr=json.loads(z.read(Y+'/results/report.json'))
        if yr['version']!='v18.50y':raise RuntimeError('Incorrect v18.50y parent')
        ydata=np.load(io.BytesIO(z.read(Y+'/results/transported_sensitivity_centerline_tensors.npz')))
        yt={k:ydata[k].copy() for k in ydata.files}
        xblob=z.read(Y+'/inputs/'+X+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(xblob)) as z:
        xs=authenticate_one(z,X)
        xr=json.loads(z.read(X+'/results/report.json'))
        if xr['version']!='v18.50x':raise RuntimeError('Incorrect v18.50x')
        xdata=np.load(io.BytesIO(z.read(X+'/results/full_projector_sensitivity_tensors.npz')))
        xt={k:xdata[k].copy() for k in xdata.files}
        xcode=z.read(X+'/scripts/run_audit.py')
        wblob=z.read(X+'/inputs/'+W+'_server_sendback.zip')
    return yt,xt,xcode,wblob,{'y':ys,'x':xs,'y_sha256':digest(PARENT.read_bytes()),'x_sha256':digest(xblob)}

def stage_x_model(root,xcode,wblob):
    stage=root/X
    (stage/'scripts').mkdir(parents=True)
    (stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(xcode)
    (stage/'inputs'/(W+'_server_sendback.zip')).write_bytes(wblob)
    spec=importlib.util.spec_from_file_location('v1850z_parent_x',stage/'scripts/run_audit.py')
    mod=importlib.util.module_from_spec(spec)
    sys.modules[spec.name]=mod
    spec.loader.exec_module(mod)
    v,vr,parts,auth=mod.authenticate_and_stage(root)
    return v,vr,parts,auth

def fn(a):return float(np.linalg.norm(a,'fro'))
def skew(a):return (a-a.T)/2
def comm(a,b):return a@b-b@a

def unit_angle(a,b):
    a=a/fn(a);b=b/fn(b)
    return float(np.degrees(2*np.arctan2(fn(a-b),fn(a+b))))

def offblock_generator(P,J):
    Q=np.eye(10)-P
    H=Q@J@P
    return H-H.T

def projector_rate_J(P,J):
    Q=np.eye(10)-P
    H=Q@J@P
    return H+H.T

def make_frame(xi,K):
    spl=CubicSpline(xi,K,axis=0)
    def rhs(t,z):
        A=skew(spl(t))
        return (A@z.reshape(10,10)).ravel()
    sol=solve_ivp(rhs,(float(xi[0]),float(xi[-1])),np.eye(10).ravel(),
        method='DOP853',rtol=2e-12,atol=2e-13,t_eval=xi,
        max_step=float(xi[-1]-xi[0])/160)
    if not sol.success or abs(sol.t[-1]-xi[-1])>1e-12:
        raise RuntimeError('Incomplete 10D frame ODE '+sol.message)
    U=sol.y.T.reshape(-1,10,10)
    return U,sol.nfev

def integrate_full_flow(xi,J_coarse,J_fine,xi_fine):
    # Two independent interpolation resolutions of the genuine model jet.
    def integrate(x,jet):
        spl=CubicSpline(x,jet,axis=0)
        def rhs(t,z):return (spl(t)@z.reshape(10,10)).ravel()
        sol=solve_ivp(rhs,(float(xi[0]),float(xi[-1])),np.eye(10).ravel(),
            method='DOP853',rtol=2e-11,atol=2e-12,
            t_eval=xi,max_step=float(xi[-1]-xi[0])/160)
        if not sol.success or abs(sol.t[-1]-xi[-1])>1e-12:raise RuntimeError('Incomplete tangent flow')
        return sol.y.T.reshape(-1,10,10),sol.nfev
    coarse,n1=integrate(xi,J_coarse)
    fine,n2=integrate(xi_fine,J_fine)
    return fine,coarse,n1,n2

def model_J(engine,ctx,ti,kappa,shared_scale,sol):
    z=np.asarray(sol.sol(ti),float)
    y=np.r_[z,ctx['theta'](ti)]
    f,J,H=engine.jet.structural_jet(y,kappa,engine.params,engine.slope)
    s=shared_scale
    out=(s[:,None]*J[:10,:10])/s[None,:]
    return out,y,J

def branch(seed,yt,xt,engine,p,o,drpt,creport,v,vr,shared_scale):
    xi=np.asarray(xt['xi'],float)
    offset=np.asarray(xt['offset_units'],float)
    idx=int(np.argmin(abs(offset-.5)))
    if abs(offset[idx]-.5)>1e-12:raise RuntimeError('Missing midpoint κ')
    kappa=float(xt['kappa'][idx])
    ctx=p.make_context(o,seed,engine,None,drpt,creport) if False else None
    return ctx

def calculate_one(seed,yt,xt,v,parts,vr):
    t,q,p,o,engine,unit,drpt,creport,tinfo=parts
    ctx=p.make_context(o,seed,engine,unit,drpt,creport)
    xi=np.asarray(xt['xi'],float)
    off=np.asarray(xt['offset_units'],float)
    ic=int(np.argmin(abs(off-.5)))
    if abs(off[ic]-.5)>1e-12:raise RuntimeError('No mid κ position')
    kappa=float(xt['kappa'][ic])
    if not np.allclose(xi,yt['xi'],rtol=0,atol=1e-14):raise RuntimeError('Time grids differ')
    P=np.asarray(xt['P_'+seed][ic],float)
    E=np.asarray(yt['E_'+seed],float)
    Ky=np.asarray(yt['K_'+seed],float)
    Uy=np.asarray(yt['U_'+seed],float)
    s=np.asarray(xt['shared_scale_10d'],float)
    # Independent same-seed physical IVP at the MIDPOINT parameter.
    sol,rhs=v.make_ivp(engine,ctx,kappa,float(xi[-1]),2e-10,2e-11,.00125)
    tt=np.asarray(ctx['event']+xi,float)
    finer=np.sort(np.unique(np.r_[xi,(xi[:-1]+xi[1:])/2]))
    JJ=[];Jfine=[];obs_res=[];rhs_res=[]
    weights=np.asarray(drpt['common_metric_scale_4d'],float)
    for idx,x in enumerate(finer):
        ti=float(ctx['event']+x)
        J,y,Jphy=model_J(engine,ctx,ti,kappa,s,sol)
        Jfine.append(J)
        if idx in (0,len(finer)//2,len(finer)-1):
            d,B,physical_J=t.physical_observer(q,engine,y,kappa,ctx['scale'],s,weights)
            Px,Kx,sv=t.basis_projector(q,B)
            nearest=int(np.argmin(abs(xi-x)))
            if abs(xi[nearest]-x)<1e-13:
                obs_res.append(fn(Px-P[nearest]))
            phys_rhs=np.asarray(rhs(ti,np.asarray(sol.sol(ti),float)),float)
            f11=np.asarray(engine.jet.structural_jet(y,kappa,engine.params,engine.slope)[0],float)
            rhs_res.append(float(np.linalg.norm(f11[:10]-phys_rhs)/max(1,np.linalg.norm(phys_rhs))))
    Jfine=np.asarray(Jfine,float)
    J=Jfine[np.searchsorted(finer,xi)]
    # The geometric transport is independent of E; the model comparator uses
    # only P and the genuine analytic tangent generator in the shared chart.
    Kdyn=np.asarray([offblock_generator(P[i],J[i]) for i in range(len(xi))])
    Pdot=CubicSpline(xi,P,axis=0).derivative()(xi)
    Kobs=np.asarray([skew(comm(Pdot[i],P[i])) for i in range(len(xi))])
    Dobs=CubicSpline(xi,E,axis=0).derivative()(xi)-np.asarray([comm(Kobs[i],E[i]) for i in range(len(xi))])
    Ddyn=CubicSpline(xi,E,axis=0).derivative()(xi)-np.asarray([comm(Kdyn[i],E[i]) for i in range(len(xi))])
    if np.max(abs(Kobs-Ky))>1e-9:raise RuntimeError('Canonical connection mismatch versus authenticated y')
    Uobs=Uy
    Udyn,nframe=make_frame(xi,Kdyn)
    Phi,Phi79,ncoarse,nfine=integrate_full_flow(xi,J,Jfine,finer)
    rows=[]
    E0=E[0]
    I=np.eye(10)
    for i,x in enumerate(xi):
        pi=P[i];j=J[i];kc=Kobs[i];km=Kdyn[i]
        obsrate=Pdot[i]
        modelrate=projector_rate_J(pi,j)
        mismatch=obsrate-modelrate
        # Full 10D tangent flow lifts the initial 7D subspace by QR.
        _,_,Vt=np.linalg.svd(P[0]);Q0=Vt[:7].T if False else np.linalg.eigh(P[0])[1][:,-7:]
        V=Phi[i]@Q0;V,_=np.linalg.qr(V)
        Pphi=V@V.T
        # Model polar part: independent deformation-induced orthogonal motion.
        Ortho,Stretch=polar(Phi[i])
        Emodel=Ortho.T@E[i]@Ortho
        Ecanon=Uobs[i].T@E[i]@Uobs[i]
        Edyn=Udyn[i].T@E[i]@Udyn[i]
        nr=fn(E[i]);aa=CubicSpline(xi,E,axis=0).derivative()(xi)[i]
        radial=np.sum(E[i]*aa)/nr
        dcanon=Dobs[i];ddyn=Ddyn[i]
        def theta_rate(d):
            perp=d-(np.sum(E[i]*d)/nr**2)*E[i]
            return fn(perp)/nr
        rows.append({'seed_family':seed,'xi':float(x),'kappa':kappa,
           'norm_J10':fn(j),'norm_K_canonical':fn(kc),'norm_K_model_crossblock':fn(km),
           'norm_connection_gap':fn(kc-km),
           'projector_rate_gap':fn(mismatch),
           'norm_Pdot_observed':fn(obsrate),'norm_Pdot_model_induced':fn(modelrate),
           'norm_E':nr,'norm_Eprime':fn(aa),'radial_growth':radial,
           'norm_D_canonical':fn(dcanon),'norm_D_model_crossblock':fn(ddyn),
           'norm_correction_canonical':fn(comm(kc,E[i])),
           'norm_correction_model':fn(comm(km,E[i])),
           'angular_rate_canonical':theta_rate(dcanon),'angular_rate_model_crossblock':theta_rate(ddyn),
           'angle_raw_deg':unit_angle(E0,E[i]),
           'angle_canonical_deg':unit_angle(E0,Ecanon),
           'angle_model_crossblock_deg':unit_angle(E0,Edyn),
           'angle_model_polar_deg':unit_angle(E0,Emodel),
           'phi_condition':float(np.linalg.cond(Phi[i])),
           'full_tangent_kernel_gap_frob':fn(pi-Pphi),
           'full_tangent_kernel_gap_op':float(np.linalg.norm(pi-Pphi,2)),
           'model_frame_orthogonality':fn(Udyn[i].T@Udyn[i]-I),
           'polar_frame_orthogonality':fn(Ortho.T@Ortho-I)})
    out=pd.DataFrame(rows)
    # Generator and projector identities (in the fixed Euclidean COMMON chart).
    ident=max(fn(Pdot[i]-comm(Kobs[i],P[i])) for i in range(len(xi)))
    # P model rate mismatch identity follows from off-block skewness.
    id2=max(fn(projector_rate_J(P[i],J[i])-comm(Kdyn[i],P[i])) for i in range(len(xi)))
    metrics={'seed':seed,'kappa':kappa,'xi_max':float(xi[-1]),
        'authentic_x_projector_max_frob':float(max(obs_res)),
        'original_driven_rhs_relative_max':float(max(rhs_res)),
        'projector_kinematics_defect_max':ident,
        'model_crossblock_identity_max':id2,
        'canonical_vs_y_K_max':float(np.max(abs(Kobs-Ky))),
        'parent_y_canonical_U_end_frob':fn(Uobs[-1].T@Uobs[-1]-I),
        'physical_ivp_nfev':int(sol.nfev),'physical_ivp_success':bool(sol.success),
        'model_jet_grid_samples':len(Jfine),'model_crossblock_frame_ivp_nfev':nframe,
        'tangent_interpolation_coarse_nfev':ncoarse,'tangent_interpolation_fine_nfev':nfine,
        'full_tangent_endpoint_coarse_fine_difference':fn(Phi[-1]-Phi79[-1]),
        'tangent_flow_finite':bool(np.isfinite(Phi).all()),
        'model_transport_convention':'K_J=(I-P)J P -P J^T(I-P), skew off-block; not full J',
        'full_model_transport_convention':'Phi prime = J10(xi) Phi; J10 is interpolated from authenticated analytic jet',
        'material_kinetic_metric':'NOT established'}
    return out,metrics,{'xi':xi,'J':J,'K_canonical':Kobs,'K_model':Kdyn,'E':E,'U_model':Udyn,'Phi':Phi}

def plot(df,out):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.5))
    for ax,seed in zip(axes,('original','autonomous')):
        d=df[df.seed_family==seed]
        ax.plot(d.xi,d.angle_raw_deg,label='fixed chart')
        ax.plot(d.xi,d.angle_canonical_deg,label='canonical P frame')
        ax.plot(d.xi,d.angle_model_crossblock_deg,label='model J crossblock frame')
        ax.plot(d.xi,d.angle_model_polar_deg,label='polar frame of full tangent Phi',linestyle='--')
        ax.set(xlabel='Evolution xi',ylabel='E angle from initial (deg)',title=seed)
        ax.grid(alpha=.25);ax.legend(fontsize=7)
    fig.suptitle('v18.50z | Same E, four independently specified frames')
    fig.tight_layout();fig.savefig(out/'sensitivity_transport_frames.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.5))
    for ax,seed in zip(axes,('original','autonomous')):
        d=df[df.seed_family==seed]
        ax.plot(d.xi,d.projector_rate_gap,label='||Pdot - Pdot_J||F')
        ax.plot(d.xi,d.norm_connection_gap,label='||Kobs - K_J||F',ls='--')
        ax.plot(d.xi,d.full_tangent_kernel_gap_frob,label='||P - P(Phi K0)||F')
        ax.set(xlabel='Evolution xi',ylabel='Normalized common-chart norm',title=seed)
        ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('v18.50z | Model tangent transports the 7D plane differently')
    fig.tight_layout();fig.savefig(out/'projector_model_vs_canonical_gap.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(11.8,4.5))
    for ax,seed in zip(axes,('original','autonomous')):
        d=df[df.seed_family==seed]
        ax.plot(d.xi,d.angular_rate_canonical,label='canonical ∇ E')
        ax.plot(d.xi,d.angular_rate_model_crossblock,label='model crossblock ∇ E')
        ax.set(xlabel='Evolution xi',ylabel='Instantaneous angular rate (rad/xi)',title=seed)
        ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('v18.50z | Sensitivity transport rates')
    fig.tight_layout();fig.savefig(out/'sensitivity_covariant_rates.png',dpi=145);plt.close(fig)

def main():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    yt,xt,xcode,wblob,parent=read_authenticated_data()
    print('AUTHENTICATED v18.50y and embedded v18.50x',parent,flush=True)
    data=[]; summaries={}; tensors={}
    with tempfile.TemporaryDirectory(prefix='v1850z_genealogy_') as tmp:
        v,vr,parts,auth=stage_x_model(Path(tmp),xcode,wblob)
        print('AUTHENTICATED MODEL ANCESTRY',auth,flush=True)
        for seed in ('original','autonomous'):
            print('REPLAY MODEL-JET CENTERLINE',seed,flush=True)
            df,checks,arrays=calculate_one(seed,yt,xt,v,parts,vr)
            data.append(df);summaries[seed]=checks
            tensors[seed]=arrays
            print('BRANCH COMPLETE',seed,'angle model J',df.angle_model_crossblock_deg.iloc[-1],
                  'Phi condition',df.phi_condition.iloc[-1],flush=True)
    df=pd.concat(data,ignore_index=True)
    if not np.isfinite(df.select_dtypes(include=[np.number]).to_numpy()).all():raise RuntimeError('Nonfinite audit values')
    if any(not summaries[s]['physical_ivp_success'] for s in summaries):raise RuntimeError('Incomplete physical IVPs')
    if max(summaries[s]['authentic_x_projector_max_frob'] for s in summaries)>1e-6:
        raise RuntimeError('Model/parent P discrepancy too large: mismatch of dynamics or phase chart')
    if max(summaries[s]['original_driven_rhs_relative_max'] for s in summaries)>1e-8:
        raise RuntimeError('Analytic structural jet does not match driven original RHS')
    if max(summaries[s]['model_crossblock_identity_max'] for s in summaries)>1e-7:
        raise RuntimeError('Model transport algebra failed')
    df.to_csv(out/'model_vs_canonical_transport_ledger.csv',index=False,float_format='%.17g')
    np.savez_compressed(out/'model_vs_canonical_centerline_tensors.npz',
       xi=tensors['original']['xi'],
       J_original=tensors['original']['J'],J_autonomous=tensors['autonomous']['J'],
       K_canonical_original=tensors['original']['K_canonical'],K_model_original=tensors['original']['K_model'],
       K_canonical_autonomous=tensors['autonomous']['K_canonical'],K_model_autonomous=tensors['autonomous']['K_model'],
       E_original=tensors['original']['E'],E_autonomous=tensors['autonomous']['E'],
       U_model_original=tensors['original']['U_model'],U_model_autonomous=tensors['autonomous']['U_model'],
       Phi_original=tensors['original']['Phi'],Phi_autonomous=tensors['autonomous']['Phi'])
    plot(df,out)
    summary={s:df[df.seed_family==s].iloc[-1].to_dict() for s in summaries}
    report={'version':'v18.50z','title':'Model-Generated Tangent Transport vs Canonical Observer Connection Audit',
            'classification':'AUTHENTICATED_MODEL_TANGENT_VS_OBSERVER_GEOMETRIC_TRANSPORT_DIAGNOSTIC_NOT_MATERIAL_CONNECTION_CERTIFICATE',
            'parent':parent,'model_replay':summaries,'endpoint':summary,
            'checks':{'rows':len(df),'branches':len(summaries),
               'max_observer_generator_kinematic_error':max(summaries[s]['projector_kinematics_defect_max'] for s in summaries),
               'max_full_tangent_interpolation_endpoint_delta':max(summaries[s]['full_tangent_endpoint_coarse_fine_difference'] for s in summaries)},
            'limitations':['All norms and polar transports use the inherited shared Euclidean 10D chart, not a certified kinetic metric.',
               'The model induced K_J is the orthogonal crossblock part of an independently computed analytic J10; it is not the full model tangent flow.',
               'The full Phi tangent flow is nonorthogonal; its polar factor depends on the chart metric.',
               'Finite 79-point J interpolation and 157-point refinement are numerical consistency checks, not interval error bounds.',
               'The canonical horizontal connection is determined by the observed P trajectory.',
               'No material-memory, physical torsion, narrow-band activation or observer-independent anisotropy certificate is claimed.'],
            'environment':{'python':platform.python_version(),'numpy':np.__version__,
                           'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,default=float)+'\n')
    print('v18.50z COMPLETED',json.dumps({'branches':len(summaries),'rows':len(df),
             'endpoint':{s:{k:v for k,v in summary[s].items() if k in
              ('angle_canonical_deg','angle_model_crossblock_deg','angle_model_polar_deg','full_tangent_kernel_gap_frob')} for s in summary}},indent=2),flush=True)

if __name__=='__main__': main()
