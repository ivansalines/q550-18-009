#!/usr/bin/env python3
"""Q550 v18.51c: model-Jacobian Gram metrics and spectral-source robustness.

All observations are POSTPROCESSING of authenticated 10D matrices. A positive
Jacobian-Gram metric is a MODEL-DERIVED REGULARIZED OBSERVER METRIC, NOT a
certified kinetic/material metric. Constant and evolving metrics are treated
separately. Spectral analysis uses metric-skew reduction, preserving the
mathematical meaning of a skew generator in the weighted geometry.
"""
from __future__ import annotations
import csv, hashlib, io, json, platform, zipfile
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
B='q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle'
A='q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle'
Z='q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle'
Y='q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle'
X='q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle'
PARENT=ROOT/'inputs'/(B+'_server_sendback.zip')
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)
ID=np.eye(10)

def sha(b):return hashlib.sha256(b).hexdigest()

def authenticate(z,root,version):
    if z.testzip() is not None:raise RuntimeError('CRC failed '+root)
    sm=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
    if (sm['root'],sm['version'],om['root'],om.get('version',version))!=(root,version,root,version):
        raise RuntimeError('Manifest root or version mismatch: '+root)
    files={**sm['files'],**om['file_sha256']}
    expected=set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}
    actual={n[len(root)+1:] for n in z.namelist() if n.startswith(root+'/') and not n.endswith('/')}
    if actual!=expected:raise RuntimeError('Missing/unlisted items in '+root+': '+str(actual^expected))
    for rel,h in files.items():
        if sha(z.read(root+'/'+rel))!=h:raise RuntimeError('SHA mismatch '+root+'/'+rel)
    return {'version':version,'sources':len(sm['files']),'results':len(om['file_sha256'])}

def load_npz(data):
    with np.load(io.BytesIO(data),allow_pickle=False) as z:
        return {k:np.array(z[k],copy=True) for k in z.files}

def load_ancestors():
    with zipfile.ZipFile(PARENT) as b:
        lineage={'v18.51b':authenticate(b,B,'v18.51b')}
        b_csv=b.read(B+'/results/spectral_source_attribution_phase_ledger.csv').decode('utf-8')
        a_blob=b.read(B+'/inputs/'+A+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(a_blob)) as a:
        lineage['v18.51a']=authenticate(a,A,'v18.51a')
        z_blob=a.read(A+'/inputs/'+Z+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(z_blob)) as z:
        lineage['v18.50z']=authenticate(z,Z,'v18.50z')
        J=load_npz(z.read(Z+'/results/model_vs_canonical_centerline_tensors.npz'))
        y_blob=z.read(Z+'/inputs/'+Y+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(y_blob)) as y:
        lineage['v18.50y']=authenticate(y,Y,'v18.50y')
        x_blob=y.read(Y+'/inputs/'+X+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(x_blob)) as x:
        lineage['v18.50x']=authenticate(x,X,'v18.50x')
        P=load_npz(x.read(X+'/results/full_projector_sensitivity_tensors.npz'))
    rows=list(csv.DictReader(io.StringIO(b_csv)))
    xi=np.array(J['xi'],float)
    if len(xi)!=79 or not np.allclose(P['xi'],xi,rtol=0,atol=1e-14):
        raise RuntimeError('Parent grid mismatch')
    mid=(1/6+7*np.pi/132)/2
    kidx=int(np.argmin(abs(P['kappa']-mid)))
    if abs(P['kappa'][kidx]-mid)>1e-13:raise RuntimeError('Mid κ not found')
    lineage['parent_b_sha256']=sha(PARENT.read_bytes())
    lineage['kappa_midpoint']=mid
    return J,P,rows,xi,kidx,lineage

def sym(a):return .5*(a+a.T)
def skew(a):return .5*(a-a.T)
def fn(a):return float(np.linalg.norm(a,'fro'))
def inp(a,b):return float(np.einsum('ij,ij->',a,b))
def whiten(G):
    ev,U=np.linalg.eigh(sym(G))
    if ev.min()<1e-8:raise RuntimeError('Non-positive metric')
    L=(U*np.sqrt(ev))@U.T
    Li=(U/np.sqrt(ev))@U.T
    return L,Li,float(ev.max()/ev.min())

def proj_spectral(W):
    H=sym(-(W@W))
    ev,V=np.linalg.eigh(H)
    I=np.argsort(ev)[::-1]
    if ev[I[3]]<1e-5 or ev[I[1]]-ev[I[2]]<1 or ev[I[2]]-ev[I[4]]<1:
        raise RuntimeError('Dominant 2+2 spectral separation failed')
    q1=V[:,I[:2]]@V[:,I[:2]].T
    q2=V[:,I[2:4]]@V[:,I[2:4]].T
    l1=.5*sum(ev[I[:2]]); l2=.5*sum(ev[I[2:4]])
    strengths=[float(np.sqrt(l1)),float(np.sqrt(l2))]
    extras=[float(np.sqrt(max(0,.5*sum(ev[I[i:i+2]])))) for i in (4,6,8)]
    return H,q1,q2,float(l1-l2),strengths,extras

def jacobian_metric(Joriginal,Jauto,alpha,scale):
    return ID + alpha*sym(Joriginal.T@Joriginal+Jauto.T@Jauto)/(2*scale)

def time_derivative(x,values):
    return np.asarray(CubicSpline(x,values,axis=0).derivative()(x))

def write_csv(name,rows):
    if not rows:raise RuntimeError('Empty table '+name)
    with open(OUT/name,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def one_branch(seed,metric_name,alpha,move,xi,j,zp,Gseries,dGseries):
    P=zp
    km=j['K_model_'+seed];kc=j['K_canonical_'+seed];
    JJ=j['J_'+seed];
    dJJ=time_derivative(xi,JJ);dP=time_derivative(xi,P)
    dKC=time_derivative(xi,kc)
    dKM=time_derivative(xi,km)
    rows=[];matrices={'W':[],'Wprime':[],'Q1':[],'Q2':[],'source_gen':[],'source_post':[],'source_can':[],'source_metric':[]}
    for i,ti in enumerate(xi):
        p=P[i];pd=dP[i];q=ID-p;J0=JJ[i];dJ=dJJ[i]
        origW=km[i]-kc[i]
        dMgen=q@dJ@p-p@dJ.T@q
        dMpost=-pd@J0@p+q@J0@pd-pd@J0.T@q+p@J0.T@pd
        src={'gen':dMgen,'post':dMpost,'can':-dKC[i]}
        L,Li,condition=whiten(Gseries[i]);
        raw=L@origW@Li
        weighted=skew(raw)
        if move:
            # Time-dependent whitening contributes an explicitly separated
            # metric-rate term. This is NOT a dynamically defined metric connection.
            spl_Lp=dGseries[i] # source holds Lprime from spline
            D=spl_Lp@Li
            metric_part=skew(D@raw-raw@D)
        else:metric_part=np.zeros((10,10))
        srcW={k:skew(L@v@Li) for k,v in src.items()}
        srcW['metric']=metric_part
        H,Q1,Q2,gap,strengths,extras=proj_spectral(weighted)
        outH={k:sym(-(v@weighted+weighted@v)) for k,v in srcW.items()}
        fullH=sum(outH.values())
        parts={k:Q2@v@Q1/gap for k,v in outH.items()}
        total=sum(parts.values()); rate=fn(total)
        if rate<1e-12:raise RuntimeError('Degenerate interplane rate')
        shares={k:inp(parts[k],total)/rate**2 for k in parts}
        dStrength={k:(inp(Q1,v)/(4*strengths[0]),inp(Q2,v)/(4*strengths[1])) for k,v in outH.items()}
        row={'seed_family':seed,'metric':metric_name,'alpha':alpha,'xi':float(ti),
             'metric_condition':condition, 'sigma1':strengths[0],'sigma2':strengths[1],
             'sigma3':extras[0],'sigma4':extras[1],'pair_gap':gap,
             'coupling_rate':rate,'source_model_rate':fn(parts['gen']+parts['post']),
             'source_canonical_rate':fn(parts['can']),'source_metric_rate':fn(parts['metric']),
             'signed_generator':shares['gen'],'signed_posture':shares['post'],
             'signed_canonical':shares['can'],'signed_metric':shares['metric'],
             'signed_model_total':shares['gen']+shares['post'],
             'signed_sum_residual':abs(sum(shares.values())-1),
             'sigma1_rate':sum(v[0] for v in dStrength.values()),
             'sigma2_rate':sum(v[1] for v in dStrength.values()),
             'model_sigma1_rate':dStrength['gen'][0]+dStrength['post'][0],
             'canonical_sigma1_rate':dStrength['can'][0],
             'metric_sigma1_rate':dStrength['metric'][0],
             'model_sigma2_rate':dStrength['gen'][1]+dStrength['post'][1],
             'canonical_sigma2_rate':dStrength['can'][1],
             'metric_sigma2_rate':dStrength['metric'][1],
             'offblock_source_analytic_derivative_error':fn(src['gen']+src['post']-dKM[i])/max(fn(dKM[i]),1),
             'spectral_reconstruction_error':fn(total-Q2@fullH@Q1/gap)/max(rate,1),
             'weighted_skew_error':fn(weighted+weighted.T),
             }
        rows.append(row)
        for k,v in [('W',weighted),('Wprime',sum(srcW.values())),('Q1',Q1),('Q2',Q2),('source_gen',parts['gen']),('source_post',parts['post']),('source_can',parts['can']),('source_metric',parts['metric'])]:matrices[k].append(v)
    for k in matrices:matrices[k]=np.array(matrices[k])
    # Independent derivative of the observed weighted-skew trajectory.
    # This can reveal missed metric-rate terms despite exact source addition.
    wprime_spline=time_derivative(xi,matrices['W'])
    for i,row in enumerate(rows):
        row['weighted_W_derivative_relative_error']=fn(wprime_spline[i]-matrices['Wprime'][i])/max(fn(wprime_spline[i]),1)
    return rows,matrices

def passive_control(W,G,src):
    # Passive nonorthogonal chart change xnew = A xold. Transform both metric
    # and operator, then compare the Euclidean-whitened skew reductions via
    # an orthogonal similarity O = sqrt(Gnew) A inv(sqrt(Gold)).
    A=np.eye(10);A[0,1]=.17;A[2,5]=-.12;A[4,9]=.21;A[8,7]=.09
    A=A@np.diag([1.4,.8,1.1,.7,1.8,.9,1.3,.85,1.7,.95])
    Ai=np.linalg.inv(A)
    Ln,Lni,_=whiten(Ai.T@G@Ai)
    L,Li,_=whiten(G)
    O=Ln@A@Li
    red1=skew(L@W@Li)
    red2=skew(Ln@A@W@Ai@Lni)
    src1=skew(L@src@Li)
    src2=skew(Ln@A@src@Ai@Lni)
    return {'orthogonality_residual':fn(O.T@O-ID),
            'W_similarity_error':fn(red2-O@red1@O.T)/max(1,fn(red1)),
            'source_similarity_error':fn(src2-O@src1@O.T)/max(1,fn(src1))}

def graph(rows):
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for metric in ['euclidean','Jgram_0p1_frozen','Jgram_1_frozen','Jgram_4_frozen','Jgram_1_evolving']:
        r=[a for a in rows if a['seed_family']=='original' and a['metric']==metric]
        xx=[v['xi'] for v in r]
        axs[0].plot(xx,[v['signed_canonical'] for v in r],label=metric)
        axs[1].plot(xx,[v['signed_model_total'] for v in r],label=metric)
    axs[0].set_ylabel('Signed canonical contribution');axs[1].set_ylabel('Signed model contribution')
    axs[1].set_xlabel('Evolution coordinate ξ');axs[0].legend(fontsize=8,ncol=2)
    fig.suptitle('v18.51c | Model-derived metric robustness of spectral source attribution')
    fig.tight_layout();fig.savefig(OUT/'metric_attribution_comparison.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for metric in ['euclidean','Jgram_0p1_frozen','Jgram_1_frozen','Jgram_4_frozen','Jgram_1_evolving']:
        r=[a for a in rows if a['seed_family']=='original' and a['metric']==metric]
        xx=[v['xi'] for v in r]
        axs[0].plot(xx,[v['sigma1'] for v in r],label=metric)
        axs[1].plot(xx,[v['sigma3'] for v in r],label=metric)
    axs[0].set_ylabel('First singular strength');axs[1].set_ylabel('Third singular strength')
    axs[1].set_xlabel('Evolution coordinate ξ');axs[0].legend(fontsize=8,ncol=2)
    fig.suptitle('v18.51c | Change of spectral structure under model-derived metrics')
    fig.tight_layout();fig.savefig(OUT/'metric_spectral_channel_emergence.png',dpi=160);plt.close(fig)
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed in ('original','autonomous'):
        r=[a for a in rows if a['seed_family']==seed and a['metric']=='Jgram_1_evolving']
        xx=[v['xi'] for v in r]
        axs[0].plot(xx,[v['signed_metric'] for v in r],label=seed)
        axs[1].plot(xx,[v['source_metric_rate'] for v in r],label=seed)
    axs[0].set_ylabel('Signed metric-motion fraction');axs[1].set_ylabel('Metric-motion interplane rate')
    axs[1].set_xlabel('Evolution coordinate ξ');axs[0].legend()
    fig.suptitle('v18.51c | Contribution from metric change (not hidden in model source)')
    fig.tight_layout();fig.savefig(OUT/'moving_metric_source_ledger.png',dpi=160);plt.close(fig)

def main():
    Z,X,brows,xi,kidx,lineage=load_ancestors()
    J0=(Z['J_original'][0].T@Z['J_original'][0]+Z['J_autonomous'][0].T@Z['J_autonomous'][0])/2
    scale=float(np.linalg.eigvalsh(sym(J0)).max())
    if scale<=0:raise RuntimeError('Invalid model Gram normalizer')
    variants=[('euclidean',0.,False),('Jgram_0p1_frozen',.1,False),('Jgram_1_frozen',1.,False),('Jgram_4_frozen',4.,False),('Jgram_1_evolving',1.,True)]
    allrows=[];matrices={}; passive=[]
    for name,alpha,move in variants:
        if move:
            Gseries=np.array([jacobian_metric(Z['J_original'][i],Z['J_autonomous'][i],alpha,scale) for i in range(len(xi))])
        else:
            g=jacobian_metric(Z['J_original'][0],Z['J_autonomous'][0],alpha,scale)
            Gseries=np.broadcast_to(g,(len(xi),10,10)).copy()
        if move:
            Lseries=np.array([whiten(g)[0] for g in Gseries]); dLseries=time_derivative(xi,Lseries)
        else:dLseries=np.zeros_like(Gseries)
        for seed in ('original','autonomous'):
            data,mat=one_branch(seed,name,alpha,move,xi,Z,X['P_'+seed][kidx],Gseries,dLseries)
            allrows.extend(data)
            if name in ('euclidean','Jgram_1_frozen','Jgram_1_evolving'):
                for key in ('W','Q1','Q2'):
                    matrices[name+'_'+seed+'_'+key]=mat[key]
        passive.append({'metric':name,'alpha':alpha,'evolving':bool(move),**passive_control(Z['K_model_original'][0]-Z['K_canonical_original'][0],Gseries[0],Z['K_model_original'][0])})
    # Baseline must reproduce the canonical Euclidean v18.51b decomposition.
    bindex={(row['seed_family'],float(row['xi'])):row for row in brows}
    err=[]
    for r in allrows:
        if r['metric']!='euclidean':continue
        nearest=min((rr for rr in brows if rr['seed_family']==r['seed_family']),key=lambda q:abs(float(q['xi'])-r['xi']))
        err.append(max(abs(r['coupling_rate']-float(nearest['coupling_rate_spectral'])),
                       abs(r['signed_canonical']-float(nearest['signed_canonical_fraction'])),
                       abs(r['sigma1']-float(nearest['sigma_pair1']))))
    baseline=max(err)
    bymetric={}
    for seed in ('original','autonomous'):
      for name,alpha,move in variants:
        rr=[a for a in allrows if a['seed_family']==seed and a['metric']==name]
        bymetric[seed+'/'+name]={
          'seed':seed,'metric':name,'alpha':alpha,'metric_moves':move,'samples':len(rr),
          'start_canonical_fraction':rr[0]['signed_canonical'], 'end_canonical_fraction':rr[-1]['signed_canonical'],
          'start_model_fraction':rr[0]['signed_model_total'],'end_model_fraction':rr[-1]['signed_model_total'],
          'start_metric_fraction':rr[0]['signed_metric'],'end_metric_fraction':rr[-1]['signed_metric'],
          'start_sigma1':rr[0]['sigma1'],'end_sigma1':rr[-1]['sigma1'],
          'start_sigma2':rr[0]['sigma2'],'end_sigma2':rr[-1]['sigma2'],
          'max_sigma3':max(a['sigma3'] for a in rr),
          'model_rate_dominates_canonical_everywhere':all(a['source_model_rate']>a['source_canonical_rate'] for a in rr),
          'canonical_signed_fraction_exceeds_model_everywhere':all(a['signed_canonical']>a['signed_model_total'] for a in rr),
          'sigma1_monotone_increasing':all(np.diff([a['sigma1'] for a in rr])>0),
          'sigma2_monotone_decreasing':all(np.diff([a['sigma2'] for a in rr])<0),
          'max_metric_condition':max(a['metric_condition'] for a in rr),
          'max_source_identity_residual':max(a['signed_sum_residual'] for a in rr),
        }
    checks={
      'parent_b_and_four_ancestors_authenticated':set(lineage)>= {'v18.51b','v18.51a','v18.50z','v18.50y','v18.50x'},
      'two_seed_families_five_metrics_79_samples':len(allrows)==790,
      'euclidean_parent_b_regression':baseline<3e-6,
      'metric_positive_definite':all(p['max_metric_condition']<=5.00000001 for p in bymetric.values()),
      'algebraic_source_sum':max(r['signed_sum_residual'] for r in allrows)<1e-10,
      'passive_chart_covariance':max(max(p['W_similarity_error'],p['source_similarity_error'],p['orthogonality_residual']) for p in passive)<1e-11,
      'metric_weighted_skew_symmetry':max(r['weighted_skew_error'] for r in allrows)<1e-10,
      'spectral_reconstruction':max(r['spectral_reconstruction_error'] for r in allrows)<1e-10,
      'independent_weighted_time_derivative':max(r['weighted_W_derivative_relative_error'] for r in allrows)<2e-4,
    }
    if not all(checks.values()):raise RuntimeError('Required checks failed: '+str(checks))
    write_csv('metric_spectral_source_phase_ledger.csv',allrows)
    write_csv('metric_spectral_source_summary.csv',list(bymetric.values()))
    write_csv('passive_chart_covariance_control.csv',passive)
    graph(allrows)
    np.savez_compressed(OUT/'weighted_spectral_channel_projectors.npz',xi=xi,**matrices)
    report={'version':'v18.51c','title':'Model-Gram Metric & Spectral-Source Robustness Audit',
      'classification':'MODEL_DERIVED_REGULARIZED_OBSERVER_METRIC_SENSITIVITY_NOT_CERTIFIED_KINETIC_METRIC_OR_MATERIAL_CAUSALITY',
      'lineage':lineage,'common_kappa':lineage['kappa_midpoint'],
      'model_gram_scale':scale,'metric_construction':'G(alpha,xi)=I+alpha*(J_o(xi)^T J_o(xi)+J_a(xi)^T J_a(xi))/(2*lambda_max(Jgram(0))); frozen variants use xi=0',
      'operator_reduction':'skew(sqrt(G) W invsqrt(G)), W=Kmodel-Kcanonical',
      'source_split':'generator-J drift, P posture, -canonical connection drift; for evolving G include metric-rate commutator [Lprime Linv, L W Linv] before skew',
      'all_rows':len(allrows),'results':bymetric,'passive_chart_checks':passive,'checks':checks,
      'euclidean_parent_b_max_abs_diff':baseline,
      'max_independent_weighted_time_derivative_relative_error':max(r['weighted_W_derivative_relative_error'] for r in allrows),
      'limitations':[
        'The Jacobian-Gram metric is constructed from genuine model tangent generators, but no identification with the physical kinetic metric is established.',
        'Both seed preparations are measured at ONE common midpoint kappa, not at two different kappa branches.',
        'Changing from Euclidean to Jacobian-Gram metric changes what angular/skew response is being measured; it is not a passive coordinate change.',
        'Metric skew projection can reveal additional spectral pairs absent or near zero in the Euclidean representation.',
        'Evolving metric includes an extra time-dependent whitening source; the metric-skew construction is a declared diagnostic, not the unique metric-compatible dynamical connection.',
        'Time derivatives of stored J, P, K are inferred by cubic splines across 79 nonuniform samples; no new physical Q550 integration occurs.',
        'Spectral signed fractions and pair-plane couplings are algebraic, not physical energies, stresses, or material causes.',
        'There is no certification of universal invariance under arbitrary physical metrics, nor interval verified differentiation.'
      ],'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':'CubicSpline','matplotlib':matplotlib.__version__}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('v18.51c COMPLETED',json.dumps({'samples':len(allrows),'checks':checks,'regression_error':baseline,'metrics':bymetric},indent=2))

if __name__=='__main__':main()
