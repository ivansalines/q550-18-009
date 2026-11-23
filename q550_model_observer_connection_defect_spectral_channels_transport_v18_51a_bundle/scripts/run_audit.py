#!/usr/bin/env python3
"""v18.51a: gauge-free spectral channel projectors of the z connection defect.

This audit analyzes authenticated v18.50z model outputs, not fresh Q550 IVPs.
All coordinates and norms use the parent's common Euclidean 10D chart.
The two dominant skew pairs are tracked by rank-2 *projectors*, not SVD signs.
The tiny third pair is not interpreted as a physical or robust plane.
"""
from __future__ import annotations
import io, json, hashlib, platform, zipfile, sys
from pathlib import Path
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
PARENT_ROOT='q550_model_generated_tangent_transport_canonical_observer_connection_v18_50z_bundle'
PARENT=ROOT/'inputs'/(PARENT_ROOT+'_server_sendback.zip')
OUT=ROOT/'results'
OUT.mkdir(exist_ok=True)


def hbytes(b:bytes)->str:
    return hashlib.sha256(b).hexdigest()


def verify_parent():
    # Read the authenticated server sendback without extracting the 49 ZIP ancestors.
    with zipfile.ZipFile(PARENT) as z:
        bad=z.testzip()
        if bad: raise RuntimeError('Parent ZIP CRC failure: '+bad)
        m=json.loads(z.read(PARENT_ROOT+'/SOURCE_MANIFEST.json'))
        om=json.loads(z.read(PARENT_ROOT+'/SHA256SUMS_OUTPUT.json'))
        if m['root']!=PARENT_ROOT or om['root']!=PARENT_ROOT:
            raise RuntimeError('Unexpected parent root')
        if m.get('version')!='v18.50z' or om.get('version')!='v18.50z':
            raise RuntimeError('Incorrect parent version')
        listed=set(m['files'])|set(om['file_sha256'])|{'SOURCE_MANIFEST.json','SHA256SUMS_OUTPUT.json'}
        actual={n[len(PARENT_ROOT)+1:] for n in z.namelist() if n.startswith(PARENT_ROOT+'/') and not n.endswith('/')}
        if actual!=listed:raise RuntimeError('Unexpected parent membership: '+str(actual^listed))
        for rel,expected in {**m['files'],**om['file_sha256']}.items():
            if hbytes(z.read(PARENT_ROOT+'/'+rel)) != expected:
                raise RuntimeError('Parent hash mismatch: '+rel)
        d=np.load(io.BytesIO(z.read(PARENT_ROOT+'/results/model_vs_canonical_centerline_tensors.npz')))
        tensors={name:np.array(d[name],copy=True) for name in d.files}
        report=json.loads(z.read(PARENT_ROOT+'/results/report.json'))
    if report['version']!='v18.50z':raise RuntimeError('Wrong report version')
    for seed in ('original','autonomous'):
        if not report['model_replay'][seed]['physical_ivp_success']:
            raise RuntimeError('Parent physical integration was incomplete')
    return tensors, {'source_files':len(m['files']),'result_files':len(om['file_sha256']),
        'parent_zip_sha256':hbytes(PARENT.read_bytes()), 'parent_version':'v18.50z'}


def fn(a):return float(np.linalg.norm(a,ord='fro'))


def spectral_channels(k):
    """Two stable 2D spectral projectors of a real skew 10x10 generator."""
    k=np.asarray(k,dtype=float)
    skew_err=fn(k+k.T)/max(fn(k),1e-16)
    if skew_err>2e-12:raise RuntimeError('Defect is not skew '+str(skew_err))
    U,s,VT=np.linalg.svd(k,full_matrices=True)
    q1=U[:,:2]@U[:,:2].T
    q2=U[:,2:4]@U[:,2:4].T
    intensities=np.array([np.mean(s[0:2]),np.mean(s[2:4]),np.mean(s[4:6])])
    if (intensities[0]-intensities[1])<0.5 or intensities[1]<0.1:
        raise RuntimeError('Dominant pair spectral gap closed; track clusters instead')
    # Skew singular pairs have duplicated values; our projectors do not depend
    # on the arbitrary SVD vectors/signs within each two-dimensional channel.
    pair_res=float(max(abs(s[0]-s[1]),abs(s[2]-s[3]))/max(s[0],1))
    recon=fn(k-(q1+q2)@k@(q1+q2))/max(fn(k),1e-16)
    return intensities,np.stack((q1,q2)),skew_err,pair_res,recon


def angle_from_projectors(p0,q):
    # Stable principal-angle measurement: sin(theta) from an orthogonal lift.
    vals,vec=np.linalg.eigh(q)
    lift=vec[:,-2:]
    sinmax=np.linalg.norm((np.eye(q.shape[0])-p0)@lift,2)
    return float(np.degrees(np.arcsin(np.clip(sinmax,0,1))))


def analyze_one(seed,xi,src):
    A=np.asarray(src['K_model_'+seed],float)
    B=np.asarray(src['K_canonical_'+seed],float)
    if A.shape!=(len(xi),10,10) or B.shape!=A.shape:
        raise RuntimeError('Unexpected original tensors shape')
    sk=[];proj=[];skewres=[];pairres=[];recon=[]
    for a,b in zip(A,B):
        s,p,e,g,r=spectral_channels(a-b)
        sk.append(s);proj.append(p);skewres.append(e);pairres.append(g);recon.append(r)
    sk=np.asarray(sk);proj=np.asarray(proj)
    q1,q2=proj[:,0],proj[:,1]
    # Independent diagnostics of time differentiation on the irregular xi grid.
    dq1=CubicSpline(xi,q1,axis=0).derivative()(xi)
    dq2=CubicSpline(xi,q2,axis=0).derivative()(xi)
    fd1=np.gradient(q1,xi,axis=0,edge_order=2)
    fd2=np.gradient(q2,xi,axis=0,edge_order=2)
    pi=np.eye(10)
    rows=[]
    for j,t in enumerate(xi):
        s1,s2,s3=sk[j]
        strength=s1*s1+s2*s2+s3*s3
        mix12=fn(q2[j]@dq1[j]@q1[j])
        mix21=fn(q1[j]@dq2[j]@q2[j])
        out1=fn((pi-q1[j])@dq1[j]@q1[j])
        out2=fn((pi-q2[j])@dq2[j]@q2[j])
        coupling_fraction=mix12/out1 if out1>1e-12 else float('nan')
        rows.append({
            'seed_family':seed,'xi':float(t), 'sigma_pair_1':float(s1),
            'sigma_pair_2':float(s2), 'sigma_pair_3_near_floor':float(s3),
            'sigma_gap_1_2':float(s1-s2),'sigma_ratio_1_2':float(s1/s2),
            'quadratic_share_pair_1':float(s1*s1/strength),
            'quadratic_share_pair_2':float(s2*s2/strength),
            'angle_pair_1_from_start_deg':angle_from_projectors(q1[0],q1[j]),
            'angle_pair_2_from_start_deg':angle_from_projectors(q2[0],q2[j]),
            'rate_pair1_out_of_plane':out1,'rate_pair2_out_of_plane':out2,
            'rate_pair1_into_pair2':mix12,'rate_pair2_into_pair1':mix21,
            'pair1_coupling_fraction_of_out_rate':coupling_fraction,
            'derivative_spline_fd_rel_pair1':fn(dq1[j]-fd1[j])/max(1,fn(dq1[j])),
            'derivative_spline_fd_rel_pair2':fn(dq2[j]-fd2[j])/max(1,fn(dq2[j])),
            'max_skew_symmetry_relative':skewres[j],
            'pair_degeneracy_relative':pairres[j],
            'rank4_spectral_reconstruction_residual':recon[j],
            'projector_orthogonality_residual':fn(q1[j]@q2[j]),
            'projector_idempotence_residual':max(fn(q1[j]@q1[j]-q1[j]),fn(q2[j]@q2[j]-q2[j])),
        })
    return rows,proj,sk


def write_csv(path,rows):
    import csv
    with open(path,'w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]))
        writer.writeheader();writer.writerows(rows)


def render(allrows):
    # Use provided normal Matplotlib color cycle (not a physical color encoding).
    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,dat in allrows.items():
        x=np.array([r['xi'] for r in dat])
        axs[0].plot(x,[r['sigma_pair_1'] for r in dat],label=f'{seed} · pair 1')
        axs[0].plot(x,[r['sigma_pair_2'] for r in dat],label=f'{seed} · pair 2',linestyle='--')
        axs[1].plot(x,100*np.array([r['quadratic_share_pair_1'] for r in dat]),label=seed)
    axs[0].set_ylabel('Singular intensity of skew defect');axs[0].legend(fontsize=9,ncol=2)
    axs[1].set_ylabel('Pair 1 / total squared norm (%)');axs[1].set_xlabel('Evolution coordinate ξ')
    axs[1].legend();fig.suptitle('v18.51a · Two dominant spectral channels (no handover)')
    fig.tight_layout();fig.savefig(OUT/'spectral_channel_strengths.png',dpi=160);plt.close(fig)

    fig,axs=plt.subplots(2,1,figsize=(10,8),sharex=True)
    for seed,dat in allrows.items():
        x=np.array([r['xi'] for r in dat]);axs[0].plot(x,[r['angle_pair_1_from_start_deg'] for r in dat],label=f'{seed} · pair 1')
        axs[0].plot(x,[r['angle_pair_2_from_start_deg'] for r in dat],linestyle='--',label=f'{seed} · pair 2')
        axs[1].plot(x,100*np.array([r['pair1_coupling_fraction_of_out_rate'] for r in dat]),label=seed)
    axs[0].set_ylabel('Largest principal angle from initial plane (°)');axs[0].legend(fontsize=9,ncol=2)
    axs[1].set_ylabel('Pair1 out-of-plane rate into pair2 (%)');axs[1].set_xlabel('Evolution coordinate ξ');axs[1].legend()
    fig.suptitle('v18.51a · Spectral-plane transport and inter-channel coupling')
    fig.tight_layout();fig.savefig(OUT/'spectral_plane_rotation_coupling.png',dpi=160);plt.close(fig)

    fig,axs=plt.subplots(1,2,figsize=(12,4))
    for seed,dat in allrows.items():
        x=np.array([r['xi'] for r in dat]);
        axs[0].plot(x,[r['rate_pair1_into_pair2'] for r in dat],label=seed)
        axs[1].semilogy(x,[r['sigma_pair_3_near_floor'] for r in dat],label=seed)
    axs[0].set_title('Inter-channel coupling rate (matrix norm)');axs[0].set_ylabel('||Q₂ Q₁\u2032 Q₁||F');axs[1].set_title('Small third pair: numerical-floor diagnostic')
    axs[1].set_ylabel('Third pair singular intensity');
    for ax in axs:ax.set_xlabel('ξ');ax.legend()
    fig.tight_layout();fig.savefig(OUT/'coupling_and_near_floor.png',dpi=160);plt.close(fig)


def main():
    tensors,parent=verify_parent()
    xi=np.asarray(tensors['xi'],float)
    if len(xi)!=79 or not np.all(np.diff(xi)>0) or abs(xi[0])>1e-14 or abs(xi[-1]-0.05)>1e-14:
        raise RuntimeError('Unexpected parent grid')
    byseed={};planes={};sing={}
    for seed in ('original','autonomous'):
        rows,P,sk=analyze_one(seed,xi,tensors)
        byseed[seed]=rows;planes[seed]=P;sing[seed]=sk
    allrows=byseed['original']+byseed['autonomous']
    write_csv(OUT/'spectral_channel_phase_ledger.csv',allrows)
    summary=[];per={}
    for seed,rows in byseed.items():
        first=rows[0];last=rows[-1]
        data={
            'seed_family':seed,'samples':len(rows),
            'sigma_pair1_start':first['sigma_pair_1'],'sigma_pair1_end':last['sigma_pair_1'],
            'sigma_pair2_start':first['sigma_pair_2'],'sigma_pair2_end':last['sigma_pair_2'],
            'share_pair1_start':first['quadratic_share_pair_1'],'share_pair1_end':last['quadratic_share_pair_1'],
            'pair1_endpoint_max_angle_deg':last['angle_pair_1_from_start_deg'],
            'pair2_endpoint_max_angle_deg':last['angle_pair_2_from_start_deg'],
            'pair1_coupling_fraction_start':first['pair1_coupling_fraction_of_out_rate'],
            'pair1_coupling_fraction_end':last['pair1_coupling_fraction_of_out_rate'],
            'max_sigma3':max(r['sigma_pair_3_near_floor'] for r in rows),
            'max_spline_fd_relative_error':max(max(r['derivative_spline_fd_rel_pair1'],r['derivative_spline_fd_rel_pair2']) for r in rows),
            'min_gap_pair1_pair2':min(r['sigma_gap_1_2'] for r in rows),
            'pair1_monotone_increasing_samples':all(rows[i+1]['sigma_pair_1']>rows[i]['sigma_pair_1'] for i in range(len(rows)-1)),
            'pair2_monotone_decreasing_samples':all(rows[i+1]['sigma_pair_2']<rows[i]['sigma_pair_2'] for i in range(len(rows)-1)),
            'max_projector_idempotence_residual':max(r['projector_idempotence_residual'] for r in rows),
            'max_pair_projector_orthogonality_residual':max(r['projector_orthogonality_residual'] for r in rows),
            'max_skew_symmetry_residual':max(r['max_skew_symmetry_relative'] for r in rows),
            'max_pair_degeneracy_residual':max(r['pair_degeneracy_relative'] for r in rows),
            'max_rank4_reconstruction_residual':max(r['rank4_spectral_reconstruction_residual'] for r in rows),
        }
        per[seed]=data;summary.append(data)
    write_csv(OUT/'spectral_channel_summary.csv',summary)
    render(byseed)
    # The third singular subspace is deliberately omitted due to numerical instability.
    np.savez_compressed(OUT/'dominant_spectral_channel_projectors.npz',xi=xi,
        projector_pair1_original=planes['original'][:,0],projector_pair2_original=planes['original'][:,1],
        projector_pair1_autonomous=planes['autonomous'][:,0],projector_pair2_autonomous=planes['autonomous'][:,1],
        skew_singular_pair_strengths_original=sing['original'],
        skew_singular_pair_strengths_autonomous=sing['autonomous'])
    tests={
        'all_spectral_gaps_positive':all(d['min_gap_pair1_pair2']>1 for d in per.values()),
        'first_pair_stronger_at_all_sections':all(d['pair1_monotone_increasing_samples'] for d in per.values()),
        'second_pair_weakens_at_all_sections':all(d['pair2_monotone_decreasing_samples'] for d in per.values()),
        'rank2_projectors_well_formed':all(d['max_projector_idempotence_residual']<1e-12 and d['max_pair_projector_orthogonality_residual']<1e-12 for d in per.values()),
        'stable_skew_singular_pairing':all(d['max_skew_symmetry_residual']<1e-12 and d['max_pair_degeneracy_residual']<1e-12 for d in per.values()),
        'rank4_explains_reported_defect':all(d['max_rank4_reconstruction_residual']<1e-7 for d in per.values()),
        'derivative_discretizations_agree':all(d['max_spline_fd_relative_error']<1e-3 for d in per.values()),
        'weak_third_pair_not_resolved':all(d['max_sigma3']<1e-6 for d in per.values()),
        'all_samples_present':len(allrows)==158,
    }
    if not all(tests.values()):raise RuntimeError('Scientific checks failed: '+str(tests))
    report={'version':'v18.51a','title':'Model–Observer Connection Defect: Spectral Channels & Transport Audit',
      'classification':'AUTHENTICATED_SPECTRAL_PROJECTOR_CHANNEL_DIAGNOSTIC_NOT_PHYSICAL_MODE_OR_ENERGY_TRANSFER_CERTIFICATE',
      'parent':parent,'samples':len(allrows),'branches':2,'shared_midpoint_kappa':0.1666331385421536,
      'family_interpretation':'Two distinct natural-seed preparations at the same midpoint κ0, NOT two simultaneously evolving κ0 parameters.',
      'results':per,'checks':tests,
      'definitions':{
        'defect':'W=K_model_crossblock-K_canonical (skew; 10D shared Euclidean chart)',
        'channel_projectors':'Q_i=U_i U_i^T for singular pairs i=1,2 of W (rank-2, sign/gauge insensitive)',
        'coupling_rate':'||Q2 (dQ1/dxi) Q1||_F',
        'fraction':'coupling rate divided by ||(I-Q1)(dQ1/dxi)Q1||_F',
        'channel_strength':'duplicated singular intensities σ1,σ2 of skew W',
        'quadratic_share':'σ_i²/(σ1²+σ2²+σ3²); relative squared Frobenius weight, NOT energy',
        'third_channel':'not identified; near numerical floor and is not tracked as a stable plane'},
      'limitations':[
        'This is a post-processing audit of authenticated v18.50z tensors; there are NO new Q550 integrations.',
        'The K_model comparator is the skew offblock reduction of J10, NOT full nonorthogonal tangent flow.',
        'All Frobenius norms and spectral planes use the inherited 10D Euclidean chart; no physical kinetic metric is established.',
        'Differentiation uses 79 nonuniform phases; CubicSpline vs nonuniform three-point gradient is a numerical check, not an interval error bound.',
        'The tiny third pair is numerically delicate, so its plane orientation is not interpreted.',
        'Changing the observer/metric can change spectral decomposition. Do not infer material modes, torsional flip, polymer physics, physical band activation, or energy transfer.'
        ],
      'environment':{'python':platform.python_version(),'numpy':np.__version__}}
    (OUT/'report.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print('v18.51a COMPLETED',json.dumps({'source_files':parent['source_files'],'result_files':parent['result_files'], 'rows':len(allrows),'checks':sum(tests.values()),'original':per['original'],'autonomous':per['autonomous']},indent=2))
    return report

if __name__=='__main__':main()
