#!/usr/bin/env python3
"""Q550 v18.51d: historical kinetic pullback, compatible connection, spectral attribution.

CONSTRUCTION: exact original v18.49h kinetic configuration and state immersion.
AUDIT: recompute states at v18.50z common midpoint kappa, compare with authenticated
v18.51c and split spectral source terms in the physical Cartesian kinetic frame.

The tau_ref family is a declared Sasaki-type position/velocity state metric.
It is NOT unique and should not be mistaken for an observer-independent theorem.
"""
from __future__ import annotations
import csv, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
C='q550_model_gram_metric_spectral_source_robustness_v18_51c_bundle'
B='q550_spectral_channel_coupling_source_generator_attribution_v18_51b_bundle'
A='q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle'
Z='q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle'
Y='q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle'
X='q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle'
W='q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle'
PARENT=ROOT/'inputs'/(C+'_server_sendback.zip')
OUT=ROOT/'results'
ID=np.eye(10)
TAUS=(.5,1.,2.)

def load_module(path, name):
    spec=importlib.util.spec_from_file_location(name,path)
    mod=importlib.util.module_from_spec(spec)
    sys.modules[name]=mod
    spec.loader.exec_module(mod)
    return mod

kin=load_module(ROOT/'reference/kinetic_metric_v18_49h.py','v1851d_historical_kinetic')
zhelper=load_module(ROOT/'reference/z_replay_helpers_v18_50z.py','v1851d_z_helpers')

def sha(b):return hashlib.sha256(b).hexdigest()
def auth(z,root,version):
    if z.testzip() is not None:raise RuntimeError('Parent ZIP CRC: '+root)
    sm=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
    if (sm['root'],sm.get('version',version),om['root'],om.get('version',version)) != (root,version,root,version):
        raise RuntimeError('Parent identity mismatch: '+root)
    paths={**sm['files'],**om['file_sha256']}
    actual={n[len(root)+1:] for n in z.namelist() if n.startswith(root+'/') and not n.endswith('/')}
    if actual!=set(paths)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}:
        raise RuntimeError('Parent member mismatch '+root)
    for rel,hexdigest in paths.items():
        if sha(z.read(root+'/'+rel))!=hexdigest:
            raise RuntimeError('Parent SHA256 mismatch '+root+'/'+rel)
    return dict(version=version,source_files=len(sm['files']),result_files=len(om['file_sha256']))

def npz_bytes(b):
    with np.load(io.BytesIO(b),allow_pickle=False) as z:return {n:z[n].copy() for n in z.files}

def load_ancestry():
    lineage={}
    with zipfile.ZipFile(PARENT) as z:
        lineage['c']=auth(z,C,'v18.51c')
        c_summary=json.loads(z.read(C+'/results/report.json'))
        c_table=list(csv.DictReader(io.StringIO(z.read(C+'/results/metric_spectral_source_phase_ledger.csv').decode())))
        bb=z.read(C+'/inputs/'+B+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(bb)) as z:
        lineage['b']=auth(z,B,'v18.51b'); aa=z.read(B+'/inputs/'+A+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(aa)) as z:
        lineage['a']=auth(z,A,'v18.51a'); zz=z.read(A+'/inputs/'+Z+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(zz)) as z:
        lineage['z']=auth(z,Z,'v18.50z')
        zdata=npz_bytes(z.read(Z+'/results/model_vs_canonical_centerline_tensors.npz'))
        yy=z.read(Z+'/inputs/'+Y+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(yy)) as z:
        lineage['y']=auth(z,Y,'v18.50y'); xx=z.read(Y+'/inputs/'+X+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(xx)) as z:
        lineage['x']=auth(z,X,'v18.50x')
        xdata=npz_bytes(z.read(X+'/results/full_projector_sensitivity_tensors.npz'))
        xcode=z.read(X+'/scripts/run_audit.py')
        wblob=z.read(X+'/inputs/'+W+'_server_sendback.zip')
    if not np.array_equal(zdata['xi'],xdata['xi']):raise RuntimeError('Ancestors use different time sections')
    lineage['parent_sha256']=sha(PARENT.read_bytes())
    lineage['historical_v18_49h_kinetic_source_sha256']=sha((ROOT/'reference/kinetic_metric_v18_49h.py').read_bytes())
    if lineage['historical_v18_49h_kinetic_source_sha256']!='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a':
        raise RuntimeError('Historical kinetic source bytes differ from original v18.49h')
    return lineage,c_summary,c_table,zdata,xdata,xcode,wblob

def sym(M):return (M+M.T)/2
def skew(M):return (M-M.T)/2
def fn(M):return float(np.linalg.norm(M,'fro'))
def dot(A,B):return float(np.einsum('ij,ij->',A,B))
def comm(A,B):return A@B-B@A

def spectral(W):
    W=skew(W)
    H=sym(-(W@W))
    vals,V=np.linalg.eigh(H)
    order=np.argsort(vals)[::-1]
    if vals[order[1]]-vals[order[2]]<1e-7 or vals[order[3]]-vals[order[4]]<1e-7:
        # A non-isolated channel cannot be assigned a reliable differential projector.
        return None
    q1=V[:,order[:2]]@V[:,order[:2]].T
    q2=V[:,order[2:4]]@V[:,order[2:4]].T
    eig1=float(np.mean(vals[order[:2]]));eig2=float(np.mean(vals[order[2:4]]))
    sigma3=float(np.sqrt(max(0.,np.mean(vals[order[4:6]]))))
    return H,q1,q2,eig1-eig2,float(np.sqrt(max(0,eig1))),float(np.sqrt(max(0,eig2))),sigma3

def passive_chart(L,W):
    # Same physical kinetic embedding under an invertible observer-coordinate chart.
    A=ID.copy();A[0,1]=.12;A[3,4]=-.08;A[8,9]=.19
    A=A@np.diag([1.3,.77,1.1,.93,1.4,.89,1.18,1.25,.91,1.07])
    Ai=np.linalg.inv(A)
    Lnew=L@Ai
    Wnew=A@W@Ai
    old=skew(L@W@np.linalg.inv(L))
    new=skew(Lnew@Wnew@np.linalg.inv(Lnew))
    G=L.T@L
    Gnew=Ai.T@G@Ai
    return {'physical_operator':fn(new-old)/max(1,fn(old)),
            'metric_pullback':fn(Gnew-Lnew.T@Lnew)/max(1,fn(Gnew)),
            'kinetic_dot':abs(float(np.trace(A.T@Gnew@A-G)))/max(1,fn(G))}

def integrate_seeds(zdata,xdata,xcode,wblob):
    # Regenerate 2 independent physical states along the EXACT inherited centerline.
    result={}
    with tempfile.TemporaryDirectory(prefix='v18_51d_kinetic_model_') as td:
        print('STAGING original authenticated solver genealogy',flush=True)
        v,vr,parts,auth_info=zhelper.stage_x_model(Path(td),xcode,wblob)
        t,q,p,o,engine,unit,drpt,creport,tinfo=parts
        mid=float(vr['kappa']['autonomous'])+0.5*float(vr['kappa']['delta'])
        ks=xdata['kappa'];ic=int(np.argmin(abs(ks-mid)))
        if abs(ks[ic]-mid)>1e-12:raise RuntimeError('Kappa midpoint mismatch')
        xs=np.asarray(xdata['xi'],float)
        scales=np.asarray(xdata['shared_scale_10d'],float)
        for seed in ('original','autonomous'):
            print('INTEGRATING seed',seed,flush=True)
            ctx=p.make_context(o,seed,engine,unit,drpt,creport)
            sol,rhs=v.make_ivp(engine,ctx,mid,float(xs[-1]),2e-10,2e-11,.00125)
            if not sol.success:raise RuntimeError('Physical IVP failed: '+seed)
            y=[];jdiff=[];en_err=[]
            for xi in xs:
                ti=float(ctx['event']+xi)
                yy=np.r_[np.asarray(sol.sol(ti),float),float(ctx['theta'](ti))]
                field,JF,_=engine.jet.structural_jet(yy,mid,engine.params,engine.slope)
                j=(scales[:,None]*JF[:10,:10])/scales[None,:]
                jdiff.append(fn(j-zdata['J_'+seed][len(y)])/max(1,fn(j)))
                # Preserve only the authentic 10D material state coordinates.
                y.append(yy[:10])
                h,_=kin.embedding_and_jac(yy[:10],engine.params.m_x,1.)
                rho1,rho2=np.exp(yy[0]),np.exp(yy[4]);xx=kin.sigmoid(yy[8]);xd=xx*(1-xx)*yy[9]
                expected=.5*(rho1**2*(yy[1]**2+yy[3]**2)+rho2**2*(yy[5]**2+yy[7]**2)+engine.params.m_x*xd**2)
                en_err.append(abs(.5*h[5:]@h[5:]-expected)/max(1,abs(expected)))
            result[seed]={'state':np.asarray(y),'mx':float(engine.params.m_x),'nfev':int(sol.nfev),
                'max_jet_relative_mismatch':float(max(jdiff)),'max_kinetic_energy_relative_mismatch':float(max(en_err))}
            print('SEED DONE',seed,'nfev',sol.nfev,'jet error',max(jdiff),flush=True)
    return result,mid,scales

def analyze_seed(seed,tau,states,scales,xi,Z,X):
    mx=states['mx'];state=states['state'];S=np.diag(scales)
    L=np.asarray([kin.embedding_and_jac(y,mx,tau)[1]@S for y in state])
    Lprime=CubicSpline(xi,L,axis=0).derivative()(xi)
    G=np.asarray([li.T@li for li in L]);Gprime=CubicSpline(xi,G,axis=0).derivative()(xi)
    P=X['P_'+seed][int(np.argmin(abs(X['offset_units']-.5)))]
    J=Z['J_'+seed];KC=Z['K_canonical_'+seed];KM=Z['K_model_'+seed]
    dP=CubicSpline(xi,P,axis=0).derivative()(xi)
    dJ=CubicSpline(xi,J,axis=0).derivative()(xi)
    dKC=CubicSpline(xi,KC,axis=0).derivative()(xi)
    dKM=CubicSpline(xi,KM,axis=0).derivative()(xi)
    rows=[];frames=[];max_g=np.linalg.cond(L[0]);passive=[]
    for i,x in enumerate(xi):
        Li=L[i];Linv=np.linalg.inv(Li);lp=Lprime[i]
        Gm=G[i];Gamma=Linv@lp;D=lp@Linv
        # Covariant metric compatibility in the shared 10D observer chart.
        gdot=lp.T@Li+Li.T@lp
        cov=fn(gdot-Gamma.T@Gm-Gm@Gamma)/max(1,fn(gdot))
        independent=fn(Gprime[i]-gdot)/max(1,fn(Gprime[i]))
        q=ID-P[i];p=P[i];pd=dP[i];ji=J[i];jd=dJ[i]
        s_gen=q@jd@p-p@jd.T@q
        s_post=-pd@ji@p+q@ji@pd-pd@ji.T@q+p@ji.T@pd
        s_can=-dKC[i]
        primitive=KM[i]-KC[i]
        prate=dKM[i]-dKC[i]
        src_error=fn(s_gen+s_post+s_can-prate)/max(1,fn(prate))
        A=Li@primitive@Linv
        W=skew(A)
        src={
         'generator':skew(Li@s_gen@Linv),
         'posture':skew(Li@s_post@Linv),
         'canonical':skew(Li@s_can@Linv),
         'metric_frame':skew(comm(D,A)),
        }
        Wprime=sum(src.values())
        spec=spectral(W)
        if spec is None:
            raise RuntimeError('First two spectral pairs not isolated at seed='+seed+', tau='+str(tau)+', xi='+str(x))
        H,Q1,Q2,gap,sigma1,sigma2,sigma3=spec
        ds={k:sym(-(v@W+W@v)) for k,v in src.items()}
        parts={k:Q2@h@Q1/gap for k,h in ds.items()}
        total=sum(parts.values());rate=fn(total)
        shares={k:dot(pv,total)/max(1e-28,rate**2) for k,pv in parts.items()}
        sym_fraction=fn(sym(A))/max(1e-28,fn(A))
        row={
         'seed_family':seed,'tau_ref':tau,'xi':float(x),'kappa':float(X['kappa'][int(np.argmin(abs(X['offset_units']-.5)))]),
         'kinetic_metric_condition':float(np.linalg.cond(Gm)),
         'jacobian_immersion_condition':float(np.linalg.cond(Li)),
         'kinetic_connection_norm':fn(Gamma),
         'connection_compatibility_residual':cov,
         'independent_metric_time_derivative_relative_error':independent,
         'original_source_identity_relative_error':src_error,
         'sigma1':sigma1,'sigma2':sigma2,'sigma3':sigma3,
         'dominant_pair_gap':gap,
         'interplane_rate':rate,
         'signed_generator':shares['generator'],
         'signed_posture':shares['posture'],
         'signed_model_total':shares['generator']+shares['posture'],
         'signed_canonical':shares['canonical'],
         'signed_kinetic_frame':shares['metric_frame'],
         'signed_fraction_sum_error':abs(sum(shares.values())-1),
         'metric_skew_projection_removed_symmetric_fraction':sym_fraction,
         'source_model_interplane_norm':fn(parts['generator']+parts['posture']),
         'source_canonical_interplane_norm':fn(parts['canonical']),
         'source_kinetic_frame_interplane_norm':fn(parts['metric_frame']),
        }
        rows.append(row)
        if i in (0,len(xi)//2,len(xi)-1):passive.append({'seed_family':seed,'tau_ref':tau,'xi':float(x),**passive_chart(Li,primitive)})
        frames.append(W)
        max_g=max(max_g,float(np.linalg.cond(Gm)))
    Wsp=CubicSpline(xi,np.asarray(frames),axis=0).derivative()(xi)
    for i,row in enumerate(rows):
        # Independent numerical rate, including the metric-frame contribution.
        li=L[i];linv=np.linalg.inv(li);gdot=Lprime[i]@linv
        prim=KM[i]-KC[i];a=li@prim@linv;p=P[i];q=ID-p;pd=dP[i];j=J[i]
        sgen=q@dJ[i]@p-p@dJ[i].T@q
        spost=-pd@j@p+q@j@pd-pd@j.T@q+p@j.T@pd
        calculated=skew(li@(sgen+spost-dKC[i])@linv + comm(gdot,a))
        row['independent_kinetic_W_rate_relative_error']=fn(calculated-Wsp[i])/max(1,fn(Wsp[i]))
    return rows,passive

def save_csv(path,rows):
    if not rows:raise RuntimeError('Empty table')
    with open(path,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def graphs(rows):
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[v for v in rows if v['seed_family']==seed and v['tau_ref']==tau]
            ax.plot([r['xi'] for r in rr],[100*r['signed_canonical'] for r in rr],label=f'tau_ref={tau:g}')
        ax.set(xlabel='Evolution ξ',ylabel='Signed canonical share (%)',title=seed)
        ax.grid(alpha=.2);ax.legend()
    fig.suptitle('v18.51d | Canonical attribution under historical kinetic pullback family')
    fig.tight_layout();fig.savefig(OUT/'kinetic_metric_source_attribution.png',dpi=155);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[v for v in rows if v['seed_family']==seed and v['tau_ref']==tau]
            ax.plot([r['xi'] for r in rr],[100*r['signed_kinetic_frame'] for r in rr],label=f'tau_ref={tau:g}')
        ax.set(xlabel='Evolution ξ',ylabel='Signed kinetic-frame rate source (%)',title=seed)
        ax.grid(alpha=.2);ax.legend()
    fig.suptitle('v18.51d | Explicit moving kinetic-frame source')
    fig.tight_layout();fig.savefig(OUT/'moving_kinetic_frame_source.png',dpi=155);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12,4.8),sharey=True)
    for ax,seed in zip(axes,('original','autonomous')):
        for tau in TAUS:
            rr=[v for v in rows if v['seed_family']==seed and v['tau_ref']==tau]
            ax.plot([r['xi'] for r in rr],[r['sigma3'] for r in rr],label=f'tau_ref={tau:g}')
        ax.set(xlabel='Evolution ξ',ylabel='Third singular pair',title=seed)
        ax.grid(alpha=.2);ax.legend()
    fig.suptitle('v18.51d | Secondary spectrum in kinetic state geometry')
    fig.tight_layout();fig.savefig(OUT/'kinetic_metric_secondary_spectrum.png',dpi=155);plt.close(fig)

def run():
    OUT.mkdir(exist_ok=True)
    lineage,c_summary,c_table,z,x,xcode,wblob=load_ancestry()
    print('AUTHENTICATED c,b,a,z,y,x and historical v18.49h kinetic formula',flush=True)
    states,mid,scales=integrate_seeds(z,x,xcode,wblob)
    xi=np.asarray(z['xi'],float)
    rows=[];passive=[]
    for seed in ('original','autonomous'):
        for tau in TAUS:
            rr,pp=analyze_seed(seed,tau,states[seed],scales,xi,z,x)
            rows+=rr;passive+=pp
            print('KINETIC BRANCH',seed,tau,'canon share end',rr[-1]['signed_canonical'],
                  'compat max',max(r['connection_compatibility_residual'] for r in rr),flush=True)
    save_csv(OUT/'kinetic_metric_spectral_source_ledger.csv',rows)
    save_csv(OUT/'passive_kinetic_chart_controls.csv',passive)
    comparisons=[]
    for seed in ('original','autonomous'):
        b=[r for r in c_table if r['seed_family']==seed and r['metric']=='euclidean']
        b.sort(key=lambda r:float(r['xi']))
        for tau in TAUS:
            rr=[r for r in rows if r['seed_family']==seed and r['tau_ref']==tau]
            comparisons.append({'seed_family':seed,'tau_ref':tau,'sections':len(rr),
                'canonical_start':rr[0]['signed_canonical'],'canonical_end':rr[-1]['signed_canonical'],
                'canonical_exceeds_model_end':rr[-1]['signed_canonical']>rr[-1]['signed_model_total'],
                'canonical_exceeds_model_all_samples':all(r['signed_canonical']>r['signed_model_total'] for r in rr),
                'model_end':rr[-1]['signed_model_total'],'frame_end':rr[-1]['signed_kinetic_frame'],
                'euclidean_b_canonical_start':float(b[0]['signed_canonical']),
                'euclidean_b_canonical_end':float(b[-1]['signed_canonical']),
                'sigma3_max':max(r['sigma3'] for r in rr),
                'max_G_condition':max(r['kinetic_metric_condition'] for r in rr),
                'max_independent_W_rate_error':max(r['independent_kinetic_W_rate_relative_error'] for r in rr),
                'max_metric_rate_error':max(r['independent_metric_time_derivative_relative_error'] for r in rr),
                'max_compatibility_error':max(r['connection_compatibility_residual'] for r in rr)})
    save_csv(OUT/'kinetic_vs_model_gram_source_summary.csv',comparisons)
    graphs(rows)
    checks={
      'lineage_c_b_a_z_y_x_authenticated':len(lineage)==8,
      'historical_kinetic_implementation_hash':lineage['historical_v18_49h_kinetic_source_sha256']=='29bef2c91899a9da46bc8c9159b89c70362f505e0adead3f814c487a9a17bb1a',
      'two_physical_seed_ivps_completed':len(states)==2 and all(q['nfev']>0 for q in states.values()),
      'kinetic_energy_matches_original':max(q['max_kinetic_energy_relative_mismatch'] for q in states.values())<2e-12,
      'model_jacobian_kinematic_replay':max(q['max_jet_relative_mismatch'] for q in states.values())<1e-6,
      'two_seeds_three_tau_79_sections':len(rows)==474,
      'kinetic_compatible_connection_identity':max(r['connection_compatibility_residual'] for r in rows)<5e-9,
      'source_identity':max(r['original_source_identity_relative_error'] for r in rows)<1e-4,
      'weighted_spectral_ledger_sum':max(r['signed_fraction_sum_error'] for r in rows)<1e-8,
      'passive_chart_covariance':max(max(rr['physical_operator'],rr['metric_pullback'],rr['kinetic_dot']) for rr in passive)<1e-10,
      'finite_metric_condition':max(r['kinetic_metric_condition'] for r in rows)<1e14,
      'kinetic_embedding_rate_independent_check':max(r['independent_kinetic_W_rate_relative_error'] for r in rows)<3e-3,
    }
    classification=('KINETIC_PULLBACK_COMPATIBLE_CONNECTION_DIAGNOSTIC_NOT_UNIQUE_PHYSICAL_PHASE_METRIC_OR_MATERIAL_CAUSALITY')
    report={'version':'v18.51d',
       'title':'Kinetic-Metric Construction & Connection Compatibility Audit',
       'classification':classification,
       'construction':'Authentic Q550 v18.49h 5D kinetic Cartesian configuration Q; Sasaki-type material 10D H=(Q,tau_ref V). G=(DH diag(shared_scale))^T(DH diag(shared_scale)), Gamma=L^-1 Lprime.',
       'source_split':'Inherited b: generator J drift + P posture - canonical drift; explicit additional frame commutator in Cartesian kinetic embedding.',
       'metric_weighting_tau_ref':list(TAUS),'kappa_midpoint':mid,'xi_max':float(xi[-1]),
       'lineage':lineage,'new_physical_10D_ivps':2,
       'new_ivp_nfev':{seed:q['nfev'] for seed,q in states.items()},
       'observations':len(rows),'passive_chart_controls':len(passive),
       'comparisons':comparisons,'checks':checks,
       'max_errors':{
        'metric_compatibility':max(r['connection_compatibility_residual'] for r in rows),
        'independent_kinetic_frame_rate':max(r['independent_kinetic_W_rate_relative_error'] for r in rows),
        'independent_metric_time_rate':max(r['independent_metric_time_derivative_relative_error'] for r in rows),
        'historical_jet_replay':max(q['max_jet_relative_mismatch'] for q in states.values()),
        'historical_kinetic_energy':max(q['max_kinetic_energy_relative_mismatch'] for q in states.values())},
       'limitations':[
        'The tau-time kinetic energy fixes the Cartesian configuration metric. Its Sasaki-type material state extension uses a freely declared tau_ref and is not unique.',
        'Two Q550 trajectories are recomputed at the same midpoint kappa; they correspond to differently prepared natural seeds, not two concurrent distinct-kappa boundaries.',
        'The original Q550 driven dynamics is not proven to preserve the kinetic state metric; compatible connection identity is a geometric statement.',
        'The metric-skew part discards symmetric strain; its spectral-source fractions do not quantify energy.',
        'Whitening and Cartesian embedding choices affect how matrix rates are attributed; moving-frame contribution is reported explicitly.',
        'Both original model and observed projector data come from authenticated ancestors; new fitted parameters or new physical laws are not introduced.',
        'Spline-derived Lprime, dJ and dP are numerical, not interval-certified. No material torsion or hysteresis certification.',
       ],
       'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('v18.51d COMPLETED',json.dumps({'checks':checks,'comparisons':comparisons},indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('Failed one or more declared scientific controls')

if __name__=='__main__':run()
