"""ECCO fixed-path waveform controls v001. Visual default v004 is NOT owner-approved.

Geometry is authored once. Re-baking changes material keyframes only.
No calibrated acoustic propagation or inferred casing response is supplied.
"""
from dataclasses import dataclass, asdict
import math, json, hashlib, csv
from pathlib import Path

@dataclass(frozen=True)
class Controls:
    send_frame: float = 300
    contact_frame: float = 309
    receive_frame: float = 318
    playback_rate: float = 1.0
    playback_origin: float = 300
    head_width: float = .07
    trail_decay: float = .16
    return_strength: float = .55
    base_brightness: float = .012
    peak_brightness: float = 1.0
    emission_gain: float = 3.0
    outbound_color: tuple = (.025, .78, 1.0)
    return_color: tuple = (.03, .7, .48)
    context: str = 'open-hole'

    def validate(self):
        data=asdict(self)
        for key,value in data.items():
            if isinstance(value,(int,float)) and not math.isfinite(value):
                raise ValueError(f'{key} must be finite')
        if not self.send_frame < self.contact_frame < self.receive_frame:
            raise ValueError('Require send_frame < contact_frame < receive_frame')
        if self.playback_rate <= 0 or self.head_width <= 0 or self.trail_decay <= 0:
            raise ValueError('Playback rate, head width and decay must be positive')
        if not 0 <= self.return_strength <= 1:
            raise ValueError('Return strength must be in [0,1]')
        if not 0 <= self.base_brightness <= self.peak_brightness <= 1:
            raise ValueError('Require 0 <= base <= peak <= 1')
        if self.emission_gain < 0: raise ValueError('Emission gain must be nonnegative')
        for key in ('outbound_color','return_color'):
            color=getattr(self,key)
            if len(color)!=3 or any(not math.isfinite(x) or x<0 or x>1 for x in color):
                raise ValueError(f'{key} requires three finite values in [0,1]')
        if self.context not in ('open-hole','cased-hole'):
            raise ValueError('context must be open-hole or cased-hole')
        return self

@dataclass(frozen=True)
class PathSpec:
    cycles: float = 5.0
    amplitude_fraction: float = .105
    depth_fraction: float = .018
    radius_m: float = .000065
    segments: int = 60
    points_per_segment: int = 16

    def validate(self):
        for key in ('cycles','amplitude_fraction','depth_fraction','radius_m'):
            value=getattr(self,key)
            if not math.isfinite(value) or value<0:raise ValueError(f'{key} must be finite/nonnegative')
        if self.cycles==0 or self.radius_m==0:raise ValueError('cycles/radius must be positive')
        if not isinstance(self.segments,int) or self.segments<2:raise ValueError('segments must be integer >=2')
        if not isinstance(self.points_per_segment,int) or self.points_per_segment<2:raise ValueError('points_per_segment must be integer >=2')
        return self

@dataclass(frozen=True)
class SampleSeries:
    """Explicitly selected echo window; samples affect return brightness, never path shape."""
    times: tuple
    amplitudes: tuple
    provenance: dict

    def validate(self):
        if len(self.times)<2 or len(self.times)!=len(self.amplitudes):raise ValueError('At least two paired samples required')
        if any(not math.isfinite(x) for x in self.times+self.amplitudes):raise ValueError('Non-finite sample')
        if any(b<=a for a,b in zip(self.times,self.times[1:])):raise ValueError('Sample times must strictly increase')
        for key in ('source_label','kind','time_unit','amplitude_unit','window_meaning'):
            if not self.provenance.get(key):raise ValueError(f'Missing sample provenance {key}')
        if self.provenance['kind'] not in ('recorded','synthetic'):raise ValueError('kind must be recorded or synthetic')
        if self.provenance['window_meaning']!='selected_echo_window':raise ValueError('Explicit selected_echo_window required; do not infer echo window')
        return self

    def envelope(self,progress):
        self.validate()
        t=self.times[0]+max(0,min(1,progress))*(self.times[-1]-self.times[0])
        i=next((i for i in range(len(self.times)-1) if self.times[i]<=t<=self.times[i+1]),len(self.times)-2)
        u=(t-self.times[i])/(self.times[i+1]-self.times[i])
        a=self.amplitudes[i]*(1-u)+self.amplitudes[i+1]*u
        scale=max(abs(x) for x in self.amplitudes)
        return abs(a)/scale if scale else 0.0

def read_samples_csv(path,provenance):
    """CSV columns time,amplitude. Input stays local; no dataset is copied to the library."""
    path=Path(path);rows=list(csv.DictReader(path.open(newline='',encoding='utf-8-sig')))
    meta=dict(provenance,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
              normalization='absolute amplitude / selected-window maximum',mapping='return-leg cinematic brightness only')
    return SampleSeries(tuple(float(r['time']) for r in rows),tuple(float(r['amplitude']) for r in rows),meta).validate()

def signal_at(frame,position,controls,samples=None):
    """Returns (RGB, emission_strength); no geometry or position update."""
    controls.validate()
    if not math.isfinite(frame) or not 0<=position<=1:raise ValueError('Finite frame and path position [0,1] required')
    f=controls.playback_origin+(frame-controls.playback_origin)*controls.playback_rate
    outgoing=controls.send_frame<=f<=controls.contact_frame
    returning=controls.contact_frame<f<=controls.receive_frame
    value=0.0;hue=controls.outbound_color
    if outgoing:
        progress=(f-controls.send_frame)/(controls.contact_frame-controls.send_frame)
        delta=position-progress
    elif returning:
        progress=(f-controls.contact_frame)/(controls.receive_frame-controls.contact_frame)
        delta=(1-progress)-position;hue=controls.return_color
    else:delta=5
    if outgoing or returning:
        value=math.exp(-(delta/controls.head_width)**2) if delta>=0 else math.exp(delta/controls.trail_decay)
        if returning:
            value*=controls.return_strength
            if samples is not None:value*=samples.envelope(progress)
    value*=controls.peak_brightness
    color=tuple(controls.base_brightness+(channel-controls.base_brightness)*value for channel in hue)
    return color, .25+value*controls.emission_gain

def generated_path(start,end,spec=PathSpec()):
    """Generate immutable path points. cycles is spatial styling, never signal frequency Hz."""
    spec.validate()
    if len(start)!=3 or len(end)!=3 or any(not math.isfinite(x) for x in tuple(start)+tuple(end)):
        raise ValueError('Two finite XYZ anchors required')
    axis=tuple(b-a for a,b in zip(start,end));length=math.sqrt(sum(x*x for x in axis))
    if length<=1e-9:raise ValueError('Distinct source and target required')
    a=tuple(x/length for x in axis);up=(0,0,1) if abs(a[2])<.9 else (0,1,0)
    dot=sum(x*y for x,y in zip(a,up));v=tuple(up[i]-dot*a[i] for i in range(3));vn=math.sqrt(sum(x*x for x in v));v=tuple(x/vn for x in v)
    d=(a[1]*v[2]-a[2]*v[1],a[2]*v[0]-a[0]*v[2],a[0]*v[1]-a[1]*v[0])
    count=spec.segments*(spec.points_per_segment-1)+1;points=[]
    for i in range(count):
        t=i/(count-1);env=math.sin(math.pi*t)**.6;phase=math.tau*spec.cycles*t
        points.append(tuple(start[k]+axis[k]*t+v[k]*length*spec.amplitude_fraction*env*math.sin(phase)+d[k]*length*spec.depth_fraction*env*math.cos(phase) for k in range(3)))
    points[0]=tuple(start);points[-1]=tuple(end)
    return points

def validate_supplied_path(points):
    points=[tuple(float(x) for x in p) for p in points]
    if len(points)<3 or any(len(p)!=3 or any(not math.isfinite(x) for x in p) for p in points):raise ValueError('Path requires >=3 finite XYZ points')
    if any(sum((a-b)**2 for a,b in zip(p,q))<1e-20 for p,q in zip(points,points[1:])):raise ValueError('Consecutive path points must differ')
    return points

def geometry_digest(collection):
    data=[]
    for ob in sorted(collection.objects,key=lambda o:o.name):
        if ob.type=='CURVE':data.append({'name':ob.name,'matrix':[list(r) for r in ob.matrix_world], 'points':[[list(p.co) for p in sp.points] for sp in ob.data.splines], 'radius':ob.data.bevel_depth})
    return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()

def create_asset(name,start=None,end=None,points=None,spec=PathSpec(),controls=Controls(),scene=None):
    """Blender-only. Create new exclusive collection; never replace existing named assets."""
    import bpy
    spec.validate();controls.validate()
    if name in bpy.data.collections:raise ValueError('Collection exists; choose a versioned new name')
    points=generated_path(start,end,spec) if points is None else validate_supplied_path(points)
    col=bpy.data.collections.new(name);(scene or bpy.context.scene).collection.children.link(col)
    ctrl=bpy.data.objects.new(name+'_CONTROL',None);col.objects.link(ctrl)
    ctrl['package_version']='fixed-path-controls-v001';ctrl['visual_status']='v004 default UNAPPROVED; owner review pending'
    ctrl['path_spec_json']=json.dumps(asdict(spec));ctrl['path_generation_note']='cycles are spatial styling; change requires a new geometry version, never animate phase'
    for key,value in asdict(controls).items():ctrl[key]=value
    step=max(1,math.ceil((len(points)-1)/spec.segments))
    for i,first in enumerate(range(0,len(points)-1,step)):
        chunk=points[first:min(first+step+1,len(points))]
        curve=bpy.data.curves.new(f'{name}_SEG_{i:03}','CURVE');curve.dimensions='3D';curve.bevel_depth=spec.radius_m;curve.bevel_resolution=2
        spline=curve.splines.new('POLY');spline.points.add(len(chunk)-1)
        for p,xyz in zip(spline.points,chunk):p.co=(*xyz,1)
        ob=bpy.data.objects.new(curve.name,curve);col.objects.link(ob)
        mat=bpy.data.materials.new(curve.name+'_SIGNAL');mat.use_nodes=True
        nodes=mat.node_tree.nodes;nodes.clear();em=nodes.new('ShaderNodeEmission');em.name='SignalEmission';out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(em.outputs[0],out.inputs[0])
        mat['path_position']=(first+(len(chunk)-1)/2)/(len(points)-1);curve.materials.append(mat)
    ctrl['geometry_sha256']=geometry_digest(col)
    return col,ctrl

def controls_from_object(control):
    values={key:control[key] for key in asdict(Controls())}
    for key in ('outbound_color','return_color'):values[key]=tuple(values[key])
    return Controls(**values).validate()

def bake_material_animation(collection,control,frame_start,frame_end,samples=None):
    """Apply local property edits. Only material actions change; geometry hash enforced."""
    controls=controls_from_object(control)
    if not isinstance(frame_start,int) or not isinstance(frame_end,int) or frame_end<=frame_start:raise ValueError('Increasing integer bake range required')
    if samples:samples.validate()
    before=geometry_digest(collection)
    if before!=control['geometry_sha256']:raise ValueError('Path changed since creation; version the geometry instead of silently rebaking')
    for ob in collection.objects:
        if ob.type!='CURVE':continue
        mat=ob.data.materials[0];mat.animation_data_clear();mat.node_tree.animation_data_clear();em=mat.node_tree.nodes['SignalEmission'];position=mat['path_position']
        for frame in range(frame_start,frame_end+1):
            rgb,strength=signal_at(frame,position,controls,samples)
            mat.diffuse_color=(*rgb,1);mat.keyframe_insert('diffuse_color',frame=frame)
            em.inputs[0].default_value=(*rgb,1);em.inputs[0].keyframe_insert('default_value',frame=frame)
            em.inputs[1].default_value=strength;em.inputs[1].keyframe_insert('default_value',frame=frame)
    after=geometry_digest(collection)
    if before!=after:raise RuntimeError('Unexpected geometry mutation during material bake')
    control['bake_range']=[frame_start,frame_end]
    control['sample_provenance_json']=json.dumps(samples.provenance if samples else {'kind':'synthetic','source_label':'authored cinematic brightness envelope','calibrated':False})
    return {'geometry_unchanged':True,'geometry_sha256':after,'controls':asdict(controls),'samples':samples.provenance if samples else None}
