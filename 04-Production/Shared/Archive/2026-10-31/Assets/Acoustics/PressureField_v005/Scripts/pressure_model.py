"""Assumed 1-D linear pressure pulse/reflection. Not measured ECCO data or full-wave CFD/FEM."""
from dataclasses import dataclass,asdict,replace
from pathlib import Path
import math,json,csv,hashlib
import numpy as np

@dataclass(frozen=True)
class Model:
    gap_m:float=.024575852808900598
    sound_speed_m_s:float=1500.0
    carrier_hz:float=400000.0
    pulse_duration_s:float=8e-6
    decay_s:float=6e-6
    sample_interval_s:float=5e-8
    attenuation_np_m:float=4.0
    pressure_reflection:float=.55
    def validate(self):
        for k,v in asdict(self).items():
            if not math.isfinite(v):raise ValueError(f'{k} must be finite')
        for k in ('gap_m','sound_speed_m_s','carrier_hz','pulse_duration_s','decay_s','sample_interval_s'):
            if getattr(self,k)<=0:raise ValueError(f'{k} must be positive')
        if self.carrier_hz>=.5/self.sample_interval_s:raise ValueError('Carrier must be below sample Nyquist frequency')
        if self.attenuation_np_m<0 or abs(self.pressure_reflection)>1:raise ValueError('Invalid passive model attenuation/reflection')
        return self

def pulse_samples(model=Model()):
    model.validate();t=np.arange(0,model.pulse_duration_s+model.sample_interval_s*.5,model.sample_interval_s)
    p=np.sin(2*np.pi*model.carrier_hz*t)*np.sin(np.pi*t/model.pulse_duration_s)**2*np.exp(-t/model.decay_s)
    p[0]=p[-1]=0;p/=max(abs(p))
    return t,p

def validate_input(t,p,metadata):
    t=np.asarray(t,dtype=float);p=np.asarray(p,dtype=float)
    if t.ndim!=1 or p.shape!=t.shape or len(t)<3 or not np.isfinite(t).all() or not np.isfinite(p).all():raise ValueError('Finite paired 1-D samples required')
    if np.any(np.diff(t)<=0):raise ValueError('Sample times must strictly increase')
    for k in ('kind','source_label','signal_role','time_unit','amplitude_unit','time_zero_definition'):
        if not metadata.get(k):raise ValueError(f'Metadata required: {k}')
    if metadata['kind'] not in ('assumed_model','recorded'):raise ValueError('Explicit assumed_model or recorded kind required')
    if metadata['time_unit']!='s':raise ValueError('Convert time to seconds explicitly before import')
    if metadata['signal_role'] not in ('source_pressure','receiver_trace'):raise ValueError('Specify source_pressure or receiver_trace role')
    metadata=dict(metadata)
    if metadata['kind']=='recorded':
        for k in ('sensor_context','gain_filter','provenance_reference','use_permission'):
            if not metadata.get(k):raise ValueError(f'Recorded-data metadata required: {k}')
        if metadata['amplitude_unit']=='normalized_pressure' and not metadata.get('normalization'):
            raise ValueError('Recorded normalized pressure needs an explicit normalization description')
    if metadata['signal_role']=='source_pressure' and metadata['amplitude_unit'] not in ('Pa','normalized_pressure'):
        calibration=metadata.get('pressure_calibration',{})
        factor=calibration.get('pressure_pa_per_unit')
        if not isinstance(factor,(int,float)) or not math.isfinite(factor) or factor<=0 or not calibration.get('source_reference'):
            raise ValueError('Source pressure requires Pa/normalized_pressure, or an explicit sourced pressure calibration')
        p=p*factor;metadata['original_amplitude_unit']=metadata['amplitude_unit'];metadata['amplitude_unit']='Pa';metadata['pressure_calibration_applied']=True
    return t,p,metadata

def read_csv(csv_path,metadata_path):
    path=Path(csv_path);meta=json.loads(Path(metadata_path).read_text());rows=list(csv.DictReader(path.open(newline='',encoding='utf-8-sig')))
    meta['input_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    return validate_input([float(r['time_s']) for r in rows],[float(r['amplitude']) for r in rows],meta)

def components(s,t,model=Model(),source=None):
    """Sample at fixed s in metres. A receiver trace alone cannot determine this field."""
    model.validate()
    if source is None:ts,ps=pulse_samples(model)
    else:
        ts,ps,meta=validate_input(*source)
        if meta['signal_role']!='source_pressure':raise ValueError('Receiver trace cannot uniquely define the full pressure field; a source model is required')
    s=np.asarray(s,dtype=float);t=np.asarray(t,dtype=float)
    if np.any(s<0) or np.any(s>model.gap_m) or not np.isfinite(s).all() or not np.isfinite(t).all():raise ValueError('Finite coordinates within actual gap required')
    outgoing=np.interp(t-s/model.sound_speed_m_s,ts,ps,left=0,right=0)*np.exp(-model.attenuation_np_m*s)
    path=2*model.gap_m-s
    returning=np.interp(t-path/model.sound_speed_m_s,ts,ps,left=0,right=0)*model.pressure_reflection*np.exp(-model.attenuation_np_m*path)
    return outgoing,returning,outgoing+returning

def spectrum_summary(ts,ps):
    dt=float(np.median(np.diff(ts)));n=65536
    magnitude=abs(np.fft.rfft(ps,n));freq=np.fft.rfftfreq(n,dt);peak=int(np.argmax(magnitude));mask=magnitude>=magnitude[peak]*(10**(-6/20))
    band=freq[mask]
    return {'sample_rate_hz':1/dt,'fft_peak_hz':float(freq[peak]),'minus_6db_amplitude_band_hz':[float(band.min()),float(band.max())],'strictly_bandlimited':False,'note':'Finite smooth window has spectral tails; bandwidth measured from authored discrete samples, not ENP3 specification'}

def export_model(folder,model=Model()):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True);ts,ps=pulse_samples(model)
    metadata={'kind':'assumed_model','source_label':'Finite Hann-tapered exponentially damped sinusoid','signal_role':'source_pressure','time_unit':'s','amplitude_unit':'normalized_pressure','normalization':'divide authored pulse by its maximum absolute sample; damping changes normalized shape/spectrum, not predicted absolute power','time_zero_definition':'start of modeled source pulse','measured_ECCO':False,'parameters':asdict(model),'spectrum':spectrum_summary(ts,ps),'limits':['1-D homogeneous nondispersive fluid','single planar scalar reflection','no diffraction, beam spreading, shear conversion, transducer response, receiver filter, noise or multiple interfaces','input receiver trace does not uniquely reconstruct full field','display gain is separate from physical amplitude; normalization prevents absolute-output prediction']}
    with (folder/'source_pulse.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['time_s','amplitude']);w.writerows(zip(ts,ps))
    (folder/'source_pulse.json').write_text(json.dumps(metadata,indent=2))
    time=np.arange(0,2*model.gap_m/model.sound_speed_m_s+model.pulse_duration_s+2e-6,model.sample_interval_s)
    a,b,p=components(0,time,model)
    with (folder/'receiver_model.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['time_s','source_ringdown','returned_pressure','sum_pressure']);w.writerows(zip(time,a,b,p))
    return metadata

def verify(model=Model()):
    ts,ps=pulse_samples(model);D=model.gap_m;c=model.sound_speed_m_s
    checks={}
    checks['zero_before_source']=bool(np.all(components(np.linspace(0,D,40),-1e-6,model)[2]==0))
    checks['receiver_echo_zero_before_roundtrip']=bool(np.all(components(0,np.linspace(0,2*D/c-1e-10,200),model)[1]==0))
    checks['wall_reflection_zero_before_contact']=bool(np.all(components(D,np.linspace(0,D/c-1e-10,100),model)[1]==0))
    peak_t=float(ts[np.argmax(abs(ps))]);expected=model.pressure_reflection*math.exp(-2*model.attenuation_np_m*D)
    observed=float(components(0,2*D/c+peak_t,model)[1])/float(ps[np.argmax(abs(ps))])
    checks['echo_gain_correct']=abs(observed-expected)<1e-10
    t=D/c+ts;a,b,p=components(D,t,model);checks['wall_superposition_correct']=bool(np.allclose(p,a*(1+model.pressure_reflection)))
    doubled=replace(model,sound_speed_m_s=2*c)
    grid=np.arange(0,2*D/c+model.pulse_duration_s+model.sample_interval_s,model.sample_interval_s)
    slow_return=components(0,grid,model)[1];fast_return=components(0,grid,doubled)[1]
    slow_peak=float(grid[np.argmax(abs(slow_return))]);fast_peak=float(grid[np.argmax(abs(fast_return))])
    slow_first=float(grid[np.flatnonzero(abs(slow_return)>1e-8)[0]]);fast_first=float(grid[np.flatnonzero(abs(fast_return)>1e-8)[0]])
    checks['double_speed_halves_delay_from_sampled_peak']=abs((fast_peak-peak_t)/(slow_peak-peak_t)-.5)<.01
    checks['double_speed_advances_sampled_support']=abs((slow_first-fast_first)-D/c)<=2*model.sample_interval_s
    noecho=replace(model,pressure_reflection=0);checks['zero_reflection_zero_echo']=bool(np.all(components(0,ts+2*D/c,noecho)[1]==0))
    meta={'kind':'recorded','source_label':'synthetic interface contract test, not a real recording','signal_role':'receiver_trace','time_unit':'s','amplitude_unit':'V','time_zero_definition':'test trigger','sensor_context':'test fixture only','gain_filter':'test fixture only','provenance_reference':'test code, not measurement','use_permission':'synthetic test fixture'}
    try:components(0,0,model,(ts,ps,meta));checks['receiver_trace_not_treated_as_field']=False
    except ValueError:checks['receiver_trace_not_treated_as_field']=True
    checks['metadata_preserved']=validate_input(ts,ps,meta)[2]==meta
    try:validate_input(ts,ps,dict(meta,signal_role='source_pressure'));checks['voltage_not_accepted_as_pressure_without_calibration']=False
    except ValueError:checks['voltage_not_accepted_as_pressure_without_calibration']=True
    calibrated=validate_input(ts,ps,dict(meta,signal_role='source_pressure',pressure_calibration={'pressure_pa_per_unit':2.0,'source_reference':'synthetic test conversion'}))
    checks['explicit_calibration_applied']=bool(np.allclose(calibrated[1],2*ps) and calibrated[2]['amplitude_unit']=='Pa')
    return {'checks':checks,'all_pass':all(checks.values()),'gap_m':D,'one_way_s':D/c,'roundtrip_s':2*D/c,'receiver_echo_gain':observed,'sampled_speed_check':{'slow_peak_s':slow_peak,'fast_peak_s':fast_peak,'slow_first_s':slow_first,'fast_first_s':fast_first},'spectrum':spectrum_summary(ts,ps)}
