import bpy,math,pathlib,json,os,numpy as np
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/Waveform_shared_v014';O.mkdir(parents=True,exist_ok=True)
SPECS=[('Playback Speed',1.,.1,4.),('Frequency Multiplier',1.,.25,4.),('Strength',1.,0.,1.),('Echo Strength',.5,0.,1.),('Decay Tightness',1.,.25,4.),('Source Duration Frames',30.,1.,240.),('One Way Frames',12.,1.,120.),('Reference Height m',.0400390625,.001,.08),('Width m',.0400000084,.001,.08),('Emission',3.5,0.,20.),('Strand Radius m',.000018,.000005,.0002),('Opacity Power',.65,.2,3.),('Color Violet',(.11,.04,.6,1)),('Color Cyan',(.025,.85,1,1))]
class G:
 def __init__(self,name):
  self.g=bpy.data.node_groups.new(name,'GeometryNodeTree');self.g.is_modifier=True;self.ins={};self.i=self.g.nodes.new('NodeGroupInput');self.o=self.g.nodes.new('NodeGroupOutput');self.socket('Geometry','NodeSocketGeometry',None);self.g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry')
 def socket(self,name,typ='NodeSocketFloat',default=0,lo=None,hi=None,description=''):
  x=self.g.interface.new_socket(name=name,in_out='INPUT',socket_type=typ);self.ins[name]=x.identifier
  if default is not None:x.default_value=default
  if lo is not None:x.min_value=lo
  if hi is not None:x.max_value=hi
  x.description=description;return self.i.outputs[name]
 def node(self,typ):return self.g.nodes.new(typ)
 def link(self,a,b):self.g.links.new(a,b)
 def set(self,a,b):
  if hasattr(a,'bl_idname'):self.link(a,b)
  else:b.default_value=a
 def op(self,typ,a,b=None):
  n=self.node('ShaderNodeMath');n.operation=typ;self.set(a,n.inputs[0]);
  if b is not None:self.set(b,n.inputs[1])
  return n.outputs[0]
 def vec(self,x,y,z):
  n=self.node('ShaderNodeCombineXYZ');self.set(x,n.inputs[0]);self.set(y,n.inputs[1]);self.set(z,n.inputs[2]);return n.outputs[0]
 def vop(self,typ,a,b=None):
  n=self.node('ShaderNodeVectorMath');n.operation=typ;self.set(a,n.inputs[0]);
  if b is not None:self.set(b,n.inputs[3] if typ=='SCALE' else n.inputs[1])
  return n.outputs[0]
 def attr(self,name,typ='FLOAT'):
  n=self.node('GeometryNodeInputNamedAttribute');n.data_type=typ;n.inputs['Name'].default_value=name;return n.outputs['Attribute']
 def store(self,geo,name,value,typ='FLOAT'):
  n=self.node('GeometryNodeStoreNamedAttribute');n.data_type=typ;n.domain='POINT';self.link(geo,n.inputs['Geometry']);n.inputs['Name'].default_value=name;self.set(value,n.inputs['Value']);return n.outputs['Geometry']
 def shared(self,obj,name,color=False):
  info=self.node('GeometryNodeObjectInfo');info.inputs['Object'].default_value=obj;info.transform_space='ORIGINAL';sample=self.node('GeometryNodeSampleIndex');sample.data_type='FLOAT_COLOR' if color else 'FLOAT';sample.domain='POINT';sample.inputs['Index'].default_value=0;self.link(info.outputs['Geometry'],sample.inputs['Geometry']);self.link(self.attr('wf_'+name,'FLOAT_COLOR' if color else 'FLOAT'),sample.inputs['Value']);return sample.outputs['Value']
 def choose(self,condition,a,b):
  n=self.node('GeometryNodeSwitch');n.input_type='FLOAT';self.set(condition,n.inputs['Switch']);self.set(a,n.inputs['True']);self.set(b,n.inputs['False']);return n.outputs['Output']
def value(mod,name,value):
 ident=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);getattr(mod.properties.inputs,ident).value=value

def material():
 m=bpy.data.materials.new('WF_SHARED_FIELD_MATERIAL');m.use_nodes=True;m.diffuse_color=(.025,.7,1,1);nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');mix=nt.nodes.new('ShaderNodeMixShader');tr=nt.nodes.new('ShaderNodeBsdfTransparent');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(tr.outputs[0],mix.inputs[1]);nt.links.new(em.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0])
 for attr,socket,outname in [('wf_alpha',mix.inputs[0],'Fac'),('wf_color',em.inputs[0],'Color'),('wf_emission',em.inputs[1],'Fac')]:n=nt.nodes.new('ShaderNodeAttribute');n.attribute_name=attr;nt.links.new(n.outputs[outname],socket)
 m.surface_render_method='DITHERED';m.use_transparency_overlap=False;return m
s=bpy.context.scene;old=bpy.data.objects['COHERENT_EVOLVING_FIELD_v013'];frames=[1,12,18,26,30,38,54,62,68,96];reference={}
for f in frames:
 s.frame_set(f);ev=old.evaluated_get(bpy.context.evaluated_depsgraph_get());a=np.empty(len(ev.data.vertices)*3);ev.data.vertices.foreach_get('co',a);reference[f]=a.reshape(-1,3)
col=bpy.data.collections.new('WF_SHARED_CONTROLS');s.collection.children.link(col);mesh=bpy.data.meshes.new('WF_CONTROL_POINT');mesh.from_pydata([(0,0,0)],[],[]);ctrl=bpy.data.objects.new('WF_MASTER_CONTROLS',mesh);col.objects.link(ctrl);ctrl['README']='Edit modifier MASTER CONTROLS, save source, reload consumers. Native GN, no handlers. Display values only.';cg=G('WF_MASTER_CONTROL_VALUES');geo=cg.i.outputs['Geometry']
for spec in SPECS:
 name,default=spec[:2];color=isinstance(default,tuple);sock=cg.socket(name,'NodeSocketColor' if color else 'NodeSocketFloat',default,None if color else spec[2],None if color else spec[3],description='Shared display control. Not physical calibration.');geo=cg.store(geo,'wf_'+name,sock,'FLOAT_COLOR' if color else 'FLOAT')
cg.link(geo,cg.o.inputs['Geometry']);cm=ctrl.modifiers.new('MASTER CONTROLS — shared across consumers','NODES');cm.node_group=cg.g
for spec in SPECS:value(cm,spec[0],spec[1])
fg=G('WF_FIELD_LIVE_v014');local={}
for name,default,lo,hi in [('Start Frame',8.,-10000,10000),('Playback Override',1.,.1,4.),('Duration Override',0.,0.,240.),('Travel Override',0.,0.,120.),('Echo Delay Frames',0.,0.,120.),('Return Travel Override',0.,0.,120.),('Outbound End Frame',0.,0.,10000.),('Return End Frame',0.,0.,10000.),('Lock Event Timing',0.,0.,1.),('Frequency Override',1.,.25,4.),('Strength Override',1.,0.,1.),('Echo Override',1.,0.,2.),('Decay Override',1.,.25,4.),('Radius Override',1.,.25,12.),('Width Override',1.,.1,2.),('Height Override',1.,.1,2.),('Gap Length m',.0245758528089,.0001,1.),('Preset 0 Open 1 Cased',0,0,1),('Enabled',1,0,1)]:local[name]=fg.socket(name,'NodeSocketInt' if name.startswith('Preset') else 'NodeSocketFloat',default,lo,hi,description='Local consumer control. Zero timing override uses shared default.')
for name,default in [('Route Axis',(1,0,0)),('Transverse Axis',(0,1,0)),('Up Axis',(0,0,1))]:local[name]=fg.socket(name,'NodeSocketVector',default)
shared={spec[0]:fg.shared(ctrl,spec[0],isinstance(spec[1],tuple)) for spec in SPECS};op=fg.op;u=fg.attr('route_u');v=op('SUBTRACT',op('MULTIPLY',fg.attr('strand_v'),2),1);scene=fg.node('GeometryNodeInputSceneTime');t=op('MULTIPLY',op('SUBTRACT',scene.outputs['Frame'],local['Start Frame']),op('MULTIPLY',fg.choose(local['Lock Event Timing'],1,shared['Playback Speed']),local['Playback Override']));duration=fg.choose(op('GREATER_THAN',local['Duration Override'],0),local['Duration Override'],shared['Source Duration Frames']);travel=fg.choose(op('GREATER_THAN',local['Travel Override'],0),local['Travel Override'],shared['One Way Frames']);cased=local['Preset 0 Open 1 Cased'];decay=op('MULTIPLY',shared['Decay Tightness'],op('MULTIPLY',local['Decay Override'],op('ADD',1,op('MULTIPLY',cased,.2))));freq=op('MULTIPLY',shared['Frequency Multiplier'],local['Frequency Override']);echo=op('MULTIPLY',shared['Echo Strength'],op('MULTIPLY',local['Echo Override'],op('SUBTRACT',1,op('MULTIPLY',cased,.2))))
def component(age,is_echo=False):
 phase=op('MULTIPLY',op('DIVIDE',age,7.5),op('MULTIPLY',math.tau,freq));ratio=op('DIVIDE',age,duration);bounded=op('MINIMUM',op('MAXIMUM',ratio,0),1);env=op('POWER',op('MAXIMUM',op('SINE',op('MULTIPLY',bounded,math.pi)),0),op('MULTIPLY',2,decay));env=op('MULTIPLY',env,op('MULTIPLY',op('GREATER_THAN',age,0),op('LESS_THAN',age,duration)));sp=op('ADD',op('MULTIPLY',1.15,v),op('MULTIPLY',.22,op('SINE',op('MULTIPLY',math.pi,v))))
 if is_echo:w=op('ADD',op('MULTIPLY',.82,op('SINE',op('ADD',op('ADD',phase,.8),sp))),op('MULTIPLY',.18,op('SINE',op('ADD',op('SUBTRACT',op('MULTIPLY',1.65,phase),.5),op('MULTIPLY',.8,v)))))
 else:w=op('ADD',op('MULTIPLY',.73,op('SINE',op('ADD',phase,sp))),op('MULTIPLY',.27,op('SINE',op('ADD',op('ADD',op('MULTIPLY',1.65,phase),.65),op('MULTIPLY',1.8,v)))))
 w=op('MULTIPLY',w,op('ADD',.85,op('MULTIPLY',.15,op('COSINE',op('MULTIPLY',math.pi/2,v)))));return op('MULTIPLY',env,w),env
returntravel=fg.choose(op('GREATER_THAN',local['Return Travel Override'],0),local['Return Travel Override'],travel)
out,eo=component(op('SUBTRACT',t,op('MULTIPLY',travel,u)));ret,er=component(op('SUBTRACT',op('SUBTRACT',t,op('ADD',travel,op('MULTIPLY',returntravel,op('SUBTRACT',1,u)))),local['Echo Delay Frames']),True)
for which,end in [('out','Outbound End Frame'),('ret','Return End Frame')]:
 gate=fg.choose(op('GREATER_THAN',local[end],0),op('LESS_THAN',scene.outputs['Frame'],local[end]),1)
 if which=='out':out=op('MULTIPLY',out,gate);eo=op('MULTIPLY',eo,gate)
 else:ret=op('MULTIPLY',ret,gate);er=op('MULTIPLY',er,gate)
height=op('MULTIPLY',op('ADD',out,op('MULTIPLY',echo,ret)),op('MULTIPLY',.019331816745520012,op('MULTIPLY',op('DIVIDE',shared['Reference Height m'],.0400390625),op('MULTIPLY',shared['Strength'],op('MULTIPLY',local['Strength Override'],local['Height Override'])))));env=op('MAXIMUM',eo,op('MULTIPLY',er,.75));spread=op('MULTIPLY',v,op('MULTIPLY',.5,op('MULTIPLY',shared['Width m'],op('MULTIPLY',local['Width Override'],op('SQRT',env)))));radius=op('MULTIPLY',shared['Strand Radius m'],local['Radius Override']);height=op('ADD',height,op('MULTIPLY',fg.attr('ring_cos'),radius));spread=op('ADD',spread,op('MULTIPLY',fg.attr('ring_sin'),radius));pos=fg.vop('ADD',fg.vop('SCALE',local['Route Axis'],op('MULTIPLY',u,local['Gap Length m'])),fg.vop('ADD',fg.vop('SCALE',local['Up Axis'],height),fg.vop('SCALE',local['Transverse Axis'],spread)));setp=fg.node('GeometryNodeSetPosition');fg.link(fg.i.outputs['Geometry'],setp.inputs['Geometry']);fg.link(pos,setp.inputs['Position']);geo=setp.outputs['Geometry'];alpha=op('MULTIPLY',op('POWER',env,shared['Opacity Power']),local['Enabled']);geo=fg.store(geo,'wf_alpha',alpha);geo=fg.store(geo,'wf_emission',shared['Emission']);mix=fg.node('ShaderNodeMixRGB');mix.blend_type='MIX';fg.link(fg.attr('strand_v'),mix.inputs[0]);fg.link(shared['Color Violet'],mix.inputs[1]);fg.link(shared['Color Cyan'],mix.inputs[2]);geo=fg.store(geo,'wf_color',mix.outputs[0],'FLOAT_COLOR');delete=fg.node('GeometryNodeDeleteGeometry');delete.domain='POINT';delete.mode='ALL';fg.link(geo,delete.inputs['Geometry']);fg.link(op('LESS_THAN',alpha,1e-7),delete.inputs['Selection']);setmat=fg.node('GeometryNodeSetMaterial');mat=material();setmat.inputs['Material'].default_value=mat;fg.link(delete.outputs['Geometry'],setmat.inputs['Geometry']);fg.link(setmat.outputs['Geometry'],fg.o.inputs['Geometry'])
# Base topology/data carries immutable parameter sites and original vertex index.
base=old.data.copy();base.name='WF_PARAMETER_DOMAIN';live=bpy.data.objects.new('WF_LIVE_FIELD',base);s.collection.objects.link(live);live.matrix_world=old.matrix_world.copy();live.shape_key_clear();n=len(base.vertices)
for name,data,typ in [('ring_cos',np.cos(np.tile(np.arange(4),n//4)*math.tau/4),'FLOAT'),('ring_sin',np.sin(np.tile(np.arange(4),n//4)*math.tau/4),'FLOAT'),('wf_index',np.arange(n),'INT')]:
 att=base.attributes.get(name) or base.attributes.new(name,typ,'POINT');att.data.foreach_set('value',data)
mod=live.modifiers.new('WAVEFORM — local overrides and timing','NODES');mod.node_group=fg.g
p=json.loads((T/'ribbon-build_v010.json').read_text());axis=Vector(p['path_end'])-Vector(p['path_start']);d=axis.normalized().cross(Vector((0,0,1))).normalized()
for name,val in [('Gap Length m',axis.length),('Route Axis',tuple(axis.normalized())),('Transverse Axis',tuple(d)),('Up Axis',(0,0,1))]:value(mod,name,val)
old.hide_render=True;old.hide_viewport=True
checks=[]
for f in frames:
 s.frame_set(f);bpy.context.view_layer.update();ev=live.evaluated_get(bpy.context.evaluated_depsgraph_get());ids=np.array([x.value for x in ev.data.attributes['wf_index'].data],dtype=int) if 'wf_index' in ev.data.attributes else np.array([],dtype=int);co=np.array([v.co[:] for v in ev.data.vertices]);err=float(np.max(np.abs(co-reference[f][ids]))) if len(ids) else 0;checks.append({'frame':f,'vertices':len(ids),'max_coordinate_error_m':err,'height_m':float(np.ptp(co[:,2])) if len(ids) else 0})
s.frame_set(30);bpy.context.view_layer.objects.active=ctrl;ctrl.select_set(True);target=O/'Waveform_shared_v014.blend';bpy.ops.wm.save_as_mainfile(filepath=str(target),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(target));(T/'shared-default-comparison_v014.json').write_text(json.dumps({'checks':checks,'pass':all(x['max_coordinate_error_m']<2e-6 for x in checks),'master':str(target),'node_group':fg.g.name,'master_controls':ctrl.name,'shared_collection':col.name,'controls':cg.ins,'local_controls':fg.ins,'note':'live native GN; invisible sites removed; compare active vertex indices to baked v013'},indent=2));print('DEFAULT_COMPARISON',json.dumps(checks))
