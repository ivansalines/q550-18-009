#!/usr/bin/env python3
"""Q550 v18.50t — Paired-kappa phase-aligned edge motion and projector separation.

The authenticated v18.50s sendback is an immutable provenance ancestor.
Two genuine, separately prepared driven Q550 trajectories are replayed, and
analytic first derivatives of the normalized 4D structural observer are
compared on a common physical 10D chart. No response vectors are used for
fitting. All scientific source comments are in English.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
S='q550_principal_angle_conditioning_tangent_integrator_convergence_v18_50s_bundle'
R='q550_differential_kernel_invariance_analytic_tangent_generator_v18_50r_bundle'
Q='q550_analytic_observer_jacobian_nullspace_projector_transport_v18_50q_bundle'
P='q550_near_null_tangent_direction_stencil_order_transport_v18_50p_bundle'
SFILE=ROOT/'inputs'/(S+'_server_sendback.zip')

def sha(b):return hashlib.sha256(b).hexdigest()

def authenticate_s():
    with zipfile.ZipFile(SFILE) as z:
        if z.testzip() is not None:raise RuntimeError('Parent s ZIP CRC error')
        sm=json.loads(z.read(S+'/SOURCE_MANIFEST.json'))
        om=json.loads(z.read(S+'/SHA256SUMS_OUTPUT.json'))
        if sm['root']!=S or om['root']!=S:raise RuntimeError('Parent root mismatch')
        for manifest,key in ((sm,'files'),(om,'file_sha256')):
            for rel,h in manifest[key].items():
                if sha(z.read(S+'/'+rel))!=h:raise RuntimeError('Parent source/result SHA256 mismatch: '+rel)
        report=json.loads(z.read(S+'/results/report.json'))
        script=z.read(S+'/scripts/run_audit.py')
        rblob=z.read(S+'/inputs/'+R+'_server_sendback.zip')
    if report['version']!='v18.50s' or report['counts']['complete_tangent_integrations']!=24:
        raise RuntimeError('Unexpected 50s scientific parent')
    return {'sha256':sha(SFILE.read_bytes()),'source_count':len(sm['files']),
            'result_count':len(om['file_sha256']),'completed_integrations':24},script,rblob

def dynamic_model_stage(tmp,s_script,r_blob):
    stage=tmp/S;(stage/'scripts').mkdir(parents=True);(stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(s_script)
    (stage/'inputs'/(R+'_server_sendback.zip')).write_bytes(r_blob)
    spec=importlib.util.spec_from_file_location('q550_v18_50t_parent_s',stage/'scripts/run_audit.py')
    s=importlib.util.module_from_spec(spec);sys.modules[spec.name]=s;spec.loader.exec_module(s)
    info,rscript,qblob,rreport,qprior=s.authenticate_r()
    r=s.stage_r(tmp,rscript,qblob)
    ri,qscript,pblob,qreport,old=r.authenticate_q()
    q=r.stage_q(tmp,qscript,pblob)
    pi,pscript,oblob,_,_=q.authenticate_parent()
    p=q.stage_p(pscript,oblob,tmp)
    o,p,engine,unit,drpt,creport,events=q.stage_model(p,tmp)
    return q,r,p,o,engine,unit,drpt,creport,events

def physical_observer(q,engine,y,kappa,branch_scale,common_scale,observable_weights):
    f,j,h=engine.jet.structural_jet(y,kappa,engine.params,engine.slope)
    d,Bbranch,_,_=q.analytic_structural_observer_jet(f,j,h,observable_weights,branch_scale)
    # The branch Jacobian is d(observer)/d(branch_scale * physical_state).
    # Convert it to a shared chart, z_i = common_scale_i * physical_state_i.
    Bshared=Bbranch*branch_scale[None,:]/common_scale[None,:]
    return d,Bshared,j

def basis_projector(q,B):
    P,K,s,rank=q.projector(B,rtol=1e-9)
    if rank!=3:raise RuntimeError('Observer rank != 3')
    return P,K,s

def pair_geometry(Pa,Ka,Pb,Kb):
    # Stable sin of largest principal angle; avoid acos near 1.
    I=np.eye(Pa.shape[0]);sin=float(np.linalg.svd((I-Pa)@Kb,compute_uv=False)[0])
    sop=float(np.linalg.svd(Pa-Pb,compute_uv=False)[0])
    other=np.linalg.svd((I-Pa)@Kb,compute_uv=False)
    return {'projector_op_gap':sop,'projector_fro_gap':float(np.linalg.norm(Pa-Pb,'fro')),
       'max_principal_angle_deg':float(np.degrees(np.arcsin(np.clip(sin,0,1)))),
       'second_principal_angle_deg':float(np.degrees(np.arcsin(np.clip(other[1],0,1)))),
       'third_principal_angle_deg':float(np.degrees(np.arcsin(np.clip(other[2],0,1)))),
       'angle_identity_abs_res':abs(sin-sop)}

def entry_at(q,engine,ctx,kappa,xi,branch_scale,common_scale,weights):
    t=ctx['event']+xi
    z=np.asarray(ctx['sol'].sol(t),float)
    y=np.r_[z,ctx['theta'](t)]
    d,B,J=physical_observer(q,engine,y,kappa,branch_scale,common_scale,weights)
    Pa,Ka,s=basis_projector(q,B)
    return {'y':y,'d':d,'P':Pa,'K':Ka,'s':s,'B':B,'J':J,'t':t}

def local_clock_phase(ctx,engine,xi):
    # Physical imposed clock readout relative to its own turning section.
    t=ctx['event']+xi
    return float(ctx['theta'](t)-ctx['theta'](ctx['event']))

def metrics_for_grid(q,engine,ctx_o,ctx_a,common_scale,weights,grid,events,mode):
    original_k=ctx_o['kappa0'];autonomous_k=ctx_a['kappa0']
    output=[]
    for i,(xi_o,xi_a) in enumerate(grid):
        eo=entry_at(q,engine,ctx_o,original_k,float(xi_o),ctx_o['scale'],common_scale,weights)
        ea=entry_at(q,engine,ctx_a,autonomous_k,float(xi_a),ctx_a['scale'],common_scale,weights)
        ep=entry_at(q,engine,ctx_o,autonomous_k,float(xi_o),ctx_o['scale'],common_scale,weights)
        eq=entry_at(q,engine,ctx_a,original_k,float(xi_a),ctx_a['scale'],common_scale,weights)
        full=pair_geometry(eo['P'],eo['K'],ea['P'],ea['K'])
        po=pair_geometry(eo['P'],eo['K'],ep['P'],ep['K'])
        pa=pair_geometry(eq['P'],eq['K'],ea['P'],ea['K'])
        so=pair_geometry(eo['P'],eo['K'],eq['P'],eq['K'])
        sa=pair_geometry(ep['P'],ep['K'],ea['P'],ea['K'])
        row={'mode':mode,'index':i,'xi_original':float(xi_o),'xi_autonomous':float(xi_a),
          'theta_relative_original':local_clock_phase(ctx_o,engine,float(xi_o)),
          'theta_relative_autonomous':local_clock_phase(ctx_a,engine,float(xi_a)),
          'clock_phase_difference':local_clock_phase(ctx_o,engine,float(xi_o))-local_clock_phase(ctx_a,engine,float(xi_a)),
          'full_projector_gap':full['projector_op_gap'],
          'full_angle_deg':full['max_principal_angle_deg'],
          'second_angle_deg':full['second_principal_angle_deg'],
          'third_angle_deg':full['third_principal_angle_deg'],
          'full_fro_gap':full['projector_fro_gap'],
          'param_only_on_original_state':po['projector_op_gap'],
          'param_only_on_autonomous_state':pa['projector_op_gap'],
          'state_only_at_original_kappa':so['projector_op_gap'],
          'state_only_at_autonomous_kappa':sa['projector_op_gap'],
          'max_identity_residual':max(a['angle_identity_abs_res'] for a in (full,po,pa,so,sa)),
          'min_strong_s3':min(eo['s'][2],ea['s'][2]),
          'observer_d_angle_deg':float(np.degrees(np.arccos(np.clip(float(eo['d']@ea['d']),-1,1))))}
        output.append(row)
    return pd.DataFrame(output)

def extrema_diagnostic(df,key):
    x=df.xi_original.to_numpy();d=df[key].to_numpy()
    # A candidate requires a sign reversal of first difference supported by a
    # nontrivial two-sided prominence. Endpoint extrema are NOT oscillation.
    dx=np.diff(d)
    floor=max(float(np.ptp(d))*0.005,1e-12)
    out=[]
    for i in range(1,len(d)-1):
        if dx[i-1]*dx[i]<0 and min(abs(dx[i-1]),abs(dx[i]))>floor/len(d):
            lo=max(0,i-8);hi=min(len(d),i+9)
            prom=min(abs(d[i]-d[lo]),abs(d[i]-d[hi-1]))
            if prom>=floor:out.append({'xi':float(x[i]),'type':'max' if dx[i-1]>0 else 'min','prominence':float(prom)})
    return out

def plot(df,gate,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(9,5))
    ax.plot(df.xi_original,df.full_angle_deg,label='Paired 7D nullspaces (both states, both kappas)',lw=2)
    ax.plot(df.xi_original,np.degrees(np.arcsin(np.clip(df.param_only_on_original_state,0,1))),label='Only kappa changed at original state',alpha=.85)
    ax.plot(df.xi_original,np.degrees(np.arcsin(np.clip(df.state_only_at_original_kappa,0,1))),label='Only state changed at original kappa',alpha=.85)
    ax.set(xlabel='Drive/turn-relative evolution offset ξ',ylabel='Maximum principal angle (deg)',
      title='Q550 v18.50t — Paired-kappa observer kernel edges in a shared 10D chart')
    ax.legend(fontsize=8);ax.grid(alpha=.25);fig.tight_layout();fig.savefig(out/'paired_kappa_kernel_edges.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    ax.plot(gate.index/(len(gate)-1),gate.full_angle_deg,label='Two separately prepared branches')
    ax.plot(gate.index/(len(gate)-1),np.degrees(np.arcsin(np.clip(gate.param_only_on_original_state,0,1))),label='Parameter-only, fixed original state')
    ax.plot(gate.index/(len(gate)-1),np.degrees(np.arcsin(np.clip(gate.state_only_at_original_kappa,0,1))),label='State-only, original kappa')
    ax.set(xlabel='Normalized parity-to-maximum gate coordinate (0..1)',ylabel='Largest principal angle (deg)',
       title='Q550 v18.50t — Event-aligned paired nullspaces')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'phase_aligned_gate_separation.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    ax.plot(df.xi_original,df.full_projector_gap,label='Full pair')
    ax.plot(df.xi_original,df.param_only_on_original_state,label='Parameter-only on original state')
    ax.plot(df.xi_original,df.state_only_at_original_kappa,label='State-only at original kappa')
    ax.set(xlabel='Turn-relative offset ξ',ylabel='Operator norm of projector difference',
       title='Q550 v18.50t — Parameter versus state-preparation comparison')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'state_parameter_factorization.png',dpi=145);plt.close(fig)
    # Resolve the tiny drift instead of visually flattening it against the full gap.
    fig,ax=plt.subplots(figsize=(9,4.8))
    x=df.xi_original
    ax.plot(x,1e8*(df.full_projector_gap-df.full_projector_gap.iloc[0]),label='Paired projector gap Δ from start',lw=2)
    ax.plot(x,1e8*(df.param_only_on_original_state-df.param_only_on_original_state.iloc[0]),label='Parameter-only Δ from start')
    ax.plot(x,1e8*(df.state_only_at_original_kappa-df.state_only_at_original_kappa.iloc[0]),label='State-only Δ from start')
    ax.set(xlabel='Turn-relative evolution offset ξ',ylabel='Change in projector operator gap (×10⁻⁸)',
           title='Q550 v18.50t — Resolved drift (not an oscillation)')
    ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout();fig.savefig(out/'paired_kappa_microgap_drift.png',dpi=145);plt.close(fig)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--broad-points',type=int,default=129)
    ap.add_argument('--gate-points',type=int,default=65)
    ap.add_argument('--broad-end',type=float,default=.001092)
    ap.add_argument('--preflight-only',action='store_true')
    a=ap.parse_args()
    if a.broad_points<17 or a.gate_points<17 or not 0<a.broad_end<=.001092:raise ValueError('Invalid grid')
    info,s_script,r_blob=authenticate_s()
    print('AUTHENTICATED v18.50s',info,flush=True)
    if a.preflight_only:return
    out=ROOT/'results';out.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='q550_v18_50t_',dir=str(ROOT)) as path:
        q,r,p,o,engine,unit,drpt,creport,events=dynamic_model_stage(Path(path),s_script,r_blob)
        co=p.make_context(o,'original',engine,unit,drpt,creport)
        ca=p.make_context(o,'autonomous',engine,unit,drpt,creport)
        shared_scale=np.maximum.reduce((np.ones(10),np.asarray(co['scale']),np.asarray(ca['scale'])))
        weights=np.asarray(drpt['common_metric_scale_4d'])
        e={}
        for kind in ('original','autonomous'):
            ev=events[(events.kind==kind)&(events.metric=='common_parent_c')&np.isclose(events.epsilon,1e-4)]
            if len(ev)!=1:raise RuntimeError('Missing gate events for '+kind)
            e[kind]=[float(ev.iloc[0].parity_xi),float(ev.iloc[0].stationary_xi)]
        print('ORIGINAL kappa',co['kappa0'],'AUTONOMOUS kappa',ca['kappa0'],'gate',e,flush=True)
        xs=np.linspace(0,a.broad_end,a.broad_points)
        common=[(float(x),float(x)) for x in xs]
        frame=metrics_for_grid(q,engine,co,ca,shared_scale,weights,common,e,'same_turn_relative_xi')
        print('BROAD PAIR COMPLETED',len(frame),flush=True)
        u=np.linspace(0,1,a.gate_points)
        gategrid=[(e['original'][0]+t*(e['original'][1]-e['original'][0]),
                   e['autonomous'][0]+t*(e['autonomous'][1]-e['autonomous'][0])) for t in u]
        gate=metrics_for_grid(q,engine,co,ca,shared_scale,weights,gategrid,e,'event_normalized')
        print('GATE PAIR COMPLETED',len(gate),flush=True)
        # Parallel raw-physical-unit chart control at a sparse subset.
        controls=[(float(x),float(x)) for x in xs[::8]]
        raw=metrics_for_grid(q,engine,co,ca,np.ones(10),weights,controls,e,'raw_physical_chart')
    frame.to_csv(out/'paired_kappa_same_phase_10d.csv',index=False,float_format='%.17g')
    gate.to_csv(out/'paired_kappa_event_aligned_gate.csv',index=False,float_format='%.17g')
    raw.to_csv(out/'paired_kappa_raw_chart_control.csv',index=False,float_format='%.17g')
    plot(frame,gate,out)
    maxima=extrema_diagnostic(frame,'full_projector_gap')
    even_extrema=extrema_diagnostic(frame.iloc[::2].reset_index(drop=True),'full_projector_gap')
    report={'version':'v18.50t','title':'Paired-κ0 Phase-Aligned Edge Motion & Projector Separation Audit',
       'classification':'PAIRED_PARAMETER_AND_INITIAL_STATE_SENSITIVE_10D_OBSERVER_PROJECTOR_DIAGNOSTIC_NOT_DYNAMIC_ACTIVATION_BAND_CERTIFICATE',
       'parent_s':info,'model_kappas':{'original':co['kappa0'],'autonomous':ca['kappa0']},
       'chart':{'name':'shared diagonal state chart','source':'componentwise maximum of both inherited branch seed scales and one','shared_scale':shared_scale.tolist(),
           'observer_weights':weights.tolist(),'raw_physical_chart_control':True},
       'grid':{'broad_points':len(frame),'broad_end':a.broad_end,'event_aligned_points':len(gate),'raw_chart_points':len(raw),'event_xi':e},
       'replays':{'natural_orbit_preparations':2,'natural_driven_10d_integrations':2,'counterfactual_state_evaluations':'Same 10D states with kappa swapped; no re-integration for changed kappa'},
       'diagnostics':{'full_pair_max_principal_angle_deg_min':float(frame.full_angle_deg.min()),
          'full_pair_max_principal_angle_deg_max':float(frame.full_angle_deg.max()),
          'full_pair_gap_min':float(frame.full_projector_gap.min()),
          'full_pair_gap_max':float(frame.full_projector_gap.max()),
          'full_pair_gap_start':float(frame.full_projector_gap.iloc[0]),
          'full_pair_gap_end':float(frame.full_projector_gap.iloc[-1]),
          'full_pair_gap_slope_sign_changes':int(np.count_nonzero(np.diff(np.sign(np.diff(frame.full_projector_gap.values)))!=0)),
          'prominent_internal_extrema':maxima,'even_grid_prominent_internal_extrema':even_extrema,
          'max_observer_rank_residual':float(frame.max_identity_residual.max()),
          'minimum_strong_singular_value':float(frame.min_strong_s3.min()),
          'max_clock_phase_offset':float(frame.clock_phase_difference.abs().max()),
          'mean_parameter_only_gap':float(frame.param_only_on_original_state.mean()),
          'mean_state_only_gap':float(frame.state_only_at_original_kappa.mean()),
          'raw_chart_full_gap_range':[float(raw.full_projector_gap.min()),float(raw.full_projector_gap.max())]},
       'decision_rules':{'oscillation_requires':'At least two alternating, prominent interior extrema persistent on grid decimation and independent chart/control; not asserted from endpoint differences.',
           'narrow_band_requires':'Independent κ0 parameter sweep with dynamical replay and bandwidth definition; two endpoints cannot establish a narrow-band activator.'},
       'limitations':['The two natural states are independently prepared and are not a controlled single-state parameter perturbation.',
         'Turn-relative offsets are an alignment convention; the imposed clock phases may differ.',
         'Shared diagonal chart is well-defined but not a certified kinetic material metric; raw physical chart is a sensitivity control.',
         'Parameter-only swap evaluates the Jacobian on the same state and is not a new trajectory under the swapped κ0.',
         'Finite sampling cannot prove lack or existence of fast oscillations between points.',
         'No narrow-band activation, universal material edge, torsional flip, or constitutive polymer equivalence is established.'],
       'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('v18.50t COMPLETED',json.dumps(report['diagnostics'],indent=2),flush=True)

if __name__=='__main__':main()
