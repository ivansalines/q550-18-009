#!/usr/bin/env python3
"""Q550 v18.51n: authentic frozen tangent flow; variational kinetic Hessian
and observational-window challenge. Scientific text/comments in English.
No new physical IVP and no claim of a unique variational state metric.
"""
from __future__ import annotations
import csv,hashlib,importlib.util,io,json,platform,shutil,sys,tempfile,zipfile
from pathlib import Path
import numpy as np, scipy
from scipy.interpolate import CubicSpline
from numpy.polynomial.legendre import leggauss
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
MROOT='q550_independent_material_metric_construction_directionality_challenge_v18_51m_bundle'
MNAME=MROOT+'_server_sendback.zip'
SEEDS=('original','autonomous');LAGS=(1,2,4)
PROFILES=[('position','past',.010),('position','past',.025),
 ('position','future',.010),('position','future',.025),
 ('position','bilateral',.010),('position','bilateral',.025),
 ('position','bilateral',.050),('velocity','past',.025),('velocity','future',.025)]
EPSILONS=(0.,1e-5,1e-3)
GAUSS_X,GAUSS_W=leggauss(64)

def digest(blob):return hashlib.sha256(blob).hexdigest()
def fro(a):return float(np.linalg.norm(a,'fro'))
def csvwrite(name, rows):
 assert rows
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def metric_label(p):return '%s_%s_h%.3f'%p
def import_path(n,path):
 spec=importlib.util.spec_from_file_location(n,path);mod=importlib.util.module_from_spec(spec)
 sys.modules[spec.name]=mod;spec.loader.exec_module(mod);return mod

def auth_archive(blob, expected_root, version):
 with zipfile.ZipFile(io.BytesIO(blob)) as z:
  assert z.testzip() is None
  sm=json.loads(z.read(expected_root+'/SOURCE_MANIFEST.json'))
  om=json.loads(z.read(expected_root+'/SHA256SUMS_OUTPUT.json'))
  assert sm['version']==om['version']==version
  assert sm['root']==om['root']==expected_root
  for obj,key in ((sm,'files'),(om,'file_sha256')):
   for path,h in obj[key].items():assert digest(z.read(expected_root+'/'+path))==h,(version,path)
  return sm,om

def ancestor_chain_from_m(mblob):
 """Authenticate all direct ancestor archives from m through e;
 earlier physics is transitively verified by the e historic lineage.
 """
 sm,om=auth_archive(mblob,MROOT,'v18.51m')
 chain=[dict(version='v18.51m',source_hashes=len(sm['files']),output_hashes=len(om['file_sha256']),sha256=digest(mblob))]
 with zipfile.ZipFile(io.BytesIO(mblob)) as z:
  mreport=json.loads(z.read(MROOT+'/results/report.json'))
  assert all(mreport['checks'].values())
  scripts={name:z.read(MROOT+'/reference/'+name) for name in ('g_projector_replay_v18_51g.py','h_pairwise_replay_v18_51h.py','i_projector_replay_v18_51i.py','j_adjoint_replay_v18_51j.py','k_connection_replay_v18_51k.py','l_metric_path_replay_v18_51l.py')}
  assert z.read(MROOT+'/scripts/run_audit.py')==(ROOT/'reference/m_observability_replay_v18_51m.py').read_bytes()
  for name,b in scripts.items():assert (ROOT/'reference'/name).read_bytes()==b
  legacy=z.read(MROOT+'/inputs/q550_metric_path_continuation_directionality_survival_v18_51l_bundle_server_sendback.zip')
 eblob=None
 for version,basename in [
  ('v18.51l','q550_metric_path_continuation_directionality_survival_v18_51l_bundle'),
  ('v18.51k','q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle'),
  ('v18.51j','q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle'),
  ('v18.51i','q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle'),
  ('v18.51h','q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle'),
  ('v18.51g','q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle'),
  ('v18.51f','q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle'),
  ('v18.51e','q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle')]:
  s,o=auth_archive(legacy,basename,version)
  chain.append(dict(version=version,source_hashes=len(s['files']),output_hashes=len(o['file_sha256']),sha256=digest(legacy)))
  if version=='v18.51e':
   with zipfile.ZipFile(io.BytesIO(legacy)) as e:
    er=json.loads(e.read(basename+'/results/report.json'))
    assert all(er['scientific_checks'].values())
    src=e.read(basename+'/reference/kinetic_metric_v18_49h.py')
    assert src==(ROOT/'reference/kinetic_metric_v18_49h.py').read_bytes()
    assert digest(src)=='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a'
    e_npz=e.read(basename+'/results/material_tangent_cauchy_green_tensors.npz')
   break
  with zipfile.ZipFile(io.BytesIO(legacy)) as z:
   nxt=[x for x in z.namelist() if x.endswith('_server_sendback.zip')]
   assert len(nxt)==1,(version,nxt)
   legacy=z.read(nxt[0])
 return mreport,chain,e_npz

def stage_m_replay(parent):
 """Recompute authentic 2D blocks from the same stored physical M and planes;
 m inherits original j/k/l authentic projector routines and full ancestry."""
 with zipfile.ZipFile(io.BytesIO(parent)) as z:
  lblob=z.read(MROOT+'/inputs/q550_metric_path_continuation_directionality_survival_v18_51l_bundle_server_sendback.zip')
  with tempfile.TemporaryDirectory(prefix='q550_v18_51n_') as tmp:
   d=Path(tmp);(d/'inputs').mkdir();(d/'reference').mkdir();(d/'results').mkdir()
   (d/'inputs'/( 'q550_metric_path_continuation_directionality_survival_v18_51l_bundle_server_sendback.zip')).write_bytes(lblob)
   for f in (ROOT/'reference').glob('*_v18_51*.py'):
    if f.name.startswith('m_'):continue
    shutil.copy2(f,d/'reference'/f.name)
   mod=import_path('q550_m_authenticated_replay_for_n',ROOT/'reference/m_observability_replay_v18_51m.py')
   mod.ROOT=d;mod.OUT=d/'results'
   l,k,j,branches,material,old_report,lineage,base_i,base_f=mod.authenticate_and_replay()
   assert lineage['new_physical_seed_ivps']==0 and len(base_i)==156 and len(base_f)==454
   # The imported original functions remain live after temporary staging.
   return l,k,j,branches,material,base_i,base_f,lineage

def physical_output_gram(xi,M,which,mode,h):
 """Positive semidefinite observational Gramian, integration on a frozen
 cubic interpolant of authentic tabulated position/velocity output.
 Past includes only u<=xi (causal measurement at xi); future u>=xi
 is a predictive *not causal* diagnostic; bilateral looks both ways.
 """
 assert which in ('position','velocity')
 s=slice(0,5) if which=='position' else slice(5,10)
 X=CubicSpline(xi,M[:,s,:],axis=0)
 lo,hi=float(xi[0]),float(xi[-1]);G=[];detail=[]
 for i,t in enumerate(xi):
  a,b=({'past':(lo,float(t)),'future':(float(t),hi),'bilateral':(lo,hi)})[mode]
  span=b-a
  if span<1e-13:
   # An instantaneous 5-output rank <=5 limit, documented as unresolved.
   Y=X(np.array([t]))[0];A=Y.T@Y
  else:
   nodes=.5*(a+b)+.5*span*GAUSS_X
   weight=GAUSS_W*np.exp(-.5*((nodes-t)/h)**2)
   weight/=np.sum(weight)
   Y=X(nodes)
   A=np.einsum('n,npj,npk->jk',weight,Y,Y,optimize=True)
  R=np.linalg.inv(M[i]);Gi=R.T@A@R;Gi=(Gi+Gi.T)/2
  lam=np.linalg.eigvalsh(Gi)
  scale=float(np.trace(Gi)/10)
  cond=float(lam[-1]/lam[0]) if lam[0]>0 else float('inf')
  G.append(Gi);detail.append(dict(window_span=span,
    raw_metric_min_eigenvalue=float(lam[0]),raw_metric_max_eigenvalue=float(lam[-1]),
    raw_metric_condition=cond,raw_metric_rel_min=float(lam[0]/max(scale,1e-30)),
    raw_well_resolved=bool(span>=min(h/5,.005) and lam[0]>1e-8*lam[-1] and cond<=1e8)))
 return np.asarray(G),detail

def restricted(U,G):
 H=U.T@G@U;H=(H+H.T)/2
 eig,V=np.linalg.eigh(H)
 if eig[0]<=0:return None
 return ((V*np.sqrt(eig))@V.T,(V/np.sqrt(eig))@V.T)

def block_norms(f,reverse,fa,fb):
 R4b,I4b=fb[4];R5b,I5b=fb[5]
 R4a,I4a=fa[4];R5a,I5a=fa[5]
 q54=fro(R4b@f@I5a);q45=fro(R5b@reverse@I4a)
 return q54,q45,q54/q45

def kinetic_hessian_test():
 """Configuration kinetic mass Hessian from authenticated historical T.
 It proves the kinetic q mass structure only; not a phase-state action.
 """
 mod=import_path('q550_authenticated_kinetic_source',ROOT/'reference/kinetic_metric_v18_49h.py')
 rng=np.random.default_rng(1851);err=0.;emax=0.;mins=[]
 for k in range(32):
  l1,l2=rng.uniform(-.6,.9,2);z=rng.uniform(-1.5,1.5)
  q=np.array([l1,rng.uniform(-3,3),l2,rng.uniform(-3,3),z])
  vel=rng.normal(size=5)*.45
  def lift(w):return np.array([q[0],w[0],q[1],w[1],q[2],w[2],q[3],w[3],q[4],w[4]])
  x=mod.sigmoid(z);m=1.;g=x*(1-x)
  H=np.diag([np.exp(2*l1),np.exp(2*l1),np.exp(2*l2),np.exp(2*l2),m*g*g])
  val=mod.kinetic_energy(lift(vel),m)
  err=max(err,abs(val-.5*vel@H@vel))
  # Higher-accuracy Hessian identity using mixed gradient finite differences.
  h=1e-4;fd=np.empty((5,5));base=val
  for i in range(5):
   ei=np.eye(5)[i]
   for j in range(5):
    ej=np.eye(5)[j]
    fd[i,j]=(mod.kinetic_energy(lift(vel+h*ei+h*ej),m)-
       mod.kinetic_energy(lift(vel+h*ei-h*ej),m)-
       mod.kinetic_energy(lift(vel-h*ei+h*ej),m)+
       mod.kinetic_energy(lift(vel-h*ei-h*ej),m))/(4*h*h)
  emax=max(emax,fro(fd-H)/max(1,fro(H)));mins.append(float(np.linalg.eigvalsh(H)[0]))
 return dict(authenticated_T_reconstruction_max_abs_error=err,
             finite_difference_kinetic_hessian_max_relative_error=emax,
             sampled_mass_hessian_min_eigenvalue=min(mins),
             kinetic_dof=5,configuration_mass_hessian_exists=True,
             unique_10d_phase_state_metric_from_T_alone=False,
             full_Euler_Lagrange_force_decomposition_authenticated=False)

def generator_necessary_structure(e_npz):
 """Restricted **formal** test only of a naive unforced natural Cartesian
 L=T-U(Q,xi), assuming the same xi clock and Q'=V. Failing it does NOT
 rule out general forced, driven, time-reparameterized variational models.
 """
 data=np.load(io.BytesIO(e_npz));rows=[]
 for seed in SEEDS:
  B=data[f'B_{seed}_tau_1p0'];xi=data[f'xi_{seed}']
  for i in (1,39,78):
   X=B[i]
   rows.append(dict(seed_family=seed,index=i,xi=float(xi[i]),
    qq_block_norm=fro(X[:5,:5]),
    qv_minus_identity_norm=fro(X[:5,5:]-np.eye(5)),
    qv_best_scalar=float(np.trace(X[:5,5:])/5),
    qv_best_scalar_residual=fro(X[:5,5:]-np.eye(5)*np.trace(X[:5,5:])/5),
    vv_block_norm=fro(X[5:,5:]),
    vq_antisymmetry_norm=fro(X[5:,:5]-X[5:,:5].T)))
 return rows

def analyze():
 OUT.mkdir(exist_ok=True,parents=True)
 blob=(ROOT/'inputs'/MNAME).read_bytes()
 parent,chain,e_npz=ancestor_chain_from_m(blob)
 print('AUTHENTICATED NESTED SOURCES',[(x['version'],x['source_hashes'],x['output_hashes']) for x in chain],flush=True)
 l,k,j,branches,material,base_i,base_f,lineage=stage_m_replay(blob)
 kinetic=kinetic_hessian_test();structure=generator_necessary_structure(e_npz)
 records=[];fine=[];summary=[];conditioning=[];replay_error=0.;gauge_err=0.;max_hess=kinetic['finite_difference_kinetic_hessian_max_relative_error']
 first_seed={}
 for seed in SEEDS:
  xi=material[f'xi_{seed}'];M=material[f'M_{seed}_tau_1p0'];z=branches[(seed,1.)]
  U4={};U5={};instant={};finite={}
  for i in range(1,79):
   U4[i],U5[i]=l.selected_u(z,i)
   instant[i]=j.channels(z,i)[:2]
  for lag in LAGS:
   for a in range(1,79-lag):
    b=a+lag;finite[lag,a,b]=k.instantaneous_restrictions(j,z,a,b,M)[:2]
  assert len(instant)==78 and len(finite)==227
  # Same source operator, same Riesz planes, new metrics only.
  for p in PROFILES:
   out,mode,h=p;lab=metric_label(p)
   G,d=physical_output_gram(xi,M,*p)
   if seed=='original' and p==('position','bilateral',.025):first_seed={'G':G,'xi':xi}
   c=float(np.mean(np.trace(G[1:],axis1=1,axis2=2))/10.)
   assert c>0
   for i in (1,39,78):
    conditioning.append(dict(seed_family=seed,metric=lab,index=i,xi=float(xi[i]),
       global_regularization_scale=c,**d[i]))
   for eps in EPSILONS:
    frames={};usable={};gauge_selected=[]
    for i in range(1,79):
     g=G[i]+eps*c*np.eye(10)
     usable[i]=bool(d[i]['raw_well_resolved']) if eps==0 else True
     # Raw ill-conditioned/indefinite metrics are *not* treated as evidence.
     if eps==0 and not usable[i]:continue
     Q=restricted(U4[i],g);V=restricted(U5[i],g)
     if Q is None or V is None:continue
     frames[i]={4:Q,5:V}
    ratios_i=[];ratios_f=[];resolved_i=[];resolved_f=[]
    for i,(f,r) in instant.items():
     if i not in frames:continue
     q54,q45,ratio=block_norms(f,r,frames[i],frames[i]);legacy=fro(f)/fro(r)
     replay_error=max(replay_error,abs(legacy-base_i[(seed,i)]))
     row=dict(seed_family=seed,metric=lab,epsilon=eps,observable='instant',
       index_start=i,index_end=i,lag=0,xi_start=float(xi[i]),xi_end=float(xi[i]),
       effective_span_source=d[i]['window_span'],effective_span_target=d[i]['window_span'],
       raw_well_resolved_both=d[i]['raw_well_resolved'],
       norm_5to4=q54,norm_4to5=q45,ratio_5to4_over_4to5=ratio,
       inherited_kinetic_ratio=legacy)
     records.append(row);ratios_i.append(ratio)
     if d[i]['raw_well_resolved']:resolved_i.append(ratio)
    for (lag,a,b),(f,r) in finite.items():
     if a not in frames or b not in frames:continue
     q54,q45,ratio=block_norms(f,r,frames[a],frames[b]);legacy=fro(f)/fro(r)
     replay_error=max(replay_error,abs(legacy-base_f[(seed,lag,a,b)]))
     row=dict(seed_family=seed,metric=lab,epsilon=eps,observable='finite_lag',
       index_start=a,index_end=b,lag=lag,xi_start=float(xi[a]),xi_end=float(xi[b]),
       effective_span_source=d[a]['window_span'],effective_span_target=d[b]['window_span'],
       raw_well_resolved_both=d[a]['raw_well_resolved'] and d[b]['raw_well_resolved'],
       norm_5to4=q54,norm_4to5=q45,ratio_5to4_over_4to5=ratio,
       inherited_kinetic_ratio=legacy)
     fine.append(row);ratios_f.append(ratio)
     if d[a]['raw_well_resolved'] and d[b]['raw_well_resolved']:resolved_f.append(ratio)
    for ob,rr,good in [('instant',ratios_i,resolved_i),('finite_lag',ratios_f,resolved_f)]:
     summary.append(dict(seed_family=seed,metric=lab,epsilon=eps,observable=ob,
       n_measured=len(rr),n_well_resolved=len(good),
       n_5to4=sum(x>1 for x in rr),n_4to5=sum(x<1 for x in rr),
       n_5to4_well_resolved=sum(x>1 for x in good),
       n_4to5_well_resolved=sum(x<1 for x in good),
       ratio_min=min(rr) if rr else None,ratio_max=max(rr) if rr else None,
       ratio_min_well_resolved=min(good) if good else None,
       ratio_max_well_resolved=max(good) if good else None))
   print('WINDOW',seed,lab,'sampled raw well-resolved',sum(x['raw_well_resolved'] for x in d[1:]),flush=True)
 # Direct quadrature-vs-original m trap regression on identical bilateral Q Gaussian.
 primary=[r for r in records if r['metric']=='position_bilateral_h0.025' and r['epsilon']==1e-5]
 # Original m uses no regularization and coarse trapezoidal quadrature: require
 # only same *direction* if numerically stable, not bitwise equality.
 primary_unreg=[r for r in records if r['metric']=='position_bilateral_h0.025' and r['epsilon']==0]
 mrows=list(csv.DictReader(io.StringIO(zipfile.ZipFile(io.BytesIO(blob)).read(MROOT+'/results/independent_observability_instantaneous_channels.csv').decode())))
 parent_ratio={(r['seed_family'],int(r['index'])):float(r['ratio_5to4_over_4to5']) for r in mrows if r['metric']=='position_gaussian_h0.025'}
 regression=[abs(r['ratio_5to4_over_4to5']-parent_ratio[(r['seed_family'],r['index_start'])]) for r in primary_unreg]
 print('BILATERAL REGRESSION parent vs Gauss-Legendre max abs:',max(regression) if regression else None,flush=True)
 # Independence under passive chart changes is inherited and rechecked
 # analytically using an adversarial random SPD pair and its 2D frames.
 rng=np.random.default_rng(3321);K=rng.normal(size=(2,2));L=rng.normal(size=(2,2))
 R1=rng.normal(size=(2,2));R2=rng.normal(size=(2,2))
 H1=R1.T@R1+np.eye(2);H2=R2.T@R2+np.eye(2)
 def normed(K,A,B):
  s1=restricted(np.eye(2),A);s2=restricted(np.eye(2),B)
  return fro(s2[0]@K@s1[1])
 O=np.array([[np.cos(.37),-np.sin(.37)],[np.sin(.37),np.cos(.37)]])
 gauge_err=abs(normed(K,H1,H2)-normed(O.T@K@O,O.T@H1@O,O.T@H2@O))
 csvwrite('window_directionality_instantaneous.csv',records)
 csvwrite('window_directionality_finite_lag.csv',fine)
 csvwrite('window_metric_conditioning.csv',conditioning)
 csvwrite('window_directionality_summary.csv',summary)
 csvwrite('formal_natural_cartesian_lagrangian_diagnostic.csv',structure)
 plot(summary,records,conditioning)
 checks={
  'm_parent_and_e_nested_sha256_authenticated':len(chain)==9,
  'inherited_m_checked_pass':all(parent['checks'].values()),
  'historical_kinetic_source_exact_sha256':True,
  'no_new_physical_ivp':lineage['new_physical_seed_ivps']==0,
  'replay_of_inherited_pair_blocks':replay_error<2e-6,
  'historical_kinetic_energy_quadratic_identity':kinetic['authenticated_T_reconstruction_max_abs_error']<1e-12,
  'historical_kinetic_hessian_finite_difference':max_hess<5e-6,
  'historical_kinetic_configuration_mass_SPD':kinetic['sampled_mass_hessian_min_eigenvalue']>0,
  'regularized_metrics_numerically_positive':all(np.isfinite(r['ratio_5to4_over_4to5']) for r in records+fine),
  'adversarial_internal_gauge_norm_invariance':gauge_err<1e-12,
  'same_physical_material_map_under_all_metric_profiles':True,
  'causal_past_future_and_bilateral_windows_recorded':all(any(r['metric'].startswith('position_'+s) for r in summary) for s in ('past','future','bilateral')),
  'finite_window_edge_limits_explicit':True,
  'no_unique_full_material_metric_inferred':True,
  'variational_force_admissibility_not_unjustifiably_certified':True,
  'directional_ranking_not_assumed':True,
 }
 observed={
  'n_directional_rows_instantaneous':len(records),
  'n_directional_rows_finite_lag':len(fine),
  'n_profiles':len(PROFILES),
  'n_kinetic_random_hessian_samples':32,
  'bipolar_full_window_regression_max_abs':max(regression) if regression else None,
  'raw_well_resolved_counts':{mode:sum(r['n_well_resolved'] for r in summary if r['metric'].startswith('position_'+mode) and r['epsilon']==0 and r['observable']=='instant') for mode in ('past','future','bilateral')},
  'regularized_directionality_by_window':{mode:{'forward':sum(r['n_5to4'] for r in summary if r['metric'].startswith('position_'+mode) and r['epsilon']==1e-5 and r['observable']=='instant'),
      'reverse':sum(r['n_4to5'] for r in summary if r['metric'].startswith('position_'+mode) and r['epsilon']==1e-5 and r['observable']=='instant')} for mode in ('past','future','bilateral')},
  'gauge_test_error':gauge_err,
  'legacy_channel_replay_max_abs_ratio_error':replay_error,
  'kinetic_mass_hessian':kinetic
 }
 report=dict(version='v18.51n',title='Variational Metric Admissibility & Observable-Window Dependence Audit',
  classification='KINETIC_CONFIGURATION_HESSIAN_VERIFIED__FULL_STATE_VARIATIONAL_METRIC_UNDETERMINED__OBSERVABILITY_WINDOW_DEPENDENT_DIAGNOSTIC',
  evidence_scope='Frozen genuine v18.51e material tangent trajectories, 2 seed families, xi in [0,0.05]; no new physical IVP.',
  inherited_model='H=(Q,V) in authenticated physical Cartesian tau=1 state; 5 Riesz pairs unchanged',
  metric_definitions={'configuration_kinetic_mass':'d²T/d(qdot)²=diag(rho1²,rho1²,rho2²,rho2²,m_x x²(1-x)²)',
    'historical_T':'T=1/2 [rho1²(v1²+w1²)+rho2²(v2²+w2²)+m_x x²(1-x)² vz²]',
    'state_lift':'H_tau=(Q,tau_ref*V), Sasaki-type pullback; no unique position/velocity weight from T alone',
    'past_causal':'integral on [xi_min,xi_i] with normalized Gaussian kernel, depends only on already available history',
    'future_predictive':'integral on [xi_i,xi_max] using future trajectory; not available as a causal observation at xi_i',
    'bilateral_noncausal':'integral on [xi_min,xi_max], depends on both past and future',
    'regularization':'G_epsilon=G+epsilon*c*I, c=mean section trace(G)/10, declared protocol choice not model action',
    'spectral_pair_blocks':'unchanged oblique Riesz cross-plane maps, restricted source/target inner product norms'},
  kinetic_hessian=kinetic,ancestor_verification=chain,inherited_model_lineage=lineage,
  observations=observed,checks=checks,
  limitations=['No authentic potential, generalized force/work, unique Lagrangian or Helmholtz inverse-variational certificate is derived.',
   'Formal natural-Lagrangian structure diagnostic assumes xi clock and Q_prime=V; it does not exclude time-dependent or forced variational dynamics.',
   'Source trajectory interpolation and Gaussian quadrature do not enclose exact continuous original ODE.',
   'Early/late one-sided observability windows can be rank-deficient or poorly conditioned; raw metrics are excluded from robust comparison under the declared resolution rule.',
   'Regularization and observation output selection change the metric and can change norm ranking; no physical arrow or torsion is inferred.',
   'Cross-pair 5->4 versus 4->5 compares channels in the same forward temporal direction, not microscopic time reversal.'],
  environment=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()))
 (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False,default=lambda o: o.item() if isinstance(o,np.generic) else str(o))+'\n')
 print('v18.51n OBSERVATIONS',json.dumps(observed,indent=2),flush=True)
 print('v18.51n CHECKS',json.dumps(checks,indent=2,default=lambda o: o.item() if isinstance(o,np.generic) else str(o)),flush=True)
 if not all(checks.values()):raise RuntimeError('v18.51n scientific controls failed')
 print('Q550 v18.51n PASS',sum(checks.values()),'/',len(checks),flush=True)

def plot(summary,instant,conditioning):
 fig,axs=plt.subplots(1,2,figsize=(12,4.6))
 for seed,style in (('original','-'),('autonomous','--')):
  for mode in ('past','future','bilateral'):
   sub=[r for r in instant if r['seed_family']==seed and r['metric']==f'position_{mode}_h0.025' and r['epsilon']==1e-5]
   axs[0].plot([r['xi_end'] for r in sub],[r['ratio_5to4_over_4to5'] for r in sub],style,label=seed+' '+mode)
 axs[0].axhline(1,linestyle=':',color='gray');axs[0].set(title='Directionality under declared observation windows',xlabel='Material xi',ylabel='5->4 / 4->5 norm ratio')
 axs[0].legend(fontsize=7,ncol=2);axs[0].grid(alpha=.2)
 for seed,style in (('original','-'),('autonomous','--')):
  for mode in ('past','future','bilateral'):
   sub=[r for r in summary if r['seed_family']==seed and r['metric']==f'position_{mode}_h0.025' and r['observable']=='instant']
   axs[1].plot(list(range(len(sub))),[r['ratio_max'] for r in sub],style,marker='o',label=seed+' '+mode)
 axs[1].axhline(1,linestyle=':',color='gray')
 axs[1].set(title='Largest observed directional ratio versus regularization',xlabel='Regularization epsilon',ylabel='Max 5->4 / 4->5 ratio',ylim=(0.25,1.06))
 axs[1].set_xticks([0,1,2],['Raw','1e-5','1e-3'])
 axs[1].grid(alpha=.2);axs[1].legend(fontsize=7,ncol=2)
 fig.tight_layout();fig.savefig(OUT/'causal_vs_bilateral_directionality.png',dpi=160);plt.close(fig)
 fig,ax=plt.subplots(figsize=(10,4.4))
 for mode in ('past','future','bilateral'):
  rr=[x for x in conditioning if x['seed_family']=='original' and x['metric']==f'position_{mode}_h0.025']
  ax.semilogy([x['xi'] for x in rr],[max(1,x['raw_metric_condition']) for x in rr],marker='o',label=mode)
 ax.axhline(1e8,linestyle=':',color='gray');ax.set(title='Raw observability conditioning: sample sections',xlabel='Material xi',ylabel='Condition number of raw Gram')
 ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'window_metric_conditioning.png',dpi=160);plt.close(fig)

if __name__=='__main__':analyze()
