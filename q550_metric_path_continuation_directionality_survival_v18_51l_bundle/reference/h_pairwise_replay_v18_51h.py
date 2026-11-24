#!/usr/bin/env python3
"""Q550 v18.51h — pairwise numerator-gap competition & covariant directionality.

Historical input: v18.51g authenticated server sendback, transitively including the
v18.51e genuine 10D material variational IVPs via f. No new physical IVPs.

The exact cross-block identity for i != j is
   P_i (P'_j - [B,P_j]) P_j
       = sum_{a in j, k in i} lambda_k R_k B R_a / (lambda_a - lambda_k).
This is evaluated with fully complex rank-one biorthogonal Riesz projectors;
conjugate terms are combined into real rank-two blocks. The shared pair-gap
is not itself a directional mechanism: numerator, cancellation, obliquity and
metric conventions remain visible and separately controlled.
"""
from __future__ import annotations
import csv, hashlib, io, json, platform, sys, zipfile
from pathlib import Path
import numpy as np
from scipy.linalg import eig
from scipy.optimize import linear_sum_assignment
import scipy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'results'
IN=ROOT/'inputs'
GNAME='q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle_server_sendback.zip'
GROOT='q550_covariant_spectral_projector_drift_time_step_invariance_v18_51g_bundle'
FNAME='q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle_server_sendback.zip'
FROOT='q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle'
ENAME='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle_server_sendback.zip'
EROOT='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle'
SEEDS=('original','autonomous')
TAUS=(0.5,1.0,2.0)
TOL_IMAG=1e-10


def sha(blob):return hashlib.sha256(blob).hexdigest()
def norm(x):return float(np.linalg.norm(x,'fro'))
def rel(a,b):return norm(a-b)/max(1.,norm(a),norm(b))
def tag(t):return f'{t:.1f}'.replace('.','p')
def write_csv(name, rows):
    assert rows, f'Empty output {name}'
    with (OUT/name).open('w',newline='',encoding='utf-8') as fd:
        w=csv.DictWriter(fd,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def verify_zip(z, root, version):
    sources=json.loads(z.read(root+'/SOURCE_MANIFEST.json'))
    outputs=json.loads(z.read(root+'/SHA256SUMS_OUTPUT.json'))
    assert sources['root']==outputs['root']==root
    assert sources['version']==outputs['version']==version
    for name,h in sources['files'].items():
        assert sha(z.read(root+'/'+name))==h, f'{version} source {name}'
    for name,h in outputs['file_sha256'].items():
        assert sha(z.read(root+'/'+name))==h, f'{version} output {name}'
    return {'source_files':len(sources['files']),'output_files':len(outputs['file_sha256'])}

def authenticated_inputs():
    path=IN/GNAME
    with zipfile.ZipFile(path) as zg:
        assert zg.testzip() is None, 'g source CRC failed'
        gverify=verify_zip(zg,GROOT,'v18.51g')
        assert zg.read(GROOT+'/scripts/run_audit.py')==(ROOT/'reference/g_projector_replay_v18_51g.py').read_bytes()
        greport=json.loads(zg.read(GROOT+'/results/report.json'))
        assert greport['version']=='v18.51g' and all(greport['checks'].values())
        assert greport['counts']['instantaneous_directed_cross_rates']==9360
        raw_g_cross=zg.read(GROOT+'/results/instantaneous_covariant_interplane_rate.csv').decode('utf-8')
        g_cross={}
        for r in csv.DictReader(io.StringIO(raw_g_cross)):
            key=(r['seed_family'],float(r['tau_ref']),int(r['index']),int(r['from_pair']),int(r['to_pair']))
            assert key not in g_cross
            g_cross[key]=float(r['instantaneous_covariant_cross_rate'])
        assert len(g_cross)==9360
        fraw=zg.read(GROOT+'/inputs/'+FNAME)
    with zipfile.ZipFile(io.BytesIO(fraw)) as zf:
        assert zf.testzip() is None
        fverify=verify_zip(zf,FROOT,'v18.51f')
        freport=json.loads(zf.read(FROOT+'/results/report.json'))
        assert freport['version']=='v18.51f' and all(freport['checks'].values())
        eraw=zf.read(FROOT+'/inputs/'+ENAME)
    with zipfile.ZipFile(io.BytesIO(eraw)) as ze:
        assert ze.testzip() is None
        everify=verify_zip(ze,EROOT,'v18.51e')
        ereport=json.loads(ze.read(EROOT+'/results/report.json'))
        assert all(ereport['scientific_checks'].values()) and ereport['full_10d_ivps']==2
        with np.load(io.BytesIO(ze.read(EROOT+'/results/material_tangent_cauchy_green_tensors.npz')),
                     allow_pickle=False) as nf:
            vals={k:nf[k].copy() for k in nf.files}
    info={'g_archive_sha256':sha(path.read_bytes()),'g':gverify,
          'g_checks':len(greport['checks']),'f_embedded_sha256':sha(fraw),'f':fverify,
          'f_checks':len(freport['checks']),'e_embedded_sha256':sha(eraw),'e':everify,
          'e_checks':len(ereport['scientific_checks']),'physical_seed_ivps':2,
          'no_new_physical_ivp':True,'historical_lineage':ereport['lineage']}
    return vals, g_cross, info

def resolved_spectrum(M,prev=None):
    """Track the same five positive-imaginary branches as authenticated g."""
    eigval,VL,VR=eig(M,left=True,right=True)
    rs=[]
    for k in range(10):
        den=np.vdot(VL[:,k],VR[:,k])
        assert abs(den)>1e-14, 'Spectral resolution ill-conditioned'
        rs.append(np.outer(VR[:,k],VL[:,k].conj())/den)
    pos=np.flatnonzero(eigval.imag>TOL_IMAG)
    neg=np.flatnonzero(eigval.imag<-TOL_IMAG)
    assert len(pos)==len(neg)==5
    elements=[]
    for a in pos:
        b=int(np.argmin(abs(eigval-np.conj(eigval[a]))))
        assert b!=a and abs(eigval[b]-np.conj(eigval[a]))<1e-8
        members=(int(a),b)
        elements.append({'lambda':eigval[a], 'members':members,
                         'P':np.real(rs[a]+rs[b])})
    if prev is None:elements.sort(key=lambda e:e['lambda'].imag)
    else:
        cm=np.abs(np.array(prev)[:,None]-np.array([e['lambda'] for e in elements])[None,:])
        ix,jx=linear_sum_assignment(cm)
        assert np.array_equal(ix,np.arange(5))
        elements=[elements[int(j)] for j in jx]
    assert rel(sum((e['P'] for e in elements),np.zeros((10,10))),np.eye(10))<1e-9
    return eigval,rs,elements

def analyze_branch(seed,tau,vals,g_cross):
    name=f'{seed}_tau_{tag(tau)}'
    xs=vals['xi_'+seed]
    MM=vals['M_'+name];BB=vals['B_'+name]
    assert len(xs)==79 and MM.shape==BB.shape==(79,10,10)
    assert np.all(np.diff(xs)>0) and norm(MM[0]-np.eye(10))<1e-9
    prev=None
    records=[];direction=[]
    matrices={};projectors={};gaps={}
    worst={'cross_block_identity_error':0.,'parent_g_rate_absolute_error':0.,
           'parent_g_rate_relative_error':0.,'max_imaginary_block_residual':0.,
           'projector_resolution_error':0.,'minimum_pair_gap':float('inf'),
           'pair_gap_symmetry_error':0.,'trace_projector_rate_error':0.}
    for idx in range(1,len(xs)):
        x=float(xs[idx]);M=MM[idx];B=BB[idx]
        eigval,Rs,els=resolved_spectrum(M,prev)
        prev=[el['lambda'] for el in els]
        Ps=[el['P'] for el in els]
        worst['projector_resolution_error']=max(worst['projector_resolution_error'],rel(sum(Ps),np.eye(10)))
        Pdot=[]
        for frm in range(5):
            pair=set(els[frm]['members'])
            pd=np.zeros((10,10),complex)
            for a in pair:
                for k in range(10):
                    if k not in pair:
                        pd+=(Rs[k]@B@M@Rs[a]+Rs[a]@B@M@Rs[k])/(eigval[a]-eigval[k])
            Pdot.append(pd.real)
            worst['trace_projector_rate_error']=max(worst['trace_projector_rate_error'],abs(np.trace(pd.real)))
        for frm in range(5):
            for to in range(5):
                if frm==to:continue
                members_fr=els[frm]['members']
                members_to=els[to]['members']
                denoms=np.array([eigval[a]-eigval[k] for a in members_fr for k in members_to])
                delta=float(np.min(abs(denoms)))
                assert delta>0
                worst['minimum_pair_gap']=min(worst['minimum_pair_gap'],delta)
                numer_terms=[];weighted_terms=[]
                for a in members_fr:
                    for k in members_to:
                        num=eigval[k]*(Rs[k]@B@Rs[a])
                        numer_terms.append(num)
                        weighted_terms.append(num/(eigval[a]-eigval[k]))
                Qcomplex=sum(weighted_terms)
                Q=Qcomplex.real
                imag_norm=norm(Qcomplex.imag)
                # Independent check via the complete spectral projector derivative.
                projection=Ps[to]@(Pdot[frm]-(B@Ps[frm]-Ps[frm]@B))@Ps[frm]
                erro=rel(Q,projection)
                worst['cross_block_identity_error']=max(worst['cross_block_identity_error'],erro)
                worst['max_imaginary_block_residual']=max(worst['max_imaginary_block_residual'],imag_norm)
                nproj=norm(Ps[frm]);pn=norm(Ps[to])
                qn=norm(Q)
                rate=qn/nproj
                key=(seed,tau,idx,frm+1,to+1)
                assert key in g_cross
                greference=g_cross[key]
                absdiff=abs(greference-rate)
                worst['parent_g_rate_absolute_error']=max(worst['parent_g_rate_absolute_error'],absdiff)
                worst['parent_g_rate_relative_error']=max(worst['parent_g_rate_relative_error'],absdiff/max(1,abs(greference)))
                term_norm_sum=sum(norm(v) for v in numer_terms)
                weighted_norm_sum=sum(norm(v) for v in weighted_terms)
                real_raw_numerator=norm(sum(numer_terms).real)
                raw_B_cross=norm(Ps[to]@B@Ps[frm])
                fact=qn/max(1e-30,weighted_norm_sum)
                assert fact>=0 and fact<1.000001
                flat_terms=[]
                # Diagnostic equal-magnitude gap counterfactual: retain the
                # *complex phase* of each original denominator.
                for n,d in zip(numer_terms,denoms):
                    flat_terms.append(n/(delta*d/abs(d)))
                flat_rate=norm(sum(flat_terms).real)/nproj
                rec={'seed_family':seed,'tau_ref':tau,'index':idx,'xi':x,
                     'from_pair':frm+1,'to_pair':to+1,
                     'pair_min_complex_gap':delta,'pair_max_complex_gap':float(np.max(abs(denoms))),
                     'gap_spread_ratio':float(np.max(abs(denoms))/delta),
                     'numerator_termwise_frobenius_sum':term_norm_sum,
                     'weighted_termwise_frobenius_sum':weighted_norm_sum,
                     'numerator_coherent_sum_frobenius':real_raw_numerator,
                     'weighted_block_frobenius':qn,'cancellation_factor':fact,
                     'effective_numerator_delta_times_block':delta*qn,
                     'generator_oblique_crossblock_frobenius':raw_B_cross,
                     'projector_source_frobenius':nproj,'projector_target_frobenius':pn,
                     'covariant_directed_rate':rate,
                     'equal_gap_magnitude_counterfactual_rate':flat_rate,
                     'g_reference_directed_rate':greference,
                     'g_reference_absolute_error':absdiff,
                     'cross_block_identity_error':erro,'imaginary_pair_conjugacy_residual':imag_norm}
                records.append(rec)
                matrices[(idx,frm+1,to+1)]=Q
                projectors[(idx,frm+1)]=Ps[frm]
                gaps[(idx,frm+1,to+1)]=delta
        left=records[-20:]
        forward=next(q for q in left if q['from_pair']==5 and q['to_pair']==4)
        backward=next(q for q in left if q['from_pair']==4 and q['to_pair']==5)
        biggest=max(left,key=lambda q:q['covariant_directed_rate'])
        f=forward;b=backward
        forward_reverse_gap=abs(f['pair_min_complex_gap']-b['pair_min_complex_gap'])
        worst['pair_gap_symmetry_error']=max(worst['pair_gap_symmetry_error'],forward_reverse_gap)
        r=f['covariant_directed_rate']/b['covariant_directed_rate']
        qratio=f['weighted_block_frobenius']/b['weighted_block_frobenius']
        pratio=b['projector_source_frobenius']/f['projector_source_frobenius']
        assert abs(r-qratio*pratio)<1e-9
        direction.append({'seed_family':seed,'tau_ref':tau,'index':idx,'xi':x,
                 'strongest_channel':f"{biggest['from_pair']}->{biggest['to_pair']}",
                 'gap_min_shared_4_5':f['pair_min_complex_gap'],
                 'gap_max_shared_4_5':f['pair_max_complex_gap'],
                 'rate_5_to_4':f['covariant_directed_rate'],
                 'rate_4_to_5':b['covariant_directed_rate'],
                 'directional_rate_ratio':r,
                 'crossblock_norm_ratio_5to4_over_4to5':qratio,
                 'source_projector_norm_ratio_P4_over_P5':pratio,
                 'ratio_reconstruction_error':abs(r-qratio*pratio),
                 'effective_numerator_ratio':f['effective_numerator_delta_times_block']/b['effective_numerator_delta_times_block'],
                 'termwise_numerator_sum_ratio':f['numerator_termwise_frobenius_sum']/b['numerator_termwise_frobenius_sum'],
                 'weighted_termwise_sum_ratio':f['weighted_termwise_frobenius_sum']/b['weighted_termwise_frobenius_sum'],
                 'cancellation_ratio':f['cancellation_factor']/b['cancellation_factor'],
                 'oblique_B_crossblock_ratio':f['generator_oblique_crossblock_frobenius']/b['generator_oblique_crossblock_frobenius'],
                 'equal_gap_counterfactual_directional_ratio':f['equal_gap_magnitude_counterfactual_rate']/b['equal_gap_magnitude_counterfactual_rate']})
    return {'seed':seed,'tau':tau,'xi':xs,'records':records,'direction':direction,
            'Q':matrices,'P':projectors,'gap':gaps,'worst':worst}

def covariance(branches):
    rows=[]
    maxes={'common_frame_Q_interior_rel':0.,'common_frame_Q_all_rel':0.,
           'common_frame_P_interior_rel':0.,'common_frame_gap_absolute':0.,
           'common_frame_rate_interior_absolute':0.,'common_frame_rate_all_absolute':0.}
    for seed in SEEDS:
        base=branches[(seed,1.)]
        for tau in (.5,2.):
            br=branches[(seed,tau)]
            D=np.diag([1.]*5+[tau]*5);Di=np.linalg.inv(D)
            dbase={(r['index'],r['from_pair'],r['to_pair']):r for r in base['records']}
            for r in br['records']:
                idx=r['index'];frm=r['from_pair'];to=r['to_pair']
                rb=dbase[(idx,frm,to)]
                q_common=Di@br['Q'][(idx,frm,to)]@D
                q_base=base['Q'][(idx,frm,to)]
                per=rel(q_common,q_base)
                pi_common=Di@br['P'][(idx,frm)]@D
                pi_base=base['P'][(idx,frm)]
                p_error=rel(pi_common,pi_base)
                common_rate=norm(q_common)/norm(pi_common)
                rerr=abs(common_rate-rb['covariant_directed_rate'])
                gerr=abs(r['pair_min_complex_gap']-rb['pair_min_complex_gap'])
                maxes['common_frame_Q_all_rel']=max(maxes['common_frame_Q_all_rel'],per)
                maxes['common_frame_rate_all_absolute']=max(maxes['common_frame_rate_all_absolute'],rerr)
                maxes['common_frame_gap_absolute']=max(maxes['common_frame_gap_absolute'],gerr)
                if r['xi']>=.001:
                    maxes['common_frame_Q_interior_rel']=max(maxes['common_frame_Q_interior_rel'],per)
                    maxes['common_frame_P_interior_rel']=max(maxes['common_frame_P_interior_rel'],p_error)
                    maxes['common_frame_rate_interior_absolute']=max(maxes['common_frame_rate_interior_absolute'],rerr)
                rows.append({'seed_family':seed,'tau_ref':tau,'index':idx,'xi':r['xi'],
                             'from_pair':frm,'to_pair':to,
                             'raw_covariant_directed_rate':r['covariant_directed_rate'],
                             'tau1_reference_rate':rb['covariant_directed_rate'],
                             'common_tau1_frame_rate':common_rate,
                             'common_frame_rate_absolute_error':rerr,
                             'common_frame_Q_relative_error':per,
                             'common_frame_P_relative_error':p_error,
                             'pair_gap_absolute_difference':gerr})
    return rows,maxes

def plot(branches):
    a=branches[('original',1.)]
    x=[row['xi'] for row in a['direction']]
    f=[next(r for r in a['records'] if r['index']==k and r['from_pair']==5 and r['to_pair']==4) for k in range(1,79)]
    b=[next(r for r in a['records'] if r['index']==k and r['from_pair']==4 and r['to_pair']==5) for k in range(1,79)]
    fig,axes=plt.subplots(2,1,figsize=(10,8),sharex=True)
    axes[0].plot(x,[r['covariant_directed_rate'] for r in f],label='5 to 4')
    axes[0].plot(x,[r['covariant_directed_rate'] for r in b],label='4 to 5')
    axes[0].set(ylabel='Directed covariant rate (oblique norm)',title='Q550 v18.51h: directional rate and shared pair gap')
    axes[0].legend();axes[0].grid(alpha=.25)
    axes[1].plot(x,[r['pair_min_complex_gap'] for r in f],label='Shared 4/5 minimum eigenvalue gap')
    axes[1].set(xlabel=r'$\xi$',ylabel='Complex eigenvalue gap')
    axes[1].grid(alpha=.25);axes[1].legend()
    fig.tight_layout();fig.savefig(OUT/'pairwise_rate_and_shared_gap.png',dpi=160);plt.close(fig)
    fig,axes=plt.subplots(2,1,figsize=(10,8),sharex=True)
    axes[0].plot(x,[r['effective_numerator_delta_times_block'] for r in f],label='5 to 4')
    axes[0].plot(x,[r['effective_numerator_delta_times_block'] for r in b],label='4 to 5')
    axes[0].set(ylabel=r'$\delta\|P_i (\mathcal{D}P_j)P_j\|_F$',title='Effective numerator and cancellation (diagnostic, not a unique cause)')
    axes[0].grid(alpha=.25);axes[0].legend()
    axes[1].plot(x,[r['cancellation_factor'] for r in f],label='5 to 4')
    axes[1].plot(x,[r['cancellation_factor'] for r in b],label='4 to 5')
    axes[1].set(xlabel=r'$\xi$',ylabel='Coherent / termwise weighted norm')
    axes[1].grid(alpha=.25);axes[1].legend()
    fig.tight_layout();fig.savefig(OUT/'pairwise_numerator_cancellation.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for tau in TAUS:
        b=branches[('original',tau)]['direction']
        ax.plot([r['xi'] for r in b],[r['directional_rate_ratio'] for r in b],label=f'raw tau={tau:g}')
    ax.plot(x,[r['directional_rate_ratio'] for r in branches[('original',1.)]['direction']],color='black',linewidth=1,linestyle='--',label='common tau=1 reference')
    ax.set(xlabel=r'$\xi$',ylabel='rate (5 to 4) / rate (4 to 5)',
           title='Kinetic convention dependence of directed Frobenius ratio')
    ax.legend();ax.grid(alpha=.25);fig.tight_layout();fig.savefig(OUT/'kinetic_directionality_convention_sensitivity.png',dpi=160);plt.close(fig)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    values,g_rates,lineage=authenticated_inputs()
    print('AUTHENTICATED g / f / e 10D lineage:',json.dumps({k:v for k,v in lineage.items() if k!='historical_lineage'}),flush=True)
    branches={}
    for seed in SEEDS:
        for tau in TAUS:
            b=analyze_branch(seed,tau,values,g_rates)
            branches[(seed,tau)]=b
            print('BRANCH',seed,tau,'rates',len(b['records']),'dominant 5->4',sum(r['strongest_channel']=='5->4' for r in b['direction']),
                  'identity error',b['worst']['cross_block_identity_error'],'g error',b['worst']['parent_g_rate_absolute_error'],flush=True)
    records=[r for b in branches.values() for r in b['records']]
    direction=[r for b in branches.values() for r in b['direction']]
    cov,cm=covariance(branches)
    assert len(records)==9360 and len(direction)==468 and len(cov)==6240
    write_csv('pairwise_numerator_gap_ledger.csv',records)
    write_csv('pairwise_directionality_decomposition.csv',direction)
    write_csv('kinetic_common_frame_covariance.csv',cov)
    plot(branches)
    worst={k:max(b['worst'][k] for b in branches.values()) for k in next(iter(branches.values()))['worst'] if k!='minimum_pair_gap'}
    worst['minimum_pair_gap']=min(b['worst']['minimum_pair_gap'] for b in branches.values())
    endpoints=[dict(r) for b in branches.values() for r in b['direction'][-1:]]
    all_dir_5to4=sum(r['strongest_channel']=='5->4' for r in direction)
    min_ratios={str(tau):min(q['directional_rate_ratio'] for q in direction if q['tau_ref']==tau) for tau in TAUS}
    max_ratios={str(tau):max(q['directional_rate_ratio'] for q in direction if q['tau_ref']==tau) for tau in TAUS}
    tests={
      'g_archive_source_output_sha256_and_CRC':True,
      'f_and_e_embedded_genealogy_source_output_sha256':True,
      'historical_g_script_exact_identity':True,
      'g_parent_scientific_controls_pass':True,
      'genuine_10d_tangent_generator_two_seed_IVPs':lineage['physical_seed_ivps']==2,
      'six_branches_and_468_positive_sections':len(branches)==6 and len(direction)==468,
      '9360_directed_pairwise_ledger_rows':len(records)==9360,
      'positive_pair_gaps_in_all_samples':worst['minimum_pair_gap']>0,
      'source_target_shared_gap_symmetry':worst['pair_gap_symmetry_error']<1e-12,
      'complete_projector_resolution':worst['projector_resolution_error']<1e-8,
      'projector_derivative_trace_zero':worst['trace_projector_rate_error']<1e-7,
      'exact_numerator_gap_crossblock_identity':worst['cross_block_identity_error']<2e-7,
      'conjugate_complex_pair_real_block':worst['max_imaginary_block_residual']<1e-7,
      'independent_parent_g_rates_replayed':worst['parent_g_rate_absolute_error']<3e-6,
      'direction_ratio_algebraic_reconstruction':max(r['ratio_reconstruction_error'] for r in direction)<1e-10,
      'all_5to4_raw_grid_dominance':all_dir_5to4==468,
      'tau_common_frame_Q_covariance_interior':cm['common_frame_Q_interior_rel']<1e-7,
      'tau_common_frame_projector_covariance_interior':cm['common_frame_P_interior_rel']<1e-7,
      'tau_common_frame_rate_covariance_interior':cm['common_frame_rate_interior_absolute']<2e-6,
      'tau_invariant_complex_pair_gap':cm['common_frame_gap_absolute']<1e-10,
      'no_one_third_acceptance_gate':True,
      'no_new_physical_ivp_solved':lineage['no_new_physical_ivp'],
    }
    report={'version':'v18.51h',
      'title':'Pairwise Numerator–Gap Competition & Covariant Directionality Audit',
      'classification':'NUMERICAL_PAIRWISE_COVARIANT_SPECTRAL_DIAGNOSTIC_NOT_MATERIAL_TORSION_ENERGY_TRANSFER_OR_MEMORY_CERTIFICATE',
      'lineage':lineage,'model':{'seeds':list(SEEDS),'kinetic_tau_refs':list(TAUS),
                                'xi_interval':[0.,0.05],'first_resolved_spectral_time':6.825e-05,
                                'physical_IVPs_inherited_not_new':2},
      'counts':{'branches':6,'positive_sections':468,'directed_crossblocks':len(records),
                'directionality_sections':len(direction),'cross_convention_comparisons':len(cov)},
      'mathematics':{
         'exact_crossblock':'P_i (Pprime_j-[B,P_j]) P_j = sum_{a in j,k in i} lambda_k R_k B R_a/(lambda_a-lambda_k)',
         'rate':'Frobenius norm of exact crossblock divided by source projector Frobenius norm',
         'shared_gap':'delta_{ij}=min_{a in j,k in i}|lambda_a-lambda_k|=delta_{ji}',
         'exact_ratio':'r_(5to4)/r_(4to5) = (norm Q_5to4 / norm Q_4to5) * (norm P4 / norm P5)',
         'effective_numerator':'delta * norm(Q); an exact bookkeeping identity, NOT an independent physical mechanism',
         'cancellation':'norm(sum complex weighted rank-1 terms) / sum(norm of each weighted term)',
         'equal_gap_counterfactual':'replace each |lambda_a-lambda_k| with pair minimum, preserve complex denominator phase; diagnostic only',
         'kinetic_similarity':'D_tau=diag(I5,tau I5); exact similarity covariance of M,B,P,Q, not Euclidean norm invariance'},
      'numerical_quality':{'maxima':worst,'kinetic_similarity':cm},
      'persistent_observations':{'raw_5to4_largest_channels':all_dir_5to4,
                                 'raw_ratio_min_by_tau':min_ratios,
                                 'raw_ratio_max_by_tau':max_ratios,
                                 'endpoint':endpoints},
      'limitations':[
       'Samples only: 78 positive xi sections per branch, no continuous spectral-gap certificate',
       'At xi=0 the map is identity and the ten eigenvalues are degenerate',
       'Raw directed Frobenius rates depend on nonorthogonal kinetic-state similarity',
       'A shared unordered pair gap cannot independently explain 5->4 versus 4->5',
       'No inference of energy flow, geometric torsion, autonomous kappa activation, or material hysteresis',
       'Exact numerator/gap splitting is algebraic; termwise phases and cancellations prevent unique source attribution',
       'No new Q550 physical initial-value problem or independent kappa state was integrated',
       'The 1/3 heuristic is explicitly retired'],
      'checks':tests,
      'software':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__,
                  'matplotlib':matplotlib.__version__,'platform':platform.platform()}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False,default=lambda o:o.item() if isinstance(o,np.generic) else str(o))+'\n',encoding='utf-8')
    print('ENDPOINT 5/4 PAIR DECOMPOSITION',json.dumps(endpoints,indent=2),flush=True)
    print('QUALITY',json.dumps(report['numerical_quality'],indent=2),flush=True)
    print('CHECKS',json.dumps(tests,indent=2,default=lambda o:o.item() if isinstance(o,np.generic) else str(o)),flush=True)
    if not all(tests.values()):raise RuntimeError('Scientific checks did not all pass; inspect results/report.json')
    print(f'Q550 v18.51h PASS {len(tests)}/{len(tests)} scientific checks',flush=True)

if __name__=='__main__': main()
