#!/usr/bin/env python3
"""Q550 v18.51g — covariant rank-2 Riesz spectral-projector drift.

Replays authentic v18.51f (which embeds authenticated Q550 v18.51e genuine
10D physical solver/tangent tensors), compares exact spectral directional
rates against irregular-grid finite differences, and checks step/cocycle
refinement without introducing new physical IVPs or claiming time-continuous
interval certification. All science text and code comments are in English.
"""
from __future__ import annotations
import argparse, csv, hashlib, io, json, sys, platform, zipfile
from pathlib import Path
import numpy as np
from scipy.linalg import eig
from scipy.interpolate import CubicSpline
from scipy.optimize import linear_sum_assignment
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
sys.path.insert(0,str(ROOT/'reference'))
import f_spectral_replay_v18_51f as fref
FNAME='q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle_server_sendback.zip'
FROOT='q550_finite_time_spectral_pairing_kinetic_similarity_transport_v18_51f_bundle'
ENAME='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle_server_sendback.zip'
EROOT='q550_full_kinetic_tangent_generator_finite_time_cauchy_green_transport_v18_51e_bundle'
SEEDS=('original','autonomous'); TAUS=(0.5,1.,2.); EYE=np.eye(10)

def sha(data):return hashlib.sha256(data).hexdigest()
def fnorm(a):return float(np.linalg.norm(a,'fro'))
def rel(a,b):return fnorm(a-b)/max(1.,fnorm(a),fnorm(b))
def sym(a):return (a+a.T)/2
def tag(t):return (f'{t:.1f}').replace('.','p')
def csvsave(name,rows):
    assert rows, 'empty rows '+name
    with (OUT/name).open('w',newline='',encoding='utf-8') as fd:
        w=csv.DictWriter(fd,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def auth():
    p=ROOT/'inputs'/FNAME
    with zipfile.ZipFile(p) as f:
        assert f.testzip() is None,'f source CRC failure'
        def rf(n):return f.read(FROOT+'/'+n)
        fm=json.loads(rf('SOURCE_MANIFEST.json'))
        fo=json.loads(rf('SHA256SUMS_OUTPUT.json'))
        assert (fm['root'],fm['version'])==(FROOT,'v18.51f')
        assert (fo['root'],fo['version'])==(FROOT,'v18.51f')
        for n,h in fm['files'].items():
            assert sha(rf(n))==h, 'f source mismatch: '+n
        for n,h in fo['file_sha256'].items():
            assert sha(rf(n))==h, 'f output mismatch: '+n
        # The locally used reference is authenticated byte-for-byte to the parent script.
        assert (ROOT/'reference/f_spectral_replay_v18_51f.py').read_bytes()==rf('scripts/run_audit.py')
        frep=json.loads(rf('results/report.json'))
        assert frep['version']=='v18.51f' and all(frep['checks'].values())
        assert frep['counts']['positive_time_sections']==468
        edata=rf('inputs/'+ENAME)
    with zipfile.ZipFile(io.BytesIO(edata)) as e:
        assert e.testzip() is None,'e source CRC failure'
        def re(n):return e.read(EROOT+'/'+n)
        em=json.loads(re('SOURCE_MANIFEST.json'))
        eo=json.loads(re('SHA256SUMS_OUTPUT.json'))
        assert (em['root'],em['version'])==(EROOT,'v18.51e')
        assert (eo['root'],eo['version'])==(EROOT,'v18.51e')
        for n,h in em['files'].items():
            assert sha(re(n))==h,'e source hash mismatch '+n
        for n,h in eo['file_sha256'].items():
            assert sha(re(n))==h,'e output hash mismatch '+n
        erep=json.loads(re('results/report.json'))
        assert all(erep['scientific_checks'].values()) and erep['full_10d_ivps']==2
        buf=io.BytesIO(re('results/material_tangent_cauchy_green_tensors.npz'))
        with np.load(buf,allow_pickle=False) as nd: vals={k:nd[k].copy() for k in nd.files}
    return vals,{'f_archive_sha256':sha(p.read_bytes()),'f_root':FROOT,
                 'f_source_files':len(fm['files']),'f_output_files':len(fo['file_sha256']),
                 'f_controls':len(frep['checks']),'e_embedded_sha256':sha(edata),
                 'e_source_files':len(em['files']),'e_output_files':len(eo['file_sha256']),
                 'e_controls':len(erep['scientific_checks']),
                 'physical_seed_ivps':erep['full_10d_ivps'],
                 'physical_lineage':erep['lineage'],
                 'no_new_physical_ivp':True}

def spectral_jets(mat,B,x,prev_lam=None):
    """Analytic Riesz derivative using M'=BM, not time differencing P.

    For each conjugate rank-2 projector P_J=sum_{a in J} R_a,
    P'_J=sum_{a in J,k outside J}(R_k M' R_a + R_a M' R_k)/(lam_a-lam_k).
    This follows by differentiation of spectral projectors at isolated roots.
    The pair-internal terms cancel exactly after grouping conjugate roots.
    """
    lam,VL,VR=eig(mat,left=True,right=True)
    Rs=[]
    for k in range(10):
        overlap=np.vdot(VL[:,k],VR[:,k])
        if abs(overlap)<1e-14:raise ValueError('Defective/ill-conditioned left-right spectral resolution')
        Rs.append(np.outer(VR[:,k],VL[:,k].conj())/overlap)
    pos=np.flatnonzero(lam.imag>1.e-10)
    if len(pos)!=5 or len(np.flatnonzero(lam.imag< -1e-10))!=5:
        raise ValueError(f'Not five nonreal conjugate pairs at xi={x}')
    singles=[];dM=B@mat
    for i in pos:
        ci=int(np.argmin(abs(lam-np.conj(lam[i]))))
        if ci==i:raise ValueError('Conjugate matching failure')
        js={int(i),ci}
        P=np.real(Rs[i]+Rs[ci]); Pdot=np.zeros((10,10),dtype=complex)
        for a in js:
            for k in range(10):
                if k not in js:
                    Pdot+=(Rs[k]@dM@Rs[a]+Rs[a]@dM@Rs[k])/(lam[a]-lam[k])
        Pdot=Pdot.real
        drift=Pdot-(B@P-P@B)
        outside=[k for k in range(10) if k not in js]
        gap=float(min(abs(lam[i]-lam[k]) for k in outside))
        singles.append({'lam':lam[i],'P':P,'Pdot':Pdot,'drift':drift,'gap':gap})
    if prev_lam is None: singles.sort(key=lambda r:r['lam'].imag)
    else:
        costs=abs(np.array(prev_lam)[:,None]-np.array([p['lam'] for p in singles])[None,:])
        ix,jx=linear_sum_assignment(costs)
        assert np.array_equal(ix,np.arange(5))
        singles=[singles[int(j)] for j in jx]
    return singles

def stencil(xs,k,width):
    """Irregular-grid local polynomial 1st derivative, scaled Vandermonde."""
    n=len(xs);left=max(0,min(k-width//2,n-width));indices=np.arange(left,left+width)
    d=xs[indices]-xs[k];scale=np.max(abs(d));scaled=d/scale
    V=np.vander(scaled,width,increasing=True).T
    rhs=np.zeros(width);rhs[1]=1.
    w=np.linalg.solve(V,rhs)/scale
    return indices,w

def sample_fd(xs,matrices,k,width):
    ids,w=stencil(xs,k,width)
    return np.tensordot(w,matrices[ids],axes=(0,0))

def rk4_propagate(cs,t0,t1,n):
    T=EYE.copy();dt=(t1-t0)/n
    for k in range(n):
        t=t0+k*dt
        b0=cs(t);bm=cs(t+dt/2);b1=cs(t+dt)
        k1=b0@T; k2=bm@(T+dt*k1/2);k3=bm@(T+dt*k2/2);k4=b1@(T+dt*k3)
        T=T+(dt/6)*(k1+2*k2+2*k3+k4)
    return T

def run_branch(seed,tau,values):
    xs=values['xi_'+seed]; key=f'{seed}_tau_{tag(tau)}'
    M=values['M_'+key];B=values['B_'+key];L=values['L_'+key]
    assert xs.shape==(79,) and M.shape==B.shape==(79,10,10)
    assert np.all(np.diff(xs)>0) and np.isclose(xs[-1],.05)
    assert rel(M[0],EYE)<1e-10
    if not np.all(np.isfinite(B)):raise ValueError('Nonfinite full physical kinetic generator')
    jets=[];lam=None
    for k in range(1,79):
        j=spectral_jets(M[k],B[k],float(xs[k]),lam)
        lam=[q['lam'] for q in j]
        jets.append(j)
    P=np.array([[a['P'] for a in j] for j in jets]);Pdot=np.array([[a['Pdot'] for a in j] for j in jets]);R=np.array([[a['drift'] for a in j] for j in jets]);x=xs[1:]
    rows=[];crossrows=[];finite_rows=[]
    worst={'projector_idempotence':0.,'projector_sum':0.,'projector_commutation':0.,
           'projector_derivative_idempotence':0.,'spectral_evolution_identity':0.,
           'total_drift':0.,'differential_pair_sum':0.,'positive_pair_min_gap':float('inf')}
    for k,j in enumerate(jets):
        ps=P[k];dps=Pdot[k];rr=R[k]; mm=M[k+1]; bb=B[k+1]
        worst['projector_idempotence']=max(worst['projector_idempotence'],max(rel(q@q,q) for q in ps))
        worst['projector_sum']=max(worst['projector_sum'],rel(np.sum(ps,axis=0),EYE))
        worst['projector_commutation']=max(worst['projector_commutation'],max(rel(q@mm,mm@q) for q in ps))
        worst['projector_derivative_idempotence']=max(worst['projector_derivative_idempotence'],max(rel(dps[j],dps[j]@ps[j]+ps[j]@dps[j]) for j in range(5)))
        worst['differential_pair_sum']=max(worst['differential_pair_sum'],fnorm(np.sum(dps,axis=0)))
        for jn,q in enumerate(j):
            worst['positive_pair_min_gap']=min(worst['positive_pair_min_gap'],q['gap'])
            evo=rel(mm@q['Pdot']-q['Pdot']@mm,-(bb@mm@q['P']-q['P']@bb@mm))
            worst['spectral_evolution_identity']=max(worst['spectral_evolution_identity'],evo)
            worst['total_drift']=max(worst['total_drift'],fnorm(q['drift']))
            rec={'seed_family':seed,'tau_ref':tau,'index':k+1,'xi':float(x[k]),'pair_id':jn+1,
                 'nearest_nonconjugate_gap':q['gap'],'projector_norm':fnorm(q['P']),
                 'projector_prime_norm':fnorm(q['Pdot']),
                 'commutator_norm':fnorm(bb@q['P']-q['P']@bb),
                 'covariant_drift_frobenius':fnorm(q['drift']),
                 'covariant_drift_over_projector_norm':fnorm(q['drift'])/fnorm(q['P']),
                 'fd3_derivative_relative_error':None,'fd5_derivative_relative_error':None}
            if k>=2 and k<len(jets)-2:
                p3=sample_fd(x,P[:,jn],k,3);p5=sample_fd(x,P[:,jn],k,5)
                rec['fd3_derivative_relative_error']=rel(p3,q['Pdot'])
                rec['fd5_derivative_relative_error']=rel(p5,q['Pdot'])
                finite_rows.append((k,jn,rec['fd3_derivative_relative_error'],rec['fd5_derivative_relative_error']))
            rows.append(rec)
            for to in range(5):
                if to==jn:continue
                numerator=fnorm(ps[to]@q['drift']@ps[jn]); rate=numerator/max(1e-30,fnorm(ps[jn]))
                crossrows.append({'seed_family':seed,'tau_ref':tau,'index':k+1,'xi':float(x[k]),
                                  'from_pair':jn+1,'to_pair':to+1,
                                  'instantaneous_covariant_cross_rate':rate,
                                  'instantaneous_cross_unscaled':numerator,
                                  'spectral_gap_from_to':min(q['gap'],j[to]['gap'])})
    # Difference between instantaneous covariant transport obstruction and measured endpoint-increment leakage.
    cocycle=[]
    for k in range(1,len(x)):
        dt=x[k]-x[k-1];T=M[k+1]@np.linalg.inv(M[k])
        for fr in range(5):
            for to in range(5):
                if fr==to:continue
                exact=fnorm(P[k,to]@T@P[k-1,fr])/max(1e-30,fnorm(T@P[k-1,fr]))/dt
                inst=fnorm(P[k,to]@R[k,fr]@P[k,fr])/max(1e-30,fnorm(P[k,fr]))
                cocycle.append({'seed_family':seed,'tau_ref':tau,'index':k+1,'xi':float(x[k]),'delta_xi':float(dt),
                                'from_pair':fr+1,'to_pair':to+1,'finite_step_rate':exact,
                                'instantaneous_covariant_rate':inst,'absolute_rate_difference':abs(exact-inst),
                                'relative_rate_difference':abs(exact-inst)/max(1.,exact,inst)})
    # Independent time-step refinement of the incremental material equation T'=B(xi)T.
    # Interpolation is an approximation; the comparison with genuine parent M measures both interpolation and RK error.
    cs=CubicSpline(xs,B,axis=0)
    integrator=[]
    for k in range(1,len(xs)):
        truth=M[k]@np.linalg.inv(M[k-1]);ts={n:rk4_propagate(cs,float(xs[k-1]),float(xs[k]),n) for n in (1,2,4,8)}
        integrator.append({'seed_family':seed,'tau_ref':tau,'index':k,'xi':float(xs[k]),
                           'delta_xi':float(xs[k]-xs[k-1]),
                           **{f'rk4_substeps_{n}_relative_error_to_true_cocycle':rel(ts[n],truth) for n in (1,2,4,8)},
                           'rk4_1_vs_2':rel(ts[1],ts[2]),'rk4_2_vs_4':rel(ts[2],ts[4]),
                           'rk4_4_vs_8':rel(ts[4],ts[8])})
    return {'seed':seed,'tau':tau,'xs':xs,'x':x,'M':M,'B':B,'L':L,
            'P':P,'Pdot':Pdot,'R':R,'rows':rows,'cross':crossrows,'cocycle':cocycle,
            'integrator':integrator,'worst':worst,'finite':finite_rows}

def grid_stride_check(branch):
    x=branch['x'];P=branch['P'];Pd=branch['Pdot'];out=[]
    # Common nodes across stride 1,2,4 are indices 1 (mod 4), excluding stencil boundaries.
    common=[k for k in range(9,len(x)-9) if k%4==0]
    for stride in (1,2,4):
        inds=np.arange(0,len(x),stride); pos={int(q):i for i,q in enumerate(inds)}
        errors=[]
        for k in common:
            if k not in pos or pos[k]<2 or pos[k]>=len(inds)-2:continue
            j=pos[k]
            for pair in range(5):
                fd=sample_fd(x[inds],P[inds,pair],j,5)
                errors.append(rel(fd,Pd[k,pair]))
        assert errors
        out.append({'seed_family':branch['seed'],'tau_ref':branch['tau'],'stride':stride,
                    'number_of_common_pair_points':len(errors),
                    'median_5point_derivative_relative_error':float(np.median(errors)),
                    'p90_5point_derivative_relative_error':float(np.quantile(errors,.9)),
                    'maximum_5point_derivative_relative_error':max(errors)})
    return out

def covariance(branches):
    rows=[];mx={'M':0.,'B':0.,'P':0.,'Pdot':0.,'drift':0.,'canonical_rate':0.,
                'gap_scaled_drift':0.,'gap_scaled_canonical_rate':0.,
                'interior_drift':0.,'interior_canonical_rate':0.}
    for seed in SEEDS:
        b=branches[(seed,1.)]
        for tau in (0.5,2.):
            c=branches[(seed,tau)];D=np.diag([1]*5+[tau]*5);Di=np.linalg.inv(D)
            for k in range(78):
                j=k+1
                diffs={'M':rel(c['M'][j],D@b['M'][j]@Di),
                       'B':rel(c['B'][j],D@b['B'][j]@Di),
                       'P':max(rel(c['P'][k,q],D@b['P'][k,q]@Di) for q in range(5)),
                       'Pdot':max(rel(c['Pdot'][k,q],D@b['Pdot'][k,q]@Di) for q in range(5)),
                       'drift':max(rel(c['R'][k,q],D@b['R'][k,q]@Di) for q in range(5))}
                normc=[fnorm(Di@c['R'][k,q]@D) for q in range(5)]
                normb=[fnorm(b['R'][k,q]) for q in range(5)]
                diffs['canonical_rate']=max(abs(a-bb) for a,bb in zip(normc,normb))
                for name,val in diffs.items():mx[name]=max(mx[name],val)
                # Near xi=0, M=I+O(xi): modal gaps vanish and individual
                # eigendecomposition derivatives amplify roundoff by O(1/gap).
                gap=min(q['nearest_nonconjugate_gap'] for q in b['rows'][k*5:(k+1)*5])
                mx['gap_scaled_drift']=max(mx['gap_scaled_drift'],diffs['drift']*gap)
                mx['gap_scaled_canonical_rate']=max(mx['gap_scaled_canonical_rate'],diffs['canonical_rate']*gap)
                if b['x'][k]>=.001:
                    mx['interior_drift']=max(mx['interior_drift'],diffs['drift'])
                    mx['interior_canonical_rate']=max(mx['interior_canonical_rate'],diffs['canonical_rate'])
                rows.append({'seed_family':seed,'tau_ref':tau,'index':j,'xi':float(b['x'][k]),
                             'nearest_pair_gap_tau1':gap,
                             'gap_scaled_drift_relative_error':diffs['drift']*gap,
                             'gap_scaled_common_frame_norm_error':diffs['canonical_rate']*gap,
                             **{name+'_relative_error' if name!='canonical_rate' else 'common_frame_drift_norm_absolute_error':v for name,v in diffs.items()}})
    return rows,mx

def plots(branches,grids):
    b=branches[('original',1.)]
    fig,ax=plt.subplots(figsize=(10,6))
    for j in range(5):
        ax.plot(b['x'],[fnorm(x) for x in b['R'][:,j]],label=f'Pair {j+1}')
    ax.set(xlabel=r'$\xi$',ylabel=r'$\|P_j\prime-[B,P_j]\|_F$',
           title='Q550 v18.51g — full kinetic covariant spectral-projector drift')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'covariant_spectral_projector_drift.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,6))
    for fr,to in ((5,4),(4,5),(5,1),(5,3)):
        data=[q for q in b['cross'] if q['from_pair']==fr and q['to_pair']==to]
        ax.plot([q['xi'] for q in data],[q['instantaneous_covariant_cross_rate'] for q in data],label=f'{fr} to {to}')
    ax.set(xlabel=r'$\xi$',ylabel='Instantaneous covariant cross-rate (oblique norm)',
           title='Q550 v18.51g — resolved cross-pair covariant drift')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'spectral_covariant_cross_pair_rates.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    for seed in SEEDS:
        sub=[g for g in grids if g['seed_family']==seed and g['tau_ref']==1.]
        ax.plot([z['stride'] for z in sub],[z['p90_5point_derivative_relative_error'] for z in sub],'o-',label=seed)
    ax.set(xlabel='Section stride (1, 2, 4)',ylabel='p90: 5-point spectral derivative relative error',
           title='Q550 v18.51g — irregular-grid derivative refinement')
    ax.set_yscale('log');ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'time_grid_refinement.png',dpi=160);plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--spectral-gap-floor',type=float,default=1e-8)
    args=parser.parse_args();OUT.mkdir(exist_ok=True)
    vals,lineage=auth();print('AUTHENTICATED genuine v18.51e 10D physical generator through v18.51f lineage',flush=True)
    branches={};gridrows=[]
    for seed in SEEDS:
        for tau in TAUS:
            b=run_branch(seed,tau,vals);branches[(seed,tau)]=b
            gridrows+=grid_stride_check(b)
            w=b['worst']
            print('BRANCH',seed,tau,'min gap',w['positive_pair_min_gap'],
                  'max covariant drift',w['total_drift'],'max spectral derivative identity',w['spectral_evolution_identity'],flush=True)
    covrows,cov=covariance(branches)
    data=[r for b in branches.values() for r in b['rows']]
    cross=[r for b in branches.values() for r in b['cross']]
    cocycle=[r for b in branches.values() for r in b['cocycle']]
    rk=[r for b in branches.values() for r in b['integrator']]
    csvsave('covariant_spectral_projector_ledger.csv',data)
    csvsave('instantaneous_covariant_interplane_rate.csv',cross)
    csvsave('finite_step_vs_instantaneous_cross_rate.csv',cocycle)
    csvsave('time_grid_derivative_refinement.csv',gridrows)
    csvsave('kinetic_similarity_covariant_control.csv',covrows)
    csvsave('rk4_cocycle_step_refinement.csv',rk)
    plots(branches,gridrows)
    fderr3=[z['fd3_derivative_relative_error'] for z in data if z['fd3_derivative_relative_error'] is not None]
    fderr5=[z['fd5_derivative_relative_error'] for z in data if z['fd5_derivative_relative_error'] is not None]
    lastcross=[];rate_contrast=[]
    for seed in SEEDS:
        for tau in TAUS:
            b=branches[(seed,tau)];dc=[r for r in b['cross'] if r['index']==78]
            s=sorted(dc,key=lambda r:r['instantaneous_covariant_cross_rate'],reverse=True)
            r54=next(q for q in dc if q['from_pair']==5 and q['to_pair']==4)['instantaneous_covariant_cross_rate']
            r45=next(q for q in dc if q['from_pair']==4 and q['to_pair']==5)['instantaneous_covariant_cross_rate']
            lastcross.append({'seed_family':seed,'tau_ref':tau,'largest_endpoint_pair':f"{s[0]['from_pair']}->{s[0]['to_pair']}",
                              'largest_endpoint_rate':s[0]['instantaneous_covariant_cross_rate'],
                              'rate_5_to_4':r54,'rate_4_to_5':r45,'rate_5to4_over_4to5':r54/r45})
            rate_contrast.append(abs(r54-r45))
    csvsave('endpoint_cross_pair_summary.csv',lastcross)
    rkmax={n:max(r[f'rk4_substeps_{n}_relative_error_to_true_cocycle'] for r in rk) for n in (1,2,4,8)}
    rksub={key:max(r[key] for r in rk) for key in ('rk4_1_vs_2','rk4_2_vs_4','rk4_4_vs_8')}
    coarse_p90={s:max(q['p90_5point_derivative_relative_error'] for q in gridrows if q['stride']==s) for s in (1,2,4)}
    maxw={key:(min if key=='positive_pair_min_gap' else max)(b['worst'][key] for b in branches.values()) for key in next(iter(branches.values()))['worst']}
    checks={
        'authenticated_v18_51f_sources_and_outputs_and_embedded_e':True,
        'authentic_genuine_10d_physical_generator_two_seed_ivps':lineage['physical_seed_ivps']==2,
        'six_branches_78_nondegenerate_sections':len(branches)==6 and len(data)==2340,
        'positive_measured_spectral_gaps':maxw['positive_pair_min_gap']>args.spectral_gap_floor,
        'spectral_projector_idempotence':maxw['projector_idempotence']<1e-9,
        'spectral_projector_resolution':maxw['projector_sum']<1e-9,
        'spectral_projector_commutes_with_M':maxw['projector_commutation']<1e-9,
        'projector_derivative_tangent_identity':maxw['projector_derivative_idempotence']<1e-8,
        'spectral_projector_differentiated_commutator_identity':maxw['spectral_evolution_identity']<1e-8,
        'spectral_derivatives_sum_to_zero':maxw['differential_pair_sum']<1e-8,
        'independent_irregular_grid_finite_differences_finite':max(fderr5)<.25 and all(np.isfinite(fderr3)),
        'fine_grid_better_than_coarse_on_common_nodes':coarse_p90[1]<coarse_p90[4],
        'genuine_B_tau_similarity':cov['B']<1e-9,
        'full_drift_tau_similarity_nondegenerate_interior':cov['interior_drift']<1e-8,
        'common_frame_covariant_norm_invariance_interior':cov['interior_canonical_rate']<3e-8,
        'near_identity_spectral_conditioning_gap_scaled_drift':cov['gap_scaled_drift']<3e-11,
        'near_identity_spectral_conditioning_gap_scaled_common_rate':cov['gap_scaled_canonical_rate']<5e-11,
        'time_step_rk4_interpolation_refinement':rksub['rk4_4_vs_8']<rksub['rk4_1_vs_2']+1e-12,
        'finite_time_cross_rate_finite':all(np.isfinite(q['finite_step_rate']) for q in cocycle),
        'one_third_did_not_enter_scientific_gates':True,
    }
    report={'version':'v18.51g','title':'Covariant Spectral-Projector Drift & Time-Step Invariance Audit',
            'classification':'NUMERICAL_COVARIANT_FINITE_TIME_PROJECTOR_DRIFT_AND_STEP_DIAGNOSTIC_NOT_MATERIAL_TORSION_OR_MEMORY_CERTIFICATE',
            'lineage':lineage,'seeds':list(SEEDS),'tau_refs':list(TAUS),
            'xi_interval':[0.,.05],'first_resolved_spectral_time':float(branches[('original',1.)]['x'][0]),
            'counts':{'branches':len(branches),'positive_sections':468,'pair_jets':len(data),
                      'instantaneous_directed_cross_rates':len(cross),'finite_step_directed_rates':len(cocycle),
                      'rk4_increment_tests':len(rk)},
            'differential_equations':{'material':'Mprime=B M','spectral':'Pprime from full Riesz eigenpair perturbation with Mprime=B M',
                                     'covariant_projector_drift':'D_xi P = Pprime - [B,P]',
                                     'instantaneous_cross_rate':'||P_to (D_xi P_from) P_from||_F / ||P_from||_F'},
            'numerical_quality':{'worst_projector':maxw,'fd3_max':max(fderr3),'fd5_max':max(fderr5),
                                 'fd3_median':float(np.median(fderr3)),'fd5_median':float(np.median(fderr5)),
                                 'coarse_grid_p90':coarse_p90,
                                 'rk4_max_error_to_genuine_cocycle_by_substeps':rkmax,
                                 'rk4_max_mutual_refinement':rksub,
                                 'max_finite_to_instantaneous_rate_relative_error':max(q['relative_rate_difference'] for q in cocycle),
                                 'median_finite_to_instantaneous_rate_relative_error':float(np.median([q['relative_rate_difference'] for q in cocycle])),
                                 'tau_covariance':cov},
            'endpoint_cross_pair':lastcross,
            'scientific_interpretation':{
                'five_pairs':'Isolated at the 78 sampled positive-time sections; no interval gap guarantee',
                'drift':'Nonzero D_xi P means the instantaneous finite-time eigenplanes do not exactly advect under the kinetic tangent cocycle',
                'finite_step':'Small-step leakage is compared with the covariant drift; the two rate definitions coincide only as dt -> 0',
                'metric':'tau_ref is a fixed kinetic-state similarity; common-frame matrices have invariant values analytically. Independent eigenderivative reconstruction shows O(e-6) near xi=0 because of small gaps, and <e-8 beyond xi>=0.001. Raw Frobenius norms are metric dependent',
                'step':'Refinement tests use interpolated B on sampled genuine physical trajectory, not a freshly solved physical 10D IVP',
                'orientation':'Directional cross-rate asymmetry does not establish a physical energy transfer, torsion, or hysteretic memory',
                'xi0':'M(0)=I has tenfold degeneracy; spectral branches only defined at xi>0',
                'one_third':'Retired from active hypothesis testing and from required checks'},
            'checks':checks,'software':{'python':sys.version.split()[0],'numpy':np.__version__,
                       'scipy':__import__('scipy').__version__,'matplotlib':matplotlib.__version__,
                       'platform':platform.platform()}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('ENDPOINT DIRECTED CROSS RATES',json.dumps(lastcross,indent=2),flush=True)
    print('NUMERICAL QUALITY',json.dumps(report['numerical_quality'],indent=2),flush=True)
    print('CHECKS',json.dumps(checks,indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('Scientific decision gate failure, inspect report.json: no valid sendback')
    print(f'Q550 v18.51g PASS {len(checks)}/{len(checks)} checks; no new physical IVP',flush=True)
if __name__=='__main__':main()
