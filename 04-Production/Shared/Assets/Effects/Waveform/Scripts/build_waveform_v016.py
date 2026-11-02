"""Additive Organic/Short Event shared waveform. Run in background Blender."""
import bpy,math,json,hashlib,numpy as np
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';Q=R/'04-Production/Shots/S01-S02'
source=B/'Waveform_shared_v015.blend';target=B/'Waveform_shared_v016.blend';assert not target.exists()
before=hashlib.sha256(source.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(source))
live=bpy.data.objects['WF_LIVE_FIELD'];ctrl=bpy.data.objects['WF_MASTER_CONTROLS'];old=live.modifiers[0].node_group
def coordinates(f):
 bpy.context.scene.frame_set(f);bpy.context.view_layer.update();ev=live.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();a=np.empty(len(me.vertices)*3);me.vertices.foreach_get('co',a);ev.to_mesh_clear();return a
reference={f:coordinates(f) for f in [1,12,18,26,30,38,54,62,68,96]}
helpers=(R/'04-Production/Records/Tasks/T-056/build_shared_gn_v014.py').read_text()
exec(helpers[helpers.index('class G:'):helpers.index('\ndef value(')])
def parameter(mod,name):
 ident=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name)
 return getattr(mod.properties.inputs,ident)
# Append shared style attributes without modifying the original field mathematics.
cg=ctrl.modifiers[0].node_group;cg.name='WF_MASTER_CONTROL_VALUES_v016';gi=next(n for n in cg.nodes if n.bl_idname=='NodeGroupInput');go=next(n for n in cg.nodes if n.bl_idname=='NodeGroupOutput');geo=go.inputs['Geometry'].links[0].from_socket
specs=[('Short Crests',2.,1.,4.),('Short Packet Fraction',.9,.3,1.5),('Short Contact Blend Frames',4.,0.,8.),('Short Return Fade Frames',3.,1.,8.),('Short Stroke Factor',1.5,.5,3.),('Short Taper Power',.65,.2,2.),('Short Height Fraction',.65,.1,1.)]
for name,default,lo,hi in specs:
 sock=cg.interface.new_socket(name=name,in_out='INPUT',socket_type='NodeSocketFloat');sock.default_value=default;sock.min_value=lo;sock.max_value=hi
 sock.description='Reusable short-event display style; event landmarks remain shot-local.'
 n=cg.nodes.new('GeometryNodeStoreNamedAttribute');n.data_type='FLOAT';n.domain='POINT';n.inputs['Name'].default_value='wf_'+name;cg.links.new(geo,n.inputs['Geometry']);cg.links.new(gi.outputs[name],n.inputs['Value']);geo=n.outputs['Geometry']
cg.links.new(geo,go.inputs['Geometry'])
for name,default,lo,hi in specs:parameter(ctrl.modifiers[0],name).value=default
ctrl.update_tag();bpy.context.view_layer.update()

# Both presets expose the original local API. New explicit contact/receipt inputs
# default to derivation from existing travel/delay settings.
short=G('WF_SHORT_EVENT_FIELD_v016');local={};original_inputs=[]
for x in old.interface.items_tree:
 if getattr(x,'in_out','')!='INPUT' or x.socket_type=='NodeSocketGeometry':continue
 original_inputs.append(x.name);default=x.default_value
 if x.socket_type in ['NodeSocketVector','NodeSocketColor']:default=tuple(default)
 local[x.name]=short.socket(x.name,x.socket_type,default,getattr(x,'min_value',None),getattr(x,'max_value',None),description=x.description)
for name in ['Contact Frame','Receipt Frame']:local[name]=short.socket(name,'NodeSocketFloat',0.,0.,100000.)
names=['Playback Speed','Frequency Multiplier','Strength','Echo Strength','Decay Tightness','One Way Frames','Reference Height m','Width m','Strand Radius m','Opacity Power','Emission','Color Violet','Color Cyan']+[x[0] for x in specs]
shared={name:short.shared(ctrl,name,name.startswith('Color ')) for name in names};op=short.op
u=short.attr('route_u');v=op('SUBTRACT',op('MULTIPLY',short.attr('strand_v'),2),1)
scene=short.node('GeometryNodeInputSceneTime');frame=scene.outputs['Frame'];start=local['Start Frame'];elapsed=op('SUBTRACT',frame,start)
travel=short.choose(op('GREATER_THAN',local['Travel Override'],0),local['Travel Override'],shared['One Way Frames'])
contact=short.choose(op('GREATER_THAN',local['Contact Frame'],0),local['Contact Frame'],op('ADD',start,travel))
return_start=op('ADD',contact,local['Echo Delay Frames'])
rettravel=short.choose(op('GREATER_THAN',local['Return Travel Override'],0),local['Return Travel Override'],travel)
receipt=short.choose(op('GREATER_THAN',local['Receipt Frame'],0),local['Receipt Frame'],op('ADD',return_start,rettravel))
def clamp(x):return op('MINIMUM',op('MAXIMUM',x,0),1)
def smooth(x):
 x=clamp(x);return op('MULTIPLY',op('MULTIPLY',x,x),op('SUBTRACT',3,op('MULTIPLY',2,x)))
cased=local['Preset 0 Open 1 Cased'];decay=op('MULTIPLY',shared['Decay Tightness'],op('MULTIPLY',local['Decay Override'],op('ADD',1,op('MULTIPLY',cased,.2))))
fraction=op('MAXIMUM',shared['Short Packet Fraction'],.1)
front_out=op('DIVIDE',elapsed,op('MAXIMUM',op('SUBTRACT',contact,start),.001))
front_ret=op('DIVIDE',op('SUBTRACT',frame,return_start),op('MAXIMUM',op('SUBTRACT',receipt,return_start),.001))
po=op('DIVIDE',op('SUBTRACT',front_out,u),fraction);pr=op('DIVIDE',op('SUBTRACT',u,op('SUBTRACT',1,front_ret)),fraction)
def envelope(p):
 return op('MULTIPLY',op('POWER',op('MAXIMUM',op('SINE',op('MULTIPLY',clamp(p),math.pi)),0),op('MULTIPLY',2,decay)),op('MULTIPLY',op('GREATER_THAN',p,0),op('LESS_THAN',p,1)))
blend=op('MINIMUM',shared['Short Contact Blend Frames'],op('MULTIPLY',op('SUBTRACT',receipt,return_start),.75))
out_fade=op('SUBTRACT',1,smooth(op('DIVIDE',op('SUBTRACT',frame,contact),op('MAXIMUM',blend,.001))))
fade=op('MINIMUM',shared['Short Return Fade Frames'],op('MULTIPLY',op('SUBTRACT',receipt,return_start),.5))
ret_fade=op('SUBTRACT',1,smooth(op('DIVIDE',op('SUBTRACT',frame,op('SUBTRACT',receipt,fade)),op('MAXIMUM',fade,.001))))
active=op('MULTIPLY',op('GREATER_THAN',frame,start),op('LESS_THAN',frame,receipt))
eo=op('MULTIPLY',envelope(po),op('MULTIPLY',out_fade,active));er=op('MULTIPLY',envelope(pr),op('MULTIPLY',ret_fade,active))
frequency=op('MULTIPLY',shared['Frequency Multiplier'],local['Frequency Override'])
speed=op('MULTIPLY',local['Playback Override'],short.choose(local['Lock Event Timing'],1,shared['Playback Speed']))
clock=op('MULTIPLY',op('DIVIDE',op('MULTIPLY',elapsed,speed),7.5),frequency)
sp=op('ADD',op('MULTIPLY',1.15,v),op('MULTIPLY',.22,op('SINE',op('MULTIPLY',math.pi,v))))
def wave(reverse=False):
 along=op('SUBTRACT',1,u) if reverse else u
 phase=op('MULTIPLY',math.tau,op('SUBTRACT',op('MULTIPLY',shared['Short Crests'],along),clock))
 phase=op('ADD',phase,.8 if reverse else 0)
 primary=op('SINE',op('ADD',phase,sp))
 secondary=op('SINE',op('ADD',op('ADD',op('MULTIPLY',phase,1.65),-.5 if reverse else .65),op('MULTIPLY',.8 if reverse else 1.8,v)))
 return op('MULTIPLY',op('ADD',op('MULTIPLY',.82 if reverse else .73,primary),op('MULTIPLY',.18 if reverse else .27,secondary)),op('ADD',.85,op('MULTIPLY',.15,op('COSINE',op('MULTIPLY',math.pi/2,v)))))
echo=op('MULTIPLY',shared['Echo Strength'],op('MULTIPLY',local['Echo Override'],op('SUBTRACT',1,op('MULTIPLY',cased,.2))))
shape=op('ADD',op('MULTIPLY',eo,wave()),op('MULTIPLY',op('MULTIPLY',echo,er),wave(True)))
height=op('MULTIPLY',shape,op('MULTIPLY',op('MULTIPLY',.5,shared['Reference Height m']),op('MULTIPLY',shared['Short Height Fraction'],op('MULTIPLY',shared['Strength'],op('MULTIPLY',local['Strength Override'],local['Height Override'])))))
env=op('MAXIMUM',eo,op('MULTIPLY',.75,er));alpha=op('MULTIPLY',op('POWER',env,shared['Opacity Power']),local['Enabled'])
spread=op('MULTIPLY',v,op('MULTIPLY',.5,op('MULTIPLY',shared['Width m'],op('MULTIPLY',local['Width Override'],op('SQRT',env)))))
radius=op('MULTIPLY',op('MULTIPLY',shared['Strand Radius m'],local['Radius Override']),op('MULTIPLY',shared['Short Stroke Factor'],op('POWER',env,shared['Short Taper Power'])))
height=op('ADD',height,op('MULTIPLY',short.attr('ring_cos'),radius));spread=op('ADD',spread,op('MULTIPLY',short.attr('ring_sin'),radius))
pos=short.vop('ADD',short.vop('SCALE',local['Route Axis'],op('MULTIPLY',u,local['Gap Length m'])),short.vop('ADD',short.vop('SCALE',local['Up Axis'],height),short.vop('SCALE',local['Transverse Axis'],spread)))
setp=short.node('GeometryNodeSetPosition');short.link(short.i.outputs['Geometry'],setp.inputs['Geometry']);short.link(pos,setp.inputs['Position']);geo=setp.outputs['Geometry']
for name,val in [('wf_alpha',alpha),('wf_emission',shared['Emission']),('wf_out_envelope',eo),('wf_return_envelope',er)]:geo=short.store(geo,name,val)
mix=short.node('ShaderNodeMixRGB');short.link(short.attr('strand_v'),mix.inputs[0]);short.link(shared['Color Violet'],mix.inputs[1]);short.link(shared['Color Cyan'],mix.inputs[2]);geo=short.store(geo,'wf_color',mix.outputs[0],'FLOAT_COLOR')
delete=short.node('GeometryNodeDeleteGeometry');delete.domain='POINT';delete.mode='ALL';short.link(geo,delete.inputs['Geometry']);short.link(op('LESS_THAN',alpha,1e-6),delete.inputs['Selection'])
mat=short.node('GeometryNodeSetMaterial');mat.inputs['Material'].default_value=bpy.data.materials['WF_SHARED_FIELD_MATERIAL'];short.link(delete.outputs['Geometry'],mat.inputs['Geometry']);short.link(mat.outputs['Geometry'],short.o.inputs['Geometry'])

wrapper=G('WF_FIELD_LIVE_v016');inputs={}
for x in old.interface.items_tree:
 if getattr(x,'in_out','')!='INPUT' or x.socket_type=='NodeSocketGeometry':continue
 default=x.default_value
 if x.socket_type in ['NodeSocketVector','NodeSocketColor']:default=tuple(default)
 inputs[x.name]=wrapper.socket(x.name,x.socket_type,default,getattr(x,'min_value',None),getattr(x,'max_value',None),description=x.description)
inputs['Contact Frame']=wrapper.socket('Contact Frame','NodeSocketFloat',0.,0.,100000.)
inputs['Receipt Frame']=wrapper.socket('Receipt Frame','NodeSocketFloat',0.,0.,100000.)
preset=wrapper.socket('Motion Preset 0 Organic 1 Short','NodeSocketInt',0,0,1,'Organic preserves v015. Short fits explicit local landmarks with rolling/tapered geometry.')
for name,position in [('Motion Preset 0 Organic 1 Short',2),('Contact Frame',4),('Receipt Frame',5)]:
 wrapper.g.interface.move(next(x for x in wrapper.g.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name),position)
for x in wrapper.g.interface.items_tree:
 if x.name=='Duration Override':x.description='Organic only. Short uses packet fraction and explicit event landmarks.'
 elif x.name in ['Outbound End Frame','Return End Frame']:x.description='Organic legacy gate. Short uses Contact/Receipt with shared blend/fade.'
organic=wrapper.node('GeometryNodeGroup');organic.node_tree=old
compact=wrapper.node('GeometryNodeGroup');compact.node_tree=short.g
for group in [organic,compact]:
 wrapper.link(wrapper.i.outputs['Geometry'],group.inputs['Geometry'])
 for name,val in inputs.items():
  if name in group.inputs:wrapper.link(val,group.inputs[name])
switch=wrapper.node('GeometryNodeSwitch');switch.input_type='GEOMETRY';wrapper.link(preset,switch.inputs['Switch']);wrapper.link(organic.outputs['Geometry'],switch.inputs['False']);wrapper.link(compact.outputs['Geometry'],switch.inputs['True']);wrapper.link(switch.outputs[0],wrapper.o.inputs['Geometry'])
mod=live.modifiers[0];mod.node_group=wrapper.g
# Preserve the original source-native route settings on the new modifier.
for x in old.interface.items_tree:
 if getattr(x,'in_out','')=='INPUT' and x.socket_type!='NodeSocketGeometry':parameter(mod,x.name).value=tuple(x.default_value) if x.socket_type in ['NodeSocketVector','NodeSocketColor'] else x.default_value
# v015 instance's authored route is not equal to generic group socket defaults.
parameter(mod,'Route Axis').value=(.3583680987358093,-.9335803985595703,0)
parameter(mod,'Transverse Axis').value=(-.9335803985595703,-.3583680987358093,0)
parameter(mod,'Up Axis').value=(0,0,1)
live.update_tag();checks=[]
for f,a in reference.items():
 b=coordinates(f);err=float(np.max(np.abs(a-b))) if len(a)==len(b) and len(a) else (0. if not len(a) and not len(b) else 999.)
 checks.append({'frame':f,'vertices':len(b)//3,'max_error_m':err});assert err<1e-7
txt=bpy.data.texts.new('v016 presets and timing');txt.write('Candidate. Motion Preset0 Organic preserves v015;1 Short uses explicit Start/Contact/Receipt landmarks, 7.5frame carrier period, spatial crests, brief post-contact overlap and geometry taper for Workbench. MASTER controls own Short style. Shot owns landmarks/route/context. Short geometry ends at receipt; no measurement data or camera in shared source. Authored illustration, not calibrated physics.\n')
bpy.context.scene.frame_set(30);bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
assert hashlib.sha256(source.read_bytes()).hexdigest()==before
report={'native':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_v015_sha256':before,'source_unchanged':True,'organic_reference_checks':checks,'group':wrapper.g.name,'presets':{'0':'Organic v015 exact','1':'Short Event rolling/tapered'},'shared_short_controls':{x[0]:x[1] for x in specs},'local_landmarks':['Start Frame','Contact Frame','Receipt Frame','Echo Delay Frames'],'consumers':['S01-S02 waveform trial v009','S04 open/cased fixture proof only'],'status':'candidate, not owner accepted'}
(B/'Waveform_interface_v016.json').write_text(json.dumps(report,indent=2));(Q/'Notes/waveform_v016_build.json').write_text(json.dumps(report,indent=2));print('WAVEFORM_V016_READY',checks)
