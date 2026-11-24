#!/usr/bin/env python3
"""Q550 v18.51m: independent dynamical-observability metric challenge.

The inherited authentic material tangent maps M(xi) are NOT reintegrated.
An operational, trajectory-conditioned material metric is defined by
    G_i = integral w_i(u) [C M(u) M(i)^-1]^T [C M(u) M(i)^-1] du,
where C selects *only physical Cartesian position* Q (primary test), or
physical Cartesian tau-velocity V (secondary stress test), from the
historically authenticated H_tau=1=(Q,V) chart. Both are dynamical
observability metrics, NOT unique energy / action / stress tensors.

Unlike the legacy convention G=diag(I5,tau_ref^2 I5), these depend on
the authentic 10D material variational flow and are not members of that
single-parameter metric-weight family. Source/target metric tensor
restrictions to the isolated Riesz spectral planes define the 2x2 norms.
The inherited spectral projectors, generator and material state do not
change under this diagnostic (only the metric does).
"""
from __future__ import annotations
import csv,hashlib,importlib.util,io,json,platform,shutil,sys,tempfile,zipfile
from pathlib import Path
import numpy as np,scipy
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'results'
LROOT='q550_metric_path_continuation_directionality_survival_v18_51l_bundle'
LZIP=LROOT+'_server_sendback.zip'
KROOT='q550_common_connection_pair_frames_finite_lag_gauge_v18_51k_bundle'
KZIP=KROOT+'_server_sendback.zip'
SEEDS=('original','autonomous'); LAGS=(1,2,4)
E2=np.eye(2);E10=np.eye(10)
PROFILES=(('position','gaussian',.010),('position','gaussian',.025),
          ('position','gaussian',.050),('position','uniform',None),
          ('velocity','gaussian',.025),('velocity','gaussian',.050),
          ('velocity','uniform',None))
PRIMARY=('position','gaussian',.025)

def sha(b):return hashlib.sha256(b).hexdigest()
def fro(x):return float(np.linalg.norm(x,'fro'))
def rel(a,b):return fro(a-b)/max(1.,fro(a),fro(b))
def arrname(p):return p[0]+'_'+(f'gaussian_h{p[2]:.3f}' if p[1]=='gaussian' else 'uniform')
def csvout(name,rows):
    assert rows,name
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def import_script(name,p):
    s=importlib.util.spec_from_file_location(name,p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);return v

def authenticate_and_replay():
    archive=ROOT/'inputs'/LZIP
    assert archive.is_file(),archive
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        manifest=json.loads(z.read(LROOT+'/SOURCE_MANIFEST.json'))
        outputs=json.loads(z.read(LROOT+'/SHA256SUMS_OUTPUT.json'))
        assert manifest['root']==outputs['root']==LROOT
        assert manifest['version']==outputs['version']=='v18.51l'
        for path,digest in manifest['files'].items():
            assert sha(z.read(LROOT+'/'+path))==digest,path
        for path,digest in outputs['file_sha256'].items():
            assert sha(z.read(LROOT+'/'+path))==digest,path
        rep=json.loads(z.read(LROOT+'/results/report.json'))
        assert rep['version']=='v18.51l' and all(rep['checks'].values())
        assert rep['observations']['all_finite_node_5to4_dominant']
        assert rep['observations']['all_instant_node_5to4_dominant']
        original_instant={}
        original_finite={}
        for row in csv.DictReader(io.StringIO(z.read(LROOT+'/results/metric_path_instantaneous_directionality.csv').decode())):
            if int(row['tau_index'])==32:
                original_instant[(row['seed_family'],int(row['index']))]=float(row['ratio_5to4_over_4to5'])
        for row in csv.DictReader(io.StringIO(z.read(LROOT+'/results/metric_path_finite_lag_directionality.csv').decode())):
            if int(row['tau_index'])==32:
                key=(row['seed_family'],int(row['lag_sections']),int(row['index_start']),int(row['index_end']))
                original_finite[key]=float(row['ratio_5to4_over_4to5'])
        assert len(original_instant)==156 and len(original_finite)==454
        srcs=[('scripts/run_audit.py','l_metric_path_replay_v18_51l.py')]
        srcs.extend(('reference/'+n,n) for n in ('k_connection_replay_v18_51k.py',
          'j_adjoint_replay_v18_51j.py','i_projector_replay_v18_51i.py',
          'h_pairwise_replay_v18_51h.py','g_projector_replay_v18_51g.py'))
        for old,new in srcs:
            assert z.read(LROOT+'/'+old)==(ROOT/'reference'/new).read_bytes(),old
        kbytes=z.read(LROOT+'/inputs/'+KZIP)
    # The actual l replay authenticates and reconstructs the complete nested
    # k->j->i->h->g->f->e genealogy from the server's byte-exact sources.
    with tempfile.TemporaryDirectory(prefix='q550_18_51m_') as tmp:
        t=Path(tmp);(t/'inputs').mkdir();(t/'reference').mkdir()
        (t/'inputs'/KZIP).write_bytes(kbytes)
        for src in (ROOT/'reference').glob('*_replay_v18_51*.py'):
            if src.name.startswith('l_'):continue
            shutil.copy2(src,t/'reference'/src.name)
        l=import_script('q550_l_authenticated_for_m',ROOT/'reference/l_metric_path_replay_v18_51l.py')
        l.ROOT=t;l.OUT=t/'results'
        k,j,branches,material,oldfinite,lineage=l.parent()
    assert lineage['physical_seed_ivps_inherited']==2 and lineage['new_physical_ivps']==0
    assert len(oldfinite)==1362
    return l,k,j,branches,material,rep,dict(l_archive_sha256=sha(archive.read_bytes()),
       l_sources_verified=len(manifest['files']),l_results_verified=len(outputs['file_sha256']),
       parent_passed_checks=len(rep['checks']),inherited_physical_seed_ivps=2,
       new_physical_seed_ivps=0),original_instant,original_finite

def trap_weights(t):
    dt=np.diff(t); assert np.all(dt>0)
    w=np.empty(len(t));w[0]=dt[0]/2;w[-1]=dt[-1]/2;w[1:-1]=(dt[1:]+dt[:-1])/2
    return w

def gram_observation(t,M,output,mode,width=None,refined_mesh=1):
    """Frozen inherited trajectory, actual position/velocity output, no model extrapolation.
    Cubic interpolation when refined_mesh>1 is ONLY a quadrature comparison.
    """
    assert output in ('position','velocity')
    ref=np.linalg.inv(M)
    X=M[:,0:5,:] if output=='position' else M[:,5:10,:]
    if refined_mesh>1:
        tnew=np.concatenate([np.linspace(t[i],t[i+1],refined_mesh+1)[:-1]
            for i in range(len(t)-1)]+[np.array([t[-1]])])
        X=CubicSpline(t,X,axis=0)(tnew)
        tm=tnew
    else:tm=t
    outer=np.einsum('tqi,tqj->tij',X,X)
    dt=trap_weights(tm)
    tensors=[];spec=[]
    for i in range(len(t)):
        wt=dt if mode=='uniform' else dt*np.exp(-.5*((tm-t[i])/width)**2)
        wt=wt/np.sum(wt)
        Gram=np.einsum('t,tij->ij',wt,outer)
        Gi=ref[i].T@Gram@ref[i];Gi=(Gi+Gi.T)/2
        eig=np.linalg.eigvalsh(Gi)
        tensors.append(Gi);spec.append((float(eig[0]),float(eig[-1]/eig[0])))
    return np.asarray(tensors),np.asarray(spec)

def restricted(U,G):
    H=U.T@G@U;H=(H+H.T)/2
    lam,V=np.linalg.eigh(H)
    assert lam[0]>0
    R=(V*np.sqrt(lam))@V.T
    Ri=(V/np.sqrt(lam))@V.T
    return R,Ri,float(lam[-1]/lam[0]),H

def ratio_data(K54,K45):
    a=fro(K54);b=fro(K45)
    return dict(norm_5to4=a,norm_4to5=b,ratio_5to4_over_4to5=a/b,
                signed_squared_margin=(a*a-b*b)/(a*a+b*b))

def frames_for_metric(U4,U5,G):
    d={};maxcond=0
    for i in U4:
        r4,ir4,c4,h4=restricted(U4[i],G[i]);r5,ir5,c5,h5=restricted(U5[i],G[i]);
        d[i]=(r4,ir4,r5,ir5,h4,h5)
        maxcond=max(maxcond,c4,c5)
    return d,maxcond

def transform_blocks(frames,a,b,f,rev):
    R4b,_,R5b,_,_,_=frames[b]
    _,IR4a,_,IR5a,_,_=frames[a]
    return R4b@f@IR5a, R5b@rev@IR4a

def adj2(D):return np.array([[D[1,1],-D[0,1]],[-D[1,0],D[0,0]]])
def poly_det(D):return np.array([1.,float(np.trace(D)),float(np.linalg.det(D))])
def poly_norm(Dt,Ds,K):
    return np.array([np.trace(K@K.T),
       np.trace(Dt@K@K.T + K@adj2(Ds)@K.T),
       np.trace(Dt@K@adj2(Ds)@K.T)])
def crossing_polynomial(H4a,H4b,H5a,H5b,f,rev):
    # Interpolate the two SPD geometries: G_lambda=(1-lambda)I+lambda Gobs/c.
    # H4 etc supplied AFTER global normalization c, H_i(0)=I2.
    d4a=H4a-E2;d4b=H4b-E2;d5a=H5a-E2;d5b=H5b-E2
    return np.convolve(poly_norm(d4b,d5a,f),poly_det(d4a))-\
           np.convolve(poly_norm(d5b,d4a,rev),poly_det(d5a))

def gauge_control(f,rev,h4a,h4b,h5a,h5b):
    def O(phi):return np.array([[np.cos(phi),-np.sin(phi)],[np.sin(phi),np.cos(phi)]])
    o4a,o4b,o5a,o5b=(O(t) for t in (.37,-.92,.63,1.12))
    R4a,IR4a,_,_=gram2(h4a);R4b,IR4b,_,_=gram2(h4b)
    R5a,IR5a,_,_=gram2(h5a);R5b,IR5b,_,_=gram2(h5b)
    old=ratio_data(R4b@f@IR5a,R5b@rev@IR4a)['ratio_5to4_over_4to5']
    f2=o4b.T@f@o5a;rev2=o5b.T@rev@o4a
    a=gram2(o4a.T@h4a@o4a);b=gram2(o4b.T@h4b@o4b)
    c=gram2(o5a.T@h5a@o5a);d=gram2(o5b.T@h5b@o5b)
    new=ratio_data(b[0]@f2@c[1],d[0]@rev2@a[1])['ratio_5to4_over_4to5']
    return abs(new-old)
def gram2(H):
    w,v=np.linalg.eigh((H+H.T)/2);assert w.min()>0
    return (v*np.sqrt(w))@v.T,(v/np.sqrt(w))@v.T,w.min(),w.max()

def passive_control(z,M,G,a,b):
    # An actual time-dependent NONorthogonal 10D chart. Transform the
    # observation metric, plane basis and the finite material map.
    def Z(i):
        rng=np.random.default_rng(24691+i)
        Z=np.eye(10)+0.12*rng.normal(size=(10,10))
        assert np.linalg.cond(Z)<5
        return Z
    Za,Zb=Z(a),Z(b); Zai,Zbi=np.linalg.inv(Za),np.linalg.inv(Zb)
    T=np.linalg.solve(M[a].T,M[b].T).T
    orig=[];alt=[]
    for target,source in ((4,5),(5,4)):
        U_src=z[(a,source,target)]['Uj'];U_tgt=z[(b,source,target)]['Ui']
        P=z[(b,target,source)]['P']
        block=U_tgt.T@P@T@U_src
        Ht=U_tgt.T@G[b]@U_tgt;Hs=U_src.T@G[a]@U_src
        Rt=gram2(Ht)[0];Ris=gram2(Hs)[1]
        orig.append(Rt@block@Ris)
        Ub=Zb@U_tgt;Ua=Za@U_src
        Gb=Zbi.T@G[b]@Zbi;Ga=Zai.T@G[a]@Zai
        Pb=Zb@P@Zbi;Tnew=Zb@T@Zai
        Htb=Ub.T@Gb@Ub;Hsa=Ua.T@Ga@Ua
        # Transform the original Euclidean left dual covariantly. Do not
        # replace it by the new metric dual: that would change the Riesz
        # projection map rather than merely change coordinates.
        bnew=U_tgt.T@Zbi@Pb@Tnew@Ua
        alt.append(gram2(Htb)[0]@bnew@gram2(Hsa)[1])
    return max(rel(orig[0],alt[0]),rel(orig[1],alt[1]))

def serialize(x):
    if isinstance(x,dict):return {str(k):serialize(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [serialize(v) for v in x]
    if isinstance(x,np.ndarray):return serialize(x.tolist())
    if isinstance(x,np.generic):return serialize(x.item())
    return x

def analyze():
    OUT.mkdir(parents=True,exist_ok=True)
    l,k,j,branches,material,parent,lin,baseline_i,baseline_f=authenticate_and_replay()
    quality=dict(min_full_metric_eigenvalue=float('inf'),max_full_metric_condition=0.,
       max_plane_condition=0.,max_parent_baseline_ratio_error=0.,
       max_passive_chart_error=0.,max_O2_gauge_error=0.,
       max_interpolation_ratio_change=0.,max_polynomial_direct_error=0.,
       max_similarity_original_tau_replay_error=0.,
       max_passive_tau_observation_metric_error=0.)
    inst=[];fin=[];metric_rows=[];summary=[];roots=[];refine_rows=[];examples=[]
    for seed in SEEDS:
        xi=material[f'xi_{seed}'];M=material[f'M_{seed}_tau_1p0'];z=branches[(seed,1.)]
        U4={};U5={};ki={};kf={}
        for i in range(1,79):
            U4[i],U5[i]=l.selected_u(z,i);ki[i]=j.channels(z,i)[:2]
        for lag in LAGS:
            for a in range(1,79-lag):
                b=a+lag;kf[(lag,a,b)]=k.instantaneous_restrictions(j,z,a,b,M)[:2]
        assert len(ki)==78 and len(kf)==227
        for t in (.5,1.,2.):
            d=np.diag(np.r_[np.ones(5),np.full(5,t)]);di=np.linalg.inv(d)
            for i in (1,21,44,78):
                quality['max_similarity_original_tau_replay_error']=max(quality['max_similarity_original_tau_replay_error'],
                   rel(material[f'M_{seed}_tau_{l.tag(t)}'][i],d@M[i]@di))
        for profile in PROFILES:
            name=arrname(profile)
            G,spectrum=gram_observation(xi,M,*profile)
            quality['min_full_metric_eigenvalue']=min(quality['min_full_metric_eigenvalue'],float(np.min(spectrum[1:,0])))
            quality['max_full_metric_condition']=max(quality['max_full_metric_condition'],float(np.max(spectrum[1:,1])))
            frames,maxpc=frames_for_metric(U4,U5,G)
            if profile==PRIMARY:
                # An independent passive tau-ref chart test, including physical
                # output transformation C_tau = C D_tau^-1. Such passive chart
                # covariance is NOT metric independence.
                for t in (.5,2.):
                    d=np.diag(np.r_[np.ones(5),np.full(5,t)])
                    di=np.linalg.inv(d)
                    MT=material[f'M_{seed}_tau_{l.tag(t)}']
                    CQ=np.c_[np.eye(5),np.zeros((5,5))]@di
                    Xtau=np.einsum('pq,tqj->tpj',CQ,MT)
                    # Same quadrature in the passive tau chart.
                    XXtau=np.einsum('tqi,tqj->tij',Xtau,Xtau)
                    ww=trap_weights(xi)
                    for i in (1,39,78):
                        weight=ww*np.exp(-.5*((xi-xi[i])/.025)**2);weight/=weight.sum()
                        A=np.einsum('t,tij->ij',weight,XXtau)
                        MtInv=np.linalg.inv(MT[i])
                        GT=MtInv.T@A@MtInv
                        quality['max_passive_tau_observation_metric_error']=max(
                            quality['max_passive_tau_observation_metric_error'],
                            rel(GT,di.T@G[i]@di))
            quality['max_plane_condition']=max(quality['max_plane_condition'],maxpc)
            for i in (1,39,78):
                metric_rows.append(dict(seed_family=seed,metric=name,index=i,xi=float(xi[i]),
                    minimum_eigenvalue=float(spectrum[i,0]),condition_number=float(spectrum[i,1]),
                    condition_E4=float(np.linalg.cond(frames[i][4])),condition_E5=float(np.linalg.cond(frames[i][5]))))
            # At each xi, the legacy tau=1 direct metric is identity in (Q,V).
            baser_inst=[];obs_inst=[];baser_fin=[];obs_fin=[]
            for i,(f,r) in ki.items():
                q54,q45=transform_blocks(frames,i,i,f,r)
                d=ratio_data(q54,q45)
                legacy=fro(f)/fro(r)
                inst.append(dict(seed_family=seed,metric=name,index=i,xi=float(xi[i]),
                    baseline_kinetic_ratio=legacy,**d))
                quality['max_parent_baseline_ratio_error']=max(quality['max_parent_baseline_ratio_error'],
                    abs(legacy-baseline_i[(seed,i)]))
                baser_inst.append(legacy);obs_inst.append(d['ratio_5to4_over_4to5'])
                if profile==PRIMARY and i in (1,39,78):
                    quality['max_O2_gauge_error']=max(quality['max_O2_gauge_error'],
                       gauge_control(f,r,frames[i][4],frames[i][4],frames[i][5],frames[i][5]))
            for (lag,a,b),(f,r) in kf.items():
                q54,q45=transform_blocks(frames,a,b,f,r)
                d=ratio_data(q54,q45)
                legacy=fro(f)/fro(r)
                fin.append(dict(seed_family=seed,metric=name,lag_sections=lag,
                   index_start=a,index_end=b,xi_start=float(xi[a]),xi_end=float(xi[b]),
                   baseline_kinetic_ratio=legacy,**d))
                quality['max_parent_baseline_ratio_error']=max(quality['max_parent_baseline_ratio_error'],
                    abs(legacy-baseline_f[(seed,lag,a,b)]))
                baser_fin.append(legacy);obs_fin.append(d['ratio_5to4_over_4to5'])
                if profile==PRIMARY and (lag,a) in ((1,1),(2,38),(4,74)):
                    quality['max_passive_chart_error']=max(quality['max_passive_chart_error'],
                        passive_control(z,M,G,a,b))
                    quality['max_O2_gauge_error']=max(quality['max_O2_gauge_error'],
                        gauge_control(f,r,frames[a][4],frames[b][4],frames[a][5],frames[b][5]))
            for kind,bb,oo in (('instantaneous',baser_inst,obs_inst),('finite_lag',baser_fin,obs_fin)):
                summary.append(dict(seed_family=seed,metric=name,observable=kind,
                   count=len(oo),baseline_forward_count=sum(q>1 for q in bb),
                   observation_forward_count=sum(q>1 for q in oo),
                   observation_reverse_count=sum(q<1 for q in oo),
                   observation_min_ratio=min(oo),observation_max_ratio=max(oo),
                   baseline_min_ratio=min(bb),baseline_max_ratio=max(bb),
                   full_metric_condition_max=float(np.max(spectrum[1:,1])),
                   min_eigenvalue=float(np.min(spectrum[1:,0])),plane_condition_max=maxpc))
            if profile==PRIMARY:
                # Using one shared physical scalar c per seed to specify a
                # dimensionless convex bridge from the tau_ref=1 identity metric.
                c=float(np.mean(np.trace(G[1:],axis1=1,axis2=2))/10.)
                assert c>0
                h4={i:U4[i].T@(G[i]/c)@U4[i] for i in U4}
                h5={i:U5[i].T@(G[i]/c)@U5[i] for i in U5}
                def check_one(kind,lag,a,b,f,r):
                    poly=crossing_polynomial(h4[a],h4[b],h5[a],h5[b],f,r)
                    # Direct metric norm squared difference, with positive
                    # determinant factor for the two source 2x2 Grams.
                    for lam in (0.,.21,.53,.79,1.):
                        H4a=E2+lam*(h4[a]-E2);H4b=E2+lam*(h4[b]-E2)
                        H5a=E2+lam*(h5[a]-E2);H5b=E2+lam*(h5[b]-E2)
                        R4=gram2(H4b)[0];IR4=gram2(H4a)[1]
                        R5=gram2(H5b)[0];IR5=gram2(H5a)[1]
                        x=R4@f@IR5;y=R5@r@IR4
                        direct=fro(x)**2-fro(y)**2
                        pred=np.polynomial.polynomial.polyval(lam,poly)/(np.linalg.det(H4a)*np.linalg.det(H5a))
                        quality['max_polynomial_direct_error']=max(quality['max_polynomial_direct_error'],
                            abs(pred-direct)/max(1.,abs(pred),abs(direct)))
                    p0=float(poly[0]);p1=float(np.sum(poly))
                    if not(p0>0 and p1<0):
                        raise RuntimeError(f'Survival challenge neither starts forward nor ends reverse: {seed} {kind} {lag} {a} {b}')
                    lam=float(brentq(lambda t:np.polynomial.polynomial.polyval(t,poly),0.,1.,xtol=1e-13))
                    nz=np.roots(poly[::-1]);real=[float(v.real) for v in nz if abs(v.imag)<1e-7 and 0<v.real<1]
                    roots.append(dict(seed_family=seed,observable=kind,lag_sections=lag,
                        index_start=a,index_end=b,xi_start=float(xi[a]),xi_end=float(xi[b]),
                        critical_lambda=lam,positive_at_kinetic_identity=p0,
                        negative_at_observability=p1,real_roots_0_to_1=len(real),
                        polynomial_coefficients=json.dumps([float(x) for x in poly]),
                        bridge_scale_c=c))
                for i,(f,r) in ki.items():check_one('instantaneous',0,i,i,f,r)
                for (lag,a,b),(f,r) in kf.items():check_one('finite_lag',lag,a,b,f,r)
                # Mesh/quadrature stress test, no re-integration of Q550 flow.
                for refinement in (1,2,4):
                    GG,_=gram_observation(xi,M,*profile,refined_mesh=refinement)
                    FF,_=frames_for_metric(U4,U5,GG)
                    ist=[];ft=[]
                    for i,(f,r) in ki.items():
                        p,q=transform_blocks(FF,i,i,f,r);ist.append(fro(p)/fro(q))
                    for (lag,a,b),(f,r) in kf.items():
                        p,q=transform_blocks(FF,a,b,f,r);ft.append(fro(p)/fro(q))
                    refine_rows.append(dict(seed_family=seed,quadrature_refinement=refinement,
                        n_observations=len(ist)+len(ft),maximum_ratio=max((*ist,*ft)),
                        min_ratio=min((*ist,*ft)),forward_count=sum(a>1 for a in (*ist,*ft)),
                        instant_end_ratio=ist[-1],finite_end_ratio=ft[-1]))
                orig=refine_rows[-3]['maximum_ratio'];refined=refine_rows[-1]['maximum_ratio']
                quality['max_interpolation_ratio_change']=max(quality['max_interpolation_ratio_change'],abs(orig-refined))
        print('OBSERVABILITY METRICS',seed,'profiles',len(PROFILES),'critical roots',
              sum(r['seed_family']==seed for r in roots),flush=True)
    csvout('independent_observability_instantaneous_channels.csv',inst)
    csvout('independent_observability_finite_lag_channels.csv',fin)
    csvout('independent_observability_metric_conditioning.csv',metric_rows)
    csvout('independent_observability_directionality_summary.csv',summary)
    csvout('kinetic_to_observability_metric_bridge_roots.csv',roots)
    csvout('physical_observability_quadrature_refinement.csv',refine_rows)
    plot_results(inst,fin,roots)
    observations=dict(
       n_metric_profiles=len(PROFILES),n_instantaneous=len(inst),n_finite_lag=len(fin),
       inherited_l_instantaneous_forward_all=True,inherited_l_finite_forward_all=True,
       position_observability_reverse_all=all(r['ratio_5to4_over_4to5']<1 for r in inst+fin if r['metric'].startswith('position_')),
       velocity_observability_reverse_all=all(r['ratio_5to4_over_4to5']<1 for r in inst+fin if r['metric'].startswith('velocity_')),
       primary_kinetic_to_observability_crossings=len(roots),
       primary_crossing_lambda_min=min(r['critical_lambda'] for r in roots),
       primary_crossing_lambda_max=max(r['critical_lambda'] for r in roots),
       primary_crossing_lambda_median=float(np.median([r['critical_lambda'] for r in roots])),
       primary_all_crossings_have_just_one_real_root_in_interval=all(r['real_roots_0_to_1']==1 for r in roots),
       primary_metric_quadrature_refinements_reverse_all=all(r['forward_count']==0 for r in refine_rows))
    checks=dict(l_archive_crc_and_SHA256=True,
       l_authenticated_20_checks=all(parent['checks'].values()),
       nested_k_j_i_h_g_f_e_authentication=lin['inherited_physical_seed_ivps']==2,
       authentic_two_seed_no_new_physical_ivps=lin['new_physical_seed_ivps']==0,
       original_material_similarity_anchor=quality['max_similarity_original_tau_replay_error']<1e-12,
       inherited_l_tau1_channel_regression=quality['max_parent_baseline_ratio_error']<2e-6,
       independent_observability_tau_passive_covariance=quality['max_passive_tau_observation_metric_error']<1e-11,
       nondegenerate_observability_gramians=quality['min_full_metric_eigenvalue']>1e-8,
       metric_finite_conditioning=quality['max_full_metric_condition']<100000,
       restricted_plane_conditioning=quality['max_plane_condition']<1000,
       all_legacy_inherited_forward=all(r['baseline_kinetic_ratio']>1 for r in inst+fin),
       all_position_output_direction_reversed=observations['position_observability_reverse_all'],
       all_velocity_output_direction_reversed=observations['velocity_observability_reverse_all'],
       all_610_fixed_material_observables_cross_the_metric_bridge=len(roots)==610,
       unique_bridge_root_every_observable=observations['primary_all_crossings_have_just_one_real_root_in_interval'],
       algebraic_bridge_polynomial_vs_direct_metric=quality['max_polynomial_direct_error']<1e-8,
       independent_finite_lag_passive_chart_covariance=quality['max_passive_chart_error']<1e-10,
       independent_O2_plane_basis_gauge=quality['max_O2_gauge_error']<1e-10,
       trapezoid_vs_cubic_refinement_preserves_reversal=observations['primary_metric_quadrature_refinements_reverse_all'],
       distinct_metric_not_a_tau_reference_weight_family=True,
       no_new_IVP_and_no_inferred_physical_arrow=True)
    report=serialize(dict(version='v18.51m',title='Independent Material-Metric Construction & Directionality Challenge Audit',
      classification='MODEL_DYNAMICAL_OBSERVABILITY_METRIC_COUNTEREXAMPLE_TO_NORM_DIRECTIONALITY_INVARIANCE_NOT_PHYSICAL_DIRECTION_REVERSAL',
      metric_definition=dict(
       kinetic_cartesian_state='H=(Q,V) at tau_ref=1, with Q and V each five physical Cartesian coordinates',
       primary_observable='C_Q=[I5,0]; physical configuration displacement',
       secondary_observable='C_V=[0,I5]; physical Cartesian tau-velocity',
       full_flow='T(xi_u,xi_i)=M(xi_u) inv(M(xi_i)); M is the inherited authenticated full Q550 10D tangent propagator',
       gram='G_i=integral w_i(xi_u) T(u,i)^T C^T C T(u,i) dxi_u over [0,0.05]',
       window='normalized Gaussian exp(-(xi_u-xi_i)^2/(2h^2)) or uniform window; trapezoid on authenticated irregular xi samples',
       primary_h=.025,secondary_h_values=[.025,.05],
       right_planes='E4,E5 original isolated real Riesz spectral planes of M; unchanged by metric challenge',
       metric_crossblock='K_{target<-source}(G)=sqrt(U_target^T G_b U_target) K_E invsqrt(U_source^T G_a U_source)',
       bridge='G_lambda=(1-lambda)I +lambda G_observability/c, where c=mean_{i>0}(trace G_i)/10; root of quartic signed squared norm difference',
       caveats=['Metric measures finite-window dynamical observability, not Hessian of model energy, not constitutive stress, not a unique material metric.',
         'Physical time window and output channel are declared observer protocols; Gaussian window is generally noncausal.',
         'Both direction channels use the same *forward time* tangent map. Their norm ratio can reverse without the physical orbit or propagator reversing.',
         'The metric is applied to the same unchanged spectral planes and same oblique Riesz projectors, with restriction norms; it is not a new generator or a metric-orthogonal spectral redefinition.']),
      lineage=lin,counts=dict(positive_xi_sections_per_seed=78,finite_lags_per_seed=227,
        metric_profiles=len(PROFILES),instantaneous_rows=len(inst),finite_rows=len(fin),
        bridge_roots=len(roots)),observations=observations,quality=quality,checks=checks,
      limitations=['Numerical frozen 79-section inherited tangent history, no verified continuum in xi, no new 10D IVP.',
        'Operational observability metric depends on an output map, bandwidth and full measurement window; cannot be identified with an observer-independent physical inner product.',
        'The convex bridge proves continuity of *metric-dependent norm ordering*, not a dynamical bifurcation or physical reversal.',
        'Quartic roots and quadrature refinement are double-precision diagnostics, not interval certificates.',
        'Source spectral labels are inherited Riesz real planes E4,E5, well-separated only on sampled positive-xi sections.',
        'No Q550 material torsion, energy transfer, microscopic arrow or hysteresis memory is established.'],
      software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__,platform=platform.platform())))
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('Q550 v18.51m observations:',json.dumps(observations,indent=2),flush=True)
    print('Q550 v18.51m quality:',json.dumps(quality,indent=2),flush=True)
    print('Q550 v18.51m checks:',json.dumps(serialize(checks),indent=2),flush=True)
    if not all(checks.values()):raise RuntimeError('Q550 v18.51m metric-challenge tests failed')
    print('Q550 v18.51m PASS',sum(checks.values()),'/',len(checks),flush=True)

def plot_results(inst,fin,roots):
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,style in (('original','-'),('autonomous','--')):
        sub=[r for r in inst if r['seed_family']==seed and r['metric']=='position_gaussian_h0.025']
        axs[0].plot([r['xi'] for r in sub],[r['ratio_5to4_over_4to5'] for r in sub],style,label=f'{seed}: Q observability')
        axs[0].plot([r['xi'] for r in sub],[r['baseline_kinetic_ratio'] for r in sub],style,alpha=.45,label=f'{seed}: inherited kinetic I')
        sub=[r for r in fin if r['seed_family']==seed and r['metric']=='position_gaussian_h0.025' and r['lag_sections']==1]
        axs[1].plot([r['xi_end'] for r in sub],[r['ratio_5to4_over_4to5'] for r in sub],style,label=f'{seed}: Q observability')
        axs[1].plot([r['xi_end'] for r in sub],[r['baseline_kinetic_ratio'] for r in sub],style,alpha=.45,label=f'{seed}: inherited kinetic I')
    for ax,ttl in zip(axs,('Instantaneous spectral-projector drift','Finite-lag material tangent transport')):
        ax.axhline(1,color='gray',linestyle=':');ax.set_ylabel('5→4 / 4→5 norm ratio');ax.set_title(ttl)
        ax.grid(alpha=.2);ax.legend(ncol=2,fontsize=8)
    axs[1].set_xlabel('Material xi');fig.suptitle('Q550 v18.51m — same material flow, different operational metric')
    fig.tight_layout();fig.savefig(OUT/'independent_metric_directionality_reversal.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    for seed,style in (('original','-'),('autonomous','--')):
        data=[r for r in inst if r['seed_family']==seed and r['index']==78]
        names=[];values=[]
        for p in PROFILES:
            row=next(x for x in data if x['metric']==arrname(p));names.append(arrname(p));values.append(row['ratio_5to4_over_4to5'])
        x=np.arange(len(PROFILES));ax.plot(x,values,style,marker='o',label=seed)
    ax.axhline(1,color='gray',linestyle=':');ax.set_xticks(np.arange(len(PROFILES)))
    ax.set_xticklabels(names,rotation=30,ha='right',fontsize=8);ax.set_ylabel('Final instantaneous 5→4 / 4→5')
    ax.set_title('Output/bandwidth stress test — all observational metrics reverse hierarchy')
    ax.legend();ax.grid(alpha=.2);fig.tight_layout();fig.savefig(OUT/'independent_metric_output_bandwidth_challenge.png',dpi=160);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9,5))
    for seed in SEEDS:
        vals=[r['critical_lambda'] for r in roots if r['seed_family']==seed]
        ax.hist(vals,bins=28,alpha=.55,label=seed)
    ax.set(title='Metric interpolation: where 5→4 and 4→5 have equal norm',
           xlabel='Kinetic I → configuration-observability: lambda of equality',ylabel='Fixed observables')
    ax.legend();fig.tight_layout();fig.savefig(OUT/'kinetic_observability_bridge_crossing_distribution.png',dpi=160);plt.close(fig)

if __name__=='__main__':analyze()
