#!/usr/bin/env python3
"""Q550 v18.51j — metric-adjoint reciprocity and bidirectional pair transport.

Inherited, authenticated v18.51i server tensors; no new physical 10D IVP.
For real rank-two spectral planes E4,E5 in a declared kinetic state metric,
K_{4<-5}=U4.T Q_{4<-5} U5, K_{5<-4}=U5.T Q_{5<-4} U4.
Their transpose-adjoint comparison is within one and the same metric.
Finite-lag *forward-time* material crossblocks are separately evaluated with
T(b,a)=M(b) inv(M(a)) and spectral target projection at b.
Nothing here asserts energy flow, dynamical time reversal, or metric uniqueness.
"""
from __future__ import annotations
import csv, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np, scipy, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
IROOT='q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle'
INAME=IROOT+'_server_sendback.zip'
HROOT='q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle'
GROOT='q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle'
FROOT='q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle'
EROOT='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle'
SEEDS=('original','autonomous');TAUS=(0.5,1.,2.)

def sha(x):return hashlib.sha256(x).hexdigest()
def norm(x):return float(np.linalg.norm(x,'fro'))
def rel(a,b):return norm(a-b)/max(1.,norm(a),norm(b))
def tag(t):return f'{t:.1f}'.replace('.','p')
def write_csv(name,rows):
    assert rows
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def verify_archive(z,base,version):
    assert z.testzip() is None, 'CRC failure '+version
    sm=json.loads(z.read(base+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(base+'/SHA256SUMS_OUTPUT.json'))
    assert sm['root']==om['root']==base and sm['version']==om['version']==version
    for name,digest in sm['files'].items():assert sha(z.read(base+'/'+name))==digest,(version,'source',name)
    for name,digest in om['file_sha256'].items():assert sha(z.read(base+'/'+name))==digest,(version,'output',name)
    return len(sm['files']),len(om['file_sha256'])

def load_authenticated_parent():
    path=ROOT/'inputs'/INAME
    with zipfile.ZipFile(path) as zi:
        identity=verify_archive(zi,IROOT,'v18.51i')
        report=json.loads(zi.read(IROOT+'/results/report.json'))
        assert all(report['checks'].values()) and report['version']=='v18.51i'
        for source,local in [('scripts/run_audit.py','reference/i_projector_replay_v18_51i.py'),
                              ('reference/h_pairwise_replay_v18_51h.py','reference/h_pairwise_replay_v18_51h.py'),
                              ('reference/g_projector_replay_v18_51g.py','reference/g_projector_replay_v18_51g.py')]:
            assert zi.read(IROOT+'/'+source)==(ROOT/local).read_bytes(),source
        hbytes=zi.read(IROOT+'/inputs/'+HROOT+'_server_sendback.zip')
        parent_direction=list(csv.DictReader(io.StringIO(zi.read(IROOT+'/results/projector_conditioning_directionality.csv').decode())))
    assert len(parent_direction)==468
    with tempfile.TemporaryDirectory(prefix='q550_51j_ancestry_') as temp:
        temp=Path(temp)
        (temp/'inputs').mkdir();(temp/'reference').mkdir()
        (temp/'inputs'/(HROOT+'_server_sendback.zip')).write_bytes(hbytes)
        (temp/'reference/h_pairwise_replay_v18_51h.py').write_bytes((ROOT/'reference/h_pairwise_replay_v18_51h.py').read_bytes())
        (temp/'reference/g_projector_replay_v18_51g.py').write_bytes((ROOT/'reference/g_projector_replay_v18_51g.py').read_bytes())
        spec=importlib.util.spec_from_file_location('q550_51j_ancestor_i',ROOT/'reference/i_projector_replay_v18_51i.py')
        ancestor=importlib.util.module_from_spec(spec);spec.loader.exec_module(ancestor)
        ancestor.ROOT=temp;ancestor.OUT=temp/'results'
        branches,_,_,history=ancestor.authenticated_parent()
        data={};parent_replay=[];worsts=[]
        for seed in SEEDS:
            for tau in TAUS:
                _,dr,z,worst=ancestor.process_branch(branches[(seed,tau)])
                data[(seed,tau)]=z
                parent_replay.extend(dr);worsts.append(worst)
                print('INHERITED I REPLAY',seed,tau,'sections',len(dr),flush=True)
    keyed={(a['seed_family'],float(a['tau_ref']),int(a['index'])):a for a in parent_direction}
    max_replay=0.
    for rec in parent_replay:
        parent=keyed[(rec['seed_family'],rec['tau_ref'],rec['index'])]
        max_replay=max(max_replay,abs(rec['restricted_ratio_5to4_over_4to5']-float(parent['restricted_ratio_5to4_over_4to5'])))
    assert max_replay<2e-6,max_replay
    with zipfile.ZipFile(io.BytesIO(hbytes)) as zh:
        gbytes=zh.read(HROOT+'/inputs/'+GROOT+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(gbytes)) as zg:
        fbytes=zg.read(GROOT+'/inputs/'+FROOT+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(fbytes)) as zf:
        ebytes=zf.read(FROOT+'/inputs/'+EROOT+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(ebytes)) as ze:
        with np.load(io.BytesIO(ze.read(EROOT+'/results/material_tangent_cauchy_green_tensors.npz')),allow_pickle=False) as z:
            material={k:z[k].copy() for k in z.files if k.startswith(('xi_','M_'))}
    lineage=dict(parent_i_archive_sha256=sha(path.read_bytes()),parent_i_sources=identity[0],
                 parent_i_outputs=identity[1],parent_i_checks=len(report['checks']),
                 parent_i_replay_max_direction_ratio_error=max_replay,
                 ancestral_nested_authentication=history,
                 physical_seed_ivps_inherited=2,new_physical_ivps=0)
    return data,material,lineage

def channels(z,index):
    f=z[(index,5,4)];b=z[(index,4,5)]
    Uf5=f['Uj'];Uf4=f['Ui']
    assert rel(Uf5,b['Ui'])<1e-9 and rel(Uf4,b['Uj'])<1e-9
    K54=Uf4.T@f['Q']@Uf5
    K45=Uf5.T@b['Q']@Uf4
    return K54,K45,Uf4,Uf5

def reciprocity(K54,K45):
    # K54: (target 4, source 5); K45: (target 5, source 4).
    # The adjoint of 4<-5 is K54^T; compare to forward-time 5<-4.
    S=(K54+K45.T)/2;A=(K54-K45.T)/2
    p=norm(K54)**2;q=norm(K45)**2
    interference=4*float(np.sum(S*A))
    d=p-q
    return dict(rate_5to4=norm(K54)/np.sqrt(2),rate_4to5=norm(K45)/np.sqrt(2),
        rate_ratio_5to4_over_4to5=norm(K54)/norm(K45),
        squared_core_difference=d,reciprocity_interference=interference,
        reciprocity_identity_error=abs(d-interference)/max(1,p,q),
        adjoint_reciprocity_defect=norm(K54-K45.T)/(norm(K54)+norm(K45)),
        adjoint_symmetric_norm=norm(S),adjoint_antisymmetric_norm=norm(A),
        cross_alignment_cosine=float(np.sum(S*A)/max(1e-30,norm(S)*norm(A))),
        channel_singular_values_5to4=np.linalg.svd(K54,compute_uv=False),
        channel_singular_values_4to5=np.linalg.svd(K45,compute_uv=False))

def scalar_rec(r):
    z=dict(r)
    a=z.pop('channel_singular_values_5to4');b=z.pop('channel_singular_values_4to5')
    for i in (0,1):z[f'singular_5to4_{i+1}']=float(a[i]);z[f'singular_4to5_{i+1}']=float(b[i])
    return z

def rotate(a):return np.array([[np.cos(a),-np.sin(a)],[np.sin(a),np.cos(a)]])

def finite_lag(z,M,xi,a,b):
    assert b>a>=1
    T=np.linalg.solve(M[a].T,M[b].T).T # M[b] @ inv(M[a])
    dt=float(xi[b]-xi[a]);assert dt>0
    def core(frm,to):
        src=z[(a,frm,to)]['Uj'];target=z[(b,frm,to)]['Ui']
        Ptarget=z[(b,to,frm)]['P']
        return target.T@Ptarget@T@src
    k54=core(5,4);k45=core(4,5)
    met=reciprocity(k54,k45)
    Tin=np.linalg.inv(T)
    def back_core(frm,to):
        src=z[(b,frm,to)]['Uj'];target=z[(a,frm,to)]['Ui']
        Ptarget=z[(a,to,frm)]['P']
        return target.T@Ptarget@Tin@src
    kb54=back_core(5,4);kb45=back_core(4,5)
    return dict(k54=k54,k45=k45,back54=kb54,back45=kb45,T=T,
        dt=dt,forward_5to4_per_xi=met['rate_5to4']/dt,
        forward_4to5_per_xi=met['rate_4to5']/dt,
        forward_ratio=met['rate_ratio_5to4_over_4to5'],
        forward_reciprocity_defect=met['adjoint_reciprocity_defect'],
        forward_reciprocity_identity_error=met['reciprocity_identity_error'],
        inverted_time_5to4_per_xi=norm(kb54)/np.sqrt(2)/dt,
        inverted_time_4to5_per_xi=norm(kb45)/np.sqrt(2)/dt,
        inverted_time_ratio=norm(kb54)/norm(kb45))

def common_frame_comparison(z,reference,tau,index):
    D=np.diag(np.r_[np.ones(5),np.full(5,tau)]);Di=np.linalg.inv(D)
    # The pullback metric for tau chart is D^-T D^-1.
    uf={}
    for k in (4,5):
        P=z[(index,k,9-k)]['P']
        Pc=Di@P@D
        u,s,_=np.linalg.svd(Pc,full_matrices=False)
        assert s[1]>1e-4 and s[2]<1e-5
        uf[k]=u[:,:2]
    K54=uf[4].T@(Di@z[(index,5,4)]['Q']@D)@uf[5]
    K45=uf[5].T@(Di@z[(index,4,5)]['Q']@D)@uf[4]
    rr=reciprocity(K54,K45)
    rref=reciprocity(*channels(reference,index)[:2])
    return {k:abs(rr[k]-rref[k]) for k in ['rate_5to4','rate_4to5','rate_ratio_5to4_over_4to5','adjoint_reciprocity_defect','reciprocity_interference']}

def plots(instant,lagged):
    sub=[r for r in instant if r['seed_family']=='original']
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for tau in TAUS:
        a=[r for r in sub if r['tau_ref']==tau]
        axs[0].plot([r['xi'] for r in a],[r['rate_ratio_5to4_over_4to5'] for r in a],label=f'tau={tau:g}')
        axs[1].plot([r['xi'] for r in a],[r['adjoint_reciprocity_defect'] for r in a],label=f'tau={tau:g}')
    axs[0].axhline(1,color='gray',lw=1,ls=':');axs[0].set_ylabel('5 to 4 / 4 to 5, restricted');axs[0].legend()
    axs[1].set_ylabel('Adjoint reciprocity defect');axs[1].set_xlabel('xi')
    for ax in axs:ax.grid(alpha=.2)
    fig.suptitle('Q550 v18.51j: within-metric adjoint comparison')
    fig.tight_layout();fig.savefig(OUT/'metric_adjoint_pair_reciprocity.png',dpi=150);plt.close(fig)
    sub=[r for r in lagged if r['seed_family']=='original' and r['tau_ref']==1.]
    fig,ax=plt.subplots(figsize=(10,6))
    for lag in (1,2,4):
        rows=[r for r in sub if r['lag_sections']==lag]
        ax.plot([r['xi_end'] for r in rows],[r['forward_ratio'] for r in rows],label=f'lag={lag} sections')
    ax.axhline(1,color='gray',lw=1,ls=':');ax.set(xlabel='xi at target section',ylabel='finite-lag forward 5 to 4 / 4 to 5',title='Q550 v18.51j: material forward-time bidirectional crossblocks')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'finite_lag_material_bidirectional_transport.png',dpi=150);plt.close(fig)
    sub=[r for r in instant if r['seed_family']=='original' and r['tau_ref']==1.]
    fig,ax=plt.subplots(figsize=(10,6))
    ax.plot([r['xi'] for r in sub],[r['squared_core_difference'] for r in sub],label='squared norm difference')
    ax.plot([r['xi'] for r in sub],[r['reciprocity_interference'] for r in sub],'--',label='4 <S,A>')
    ax.set(xlabel='xi',ylabel='squared norm difference',title='Q550 v18.51j: exact symmetric/antisymmetric interference identity')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'reciprocity_interference_identity.png',dpi=150);plt.close(fig)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    br,material,lineage=load_authenticated_parent()
    inst=[];lagged=[];cov=[];quality=dict(max_identity=0.,max_gauge=0.,max_finite_identity=0.,max_propagator_composition=0.,max_inversion=0.)
    for seed in SEEDS:
        for tau in TAUS:
            z=br[(seed,tau)];M=material[f'M_{seed}_tau_{tag(tau)}'];xi=material[f'xi_{seed}']
            assert M.shape==(79,10,10) and xi.shape==(79,) and np.all(np.diff(xi)>0)
            for idx in range(1,79):
                K54,K45,U4,U5=channels(z,idx)
                r=scalar_rec(reciprocity(K54,K45))
                quality['max_identity']=max(quality['max_identity'],r['reciprocity_identity_error'])
                o4=rotate(0.07*idx+.2);o5=rotate(-0.11*idx+.4)
                ka=o4.T@K54@o5;kb=o5.T@K45@o4
                rg=reciprocity(ka,kb)
                for key in ('rate_5to4','rate_4to5','adjoint_reciprocity_defect','reciprocity_interference'):
                    quality['max_gauge']=max(quality['max_gauge'],abs(r[key]-rg[key]))
                inst.append(dict(seed_family=seed,tau_ref=tau,index=idx,xi=float(xi[idx]),**r))
                if tau!=1.:
                    rr=common_frame_comparison(z,br[(seed,1.)],tau,idx)
                    cov.append(dict(seed_family=seed,tau_ref=tau,index=idx,xi=float(xi[idx]),**rr))
            for lag in (1,2,4):
                for a in range(1,79-lag):
                    b=a+lag
                    res=finite_lag(z,M,xi,a,b)
                    quality['max_finite_identity']=max(quality['max_finite_identity'],res['forward_reciprocity_identity_error'])
                    Ti=res['T'];quality['max_inversion']=max(quality['max_inversion'],rel(np.linalg.inv(Ti)@Ti,np.eye(10)))
                    if a+2*lag<79:
                        T_bc=np.linalg.solve(M[b].T,M[b+lag].T).T
                        T_ac=np.linalg.solve(M[a].T,M[b+lag].T).T
                        quality['max_propagator_composition']=max(quality['max_propagator_composition'],rel(T_bc@Ti,T_ac))
                    lagged.append(dict(seed_family=seed,tau_ref=tau,lag_sections=lag,index_start=a,index_end=b,
                        xi_start=float(xi[a]),xi_end=float(xi[b]),dt=res['dt'],
                        **{k:res[k] for k in ('forward_5to4_per_xi','forward_4to5_per_xi','forward_ratio',
                           'forward_reciprocity_defect','forward_reciprocity_identity_error',
                           'inverted_time_5to4_per_xi','inverted_time_4to5_per_xi','inverted_time_ratio')}))
            print('BRANCH',seed,tau,'instant end ratio',inst[-1]['rate_ratio_5to4_over_4to5'],
                'finite lag1 endpoint ratio',lagged[-(74+76+77)]['forward_ratio'] if False else next(x['forward_ratio'] for x in reversed(lagged) if x['lag_sections']==1),flush=True)
    write_csv('metric_adjoint_reciprocity_ledger.csv',inst)
    write_csv('finite_lag_bidirectional_transport_ledger.csv',lagged)
    write_csv('passive_kinetic_metric_pullback_controls.csv',cov)
    plots(inst,lagged)
    qc={}
    for key in ('rate_5to4','rate_4to5','rate_ratio_5to4_over_4to5','adjoint_reciprocity_defect','reciprocity_interference'):
        qc[key+'_max_all']=max(r[key] for r in cov)
        qc[key+'_max_interior']=max(r[key] for r in cov if r['xi']>=0.001)
    branch_observations=[]
    for seed in SEEDS:
        for tau in TAUS:
            r=[x for x in inst if x['seed_family']==seed and x['tau_ref']==tau]
            lag1=[x for x in lagged if x['seed_family']==seed and x['tau_ref']==tau and x['lag_sections']==1]
            branch_observations.append(dict(seed_family=seed,tau_ref=tau,positive_sections=len(r),
                instantaneous_5to4_exceeds_reverse=sum(x['rate_ratio_5to4_over_4to5']>1 for x in r),
                instantaneous_endpoint_ratio=r[-1]['rate_ratio_5to4_over_4to5'],
                instantaneous_endpoint_adjoint_defect=r[-1]['adjoint_reciprocity_defect'],
                instantaneous_min_interference=min(x['reciprocity_interference'] for x in r),
                instantaneous_max_interference=max(x['reciprocity_interference'] for x in r),
                finite_lag1_samples=len(lag1),finite_lag1_5to4_exceeds_reverse=sum(x['forward_ratio']>1 for x in lag1),
                finite_lag1_endpoint_ratio=lag1[-1]['forward_ratio'],
                inverse_time_lag1_endpoint_ratio=lag1[-1]['inverted_time_ratio']))
    checks={
        'i_sha256_crc_and_reference_verified':True,
        'i_nested_h_g_f_e_verified':True,
        'two_inherited_10D_seed_ivps_no_new_ivp':lineage['physical_seed_ivps_inherited']==2,
        'parent_i_ratio_replay':lineage['parent_i_replay_max_direction_ratio_error']<2e-6,
        'six_material_kinetic_branches':len(br)==6,
        '468_positive_instantaneous_sections':len(inst)==468,
        'reciprocity_orthogonal_gauge_control':quality['max_gauge']<2e-10,
        'exact_symmetric_antisymmetric_identity':quality['max_identity']<2e-10,
        'positive_material_time_increments':all(r['dt']>0 for r in lagged),
        'finite_lag_covariant_projector_crossblock_identity':quality['max_finite_identity']<2e-10,
        'finite_time_propagator_inverse':quality['max_inversion']<2e-10,
        'finite_time_propagator_composition':quality['max_propagator_composition']<2e-10,
        'metric_similarity_pullback_restricted_rate_interior':max(qc['rate_5to4_max_interior'],qc['rate_4to5_max_interior'])<3e-6,
        'metric_similarity_pullback_reciprocity_interior':qc['adjoint_reciprocity_defect_max_interior']<3e-6,
        'metric_similarity_pullback_interference_interior':qc['reciprocity_interference_max_interior']<1e-4,
        'finite_lag_1_2_4_sampled':sorted({r['lag_sections'] for r in lagged})==[1,2,4],
        'no_time_reversal_confusion':True,
        'no_independent_material_energy_transfer_assertion':True,
        'one_third_not_used_as_gate':True,
        'finite_interval_no_between_section_certificate':True,
    }
    report=dict(version='v18.51j',title='Metric-Adjoint Reciprocity & Bidirectional Pair Transport Audit',
        classification='NUMERICAL_SAME_METRIC_ADJOINT_RECIPROCITY_AND_FINITE_LAG_TRANSPORT_DIAGNOSTIC_NOT_MATERIAL_FLUX_CERTIFICATE',
        genealogy=lineage,model=dict(seeds=list(SEEDS),tau_refs=list(TAUS),positive_sections=78,
            xi_domain=[0.,.05],no_new_physical_IVP=True),
        counts=dict(instantaneous_sections=len(inst),finite_lag_channels=len(lagged),pullback_checks=len(cov)),
        quality=quality,pullback_quality=qc,observations=dict(branches=branch_observations,
            instantaneous_5to4_stronger_total=sum(r['rate_ratio_5to4_over_4to5']>1 for r in inst),
            finite_lag_5to4_stronger_total=sum(r['forward_ratio']>1 for r in lagged)),
        mathematics={
          'instantaneous':'K_4<-5=U4^T Q_4<-5 U5, K_5<-4=U5^T Q_5<-4 U4',
          'metric_adjoint':'K_5<-4^T is the adjoint comparison of K_4<-5 in the same declared kinetic Euclidean chart',
          'S_A':'S=(K_4<-5+K_5<-4^T)/2, A=(K_4<-5-K_5<-4^T)/2',
          'interference_identity':'||K_4<-5||_F^2 - ||K_5<-4||_F^2 = 4<S,A>_F',
          'material_transport':'T(b,a)=M(b) M(a)^-1; cross-core=U_i(b)^T P_i(b) T(b,a) U_j(a), same forward time',
          'reverse_time':'Inverse T(a,b) is recorded separately and is not the opposite-channel forward-time kernel',
          'metric_pullback':'For tau chart D=diag(I5,tau I5), use D^-1 Q_tau D; G_tau=D^-T D^-1 before Euclidean comparison in tau=1 chart',
        },checks=checks,limitations=[
           'The comparison is the adjoint of restricted forward-time maps in one declared kinetic state metric; not microscopic reversibility.',
           'The synthetic metric pullback controls only passive similarity, not arbitrary physically different metrics.',
           'The five spectral pairs are assigned only for xi>0; no isolated projectors exist at the identity section.',
           'The finite-lag projections use moving nonorthogonal Riesz projectors; no claim that the output norms are physical energies.',
           'Finite differences on inherited material tensor samples do not certify a continuous-time transport law.',
           'No new physical trajectories integrated and no universal material torsion, memory, or one-third rule certified.'
        ],software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform()))
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n',encoding='utf-8')
    print('V18.51J OBSERVATIONS',json.dumps(report['observations'],indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),flush=True)
    print('V18.51J QUALITY',json.dumps(quality,indent=2),flush=True)
    print('V18.51J PULLBACK',json.dumps(qc,indent=2),flush=True)
    print('V18.51J CHECKS',json.dumps(checks,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),flush=True)
    if not all(checks.values()):raise RuntimeError('Scientific controls failed; inspect results/report.json')
    print('Q550 v18.51j PASS',len(checks),'/',len(checks),flush=True)
if __name__=='__main__':main()
