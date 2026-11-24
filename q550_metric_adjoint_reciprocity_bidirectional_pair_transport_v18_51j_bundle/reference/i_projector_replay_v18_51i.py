#!/usr/bin/env python3
"""Q550 v18.51i: projector conditioning separation and covariant directionality.

Replays authenticated v18.51h and its historical g/f/e ancestry. No physical IVP.
All comments, reports, inputs, outputs, and scientific claims are in English.

For a channel from j to i, Q_ij = P_i (P'_j - [B,P_j]) P_j.
Let U_j,U_i be orthonormal bases for the right eigenspace ranges of
P_j,P_i in a *declared* state metric. Define
    K_ij = U_i^T Q_ij U_j, R_ij = ||K_ij||_F / sqrt(2).
R is a restricted right-subspace coupling, not energy transfer or intrinsic
metric-independent directional flux. The identity
    ||Q_ij||_F / ||P_j||_F = R_ij * (||Q_ij||_F / ||K_ij||_F)
                                              / (||P_j||_F / sqrt(2))
is an exact orthonormal-frame/ambient-extension/source-conditioning split.
Its ratio between opposite 4/5 channels can be assessed without assuming it
survives. Metric similarity is checked only after pullback to tau=1.
"""
from __future__ import annotations
import csv,hashlib,importlib.util,io,json,platform,sys,tempfile,zipfile
from pathlib import Path
import numpy as np
import scipy,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
HROOT='q550_pairwise_numerator_gap_competition_covariant_directionality_v18_51h_bundle'
HNAME=HROOT+'_server_sendback.zip'
SEEDS=('original','autonomous')
TAUS=(0.5,1.,2.)

def sha(x): return hashlib.sha256(x).hexdigest()
def fnorm(a): return float(np.linalg.norm(a,'fro'))
def rel(a,b): return fnorm(a-b)/max(1.,fnorm(a),fnorm(b))
def csvwrite(file,rows):
    assert rows
    with (OUT/file).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def read_csv_blob(x):return list(csv.DictReader(io.StringIO(x.decode('utf-8'))))

def authenticated_parent():
    archive=ROOT/'inputs'/HNAME
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None,'h archive CRC verification failed'
        sm=json.loads(z.read(HROOT+'/SOURCE_MANIFEST.json'))
        om=json.loads(z.read(HROOT+'/SHA256SUMS_OUTPUT.json'))
        assert sm['root']==om['root']==HROOT and sm['version']==om['version']=='v18.51h'
        for name,digest in sm['files'].items():
            assert sha(z.read(HROOT+'/'+name))==digest,('h source',name)
        for name,digest in om['file_sha256'].items():
            assert sha(z.read(HROOT+'/'+name))==digest,('h result',name)
        report=json.loads(z.read(HROOT+'/results/report.json'))
        assert report['version']=='v18.51h' and all(report['checks'].values())
        source=z.read(HROOT+'/scripts/run_audit.py')
        gsource=z.read(HROOT+'/reference/g_projector_replay_v18_51g.py')
        assert source==(ROOT/'reference/h_pairwise_replay_v18_51h.py').read_bytes()
        assert gsource==(ROOT/'reference/g_projector_replay_v18_51g.py').read_bytes()
        garchive=z.read(HROOT+'/inputs/q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle_server_sendback.zip')
        hdir=read_csv_blob(z.read(HROOT+'/results/pairwise_directionality_decomposition.csv'))
        hledger=read_csv_blob(z.read(HROOT+'/results/pairwise_numerator_gap_ledger.csv'))
    assert len(hdir)==468 and len(hledger)==9360
    # Read the exact historical code in the authenticated input, not a re-implementation.
    with tempfile.TemporaryDirectory(prefix='q550_51i_ancestry_') as tmp:
        base=Path(tmp);(base/'inputs').mkdir();(base/'reference').mkdir()
        (base/'inputs'/('q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle_server_sendback.zip')).write_bytes(garchive)
        (base/'reference/g_projector_replay_v18_51g.py').write_bytes(gsource)
        (base/'historical_h.py').write_bytes(source)
        spec=importlib.util.spec_from_file_location('q550_51h_historical_replay',base/'historical_h.py')
        h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
        h.ROOT=base;h.IN=base/'inputs'
        vals,grates,anc=h.authenticated_inputs()
        branches={}
        for seed in SEEDS:
            for tau in TAUS:
                branches[(seed,tau)]=h.analyze_branch(seed,tau,vals,grates)
                print('AUTHENTICATED H REPLAY',seed,tau,flush=True)
    assert anc['physical_seed_ivps']==2 and anc['no_new_physical_ivp']
    return branches,hdir,hledger,{'h_archive_sha256':sha(archive.read_bytes()),
                                'h_source_files':len(sm['files']),
                                'h_output_files':len(om['file_sha256']),
                                'parent_h_checks':len(report['checks']),
                                'nested_g_f_e_verified':anc,
                                'original_ten_dimensional_ivps_inherited':2}

def orthonormal_right_range(P):
    u,s,_=np.linalg.svd(P,full_matrices=False)
    assert s[1]>1e-4 and s[2]<1e-6,('Numerical projector rank',s)
    U=u[:,:2]
    assert fnorm(U.T@U-np.eye(2))<1e-10
    assert fnorm(P@U-U)<3e-7
    return U,s

def channel_metrics(Q,Psrc,Usrc,Utarget):
    K=Utarget.T@Q@Usrc
    qn=fnorm(Q); kn=fnorm(K); pn=fnorm(Psrc)
    assert kn>1e-14 and pn>=np.sqrt(2)-1e-9
    # Q=P_target Q P_source => exactly reconstruct from its right-subspace core.
    reconstruction=Utarget@K@Usrc.T@Psrc
    re=rel(reconstruction,Q)
    restriction=kn/np.sqrt(2)
    extension=qn/kn
    source_condition=pn/np.sqrt(2)
    rate=qn/pn
    ratio_error=abs(rate-restriction*extension/source_condition)
    return dict(raw_rate=rate,restricted_rate=restriction,
       ambient_extension_factor=extension,source_projector_condition=source_condition,
       projector_source_frobenius=pn,restricted_core_frobenius=kn,
       full_crossblock_frobenius=qn,core_reconstruction_relative_error=re,
       factorization_absolute_error=ratio_error)

def process_branch(branch):
    seed,tau=branch['seed'],branch['tau']
    row=[];pair_rows=[];data={};worst={'reconstruction':0.,'rate':0.,'projector_rank_residual':0.}
    for idx in range(1,79):
        frames={}; projections={}; eigs={}
        for k in range(1,6):
            P=branch['P'][(idx,k)]
            frames[k],eigs[k]=orthonormal_right_range(P)
            projections[k]=P
            worst['projector_rank_residual']=max(worst['projector_rank_residual'],float(eigs[k][2]))
        temp=[]
        for j in range(1,6):
            for i in range(1,6):
                if i==j:continue
                Q=branch['Q'][(idx,j,i)]
                v=channel_metrics(Q,projections[j],frames[j],frames[i])
                raw_ref=next(t['covariant_directed_rate'] for t in branch['records']
                             if t['index']==idx and t['from_pair']==j and t['to_pair']==i)
                worst['rate']=max(worst['rate'],abs(v['raw_rate']-raw_ref))
                worst['reconstruction']=max(worst['reconstruction'],v['core_reconstruction_relative_error'])
                r=dict(seed_family=seed,tau_ref=tau,index=idx,xi=float(branch['xi'][idx]),
                    from_pair=j,to_pair=i,**v,
                    inherited_raw_rate=raw_ref,raw_rate_parent_difference=abs(v['raw_rate']-raw_ref))
                temp.append(r);row.append(r)
                if (j,i) in ((5,4),(4,5)):
                    data[(idx,j,i)]=dict(Q=Q,P=projections[j],Uj=frames[j],Ui=frames[i],row=r)
        a=next(r for r in temp if r['from_pair']==5 and r['to_pair']==4)
        b=next(r for r in temp if r['from_pair']==4 and r['to_pair']==5)
        Rraw=a['raw_rate']/b['raw_rate'];Rcore=a['restricted_rate']/b['restricted_rate']
        Rext=a['ambient_extension_factor']/b['ambient_extension_factor']
        Rcond=b['source_projector_condition']/a['source_projector_condition']
        angle=np.linalg.svd(frames[4].T@frames[5],compute_uv=False)
        strongest=max(temp,key=lambda r:r['restricted_rate'])
        pair_rows.append(dict(seed_family=seed,tau_ref=tau,index=idx,xi=float(branch['xi'][idx]),
            raw_ratio_5to4_over_4to5=Rraw,
            restricted_ratio_5to4_over_4to5=Rcore,
            ambient_extension_ratio=Rext,
            source_condition_ratio=Rcond,
            exact_ratio_product=Rcore*Rext*Rcond,
            ratio_factorization_error=abs(Rraw-Rcore*Rext*Rcond),
            core_5to4=a['restricted_rate'],core_4to5=b['restricted_rate'],
            projector_norm_5=a['projector_source_frobenius'],
            projector_norm_4=b['projector_source_frobenius'],
            smallest_principal_angle_4_5_degrees=float(np.rad2deg(np.arccos(np.clip(angle[0],0,1)))),
            largest_principal_angle_4_5_degrees=float(np.rad2deg(np.arccos(np.clip(angle[1],0,1)))),
            largest_restricted_channel=f"{strongest['from_pair']}->{strongest['to_pair']}",
            restricted_5to4_largest_of_20=strongest['from_pair']==5 and strongest['to_pair']==4,
            restricted_5to4_exceeds_reverse=Rcore>1,
            raw_5to4_exceeds_reverse=Rraw>1))
    return row,pair_rows,data,worst

def common_frame(branch_data,pair_rows):
    rows=[];maxes=dict(max_restricted_common_interior=0.,max_raw_common_interior=0.,
                       max_P_common_interior=0.,max_Q_common_interior=0.,
                       max_restricted_common_all=0.,max_Q_common_all=0.)
    rr={(r['seed_family'],r['tau_ref'],r['index']):r for r in pair_rows}
    for seed in SEEDS:
        reference=branch_data[(seed,1.)]
        for tau in (0.5,2.):
            source=branch_data[(seed,tau)]
            D=np.diag(np.r_[np.ones(5),np.full(5,tau)]);Di=np.linalg.inv(D)
            for idx in range(1,79):
                P_tau={k:source[(idx,k,4 if k==5 else 5)]['P'] for k in (4,5)}
                P_ref={k:reference[(idx,k,4 if k==5 else 5)]['P'] for k in (4,5)}
                Ucommon={k:orthonormal_right_range(Di@P_tau[k]@D)[0] for k in (4,5)}
                for frm,to in ((5,4),(4,5)):
                    z=source[(idx,frm,to)];ref=reference[(idx,frm,to)]
                    qc=Di@z['Q']@D
                    pc=Di@z['P']@D
                    # Metric D^{-T}D^{-1} in tau coordinates, evaluated in the tau=1 chart.
                    v=channel_metrics(qc,pc,Ucommon[frm],Ucommon[to])
                    re=abs(v['restricted_rate']-ref['row']['restricted_rate'])
                    rawdiff=abs(v['raw_rate']-ref['row']['raw_rate'])
                    pe=rel(pc,ref['P']);qe=rel(qc,ref['Q'])
                    maxes['max_restricted_common_all']=max(maxes['max_restricted_common_all'],re)
                    maxes['max_Q_common_all']=max(maxes['max_Q_common_all'],qe)
                    if float(rr[(seed,tau,idx)]['xi'])>=0.001:
                        maxes['max_restricted_common_interior']=max(maxes['max_restricted_common_interior'],re)
                        maxes['max_raw_common_interior']=max(maxes['max_raw_common_interior'],rawdiff)
                        maxes['max_P_common_interior']=max(maxes['max_P_common_interior'],pe)
                        maxes['max_Q_common_interior']=max(maxes['max_Q_common_interior'],qe)
                    rows.append(dict(seed_family=seed,tau_ref=tau,index=idx,xi=float(rr[(seed,tau,idx)]['xi']),
                        from_pair=frm,to_pair=to,
                        raw_rate_local=z['row']['raw_rate'],restricted_rate_local=z['row']['restricted_rate'],
                        restricted_rate_tau1_metric=v['restricted_rate'],
                        reference_tau1_restricted_rate=ref['row']['restricted_rate'],
                        common_rate_absolute_error=re,common_raw_rate_absolute_error=rawdiff,
                        common_projector_relative_error=pe,common_crossblock_relative_error=qe))
    return rows,maxes

def plot(directions):
    for name in ['directionality_restricted_vs_oblique.png','projector_conditioning_factorization.png','spectral_subspace_principal_angles.png']:
        (OUT/name).unlink(missing_ok=True)
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for tau in TAUS:
        r=[x for x in directions if x['seed_family']=='original' and x['tau_ref']==tau]
        xs=[x['xi'] for x in r]
        axs[0].plot(xs,[x['raw_ratio_5to4_over_4to5'] for x in r],label=f'tau={tau:g}')
        axs[1].plot(xs,[x['restricted_ratio_5to4_over_4to5'] for x in r],label=f'tau={tau:g}')
    for a,lab in zip(axs,['Oblique Frobenius directional ratio','Right-subspace orthonormal restricted ratio']):
        a.axhline(1,color='black',lw=1,ls=':');a.set_ylabel(lab);a.grid(alpha=.2);a.legend()
    axs[1].set_xlabel('xi');fig.suptitle('Q550 v18.51i: Does 5 to 4 survive projector-conditioning separation?')
    fig.tight_layout();fig.savefig(OUT/'directionality_restricted_vs_oblique.png',dpi=160);plt.close(fig)
    r=[x for x in directions if x['seed_family']=='original' and x['tau_ref']==1.]
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    xs=[x['xi'] for x in r]
    for key,lab in [('restricted_ratio_5to4_over_4to5','restricted core'),('ambient_extension_ratio','ambient extension'),('source_condition_ratio','source conditioning')]:
        axs[0].plot(xs,[x[key] for x in r],label=lab)
    axs[0].axhline(1,color='black',ls=':',lw=1);axs[0].legend();axs[0].grid(alpha=.2)
    axs[0].set_ylabel('Multiplicative factor')
    axs[1].plot(xs,[x['raw_ratio_5to4_over_4to5'] for x in r],label='raw oblique ratio')
    axs[1].plot(xs,[x['exact_ratio_product'] for x in r],linestyle='--',label='product of three factors')
    axs[1].set(xlabel='xi',ylabel='total ratio');axs[1].legend();axs[1].grid(alpha=.2)
    fig.suptitle('Q550 v18.51i: Exact source-conditioning and extension separation')
    fig.tight_layout();fig.savefig(OUT/'projector_conditioning_factorization.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for tau in TAUS:
        x=[a for a in directions if a['seed_family']=='original' and a['tau_ref']==tau]
        ax.plot([a['xi'] for a in x],[a['smallest_principal_angle_4_5_degrees'] for a in x],label=f'min angle tau={tau:g}')
    ax.set(xlabel='xi',ylabel='degrees',title='Q550 v18.51i: principal-angle sensitivity of right spectral planes 4 and 5')
    ax.grid(alpha=.2);ax.legend();fig.tight_layout();fig.savefig(OUT/'spectral_subspace_principal_angles.png',dpi=160);plt.close(fig)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    branches,hdir,hledger,lineage=authenticated_parent()
    parent_dir={(r['seed_family'],float(r['tau_ref']),int(r['index'])):r for r in hdir}
    parent_rates={(r['seed_family'],float(r['tau_ref']),int(r['index']),int(r['from_pair']),int(r['to_pair'])):float(r['covariant_directed_rate']) for r in hledger}
    allrows=[];directions=[];br_data={};w=[]
    for seed in SEEDS:
        for tau in TAUS:
            row,dr,data,worst=process_branch(branches[(seed,tau)])
            allrows.extend(row);directions.extend(dr);br_data[(seed,tau)]=data;w.append(worst)
            print('RESTRICTED',seed,tau,'5->4 / 4->5',dr[-1]['restricted_ratio_5to4_over_4to5'],
                  'survives',sum(x['restricted_5to4_exceeds_reverse'] for x in dr),'/78',
                  'largest of 20',sum(x['restricted_5to4_largest_of_20'] for x in dr),flush=True)
    assert len(allrows)==9360 and len(directions)==468
    max_hparent=0.; max_rate_ledger=0.
    for r in allrows:
        key=(r['seed_family'],r['tau_ref'],r['index'],r['from_pair'],r['to_pair'])
        max_rate_ledger=max(max_rate_ledger,abs(r['raw_rate']-parent_rates[key]))
    for r in directions:
        h=parent_dir[(r['seed_family'],r['tau_ref'],r['index'])]
        max_hparent=max(max_hparent,abs(r['raw_ratio_5to4_over_4to5']-float(h['directional_rate_ratio'])))
    cov,coverr=common_frame(br_data,directions)
    assert len(cov)==624
    csvwrite('subspace_restricted_channel_ledger.csv',allrows)
    csvwrite('projector_conditioning_directionality.csv',directions)
    csvwrite('pulled_back_kinetic_similarity_controls.csv',cov)
    plot(directions)
    maxrecon=max(a['core_reconstruction_relative_error'] for a in allrows)
    maxfact=max(a['factorization_absolute_error'] for a in allrows)
    maxratio=max(a['ratio_factorization_error'] for a in directions)
    classified=[]
    for seed in SEEDS:
        for tau in TAUS:
            s=[a for a in directions if a['seed_family']==seed and a['tau_ref']==tau]
            end=s[-1]
            classified.append(dict(seed_family=seed,tau_ref=tau,
                number_positive_sections=len(s),
                restricted_5to4_exceeds_reverse=sum(a['restricted_5to4_exceeds_reverse'] for a in s),
                restricted_5to4_largest_among_20=sum(a['restricted_5to4_largest_of_20'] for a in s),
                restricted_ratio_min=min(a['restricted_ratio_5to4_over_4to5'] for a in s),
                restricted_ratio_max=max(a['restricted_ratio_5to4_over_4to5'] for a in s),
                raw_ratio_end=end['raw_ratio_5to4_over_4to5'],restricted_ratio_end=end['restricted_ratio_5to4_over_4to5'],
                extension_ratio_end=end['ambient_extension_ratio'],source_condition_ratio_end=end['source_condition_ratio'],
                min_principal_angle_end_degrees=end['smallest_principal_angle_4_5_degrees']))
    tests={
       'h_complete_sha256_and_crc':True,
       'h_reference_source_byte_exact':True,
       'g_f_e_nested_authenticated':True,
       'historical_two_10d_ivps_inherited':lineage['original_ten_dimensional_ivps_inherited']==2,
       'six_kinetic_branches':len(branches)==6,
       '468_positive_sections':len(directions)==468,
       '9360_restricted_directed_channels':len(allrows)==9360,
       'rank_two_right_eigenspace_all_samples':max(q['projector_rank_residual'] for q in w)<1e-6,
       'oblique_crossblock_reconstruction':maxrecon<3e-7,
       'all_channel_exact_factorization':maxfact<5e-10,
       'directional_ratio_three_factor_identity':maxratio<5e-10,
       'independent_h_rate_ledger_replay':max_rate_ledger<3e-6,
       'independent_h_directional_ratio_replay':max_hparent<2e-6,
       'kinetic_pulled_back_Q_covariance_interior':coverr['max_Q_common_interior']<1e-7,
       'kinetic_pulled_back_P_covariance_interior':coverr['max_P_common_interior']<1e-7,
       'kinetic_pulled_back_restricted_rate_interior':coverr['max_restricted_common_interior']<1e-6,
       'kinetic_pulled_back_raw_rate_interior':coverr['max_raw_common_interior']<1e-6,
       'no_one_third_acceptance':True,
       'no_new_original_physical_IVP':True,
    }
    report=dict(version='v18.51i',title='Projector Conditioning Separation & Covariant Directionality Audit',
        classification='NUMERICAL_RESTRICTED_SUBSPACE_DIRECTIONALITY_DIAGNOSTIC_NOT_OBSERVER_INDEPENDENT_MATERIAL_ENERGY_TRANSFER',
        lineage=lineage,
        model=dict(seeds=list(SEEDS),tau_refs=list(TAUS),xi=[0.,.05],
              sections_per_branch_positive=78,physical_tangent_ivps_inherited=2,no_new_ivp=True),
        counts=dict(sections=468,channels=9360,covariance_controls=len(cov)),
        mathematics={
            'crossblock':'Q_ij=P_i (Pprime_j-[B,P_j]) P_j, from exact inherited v18.51h Riesz decomposition',
            'frames':'U_j orthonormal spanning range(P_j), with inner product declared in physical kinetic Cartesian chart',
            'restricted_rate':'||U_i^T Q_ij U_j||_F / sqrt(2)',
            'oblique_rate':'||Q_ij||_F / ||P_j||_F',
            'exact_split':'oblique_rate = restricted_rate * (||Q_ij||_F/||K_ij||_F) / (||P_j||_F/sqrt(2))',
            'reverse_ratio':'raw_54/raw_45=restricted_54/restricted_45 * extension_54/extension_45 * condition_source_4/condition_source_5',
            'metric_similarity':'For tau, D=diag(I5,tau I5); compare D^-1 Q_tau D and D^-1 P_tau D with tau=1. The pulled-back metric is D^-T D^-1; Euclidean norms in different tau charts are not invariant.',
            'angles':'Principal angles of right spectral 2-planes within declared kinetic convention, not intrinsic metric invariants.'},
        quality=dict(max_core_reconstruction_error=maxrecon,max_factor_error=maxfact,
           max_direction_ratio_factor_error=maxratio,max_parent_h_raw_rate_difference=max_rate_ledger,
           max_parent_h_ratio_difference=max_hparent,kinetic_common_frame=coverr),
        observations=dict(branches=classified,restricted_survival=sum(a['restricted_5to4_exceeds_reverse'] for a in directions),
            largest_restricted_5to4=sum(a['restricted_5to4_largest_of_20'] for a in directions),
            raw_survival=sum(a['raw_5to4_exceeds_reverse'] for a in directions)),
        checks=tests,limitations=[
           'The restriction removes source projector Frobenius normalization and extension from the full ambient domain; it does not eliminate nonnormal eigenprojector geometry from Q.',
           'Restricted rates remain inner-product dependent; only after carrying the metric back to a common reference chart can covariance be asserted.',
           'No unique phase-space kinetic metric is established; tau_ref still denotes a scale convention.',
           'The right spectral planes are not necessarily orthogonal to one another and the restricted amplitudes are not physical energy fluxes.',
           'No eigenvalue-gap certificate between sampled xi points, especially near xi=0 spectral degeneracy.',
           'No new Q550 10D physical IVP integrated, no causal claim of torsion or memory, no model parameter fitted to 1/3.'
        ],software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform()))
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n',encoding='utf-8')
    print('ENDPOINTS',json.dumps(classified,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),flush=True)
    print('QUALITY',json.dumps(report['quality'],indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),flush=True)
    print('CHECKS',json.dumps(tests,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v)),flush=True)
    if not all(tests.values()):raise RuntimeError('FAILED: inspect report and scientific controls')
    print('Q550 v18.51i PASS',len(tests),'/',len(tests),flush=True)
if __name__=='__main__':main()
