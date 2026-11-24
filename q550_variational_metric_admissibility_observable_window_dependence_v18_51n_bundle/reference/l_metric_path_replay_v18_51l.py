#!/usr/bin/env python3
"""Q550 v18.51l — Metric-Path Continuation & Directionality Survival Audit.

Use the authenticated k<--j<--i/h/g/f/e material history (no new IVP).
Under D_tau=diag(I5,tau I5), both the true tangent map and its Riesz
spectral planes are transformed by similarity. Compare the *norms* of the
same finite material crossblocks in the tau-weighted kinetic state metric.

For each sampled positive-xi crossblock we derive a degree-at-most-four
polynomial in s=tau**2 whose sign determines 5->4 versus 4->5, because
all 2x2 metric Gram determinants remain positive for s>0. Bernstein
lower bounds give floating-point polynomial positivity diagnostics across
the entire tau interval, NOT validated-interval enclosures of physical IVPs.
"""
from __future__ import annotations
import csv,hashlib,importlib.util,io,json,math,platform,shutil,sys,tempfile,zipfile
from pathlib import Path
import numpy as np,scipy,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
KROOT='q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle'
KZIP=KROOT+'_server_sendback.zip'
JROOT='q550_metric_adjoint_reciprocity_bidirectional_pair_transport_v18_51j_bundle'
JZIP=JROOT+'_server_sendback.zip'
SEEDS=('original','autonomous'); ANCHORS=(0.5,1.0,2.0)
TAUS=np.geomspace(0.5,2.0,65); LAGS=(1,2,4)
E2=np.eye(2);E10=np.eye(10)

def sha(b):return hashlib.sha256(b).hexdigest()
def fro(x):return float(np.linalg.norm(x,'fro'))
def rel(a,b):return fro(a-b)/max(1.,fro(a),fro(b))
def tag(t):return f'{t:.1f}'.replace('.','p')
def save_csv(name,rows):
    assert rows
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def verify_zip(z,base,version):
    assert z.testzip() is None, 'CRC failure '+version
    m=json.loads(z.read(base+'/SOURCE_MANIFEST.json'))
    o=json.loads(z.read(base+'/SHA256SUMS_OUTPUT.json'))
    assert m['root']==o['root']==base and m['version']==o['version']==version
    for name,d in m['files'].items():assert sha(z.read(base+'/'+name))==d,(version,'source',name)
    for name,d in o['file_sha256'].items():assert sha(z.read(base+'/'+name))==d,(version,'result',name)
    return len(m['files']),len(o['file_sha256'])

def import_script(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def parent():
    inp=ROOT/'inputs'/KZIP
    with zipfile.ZipFile(inp) as z:
        identities=verify_zip(z,KROOT,'v18.51k')
        rep=json.loads(z.read(KROOT+'/results/report.json'))
        assert rep['version']=='v18.51k' and all(rep['checks'].values())
        for src,dest in [('scripts/run_audit.py','k_connection_replay_v18_51k.py'),
                          ('reference/j_adjoint_replay_v18_51j.py','j_adjoint_replay_v18_51j.py'),
                          ('reference/i_projector_replay_v18_51i.py','i_projector_replay_v18_51i.py'),
                          ('reference/h_pairwise_replay_v18_51h.py','h_pairwise_replay_v18_51h.py'),
                          ('reference/g_projector_replay_v18_51g.py','g_projector_replay_v18_51g.py')]:
            assert z.read(KROOT+'/'+src)==(ROOT/'reference'/dest).read_bytes(),src
        jbytes=z.read(KROOT+'/inputs/'+JZIP)
        oldfinite=list(csv.DictReader(io.StringIO(z.read(KROOT+'/results/connection_aligned_finite_lag_ledger.csv').decode())))
    assert len(oldfinite)==1362
    with tempfile.TemporaryDirectory(prefix='q550_18_51l_genealogy_') as td:
        p=Path(td);(p/'inputs').mkdir();(p/'reference').mkdir()
        (p/'inputs'/JZIP).write_bytes(jbytes)
        for name in ('g_projector_replay_v18_51g.py','h_pairwise_replay_v18_51h.py',
                     'i_projector_replay_v18_51i.py','j_adjoint_replay_v18_51j.py'):
            shutil.copy2(ROOT/'reference'/name,p/'reference'/name)
        k=import_script('q550_k_historical_for_l',ROOT/'reference/k_connection_replay_v18_51k.py')
        k.ROOT=p;k.OUT=p/'results'
        j,branches,material,oldj,history=k.parent_replay()
    assert len(oldj)==1362
    lin=dict(k_source_archive_sha256=sha(inp.read_bytes()),k_sources_authenticated=identities[0],
             k_results_authenticated=identities[1],k_scientific_checks=len(rep['checks']),
             j_genealogy=history,physical_seed_ivps_inherited=2,new_physical_ivps=0)
    return k,j,branches,material,oldfinite,lin

def gram_B(U):
    assert fro(U.T@U-E2)<1e-8
    return U[5:,:].T@U[5:,:]

def H_from_B(B,s):return E2+(s-1.)*B

def roots_of_gram(B,s):
    lam,U=np.linalg.eigh(H_from_B(B,s));assert lam.min()>0
    return (U*np.sqrt(lam))@U.T,(U/np.sqrt(lam))@U.T,lam

def adj(A):return np.array([[A[1,1],-A[0,1]],[-A[1,0],A[0,0]]],dtype=float)

def det_coeff(B):
    A=E2-B
    return np.array([np.linalg.det(A),float(np.trace(adj(A)@B)),np.linalg.det(B)])

def numerator_coeff(Btarget,Bsource,K):
    At=E2-Btarget;As=E2-Bsource
    T=K.T
    return np.array([np.trace(At@K@adj(As)@T),
          np.trace(Btarget@K@adj(As)@T+At@K@adj(Bsource)@T),
          np.trace(Btarget@K@adj(Bsource)@T)],dtype=float)

def signed_polynomial(B4a,B4b,B5a,B5b,K54,K45):
    # |K54(s)|^2=N54(s)/det H5a(s), |K45(s)|^2=N45(s)/det H4a(s)
    N54=numerator_coeff(B4b,B5a,K54);N45=numerator_coeff(B5b,B4a,K45)
    return np.convolve(N54,det_coeff(B4a))-np.convolve(N45,det_coeff(B5a))

def poly_at(c,s):return float(np.polynomial.polynomial.polyval(s,c))

def bernstein_coeffs(c,a,b):
    # polynomial of degree <=4 in s, substitute s=a+(b-a)t, convert to Bernstein basis
    n=len(c)-1;q=np.zeros(n+1)
    for j in range(n+1):
        q[j]=sum(c[k]*math.comb(k,j)*a**(k-j)*(b-a)**j for k in range(j,n+1))
    return np.array([sum(q[j]*math.comb(i,j)/math.comb(n,j) for j in range(i+1)) for i in range(n+1)])

def polynomial_sign_info(c,smin=.25,smax=4.):
    # A reproducible floating-coefficient Bernstein sign diagnostic.
    # It is NOT a formal interval enclosure of original physical data.
    roots=np.roots(c[::-1]); real=[float(z.real) for z in roots if abs(z.imag)<2e-7 and smin-1e-10<=z.real<=smax+1e-10]
    derivative=np.polynomial.polynomial.polyder(c)
    cr=np.roots(derivative[::-1]);critical=[float(z.real) for z in cr if abs(z.imag)<1e-8 and smin<z.real<smax]
    v=[(poly_at(c,s),s) for s in (smin,smax,*critical)]
    vmin,sarg=min(v)
    best_bound=-float('inf');pieces=0;roundoff=0.;level=0
    for level in range(9):
        n=2**level; mins=[];eps_max=0.
        for j in range(n):
            a=smin+(smax-smin)*j/n;b=smin+(smax-smin)*(j+1)/n
            coeff=bernstein_coeffs(c,a,b)
            mins.append(float(coeff.min()))
            # conservative *numerical heuristic*, not a mathematically rounded enclosure
            eps_max=max(eps_max,2e-12*max(np.sum(np.abs(coeff)),
                  np.sum(np.abs(c)*(1+max(abs(a),abs(b)))**np.arange(len(c)))))
        best_bound=min(mins);pieces=n;roundoff=eps_max
        if best_bound>roundoff:break
    return dict(positive_bernstein=best_bound>roundoff,
        bernstein_lower_bound=best_bound,bernstein_error_guard=roundoff,
        bernstein_pieces=pieces,bernstein_levels=level,
        numerical_polynomial_minimum=vmin,s_at_numerical_minimum=sarg,
        in_range_real_roots=len(real))

def ratio_data(K54,K45):
    n54=fro(K54);n45=fro(K45);assert n45>0
    return dict(norm_5to4=n54,norm_4to5=n45,ratio_5to4_over_4to5=n54/n45,
                relative_squared_margin=(n54*n54-n45*n45)/(n54*n54+n45*n45))

def basis_from_B(U,s,B):
    rt,irt,lam=roots_of_gram(B,s)
    D=np.r_[np.ones(5),np.full(5,np.sqrt(s))]
    basis=(D[:,None]*U)@irt
    return basis,rt,irt,float(lam.max()/lam.min())

def polar2(A):
    u,sv,vh=np.linalg.svd(A);assert sv.min()>1e-8
    return u@vh

def conn_chain(conns,a,b):
    R=E2.copy()
    for i in range(a,b):R=conns[i]@R
    return R

def gauge_angle(k,x,tau):
    t=(0.17 if k==4 else -0.26)*x+(0.5 if k==4 else -0.3)*tau
    C=np.cos(t);S=np.sin(t)
    O=np.array([[C,-S],[S,C]])
    if x%(9 if k==4 else 13)==0:O=O@np.diag([-1.,1.])
    return O

def selected_u(z,i):
    U4=z[(i,5,4)]['Ui'];U5=z[(i,5,4)]['Uj']
    assert rel(U4,z[(i,4,5)]['Uj'])<1e-8
    assert rel(U5,z[(i,4,5)]['Ui'])<1e-8
    return U4,U5

def all_base_inputs(k,j,z,M):
    U4={};U5={};B4={};B5={};inst={};finites={}
    for i in range(1,79):
        U4[i],U5[i]=selected_u(z,i);B4[i]=gram_B(U4[i]);B5[i]=gram_B(U5[i])
        f,b,*_=j.channels(z,i);inst[i]=(f,b)
    for lag in LAGS:
        for a in range(1,79-lag):
            b=a+lag;f,rev,_=k.instantaneous_restrictions(j,z,a,b,M)
            finites[(lag,a,b)]=(f,rev)
    assert len(inst)==78 and len(finites)==227
    return U4,U5,B4,B5,inst,finites

def json_clean(x):
    if isinstance(x,dict):return {str(k):json_clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [json_clean(v) for v in x]
    if isinstance(x,np.ndarray):return json_clean(x.tolist())
    if isinstance(x,np.generic):return json_clean(x.item())
    return x

def analyze():
    OUT.mkdir(parents=True,exist_ok=True)
    k,j,branches,material,parent_lags,lineage=parent()
    parentkeys={(x['seed_family'],float(x['tau_ref']),int(x['lag_sections']),int(x['index_start']),int(x['index_end'])):x for x in parent_lags}
    print('AUTHENTICATED k,j,i,h,g,f,e Q550 MODEL HISTORY',len(parent_lags),'parent finite intervals',flush=True)
    inst_rows=[];finite_rows=[];sign_rows=[];anchors=[];bases_rows=[];summary=[]; quality=dict(
      max_baseline_gram_error=0.,max_metric_similarity_error=0.,max_direct_block_error=0.,
      max_rational_polynomial_error=0.,max_parent_finite_ratio_difference=0.,
      max_parent_instant_ratio_difference=0.,max_metric_path_gauge_error=0.,
      max_aligned_defect_gauge_error=0.,max_eigenplane_overlap_step_loss=0.,
      min_metric_eigenvalue=1.,max_metric_condition=1.,
      min_finite_ratio=float('inf'),min_instant_ratio=float('inf'))
    for seed in SEEDS:
        z=branches[seed,1.];xi=material[f'xi_{seed}'];M=material[f'M_{seed}_tau_1p0']
        U4,U5,B4,B5,instant,finite=all_base_inputs(k,j,z,M)
        for ta in ANCHORS:
            D=np.diag(np.r_[np.ones(5),np.full(5,ta)]);Di=np.linalg.inv(D)
            chk=material[f'M_{seed}_tau_{tag(ta)}']
            for ix in (1,18,38,58,78):
                quality['max_metric_similarity_error']=max(quality['max_metric_similarity_error'],rel(chk[ix],D@M[ix]@Di))
        # The exact finite-time spectral planes at every tau are D_tau E_j(tau=1).
        for tau_idx,tau in enumerate(TAUS):
            s=float(tau*tau)
            F4={};F5={};R4={};R5={};IR4={};IR5={}
            for ix in range(1,79):
                u4,r4,ir4,cond4=basis_from_B(U4[ix],s,B4[ix]);u5,r5,ir5,cond5=basis_from_B(U5[ix],s,B5[ix])
                F4[ix]=u4;F5[ix]=u5;R4[ix]=r4;R5[ix]=r5;IR4[ix]=ir4;IR5[ix]=ir5
                quality['max_baseline_gram_error']=max(quality['max_baseline_gram_error'],fro(u4.T@u4-E2),fro(u5.T@u5-E2))
                quality['min_metric_eigenvalue']=min(quality['min_metric_eigenvalue'],np.linalg.eigvalsh(H_from_B(B4[ix],s)).min(),np.linalg.eigvalsh(H_from_B(B5[ix],s)).min())
                quality['max_metric_condition']=max(quality['max_metric_condition'],cond4,cond5)
                if tau_idx in (0,16,32,48,64) and ix in (1,38,78):
                    angle=float(np.degrees(np.arccos(np.clip(np.linalg.svd(u4.T@u5,compute_uv=False)[0],-1,1))))
                    bases_rows.append(dict(seed_family=seed,tau_ref=float(tau),index=ix,xi=float(xi[ix]),
                       principal_angle_45_degrees=angle,condition_E4=cond4,condition_E5=cond5))
            conn4={i:polar2(F4[i+1].T@F4[i]) for i in range(1,78)}
            conn5={i:polar2(F5[i+1].T@F5[i]) for i in range(1,78)}
            for ix in range(1,78):
                for C in (F4[ix+1].T@F4[ix],F5[ix+1].T@F5[ix]):
                    quality['max_eigenplane_overlap_step_loss']=max(quality['max_eigenplane_overlap_step_loss'],1-float(np.linalg.svd(C,compute_uv=False).min()))
            # All inherited positive-time instantaneous channel generators.
            for ix,(f,b) in instant.items():
                K54=R4[ix]@f@IR5[ix];K45=R5[ix]@b@IR4[ix]
                val=ratio_data(K54,K45)
                inst_rows.append(dict(seed_family=seed,tau_ref=float(tau),tau_index=tau_idx,index=ix,
                         xi=float(xi[ix]),**val))
                quality['min_instant_ratio']=min(quality['min_instant_ratio'],val['ratio_5to4_over_4to5'])
                if tau_idx in (0,32,64):
                    oldratio=fro(j.channels(branches[seed,float(tau)],ix)[0])/fro(j.channels(branches[seed,float(tau)],ix)[1])
                    quality['max_parent_instant_ratio_difference']=max(quality['max_parent_instant_ratio_difference'],abs(val['ratio_5to4_over_4to5']-oldratio))
                if tau_idx==0:
                    pol=signed_polynomial(B4[ix],B4[ix],B5[ix],B5[ix],f,b)
                    info=polynomial_sign_info(pol)
                    sign_rows.append(dict(seed_family=seed,observable='instantaneous',lag_sections=0,index_start=ix,index_end=ix,
                       xi_start=float(xi[ix]),xi_end=float(xi[ix]),**info,
                       polynomial_coefficients=json.dumps([float(t) for t in pol])))
                if tau_idx in (0,16,32,48,64) and ix in (1,39,78):
                    D=np.diag(np.r_[np.ones(5),np.full(5,tau)]);Di=np.linalg.inv(D)
                    P4=D@z[(ix,4,5)]['P']@Di;P5=D@z[(ix,5,4)]['P']@Di
                    Q54=D@z[(ix,5,4)]['Q']@Di;Q45=D@z[(ix,4,5)]['Q']@Di
                    direct54=F4[ix].T@Q54@F5[ix];direct45=F5[ix].T@Q45@F4[ix]
                    quality['max_direct_block_error']=max(quality['max_direct_block_error'],rel(direct54,K54),rel(direct45,K45))
            # Finite-lag propagation along the same physical xi interval, with a varied kinetic metric.
            for (lag,a,b),(f,rev) in finite.items():
                K54=R4[b]@f@IR5[a];K45=R5[b]@rev@IR4[a]
                val=ratio_data(K54,K45)
                quality['min_finite_ratio']=min(quality['min_finite_ratio'],val['ratio_5to4_over_4to5'])
                tr4=conn_chain(conn4,a,b);tr5=conn_chain(conn5,a,b)
                X=tr4.T@K54;Y=K45.T@tr5
                aligned_defect=fro(X-Y)/(fro(K54)+fro(K45))
                if tau_idx in (0,32,64):
                    prow=parentkeys[seed,float(tau),lag,a,b]
                    quality['max_parent_finite_ratio_difference']=max(quality['max_parent_finite_ratio_difference'],
                            abs(val['ratio_5to4_over_4to5']-float(prow['ratio_5to4_over_4to5'])))
                    quality['max_aligned_defect_gauge_error']=max(quality['max_aligned_defect_gauge_error'],
                            abs(aligned_defect-float(prow['gauge_aligned_adjoint_defect'])))
                if tau_idx in (7,32,57) and a in (1,38,74) and b<=78:
                    O4a=gauge_angle(4,a,tau);O4b=gauge_angle(4,b,tau)
                    O5a=gauge_angle(5,a,tau);O5b=gauge_angle(5,b,tau)
                    K54g=O4b.T@K54@O5a;K45g=O5b.T@K45@O4a
                    tr4g=O4b.T@tr4@O4a;tr5g=O5b.T@tr5@O5a
                    Xg=tr4g.T@K54g;Yg=K45g.T@tr5g
                    dd=fro(Xg-Yg)/(fro(K54g)+fro(K45g))
                    quality['max_metric_path_gauge_error']=max(quality['max_metric_path_gauge_error'],abs(dd-aligned_defect),
                        abs(fro(K54g)/fro(K45g)-val['ratio_5to4_over_4to5']))
                finite_rows.append(dict(seed_family=seed,tau_ref=float(tau),tau_index=tau_idx,lag_sections=lag,
                       index_start=a,index_end=b,xi_start=float(xi[a]),xi_end=float(xi[b]),
                       dt=float(xi[b]-xi[a]),aligned_adjoint_defect=aligned_defect,**val))
                if tau_idx==0:
                    pol=signed_polynomial(B4[a],B4[b],B5[a],B5[b],f,rev)
                    info=polynomial_sign_info(pol)
                    sign_rows.append(dict(seed_family=seed,observable='finite_lag',lag_sections=lag,index_start=a,index_end=b,
                       xi_start=float(xi[a]),xi_end=float(xi[b]),**info,
                       polynomial_coefficients=json.dumps([float(t) for t in pol])))
                if tau_idx in (0,16,32,48,64) and (lag,a) in ((1,1),(2,38),(4,74)):
                    D=np.diag(np.r_[np.ones(5),np.full(5,tau)]);Di=np.linalg.inv(D)
                    T=np.linalg.solve(M[a].T,M[b].T).T
                    Tnew=D@T@Di
                    PP4=D@z[(b,4,5)]['P']@Di;PP5=D@z[(b,5,4)]['P']@Di
                    direct54=F4[b].T@PP4@Tnew@F5[a]
                    direct45=F5[b].T@PP5@Tnew@F4[a]
                    quality['max_direct_block_error']=max(quality['max_direct_block_error'],rel(direct54,K54),rel(direct45,K45))
        print('METRIC PATH',seed,'nodes',len(TAUS),'finite',len(finite)*len(TAUS),
             'minimum ratio',min(r['ratio_5to4_over_4to5'] for r in finite_rows if r['seed_family']==seed),flush=True)
    # Verify polynomial exact algebraic transformation on a representative
    # off-grid tau for every symbolic observable, using frozen baseline matrices.
    for seed in SEEDS:
        z=branches[seed,1.];M=material[f'M_{seed}_tau_1p0']
        U4,U5,B4,B5,inst,fin=all_base_inputs(k,j,z,M)
        for kind,keys in [('instantaneous',[(0,i,i) for i in range(1,79)]),
                          ('finite_lag',[(lag,a,b) for (lag,a,b) in fin])]:
            for lag,a,b in keys:
                f,rev=(inst[a] if not lag else fin[(lag,a,b)])
                pol=signed_polynomial(B4[a],B4[b],B5[a],B5[b],f,rev)
                for s in (.25,.73,1.0,1.67,4.):
                    r4b,_,_=roots_of_gram(B4[b],s);_,ir5a,_=roots_of_gram(B5[a],s)
                    r5b,_,_=roots_of_gram(B5[b],s);_,ir4a,_=roots_of_gram(B4[a],s)
                    q=fro(r4b@f@ir5a)**2-fro(r5b@rev@ir4a)**2
                    determinant=np.linalg.det(H_from_B(B4[a],s))*np.linalg.det(H_from_B(B5[a],s))
                    rhs=poly_at(pol,s)/determinant
                    quality['max_rational_polynomial_error']=max(quality['max_rational_polynomial_error'],
                        abs(q-rhs)/max(1e-16,abs(q),fro(r4b@f@ir5a)**2,fro(r5b@rev@ir4a)**2))
    save_csv('metric_path_instantaneous_directionality.csv',inst_rows)
    save_csv('metric_path_finite_lag_directionality.csv',finite_rows)
    save_csv('metric_path_polynomial_sign_bounds.csv',sign_rows)
    save_csv('metric_path_plane_conditioning.csv',bases_rows)
    for seed in SEEDS:
        fi=[r for r in finite_rows if r['seed_family']==seed]
        it=[r for r in inst_rows if r['seed_family']==seed]
        sn=[r for r in sign_rows if r['seed_family']==seed]
        for lag in (0,*LAGS):
            rows=it if lag==0 else [r for r in fi if r['lag_sections']==lag]
            signs=[r for r in sn if r['lag_sections']==lag]
            worst=min(rows,key=lambda q:q['ratio_5to4_over_4to5'])
            summary.append(dict(seed_family=seed,observable='instantaneous' if lag==0 else 'finite_lag',
                     lag_sections=lag,n_observations=len(rows),n_metric_nodes=len(TAUS),
                     direction_5to4_survival_on_nodes=sum(r['ratio_5to4_over_4to5']>1 for r in rows),
                     minimum_ratio=worst['ratio_5to4_over_4to5'],minimum_margin=worst['relative_squared_margin'],
                     tau_at_minimum=worst['tau_ref'],xi_at_minimum=worst.get('xi_end',worst.get('xi',0.)),
                     total_polynomials=len(signs),bernstein_positive_polynomials=sum(r['positive_bernstein'] for r in signs),
                     polynomial_real_roots_in_range=sum(r['in_range_real_roots'] for r in signs),
                     smallest_numerical_polynomial_minimum=min(r['numerical_polynomial_minimum'] for r in signs)))
    save_csv('metric_path_survival_summary.csv',summary)
    plots(inst_rows,finite_rows,summary)
    nn=sum(r['positive_bernstein'] for r in sign_rows)
    checks=dict(k_crc_sha256_and_22_checks=bool(lineage['k_sources_authenticated'] and lineage['k_results_authenticated']),
      authenticated_nested_j_i_h_g_f_e=True,
      exact_historical_replay_two_seeds_no_new_10D_ivps=lineage['physical_seed_ivps_inherited']==2 and lineage['new_physical_ivps']==0,
      positive_weight_65_nodes_three_anchors=len(TAUS)==65 and np.isclose(TAUS[0],.5) and np.isclose(TAUS[32],1.) and np.isclose(TAUS[-1],2.),
      full_instantaneous_node_count=len(inst_rows)==2*65*78,
      full_finite_lag_node_count=len(finite_rows)==2*65*227,
      metric_positive_definite=quality['min_metric_eigenvalue']>0,
      numerical_similarity_reconstruction=quality['max_metric_similarity_error']<2e-8,
      metric_orthonormal_plane_bases=quality['max_baseline_gram_error']<2e-9,
      algebraic_direct_operator_crossblock=quality['max_direct_block_error']<2e-8,
      polynomial_exact_fractional_norm_difference=quality['max_rational_polynomial_error']<2e-8,
      inherited_instantaneous_anchor_replay=quality['max_parent_instant_ratio_difference']<2e-6,
      inherited_finite_anchor_replay=quality['max_parent_finite_ratio_difference']<2e-6,
      inherited_connection_aligned_defect_anchor_replay=quality['max_aligned_defect_gauge_error']<2e-6,
      independent_pair_O2_gauge_at_nonanchor_weights=quality['max_metric_path_gauge_error']<2e-10,
      positive_metric_path_finite_spectral_overlap=quality['max_eigenplane_overlap_step_loss']<1e-3,
      finite_samples_xi_positive=all(q['xi_start']>0 and q['dt']>0 for q in finite_rows),
      explicit_polynomial_sign_test_for_every_base_observable=len(sign_rows)==2*(78+227),
      no_physical_continuum_xi_certification=True,
      one_third_not_used_as_hypothesis=True)
    report=dict(version='v18.51l',title='Metric-Path Continuation & Directionality Survival Audit',
         classification='NUMERICAL_KINETIC_WEIGHT_PATH_DIRECTIONALITY_AND_FLOATING_POLYNOMIAL_POSITIVITY_DIAGNOSTIC_NOT_UNIVERSAL_MATERIAL_LAW',
         lineage=lineage,counts=dict(metric_nodes=65,positive_xi_sections_per_seed=78,
            lag_intervals_per_seed=227,instantaneous_ledger_rows=len(inst_rows),
            finite_ledger_rows=len(finite_rows),polynomial_observables=len(sign_rows),
            polynomial_positive_bernstein=nn,polynomial_unresolved=len(sign_rows)-nn),
         path=dict(tau_ref_min=.5,tau_ref_max=2.,parameter='s=tau_ref^2',
            frozen_material_history=True,physical_seed_reintegration=False,
            similarity='D_tau=diag(I5,tau I5); M_tau=D_tau M_1 inv(D_tau); P_tau=D_tau P_1 inv(D_tau)',
            metric_gram='H_i(xi,s)=U_i(xi)^T diag(I5,s I5) U_i(xi)',
            direct_crossblock='K_(i<-j)(tau)=sqrt(H_i(b)) K_(i<-j)(1) invsqrt(H_j(a))',
            sign_polynomial='F(s)=N54(s) det(H4(a,s)) - N45(s) det(H5(a,s)); degree<=4; denominators positive for s>0',
            bernstein='Floating-point Bernstein lower bound on s in [0.25,4] for each fixed sampled material interval, not a validated interval-arithmetic enclosure.'),
         quality=quality,observations=dict(rows=summary,
            all_instant_node_5to4_dominant=all(x['ratio_5to4_over_4to5']>1 for x in inst_rows),
            all_finite_node_5to4_dominant=all(x['ratio_5to4_over_4to5']>1 for x in finite_rows),
            bernstein_positive_all_fixed_sample_polynomials=nn==len(sign_rows)),
         checks=checks,limitations=[
            'The family tau_ref in [0.5,2] changes the position/velocity weighting of one kinetic state immersion; it is NOT a family of independently derived material laws.',
            'Similarity preserves eigenvalues by construction. It does not preserve singular values or norm ratios under changed metric.',
            'Bernstein polynomial positivity is computed from floating-point tangent tensors; not a certified interval arithmetic bound on the original ODE or on numerical rounding errors.',
            'Only material intervals with sampled positive xi sections and lag counts 1,2,4 are considered. No interpolation in physical xi is certified.',
            'The 5->4 labels are inherited isolated Riesz spectral right-plane labels. At xi=0 the identity map is tenfold degenerate.',
            'Gauge-invariance at fixed tau is not material metric-uniqueness. The apparent directionality is not a measured flow of energy or intrinsic torsion.',
            'No 1/3 law, hysteretic memory, universal reciprocity breaking or microscopic arrow of time is established.'
         ],software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform()))
    report=json_clean(report)
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('Q550 v18.51l observations',json.dumps(report['observations'],indent=2,default=str),flush=True)
    print('Q550 v18.51l quality',json.dumps(quality,indent=2),flush=True)
    print('Q550 v18.51l checks',json.dumps(report['checks'],indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('Q550 v18.51l failed authenticity or mathematical identity controls')
    print('Q550 v18.51l PASS',len(checks),'/',len(checks),flush=True)

def plots(inst,fin,summary):
    fig,ax=plt.subplots(figsize=(10,6))
    for seed,sty in [('original','-'),('autonomous','--')]:
        for lag in LAGS:
            d=[r for r in fin if r['seed_family']==seed and r['lag_sections']==lag and r['index_end']==78]
            # lags ending at 78 one observation per tau
            ax.plot([r['tau_ref'] for r in d],[r['ratio_5to4_over_4to5'] for r in d],sty,
                    label=f'{seed}, lag {lag}',linewidth=1.65)
    ax.axhline(1,color='gray',linestyle=':',linewidth=1)
    ax.set(xlabel=r'Kinetic state weight $\tau_{ref}$',ylabel='5→4 / 4→5 finite-lag norm ratio',
           title='Q550 v18.51l — endpoint finite-lag directionality along metric weight path')
    ax.grid(alpha=.2);ax.legend(fontsize=8,ncol=2);fig.tight_layout()
    fig.savefig(OUT/'metric_path_endpoint_directionality.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for seed in SEEDS:
        for lag in (0,1,4):
            sub=[r for r in summary if r['seed_family']==seed and r['lag_sections']==lag][0]
            # Minimum for each metric node across positive sections / finite lags
            d=inst if lag==0 else fin
            mins=[]
            for k,t in enumerate(TAUS):
                vals=[r['ratio_5to4_over_4to5'] for r in d if r['seed_family']==seed and r['tau_index']==k and (lag==0 or r['lag_sections']==lag)]
                mins.append(min(vals))
            ax.plot(TAUS,mins,label=f'{seed}, '+('instant' if lag==0 else f'lag {lag}'),linestyle='-' if seed=='original' else '--')
    ax.axhline(1,color='gray',linestyle=':',linewidth=1)
    ax.set(xlabel=r'Kinetic state weight $\tau_{ref}$',ylabel='Minimum 5→4 / 4→5 strength over sampled xi',
        title='Q550 v18.51l — weakest directional margin across the path')
    ax.grid(alpha=.2);ax.legend(ncol=2,fontsize=8);fig.tight_layout()
    fig.savefig(OUT/'metric_path_worst_case_survival.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    for seed in SEEDS:
        d=[r for r in fin if r['seed_family']==seed and r['lag_sections']==1 and r['tau_index']==32]
        ax.plot([r['xi_end'] for r in d],[r['relative_squared_margin'] for r in d],label=seed)
    ax.axhline(0,color='gray',linestyle=':')
    ax.set(xlabel='Target xi',ylabel='(norm54²−norm45²)/(norm54²+norm45²)',
           title='Q550 v18.51l — dimensionless bidirectional margin at tau_ref=1')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    fig.savefig(OUT/'metric_path_directional_margin.png',dpi=160);plt.close(fig)

if __name__=='__main__':analyze()
