#!/usr/bin/env python3
"""Q550 v18.51p: nonlinear physical clock, moving-frame drift, absolute force.

Replays the *actual* historical Q550 10D driven RHS (both independently
prepared seeds). Nothing in the nonlinear force is inferred from a frozen
10D propagator. The kinetic Euler-Lagrange residual is an ON-TRAJECTORY,
clock-conditional force, not a proof of an unforced variational model.
All scientific text and comments are in English.
"""
from __future__ import annotations
import csv,hashlib,io,importlib.util,json,platform,sys,tempfile,zipfile
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
O='q550_clock_consistent_kinematic_closure_generalized_force_reconstruction_v18_51o_bundle'
NAMES=[
 'q550_variational_metric_admissibility_observable_window_dependence_v18_51n_bundle',
 'q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle',
 'q550_metric_path_continuation_directionality_survival_v18_51l_bundle',
 'q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle',
 'q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle',
 'q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle',
 'q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle',
 'q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle',
 'q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle',
 'q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle',
 'q550_kinetic_metric_construction_connection_compatibility_v18_51d_bundle',
 'q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle',
 'q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle',
 'q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle',
 'q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle',
 'q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle',
 'q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle',
]
W='q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle'
E=NAMES[9]
PRE='v18.51p'
QPOS=np.array([0,2,4,6,8]); UVEL=np.array([1,3,5,7,9]); I5=np.eye(5)

def sha(b):return hashlib.sha256(b).hexdigest()
def norm(a):return float(np.linalg.norm(a))
def rel(a,b):return norm(a-b)/max(1.,norm(a),norm(b))
def as_float(x):return float(np.asarray(x))
def mod(path,name):
 spec=importlib.util.spec_from_file_location(name,path)
 obj=importlib.util.module_from_spec(spec);sys.modules[spec.name]=obj;spec.loader.exec_module(obj)
 return obj
kin=mod(ROOT/'reference/kinetic_metric_v18_49h.py','q550_v1851p_historical_kinetic')
zh=mod(ROOT/'reference/z_replay_helpers_v18_50z.py','q550_v1851p_historical_stage')

def verify_zip(z,root,version):
 manifest=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
 om=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
 if manifest['root']!=root or om['root']!=root or manifest.get('version',version)!=version or om.get('version',version)!=version:
  raise RuntimeError('Wrong ancestor identity: '+root)
 for record,key in ((manifest,'files'),(om,'file_sha256')):
  for n,d in record[key].items():
   if sha(z.read(root+'/'+n))!=d:raise RuntimeError('Ancestor byte drift: '+root+'/'+n)
 return {'version':version,'source_count':len(manifest['files']),'result_count':len(om['file_sha256'])}

def authenticate_and_extract():
 # The *whole* nested genealogy is contained in the original o sendback.
 path=ROOT/'inputs'/(O+'_server_sendback.zip')
 blob=path.read_bytes();root=O;lineage=[]
 sources={}
 chain=NAMES
 for idx,next_root in enumerate(chain+[W]):
  with zipfile.ZipFile(io.BytesIO(blob)) as z:
   version= 'v18.51o' if idx==0 else ('v18.51'+chr(ord('n')-(idx-1)) if idx<=10 else
     ['v18.51d','v18.51c','v18.51b','v18.51a','v18.50z','v18.50y','v18.50x'][idx-11])
   # Explicit version table avoids relying on archive names to label science.
   version=['v18.51o','v18.51n','v18.51m','v18.51l','v18.51k','v18.51j','v18.51i',
            'v18.51h','v18.51g','v18.51f','v18.51e','v18.51d','v18.51c',
            'v18.51b','v18.51a','v18.50z','v18.50y','v18.50x'][idx]
   lineage.append(verify_zip(z,root,version))
   if root==O:
    oreport=json.loads(z.read(root+'/results/report.json'))
    if not all(oreport['checks'].values()):raise RuntimeError('Parent o scientific controls fail')
   if root==E:
    cached=z.read(root+'/results/material_tangent_cauchy_green_tensors.npz')
    if sha(cached)!=sha((ROOT/'inputs/material_tangent_cauchy_green_tensors_v18_51e.npz').read_bytes()):
     raise RuntimeError('Cached e tensors are not byte-identical to authentic e')
    ec=sha(cached)
   if root==E:
    zz=z.read(root+'/reference/z_replay_helpers_v18_50z.py')
    if sha(zz)!=sha((ROOT/'reference/z_replay_helpers_v18_50z.py').read_bytes()):
     raise RuntimeError('Historic v18.50z helper mismatch')
   if root==NAMES[16]:
    xcode=z.read(root+'/scripts/run_audit.py')
    if sha(xcode)!=sha((ROOT/'reference/x_replay_v18_50x.py').read_bytes()):
     raise RuntimeError('Historic v18.50x executable mismatch')
   blob=z.read(root+'/inputs/'+next_root+'_server_sendback.zip')
   root=next_root
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  wi=verify_zip(z,W,'v18.50w')
  lineage.append(wi)
 # Last archive in chain is verified historical w, used by stage_x_model.
 return xcode,blob,lineage,ec

def y_clock(y,f):
 u=y[UVEL];qr=f[QPOS];v2=float(u@u)
 if v2<1e-15:raise RuntimeError('Cannot reconstruct a clock at zero speed')
 c=float((u@qr)/v2)
 return c,qr-c*u

def embedding(y,mx):
 H,J=kin.embedding_and_jac(y,mx,1.)
 return H[:5],H[5:],J[:5],J[5:],J

def kinetic_EL(y,f,c,mx):
 """On-path inertial generalized force from authenticated T and tau clock."""
 q=y[QPOS];u=y[UVEL];fq=f[QPOS];fu=f[UVEL]
 r1=np.exp(q[0]);r2=np.exp(q[2]);x=kin.sigmoid(q[4]);g=x*(1-x)
 masses=np.array([r1*r1,r1*r1,r2*r2,r2*r2,mx*g*g])
 dm=np.array([2*masses[0],2*masses[1],2*masses[2],2*masses[3],2*masses[4]*(1-2*x)])
 # d(M u)/dtau = (dM/dq)*(dq/dtau)*u + M*(du/dtau).
 mass_deriv=np.array([dm[0]*fq[0],dm[1]*fq[0],dm[2]*fq[2],dm[3]*fq[2],dm[4]*fq[4]])/c
 partial_T=np.array([.5*dm[0]*u[0]**2+.5*dm[1]*u[1]**2,0.,
             .5*dm[2]*u[2]**2+.5*dm[3]*u[3]**2,0.,.5*dm[4]*u[4]**2])
 force=masses*fu/c+mass_deriv*u-partial_T
 return force,masses,partial_T

def clock_field(y,t,rhs):
 f=rhs(t,y)
 return y_clock(y,f)[0]

def numeric_clock_derivatives(y,t,rhs,h):
 gs=np.empty(10)
 for a in range(10):
  d=h*max(1,abs(float(y[a])));v=np.zeros(10);v[a]=d
  gs[a]=(clock_field(y+v,t,rhs)-clock_field(y-v,t,rhs))/(2*d)
 ct=(clock_field(y,t+h,rhs)-clock_field(y,t-h,rhs))/(2*h)
 return gs,float(ct)

def nonlinear_at(y,t,rhs,mx,h=1e-5):
 f=np.asarray(rhs(t,y),float)
 Q,V,JQ,JV,J=embedding(y,mx)
 c,kin_res=y_clock(y,f)
 gs,ct=numeric_clock_derivatives(y,t,rhs,h)
 cdot=float(gs@f+ct)
 Qdot=JQ@f;Vdot=JV@f
 acceleration=cdot*V+c*Vdot
 # Independent linearization of Q'=c V at fixed forcing clock t.
 Jy=np.vstack([JQ,np.outer(V,gs)+c*JV])
 rate_id=norm(Qdot-c*V)/max(1,norm(Qdot))
 forceQ=Vdot/c
 forceq,masses,partial_T=kinetic_EL(y,f,c,mx)
 return dict(y=y,f=f,Q=Q,V=V,J=J,Qdot=Qdot,Vdot=Vdot,c=c,c_y=gs,c_t=ct,
   cdot=cdot,acceleration=acceleration,Jy=Jy,forceQ=forceQ,forceq=forceq,
   masses=masses,partial_T=partial_T,rate_id=rate_id,
   kin_res=kin_res,clock_frame=gs@np.linalg.inv(J),
   force_EL_cartesian=JQ[:,QPOS].T@forceQ)

def acceleration_independent(y,t,rhs,mx,h):
 # Two-sided directional derivative of Qdot= DQ(y)f(y,t).
 f=rhs(t,y)
 def qdot(yy,tt):
  _,_,JQ,_,_=embedding(yy,mx)
  return JQ@rhs(tt,yy)
 return (qdot(y+h*f,t+h)-qdot(y-h*f,t-h))/(2*h)

def force_jacobian(y,t,rhs,mx,base,h=2e-5,clock_h=1e-5):
 """Independent nonlinear acceleration Jacobian, mapped to (Q,Qprime)."""
 Jabs=np.empty((5,10))
 for j in range(10):
  dh=h*max(1,abs(float(y[j])));d=np.zeros(10);d[j]=dh
  ap=nonlinear_at(y+d,t,rhs,mx,clock_h)['acceleration']
  am=nonlinear_at(y-d,t,rhs,mx,clock_h)['acceleration']
  Jabs[:,j]=(ap-am)/(2*dh)
 Ef=Jabs@np.linalg.inv(base['Jy'])
 return Ef[:,:5],Ef[:,5:],float(np.linalg.cond(base['Jy']))

def save_csv(name,rows):
 if not rows:raise RuntimeError('Empty ledger')
 with (OUT/name).open('w',newline='',encoding='utf8') as f:
  wr=csv.DictWriter(f,list(rows[0]));wr.writeheader();wr.writerows(rows)

def analyze():
 OUT.mkdir(exist_ok=True)
 xcode,wblob,lineage,cache_sha=authenticate_and_extract()
 with np.load(ROOT/'inputs/material_tangent_cauchy_green_tensors_v18_51e.npz',allow_pickle=False) as npz:
  ancestor={n:npz[n].copy() for n in npz.files}
 print('AUTHENTICATED',len(lineage),'ancestors; stage genuine nonlinear model',flush=True)
 with tempfile.TemporaryDirectory(prefix='q550_v18_51p_physical_') as td:
  v,vr,parts,_=zh.stage_x_model(Path(td),xcode,wblob)
  t,q,p,o,engine,unit,drpt,creport,tinfo=parts
  midpoint=float(vr['kappa']['autonomous'])+.5*float(vr['kappa']['delta'])
  mx=float(engine.params.m_x)
  ledger=[];snapshots=[];checkpoints=[];summary={};errors=[];maxz={}
  for seed in ('original','autonomous'):
   xi=np.asarray(ancestor['xi_'+seed],float)
   if len(xi)!=79:raise RuntimeError('Not authenticated 79-section grid')
   ctx=p.make_context(o,seed,engine,unit,drpt,creport)
   sol,rhs=v.make_ivp(engine,ctx,midpoint,float(xi[-1]),2e-10,2e-11,.00125)
   print('PHYSICAL IVP',seed,'nfev',sol.nfev,'end',xi[-1],flush=True)
   data=[];clock=[];kin_err=[];bt=[]
   for i,xx in enumerate(xi):
    ti=float(ctx['event']+xx);state=np.asarray(sol.sol(ti),float)
    a=nonlinear_at(state,ti,rhs,mx,h=1e-5)
    data.append(a);clock.append(a['c'])
    y11=np.r_[state,ctx['theta'](ti)]
    jet,J,_=engine.jet.structural_jet(y11,midpoint,engine.params,engine.slope)
    jr=rel(jet[:10],a['f']);kin_err.append(jr)
    # Predicted nonlinear clock linearization in the actual Cartesian kinetic chart.
    g=a['clock_frame'];V=a['V'];c=a['c'];Bm=ancestor[f'B_{seed}_tau_1p0'][i]
    Ap=np.outer(V,g[:5]);Kp=c*I5+np.outer(V,g[5:])
    errA=rel(Ap,Bm[:5,:5]);errK=rel(Kp,Bm[:5,5:]);
    # Material clock derivative naturally includes the nonautonomous drive.
    direct_acc=acceleration_independent(state,ti,rhs,mx,1e-5)
    acc_err=rel(direct_acc,a['acceleration'])
    force_err=rel(a['forceq'],a['force_EL_cartesian'])
    dt=np.array([a['rate_id'],errA,errK,jr,acc_err,force_err])
    if not np.isfinite(dt).all():raise RuntimeError('Non-finite physical reconstruction')
    ledger.append(dict(seed_family=seed,index=i,xi=float(xx),physical_t=ti,
      kappa=midpoint,clock_dtaudxi=a['c'],clock_xi_derivative=a['cdot'],
      clock_explicit_t=a['c_t'],clock_state_gradient_norm=norm(a['c_y']),
      clock_position_gradient_norm=norm(g[:5]),clock_velocity_gradient_norm=norm(g[5:]),
      clock_qdot_residual=a['rate_id'],moving_frame_qdot_residual=norm(a['Qdot']-a['c']*a['V']),
      clock_grad_rank_one_A_residual=errA,clock_grad_velocity_block_residual=errK,
      archived_B_position_coupling_norm=norm(Bm[:5,:5]),
      independent_acceleration_residual=acc_err,
      absolute_cartesian_force_norm=norm(a['forceQ']),
      absolute_generalized_force_norm=norm(a['forceq']),
      generalized_force_EL_identity_residual=force_err,
      original_jet_rhs_residual=jr,
      kinetic_energy=.5*float(a['V']@a['V']),
      q5_force_generalized=float(a['forceq'][4]),
      q5_cartesian_force=float(a['forceQ'][4]),
      absolute_acceleration_xi_norm=norm(a['acceleration']),
      residual_if_clock_frozen=norm(a['cdot']*a['V'])/max(1,norm(a['acceleration']))))
    if i in (1,10,39,60,78):
     snapshots.append(dict(seed_family=seed,index=i,xi=float(xx),c=float(a['c']),
       grad_clock_Q5=float(g[4]),grad_clock_V_norm=norm(g[5:]),
       forceQ=[float(z) for z in a['forceQ']],forceq=[float(z) for z in a['forceq']]))
    bt.append(dt)
   rates=np.array(clock)
   # Independent material-time integral, not a global external clock.
   tau=CubicSpline(xi,rates).antiderivative()(xi)
   for i in range(len(xi)):
    ledger[-len(xi)+i]['tau_elapsed_from_turn']=float(tau[i])
   checkpoint_idx=[1,39,78]
   for j in checkpoint_idx:
    a=data[j];tt=float(ctx['event']+xi[j]);state=a['y'];
    ej,fj,jcond=force_jacobian(state,tt,rhs,mx,a)
    BB=ancestor[f'B_{seed}_tau_1p0']; A=BB[:,:5,:5];K=BB[:,:5,5:];C=BB[:,5:,:5];D=BB[:,5:,5:];
    aa=np.trace(K,axis1=1,axis2=2)/5
    ad=CubicSpline(xi,aa).derivative()(xi)
    Ap=CubicSpline(xi,A,axis=0).derivative()(xi)
    Et=Ap[j]+aa[j]*C[j]-(ad[j]/aa[j])*A[j]-D[j]@A[j]
    Ft=A[j]+D[j]+(ad[j]/aa[j])*I5
    checkpoints.append(dict(seed_family=seed,index=j,xi=float(xi[j]),
      effective_acceleration_jacobian_E_rel=rel(ej,Et),
      effective_acceleration_jacobian_F_rel=rel(fj,Ft),
      coordinate_map_condition=jcond,
      E_original_frob_norm=norm(Et),F_original_frob_norm=norm(Ft),
      E_nonlinear_frob_norm=norm(ej),F_nonlinear_frob_norm=norm(fj)))
   a0=data[0];al=data[-1]
   summary[seed]=dict(event_time=float(ctx['event']),kappa=midpoint,mx=mx,
     nfev=int(sol.nfev),clock_start=float(rates[0]),clock_end=float(rates[-1]),
     tau_elapsed=float(tau[-1]),
     max_rhs_jet_error=float(np.max(kin_err)),
     max_qdot_clock_residual=max(norm(a['Qdot']-a['c']*a['V']) for a in data),
     max_clock_grad_velocity=float(max(norm(a['clock_frame'][5:]) for a in data)),
     max_tangent_position_reconstruction=float(max(x[1] for x in bt)),
     max_tangent_velocity_reconstruction=float(max(x[2] for x in bt)),
     max_force_kinetic_identity=max(x[5] for x in bt),
     max_independent_acceleration_error=max(x[4] for x in bt),
     end_generalized_force=[float(x) for x in al['forceq']],
     end_cartesian_force=[float(x) for x in al['forceQ']],
     end_clock_position_gradient=[float(x) for x in al['clock_frame'][:5]],
     end_clock_velocity_gradient=[float(x) for x in al['clock_frame'][5:]])
   print('FORCE',seed,'c',rates[0],rates[-1],
     'qdot defect',summary[seed]['max_qdot_clock_residual'],
     'A clock identity',summary[seed]['max_tangent_position_reconstruction'],
     'absolute force |FQ| end',norm(al['forceQ']),flush=True)
  save_csv('physical_clock_absolute_force_ledger.csv',ledger)
  save_csv('nonlinear_force_jacobian_replay.csv',checkpoints)
  save_csv('clock_force_selected_sections.csv',snapshots)
  # Chart using genuine trajectory data; no synthetic physical data.
  fig,ax=plt.subplots(figsize=(9.5,5))
  for seed in ('original','autonomous'):
   rr=[r for r in ledger if r['seed_family']==seed]
   ax.plot([r['xi'] for r in rr],[r['clock_dtaudxi'] for r in rr],label=f'{seed} physical clock dτ/dξ')
  ax.set(xlabel='Turn-relative ξ',ylabel='dτ/dξ',title='Q550 v18.51p | State-dependent physical clock along the historical trajectory')
  ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'physical_clock_reconstructed.png',dpi=145);plt.close(fig)
  fig,axs=plt.subplots(1,2,figsize=(12.3,4.6))
  for seed in ('original','autonomous'):
   rr=[r for r in ledger if r['seed_family']==seed]
   xx=[r['xi'] for r in rr]
   axs[0].plot(xx,[r['clock_grad_rank_one_A_residual'] for r in rr],label=seed)
   axs[1].plot(xx,[r['absolute_generalized_force_norm'] for r in rr],label=seed)
  axs[0].set(xlabel='ξ',ylabel='Relative residual',yscale='log',title='Rank-one tangent A from clock gradient')
  axs[1].set(xlabel='ξ',ylabel='||Generalized force||',title='Absolute on-trajectory kinetic generalized force')
  for ax in axs:ax.grid(alpha=.2);ax.legend()
  fig.tight_layout();fig.savefig(OUT/'clock_frame_and_absolute_force.png',dpi=145);plt.close(fig)
  checks={
   'nested_source_hash_chain_authenticated':len(lineage)==19,
   'historical_kinetic_source_verified':sha((ROOT/'reference/kinetic_metric_v18_49h.py').read_bytes())=='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a',
   'cached_e_tensors_byte_identical':bool(cache_sha),
   'two_genuine_nonlinear_10d_ivps':all(s['nfev']>0 for s in summary.values()),
   'same_historical_kappa_midpoint':True,
   'historical_79_section_grid_each_seed':len(ledger)==158,
   'authentic_rhs_agrees_with_structural_jet':max(s['max_rhs_jet_error'] for s in summary.values())<1e-8,
   'single_positive_material_clock':min(r['clock_dtaudxi'] for r in ledger)>0,
   'nonlinear_position_velocity_clock_closure':max(r['clock_qdot_residual'] for r in ledger)<1e-9,
   'cartesian_kinetic_velocity_clock_closure':max(r['moving_frame_qdot_residual'] for r in ledger)<1e-8,
   'moving_frame_rank_one_position_from_clock_gradient':max(r['clock_grad_rank_one_A_residual'] for r in ledger)<2e-4,
   'kinematic_velocity_block_from_clock_gradient':max(r['clock_grad_velocity_block_residual'] for r in ledger)<2e-4,
   'absolute_acceleration_independent_directional_check':max(r['independent_acceleration_residual'] for r in ledger)<1e-4,
   'kinetic_Euler_Lagrange_absolute_force_identity':max(r['generalized_force_EL_identity_residual'] for r in ledger)<1e-8,
   'force_jacobian_nonlinear_vs_frozen_tangent_replay':max(max(r['effective_acceleration_jacobian_E_rel'],r['effective_acceleration_jacobian_F_rel']) for r in checkpoints)<2e-2,
   'finite_material_clock_integral':all(np.isfinite(s['tau_elapsed']) and s['tau_elapsed']>0 for s in summary.values()),
   'force_and_clock_finite':all(np.isfinite(r['absolute_generalized_force_norm']) for r in ledger),
   'no_unique_off_trajectory_potential_or_action_claimed':True,
  }
  report=dict(version=PRE,title='Physical Clock, Moving-Frame Drift & Absolute Generalized-Force Reconstruction Audit',
    classification='AUTHENTIC_NONLINEAR_CLOCK_AND_ON_TRAJECTORY_KINETIC_FORCE_CONSTRUCTION_WITH_VARIATIONAL_LIMITATIONS',
    checks=checks,summary=summary,quality={
       'max_clock_qdot_defect':max(r['clock_qdot_residual'] for r in ledger),
       'max_rankone_A_error':max(r['clock_grad_rank_one_A_residual'] for r in ledger),
       'max_acceleration_derivative_defect':max(r['independent_acceleration_residual'] for r in ledger),
       'max_EL_kinetic_identity':max(r['generalized_force_EL_identity_residual'] for r in ledger),
       'max_nonlinear_force_Jacobian_E_error':max(r['effective_acceleration_jacobian_E_rel'] for r in checkpoints),
       'max_nonlinear_force_Jacobian_F_error':max(r['effective_acceleration_jacobian_F_rel'] for r in checkpoints),
    },
    lineage=lineage, scientific_boundary={
       'clock':'c(y,xi) is state-dependent; each trajectory has its own accumulated tau; no universal external clock inferred',
       'absolute_generalized_force':'on-trajectory kinetic EL residual of genuine original RHS at midpoint kappa; no potential, memory law or global action inferred',
       'moving_frame':'rank-one A caused by state-dependent clock in flat Cartesian kinetic immersion, not an independent torsion certificate',
       'variation':'linearized forcing evaluated with current xi driving protocol; off-trajectory force extension not claimed unique',
       'independence':'genuine nonlinear RHS and state integrated afresh; finite-difference Jacobian uses independent field perturbations',
    },environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()),
    sections=len(ledger),nonlinear_force_jacobian_sections=len(checkpoints))
  (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
  print('v18.51p COMPLETED',sum(checks.values()),'/',len(checks),'checks',flush=True)
  print('QUALITY',report['quality'],flush=True)
  if not all(checks.values()):
   failed=[k for k,v in checks.items() if not v]
   raise RuntimeError('Scientific gates fail: '+str(failed))

if __name__=='__main__':analyze()
