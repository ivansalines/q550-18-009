#!/usr/bin/env python3
"""Q550 v18.50s: stable principal-angle measurements and independent tangent integrator audit.

Verifies authentic v18.50r -> q genealogy; reconstructs the genuine driven
10D trajectory; integrates the tangent fundamental matrix with analytic J10.
Scientific computations use the inherited Euclidean chart, not a physical
metric. All comments, reports and output labels are in English.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

ROOT=Path(__file__).resolve().parents[1]
R='q550_differential_kernel_invariance_analytic_tangent_generator_v18_50r_bundle'
Q='q550_analytic_observer_jacobian_nullspace_projector_transport_v18_50q_bundle'
PARENT=ROOT/'inputs'/(R+'_server_sendback.zip')

def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()

def authenticate_r():
    with zipfile.ZipFile(PARENT) as z:
        if z.testzip() is not None:raise RuntimeError('Parent r ZIP CRC failed')
        sm=json.loads(z.read(R+'/SOURCE_MANIFEST.json'));om=json.loads(z.read(R+'/SHA256SUMS_OUTPUT.json'))
        if sm['root']!=R or om['root']!=R:raise RuntimeError('Parent r root mismatch')
        for man,key in ((sm,'files'),(om,'file_sha256')):
            for rel,digest in man[key].items():
                if sha(z.read(R+'/'+rel))!=digest:raise RuntimeError('Parent r hash mismatch: '+rel)
        script=z.read(R+'/scripts/run_audit.py')
        qblob=z.read(R+'/inputs/'+Q+'_server_sendback.zip')
        report=json.loads(z.read(R+'/results/report.json'))
        q_comparison=pd.read_csv(io.BytesIO(z.read(R+'/results/parent_q_transport_comparison.csv')))
    if report['version']!='v18.50r':raise RuntimeError('Parent r scientific version mismatch')
    return {'zip_sha256':sha(PARENT.read_bytes()),'source_files':len(sm['files']),
            'output_files':len(om['file_sha256']),'classification':report['classification']},script,qblob,report,q_comparison

def stage_r(tmp,script,qblob):
    stage=tmp/R
    (stage/'scripts').mkdir(parents=True)
    (stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(script)
    (stage/'inputs'/(Q+'_server_sendback.zip')).write_bytes(qblob)
    spec=importlib.util.spec_from_file_location('q550_v18_50s_authenticated_r',stage/'scripts/run_audit.py')
    mod=importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    return mod

def angle_measures(K,Qtransport):
    """Independent stable sin- and ill-conditioned cos-based angle estimates.

    K and Qtransport have orthonormal 10x7 columns. For subspaces:
    sin(theta_max)=|| (I-KK^T) Q ||_2=||KK^T-QQ^T||_2.
    Cos(theta_max)=sigma_min(K^T Q). This last form loses precision as theta->0.
    """
    K=np.asarray(K,float);Qtransport=np.asarray(Qtransport,float)
    if K.ndim!=2 or K.shape!=Qtransport.shape:raise ValueError('Subspace basis shape mismatch')
    n,k=K.shape
    e=np.eye(n);P=K@K.T;Qp=Qtransport@Qtransport.T
    sin_direct=float(np.linalg.svd((e-P)@Qtransport,compute_uv=False)[0])
    sin_projector=float(np.linalg.svd(P-Qp,compute_uv=False)[0])
    cos_min=float(np.linalg.svd(K.T@Qtransport,compute_uv=False)[-1])
    acos=float(np.degrees(np.arccos(np.clip(cos_min,-1,1))))
    asin=float(np.degrees(np.arcsin(np.clip(sin_direct,0,1))))
    atan2=float(np.degrees(np.arctan2(sin_direct,np.sqrt(max(0.,1.-sin_direct**2)))))
    return {'asin_angle_deg':asin,'acos_angle_deg':acos,'atan2_angle_deg':atan2,
            'projector_sin_angle_deg':float(np.degrees(np.arcsin(np.clip(sin_projector,0,1)))),
            'sin_max_from_residual':sin_direct,'sin_max_from_projector':sin_projector,
            'cos_min_from_overlap':cos_min,
            'sin_method_abs_diff':abs(sin_direct-sin_projector),
            'acos_asin_angle_diff_deg':acos-asin,
            'ortho_instant_defect':float(np.linalg.norm(K.T@K-np.eye(k))),
            'ortho_transported_defect':float(np.linalg.norm(Qtransport.T@Qtransport-np.eye(k)))}

def one_tangent_run(r,engine,ctx,t0,t1,K0,K1,method,tolerance,steps):
    """True 10D variational integration, not a numerical replot of parent q."""
    span=t1-t0
    if span<=0:raise ValueError('Non-positive gate span')
    state_sol=ctx['sol'];clock=ctx['theta']
    memo={}
    def J_at(t):
        key=float(t)
        if key not in memo:
            z=np.asarray(state_sol.sol(key),float)
            y=np.r_[z,clock(key)]
            f,j,h=engine.jet.structural_jet(y,ctx['kappa0'],engine.params,engine.slope)
            memo[key]=r.chart_analytic_generator(j,ctx['scale'])
        return memo[key]
    def rhs(t,v):return (J_at(t)@v.reshape(10,10)).ravel()
    def jac(t,v):return np.kron(J_at(t),np.eye(10))
    kw={'method':method,'rtol':tolerance,'atol':tolerance*.1,
        'max_step':span/steps,'dense_output':False}
    if method=='Radau':kw['jac']=jac
    with warnings.catch_warnings(record=True) as ww:
        warnings.simplefilter('always')
        try:
            sol=solve_ivp(rhs,(t0,t1),np.eye(10).ravel(),**kw)
        except Exception as exc:
            return {'method':method,'rtol':tolerance,'atol':tolerance*.1,'max_step_divisor':steps,
              'success':False,'reached_endpoint':False,'status':-100,
              'message':'exception:'+str(exc),'nfev':-1,'njev':-1,'nlu':-1,
              'warning':' | '.join(str(w.message) for w in ww),'J_eval_count':len(memo)}
    endpoint=float(sol.t[-1])
    reached=bool(abs(endpoint-t1)<=max(1e-15,2e-10*span))
    data={'method':method,'rtol':tolerance,'atol':tolerance*.1,'max_step_divisor':steps,
        'success':bool(sol.success),'reached_endpoint':reached,'status':int(sol.status),
        'message':str(sol.message),'nfev':int(sol.nfev),
        'njev':int(sol.njev),'nlu':int(sol.nlu),
        't_start':float(sol.t[0]),'t_end':endpoint,'t_target':float(t1),
        'end_error':float(abs(endpoint-t1)),
        'warning':' | '.join(str(w.message) for w in ww),'J_eval_count':len(memo)}
    if not(sol.success and reached):return data
    Phi=np.asarray(sol.y[:,-1],float).reshape(10,10)
    Qtransport,_=np.linalg.qr(Phi@K0,mode='reduced')
    data.update(angle_measures(K1,Qtransport))
    B1=ctx['B1'];data.update({'observer_leakage':float(np.linalg.norm(B1@Qtransport,'fro')/np.linalg.norm(B1,'fro')),
         'fundamental_frobenius_distance':float(np.linalg.norm(Phi-np.eye(10),'fro')),
         'principal_gap_projector_fro':float(np.linalg.norm(K1@K1.T-Qtransport@Qtransport.T,'fro'))})
    return data

def create_plots(df,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import ScalarFormatter
    for kind in ('original','autonomous'):
        d=df[(df.kind==kind)&df.success&df.reached_endpoint]
        if not len(d):continue
        fig,ax=plt.subplots(figsize=(9,4.9))
        for method in ('DOP853','Radau'):
            dd=d[(d.method==method)&(d.max_step_divisor==max(d.max_step_divisor))].sort_values('rtol')
            if len(dd):
                ax.semilogx(dd.rtol,dd.asin_angle_deg,'o-',label=method+' arcsin')
                ax.semilogx(dd.rtol,dd.acos_angle_deg,'x--',alpha=.7,label=method+' arccos')
        ax.set(xlabel='Relative solver tolerance',ylabel='Maximum principal angle (degrees)',
               title=f'Q550 v18.50s — Principal-angle conditioning ({kind})')
        ax.invert_xaxis();ax.grid(alpha=.25);ax.legend(fontsize=8)
        ax.ticklabel_format(axis='y',style='plain',useOffset=False)
        fig.tight_layout();fig.savefig(out/f'angle_conditioning_{kind}.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(8.8,5))
    for kind in ('original','autonomous'):
        d=df[(df.kind==kind)&df.success&df.reached_endpoint]
        for method in ('DOP853','Radau'):
            dd=d[(d.method==method)&(d.max_step_divisor==max(d.max_step_divisor))]
            if len(dd):ax.semilogx(dd.rtol,dd.nfev,'o-',label=kind+' '+method)
    ax.invert_xaxis();ax.set(xlabel='Solver tolerance',ylabel='Reported function evaluations',
                title='Q550 v18.50s — Endpoint-certified integrator effort')
    ax.grid(alpha=.25);ax.legend(fontsize=7);fig.tight_layout();fig.savefig(out/'tangent_integrator_effort.png',dpi=150);plt.close(fig)

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('--preflight-only',action='store_true')
    pa.add_argument('--tolerances',type=float,nargs='+',default=[1e-8,1e-10,1e-12])
    pa.add_argument('--step-divisors',type=int,nargs='+',default=[8,16])
    pa.add_argument('--methods',nargs='+',choices=['DOP853','Radau'],default=['DOP853','Radau'])
    pa.add_argument('--kinds',nargs='+',choices=['original','autonomous'],default=['original','autonomous'])
    pa.add_argument('--require-all-success',action='store_true',help='Fail run on any incomplete integration, default tolerates diagnostic failures')
    a=pa.parse_args()
    if not a.tolerances or not a.step_divisors or any(x<=0 for x in a.tolerances) or any(v<1 for v in a.step_divisors):raise ValueError('Invalid integration grid')
    info,rscript,qblob,preport,qprior=authenticate_r()
    print('AUTHENTICATED v18.50r',info,'parent q entries',len(qprior),flush=True)
    if a.preflight_only:return
    records=[];branches=[]
    with tempfile.TemporaryDirectory(prefix='q550_v18_50s_genealogy_',dir=str(ROOT)) as tmp:
        tmp=Path(tmp);r=stage_r(tmp,rscript,qblob)
        ri, qscript,pblob,qreport,old=r.authenticate_q()
        q=r.stage_q(tmp,qscript,pblob)
        parent_info,pscript,oblob,_,_=q.authenticate_parent()
        p=q.stage_p(pscript,oblob,tmp)
        o,p,engine,unit,drpt,creport,events=q.stage_model(p,tmp)
        for kind in a.kinds:
            ctx=p.make_context(o,kind,engine,unit,drpt,creport)
            ev=events[(events.kind==kind)&(events.metric=='common_parent_c')&np.isclose(events.epsilon,1e-4)]
            if len(ev)!=1:raise RuntimeError('Parent gate event missing or ambiguous')
            parity,station=float(ev.iloc[0].parity_xi),float(ev.iloc[0].stationary_xi)
            t0,t1=ctx['event']+parity,ctx['event']+station
            w=np.asarray(drpt['common_metric_scale_4d'],float)
            _,B0,_,_,_=r.observer_at(q,engine,ctx,t0,w)
            _,B1,_,_,_=r.observer_at(q,engine,ctx,t1,w)
            _,K0,_,rank0=q.projector(B0);_,K1,_,rank1=q.projector(B1)
            if (rank0,rank1)!=(3,3):raise RuntimeError('Rank three lost at gate endpoints')
            ctx['B1']=B1
            parent=qprior[qprior.kind==kind].iloc[0]
            branches.append({'kind':kind,'kappa0':float(ctx['kappa0']),
                'parity_xi':parity,'stationary_xi':station,'span_xi':station-parity,
                'original_q_arccos_angle_deg':float(parent.parent_endpoint_max_principal_angle_deg),
                'original_q_fro_gap':float(parent.parent_endpoint_projector_frobenius_gap),
                'natural_nfev':int(ctx['nfev'])})
            for method in a.methods:
                for div in a.step_divisors:
                    for tol in a.tolerances:
                        print(f'TANGENT {kind} {method} tol={tol:g} max_step=span/{div}',flush=True)
                        d=one_tangent_run(r,engine,ctx,t0,t1,K0,K1,method,tol,div)
                        d.update({'kind':kind,'kappa0':float(ctx['kappa0'])})
                        records.append(d)
                        print('  RESULT',d.get('success'),d.get('reached_endpoint'),d.get('nfev'),d.get('asin_angle_deg'),flush=True)
    out=ROOT/'results';out.mkdir(exist_ok=True)
    frame=pd.DataFrame(records);bdf=pd.DataFrame(branches)
    frame.to_csv(out/'principal_angle_integrator_convergence.csv',index=False,float_format='%.17g')
    bdf.to_csv(out/'parent_q_angle_comparison.csv',index=False,float_format='%.17g')
    create_plots(frame,out)
    valid=frame[frame.success&frame.reached_endpoint]
    if valid.empty:raise RuntimeError('No complete integrations; cannot classify angle convergence')
    stats={}
    for kind in a.kinds:
        d=valid[valid.kind==kind]
        if d.empty:raise RuntimeError('Branch has no complete integration: '+kind)
        asin=d.asin_angle_deg
        stats[kind]={'max_angle_deg':float(asin.max()),'min_angle_deg':float(asin.min()),
           'asin_spread_deg':float(asin.max()-asin.min()),
           'max_sin_projector_difference':float(d.sin_method_abs_diff.max()),
           'max_acos_asin_difference_deg':float(d.acos_asin_angle_diff_deg.abs().max()),
           'min_nfev':int(d.nfev.min()),'max_nfev':int(d.nfev.max()),
           'reference_parent_q_arccos_deg':float(bdf[bdf.kind==kind].iloc[0].original_q_arccos_angle_deg),
           'min_vs_parent_q_deg':float(np.min(np.abs(asin-float(bdf[bdf.kind==kind].iloc[0].original_q_arccos_angle_deg))))}
    incomplete=frame[~(frame.success&frame.reached_endpoint)]
    report={'version':'v18.50s','title':'Principal-Angle Conditioning & Tangent-Integrator Convergence Audit',
       'classification':'INHERITED_CHART_NUMERICAL_PRINCIPAL_ANGLE_INTEGRATOR_CONVERGENCE_NOT_MATERIAL_CERTIFICATE',
       'parent':info,'methods':{'vector_flow':'Genuine analytic 10D Jacobian J10 from the inherited 11D structural jet; independently solves 100D fundamental matrix evolution',
         'principal_angle_sin':'asin(sigma_max((I-P_instant)Q_transport))',
         'principal_angle_cos':'acos(sigma_min(K_instant.T Q_transport)); retained as conditioning comparison only',
         'independent_projector':'asin(||P_instant-P_transport||_2)',
         'completion':'Require solve_ivp.success AND solver end time matches requested terminal time',
         'accuracy':'Cross method, rtol, atol and max_step cap; no unverified endpoint accepted'},
       'config':{'methods':a.methods,'kinds':a.kinds,'rtols':a.tolerances,'max_step_divisors':a.step_divisors},
       'counts':{'attempted_tangent_integrations':len(frame),'complete_tangent_integrations':len(valid),
                 'incomplete_tangent_integrations':len(incomplete),'natural_state_replays':len(branches)},
       'per_branch':stats,'incomplete':incomplete[['kind','method','rtol','max_step_divisor','status','message']].to_dict('records'),
       'limitations':['The observer and orthogonal projector are expressed in the inherited Euclidean seed chart, not a derived material kinetic metric.',
          'Parent q used an FD tangent generator, whereas this audit uses the analytic 10D Jacobian; agreement is a regression, not a mathematical identity.',
          'Solver tolerance convergence is not an interval error bound or an exact continuous-time certification.',
          'Near-zero principal angles computed from arccos of overlaps can exhibit subtractive loss of precision.',
          'Integrations that fail or do not reach the final gate are explicitly rejected.',
          'No polymer constitutive law, memory certificate, material connection, or physical torsional flip is established.'],
       'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('v18.50s COMPLETE',json.dumps({'counts':report['counts'],'per_branch':stats},indent=2),flush=True)
    if a.require_all_success and len(incomplete):raise RuntimeError('Some integrations incomplete; see CSV')

if __name__=='__main__':main()
