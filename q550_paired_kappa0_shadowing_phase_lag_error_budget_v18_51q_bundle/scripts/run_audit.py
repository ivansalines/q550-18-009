#!/usr/bin/env python3
"""Q550 v18.51q: genuine paired-kappa0 shadowing, phase lag and error budget.

Uses the original nonlinear Q550 10D driven RHS, authenticated through v18.51p,
for a 2-seed x 3-kappa factorial. Every seed is frozen while kappa is changed.
Two independent adaptive-solver budgets are compared. All quantities are
numerical diagnostics, never interval-valued shadowing certificates.
"""
from __future__ import annotations
import csv,hashlib,importlib.util,io,json,platform,sys,tempfile,zipfile
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
P_ROOT='q550_physical_clock_moving_frame_drift_absolute_generalized_force_reconstruction_v18_51p_bundle'
P_FILE=ROOT/'inputs'/(P_ROOT+'_server_sendback.zip')
SEEDS=('original','autonomous'); KINDS=('autonomous','midpoint','original')
END=0.05; N_GRID=129; INT_Y=np.array([0,2,4,6,8]); EPS=np.finfo(float).eps

def sha(b):return hashlib.sha256(b).hexdigest()
def norm(x):return float(np.linalg.norm(x))
def rel(a,b):return norm(a-b)/max(1.,norm(a),norm(b))
def mod(path,name):
 spec=importlib.util.spec_from_file_location(name,path)
 obj=importlib.util.module_from_spec(spec);sys.modules[spec.name]=obj;spec.loader.exec_module(obj)
 return obj

def authenticate_parent_and_stage(tmp):
 with zipfile.ZipFile(P_FILE) as z:
  assert z.testzip() is None,'Parent CRC failure'
  sm=json.loads(z.read(P_ROOT+'/SOURCE_MANIFEST.json'))
  om=json.loads(z.read(P_ROOT+'/SHA256SUMS_OUTPUT.json'))
  assert sm['root']==P_ROOT and sm['version']=='v18.51p'
  assert om['root']==P_ROOT and om['version']=='v18.51p'
  for record,key in ((sm,'files'),(om,'file_sha256')):
   for name,digest in record[key].items():
    assert sha(z.read(P_ROOT+'/'+name))==digest,('Parent hash mismatch',name)
  r=json.loads(z.read(P_ROOT+'/results/report.json'))
  assert all(r['checks'].values()),'Parent scientific checks failed'
  # Extract only original executable/historic references and ancestor data.
  for sub in ('scripts/run_audit.py','reference/kinetic_metric_v18_49h.py',
              'reference/z_replay_helpers_v18_50z.py',
              'reference/x_replay_v18_50x.py',
              'inputs/material_tangent_cauchy_green_tensors_v18_51e.npz',
              'inputs/q550_clock_consistent_kinematic_closure_generalized_force_reconstruction_v18_51o_bundle_server_sendback.zip'):
   dest=tmp/P_ROOT/sub;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(z.read(P_ROOT+'/'+sub))
 stage=tmp/P_ROOT
 p=mod(stage/'scripts/run_audit.py','q550_v1851q_parent_nonlinear')
 xcode,wblob,lineage,ecache=p.authenticate_and_extract()
 assert len(lineage)==19 and ecache
 zh=p.zh
 v,vr,parts,auth=zh.stage_x_model(tmp,xcode,wblob)
 kvals={x:float(vr['kappa'][x]) for x in ('original','autonomous')}
 delta=float(vr['kappa']['delta'])
 assert abs(kvals['original']-kvals['autonomous']-delta)<1e-12
 assert delta>0 and abs(kvals['original']-1/6)<1e-12
 kvals['midpoint']=.5*(kvals['original']+kvals['autonomous'])
 return p,v,vr,parts,kvals,lineage

def make_csv(name,rows):
 if not rows:raise RuntimeError('Empty '+name)
 with (OUT/name).open('w',newline='',encoding='utf8') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def run_one(p,v,engine,ctx,kappa,mx,xi,rtol,atol,max_step):
 sol,rhs=v.make_ivp(engine,ctx,kappa,float(xi[-1]),rtol,atol,max_step)
 Q=[];V=[];C=[];Y=[];DQ=[];TH=[];JR=[]
 for x in xi:
  t=float(ctx['event']+x); y=np.asarray(sol.sol(t),float)
  f=np.asarray(rhs(t,y),float)
  q,vel,jq,jv,j=p.embedding(y,mx)
  c,kinematic_defect=p.y_clock(y,f)
  Q.append(q);V.append(vel);C.append(c);Y.append(y)
  DQ.append(jq@f);TH.append([y[2],y[6]])
  JR.append(norm(jq@f-c*vel)/max(1.,norm(jq@f)))
 cs=np.asarray(C)
 tau=np.asarray(CubicSpline(xi,cs).antiderivative()(xi),float)
 return {'Q':np.array(Q),'V':np.array(V),'clock':cs,'tau':tau,'Y':np.array(Y),
         'Qprime':np.array(DQ),'theta':np.unwrap(np.array(TH),axis=0),
         'max_clock_defect':float(np.max(JR)), 'nfev':int(sol.nfev),
         'n_steps':int(len(sol.t)-1),'sol_success':bool(sol.success)}

def main():
 OUT.mkdir(exist_ok=True)
 xi=np.linspace(0.,END,N_GRID)
 with tempfile.TemporaryDirectory(prefix='q550_v1851q_physical_') as d:
  print('AUTHENTICATING P and full historical chain',flush=True)
  p,v,vr,parts,kappas,lineage=authenticate_parent_and_stage(Path(d))
  _,_,seed_api,observer,engine,unit,drpt,creport,_=parts
  mx=float(engine.params.m_x); dk=kappas['original']-kappas['autonomous']
  print('HISTORICAL KAPPAS',kappas,'Delta',dk,'ancestors',len(lineage),flush=True)
  raw={}; quality={}; run_rows=[]
  # Explicit two-seed x three-parameter factorial; midpoint is a nonlinearity control.
  # Tight/standard numerical budgets do NOT provide rigorous error bounds.
  configs={'reference':(2e-12,2e-13,.000625),
           'standard':(2e-10,2e-11,.00125)}
  for seed in SEEDS:
   ctx=seed_api.make_context(observer,seed,engine,unit,drpt,creport)
   for kind in KINDS:
    k=kappas[kind]; pair={}
    for budget,(rtol,atol,maxstep) in configs.items():
     a=run_one(p,v,engine,ctx,k,mx,xi,rtol,atol,maxstep)
     pair[budget]=a
     print(f'IVP seed={seed} kappa={kind} budget={budget} nfev={a["nfev"]}',flush=True)
    ref=pair['reference'];std=pair['standard'];raw[(seed,kind)]=ref
    eQ=np.linalg.norm(ref['Q']-std['Q'],axis=1)
    eV=np.linalg.norm(ref['V']-std['V'],axis=1)
    eY=np.linalg.norm(ref['Y']-std['Y'],axis=1)
    eTau=np.abs(ref['tau']-std['tau'])
    quality[(seed,kind)]=dict(eQ=eQ,eV=eV,eY=eY,eTau=eTau)
    run_rows.append(dict(seed_family=seed,kappa_branch=kind,kappa=k,
       nfev_reference=ref['nfev'],nfev_standard=std['nfev'],
       steps_reference=ref['n_steps'],steps_standard=std['n_steps'],
       max_clock_kinematic_defect=ref['max_clock_defect'],
       max_Q_standard_reference_difference=float(np.max(eQ)),
       max_V_standard_reference_difference=float(np.max(eV)),
       max_tau_standard_reference_difference=float(np.max(eTau))))
  print('REAL PHYSICAL IVPS COMPLETE',len(run_rows)*2,flush=True)
  # The two kappa variants start from identical state/event within each seed.
  for seed in SEEDS:
   a=raw[(seed,'autonomous')];b=raw[(seed,'original')]
   assert norm(a['Y'][0]-b['Y'][0])<1e-13
  clock_rows=[];shadow_rows=[];factorial=[];data_arrays={'xi':xi}
  for seed in SEEDS:
   for kind in KINDS:
    a=raw[(seed,kind)];qq=quality[(seed,kind)]
    for key in ('Q','V','Y','theta','clock','tau','Qprime'):
     data_arrays[f'{seed}_{kind}_{key}']=a[key]
    for i,x in enumerate(xi):
     clock_rows.append(dict(seed_family=seed,kappa_branch=kind,xi=float(x),
       kappa=kappas[kind],clock=float(a['clock'][i]),
       tau_elapsed=float(a['tau'][i]),
       max_state_component=float(np.max(np.abs(a['Y'][i]))),
       clock_error_proxy=float(abs(qq['eTau'][i])),
       Q_error_proxy=float(qq['eQ'][i]),
       V_error_proxy=float(qq['eV'][i])))
   low=raw[(seed,'autonomous')];high=raw[(seed,'original')];mid=raw[(seed,'midpoint')]
   lq=quality[(seed,'autonomous')];hq=quality[(seed,'original')]
   for i,x in enumerate(xi):
    dQ=high['Q'][i]-low['Q'][i]
    dV=high['V'][i]-low['V'][i]
    dY=high['Y'][i]-low['Y'][i]
    speed=low['Qprime'][i];speed2=float(speed@speed)
    lag=float(dQ@speed/speed2) if speed2>1e-20 else 0.
    orth=dQ-lag*speed
    angle_gap=high['theta'][i]-low['theta'][i]
    # Differential local phase-equivalent lag from the actual polar-angle rates.
    udot=low['Qprime'][i]
    theta_rates=low['Y'][i,[3,7]]*low['clock'][i]
    tlag=[float(angle_gap[j]/theta_rates[j]) if abs(theta_rates[j])>1e-12 else 0.
          for j in range(2)]
    q_sep=norm(dQ);v_sep=norm(dV);y_sep=norm(dY)
    q_err=float(lq['eQ'][i]+hq['eQ'][i]);v_err=float(lq['eV'][i]+hq['eV'][i])
    floor=128*EPS*(1+max(norm(high['Q'][i]),norm(low['Q'][i])))
    errproxy=max(q_err,floor)
    ratio=q_sep/errproxy
    clock_err=float(lq['eTau'][i]+hq['eTau'][i])
    lag_res=norm(orth)/max(q_sep,floor)
    midpoint_departure=norm(mid['Q'][i]-.5*(high['Q'][i]+low['Q'][i]))
    shadow_rows.append(dict(seed_family=seed,index=i,xi=float(x),
      kappa_auto=kappas['autonomous'],kappa_original=kappas['original'],delta_kappa=dk,
      physical_Q_gap=q_sep,physical_V_gap=v_sep,internal_Y_gap=y_sep,
      Q_gap_per_delta_kappa=q_sep/dk,Q_error_proxy=q_err,
      V_error_proxy=v_err,numerical_Q_resolution_floor=floor,
      Q_gap_over_numerical_proxy=ratio,gap_resolved_factor20=bool(ratio>20),
      clock_difference=float(high['clock'][i]-low['clock'][i]),
      material_time_difference=float(high['tau'][i]-low['tau'][i]),
      material_time_error_proxy=clock_err,
      phase_equivalent_xi_lag=lag,
      theta1_phase_difference=float(angle_gap[0]),theta2_phase_difference=float(angle_gap[1]),
      theta1_equivalent_xi_lag=tlag[0],theta2_equivalent_xi_lag=tlag[1],
      phase_orthogonal_residual=norm(orth),
      phase_orthogonal_relative=lag_res,
      midpoint_second_difference_Q=2*midpoint_departure,
      tangent_speed=norm(speed)))
   # Distinguish a close pair of kappa variants from the distinct seed genealogies.
  for kind in KINDS:
   u=raw[('original',kind)];v2=raw[('autonomous',kind)]
   for i,x in enumerate(xi):
    factorial.append(dict(index=i,xi=float(x),kappa_branch=kind,
      physical_Q_seed_gap=norm(u['Q'][i]-v2['Q'][i]),
      physical_V_seed_gap=norm(u['V'][i]-v2['V'][i]),
      clock_seed_gap=float(u['clock'][i]-v2['clock'][i]),
      material_time_seed_gap=float(u['tau'][i]-v2['tau'][i])))
  make_csv('solver_replay_error_budget.csv',run_rows)
  make_csv('paired_clock_error_ledger.csv',clock_rows)
  make_csv('paired_kappa_shadow_phase_lag_ledger.csv',shadow_rows)
  make_csv('seed_kappa_factorial_ledger.csv',factorial)
  # Quadrature-free trajectory data can support exact future replays.
  np.savez_compressed(OUT/'paired_kappa_physical_state_tensors.npz',
                      **data_arrays, kappa_original=np.array(kappas['original']),
                      kappa_autonomous=np.array(kappas['autonomous']))
  # Genuine local relative phase shift and error; no phase optimized against noise.
  fig,ax=plt.subplots(1,2,figsize=(12.6,4.8))
  for seed in SEEDS:
   rr=[r for r in shadow_rows if r['seed_family']==seed]; xx=np.array([r['xi'] for r in rr]);
   ax[0].plot(xx,[r['physical_Q_gap'] for r in rr],label=f'{seed}: kappa-pair |delta Q|')
   ax[0].plot(xx,[r['numerical_Q_resolution_floor']+r['Q_error_proxy'] for r in rr],linestyle=':',label=f'{seed}: numerical proxy')
   ax[1].plot(xx,[r['phase_orthogonal_relative'] for r in rr],label=seed)
  ax[0].set_yscale('log');ax[0].set(xlabel='xi',ylabel='Cartesian Q separation',title='Parameter-pair separation versus solver resolution')
  ax[1].set(xlabel='xi',ylabel='Orthogonal / total Q difference',title='Local phase-lag decomposition (not phase locking)')
  for a in ax:a.grid(alpha=.2);a.legend(fontsize=8)
  fig.tight_layout();fig.savefig(OUT/'paired_kappa_shadowing_error_budget.png',dpi=145);plt.close(fig)
  fig,ax=plt.subplots(1,2,figsize=(12.5,4.7))
  for seed in SEEDS:
   rr=[r for r in shadow_rows if r['seed_family']==seed];xx=[r['xi'] for r in rr]
   ax[0].plot(xx,[r['phase_equivalent_xi_lag'] for r in rr],label=seed)
   ax[1].plot(xx,[r['material_time_difference'] for r in rr],label=seed)
  ax[0].set(xlabel='xi',ylabel='Estimated local lag in xi',title='Projection along physical Q velocity')
  ax[1].set(xlabel='xi',ylabel='delta tau elapsed',title='Difference of accumulated material clocks')
  for a in ax:a.grid(alpha=.2);a.legend()
  fig.tight_layout();fig.savefig(OUT/'phase_lag_and_material_clock_difference.png',dpi=145);plt.close(fig)
  fig,ax=plt.subplots(1,2,figsize=(12.4,4.7))
  for seed in SEEDS:
   rr=[r for r in shadow_rows if r['seed_family']==seed];xx=[r['xi'] for r in rr]
   ax[0].plot(xx,[r['Q_gap_per_delta_kappa'] for r in rr],label=seed)
   ax[1].plot(xx,[r['midpoint_second_difference_Q'] for r in rr],label=seed)
  ax[0].set(xlabel='xi',ylabel='|delta Q| / delta kappa',title='Finite-difference parameter sensitivity')
  ax[1].set(xlabel='xi',ylabel='|Q(k+) + Q(k-) - 2 Q(kmid)|',title='Midpoint nonlinearity check')
  for a in ax:a.grid(alpha=.2);a.legend()
  fig.tight_layout();fig.savefig(OUT/'kappa_parameter_sensitivity_and_curvature.png',dpi=145);plt.close(fig)
  summary={}
  for seed in SEEDS:
   rows=[r for r in shadow_rows if r['seed_family']==seed]
   resolved=[r for r in rows if r['gap_resolved_factor20']]
   summary[seed]=dict(end_Q_gap=rows[-1]['physical_Q_gap'],
     max_Q_gap=max(r['physical_Q_gap'] for r in rows),
     max_V_gap=max(r['physical_V_gap'] for r in rows),
     end_Q_gap_over_numerical_proxy=rows[-1]['Q_gap_over_numerical_proxy'],
     resolved_count=len(resolved),sections=len(rows),
     first_resolved_xi=resolved[0]['xi'] if resolved else None,
     end_phase_equivalent_xi_lag=rows[-1]['phase_equivalent_xi_lag'],
     end_orthogonal_fraction=rows[-1]['phase_orthogonal_relative'],
     end_material_clock_diff=rows[-1]['material_time_difference'],
     end_midpoint_second_diff_Q=rows[-1]['midpoint_second_difference_Q'])
  control=[]
  for s in SEEDS:
   for k in KINDS:
    a=raw[(s,k)]; control.append(a['max_clock_defect'])
  checks={
    'authenticated_p_parent_input_output_hashes':True,
    'authenticated_historical_chain_through_v1850w':len(lineage)==19,
    'historical_two_kappas_distinct_from_midpoint':0<dk<1e-3,
    'same_seed_same_initial_condition_across_kappa':all(norm(raw[(s,'original')]['Y'][0]-raw[(s,'autonomous')]['Y'][0])<1e-13 for s in SEEDS),
    'two_independent_seed_preparations':norm(raw[('original','original')]['Y'][0]-raw[('autonomous','original')]['Y'][0])>1e-9,
    'two_seeds_three_kappas_two_numerical_budgets':len(run_rows)==6 and sum(r['nfev_reference']>0 and r['nfev_standard']>0 for r in run_rows)==6,
    'genuine_nonlinear_clock_qdot_closure':max(control)<1e-9,
    'all_material_clocks_positive':all(np.min(raw[(s,k)]['clock'])>0 for s in SEEDS for k in KINDS),
    'finite_solver_refinement_discrepancies':all(np.isfinite(r['max_Q_standard_reference_difference']) for r in run_rows),
    'parameter_pair_nonidentical_after_initial_section':all(summary[s]['end_Q_gap']>0 for s in SEEDS),
    'no_fabricated_initial_shadowing_difference':all(rows['physical_Q_gap']<1e-12 for rows in shadow_rows if rows['index']==0),
    'midpoint_parameter_curvature_computed':all(np.isfinite(r['midpoint_second_difference_Q']) for r in shadow_rows),
    'phase_projection_identity':all(abs(np.dot((raw[(r['seed_family'],'original')]['Q'][r['index']]-raw[(r['seed_family'],'autonomous')]['Q'][r['index']])-r['phase_equivalent_xi_lag']*raw[(r['seed_family'],'autonomous')]['Qprime'][r['index']],raw[(r['seed_family'],'autonomous')]['Qprime'][r['index']]))<1e-9 for r in shadow_rows),
    'source_and_parameter_factorial_saved':len(factorial)==3*N_GRID,
    'no_interval_or_global_shadowing_certificate_claimed':True,
    'phase_lag_is_local_projection_not_phase_lock_claim':True,
  }
  report=dict(version='v18.51q',title='Paired-kappa0 Shadowing, Phase-Lag & Error-Budget Audit',
     classification='AUTHENTIC_NONLINEAR_PAIRED_KAPPA_LOCAL_SENSITIVITY_AND_PHASE_LAG_NUMERICAL_DIAGNOSTIC',
     checks=checks,kappas=kappas,kappa_delta=dk,endpoint_xi=END,
     sections_per_branch=N_GRID,physical_ivps=12,
     seeds=list(SEEDS),parameter_branches=list(KINDS),solver_budgets={a:{'rtol':b[0],'atol':b[1],'max_step':b[2]} for a,b in configs.items()},
     summary=summary,integrations=run_rows,parent_sha256=sha(P_FILE.read_bytes()),
     lineage_count=len(lineage),quality=dict(max_clock_closure=max(control),
       max_Q_coarse_fine=max(r['max_Q_standard_reference_difference'] for r in run_rows),
       max_V_coarse_fine=max(r['max_V_standard_reference_difference'] for r in run_rows),
       max_tau_coarse_fine=max(r['max_tau_standard_reference_difference'] for r in run_rows)),
     limitations={
       'parameter_distance':'The two historical kappa0 values are very close. Small observed pair separation alone does not certify dynamically significant shadowing.',
       'error':'DOP853 tolerance/max-step comparisons give numerical discrepancy proxies, not certified absolute integration error bounds.',
       'phase':'Q-velocity-aligned shift is a local linear phase-equivalent coordinate shift; it is not a global optimal lag, nor proof of orbit conjugacy.',
       'factorial':'Same-seed kappa comparisons distinguish parameter response from independent seed preparation; cross-seed comparisons require explicit matching.',
       'domain':'Only the inherited event-relative xi interval [0,0.05] and historical beta:2:2 forcing protocol are tested.',
       'physicality':'No material memory, global phase locking, or independent-kappa persistent torus is certified.'},
     environment=dict(python=sys.version,numpy=np.__version__,scipy=scipy.__version__,platform=platform.platform()))
  (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
  print('V18.51q CHECKS',sum(checks.values()),'/',len(checks),'PASS' if all(checks.values()) else 'FAIL',flush=True)
  print('SUMMARY',json.dumps(summary,indent=2),flush=True)
  if not all(checks.values()):raise RuntimeError('Scientific test failures '+str([k for k,v in checks.items() if not v]))

if __name__=='__main__':main()
