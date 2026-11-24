#!/usr/bin/env python3
"""Q550 v18.51o — clock-consistent tangent kinematics & effective-force germ.

All scientific comments and outputs are in English. This audit is carried out
on authenticated v18.51e *frozen full 10D physical tangent transport* inherited
through v18.51n. It is NOT a new physical-state IVP and does NOT reconstruct
an absolute or unique generalized force from the underlying nonlinear solver.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,platform,sys,zipfile
from pathlib import Path
import numpy as np
import scipy
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
PARENT='q550_variational_metric_admissibility_observable_window_dependence_v18_51n_bundle'
E='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle'
ANCESTORS=[
 ('v18.51m','q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle'),
 ('v18.51l','q550_metric_path_continuation_directionality_survival_v18_51l_bundle'),
 ('v18.51k','q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle'),
 ('v18.51j','q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle'),
 ('v18.51i','q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle'),
 ('v18.51h','q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle'),
 ('v18.51g','q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle'),
 ('v18.51f','q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle'),
 ('v18.51e',E)]
SEEDS=('original','autonomous');TAUS=(.5,1.,2.)
EYE=np.eye(5);ZERO=np.zeros((5,5))
def sha(b):return hashlib.sha256(b).hexdigest()
def norm(a):return float(np.linalg.norm(a))
def rel(a,b):return norm(a-b)/max(1,norm(a),norm(b))
def tag(t):return ('%.1f'%t).replace('.','p')
def save_csv(name,rows):
 if not rows:raise RuntimeError('Empty CSV')
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,list(rows[0].keys()));w.writeheader();w.writerows(rows)

def verify_zip(z,root,version):
 assert z.testzip() is None,(root,'CRC')
 m=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
 o=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
 assert m['root']==o['root']==root and m['version']==o['version']==version
 for manifest,key in ((m,'files'),(o,'file_sha256')):
  for path,digest in manifest[key].items():
   assert sha(z.read(root+'/'+path))==digest,(version,path)
 return {'version':version,'source_files':len(m['files']),'result_files':len(o['file_sha256'])}

def authenticate_parent():
 parent=ROOT/'inputs'/(PARENT+'_server_sendback.zip')
 blob=parent.read_bytes();lineage=[]
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  lineage.append(verify_zip(z,PARENT,'v18.51n'))
  r=json.loads(z.read(PARENT+'/results/report.json'))
  assert r['version']=='v18.51n' and all(r['checks'].values())
  data=z.read(PARENT+'/inputs/'+ANCESTORS[0][1]+'_server_sendback.zip')
 for i,(version,root) in enumerate(ANCESTORS):
  with zipfile.ZipFile(io.BytesIO(data)) as z:
   lineage.append(verify_zip(z,root,version))
   if version=='v18.51e':
    report=json.loads(z.read(root+'/results/report.json'))
    assert all(report['scientific_checks'].values()) and report['full_10d_ivps']==2
    raw=z.read(root+'/results/material_tangent_cauchy_green_tensors.npz')
    kin=z.read(root+'/reference/kinetic_metric_v18_49h.py')
    assert sha(raw)==sha((ROOT/'inputs/material_tangent_cauchy_green_tensors_v18_51e.npz').read_bytes())
    assert sha(kin)==sha((ROOT/'reference/kinetic_metric_v18_49h.py').read_bytes())
    assert sha(kin)=='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a'
    break
   nextroot=ANCESTORS[i+1][1]
   data=z.read(root+'/inputs/'+nextroot+'_server_sendback.zip')
 return lineage,sha(parent.read_bytes()),sha(raw)

def blocks(x,B):
 """Convert position–velocity tangent dynamics to (delta Q,delta Q').

 X' = B X, X = (delta Q,delta W_tau).
 Q' = A Q + a W, a=tr(B_QW)/5.
 Y=(delta Q,delta U=delta Q') = T X.
 Y'= (T'+T B)T^-1 Y = [[0,I],[E,F]]Y.
 E=A'+a C-(a'/a)A-D A ; F=A+D+(a'/a)I.
 """
 A=B[:,:5,:5];K=B[:,:5,5:];C=B[:,5:,:5];D=B[:,5:,5:]
 a=np.trace(K,axis1=1,axis2=2)/5
 adot=CubicSpline(x,a).derivative()(x)
 Aprime=CubicSpline(x,A,axis=0).derivative()(x)
 e=Aprime+a[:,None,None]*C-(adot/a)[:,None,None]*A-np.einsum('nij,njk->nik',D,A)
 f=A+D+(adot/a)[:,None,None]*EYE
 return A,K,C,D,a,adot,Aprime,e,f

def transform(B,A,a,Aprime,adot):
 T=np.block([[EYE,ZERO],[A,a*EYE]])
 Tp=np.block([[ZERO,ZERO],[Aprime,adot*EYE]])
 return (Tp+T@B)@np.linalg.inv(T)

def synthetic_checks():
 # Multiple independent systems, including a pure changing clock and
 # a conservative potential. Each uses analytically prescribed A,a,C,D.
 t=.17;aa=1.5+.2*t;ap=.2
 examples=[]
 for case in ('clock_only','conservative','drift_and_forcing'):
  if case=='clock_only':
   A=ZERO.copy();Ap=ZERO.copy();C=ZERO.copy();D=ZERO.copy()
  elif case=='conservative':
   aa=1.;ap=0.;A=ZERO.copy();Ap=ZERO.copy()
   C=np.diag([-1.,-2.,-3.,-4.,-5.]);D=ZERO.copy()
  else:
   aa=1.7;ap=.07;A=np.zeros((5,5));A[:,4]=[.2,-.3,.4,-.5,.01];
   Ap=np.zeros((5,5));Ap[:,4]=[-.01,.02,-.03,.04,.001]
   C=np.diag([-1.,2.,-3.,4.,-5.]);D=np.diag([-.1,-.2,-.3,-.4,-.5])
  B=np.block([[A,aa*EYE],[C,D]])
  E=Ap+aa*C-(ap/aa)*A-D@A;F=A+D+(ap/aa)*EYE
  G=transform(B,A,aa,Ap,ap)
  err=rel(G,np.block([[ZERO,EYE],[E,F]]))
  examples.append(dict(case=case,max_identity_error=err,clock_only_residual=norm(E) if case=='clock_only' else None))
 assert max(x['max_identity_error'] for x in examples)<1e-13
 assert examples[0]['clock_only_residual']==0
 return examples

def static_passive_control(A,a,Aprime,ap,C,D,E,F):
 # Passive constant GL(5) on both configuration and velocity components.
 R=np.eye(5);R[0,1]=.17;R[2,4]=-.13;R[4,3]=.21
 R=R@np.diag([1.21,.91,1.07,.83,1.14]);Ri=np.linalg.inv(R)
 At=R@A@Ri;Apt=R@Aprime@Ri;Ct=R@C@Ri;Dt=R@D@Ri
 Et=Apt+a*Ct-(ap/a)*At-Dt@At
 Ft=At+Dt+(ap/a)*EYE
 return max(rel(Et,R@E@Ri),rel(Ft,R@F@Ri))

def analyze():
 OUT.mkdir(exist_ok=True)
 lineage,parent_sha,source_tensor_sha=authenticate_parent()
 with np.load(ROOT/'inputs/material_tangent_cauchy_green_tensors_v18_51e.npz',allow_pickle=False) as d:
  tensor={k:d[k].copy() for k in d.files}
 synthetic=synthetic_checks()
 ledgers=[];summary=[];quality={k:0. for k in ('scalar_kinematic_block','non_column5_position_coupling',
  'velocity_damping_skew','coordinate_transform_identity','kinematic_spline_rate','acceleration_spline_rate',
  'metric_weight_force_germ','effective_clock_weight','passive_GL5','force_derivative_finite',
  'historical_kinematic_jet')}
 global_min_a=float('inf');max_asym_E=0;max_F=0
 for seed in SEEDS:
  xi=tensor['xi_'+seed];assert xi.shape==(79,) and np.all(np.diff(xi)>0)
  baseline=None
  for tau in TAUS:
   B=tensor[f'B_{seed}_tau_{tag(tau)}']
   M=tensor[f'M_{seed}_tau_{tag(tau)}']
   A,K,C,D,a,adot,Aprime,E,F=blocks(xi,B)
   assert B.shape==M.shape==(79,10,10)
   kinematic_error=np.linalg.norm(K-a[:,None,None]*EYE,axis=(1,2))
   stray_A=np.linalg.norm(A[:,:,:4],axis=(1,2))
   damping_skew=np.linalg.norm(D-np.swapaxes(D,-1,-2),axis=(1,2))
   q=CubicSpline(xi,M,axis=0)
   Q=M[:,:5,:];U=q.derivative()(xi)[:,:5,:]
   Uexpected=np.einsum('nij,njk->nik',A,Q)+a[:,None,None]*M[:,5:,:]
   eq1=np.linalg.norm(U-Uexpected,axis=(1,2))/np.maximum(1,np.linalg.norm(U,axis=(1,2)))
   A2=q.derivative(2)(xi)[:,:5,:]
   Aexpected=np.einsum('nij,njk->nik',E,Q)+np.einsum('nij,njk->nik',F,U)
   eq2=np.linalg.norm(A2-Aexpected,axis=(1,2))/np.maximum(1,np.linalg.norm(Aexpected,axis=(1,2)))
   if baseline is None:baseline=(a*tau,E,F)
   else:
    quality['metric_weight_force_germ']=max(quality['metric_weight_force_germ'],
      max(rel(E,baseline[1]),rel(F,baseline[2])))
    quality['effective_clock_weight']=max(quality['effective_clock_weight'],rel(a*tau,baseline[0]))
   for i in range(len(xi)):
    transformed=transform(B[i],A[i],a[i],Aprime[i],adot[i])
    target=np.block([[ZERO,EYE],[E[i],F[i]]])
    te=rel(transformed,target)
    gl=static_passive_control(A[i],a[i],Aprime[i],adot[i],C[i],D[i],E[i],F[i]) if i in (1,39,78) else 0
    quality['coordinate_transform_identity']=max(quality['coordinate_transform_identity'],te)
    quality['passive_GL5']=max(quality['passive_GL5'],gl)
    skewE=norm(E[i]-E[i].T)/max(1,norm(E[i]));fn=norm(F[i]);
    global_min_a=min(global_min_a,float(a[i]));max_asym_E=max(max_asym_E,skewE);max_F=max(max_F,fn)
    ledgers.append(dict(seed_family=seed,tau_ref=tau,index=i,xi=float(xi[i]),
      effective_clock_sensitivity=float(a[i]),d_effective_clock_dxi=float(adot[i]),
      log_clock_rate=float(adot[i]/a[i]),
      clock_ratio_to_tau1=float(a[i]*tau/baseline[0][i]),
      q_w_scalar_identity_residual=float(kinematic_error[i]),
      q_q_non_fifth_column_norm=float(stray_A[i]),
      q_q_column5_norm=float(norm(A[i][:,4])),
      full_position_coupling_norm=float(norm(A[i])),
      clock_only_contribution_norm=float(norm((adot[i]/a[i])*EYE)),
      effective_force_position_jacobian_norm=float(norm(E[i])),
      effective_force_velocity_jacobian_norm=fn,
      effective_force_position_nonsymmetric_fraction=float(norm(E[i]-E[i].T)/max(1,norm(E[i]))),
      effective_force_velocity_nonsymmetric_fraction=float(norm(F[i]-F[i].T)/max(1,norm(F[i]))),
      drift_position_jacobian_time_rate_norm=float(norm(Aprime[i])),
      damping_block_skew_norm=float(damping_skew[i]),
      transformed_generator_identity_residual=te,
      finite_tangent_qprime_residual=float(eq1[i]),
      finite_tangent_qsecond_residual=float(eq2[i])))
   quality['scalar_kinematic_block']=max(quality['scalar_kinematic_block'],float(np.max(kinematic_error)))
   quality['non_column5_position_coupling']=max(quality['non_column5_position_coupling'],float(np.max(stray_A)))
   quality['velocity_damping_skew']=max(quality['velocity_damping_skew'],float(np.max(damping_skew)))
   quality['kinematic_spline_rate']=max(quality['kinematic_spline_rate'],float(np.max(eq1)))
   quality['acceleration_spline_rate']=max(quality['acceleration_spline_rate'],float(np.max(eq2)))
   summary.append(dict(seed_family=seed,tau_ref=tau,sections=len(xi),
      xi_max=float(xi[-1]),a_min=float(np.min(a)),a_max=float(np.max(a)),
      a_prime_max=float(np.max(abs(adot))),
      A_position_norm_at_end=norm(A[-1]),
      E_force_position_norm_at_end=norm(E[-1]),
      F_force_velocity_norm_at_end=norm(F[-1]),
      E_nonsymmetric_fraction_at_end=norm(E[-1]-E[-1].T)/norm(E[-1]),
      max_first_tangent_rate_residual=float(np.max(eq1)),
      max_second_tangent_rate_residual=float(np.max(eq2))))
   print(f'CLOSURE {seed}, tau_ref={tau:g}: clock a={a[1]:.12g}..{a[-1]:.12g}, '
      f'Qprime residual={max(eq1):.3e}, Qsecond residual={max(eq2):.3e}, '
      f'E skew fraction end={norm(E[-1]-E[-1].T)/norm(E[-1]):.6f}',flush=True)
 save_csv('clock_kinematic_force_germ_ledger.csv',ledgers)
 save_csv('clock_kinematic_force_germ_summary.csv',summary)
 # Chart using tau_ref=1, the actual physical Cartesian kinetic (Q,V) chart.
 sub=[r for r in ledgers if r['seed_family']=='original' and r['tau_ref']==1.]
 fig,ax=plt.subplots(figsize=(9,4.8))
 x=[r['xi'] for r in sub]
 ax.plot(x,[r['effective_clock_sensitivity'] for r in sub],label='Velocity sensitivity a(ξ)')
 ax.set(xlabel='ξ',ylabel='a(ξ)',title='Q550 v18.51o | Effective tangent clock sensitivity (not independently certified clock)')
 ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'effective_clock_sensitivity.png',dpi=145);plt.close(fig)
 fig,ax=plt.subplots(figsize=(9,5))
 ax.plot(x,[r['effective_force_position_jacobian_norm'] for r in sub],label='||E||: position Jacobian')
 ax.plot(x,[r['effective_force_velocity_jacobian_norm'] for r in sub],label='||F||: velocity Jacobian')
 ax.plot(x,[r['effective_force_position_nonsymmetric_fraction'] for r in sub],label='||E − Eᵀ|| / ||E||')
 ax.set(xlabel='ξ',ylabel='Dimensionless tangent diagnostic',title='Q550 v18.51o | Effective acceleration linearization')
 ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'effective_force_linearization.png',dpi=145);plt.close(fig)
 fig,ax=plt.subplots(figsize=(9,4.8))
 for tau in TAUS:
  st=[r for r in ledgers if r['seed_family']=='original' and r['tau_ref']==tau]
  ax.plot([r['xi'] for r in st],[r['finite_tangent_qsecond_residual'] for r in st],label=f'tau_ref={tau:g}')
 ax.set(xlabel='ξ',ylabel='Relative frozen-tangent acceleration residual',yscale='log',title='Q550 v18.51o | Second-order tangent closure check')
 ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'second_order_tangent_closure.png',dpi=145);plt.close(fig)
 checks={
  'n_through_e_ancestors_byte_authenticated':len(lineage)==10,
  'authentic_historical_kinetic_source':True,
  'two_seed_three_tau_79_sections':len(ledgers)==474 and len(summary)==6,
  'scalar_velocity_to_position_tangent':quality['scalar_kinematic_block']<1e-10,
  'rank_one_position_coupling_subspace':quality['non_column5_position_coupling']<1e-7,
  'positive_effective_clock_sensitivity':global_min_a>0,
  'kinematic_spline_independent_check':quality['kinematic_spline_rate']<1e-6,
  'second_order_spline_independent_check':quality['acceleration_spline_rate']<1e-4,
  'moving_coordinate_transform_identity':quality['coordinate_transform_identity']<1e-11,
  'tau_ref_force_germ_invariance':quality['metric_weight_force_germ']<1e-8,
  'tau_ref_effective_clock_scaling':quality['effective_clock_weight']<1e-11,
  'static_passive_configuration_chart_covariance':quality['passive_GL5']<1e-11,
  'synthetic_clock_only_not_spurious_force':synthetic[0]['clock_only_residual']==0,
  'synthetic_conservative_potential_control':synthetic[1]['max_identity_error']<1e-13,
  'synthetic_driven_force_control':synthetic[2]['max_identity_error']<1e-13,
  'nontrivial_position_to_acceleration_coupling':max_asym_E>.1,
  'nontrivial_velocity_to_acceleration_coupling':max_F>.1,
  'no_new_physical_trajectory_ivps':True,
  'no_unique_full_nonlinear_force_or_action_claimed':True,
 }
 report=dict(version='v18.51o',title='Clock-Consistent Kinematic Closure & Generalized-Force Reconstruction Audit',
 classification='NUMERICAL_AUTHENTIC_FROZEN_TANGENT_SECOND_ORDER_CLOSURE_EFFECTIVE_FORCE_JACOBIAN_ONLY',
 parent_sha256=parent_sha,inherited_e_tensor_sha256=source_tensor_sha,
 inherited_physical_ivps=2,new_physical_ivps=0,
 source_lineage=lineage,checks=checks,
 max_residuals=quality,summary=summary,synthetic_controls=synthetic,
 formal_identification={
  'state':'X=(δQ,δW_tau), W_tau=tau_ref*V; xi is inherited model clock',
  'B_blocks':'[[A, alpha I],[C,D]] with alpha(xi)=tr(B_QW)/5',
  'local_kinematics':'δQprime = A δQ + alpha δW_tau',
  'kinematic_transform':'Y=(δQ,δU=δQprime)=T X, T=[[I,0],[A,alpha I]]',
  'effective_generator':'Yprime=[[0,I],[E,F]]Y',
  'effective_force_jacobian_position':'E=A_prime+alpha*C-(alpha_prime/alpha)*A-D*A',
  'effective_force_jacobian_velocity':'F=A+D+(alpha_prime/alpha)*I',
  'effective_acceleration_germ':'δQsecond=E δQ+F δQprime',
  'clock_warning':'alpha is a local tangent velocity sensitivity, NOT an independently authenticated d(tau)/d(xi). A is nonzero.',
  'force_warning':'E,F are the frozen trajectory linearized acceleration coefficients; no nonlinear baseline force, action, or unique split is inferred.'},
 environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__),
 limitations=[
  'No new original Q550 physical state IVPs were run; source B and M derive from the authenticated v18.51e original full 10D tangent IVPs.',
  'Numerical differentiations use cubic splines on the 79 historically sampled xi sections, not a continuous independently derived analytic generator derivative.',
  'The coefficient alpha is the linearized velocity-to-position sensitivity in the moving Cartesian embedding. It alone cannot identify a global clock conversion.',
  'The observed nonzero A position coupling prevents treating Qprime=alpha V as a complete nonlinear trajectory identity.',
  'Effective acceleration Jacobians E,F do not determine the absolute generalized force without the base trajectory and its absolute accelerations.',
  'Neither nonzero E antisymmetry nor F establishes failure of all possible driven, velocity-dependent, non-natural or reparameterized actions.',
  'No intrinsic material torsion, universally preferred 10D metric, hysteresis, physical direction reversal or observer-independent energy split is certified.'])
 (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
 print('v18.51o COMPLETE',len(ledgers),'rows',sum(checks.values()),'/',len(checks),'CHECKS',flush=True)
 if not all(checks.values()):
  print(json.dumps({k:v for k,v in checks.items() if not v},indent=2));raise RuntimeError('Scientific controls failed')
 return report

if __name__=='__main__':analyze()
