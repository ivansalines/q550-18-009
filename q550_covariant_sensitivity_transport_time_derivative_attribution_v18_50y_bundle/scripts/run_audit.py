#!/usr/bin/env python3
"""Q550 v18.50y — canonical projector transport of tensor-valued kappa sensitivity.

Input: authenticated v18.50x SERVER SENDBACK, including numerical 10x10 P,E,A.
No 10D physical IVPs are performed here. This is an algebraic/time-interpolation
postprocessing of existing 44 physical IVPs, not a physical metric certificate.

Let P be the orthogonal projector, K=[dP/dxi,P] (skew), E=dP/dkappa.
The canonical Grassmannian horizontal connection satisfies dP=[K,P].
The endomorphism covariant rate is D E = dE/dxi - [K,E].
K is determined from P alone, not fitted to E. A general gauge change requires
transforming the *whole connection*, including the in-frame term S' S^-1;
recomputing [P',P] alone after a gauge change does not generally give it.
"""
from __future__ import annotations
import io,json,hashlib,zipfile,platform
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
from scipy.integrate import solve_ivp
from scipy.linalg import expm

ROOT=Path(__file__).resolve().parents[1]
X='q550_anchor_free_kappa_differential_response_moving_sensitivity_geometry_v18_50x_bundle'
PARENT=ROOT/'inputs'/(X+'_server_sendback.zip')


def sha(b):return hashlib.sha256(b).hexdigest()


def auth_parent():
    with zipfile.ZipFile(PARENT) as z:
        if z.testzip() is not None:raise RuntimeError('Parent ZIP CRC failed')
        src=json.loads(z.read(X+'/SOURCE_MANIFEST.json'))
        out=json.loads(z.read(X+'/SHA256SUMS_OUTPUT.json'))
        if src['root']!=X or out['root']!=X:raise RuntimeError('Parent root mismatch')
        for rel,h in src['files'].items():
            if sha(z.read(X+'/'+rel))!=h:raise RuntimeError('Parent source drift: '+rel)
        for rel,h in out['file_sha256'].items():
            if sha(z.read(X+'/'+rel))!=h:raise RuntimeError('Parent result drift: '+rel)
        meta=json.loads(z.read(X+'/results/report.json'))
        if meta['version']!='v18.50x' or meta['design']['rows']!=3476:
            raise RuntimeError('Unexpected parent x replay/report')
        with np.load(io.BytesIO(z.read(X+'/results/full_projector_sensitivity_tensors.npz'))) as f:
            data={k:f[k].copy() for k in f.files}
    return data,{'x_sources':len(src['files']),'x_outputs':len(out['file_sha256']),
                 'x_sendback_sha256':sha(PARENT.read_bytes()),
                 'x_completed_ivps_recorded':meta['design']['new_10d_driven_ivps']}


def fnorm(a):return np.linalg.norm(a,axis=(-2,-1))

def inner(a,b):return np.einsum('...ij,...ij->...',a,b,optimize=True)

def comm(a,b):return a@b-b@a

def finite_weights(x0,xx):
    sc=float(np.max(abs(xx-x0)))
    if sc<=0:raise ValueError('repeated xi values')
    t=(xx-x0)/sc
    M=np.stack([t**j for j in range(len(t))],axis=0)
    y=np.zeros(len(t));y[1]=1/sc
    return np.linalg.solve(M,y)

def five_node_derivative(arr,x):
    out=np.empty_like(arr);n=len(x)
    if arr.shape[1]!=n:raise ValueError('second axis must be evolution sections')
    for j in range(n):
        lo=max(0,min(n-5,j-2));ids=np.arange(lo,lo+5)
        w=finite_weights(x[j],x[ids])
        out[:,j]=np.einsum('a,baij->bij',w,arr[:,ids],optimize=True)
    return out


def tensor_rates(P,E,A,xi):
    pd=CubicSpline(xi,P,axis=1).derivative()(xi)
    aspl=CubicSpline(xi,E,axis=1).derivative()(xi)
    k=comm(pd,P)
    motion=comm(k,E)
    dc=aspl-motion
    s=fnorm(E)
    radial=inner(E,aspl)/s
    radial_cov=inner(E,dc)/s
    ordinary_perp=aspl-radial[...,None,None]*E/s[...,None,None]
    cov_perp=dc-radial_cov[...,None,None]*E/s[...,None,None]
    ang_raw=fnorm(ordinary_perp)/s
    ang_cov=fnorm(cov_perp)/s
    q=np.eye(10)[None,None,:,:]-P
    checks={
      'projector_derivative_connection_residual_max':float(np.max(fnorm(pd-comm(k,P)))),
      'connection_skew_residual_max':float(np.max(fnorm(k+np.swapaxes(k,-1,-2)))),
      'radial_rate_invariance_max_abs':float(np.max(abs(radial-radial_cov))),
      'E_tangency_P_relative_max':float(np.max(fnorm(P@E@P)/s)),
      'E_tangency_Q_relative_max':float(np.max(fnorm(q@E@q)/s)),
      'covariant_E_rate_offtangent_P_relative_max':float(np.max(fnorm(P@dc@P)/np.maximum(fnorm(dc),1e-20))),
      'covariant_E_rate_offtangent_Q_relative_max':float(np.max(fnorm(q@dc@q)/np.maximum(fnorm(dc),1e-20))),
    }
    p5=five_node_derivative(P,xi)
    a5=five_node_derivative(E,xi)
    k5=comm(p5,P)
    dc5=a5-comm(k5,E)
    deriv_checks={
      'parent_A_vs_spline_relative_max':float(np.max(fnorm(A-aspl)/np.maximum(fnorm(aspl),1e-20))),
      'spline_vs_five_node_Pdot_relative_max':float(np.max(fnorm(pd-p5)/np.maximum(fnorm(pd),1e-20))),
      'spline_vs_five_node_A_relative_max':float(np.max(fnorm(aspl-a5)/np.maximum(fnorm(aspl),1e-20))),
      'spline_vs_five_node_covrate_relative_max':float(np.max(fnorm(dc-dc5)/np.maximum(fnorm(dc),1e-20))),
      'spline_vs_five_node_covrate_relative_p99':float(np.percentile(fnorm(dc-dc5)/np.maximum(fnorm(dc),1e-20),99)),
    }
    # Angle between E and its initial tensor, free of arccos cancellation.
    def unitangle(U,V):
        u=U/np.maximum(fnorm(U)[...,None,None],1e-30)
        v=V/np.maximum(fnorm(V)[...,None,None],1e-30)
        return np.degrees(2*np.arctan2(fnorm(u-v),fnorm(u+v)))
    angle=unitangle(E,E[:,0:1])
    return locals()


def parallel_centerline(xi,P,E,K,rtol=1e-12,max_div=128):
    # Numerical ODE integrates an orthogonal-frame generator from the P path;
    # it is NOT the physical tangent ODE of the underlying 10D state.
    kcs=CubicSpline(xi,K,axis=0)
    def ode(t,y):
        ki=kcs(t);ki=(ki-ki.T)*.5
        return (ki@y.reshape(10,10)).reshape(-1)
    sol=solve_ivp(ode,(float(xi[0]),float(xi[-1])),np.eye(10).ravel(),
                  method='DOP853',rtol=rtol,atol=max(rtol*0.01,1e-15),
                  max_step=float(xi[-1]-xi[0])/max_div,t_eval=xi)
    if not sol.success or abs(sol.t[-1]-xi[-1])>1e-12:raise RuntimeError('Incomplete projector transport IVP')
    U=sol.y.T.reshape(-1,10,10)
    Et=np.swapaxes(U,-1,-2)@E@U
    Pt=U@P[0]@np.swapaxes(U,-1,-2)
    def ang(a,b):
        aa=a/fnorm(a);bb=b/fnorm(b)
        return float(np.degrees(2*np.arctan2(fnorm(aa-bb),fnorm(aa+bb))))
    metric={
     'raw_angle_final_deg':ang(E[0],E[-1]),
     'horizontal_transport_corrected_angle_final_deg':ang(Et[0],Et[-1]),
     'frame_orthogonality_max':float(np.max(fnorm(np.swapaxes(U,-1,-2)@U-np.eye(10)))),
     'projector_transport_endpoint_frobenius':float(fnorm(Pt[-1]-P[-1])),
     'nfev':int(sol.nfev), 'steps':int(len(sol.t)-1),'success':bool(sol.success)}
    return Et,U,metric


def metricnorm(X,G):
    # Endomorphism Hilbert-Schmidt metric, not naive Euclidean entries after
    # a general nonorthogonal change of coordinates.
    v=np.trace(X.T@G@X@np.linalg.inv(G))
    return float(np.sqrt(max(float(v),0)))


def coordinate_gauge_controls(xi,E,A,K,points):
    # Deliberately nonorthogonal, moving coordinate change S=exp(W*xi).
    W=np.zeros((10,10))
    W[0,5]=20.;W[5,0]=-11.
    W[1,7]=-14.;W[7,1]=18.
    W[2,2]=3.;W[8,8]=-2.
    rows=[]
    for j in points:
        S=expm(W*float(xi[j]));Si=np.linalg.inv(S)
        Es=S@E[j]@Si
        As=S@A[j]@Si+comm(W,Es)
        Ks=S@K[j]@Si+W
        D=A[j]-comm(K[j],E[j])
        Ds=As-comm(Ks,Es)
        G=Si.T@Si
        invariant=metricnorm(Ds,G)
        expected=float(fnorm(D))
        bad=As-comm(S@K[j]@Si,Es) # intentionally omits W
        rows.append({'xi':float(xi[j]),'relative_covariance_residual':float(fnorm(Ds-S@D@Si)/max(fnorm(S@D@Si),1e-30)),
           'metric_norm_relative_residual':abs(invariant-expected)/max(expected,1e-30),
           'if_ignore_frame_W_norm_error':float(metricnorm(bad,G)-expected),
           'gauge_condition':float(np.linalg.cond(S))})
    return rows


def plots(df,checks,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(12.2,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        d=df[(df.seed_family==seed)&(abs(df.offset_units-.5)<1e-10)].sort_values('xi')
        ax.plot(d.xi,d.orientation_rate_ordinary,label='ordinary dE/dξ')
        ax.plot(d.xi,d.orientation_rate_horizontal,label='canonical ∇ξ E')
        ax.set(title=seed,xlabel='Turn-relative ξ',ylabel='Sensitivity direction rate (rad/ξ)')
        ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('v18.50y | Ordinary vs horizontal covariant sensitivity rate')
    fig.tight_layout();fig.savefig(out/'sensitivity_ordinary_vs_horizontal_rates.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12.2,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        d=checks[(checks.seed_family==seed)&(abs(checks.offset_units-.5)<1e-10)].sort_values('xi')
        ax.plot(d.xi,d.raw_angle_deg,label='fixed 10D chart')
        ax.plot(d.xi,d.horizontal_corrected_angle_deg,label='parallel P-transport')
        ax.set(title=seed,xlabel='Turn-relative ξ',ylabel='Angle to initial E (degrees)')
        ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('v18.50y | Sensitivity rotation relative to transported kernel frame')
    fig.tight_layout();fig.savefig(out/'sensitivity_angle_transport_attribution.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(10,5))
    for seed in ('original','autonomous'):
        d=df[(df.seed_family==seed)&(abs(df.offset_units-.5)<1e-10)].sort_values('xi')
        ax.plot(d.xi,d.connection_commutator_norm,label=seed+'  ||[K,E]||')
    ax.set(xlabel='Turn-relative ξ',ylabel='Frobenius rate norm',title='v18.50y | Observable-frame contribution to dE/dξ')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout();fig.savefig(out/'observer_frame_rate_contribution.png',dpi=145);plt.close(fig)


def run():
    out=ROOT/'results';out.mkdir(exist_ok=True)
    data,auth=auth_parent()
    xi=data['xi'];offsets=data['offset_units'];kappas=data['kappa']
    if len(xi)!=79 or len(kappas)!=22:raise RuntimeError('Unexpected x data dimensions')
    if np.any(np.diff(xi)<=0):raise RuntimeError('Time grid is not increasing')
    rows=[]; angle_rows=[];gauge_rows=[];method={}; transport={};archive={}
    for seed in ('original','autonomous'):
        P=data['P_'+seed];E=data['E_'+seed];A=data['A_'+seed]
        if P.shape!=(22,79,10,10):raise RuntimeError('Unrecognized tensor shape')
        r=tensor_rates(P,E,A,xi)
        method[seed]={'algebraic':r['checks'],'stencil':r['deriv_checks']}
        for i,offset in enumerate(offsets):
            for j,tm in enumerate(xi):
                rows.append({'seed_family':seed,'offset_units':float(offset),'kappa':float(kappas[i]),
                 'xi':float(tm),'E_norm':float(r['s'][i,j]),
                 'ordinary_E_rate_norm':float(fnorm(r['aspl'])[i,j]),
                 'horizontal_E_rate_norm':float(fnorm(r['dc'])[i,j]),
                 'connection_commutator_norm':float(fnorm(r['motion'])[i,j]),
                 'radial_rate':float(r['radial'][i,j]),
                 'orientation_rate_ordinary':float(r['ang_raw'][i,j]),
                 'orientation_rate_horizontal':float(r['ang_cov'][i,j]),
                 'radial_invariance_abs':float(abs(r['radial_cov'][i,j]-r['radial'][i,j])),
                 'ordinary_E_angle_from_start_deg':float(r['angle'][i,j]),
                 'time_A_parent_vs_spline_frob':float(fnorm(A-r['aspl'])[i,j]),
                 'E_rate_spline_vs_5pt_frob':float(fnorm(r['dc']-r['dc5'])[i,j]),
                 'Pdot_connection_residual_frob':float(fnorm(r['pd']-comm(r['k'],P))[i,j])})
        # Two original endpoints plus the midpoint are transported independently.
        for offset in (0.,.5,1.):
            i=int(np.argmin(abs(offsets-offset)))
            Et,U,d=parallel_centerline(xi,P[i],E[i],r['k'][i])
            if not d['success']:raise RuntimeError('Failed canonical transport')
            transport[f'{seed}_offset_{offset:g}']=d
            for j,tm in enumerate(xi):
                a=E[i,0]/fnorm(E[i,0]);b=E[i,j]/fnorm(E[i,j]);c=Et[j]/fnorm(Et[j]);
                raw=float(np.degrees(2*np.arctan2(fnorm(a-b),fnorm(a+b))))
                corr=float(np.degrees(2*np.arctan2(fnorm(a-c),fnorm(a+c))))
                angle_rows.append({'seed_family':seed,'offset_units':offset,'xi':float(tm),
                  'raw_angle_deg':raw,'horizontal_corrected_angle_deg':corr,
                  'orthogonality_error':float(fnorm(U[j].T@U[j]-np.eye(10)))})
            if offset==.5:
                archive['E_'+seed]=E[i]
                archive['E_horizontal_'+seed]=Et
                archive['K_'+seed]=r['k'][i]
                archive['D_horizontal_'+seed]=r['dc'][i]
                archive['U_'+seed]=U
                gauge_rows.extend([{'seed_family':seed,**v} for v in coordinate_gauge_controls(
                    xi,E[i],r['aspl'][i],r['k'][i],[0,15,35,55,78])])
        print('v18.50y',seed,'centerline raw/corrected angle:',
              transport[f'{seed}_offset_0.5']['raw_angle_final_deg'],
              transport[f'{seed}_offset_0.5']['horizontal_transport_corrected_angle_final_deg'],flush=True)
    df=pd.DataFrame(rows);angles=pd.DataFrame(angle_rows);gauge=pd.DataFrame(gauge_rows)
    df.to_csv(out/'covariant_kappa_sensitivity_ledger.csv',index=False,float_format='%.17g')
    angles.to_csv(out/'transported_sensitivity_angles.csv',index=False,float_format='%.17g')
    gauge.to_csv(out/'observer_coordinate_gauge_controls.csv',index=False,float_format='%.17g')
    np.savez_compressed(out/'transported_sensitivity_centerline_tensors.npz',xi=xi,**archive)
    plots(df,angles,out)
    if gauge.relative_covariance_residual.max()>1e-11 or gauge.metric_norm_relative_residual.max()>1e-11:
        raise RuntimeError('Covariance check failed')
    if max(method[s]['algebraic']['radial_rate_invariance_max_abs'] for s in method)>1e-9:
        raise RuntimeError('Radial invariant check failed')
    report={'version':'v18.50y','title':'Covariant Sensitivity Transport & Time-Derivative Attribution Audit',
        'classification':'CANONICAL_OBSERVER_PROJECTOR_TRANSPORT_DIAGNOSTIC_NOT_MODEL_PRIVILEGED_MATERIAL_CONNECTION_OR_ACTIVATION_CERTIFICATE',
        'parent_authentication':auth,'inputs':{'x_projector_rows':3476,'new_physical_10d_ivps':0,'new_geometric_frame_ivps':6,
         'kappa_points':22,'evolution_points':79,'seed_families':['original','autonomous'],
         'horizontal_connection':'K=[Pdot,P], with Pdot from cubic spline on inherited ξ grid',
         'covariant_sensitivity_rate':'DξE=Eprime-[K,E], Eprime from cubic spline on inherited ξ grid',
         'five_node_time_derivative':'independent nonuniform local polynomial comparison',
         'metric':'Frobenius in common inherited 10D chart, transported under changes of coordinates'},
        'derivative_and_geometry_checks':method,'transported_angles':transport,
        'gauge_checks':{'max_covariance_relative_residual':float(gauge.relative_covariance_residual.max()),
         'max_transported_metric_relative_residual':float(gauge.metric_norm_relative_residual.max()),
         'max_condition_of_gauge':float(gauge.gauge_condition.max()),
         'max_magnitude_error_when_frame_velocity_omitted':float(abs(gauge.if_ignore_frame_W_norm_error).max())},
        'limitations':['No new 10D physical IVPs. All tensor fields come from authenticated parent v18.50x.',
          'The canonical horizontal projector connection is induced by the time-dependent observed kernel P, NOT independently inferred from the original 10D physical tangent generator J.',
          'The choice of an orthogonal projector and Frobenius reference metric is observer-dependent and is not a certified material metric.',
          'Under a time-dependent coordinate change, the full connection must be transformed with its W=Sprime Sinverse term; recomputing canonical [Pprime,P] alone is insufficient in general.',
          'The gauge control is for kappa-independent coordinate changes. Kappa-dependent coordinate transformations require a separate parameter connection.',
          'Cubic spline vs five-node derivative differences are numerical diagnostics, not interval-certified errors.',
          'Two seeds carry separately defined turning-relative xi clocks; their near agreement does not establish a common material clock.',
          'Finite-time tensor rotation and corrected tensor rotation are not proof of a material torsional flip or narrow-band activation.'],
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
           'scipy':__import__('scipy').__version__,'pandas':pd.__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print('v18.50y COMPLETED',json.dumps({'parent_sources':auth['x_sources'],'rows':len(df),
         'gauge_rel_max':report['gauge_checks']['max_covariance_relative_residual'],
         'transport_center_original':transport['original_offset_0.5']},indent=2),flush=True)

if __name__=='__main__':run()
