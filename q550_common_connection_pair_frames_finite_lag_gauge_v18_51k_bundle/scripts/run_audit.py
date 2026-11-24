#!/usr/bin/env python3
"""Q550 v18.51k: common-connection pair frames and finite-lag gauge audit.

Scientific scope:
  * Reconstruct authentic j inherited i/h/g/f/e Q550 tensors, without new IVPs.
  * Use the SAME flat kinetic Cartesian ambient connection for both evolving
    spectral right planes, and their induced (Grassmann) discrete orthogonal
    polar/Procrustes lifts separately on E4 and E5.
  * Compare finite-lag crossblocks only after transporting their target/source
    frames to a common start-section frame.
  * Audit independent, section-dependent O(2) basis-gauge and nonorthogonal
    moving ambient chart covariance with its pulled-back metric and connection.

No result is presented as energy flow, intrinsic material torsion, time-reversal
symmetry, or global continuous-time certification. Only sampled xi>0 sections.
"""
from __future__ import annotations
import csv, hashlib, importlib.util, io, json, platform, sys, tempfile, zipfile
from pathlib import Path
import numpy as np
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
JROOT='q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle'
JZIP=JROOT+'_server_sendback.zip'
IROOT='q550_projector_conditioning_separation_covariant_directionality_v18_51i_bundle'
IZIP=IROOT+'_server_sendback.zip'
SEEDS=('original','autonomous'); TAUS=(0.5,1.,2.)
EYE=np.eye(10)

def sha(v):return hashlib.sha256(v).hexdigest()
def fro(v):return float(np.linalg.norm(v,'fro'))
def relative(a,b):return fro(a-b)/max(1.,fro(a),fro(b))
def tag(v):return f'{v:.1f}'.replace('.','p')
def save_csv(name,rows):
    assert rows
    with (OUT/name).open('w',encoding='utf-8',newline='') as fp:
        w=csv.DictWriter(fp,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def manifest_zip(z,base,version):
    assert z.testzip() is None, 'CRC failure: '+version
    sm=json.loads(z.read(base+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(base+'/SHA256SUMS_OUTPUT.json'))
    assert sm['root']==om['root']==base and sm['version']==om['version']==version
    for name,h in sm['files'].items():assert sha(z.read(base+'/'+name))==h,('source',name)
    for name,h in om['file_sha256'].items():assert sha(z.read(base+'/'+name))==h,('result',name)
    return len(sm['files']),len(om['file_sha256'])

def parent_replay():
    p=ROOT/'inputs'/JZIP
    with zipfile.ZipFile(p) as z:
        auth=manifest_zip(z,JROOT,'v18.51j')
        rep=json.loads(z.read(JROOT+'/results/report.json'))
        assert all(rep['checks'].values()) and rep['version']=='v18.51j'
        expected=['reference/g_projector_replay_v18_51g.py',
                  'reference/h_pairwise_replay_v18_51h.py',
                  'reference/i_projector_replay_v18_51i.py']
        for name in expected:
            assert z.read(JROOT+'/'+name)==(ROOT/name).read_bytes(), name
        assert z.read(JROOT+'/scripts/run_audit.py')==(ROOT/'reference/j_adjoint_replay_v18_51j.py').read_bytes()
        ipayload=z.read(JROOT+'/inputs/'+IZIP)
        old_inst=list(csv.DictReader(io.StringIO(z.read(JROOT+'/results/metric_adjoint_reciprocity_ledger.csv').decode())))
        old_finite=list(csv.DictReader(io.StringIO(z.read(JROOT+'/results/finite_lag_bidirectional_transport_ledger.csv').decode())))
    # Recreate an exact *functional* inherited j replay context, not edited j
    # source files. The nested i source is copied unchanged from the j sendback.
    with tempfile.TemporaryDirectory(prefix='q550_v18_51k_genealogy_') as tmp:
        t=Path(tmp);(t/'inputs').mkdir();(t/'reference').mkdir()
        (t/'inputs'/IZIP).write_bytes(ipayload)
        for name in expected:(t/'reference'/Path(name).name).write_bytes((ROOT/name).read_bytes())
        spec=importlib.util.spec_from_file_location('q550_j_inherited',ROOT/'reference/j_adjoint_replay_v18_51j.py')
        j=importlib.util.module_from_spec(spec);spec.loader.exec_module(j)
        j.ROOT=t;j.OUT=t/'results'
        branches,material,genealogy=j.load_authenticated_parent()
    assert len(old_inst)==468 and len(old_finite)==1362
    keyed={(x['seed_family'],float(x['tau_ref']),int(x['index'])):x for x in old_inst}
    max_replay=0.
    for seed in SEEDS:
        for tau in TAUS:
            z=branches[(seed,tau)]
            for i in range(1,79):
                k54,k45,*_=j.channels(z,i)
                calc=fro(k54)/fro(k45)
                max_replay=max(max_replay,abs(calc-float(keyed[seed,tau,i]['rate_ratio_5to4_over_4to5'])))
    assert max_replay<2e-6, max_replay
    return j,branches,material,old_finite,dict(parent_j_archive_sha256=sha(p.read_bytes()),
        parent_j_manifest_sources=auth[0],parent_j_manifest_outputs=auth[1],
        parent_j_checks=len(rep['checks']),parent_j_inherited_genealogy=genealogy,
        max_parent_instantaneous_replay_ratio_error=max_replay,
        physical_seed_ivps_inherited=2,new_physical_ivps=0)

def orthogonal_polar(overlap):
    U,s,Vt=np.linalg.svd(overlap)
    assert s[-1]>1e-8, 'Adjacent plane overlap rank loss; connection cannot be continued'
    return U@Vt, float(s[-1])

def rot(t):return np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])

def gauge(k,index,tau=1.,seed='original'):
    t=(.29 if k==4 else -.41)*index+(.17 if seed=='original' else -.23)+tau*.113
    o=rot(t)
    if index%(7 if k==4 else 11)==0:o=o@np.diag([-1.,1.])
    return o

def build_frames(z,gauged=False,tau=1.,seed='original'):
    frames={k:{} for k in (4,5)}
    for x in range(1,79):
        for k in (4,5):
            # j's channel objects provide an orthonormal right-plane basis.
            U=z[(x,5,4)]['Ui'] if k==4 else z[(x,5,4)]['Uj']
            if gauged:U=U@gauge(k,x,tau,seed)
            assert fro(U.T@U-np.eye(2))<1e-8
            frames[k][x]=U
    steps={k:{} for k in (4,5)}; overlaps=[]
    for k in (4,5):
        for a in range(1,78):
            W,sv=orthogonal_polar(frames[k][a+1].T@frames[k][a])
            steps[k][a]=W
            overlaps.append(dict(pair=k,index_start=a,index_end=a+1,min_overlap_singular=sv))
    return frames,steps,overlaps

def chain_connection(steps,k,a,b):
    R=np.eye(2)
    for t in range(a,b):R=steps[k][t]@R
    return R

def instantaneous_restrictions(j,z,a,b,M):
    T=np.linalg.solve(M[a].T,M[b].T).T
    def ch(src,target):
        U_src=z[(a,src,target)]['Uj'];U_tgt=z[(b,src,target)]['Ui']
        P=z[(b,target,src)]['P']
        return U_tgt.T@P@T@U_src
    return ch(5,4),ch(4,5),T

def aligned_measure(K54,K45,R4,R5):
    # Crossblocks expressed in the two *start-section* frames.  Each channel
    # is in forward xi; no reversal of physical time is used here.
    X=R4.T@K54
    Y=K45.T@R5
    S=(X+Y)/2
    A=(X-Y)/2
    eq=fro(X)**2-fro(Y)**2
    interference=4*float(np.sum(S*A))
    denom=fro(K54)+fro(K45)
    assert denom>1e-14
    return dict(gauge_aligned_adjoint_defect=fro(X-Y)/denom,
        naive_endpoint_adjoint_defect=fro(K54-K45.T)/denom,
        ratio_5to4_over_4to5=fro(K54)/fro(K45),
        paired_symmetric_norm=fro(S),paired_antisymmetric_norm=fro(A),
        signed_interference=interference, squared_rate_difference=eq,
        interference_residual=abs(eq-interference)/max(1.,fro(X)**2,fro(Y)**2),
        aligned_cross_cosine=float(np.sum(X*Y)/max(1e-30,fro(X)*fro(Y))),
        connection_pair4_det=float(np.linalg.det(R4)),
        connection_pair5_det=float(np.linalg.det(R5)))

def passive_chart(x):
    # A genuinely moving, nonorthogonal *passive* ambient chart; it MUST carry
    # both its material metric and connection C(b,a)=A(b) A(a)^-1.
    alpha=.12+6.3*x
    mat=np.eye(10)
    mat[np.ix_([0,5],[0,5])]=rot(alpha)
    mat[np.ix_([1,7],[1,7])]=rot(-.35*alpha)
    dia=np.exp(.17*np.sin(np.arange(10)*.7+8*x)+.06*np.arange(10)/10)
    return mat@np.diag(dia)

def chart_control(z,M,xi,frames,a,b,baseline):
    Aa=passive_chart(xi[a]);Ab=passive_chart(xi[b]);Aai=np.linalg.inv(Aa);Abi=np.linalg.inv(Ab)
    Ga=Aai.T@Aai;Gb=Abi.T@Abi
    flat=Ab@Aai
    k54,k45,T=instantaneous_restrictions(None,z,a,b,M)
    def transformed(src,tgt):
        Us=frames[src][a];Ut=frames[tgt][b];P=z[(b,tgt,src)]['P']
        Usx=Aa@Us;Utx=Ab@Ut
        Px=Ab@P@Abi;Tx=Ab@T@Aai
        return Utx.T@Gb@Px@Tx@Usx
    ck54=transformed(5,4);ck45=transformed(4,5)
    O4=frames[4][b].T@frames[4][a];O5=frames[5][b].T@frames[5][a]
    O4x=(Ab@frames[4][b]).T@Gb@flat@(Aa@frames[4][a]);
    O5x=(Ab@frames[5][b]).T@Gb@flat@(Aa@frames[5][a]);
    return dict(metric_connection=relative(flat.T@Gb@flat,Ga),
       crossblock=max(relative(ck54,k54),relative(ck45,k45)),
       overlap=max(relative(O4,O4x),relative(O5,O5x)),
       parent_ratio_error=abs(fro(k54)/fro(k45)-baseline),
       moving_chart_is_nonorthogonal=fro(Aa.T@Aa-EYE)>1e-3)

def plot_results(rows):
    sub=[r for r in rows if r['seed_family']=='original' and r['tau_ref']==1.]
    fig,axs=plt.subplots(2,1,figsize=(9,8),sharex=True)
    for lag in (1,2,4):
        x=[r for r in sub if r['lag_sections']==lag]
        axs[0].plot([r['xi_end'] for r in x],[r['gauge_aligned_adjoint_defect'] for r in x],label=f'lag={lag}')
        axs[1].plot([r['xi_end'] for r in x],[r['ratio_5to4_over_4to5'] for r in x],label=f'lag={lag}')
    axs[0].set_ylabel('Connection-aligned adjoint defect')
    axs[1].set_ylabel('Forward 5→4 / 4→5 strength')
    axs[1].set_xlabel('Target xi')
    axs[1].axhline(1,linestyle=':',color='gray')
    for ax in axs:ax.legend();ax.grid(alpha=.2)
    fig.suptitle('Q550 v18.51k: common-connection pair-frame transport')
    fig.tight_layout();fig.savefig(OUT/'common_connection_pair_frame_transport.png',dpi=150);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    for tau in TAUS:
        x=[r for r in rows if r['seed_family']=='original' and r['tau_ref']==tau and r['lag_sections']==1]
        ax.plot([r['xi_end'] for r in x],[r['gauge_aligned_adjoint_defect'] for r in x],label=f'tau={tau:g}')
    ax.set(xlabel='Target xi',ylabel='Connection-aligned defect',title='Same-metric finite-lag reciprocity under three kinetic weights')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'connection_adjoint_metric_sensitivity.png',dpi=150);plt.close(fig)

def main():
    OUT.mkdir(exist_ok=True,parents=True)
    j,branches,material,old_finite,lineage=parent_replay()
    original={(r['seed_family'],float(r['tau_ref']),int(r['lag_sections']),int(r['index_start']),int(r['index_end'])):r for r in old_finite}
    rows=[];charts=[];steplog=[];quality=dict(max_gauge_rate_error=0.,max_aligned_defect_gauge_error=0.,
        max_naive_defect_gauge_change=0.,max_interference_error=0.,max_parent_forward_ratio_difference=0.,
        max_chart_metric_residual=0.,max_chart_crossblock_residual=0.,max_chart_overlap_residual=0.,
        max_direct_vs_chained_connection_difference=0.,min_adjacent_overlap_singular=1.,
        max_connection_composition=0.)
    for seed in SEEDS:
        for tau in TAUS:
            z=branches[seed,tau];xi=material[f'xi_{seed}'];M=material[f'M_{seed}_tau_{tag(tau)}']
            F,conn,overlaps=build_frames(z,tau=tau,seed=seed)
            FG,conng,_=build_frames(z,gauged=True,tau=tau,seed=seed)
            quality['min_adjacent_overlap_singular']=min(quality['min_adjacent_overlap_singular'],*(v['min_overlap_singular'] for v in overlaps))
            for v in overlaps:steplog.append(dict(seed_family=seed,tau_ref=tau,xi_start=float(xi[v['index_start']]),**v))
            for lag in (1,2,4):
                for a in range(1,79-lag):
                    b=a+lag
                    K54,K45,T=instantaneous_restrictions(j,z,a,b,M)
                    R4=chain_connection(conn,4,a,b);R5=chain_connection(conn,5,a,b)
                    met=aligned_measure(K54,K45,R4,R5)
                    K54g=gauge(4,b,tau,seed).T@K54@gauge(5,a,tau,seed)
                    K45g=gauge(5,b,tau,seed).T@K45@gauge(4,a,tau,seed)
                    R4g=chain_connection(conng,4,a,b);R5g=chain_connection(conng,5,a,b)
                    mg=aligned_measure(K54g,K45g,R4g,R5g)
                    quality['max_aligned_defect_gauge_error']=max(quality['max_aligned_defect_gauge_error'],abs(met['gauge_aligned_adjoint_defect']-mg['gauge_aligned_adjoint_defect']))
                    quality['max_gauge_rate_error']=max(quality['max_gauge_rate_error'],abs(met['ratio_5to4_over_4to5']-mg['ratio_5to4_over_4to5']))
                    quality['max_naive_defect_gauge_change']=max(quality['max_naive_defect_gauge_change'],abs(met['naive_endpoint_adjoint_defect']-mg['naive_endpoint_adjoint_defect']))
                    quality['max_interference_error']=max(quality['max_interference_error'],met['interference_residual'])
                    w4,_=orthogonal_polar(F[4][b].T@F[4][a]);w5,_=orthogonal_polar(F[5][b].T@F[5][a]);
                    direct_chain=max(fro(w4-R4),fro(w5-R5))
                    quality['max_direct_vs_chained_connection_difference']=max(quality['max_direct_vs_chained_connection_difference'],direct_chain)
                    if b+1<=78:
                        for k,R in ((4,R4),(5,R5)):
                            rp=chain_connection(conn,k,b,b+1)@R
                            q=chain_connection(conn,k,a,b+1)
                            quality['max_connection_composition']=max(quality['max_connection_composition'],fro(rp-q))
                    key=(seed,tau,lag,a,b)
                    old=original[key];dr=abs(met['ratio_5to4_over_4to5']-float(old['forward_ratio']))
                    quality['max_parent_forward_ratio_difference']=max(quality['max_parent_forward_ratio_difference'],dr)
                    if a in (1,18,38,58,74) and b<=78:
                        qc=chart_control(z,M,xi,F,a,b,float(old['forward_ratio']))
                        quality['max_chart_metric_residual']=max(quality['max_chart_metric_residual'],qc['metric_connection'])
                        quality['max_chart_crossblock_residual']=max(quality['max_chart_crossblock_residual'],qc['crossblock'])
                        quality['max_chart_overlap_residual']=max(quality['max_chart_overlap_residual'],qc['overlap'])
                        charts.append(dict(seed_family=seed,tau_ref=tau,lag_sections=lag,index_start=a,index_end=b,
                            xi_start=float(xi[a]),xi_end=float(xi[b]),**qc))
                    rows.append(dict(seed_family=seed,tau_ref=tau,lag_sections=lag,index_start=a,index_end=b,
                         xi_start=float(xi[a]),xi_end=float(xi[b]),dt=float(xi[b]-xi[a]),
                         direct_vs_chain_overlap=direct_chain, aligned_gauge_control_error=abs(met['gauge_aligned_adjoint_defect']-mg['gauge_aligned_adjoint_defect']),
                         naive_gauge_shift=abs(met['naive_endpoint_adjoint_defect']-mg['naive_endpoint_adjoint_defect']),**met))
            b79=[r for r in rows if r['seed_family']==seed and r['tau_ref']==tau and r['lag_sections']==1]
            print('BRANCH',seed,tau,'lag1 count',len(b79),'endpoint ratio',b79[-1]['ratio_5to4_over_4to5'],
                  'endpoint aligned defect',b79[-1]['gauge_aligned_adjoint_defect'],flush=True)
    save_csv('connection_aligned_finite_lag_ledger.csv',rows)
    save_csv('pair_frame_overlap_conditioning.csv',steplog)
    save_csv('moving_chart_connection_covariance.csv',charts)
    plot_results(rows)
    obs=[]
    for seed in SEEDS:
        for tau in TAUS:
            sub=[r for r in rows if r['seed_family']==seed and r['tau_ref']==tau]
            l1=[r for r in sub if r['lag_sections']==1]
            obs.append(dict(seed_family=seed,tau_ref=tau,finite_intervals=len(sub),lag1_intervals=len(l1),
                forward_5to4_stronger=sum(r['ratio_5to4_over_4to5']>1 for r in sub),
                first_lag1_ratio=l1[0]['ratio_5to4_over_4to5'],
                final_lag1_ratio=l1[-1]['ratio_5to4_over_4to5'],
                final_lag1_connection_aligned_defect=l1[-1]['gauge_aligned_adjoint_defect'],
                final_lag1_naive_defect=l1[-1]['naive_endpoint_adjoint_defect'],
                max_naive_gauge_shift=max(r['naive_gauge_shift'] for r in sub)))
    checks=dict(authenticated_j_parent_source_crc_sha=True,
        authenticated_nested_i_h_g_f_e=True,
        two_inherited_physical_seed_ivps_no_new=lineage['physical_seed_ivps_inherited']==2 and lineage['new_physical_ivps']==0,
        j_instantaneous_parent_replay=lineage['max_parent_instantaneous_replay_ratio_error']<2e-6,
        six_kinetic_branches=len(obs)==6,
        finite_lag_1362_sections=len(rows)==1362,
        finite_lag_parent_tolerance_replay=quality['max_parent_forward_ratio_difference']<2e-6,
        positive_time_intervals=all(r['dt']>0 for r in rows),
        adjacent_plane_overlap_nondegenerate=quality['min_adjacent_overlap_singular']>1e-4,
        procrustes_connection_orthogonal=all(abs(abs(r['connection_pair4_det'])-1)<1e-9 and abs(abs(r['connection_pair5_det'])-1)<1e-9 for r in rows),
        connection_transport_composition=quality['max_connection_composition']<1e-11,
        aligned_interference_exact_identity=quality['max_interference_error']<1e-10,
        gauge_aligned_defect_invariant=quality['max_aligned_defect_gauge_error']<1e-10,
        directional_norm_ratio_gauge_invariant=quality['max_gauge_rate_error']<1e-10,
        unaligned_endpoint_defect_is_gauge_sensitive=quality['max_naive_defect_gauge_change']>1e-3,
        passive_moving_chart_metric_compatible=quality['max_chart_metric_residual']<1e-10,
        passive_moving_chart_crossblock_covariant=quality['max_chart_crossblock_residual']<1e-10,
        passive_moving_chart_connection_overlap_covariant=quality['max_chart_overlap_residual']<1e-10,
        all_parent_finite_pair_ratios_exceed_one=sum(r['ratio_5to4_over_4to5']>1 for r in rows)==1362,
        sample_only_no_continuous_certification=True,
        no_energy_or_memory_or_torsion_certified=True,
        one_third_not_used_as_gate=True)
    report=dict(version='v18.51k',title='Common-Connection Pair Frames & Finite-Lag Gauge Audit',
        classification='NUMERICAL_COMMON_AMBIENT_CONNECTION_PAIR_FRAME_GAUGE_DIAGNOSTIC_NOT_MATERIAL_TORSION_CERTIFICATE',
        genealogy=lineage,counts=dict(finite_intervals=len(rows),frame_overlap_sections=len(steplog),moving_chart_controls=len(charts)),
        observations=dict(branches=obs,overall_forward_5to4_stronger=sum(r['ratio_5to4_over_4to5']>1 for r in rows)),
        quality=quality,checks=checks,
        mathematics=dict(ambient_connection='Common flat kinetic Cartesian Levi-Civita connection; identity parallel map in the declared kinetic Cartesian chart.',
          induced_plane_connection='R_i(k+1,k)=polar(U_i(k+1)^T U_i(k)); R_i(b,a)=product of consecutive R_i.',
          connection_aligned_blocks='X=R_4(b,a)^T K_(4<-5)(b,a); Y=K_(5<-4)(b,a)^T R_5(b,a)',
          gauge_transformation='U_i(k) -> U_i(k) O_i(k), O_i(k) in O(2). X,Y transform by the same O4(a)^T left and O5(a) right factors.',
          finite_material_transport='T(b,a)=M(b) M(a)^-1, with inherited spectral Riesz projections at b.',
          metric_chart='Moving passive nonorthogonal A(xi), G=A^-T A^-1, ambient connection transport C(b,a)=A(b) A(a)^-1.'),
        limitations=[
          'The common ambient connection is flat in Cartesian kinetic-state coordinates and is not the dynamical tangent generator.',
          'The per-plane Procrustes lift is a discrete metric-induced Grassmann connection; direct endpoint polar maps need not coincide with stepwise products.',
          'Aligned reciprocity is an adjoint comparison of forward-time crossblocks, not microscopic time reversal.',
          'Different tau_ref choices imply different declared Euclidean state metrics, not necessarily identical restricted strengths.',
          'The inherited near-degenerate eigenprojectors can shift under independent numerical replays: parent finite-ratio agreement is required within 2e-6, not byte-exact.',
          'Projector subspaces are not orthogonal and only exist as isolated pairs at xi>0; spectral gaps are not interval certified.',
          'Results are restricted to sampled xi<=0.05 and lags 1,2,4; no global material memory, energy transfer, or intrinsic torsion is established.'
        ],software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform()))
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('Q550 v18.51k quality',json.dumps(quality,indent=2),flush=True)
    print('Q550 v18.51k checks',json.dumps(checks,indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('Q550 v18.51k scientific checks failed')
    print('Q550 v18.51k PASS',len(checks),'/',len(checks),flush=True)

if __name__=='__main__':main()
