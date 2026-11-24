#!/usr/bin/env python3
"""v18.50x: anchor-free projector-derivative field and sensitivity transport.

Replays 44 authentic fixed-seed Q550 trajectories, using inherited model, fields
and time/parameter grid. Source genealogies are checked cryptographically.
Only the compiled 10x10 projector *matrices*, not anchor-to-reference norms,
are differentiated to obtain E=∂κP and A=∂ξE.

Finite differences do not certify continuum κ or ξ derivatives, nor a material
activation. Original/autonomous natural seeds have distinct turning-event clocks.
"""
from __future__ import annotations
import argparse,hashlib,importlib.util,io,json,platform,sys,tempfile,zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
ROOT=Path(__file__).resolve().parents[1]
W='q550_moving_equidistance_gate_two_reference_transport_v18_50w_bundle'
V='q550_long_horizon_kappa_response_activation_threshold_v18_50v_bundle'
U='q550_kappa_narrow_band_common_seed_dynamic_scan_v18_50u_bundle'
PARENT=ROOT/'inputs'/(W+'_server_sendback.zip')

def sha(b):return hashlib.sha256(b).hexdigest()
def verify_zip(z,name):
    bad=z.testzip()
    if bad is not None:raise RuntimeError(f'{name} ZIP CRC: {bad}')
    sm=json.loads(z.read(name+'/SOURCE_MANIFEST.json'))
    om=json.loads(z.read(name+'/SHA256SUMS_OUTPUT.json'))
    if sm['root']!=name or om['root']!=name:raise RuntimeError('Parent root mismatch')
    for doc,key in ((sm,'files'),(om,'file_sha256')):
        for rel,h in doc[key].items():
            if sha(z.read(name+'/'+rel))!=h:raise RuntimeError('Parent digest mismatch: '+rel)
    return {'sources':len(sm['files']),'results':len(om['file_sha256'])}

def authenticate_and_stage(temp):
    with zipfile.ZipFile(PARENT) as w:
        w_info=verify_zip(w,W)
        wr=json.loads(w.read(W+'/results/report.json'))
        if wr['version']!='v18.50w':raise RuntimeError('Not parent w')
        vb=w.read(W+'/inputs/'+V+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(vb)) as z:
        v_info=verify_zip(z,V)
        vr=json.loads(z.read(V+'/results/report.json'))
        vcode=z.read(V+'/scripts/run_audit.py')
        ub=z.read(V+'/inputs/'+U+'_server_sendback.zip')
    if vr['version']!='v18.50v' or vr['design']['new_10d_driven_ivps']!=44:raise RuntimeError('Not authentic v')
    stage=temp/V
    (stage/'scripts').mkdir(parents=True)
    (stage/'inputs').mkdir(parents=True)
    (stage/'scripts/run_audit.py').write_bytes(vcode)
    (stage/'inputs'/(U+'_server_sendback.zip')).write_bytes(ub)
    spec=importlib.util.spec_from_file_location('v18_50x_parent_v',stage/'scripts/run_audit.py')
    v=importlib.util.module_from_spec(spec);sys.modules[spec.name]=v
    assert spec.loader is not None
    spec.loader.exec_module(v)
    u_info,ur,ucode,tblob=v.authenticate_u()
    engine_parts=v.stage_model(temp,ucode,tblob)
    if abs(float(ur['kappa']['delta'])-float(vr['kappa']['delta']))>1e-14:raise RuntimeError('κ mismatch')
    auth={'w':w_info,'v':v_info,'u':u_info,
          'w_zip_sha256':sha(PARENT.read_bytes()),'v_zip_sha256':sha(vb)}
    return v,vr,engine_parts,auth

def finite_weights(x0,xx):
    # Nonuniform finite differences, accurate for monomials through degree n-1.
    xx=np.asarray(xx,float)
    scale=float(np.max(np.abs(xx-x0)))
    if scale<=0:raise ValueError('Degenerate nodes')
    z=(xx-x0)/scale
    vand=np.stack([z**j for j in range(len(xx))],axis=0)
    target=np.zeros(len(xx));target[1]=1/scale
    return np.linalg.solve(vand,target)

def kappa_derivative(P,kappas,stencil=5):
    n=len(kappas)
    if n<stencil:raise ValueError('not enough kappa samples')
    output=np.empty_like(P)
    for i in range(n):
        lo=max(0,min(n-stencil,i-stencil//2))
        ids=np.arange(lo,lo+stencil)
        weights=finite_weights(kappas[i],kappas[ids])
        output[i]=np.einsum('a,atij->tij',weights,P[ids],optimize=True)
    return output

def fnorm(x):return np.linalg.norm(x,axis=(-2,-1))
def inner(a,b):return np.einsum('...ij,...ij->...',a,b,optimize=True)
def metrics(P,kappas,xis):
    # Five- vs three-node κ derivative: stable up to finite-grid accuracy.
    E5=kappa_derivative(P,kappas,5)
    E3=kappa_derivative(P,kappas,3)
    A=np.gradient(E5,xis,axis=1,edge_order=2)
    A_spline=CubicSpline(xis,E5,axis=1).derivative()(xis)
    EE=inner(E5,E5)
    mag=np.sqrt(np.maximum(EE,0))
    aa=inner(E5,A)
    radial=np.divide(aa,mag,out=np.full_like(aa,np.nan),where=mag>1e-15)
    radial_coeff=np.divide(aa,EE,out=np.zeros_like(aa),where=EE>1e-26)
    transverse=A-radial_coeff[...,None,None]*E5
    transverse_speed=fnorm(transverse)
    omega=np.divide(transverse_speed,mag,out=np.full_like(mag,np.nan),where=mag>1e-15)
    total_speed=fnorm(A)
    P_tangent=fnorm(P@E5@P)
    eye=np.eye(P.shape[-1])[None,None,:,:]
    Pcom=eye-P
    C_tangent=fnorm(Pcom@E5@Pcom)
    stencil_rel=np.divide(fnorm(E5-E3),np.maximum(mag,1e-20))
    time_rel=np.divide(fnorm(A-A_spline),np.maximum(total_speed,1e-20))
    local_curvature=kappa_derivative(E5,kappas,3)
    # κ orientation change, in the same fixed Frobenius chart as ξ orientation.
    kappar=inner(E5,local_curvature)/np.maximum(EE,1e-26)
    kappa_turn=fnorm(local_curvature-kappar[...,None,None]*E5)/np.maximum(mag,1e-20)
    start=E5[:,0];unit0=start/np.maximum(fnorm(start)[:,None,None],1e-30)
    unit=E5/np.maximum(mag[...,None,None],1e-30)
    c=np.clip(inner(unit,unit0[:,None,:,:]),-1,1)
    # atan2 is stable near zero angles, unlike direct arccos(c).
    s=np.sqrt(np.maximum(0,1-c*c))
    angles=np.rad2deg(np.arctan2(s,c))
    return {'E':E5,'A':A,'norm_E':mag,'norm_A':total_speed,
            'radial_rate':radial,'transverse_rate':transverse_speed,
            'orientation_rate':omega,'kappa_orientation_rate':kappa_turn,
            'angle_from_initial_deg':angles,
            'projector_idempotency':fnorm(P@P-P),
            'projector_symmetry':fnorm(P-np.swapaxes(P,-1,-2)),
            'off_tangent_P':P_tangent,'off_tangent_Q':C_tangent,
            'stencil_3_vs_5_relative':stencil_rel,
            'time_gradient_vs_spline_relative':time_rel}

def candidate_screen(arr,offsets,xis):
    """Exploratory interior κ maxima of sensitivity orientation rate.

    Boundary maxima aren't qualifying moving ridges. A candidate needs a peak
    above both OUTSIDE controls by >=5%, plus persistence at >=3 consecutive
    sampled times and agreement between BOTH fixed-seed trajectories.
    These thresholds are exploratory, not statistically calibrated discoveries.
    """
    inside=np.where((offsets>0)&(offsets<1))[0]
    outside=np.where((offsets<=-0.5)|(offsets>=1.5))[0]
    all_marks=[];result={}
    for seed in arr:
        rho=arr[seed]['orientation_rate']
        marks=[]
        for j,xi in enumerate(xis):
            valid=[]
            for i in inside:
                if i>0 and i<len(offsets)-1 and rho[i,j]>rho[i-1,j] and rho[i,j]>rho[i+1,j]:
                    ref=max(np.max(rho[outside,j]),1e-25)
                    ratio=float(rho[i,j]/ref)
                    if ratio>=1.05:valid.append((i,ratio))
            if valid:
                k,ratio=max(valid,key=lambda z:z[1]);marker=float(offsets[k]);flag=1
            else:
                k=-1;ratio=float('nan');marker=float('nan');flag=0
            marks.append(flag)
            all_marks.append({'seed_family':seed,'xi':float(xi),'ridge_detected':flag,
                              'max_offset':marker,'peak_to_outer_ratio':ratio})
        x=np.asarray(marks,int)
        triple=int(np.sum((x[:-2]==1)&(x[1:-1]==1)&(x[2:]==1)))
        result[seed]={'qualified_sections':int(np.sum(x)),'consecutive_triplets':triple}
    return pd.DataFrame(all_marks),result

def make_plots(ledger,report,root):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    for field,name,label in [('norm_E','projector_parameter_sensitivity','||∂κP||F'),
                             ('orientation_rate','moving_sensitivity_orientation','||A_perp||F / ||E||F')]:
        fig,axes=plt.subplots(1,2,figsize=(12.3,4.7),sharey=True)
        for ax,seed in zip(axes,('original','autonomous')):
            df=ledger[ledger.seed_family==seed]
            table=df.pivot(index='xi',columns='offset_units',values=field)
            x=table.columns.to_numpy(float);t=table.index.to_numpy(float)
            dat=table.to_numpy(float)
            im=ax.pcolormesh(x,t,dat,shading='auto',cmap='viridis')
            ax.axvspan(0,1,alpha=.12,color='white')
            ax.set(xlabel='Normalized κ coordinate (historical interval 0..1)',ylabel='Turn-relative evolution ξ',title=seed)
            fig.colorbar(im,ax=ax,label=label)
        fig.suptitle('v18.50x | Anchor-free '+label)
        fig.tight_layout();fig.savefig(root/(name+'.png'),dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12.3,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        df=ledger[(ledger.seed_family==seed)&(np.isclose(ledger.offset_units,.5,atol=1e-12))].sort_values('xi')
        ax.plot(df.xi,df.radial_rate,label='radial d||E||/dξ')
        ax.plot(df.xi,df.transverse_rate,label='direction-changing ||Aperp||')
        ax.plot(df.xi,df.norm_A,label='total ||A||',ls='--',alpha=.7)
        ax.set(xlabel='Turn-relative evolution ξ',ylabel='Derivative per unit ξ',title=seed)
        ax.grid(alpha=.25);ax.legend(fontsize=8)
    fig.suptitle('v18.50x | Growth of sensitivity versus change of its direction')
    fig.tight_layout();fig.savefig(root/'centerline_radial_transverse_rates.png',dpi=145);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9.8,5.1))
    for seed in ('original','autonomous'):
        df=ledger[(ledger.seed_family==seed)&(np.isclose(ledger.offset_units,.5,atol=1e-12))].sort_values('xi')
        ax.plot(df.xi,df.angle_from_initial_deg,label=seed)
    ax.set(xlabel='Turn-relative evolution ξ',ylabel='Angle of ∂κP from initial tensor direction (degrees)',
           title='v18.50x | Direction changes without anchored V zeros')
    ax.grid(alpha=.25);ax.legend();fig.tight_layout()
    fig.savefig(root/'sensitivity_tensor_direction_angle.png',dpi=145);plt.close(fig)
    fig,axes=plt.subplots(1,2,figsize=(12.3,4.7))
    for ax,seed in zip(axes,('original','autonomous')):
        df=ledger[(ledger.seed_family==seed)&(np.isclose(ledger.offset_units,.5,atol=1e-12))].sort_values('xi')
        ax.plot(df.xi,df.stencil_3_vs_5_relative,label='κ 3- vs 5-node')
        ax.plot(df.xi,df.time_gradient_vs_spline_relative,label='ξ gradient vs cubic spline')
        ax.set(xlabel='Turn-relative evolution ξ',ylabel='Relative diagnostic difference',title=seed)
        ax.set_yscale('log');ax.grid(alpha=.2);ax.legend(fontsize=8)
    fig.suptitle('v18.50x | Numerical conditioning checks for derivative field')
    fig.tight_layout();fig.savefig(root/'differentiation_method_controls.png',dpi=145);plt.close(fig)

def run(a):
    out=ROOT/'results';out.mkdir(exist_ok=True)
    ledger=[];summaries={};diagnostics={};integrations=[];tensor_data={}
    with tempfile.TemporaryDirectory(prefix='v18_50x_ancestry_') as td:
        v,vr,parts,auth=authenticate_and_stage(Path(td))
        t,q,p,o,engine,unit,drpt,creport,tinfo=parts
        co=p.make_context(o,'original',engine,unit,drpt,creport)
        ca=p.make_context(o,'autonomous',engine,unit,drpt,creport)
        contexts={'original':co,'autonomous':ca}
        shared_scale=np.maximum.reduce((np.ones(10),co['scale'],ca['scale']))
        weights=np.asarray(drpt['common_metric_scale_4d'],float)
        offsets=np.asarray(v.OFFSETS,float)
        kappas=float(vr['kappa']['autonomous'])+offsets*float(vr['kappa']['delta'])
        xis=v.phase_grid(a.end)
        if len(xis)!=79 or len(kappas)!=22:raise RuntimeError('Expected authentic 22x79 scan')
        for seed,ctx in contexts.items():
            print('REPLAY START',seed,flush=True)
            replay=v.measures_for_seed(t,q,engine,ctx,kappas,xis,shared_scale,weights,a.rtol,a.atol,a.max_step)
            integrations+=replay['integrations']
            m=metrics(replay['P'],kappas,xis)
            summaries[seed]=m
            tensor_data[seed]={'P':replay['P'].copy(),'E':m['E'].copy(),'A':m['A'].copy()}
            gain_direct=v.sensitivity_fields(replay,kappas,shared_scale)['projector_gain']
            # Check our 3-pt derivative implements the same formula as parent v.
            same=float(np.max(np.abs(fnorm(kappa_derivative(replay['P'],kappas,3))-gain_direct)))
            diagnostics[seed]={'max_3_point_vs_parent_v_gradient':same,
                'max_projector_idempotency':float(np.max(m['projector_idempotency'])),
                'max_projector_symmetry':float(np.max(m['projector_symmetry'])),
                'max_relative_tangency_P':float(np.max(m['off_tangent_P']/np.maximum(m['norm_E'],1e-20))),
                'max_relative_tangency_Q':float(np.max(m['off_tangent_Q']/np.maximum(m['norm_E'],1e-20))),
                'max_kappa_stencil_relative_in_band':float(np.max(m['stencil_3_vs_5_relative'][(offsets>=0)&(offsets<=1)])),
                'max_time_stencil_relative_in_band':float(np.max(m['time_gradient_vs_spline_relative'][(offsets>=0)&(offsets<=1)])),
                'min_E_norm':float(np.min(m['norm_E'])), 'max_E_norm':float(np.max(m['norm_E']))}
            print('FIELD COMPLETE',seed,diagnostics[seed],flush=True)
            for i,k in enumerate(kappas):
                for j,xi in enumerate(xis):
                    row={'seed_family':seed,'kappa':float(k),'offset_units':float(offsets[i]),'xi':float(xi)}
                    for name,value in m.items():
                        if name in ('E','A'):continue
                        row[name]=float(value[i,j])
                    ledger.append(row)
    # Preserve full 10x10 matrix data for future independent tensor analysis.
    # This avoids re-staging a multi-gigabyte historical runtime just to inspect
    # a direction, rather than its scalar norm. Source reconstruction remains
    # available in this bundle when a fresh physical replay is needed.
    np.savez_compressed(out/'full_projector_sensitivity_tensors.npz',
        kappa=kappas,offset_units=offsets,xi=xis,shared_scale_10d=shared_scale,
        P_original=tensor_data['original']['P'],E_original=tensor_data['original']['E'],
        A_original=tensor_data['original']['A'],
        P_autonomous=tensor_data['autonomous']['P'],E_autonomous=tensor_data['autonomous']['E'],
        A_autonomous=tensor_data['autonomous']['A'])
    df=pd.DataFrame(ledger)
    ridge,rstat=candidate_screen(summaries,offsets,xis)
    # Regress observable scalar gain in parent v for sampled phase points
    with zipfile.ZipFile(PARENT) as z:
        vb=z.read(W+'/inputs/'+V+'_server_sendback.zip')
    with zipfile.ZipFile(io.BytesIO(vb)) as z:
        vledger=pd.read_csv(io.BytesIO(z.read(V+'/results/long_horizon_kappa_response_ledger.csv')))
    merged=df.merge(vledger[['seed_family','offset_units','xi','projector_gain']],on=['seed_family','offset_units','xi'],validate='one_to_one')
    max_parent_diff=float(np.max(abs(merged['norm_E']-merged['projector_gain'])))
    max_parent_rel=float(np.max(abs(merged['norm_E']-merged['projector_gain'])/np.maximum(merged['projector_gain'],1e-12)))
    # use five-point vs parent three-point: small differences are expected.
    df.to_csv(out/'anchor_free_projector_sensitivity_ledger.csv',index=False,float_format='%.17g')
    ridge.to_csv(out/'unanchored_moving_ridge_watch.csv',index=False,float_format='%.17g')
    pd.DataFrame(integrations).to_csv(out/'integration_completion.csv',index=False,float_format='%.17g')
    anchorfree=[]
    for seed in ('original','autonomous'):
        for offset in (0,.5,1):
            for xi in (0,.001092,.0125,.05):
                row=df[(df.seed_family==seed)&np.isclose(df.offset_units,offset,atol=1e-12)&np.isclose(df.xi,xi,atol=1e-12)]
                if len(row)!=1:raise RuntimeError('Missing independent checkpoint')
                anchorfree.append(row.iloc[0].to_dict())
    pd.DataFrame(anchorfree).to_csv(out/'trajectory_checkpoints.csv',index=False,float_format='%.17g')
    make_plots(df,None,out)
    report={'version':'v18.50x','title':'Anchor-Free κ0 Differential Response & Moving Sensitivity Geometry Audit',
        'classification':'FIXED_SEED_ANCHOR_FREE_PROJECTOR_DERIVATIVE_DIAGNOSTIC_NOT_MATERIAL_EDGE_OR_ACTIVATION_CERTIFICATE',
        'parent_authentication':auth,'historical_v':{'parent_v_10D_ivps':44,'parent_v_rows':3476,
          'norm_E_vs_3pt_parent_gain_abs_max':max_parent_diff,'norm_E_vs_3pt_parent_gain_rel_max':max_parent_rel},
        'design':{'new_10d_driven_ivps':len(integrations),'kappa_points':len(kappas),'xi_sections':len(xis),
          'rows':len(df),'full_10x10_tensors_saved':True,'kappa_auto':float(vr['kappa']['autonomous']),
          'kappa_original':float(vr['kappa']['original']),
          'delta_kappa':float(vr['kappa']['delta']),
          'replay':'Driven 10D DOP853; same two fixed natural seeds as v18.50v',
          'time_event':'Turn-relative ξ from separate inherited events',
          'kappa_derivative':'Derivative of actual 10x10 projectors; nonuniform 5-node polynomial finite difference; 3-node control',
          'time_derivative':'3-node nonuniform gradient; cubic spline derivative control',
          'metric':'Frobenius in inherited shared 10D chart',
          'ridge_criterion':'In-band strict local maximum of orientation rate >1.05x strongest external control; 3 adjacent times + both seeds for robust interpretation',
          'no_anchor_subtraction_in_primary_measure':True},
        'checks':diagnostics,
        'ridges':rstat,
        'limits':['A finite-difference κ derivative is not a certified continuum derivative.',
          'Numerical ξ differentiation uses shared IVP samples and is not independently integrated.',
          'Fixed-seed κ variation does not give natural-state continuation at each κ.',
          'A common coordinate chart is not a privileged physical material metric.',
          'Absence of a local internal ridge in finite samples does not exclude later or narrower activation.',
          'The two seed families have different natural turning origins.',
          'Projector sensitivity rotation is a property of the chosen projector and metric, not a proven physical material edge.'],
        'environment':{'python':platform.python_version(),'numpy':np.__version__,
          'scipy':__import__('scipy').__version__,'pandas':pd.__version__}}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print('v18.50x COMPLETED',json.dumps({'parent_v_consistency_rel':max_parent_rel,'ridges':rstat,'checks':diagnostics},indent=2),flush=True)

def main():
    pa=argparse.ArgumentParser(description=__doc__)
    pa.add_argument('--end',type=float,default=.05)
    pa.add_argument('--rtol',type=float,default=2e-10)
    pa.add_argument('--atol',type=float,default=2e-11)
    pa.add_argument('--max-step',type=float,default=.00125)
    args=pa.parse_args()
    if abs(args.end-.05)>1e-12:raise ValueError('Reproduction requires the authenticated v18.50v horizon .05')
    run(args)
if __name__=='__main__':main()
