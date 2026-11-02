"""Finalize approved sharp pulse as a clean, fully native parametric library."""
import bpy,math,json,hashlib,sys
from mathutils import Vector
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from pulse_graph import Graph,socket,param,set_input,STYLE,COLORS,TIMING
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Effects/Waveform';target=B/'Waveform_shared_v017.blend';assert not target.exists() or '--candidate-rebuild' in sys.argv
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name='WF17 approved sharp pulse library';s.frame_start=1;s.frame_end=192;s.render.fps=24
collection=bpy.data.collections.new('WAVEFORM_PULSE_v017');s.collection.children.link(collection)
me=bpy.data.meshes.new('WF17 master point');me.from_pydata([(0,0,0)],[],[]);ctrl=bpy.data.objects.new('WF_MASTER_CONTROLS',me);collection.objects.link(ctrl)
cg=Graph('WF_PULSE_MASTER_VALUES_v017');geo=cg.i.outputs['Geometry']
for name,typ,default,lo,hi,panel in STYLE:
 value=cg.input(name,typ,default,lo,hi,cg.panel(panel));geo=cg.store(geo,'wf17_'+name,value)
for name,color in COLORS:
 value=cg.input(name,'NodeSocketColor',color,panel=cg.panel('Colors'));geo=cg.store(geo,'wf17_'+name,value,'FLOAT_COLOR')
cg.input('Emission','NodeSocketFloat',1.,0.,20.,cg.panel('Colors'));cg.link(geo,cg.o.inputs['Geometry']);cm=ctrl.modifiers.new('MASTER CONTROLS — reusable pulse style','NODES');cm.node_group=cg.g
def driver(prop,channel,name,component=None,expression='v'):
 fc=prop.driver_add('default_value' if channel is None else 'diffuse_color',channel) if channel is not None else prop.driver_add('default_value')
 var=fc.driver.variables.new();var.name='v';var.type='SINGLE_PROP';var.targets[0].id=ctrl
 ident=socket(cg.g,name).identifier;path=f'modifiers["{cm.name}"].properties.inputs.{ident}.value'+(f'[{component}]' if component is not None else '')
 ctrl.path_resolve(path);var.targets[0].data_path=path;fc.driver.expression=expression
def material(name,color_name,gain=1.,tint=0.):
 m=bpy.data.materials.new(name);m.diffuse_color=(.02,.85,1,1);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(em.outputs[0],out.inputs['Surface'])
 for channel in range(3):
  expr=f'({1-tint}*v+{tint})*{gain}';driver(m,channel,color_name,channel,expr)
  fc=em.inputs['Color'].driver_add('default_value',channel);v=fc.driver.variables.new();v.name='v';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path=f'modifiers["{cm.name}"].properties.inputs.{socket(cg.g,color_name).identifier}.value[{channel}]';fc.driver.expression=expr
 driver(em.inputs['Strength'],None,'Emission');return m
materials=[]
for color_name in ['Outgoing color','Reflected color']:
 for j in range(17):materials.append(material(f'WF17 {color_name} band{j:02}',color_name,.65+.35*j/16))
for name,col,gain,tint in [('Send head','Outgoing color',1.,.25),('Send tail','Outgoing color',.8,0.),('Return head','Reflected color',1.,.25),('Return tail','Reflected color',.8,0.)]:materials.append(material('WF17 '+name,col,gain,tint))
# Immutable high-resolution parameter sites; strand count remains live1–17.
SAMPLES=513;STRANDS=17;verts=[];faces=[];uvalues=[];indices=[];rings=[]
for strand in range(STRANDS):
 for sample in range(SAMPLES):
  for ring in range(4):verts.append((0,0,0));uvalues.append(sample/(SAMPLES-1));indices.append(strand);rings.append(ring)
 for sample in range(SAMPLES-1):
  a=(strand*SAMPLES+sample)*4
  for ring in range(4):faces.append((a+ring,a+(ring+1)%4,a+4+(ring+1)%4,a+4+ring))
domain=bpy.data.meshes.new('WF17 immutable pulse domain');domain.from_pydata(verts,[],faces);domain.update()
for name,values in [('wf17_u',uvalues),('wf17_strand',indices),('wf17_ring',rings)]:a=domain.attributes.new(name,'FLOAT','POINT');a.data.foreach_set('value',values)
for m in materials:domain.materials.append(m)
field=bpy.data.objects.new('WF_PULSE_FIELD',domain);collection.objects.link(field)

# Public timing sub-group can also drive shot-owned cues.
tim=Graph('WF_PULSE_TIMING_v017',False);ti={}
for name,typ,default,lo,hi in TIMING:ti[name]=tim.input(name,typ,default,lo,hi)
for name,val in [('Frame',1.),('Scene FPS',24.),('Reference FPS',24.),('Train duration',20.)]:ti[name]=tim.input(name,default=val)
op=tim.op;D=ti['Train duration'];T=ti['Travel frames'];TR=tim.switch(op('GREATER_THAN',ti['Return travel override'],0),ti['Return travel override'],T);DR=op('MULTIPLY',D,ti['Return train scale']);ST=op('ADD',T,D)
RO=tim.switch(op('COMPARE',ti['Mode 0 Both 1 Send 2 Return'],2),0,op('ADD',tim.switch(ti['Reflection after tail'],ST,T),ti['Reflection delay']));RT=op('ADD',op('ADD',RO,TR),DR)
reflect=op('MULTIPLY',ti['Reflection enabled'],op('SUBTRACT',1,op('COMPARE',ti['Mode 0 Both 1 Send 2 Return'],1)))
end=tim.switch(reflect,RT,ST);base_speed=op('MULTIPLY',ti['Speed'],tim.switch(ti['Follow scene FPS'],op('DIVIDE',ti['Reference FPS'],op('MAXIMUM',ti['Scene FPS'],1)),1))
fit=op('MULTIPLY',op('GREATER_THAN',ti['Fit end frame'],0),op('GREATER_THAN',ti['Fit end frame'],ti['Start frame']))
speed=tim.switch(fit,op('DIVIDE',end,op('MAXIMUM',op('SUBTRACT',ti['Fit end frame'],ti['Start frame']),.001)),base_speed)
period=op('MAXIMUM',op('ADD',end,ti['Loop quiet frames']),op('MULTIPLY',ti['Loop period override'],speed));elapsed=op('MULTIPLY',op('SUBTRACT',ti['Frame'],ti['Start frame']),speed);clock=tim.switch(op('MULTIPLY',ti['Loop'],op('GREATER_THAN',elapsed,-.000001)),op('MODULO',elapsed,op('MAXIMUM',period,.001)),elapsed)
values={'Time':clock,'Return offset':RO,'Return travel':TR,'Return duration':DR,'Effective speed':speed,'Cycle frames':op('DIVIDE',period,speed)}
for name,value in [('Send head arrival',T),('Send tail arrival',ST),('Return start',RO),('Return head arrival',op('ADD',RO,TR)),('Return tail arrival',RT)]:values[name]=op('ADD',ti['Start frame'],op('DIVIDE',value,speed))
for name,value in values.items():tim.link(value,tim.output(name))

g=Graph('WF_PULSE_SYSTEM_v017');local={}
for name,typ,default,lo,hi in TIMING:local[name]=g.input(name,typ,default,lo,hi,g.panel('1 Timing and playback'))
master=g.input('Use master style','NodeSocketBool',True,panel=g.panel('2 Quick instance overrides'))
quick={}
for name,typ,default,lo,hi in [('Pulse count override','NodeSocketInt',0,0,5),('Strand count override','NodeSocketInt',0,0,17),('Strand separation override','NodeSocketFloat',-1.,-1.,.9),('Strength multiplier','NodeSocketFloat',1.,0.,4.),('Width multiplier','NodeSocketFloat',1.,0.,4.),('Radius multiplier','NodeSocketFloat',1.,.1,4.),('Show markers','NodeSocketBool',True,None,None)]:quick[name]=g.input(name,typ,default,lo,hi,g.panel('2 Quick instance overrides'))
p={}
for name,typ,default,lo,hi,panel in STYLE:
 own=g.input(name,typ,default,lo,hi,g.panel('Local '+panel,True));p[name]=g.switch(master,g.sample(ctrl,name),own)
op=g.op
for name,override in [('Pulse count','Pulse count override'),('Strand count','Strand count override')]:p[name]=g.switch(op('GREATER_THAN',quick[override],0),quick[override],p[name])
p['Strand separation']=g.switch(op('GREATER_THAN',quick['Strand separation override'],-.5),quick['Strand separation override'],p['Strand separation'])
place=g.panel('3 Placement and anchors');anchor_mode=g.input('Use anchor objects','NodeSocketBool',False,panel=place);A=g.input('Start anchor','NodeSocketObject',None,panel=place);Bobj=g.input('End anchor','NodeSocketObject',None,panel=place)
origin=g.input('Origin','NodeSocketVector',(0,0,0),panel=place);gap=g.input('Gap length m','NodeSocketFloat',.0245758537,.0001,100.,place)
axis=g.input('Route axis','NodeSocketVector',(1,0,0),panel=place);side=g.input('Transverse axis','NodeSocketVector',(0,1,0),panel=place);up=g.input('Up axis','NodeSocketVector',(0,0,1),panel=place)
infoA=g.node('GeometryNodeObjectInfo');infoA.transform_space='RELATIVE';g.link(A,infoA.inputs['Object']);infoB=g.node('GeometryNodeObjectInfo');infoB.transform_space='RELATIVE';g.link(Bobj,infoB.inputs['Object']);delta=g.vop('SUBTRACT',infoB.outputs['Location'],infoA.outputs['Location']);length=g.vop('LENGTH',delta);use_anchor=op('MULTIPLY',anchor_mode,op('GREATER_THAN',length,.000001));auto_axis=g.vop('NORMALIZE',delta)
fallback=g.switch(op('GREATER_THAN',op('ABSOLUTE',g.vop('DOT_PRODUCT',auto_axis,(1,0,0))),.95),(0,1,0),(1,0,0),'VECTOR');bad_hint=op('MAXIMUM',op('LESS_THAN',g.vop('LENGTH',up),.000001),op('GREATER_THAN',op('ABSOLUTE',g.vop('DOT_PRODUCT',auto_axis,g.vop('NORMALIZE',up))),.95));hint=g.switch(bad_hint,fallback,g.vop('NORMALIZE',up),'VECTOR');auto_side=g.vop('NORMALIZE',g.vop('CROSS_PRODUCT',auto_axis,hint));auto_up=g.vop('NORMALIZE',g.vop('CROSS_PRODUCT',auto_side,auto_axis))
origin=g.switch(use_anchor,infoA.outputs['Location'],origin,'VECTOR');axis=g.switch(use_anchor,auto_axis,axis,'VECTOR');side=g.switch(use_anchor,auto_side,side,'VECTOR');up=g.switch(use_anchor,auto_up,up,'VECTOR');gap=g.switch(use_anchor,length,gap)
matpanel=g.panel('4 Per-instance materials',True);use_mats=g.input('Use material overrides','NodeSocketBool',False,panel=matpanel);outmat=g.input('Outgoing material','NodeSocketMaterial',None,panel=matpanel);retmat=g.input('Reflected material','NodeSocketMaterial',None,panel=matpanel)
# Seed0 reproduces approved variations exactly; other seeds are time-stable.
seed=p['Variation seed'];offsets=[];gains=[];widths=[]
for j in range(5):
 def pattern(original,salt):return g.switch(op('LESS_THAN',seed,.5),original,op('SINE',op('ADD',op('MULTIPLY',seed,78.233+salt),(j+1)*(12.9898+salt))))
 offsets.append(op('ADD',op('MULTIPLY',j,p['Pulse spacing']),op('MULTIPLY',op('MINIMUM',p['Spacing variation'],op('MULTIPLY',.45,p['Pulse spacing'])),pattern([0,-1,0,.8,.2][j],0))))
 gains.append(op('ADD',1,op('MULTIPLY',p['Amplitude variation'],pattern([0,-1,-.4,-.7,.1][j],2))))
 widths.append(op('MAXIMUM',.1,op('ADD',1,op('MULTIPLY',p['Width variation'],pattern([0,.923076923076923,-1,.5,-.3][j],4)))))
last=offsets[0]
for j in range(1,5):last=g.switch(op('GREATER_THAN',p['Pulse count'],j),offsets[j],last)
D=g.switch(op('GREATER_THAN',local['Train duration override'],0),local['Train duration override'],op('MAXIMUM',1.,op('ADD',last,p['Tail allowance'])))
time=g.node('GeometryNodeInputSceneTime');fps=g.switch(op('GREATER_THAN',op('ABSOLUTE',time.outputs['Seconds']),.000001),op('DIVIDE',time.outputs['Frame'],time.outputs['Seconds']),p['Reference FPS'])
tn=g.node('GeometryNodeGroup');tn.node_tree=tim.g
for name,value in local.items():g.link(value,tn.inputs[name])
for name,value in [('Frame',time.outputs['Frame']),('Scene FPS',fps),('Reference FPS',p['Reference FPS']),('Train duration',D)]:g.link(value,tn.inputs[name])
t=tn.outputs['Time'];RO=tn.outputs['Return offset'];TR=tn.outputs['Return travel'];DR=tn.outputs['Return duration'];T=local['Travel frames'];N=p['Strand count'];u=g.attr('wf17_u');index=g.attr('wf17_strand');ring=g.attr('wf17_ring');fraction=g.switch(op('GREATER_THAN',N,1),op('DIVIDE',index,op('MAXIMUM',op('SUBTRACT',N,1),1)),.5);v=op('SUBTRACT',op('MULTIPLY',fraction,2),1)
parts=[]
def setmat(geo,material):
 n=g.node('GeometryNodeSetMaterial');g.link(geo,n.inputs['Geometry']);g.set(material,n.inputs['Material']);return n.outputs['Geometry']
def custom(geo,material):return g.switch(use_mats,setmat(geo,material),geo,'GEOMETRY')
def gaussian(x,center,width):return op('EXPONENT',op('MULTIPLY',-1,op('POWER',op('DIVIDE',op('SUBTRACT',x,center),op('MAXIMUM',width,.001)),2)))
for reverse in [False,True]:
 distance=op('SUBTRACT',1,u) if reverse else u;stage=op('SUBTRACT',t,RO) if reverse else t;travel=TR if reverse else T;scale=local['Return train scale'] if reverse else 1
 age=op('DIVIDE',op('SUBTRACT',stage,op('MULTIPLY',travel,distance)),scale)
 enabled=op('MULTIPLY',local['Enabled'],op('SUBTRACT',1,op('COMPARE',local['Mode 0 Both 1 Send 2 Return'],1 if reverse else 2)))
 if reverse:enabled=op('MULTIPLY',enabled,local['Reflection enabled'])
 active=op('MULTIPLY',enabled,op('MULTIPLY',op('LESS_THAN',index,N),op('MULTIPLY',op('GREATER_THAN',age,0),op('LESS_THAN',age,D))))
 geo=g.delete(g.i.outputs['Geometry'],op('SUBTRACT',1,active))
 edge=op('MULTIPLY',g.clamp(op('DIVIDE',age,p['Head fade'])),g.clamp(op('DIVIDE',op('SUBTRACT',D,age),p['Tail fade'])))
 signal=0
 for j in range(5):
  agej=op('ADD',op('DIVIDE',op('SUBTRACT',age,offsets[j]),op('MULTIPLY',op('MULTIPLY',op('ADD',1,op('MULTIPLY',p['Dispersion'],distance)),widths[j]),p['Pulse width'])),op('MULTIPLY',p['Strand phase offset'],v))
  wave=op('ADD',op('ADD',op('MULTIPLY',op('MULTIPLY',-1,p['Pre dip']),gaussian(agej,1.3,.45)),gaussian(agej,2.1,p['Spike width'])),op('ADD',op('MULTIPLY',op('MULTIPLY',-1,p['Undershoot']),gaussian(agej,2.7,.4)),op('MULTIPLY',p['Rebound'],gaussian(agej,4.3,.9))))
  tail=op('MULTIPLY',p['Ringing'],op('MULTIPLY',op('SINE',op('DIVIDE',op('MULTIPLY',math.tau,op('SUBTRACT',agej,5)),p['Ring period'])),op('EXPONENT',op('DIVIDE',op('SUBTRACT',5,agej),p['Ring decay']))))
  tail=op('MULTIPLY',tail,op('MULTIPLY',op('GREATER_THAN',agej,5),op('LESS_THAN',agej,12)))
  signal=op('ADD',signal,op('MULTIPLY',op('GREATER_THAN',p['Pulse count'],j),op('MULTIPLY',gains[j],op('ADD',wave,tail))))
 envelope=op('ADD',p['End height fraction'],op('MULTIPLY',op('SUBTRACT',1,p['End height fraction']),op('POWER',op('SINE',op('MULTIPLY',math.pi,u)),2)))
 amp=p['Echo strength'] if reverse else 1
 if reverse:amp=op('MULTIPLY',amp,g.switch(local['Flip reflected pulse'],-1,1))
 z=op('DIVIDE',op('MULTIPLY',op('MULTIPLY',op('MULTIPLY',op('MULTIPLY',p['Height m'],quick['Strength multiplier']),envelope),edge),op('MULTIPLY',signal,amp)),op('ADD',1,op('MULTIPLY',p['Attenuation'],distance)))
 radius=op('MULTIPLY',op('MULTIPLY',p['Strand radius m'],quick['Radius multiplier']),edge);theta=op('MULTIPLY',ring,math.pi/2)
 z=op('MULTIPLY',op('ADD',z,op('MULTIPLY',radius,op('SINE',theta))),op('ADD',1,op('MULTIPLY',v,p['Strand separation'])))
 y=op('ADD',op('MULTIPLY',op('MULTIPLY',op('MULTIPLY',.5,p['Ribbon depth m']),quick['Width multiplier']),op('MULTIPLY',v,edge)),op('MULTIPLY',radius,op('COSINE',theta)))
 position=g.vop('ADD',origin,g.vop('ADD',g.vop('SCALE',axis,op('MULTIPLY',gap,u)),g.vop('ADD',g.vop('SCALE',side,y),g.vop('SCALE',up,z))))
 node=g.node('GeometryNodeSetPosition');g.link(geo,node.inputs['Geometry']);g.link(position,node.inputs['Position']);geo=node.outputs['Geometry']
 material_index=op('ADD',op('ROUND',op('MULTIPLY',fraction,16)),17 if reverse else 0);node=g.node('GeometryNodeSetMaterialIndex');g.link(geo,node.inputs['Geometry']);g.link(material_index,node.inputs['Material Index']);geo=node.outputs['Geometry'];geo=custom(geo,retmat if reverse else outmat);geo=g.store(geo,'wf17_component',2 if reverse else 1,'INT');geo=g.store(geo,'wf17_age',age);parts.append(geo)
 # Markers wait at the endpoint until the complete tail arrives, matching approval.
 duration=DR if reverse else D;finish=op('ADD',travel,duration);stage_active=op('MULTIPLY',enabled,op('MULTIPLY',op('GREATER_THAN',stage,-.000001),op('LESS_THAN',stage,op('ADD',finish,.000001))))
 for tailflag in [False,True]:
  progress=g.clamp(op('DIVIDE',op('SUBTRACT',stage,duration if tailflag else 0),travel));progress=op('SUBTRACT',1,progress) if reverse else progress
  position=g.vop('ADD',origin,g.vop('SCALE',axis,op('MULTIPLY',gap,progress)));sphere=g.node('GeometryNodeMeshUVSphere');sphere.inputs['Segments'].default_value=12;sphere.inputs['Rings'].default_value=6;g.link(p['Tail radius m'] if tailflag else p['Head radius m'],sphere.inputs['Radius']);transform=g.node('GeometryNodeTransform');g.link(sphere.outputs['Mesh'],transform.inputs['Geometry']);g.link(position,transform.inputs['Translation']);marker=setmat(transform.outputs['Geometry'],materials[34+(2 if reverse else 0)+(1 if tailflag else 0)]);marker=custom(marker,retmat if reverse else outmat);marker=g.store(marker,'wf17_component',3+(2 if reverse else 0)+(1 if tailflag else 0),'INT');show=op('MULTIPLY',stage_active,op('MULTIPLY',p['Show head tail'],quick['Show markers']));parts.append(g.switch(show,marker,None,'GEOMETRY'))
join=g.node('GeometryNodeJoinGeometry')
for geo in parts:g.link(geo,join.inputs['Geometry'])
geo=join.outputs['Geometry']
for name in ['Send head arrival','Send tail arrival','Return start','Return head arrival','Return tail arrival','Cycle frames']:geo=g.store(geo,'wf17_'+name,tn.outputs[name])
g.link(geo,g.o.inputs['Geometry']);mod=field.modifiers.new('PULSE SYSTEM — local timing and placement','NODES');mod.node_group=g.g
ctrl['README']='Shared approved pulse style. Edit this modifier for common shape/colors. Instances retain local timing, anchors and overrides.';field['README']='Live native GN, no baked shape keys. Default matches approved quickv006. Style master + per-instance timing/route/material controls. Authored display, not a calibrated acoustic model.'
text=bpy.data.texts.new('START HERE approved pulse v017');text.write('Approved sharp finite-pulse system. WF_MASTER_CONTROLS owns reusable pulse shape/variation/count/colors/strands. WF_PULSE_FIELD owns timing/placement/loop/material overrides. Defaults: start5, travel16, auto train20, return after tail+2, return travel16, three varied pulses, cyan/violet, separation0.65. Readouts: head21, tail41, return43, head59, tail79; loop96. Optional Fit end frame scales complete event, Follow scene FPS preserves duration. Timing sub-group is reusable for shot cues. No cameras, lights, keys, handlers or runtime Python. Controls have finite documented ranges; inspect short/tightly compressed windows at delivery FPS. Oldv015/v016 retained.\n')
s.frame_set(18);bpy.context.view_layer.objects.active=ctrl;ctrl.select_set(True)
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='PROPERTIES':area.spaces.active.context='MODIFIER'
  if area.type=='VIEW_3D':
   v=area.spaces.active;v.clip_start=.00001;v.clip_end=10;v.shading.type='SOLID';v.shading.color_type='MATERIAL';v.overlay.show_overlays=False;v.region_3d.view_location=(.0122879,0,.001);v.region_3d.view_distance=.08;v.region_3d.view_rotation=Vector((0,-.08,.035)).to_track_quat('Z','Y')
bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
manifest={'native':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'approved_reference':'Waveform_direction_quick_v006.blend','objects':[ctrl.name,field.name],'field_group':g.g.name,'timing_group':tim.g.name,'style':{x[0]:x[2] for x in STYLE},'colors':dict(COLORS),'timing':{x[0]:x[2] for x in TIMING},'capacity':{'pulses':5,'strands':17,'route_samples':513},'counts':{'objects':len(bpy.data.objects),'meshes':len(bpy.data.meshes),'materials':len(bpy.data.materials),'groups':len(bpy.data.node_groups),'libraries':len(bpy.data.libraries),'cameras':len(bpy.data.cameras)},'runtime':'native GN and simple material drivers; no handlers, autoexec scripts or shape-key baking','consumers':['Waveform_demo_v017 only until explicit shot migration']}
(B/'Waveform_interface_v017.json').write_text(json.dumps(manifest,indent=2));print('PULSE_V017_BUILT',manifest['counts'])
