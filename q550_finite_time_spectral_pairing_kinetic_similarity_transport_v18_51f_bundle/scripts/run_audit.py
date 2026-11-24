#!/usr/bin/env python3
"""Q550 v18.51f: authentic v18.51e full finite-time material transport spectral audit.

The parent was generated from two authentic driven Q550 10D physical IVPs and
continuously integrated 10D tangent jets. This version performs *no new IVP*:
it audits the complete 79-section M/F/L/C tensors from that authenticated parent.
No Floquet exponents, canonical phase metric, physical torsion, or material
memory are inferred from finite-time eigenvalues or their oblique projectors.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, platform, sys, zipfile
from pathlib import Path
import numpy as np
from scipy.linalg import eig, subspace_angles
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'results'
PARENT_NAME='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle_server_sendback.zip'
PARENT_ROOT='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle'
TAUS=(0.5,1.,2.)
SEEDS=('original','autonomous')
EYE=np.eye(10)

def sha(data): return hashlib.sha256(data).hexdigest()
def fro(a): return float(np.linalg.norm(a,'fro'))
def rel(a,b): return fro(a-b)/max(1.,fro(a),fro(b))
def tag(t): return ('%.1f'%t).replace('.','p')
def csv_write(path,rows):
    if not rows: raise RuntimeError('No rows for '+str(path))
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def authenticate_parent():
    data=(ROOT/'inputs'/PARENT_NAME)
    expected=(ROOT/'SOURCE_MANIFEST.json')
    if not data.is_file(): raise RuntimeError('Missing parent server sendback '+str(data))
    with zipfile.ZipFile(data,'r') as z:
        if z.testzip() is not None: raise RuntimeError('Corrupted parent ZIP')
        def read(path): return z.read(PARENT_ROOT+'/'+path)
        src=json.loads(read('SOURCE_MANIFEST.json'))
        out=json.loads(read('SHA256SUMS_OUTPUT.json'))
        if (src['root'],src['version'])!=(PARENT_ROOT,'v18.51e'): raise RuntimeError('Unexpected parent source identity')
        if (out['root'],out['version'])!=(PARENT_ROOT,'v18.51e'): raise RuntimeError('Unexpected parent output identity')
        for k,h in src['files'].items():
            if sha(read(k))!=h: raise RuntimeError('Parent source SHA mismatch '+k)
        for k,h in out['file_sha256'].items():
            if sha(read(k))!=h: raise RuntimeError('Parent output SHA mismatch '+k)
        report=json.loads(read('results/report.json'))
        if report['version']!='v18.51e' or not all(report['scientific_checks'].values()):
            raise RuntimeError('Parent failed scientific checks')
        if int(report['num_rows'])!=474 or int(report['sections_per_branch'])!=79 or int(report['full_10d_ivps'])!=2:
            raise RuntimeError('Parent physical replay scope mismatch')
        buf=io.BytesIO(read('results/material_tangent_cauchy_green_tensors.npz'))
        with np.load(buf,allow_pickle=False) as npz: vals={k:npz[k].copy() for k in npz.files}
        lineage={'parent_archive_sha256':sha(data.read_bytes()),
                 'parent_root':PARENT_ROOT,
                 'parent_source_count':len(src['files']),
                 'parent_output_count':len(out['file_sha256']),
                 'original_solver_lineage':report['lineage'],
                 'parent_checks_passed':len(report['scientific_checks']),
                 'source_of_tensors':'v18.51e original+autonomous 10D model IVPs and continuous tangent integrations',
                 'no_new_ivps':True}
    print('AUTHENTICATED v18.51e full 10D parent: source',len(src['files']), 'results',len(out['file_sha256']),flush=True)
    return vals,report,lineage

def extract_pairs(M, xi, tol_imag):
    """Riesz projectors for 5 non-real conjugate pairs, with left-right duality.

    P_j = v_j w_j^H/(w_j^H v_j) + complex-conjugate term;
    P_j is real, rank two, generally OBLIQUE and not Euclidean orthogonal.
    """
    ev,vl,vr=eig(M,left=True,right=True)
    plus=np.flatnonzero(ev.imag>tol_imag)
    minus=np.flatnonzero(ev.imag< -tol_imag)
    if len(plus)!=5 or len(minus)!=5:
        raise RuntimeError(f'Expected 5 complex pairs xi={xi}, +{len(plus)} -{len(minus)}')
    result=[]
    for k in plus:
        lam=ev[k];v=vr[:,k];w=vl[:,k]
        overlap=np.vdot(w,v)
        if abs(overlap)<1.e-13: raise RuntimeError('Nearly defective eigenpair')
        Pc=np.outer(v,np.conjugate(w))/overlap
        P=(Pc+np.conjugate(Pc)).real
        Z=np.column_stack((v.real,v.imag))
        q,r=np.linalg.qr(Z)
        if abs(np.linalg.det(r))<1.e-12:
            raise RuntimeError('Rank-deficient real modal eigenplane')
        competitors=np.delete(ev,[k,int(np.argmin(abs(ev-lam.conjugate())))])
        pair_gap=float(np.min(abs(lam-competitors)))
        conjugate_gap=float(abs(lam-lam.conjugate()))
        result.append(dict(lam=lam,P=P,Q=q[:,:2],kappa=float(np.linalg.norm(v)*np.linalg.norm(w)/abs(overlap)),
                           gap=pair_gap,conj_gap=conjugate_gap,
                           idempotence=rel(P@P,P),commute=rel(M@P,P@M)))
    return result

def order_pairs(raw,prev=None):
    if prev is None: return sorted(raw,key=lambda x: x['lam'].imag)
    prev_lams=np.array([r['lam'] for r in prev]);curr_lams=np.array([r['lam'] for r in raw])
    # A physically passive spectral matching by complex eigenvalue position.
    ix,jx=linear_sum_assignment(abs(prev_lams[:,None]-curr_lams[None,:]))
    assert np.array_equal(ix,np.arange(5))
    return [raw[j] for j in jx]

def calc_branch(seed,tau,vals,opts):
    xi=vals['xi_'+seed]
    tagtau=tag(tau)
    M=vals[f'M_{seed}_tau_{tagtau}']
    F=vals[f'F_{seed}_tau_{tagtau}']
    L=vals[f'L_{seed}_tau_{tagtau}']
    C=vals[f'C_{seed}_tau_{tagtau}']
    if M.shape!=(79,10,10) or F.shape!=M.shape or L.shape!=M.shape or C.shape!=M.shape or xi.shape!=(79,):
        raise RuntimeError('Parent tensor shape mismatch')
    if np.max(np.abs(np.diff(xi)<=0))>0: raise RuntimeError('Nonincreasing xi grid')
    if not np.allclose(xi[0],0) or not np.allclose(xi[-1],0.05):raise RuntimeError('Expected finite-time section interval not found')
    if fro(M[0]-EYE)>1e-10:raise RuntimeError('Initial M not identity')
    if max(rel(C[k],M[k].T@M[k]) for k in (0,10,40,78))>1e-11:raise RuntimeError('Parent C consistency failure')
    if max(rel(M[k],L[k]@F[k]@np.linalg.inv(L[0])) for k in (0,10,40,78))>1e-11:
        raise RuntimeError('Parent genuine finite-time M reconstruction failure')
    times=[]; pair_rows=[]; cross_rows=[];prev=None
    min_gap=np.inf; max_proj_idem=0;max_sum=0;max_inter=0;max_comm=0;max_conjugacy=0;max_det=0;max_projector=0;max_cond=0
    for ind in range(1,len(xi)):
        t=float(xi[ind]); mat=M[ind]
        curr=order_pairs(extract_pairs(mat,t,opts.imag_tolerance),prev)
        projectors=[p['P'] for p in curr]
        sump=sum(projectors,np.zeros((10,10)))
        sumerr=rel(sump,EYE);max_sum=max(max_sum,sumerr)
        idem=max(p['idempotence'] for p in curr);max_proj_idem=max(max_proj_idem,idem)
        comm=max(p['commute'] for p in curr);max_comm=max(max_comm,comm)
        inter=max(fro(projectors[j]@projectors[k]) for j in range(5) for k in range(5) if j!=k)
        max_inter=max(max_inter,inter)
        min_gap=min(min_gap,min(p['gap'] for p in curr))
        max_cond=max(max_cond,max(p['kappa'] for p in curr))
        det_prod=float(np.prod([abs(p['lam'])**2 for p in curr]));det=float(np.linalg.det(mat))
        det_err=abs(det_prod-det)/max(1.,abs(det));max_det=max(max_det,det_err)
        conj_err=max(min(abs(p['lam'].conjugate()-e) for e in np.linalg.eigvals(mat)) for p in curr)
        max_conjugacy=max(max_conjugacy,conj_err)
        for j,p in enumerate(curr):
            lam=p['lam']; ang=float(np.angle(lam));mod=float(abs(lam))
            row={'seed_family':seed,'tau_ref':tau,'index':ind,'xi':t,'pair_id':j+1,
                'lambda_real':float(lam.real),'lambda_imag_positive':float(lam.imag),
                'lambda_modulus':mod,'lambda_argument_rad':ang,'log_modulus_over_xi':float(np.log(mod)/t),
                'angle_over_xi':ang/t,'nearest_other_pair_gap':p['gap'],'conjugate_gap':p['conj_gap'],
                'eigenvalue_condition_number':p['kappa'],'riesz_projector_frobenius_norm':fro(p['P']),
                'riesz_projector_idempotence_error':p['idempotence'],'commutator_relative_error':p['commute'],
                'next_step_principal_angle_deg':None, 'next_step_transported_angle_deg':None,
                'oblique_interplane_leakage':None,'oblique_interplane_leakage_per_xi':None}
            if prev is not None:
                dt=t-float(xi[ind-1]);T=mat@np.linalg.inv(M[ind-1])
                Qprev=prev[j]['Q'];Qnow=p['Q'];qt,_=np.linalg.qr(T@Qprev)
                angle=float(np.degrees(np.max(subspace_angles(Qnow,Qprev))))
                transported=float(np.degrees(np.max(subspace_angles(Qnow,qt))))
                leak=fro((EYE-p['P'])@T@prev[j]['P'])/max(1.e-20,fro(T@prev[j]['P']))
                row.update(next_step_principal_angle_deg=angle,next_step_transported_angle_deg=transported,
                           oblique_interplane_leakage=leak,oblique_interplane_leakage_per_xi=leak/dt)
                for jj,q in enumerate(curr):
                    numer=fro(q['P']@T@prev[j]['P'])
                    cross_rows.append({'seed_family':seed,'tau_ref':tau,'index':ind,'xi':t,
                              'from_pair':j+1,'to_pair':jj+1,'cocycle_projected_frobenius_ratio':numer/max(1.e-20,fro(T@prev[j]['P'])),
                              'is_diagonal':int(j==jj)})
            pair_rows.append(row)
        times.append({'seed_family':seed,'tau_ref':tau,'index':ind,'xi':t,'pair_count':5,
            'min_nonconjugate_spectral_gap':min(p['gap'] for p in curr),
            'max_pair_condition_number':max(p['kappa'] for p in curr),
            'spectral_projector_resolution_error':sumerr,'spectral_projector_interpair_error':inter,
            'determinant_from_pairs':det_prod,'determinant_direct':det,
            'largest_cauchy_green_stretch':float(np.sqrt(np.max(np.linalg.eigvalsh(C[ind])))),
            'maximum_oblique_interplane_leakage':max(float(r['oblique_interplane_leakage']) for r in pair_rows[-5:] if r['oblique_interplane_leakage'] is not None) if prev is not None else None})
        prev=curr
    # Explicitly no projector at xi=0; M(0)=I is 10-fold degenerate.
    summary={'seed_family':seed,'tau_ref':tau,'sections_total':len(xi),'sections_nondegenerate':len(times),
        'first_nondegenerate_xi':float(xi[1]),'last_xi':float(xi[-1]),
        'complex_pairs_at_each_positive_section':all(t['pair_count']==5 for t in times),
        'minimum_pair_separation':min_gap,'max_pair_condition':max_cond,
        'max_projector_idempotence_error':max_proj_idem,'max_projector_resolution_error':max_sum,
        'max_projector_disjointness_error':max_inter,'max_projector_commutation_error':max_comm,
        'max_conjugate_pair_error':max_conjugacy,'max_determinant_product_error':max_det,
        'endpoint_volume':float(np.linalg.det(M[-1])),
        'endpoint_max_modulus':max(abs(p['lam']) for p in curr),
        'endpoint_min_modulus':min(abs(p['lam']) for p in curr),
        'endpoint_max_oblique_leakage':max(float(r['oblique_interplane_leakage']) for r in pair_rows[-5:]),
        'max_oblique_leakage':max(float(r['oblique_interplane_leakage']) for r in pair_rows if r['oblique_interplane_leakage'] is not None),
        'max_transported_subspace_angle_deg':max(float(r['next_step_transported_angle_deg']) for r in pair_rows if r['next_step_transported_angle_deg'] is not None),
        'endpoint_eigenpair_angles_rad':[float(p['lambda_argument_rad']) for p in pair_rows[-5:]],
        'endpoint_eigenpair_moduli':[float(p['lambda_modulus']) for p in pair_rows[-5:]]}
    return {'seed':seed,'tau':tau,'xi':xi,'M':M,'times':times,'pair_rows':pair_rows,
            'cross_rows':cross_rows,'summary':summary,'parent_F':F,'parent_L':L,'parent_C':C}

def similarity_controls(branches):
    rows=[];max_similarity=0;max_eigenvalue=0;max_projector=0;max_cg=0
    for seed in SEEDS:
        b=branches[(seed,1.)]
        for tau in (0.5,2.):
            bt=branches[(seed,tau)];D=np.diag([1.]*5+[tau]*5);Dinv=np.linalg.inv(D)
            for k in range(79):
                Msim=D@b['M'][k]@Dinv
                sim=rel(bt['M'][k],Msim);max_similarity=max(max_similarity,sim)
                if k==0:continue
                old=b['pair_rows'][(k-1)*5:k*5];new=bt['pair_rows'][(k-1)*5:k*5]
                lamdiff=max(abs(complex(x['lambda_real'],x['lambda_imag_positive'])-
                                complex(y['lambda_real'],y['lambda_imag_positive'])) for x,y in zip(new,old))
                max_eigenvalue=max(max_eigenvalue,lamdiff)
                # Recompute projectors for independent pairwise covariance check.
                pold=order_pairs(extract_pairs(b['M'][k],float(b['xi'][k]),1.e-10))
                pnew=order_pairs(extract_pairs(bt['M'][k],float(bt['xi'][k]),1.e-10))
                proj=max(rel(x['P'],D@y['P']@Dinv) for x,y in zip(pnew,pold));max_projector=max(max_projector,proj)
                cg_mismatch=rel(bt['parent_C'][k],Dinv.T@b['parent_C'][k]@Dinv)
                # IMPORTANT: C_tau is NOT similar to C_1: M_tau = D M_1 D^-1.
                # The above expression omits the left D^T D and must not be used as covariance.
                c_expected=Msim.T@Msim
                cg_res=rel(bt['parent_C'][k],c_expected);max_cg=max(max_cg,cg_res)
                rows.append({'seed_family':seed,'tau_ref':tau,'index':k,'xi':float(b['xi'][k]),
                    'material_similarity_relative_error':sim,'eigenvalue_similarity_max_abs_error':lamdiff,
                    'real_riesz_projector_similarity_error':proj,
                    'cauchy_green_from_similar_M_error':cg_res,
                    'naive_C_similarity_difference_not_control':cg_mismatch})
    return rows,{'max_material_similarity_relative_error':max_similarity,
                 'max_eigenvalue_similarity_absolute_error':max_eigenvalue,
                 'max_riesz_projector_similarity_relative_error':max_projector,
                 'max_cauchy_green_reconstruction_error':max_cg}

def seed_controls(branches):
    rows=[]
    for tau in TAUS:
        a=branches[('original',tau)];b=branches[('autonomous',tau)]
        for i in range(1,79):
            first=a['pair_rows'][(i-1)*5:i*5];second=b['pair_rows'][(i-1)*5:i*5]
            for p,(x,y) in enumerate(zip(first,second),1):
                l1=complex(x['lambda_real'],x['lambda_imag_positive']);l2=complex(y['lambda_real'],y['lambda_imag_positive'])
                rows.append({'tau_ref':tau,'index':i,'xi':float(a['xi'][i]),'pair_id':p,
                    'seed_eigenvalue_abs_difference':abs(l1-l2),
                    'seed_modulus_abs_difference':abs(x['lambda_modulus']-y['lambda_modulus']),
                    'seed_phase_abs_difference_rad':abs(x['lambda_argument_rad']-y['lambda_argument_rad'])})
    return rows

def plots(branches):
    d=branches[('original',1.)]['pair_rows']; fig,ax=plt.subplots(figsize=(10,6))
    for j in range(1,6):
        rr=[r for r in d if r['pair_id']==j]
        ax.plot([r['xi'] for r in rr],[r['lambda_argument_rad'] for r in rr],label=f'Pair {j}')
    ax.set(xlabel=r'Finite-time $\xi$',ylabel='Positive eigenvalue phase [rad]',title='Q550 v18.51f — five finite-time conjugate eigenpair phases (original)')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'spectral_pair_phases.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for j in range(1,6):
        rr=[r for r in d if r['pair_id']==j]
        ax.plot([r['xi'] for r in rr],[r['lambda_modulus'] for r in rr],label=f'Pair {j}')
    ax.set(xlabel=r'Finite-time $\xi$',ylabel='Eigenvalue modulus',title='Q550 v18.51f — eigenvalue moduli (not singular stretches)')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'spectral_pair_moduli.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for j in range(1,6):
        rr=[r for r in d if r['pair_id']==j and r['oblique_interplane_leakage'] is not None]
        ax.plot([r['xi'] for r in rr],[r['oblique_interplane_leakage'] for r in rr],label=f'Pair {j}')
    ax.set(xlabel=r'Finite-time $\xi$',ylabel='Oblique interplane leakage / cocycle step',title='Q550 v18.51f — modal leakage during actual finite-time transport')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'spectral_interplane_leakage.png',dpi=160);plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--imag-tolerance',type=float,default=1.e-10)
    p.add_argument('--spectral-gap-floor',type=float,default=1.e-8)
    args=p.parse_args();OUT.mkdir(exist_ok=True)
    vals,parent,lineage=authenticate_parent()
    branches={}
    for seed in SEEDS:
        for tau in TAUS:
            b=calc_branch(seed,tau,vals,args);branches[(seed,tau)]=b
            s=b['summary'];print('BRANCH',seed,tau,'five pairs',s['sections_nondegenerate'],
                 'min spectral gap',s['minimum_pair_separation'],
                 'max eigenvector kappa',s['max_pair_condition'],
                 'max oblique leakage',s['max_oblique_leakage'],flush=True)
    simrows,sim=similarity_controls(branches)
    seedrows=seed_controls(branches)
    allpairs=[r for b in branches.values() for r in b['pair_rows']]
    alltimes=[r for b in branches.values() for r in b['times']]
    allcross=[r for b in branches.values() for r in b['cross_rows']]
    summaries=[b['summary'] for b in branches.values()]
    csv_write(OUT/'spectral_pair_ledger.csv',allpairs)
    csv_write(OUT/'spectral_sections_ledger.csv',alltimes)
    csv_write(OUT/'spectral_pair_transport_cross_coupling.csv',allcross)
    csv_write(OUT/'kinetic_similarity_covariance.csv',simrows)
    csv_write(OUT/'original_autonomous_pair_comparison.csv',seedrows)
    csv_write(OUT/'spectral_branch_summary.csv',summaries)
    plots(branches)
    checks={
      'authenticated_v18_51e_source_and_outputs':True,
      'two_authentic_parent_10d_seed_ivps':parent['full_10d_ivps']==2,
      'all_78_positive_sections_have_5_complex_pairs':all(s['sections_nondegenerate']==78 and s['complex_pairs_at_each_positive_section'] for s in summaries),
      'spectral_pair_gap_nonzero':min(s['minimum_pair_separation'] for s in summaries)>args.spectral_gap_floor,
      'riesz_projector_idempotence':max(s['max_projector_idempotence_error'] for s in summaries)<1.e-9,
      'riesz_projector_resolution_of_identity':max(s['max_projector_resolution_error'] for s in summaries)<1.e-9,
      'riesz_projector_disjointness':max(s['max_projector_disjointness_error'] for s in summaries)<1.e-9,
      'riesz_projector_commutation':max(s['max_projector_commutation_error'] for s in summaries)<1.e-9,
      'conjugate_symmetry':max(s['max_conjugate_pair_error'] for s in summaries)<1.e-9,
      'volume_from_five_complex_pairs':max(s['max_determinant_product_error'] for s in summaries)<1.e-9,
      'exact_kinetic_tau_similarity':sim['max_material_similarity_relative_error']<1.e-10,
      'tau_eigenvalue_covariance':sim['max_eigenvalue_similarity_absolute_error']<1.e-9,
      'tau_riesz_projector_covariance':sim['max_riesz_projector_similarity_relative_error']<1.e-8,
      'tau_cauchy_green_consistent_but_not_similar':sim['max_cauchy_green_reconstruction_error']<1.e-10,
      'xi_zero_degeneracy_recorded_not_mislabeled':all(fro(b['M'][0]-EYE)<1.e-10 for b in branches.values()),
      'finite_and_bounded_nonnormality':all(np.isfinite(s['max_pair_condition']) and s['max_pair_condition']<1.e6 for s in summaries)
    }
    report={'version':'v18.51f','title':'Finite-Time Spectral Pairing & Kinetic Similarity Transport Audit',
      'classification':'NUMERICAL_FINITE_TIME_SPECTRAL_PAIRING_AND_SIMILARITY_DIAGNOSTIC_NOT_INTRINSIC_TORSION_OR_MEMORY_CERTIFICATE',
      'kappa_midpoint':parent['kappa_midpoint'],'xi_max':parent['xi_max'],
      'sections_per_seed':79,'spectral_sections_per_seed':78,'metric_conventions':list(TAUS),
      'seed_families':list(SEEDS),'lineage':lineage,
      'fundamental_distinctions':{
        'at_zero':'M(0)=I, tenfold eigenvalue degeneracy: no unique 5+5 decomposition at xi=0',
        'complex_pairs':'Five conjugate pairs for xi>0, not five independent physical rotating materials',
        'projectors':'Real rank-2 Riesz projectors are oblique; not orthogonal spectral energy fractions',
        'metric':'tau_ref changes the state metric and singular stretches but is a constant similarity of M',
        'phase':'arg(lambda)/xi is finite-time modal phase rate, not Floquet frequency',
        'transport':'incremental M_i M_(i-1)^-1 is a cocycle; cross-plane leakage is not transferred physical energy',
        'time_horizon':'short finite time from one common midpoint kappa; no material return or hysteresis certification',
        'one_third':'Not tested further; prior heuristic did not pass metric-convention robustness'},
      'counts':{'branches':len(branches),'positive_time_sections':len(alltimes),'pair_records':len(allpairs),
                'interplane_cocycle_records':len(allcross),'similarity_records':len(simrows),'cross_seed_records':len(seedrows)},
      'similarity':sim,'branches':summaries,
      'original_autonomous_max_eigenvalue_difference':max(r['seed_eigenvalue_abs_difference'] for r in seedrows),
      'original_autonomous_max_phase_difference_rad':max(r['seed_phase_abs_difference_rad'] for r in seedrows),
      'checks':checks,'software':{'python':sys.version.split()[0],'numpy':np.__version__,
                                 'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__,
                                 'platform':platform.platform()}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf8')
    print('CONTROL RESULTS',json.dumps(checks,indent=2),flush=True)
    if not all(checks.values()): raise RuntimeError('Scientific gate FAILED; no sendback to be packed')
    print('v18.51f SCIENTIFIC CONTROLS PASS',len(checks),flush=True)
if __name__=='__main__':main()
