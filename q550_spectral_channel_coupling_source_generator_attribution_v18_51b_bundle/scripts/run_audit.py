#!/usr/bin/env python3
"""v18.51b: authenticated spectral generator attribution of W = Kmodel-Kcanonical.

No physical IVP is solved. Differentiation of 79 saved samples is diagnostic,
not analytic in the independent evolution variable. The 10D common Euclidean
chart, reference preparations and midpoint kappa are inherited unchanged.
"""
from __future__ import annotations
import csv,hashlib,io,json,platform,zipfile
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PARENT_A='q550_model_observer_connection_defect_spectral_channels_transport_v18_51a_bundle'
PARENT_Z='q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle'
PARENT_Y='q550_covariant_sensitivity_transport_time_derivative_attribution_v18_50y_bundle'
PARENT_X='q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle'
INPUT=ROOT/'inputs'/(PARENT_A+'_server_sendback.zip')
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)


def sha(b):return hashlib.sha256(b).hexdigest()

def authenticate(z,root,version):
    if z.testzip() is not None:raise RuntimeError('ZIP CRC failed '+root)
    sm=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
    if (sm['root'],om['root'],sm['version'],om.get('version',version))!=(root,root,version,version):
        raise RuntimeError('Wrong parent root/version '+root)
    files={**sm['files'],**om['file_sha256']}
    actual={n[len(root)+1:] for n in z.namelist() if n.startswith(root+'/') and not n.endswith('/')}
    if actual!=set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}:
        raise RuntimeError('Unexpected parent ZIP members '+str(actual^(set(files)|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'})))
    for name,expected in files.items():
        if sha(z.read(root+'/'+name))!=expected:raise RuntimeError('Ancestor SHA mismatch '+root+':'+name)
    return {'version':version,'sources':len(sm['files']),'outputs':len(om['file_sha256'])}


def authentic_data():
    with zipfile.ZipFile(INPUT) as a:
        lineage={'v18.51a':authenticate(a,PARENT_A,'v18.51a')}
        parent_z_bytes=a.read(PARENT_A+'/inputs/'+PARENT_Z+'_server_sendback.zip')
        a_npz=a.read(PARENT_A+'/results/dominant_spectral_channel_projectors.npz')
    with zipfile.ZipFile(io.BytesIO(parent_z_bytes)) as z:
        lineage['v18.50z']=authenticate(z,PARENT_Z,'v18.50z')
        z_npz=z.read(PARENT_Z+'/results/model_vs_canonical_centerline_tensors.npz')
        parent_y_bytes=z.read(PARENT_Z+'/inputs/'+PARENT_Y+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(parent_y_bytes)) as y:
        lineage['v18.50y']=authenticate(y,PARENT_Y,'v18.50y')
        parent_x_bytes=y.read(PARENT_Y+'/inputs/'+PARENT_X+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(parent_x_bytes)) as x:
        lineage['v18.50x']=authenticate(x,PARENT_X,'v18.50x')
        x_npz=x.read(PARENT_X+'/results/full_projector_sensitivity_tensors.npz')
    def load(b):
        with np.load(io.BytesIO(b),allow_pickle=False) as d:return {k:np.array(d[k],copy=True) for k in d.files}
    a,z,x=load(a_npz),load(z_npz),load(x_npz)
    if not (np.allclose(a['xi'],z['xi'],rtol=0,atol=1e-14) and np.allclose(x['xi'],z['xi'],rtol=0,atol=1e-14)):
        raise RuntimeError('Evolution grids differ')
    mid=0.5*(1/6+7*np.pi/132)
    kidx=int(np.argmin(abs(x['kappa']-mid)))
    if abs(x['kappa'][kidx]-mid)>1e-13:raise RuntimeError('Midpoint not in parent 10D projector grid')
    lineage['parent_a_sha256']=sha(INPUT.read_bytes())
    lineage['shared_kappa_midpoint']=mid
    lineage['x_kappa_index']=kidx
    return a,z,x,lineage


def nrm(m):return float(np.linalg.norm(m,ord='fro'))
def inner(a,b):return float(np.einsum('ij,ij->',a,b))
def sym(m):return .5*(m+m.T)
def skew(m):return .5*(m-m.T)
def five_point_derivative(x,Y):
    """Local nonuniform 5-node polynomial derivative, independent of spline."""
    out=np.empty_like(Y)
    for i in range(len(x)):
        left=min(max(i-2,0),len(x)-5)
        idx=np.arange(left,left+5)
        scale=np.max(abs(x[idx]-x[i]))
        t=(x[idx]-x[i])/scale
        V=np.array([t**j for j in range(5)])
        e=np.zeros(5);e[1]=1
        w=np.linalg.solve(V,e)/scale
        out[i]=np.tensordot(w,Y[idx],axes=(0,0))
    return out


def projectors_from_defect(W):
    U,s,_=np.linalg.svd(W)
    p1=U[:,:2]@U[:,:2].T
    p2=U[:,2:4]@U[:,2:4].T
    sig1=.5*(s[0]+s[1]);sig2=.5*(s[2]+s[3])
    if sig1<sig2+.5 or sig2<.1:raise RuntimeError('Spectral pair gap closed')
    return p1,p2,sig1,sig2


def one_branch(seed,idx,xi,a,z,x):
    M=z['K_model_'+seed];C=z['K_canonical_'+seed];J=z['J_'+seed]
    P=x['P_'+seed][idx]
    n=len(xi);Id=np.eye(10)
    if any(arr.shape!=(n,10,10) for arr in (M,C,J,P)):
        raise RuntimeError('Unexpected operator dimensions '+seed)
    dM=CubicSpline(xi,M,axis=0).derivative()(xi)
    dC=CubicSpline(xi,C,axis=0).derivative()(xi)
    dJ=CubicSpline(xi,J,axis=0).derivative()(xi)
    dP=CubicSpline(xi,P,axis=0).derivative()(xi)
    dM5=five_point_derivative(xi,M)
    dC5=five_point_derivative(xi,C)
    q1=a['projector_pair1_'+seed]
    q2=a['projector_pair2_'+seed]
    dQ1=CubicSpline(xi,q1,axis=0).derivative()(xi)
    strengths=a['skew_singular_pair_strengths_'+seed]
    rows=[];blocks={'generator_drift':[],'observer_posture':[],'canonical_connection':[], 'total':[]}
    identity_errors=[];dlog_inputs={'xi':xi,'gap':[],'numerator':[],'rate':[]}
    for i,t in enumerate(xi):
        p=P[i];pd=dP[i];j=J[i];jd=dJ[i];q=Id-p
        km=q@j@p-p@j.T@q
        if nrm(M[i]-km)>1e-9:raise RuntimeError('Original model offblock reconstruction mismatch')
        # The exact derivative of (I-P)JP-P J^T(I-P):
        dkm_generator=q@jd@p-p@jd.T@q
        dkm_posture=-pd@j@p+q@j@pd-pd@j.T@q+p@j.T@pd
        dm_model=dkm_generator+dkm_posture
        dm_can=dC[i]
        W=M[i]-C[i]
        Q1=q1[i];Q2=q2[i]
        H=-W@W
        lam1=inner(Q1,H)/2;lam2=inner(Q2,H)/2
        gap=lam1-lam2
        if gap<1:raise RuntimeError('Gap too small')
        # Hdot = -(Wdot W+ W Wdot), with Wdot=Kmodel' - Kcanonical'.
        dH_J=-(dkm_generator@W+W@dkm_generator)
        dH_P=-(dkm_posture@W+W@dkm_posture)
        dH_can=(dm_can@W+W@dm_can)
        dH_model=dH_J+dH_P
        dH=dH_model+dH_can
        B_J=Q2@dH_J@Q1/gap
        B_P=Q2@dH_P@Q1/gap
        B_can=Q2@dH_can@Q1/gap
        B_m=B_J+B_P
        Btot=B_m+B_can
        observed=Q2@dQ1[i]@Q1
        bnorm=nrm(Btot)
        if bnorm<1e-9:raise RuntimeError('Near-zero interpair rate')
        bJ=nrm(B_J);bP=nrm(B_P);bC=nrm(B_can);bM=nrm(B_m)
        cosMC=inner(B_m,B_can)/max(bM*bC,1e-300)
        signed={k:inner(v,Btot)/bnorm**2 for k,v in [('j',B_J),('p',B_P),('can',B_can)]}
        dlam1_J=inner(Q1,dH_J)/2;dlam1_P=inner(Q1,dH_P)/2;dlam1_can=inner(Q1,dH_can)/2
        dlam2_J=inner(Q2,dH_J)/2;dlam2_P=inner(Q2,dH_P)/2;dlam2_can=inner(Q2,dH_can)/2
        source1=[dlam1_J/(2*np.sqrt(lam1)),dlam1_P/(2*np.sqrt(lam1)),dlam1_can/(2*np.sqrt(lam1))]
        source2=[dlam2_J/(2*np.sqrt(lam2)),dlam2_P/(2*np.sqrt(lam2)),dlam2_can/(2*np.sqrt(lam2))]
        directgap=(dlam1_J+dlam1_P+dlam1_can)-(dlam2_J+dlam2_P+dlam2_can)
        fullnum=nrm(Q2@dH@Q1)
        rows.append(dict(seed_family=seed,xi=float(t),
            sigma_pair1=float(strengths[i,0]),sigma_pair2=float(strengths[i,1]),lambda_gap=gap,
            numerator_norm=fullnum,coupling_rate_spectral=bnorm,coupling_rate_direct=nrm(observed),
            projector_velocity_identity_error=nrm(Btot-observed)/nrm(observed),
            model_generator_drift_rate=bJ,model_projector_posture_rate=bP,
            canonical_observer_rate=bC,model_total_rate=bM,
            signed_generator_fraction=signed['j'],signed_posture_fraction=signed['p'],
            signed_canonical_fraction=signed['can'],signed_model_total_fraction=signed['j']+signed['p'],
            cosine_model_vs_canonical=cosMC,
            norm_ratio_canonical_to_model=bC/bM,
            sigma1_rate_generator=source1[0],sigma1_rate_posture=source1[1],sigma1_rate_canonical=source1[2],
            sigma2_rate_generator=source2[0],sigma2_rate_posture=source2[1],sigma2_rate_canonical=source2[2],
            spectral_gap_derivative=directgap,
            analytic_model_offblock_derivative_residual=nrm(dm_model-dM[i])/max(nrm(dM[i]),1),
            spline_5pt_model_derivative_residual=nrm(dM[i]-dM5[i])/max(nrm(dM[i]),1),
            spline_5pt_canonical_derivative_residual=nrm(dC[i]-dC5[i])/max(nrm(dC[i]),1),
            skew_rate_residual=nrm(dH-dH.T)/max(nrm(dH),1),
            ))
        for key,matrix in [('generator_drift',B_J),('observer_posture',B_P),('canonical_connection',B_can),('total',Btot)]:
            blocks[key].append(matrix)
        identity_errors.append(nrm(Btot-observed))
        dlog_inputs['gap'].append(gap);dlog_inputs['numerator'].append(fullnum);dlog_inputs['rate'].append(bnorm)
    for k in list(blocks):blocks[k]=np.array(blocks[k])
    for k in ('gap','numerator','rate'):dlog_inputs[k]=np.array(dlog_inputs[k])
    # Equivalent rate evolution: d log(rate) = d log(numerator) - d log(gap).
    logs={k:CubicSpline(xi,np.log(dlog_inputs[k])).derivative()(xi) for k in ('gap','numerator','rate')}
    for i,r in enumerate(rows):
        r.update(dlog_numerator=logs['numerator'][i],dlog_gap=logs['gap'][i],
                 dlog_coupling_rate=logs['rate'][i],
                 log_rate_balance_error=abs(logs['rate'][i]-(logs['numerator'][i]-logs['gap'][i])))
    return rows,blocks


def write_csv(filename,rows):
    with open(OUT/filename,'w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)


def render(byseed):
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,rows in byseed.items():
        t=np.array([r['xi'] for r in rows]);
        axs[0].plot(t,[r['model_total_rate'] for r in rows],label=f'{seed}: model')
        axs[0].plot(t,[r['canonical_observer_rate'] for r in rows],'--',label=f'{seed}: canonical')
        axs[0].plot(t,[r['coupling_rate_spectral'] for r in rows],':',label=f'{seed}: combined')
        axs[1].plot(t,[r['signed_model_total_fraction'] for r in rows],label=f'{seed}: model signed fraction')
        axs[1].plot(t,[r['signed_canonical_fraction'] for r in rows],ls='--',label=f'{seed}: canonical signed fraction')
    axs[0].set_ylabel('Inter-plane source rate (Frobenius)');axs[0].legend(ncol=2,fontsize=8)
    axs[1].set_ylabel('Signed projection onto combined rate');axs[1].set_xlabel('Evolution coordinate ξ');axs[1].legend(ncol=2,fontsize=8)
    fig.suptitle('v18.51b | Connection-source decomposition of spectral interplane transport')
    fig.tight_layout();fig.savefig(OUT/'connection_source_interplane_transport.png',dpi=160);plt.close(fig)

    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,rows in byseed.items():
        t=np.array([r['xi'] for r in rows])
        axs[0].plot(t,[r['sigma1_rate_generator'] for r in rows],label=f'{seed}: generator contribution')
        axs[0].plot(t,[r['sigma1_rate_posture'] for r in rows],ls=':',label=f'{seed}: projector posture')
        axs[0].plot(t,[r['sigma1_rate_canonical'] for r in rows],ls='--',label=f'{seed}: canonical')
        axs[1].plot(t,[r['sigma2_rate_generator'] for r in rows],label=f'{seed}: generator contribution')
        axs[1].plot(t,[r['sigma2_rate_posture'] for r in rows],ls=':',label=f'{seed}: projector posture')
        axs[1].plot(t,[r['sigma2_rate_canonical'] for r in rows],ls='--',label=f'{seed}: canonical')
    axs[0].set_ylabel('Derivative of first singular strength');axs[1].set_ylabel('Derivative of second singular strength');axs[1].set_xlabel('Evolution coordinate ξ')
    axs[0].legend(ncol=2,fontsize=8);axs[1].legend(ncol=2,fontsize=8)
    fig.suptitle('v18.51b | Generator, projector posture and canonical observer')
    fig.tight_layout();fig.savefig(OUT/'generator_posture_spectral_strength_attribution.png',dpi=160);plt.close(fig)

    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,rows in byseed.items():
        t=np.array([r['xi'] for r in rows]);
        axs[0].plot(t,[r['dlog_numerator'] for r in rows],label=f'{seed}: numerator log-rate')
        axs[0].plot(t,[-r['dlog_gap'] for r in rows],ls='--',label=f'{seed}: negative gap log-rate')
        axs[1].plot(t,[r['dlog_coupling_rate'] for r in rows],label=f'{seed}: total log-rate')
    axs[0].legend(fontsize=8,ncol=2);axs[0].set_ylabel('Contributions to d log(rate)/dξ')
    axs[1].legend();axs[1].set_ylabel('d log(interplane rate)/dξ');axs[1].set_xlabel('Evolution coordinate ξ')
    fig.suptitle('v18.51b | Numerator-versus-gap competition (same measured spectral flow)')
    fig.tight_layout();fig.savefig(OUT/'spectral_numerator_gap_rate_balance.png',dpi=160);plt.close(fig)


def main():
    a,z,x,lineage=authentic_data()
    xi=np.asarray(z['xi'],float)
    if len(xi)!=79 or xi[0]!=0 or abs(xi[-1]-.05)>1e-14 or np.any(np.diff(xi)<=0):
        raise RuntimeError('Unexpected historical section grid')
    mid=lineage['x_kappa_index'];byseed={};allblocks={}
    for seed in ('original','autonomous'):
        rows,blocks=one_branch(seed,mid,xi,a,z,x)
        byseed[seed]=rows
        for name,val in blocks.items():allblocks[name+'_'+seed]=val
    rows=byseed['original']+byseed['autonomous']
    write_csv('spectral_source_attribution_phase_ledger.csv',rows)
    render(byseed)
    np.savez_compressed(OUT/'spectral_generator_attribution_blocks.npz',xi=xi,**allblocks)
    per={}
    for seed,rr in byseed.items():
        r0,rend=rr[0],rr[-1]
        per[seed]={
            'samples':len(rr), 'start':{k:float(v) for k,v in r0.items() if k not in ('seed_family','xi')},
            'end':{k:float(v) for k,v in rend.items() if k not in ('seed_family','xi')},
            'max_spectral_projector_derivative_relative_residual':max(r['projector_velocity_identity_error'] for r in rr),
            'max_model_product_derivative_relative_residual':max(r['analytic_model_offblock_derivative_residual'] for r in rr),
            'max_5point_versus_spline_relative_residual':max(max(r['spline_5pt_model_derivative_residual'],r['spline_5pt_canonical_derivative_residual']) for r in rr),
            'max_log_rate_balance_error':max(r['log_rate_balance_error'] for r in rr),
            'all_canonical_source_norms_larger_than_model':all(r['canonical_observer_rate']>r['model_total_rate'] for r in rr),
            'all_model_strength_derivative_dominant_pair1':all(abs(r['sigma1_rate_generator']+r['sigma1_rate_posture'])>abs(r['sigma1_rate_canonical']) for r in rr),
            'pair1_strength_increasing_all_samples':all((r['sigma1_rate_generator']+r['sigma1_rate_posture']+r['sigma1_rate_canonical'])>0 for r in rr),
            'pair2_strength_decreasing_all_samples':all((r['sigma2_rate_generator']+r['sigma2_rate_posture']+r['sigma2_rate_canonical'])<0 for r in rr),
        }
    checks={
       'both_preparations_present':len(rows)==158,
       'spectral_eigenprojector_identity':max(p['max_spectral_projector_derivative_relative_residual'] for p in per.values())<2e-6,
       'model_generator_product_rule':max(p['max_model_product_derivative_relative_residual'] for p in per.values())<2e-6,
       'independent_time_stencils':max(p['max_5point_versus_spline_relative_residual'] for p in per.values())<1e-4,
       'numerator_gap_log_identity':bool(max(p['max_log_rate_balance_error'] for p in per.values())<1e-7),
       'canonical_source_larger_norm_in_interplane_coupling':all(p['all_canonical_source_norms_larger_than_model'] for p in per.values()),
       'first_strength_increasing':all(p['pair1_strength_increasing_all_samples'] for p in per.values()),
       'second_strength_decreasing':all(p['pair2_strength_decreasing_all_samples'] for p in per.values()),
       'model_larger_strength_source_pair1':all(p['all_model_strength_derivative_dominant_pair1'] for p in per.values()),
    }
    if not all(checks.values()):raise RuntimeError('Scientific checks not met: '+str(checks))
    write_csv('spectral_source_attribution_summary.csv',[{'seed_family':k,
       'model_rate_start':v['start']['model_total_rate'], 'canonical_rate_start':v['start']['canonical_observer_rate'],
       'total_rate_start':v['start']['coupling_rate_spectral'],
       'model_rate_end':v['end']['model_total_rate'],'canonical_rate_end':v['end']['canonical_observer_rate'],
       'total_rate_end':v['end']['coupling_rate_spectral'],
       'sigma1_rate_start':sum(v['start']['sigma1_rate_'+nm] for nm in ('generator','posture','canonical')),
       'sigma2_rate_start':sum(v['start']['sigma2_rate_'+nm] for nm in ('generator','posture','canonical')),
       'max_projection_identity_relative_error':v['max_spectral_projector_derivative_relative_residual']
       } for k,v in per.items()])
    report={
       'version':'v18.51b','title':'Spectral-Channel Coupling Source & Generator Attribution Audit',
       'classification':'AUTHENTICATED_NUMERICAL_SPECTRAL_SOURCE_IDENTITY_NOT_UNIQUE_CAUSAL_OR_MATERIAL_ENERGY_ATTRIBUTION',
       'lineage':lineage,'samples':len(rows),'shared_kappa_midpoint':lineage['shared_kappa_midpoint'],
       'family_definition':'Two original natural-seed preparations replayed at ONE common midpoint kappa, not two moving kappa branches',
       'results':per,'checks':checks,
       'definitions':{
           'W':'K_model - K_canonical, skew offblock difference in common Euclidean 10D chart',
           'H':'-W^2, symmetric positive semidefinite; sigma_i^2 double eigenvalues',
           'Q1_Q2':'rank-2 dominant eigenprojectors of H from authenticated v18.51a',
           'gap':'lambda_1-lambda_2=sigma_1^2-sigma_2^2',
           'rate_block':'Q2 (dQ1/dxi) Q1 = Q2 (dH/dxi) Q1 / gap',
           'Hdot_source':'- {Kmodel_prime,W} + {Kcanonical_prime,W}, where {a,b}=ab+ba',
           'Kmodel':'(I-P)J P - P J^T(I-P); J is inherited analytic Q550 model tangent generator',
           'Kmodel_prime_generator':'(I-P) Jprime P - P Jprime^T(I-P)',
           'Kmodel_prime_posture':'-Pprime J P + (I-P)J Pprime - Pprime J^T(I-P) + P J^T Pprime',
           'signed_rate_fraction':'Frobenius projection <source_block,total_block>/||total_block||²; algebraic fractions sum to one',
           'strength_rate':'d sigma_i/dxi = Tr(Q_i Hprime)/(4 sigma_i)',
           'rate_gap_log_balance':'d log||Q2 Hprime Q1/gap|| = d log||Q2 Hprime Q1|| - d log(gap)',
           'derivative':'CubicSpline time derivative from 79 nonuniform saved ξ sections; independently cross-checked against local nonuniform 5-point formula',
       },
       'limitations':[
           'Post-processing of authenticated v18.51a/z/y/x tensor files; no new Q550 physical or tangent integrations.',
           'Kmodel is the skew offblock reduction of analytic J10 using observed P, not the entire nonorthogonal tangent flow.',
           'Model generator-drift attribution and observer-posture attribution arise from a product rule, not independent causal interventions.',
           'All rates, projectors, gaps and norms depend on the declared Euclidean common 10D chart and on the observed P.',
           'Numerical differentiation of saved phases is not a certified continuous-time derivative. Bounds reported are empirical cross-stencil diagnostics.',
           'The near-zero third singular pair is not assigned a stable physical channel.',
           'Strength derivatives and coupling rates are not physical energies or material-transfer rates.',
           'The two preparations use the same midpoint kappa; no critical-band or material memory certificate follows.'
       ],
       'environment':{'python':platform.python_version(),'numpy':np.__version__, 'scipy':'CubicSpline'}
    }
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('v18.51b COMPLETED',json.dumps({'rows':len(rows),'tests':checks,
        'original_start':{k:per['original']['start'][k] for k in ['model_total_rate','canonical_observer_rate','coupling_rate_spectral','sigma1_rate_generator','sigma1_rate_posture','sigma1_rate_canonical']},
        'original_end':{k:per['original']['end'][k] for k in ['model_total_rate','canonical_observer_rate','coupling_rate_spectral']},
        'max_id_err':max(d['max_spectral_projector_derivative_relative_residual'] for d in per.values())},indent=2))

if __name__=='__main__':main()
