import bpy,numpy as np,math,pathlib,json,time,os,hashlib
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v013';O.mkdir(parents=True,exist_ok=True);P=T/'Previews/Ribbon_v013';P.mkdir(parents=True,exist_ok=True);s=bpy.context.scene
C={'start':8,'source_duration':30,'one_way_frames':12,'carrier_period_frames':7.5,'echo_strength':.5,'height_limit_m':.0400390625,'width_limit_m':.0400000084,'strand_count':32,'route_samples':180,'fps':24,'frames':96}
# Replace only owned older proof packets in the new consumer file.
for name in ['OUTGOING_FINITE_PACKET','RETURN_FINITE_PACKET','RIBBON_ANCHORED_FORMATION_32_FILAMENTS']:
 ob=bpy.data.objects.get(name)
 if ob:
  data=ob.data;bpy.data.objects.remove(ob,do_unlink=True)
  if data.users==0:bpy.data.meshes.remove(data)
for name in ['EMISSION_ON_SAME_SENSOR','EXACT_WALL_CONTACT_RIPPLE','SAME_SENSOR_RECEIPT','POST_RECEIPT_WALL_MEASUREMENT']:
 ob=bpy.data.objects[name];ob.animation_data_clear();ob.hide_render=True
p=json.loads((T/'ribbon-build_v010.json').read_text());a=Vector(p['path_start']);b=Vector(p['path_end']);axis=b-a;up=Vector((0,0,1));depth=axis.normalized().cross(up).normalized();N=C['route_samples'];K=C['strand_count'];u=np.repeat(np.tile(np.linspace(0,1,N+1),K),4);v=np.repeat(np.repeat(np.linspace(-1,1,K),N+1),4);q=np.tile(np.arange(4),K*(N+1));base=np.outer(u,np.array(axis));radius=.000018;offset=np.outer(np.cos(q*math.tau/4)*radius,np.array(up))+np.outer(np.sin(q*math.tau/4)*radius,np.array(depth));faces=[]
for j in range(K):
 for i in range(1,N+1):
  k=(j*(N+1)+i)*4
  for z in range(4):faces.append((k-4+z,k-4+(z+1)%4,k+(z+1)%4,k+z))
def component(age,echo=False):
 valid=(age>0)&(age<C['source_duration']);envelope=np.sin(np.pi*np.clip(age/C['source_duration'],0,1))**2*valid;phase=math.tau*age/C['carrier_period_frames'];strandphase=1.15*v+.22*np.sin(math.pi*v)
 if echo:wave=.82*np.sin(phase+.8+strandphase)+.18*np.sin(1.65*phase-.5+.8*v)
 else:wave=.73*np.sin(phase+strandphase)+.27*np.sin(1.65*phase+.65+1.8*v)
 return envelope*wave*(.85+.15*np.cos(v*math.pi/2)),envelope
def field(f):
 out,eo=component(f-C['start']-C['one_way_frames']*u);ret,er=component(f-C['start']-C['one_way_frames']*(2-u),True);return out+C['echo_strength']*ret,np.maximum(eo,er*.75),out,ret
# One constant normalization for the entire clip; never renormalize per frame.
raw=[field(f)[0] for f in range(1,C['frames']+1)];maxspan=max(float(np.ptp(x)) for x in raw);scale=C['height_limit_m']/maxspan
me=bpy.data.meshes.new('COHERENT_EVOLVING_FIELD_MESH');me.from_pydata(base+offset,[],faces);me.update()
for name,data in [('route_u',u),('strand_v',(v+1)/2)]:att=me.attributes.new(name,'FLOAT','POINT');att.data.foreach_set('value',data)
ob=bpy.data.objects.new('COHERENT_EVOLVING_FIELD_v013',me);s.collection.objects.link(ob);ob.location=a;ob.shape_key_add(name='Anchored domain');me.shape_keys.use_relative=False;checks=[]
for f in range(1,C['frames']+1):
 h,e,out,ret=field(f);coords=base+np.outer(h*scale,np.array(up))+np.outer(v*C['width_limit_m']*.5*np.sqrt(e),np.array(depth))+offset;key=ob.shape_key_add(name=f'Field_f{f:03}');key.interpolation='KEY_LINEAR';key.data.foreach_set('co',coords.reshape(-1));me.shape_keys.eval_time=key.frame;me.shape_keys.keyframe_insert('eval_time',frame=f)
 if f in [1,12,18,22,26,30,34,38,46,54,62,68,96]:checks.append({'frame':f,'geometry_hash':hashlib.sha256(coords.tobytes()).hexdigest(),'height_m':float(np.ptp(coords[:,2])),'outgoing_energy':float(np.mean(out*out)),'echo_energy':float(np.mean((ret*C['echo_strength'])**2)),'active_route_bounds':[float(u[e>1e-5].min()),float(u[e>1e-5].max())] if np.any(e>1e-5) else None})
mat=bpy.data.materials.new('EVOLVING_FIELD_SMOOTH_VISIBILITY');mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');mix=nt.nodes.new('ShaderNodeMixShader');tr=nt.nodes.new('ShaderNodeBsdfTransparent');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(tr.outputs[0],mix.inputs[1]);nt.links.new(em.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0]);route=nt.nodes.new('ShaderNodeAttribute');route.attribute_name='route_u';layer=nt.nodes.new('ShaderNodeAttribute');layer.attribute_name='strand_v';ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.11,.04,.6,1);ramp.color_ramp.elements[1].color=(.025,.85,1,1);nt.links.new(layer.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],em.inputs[0]);em.inputs[1].default_value=3.5
clock=nt.nodes.new('ShaderNodeValue');clock.name='CINEMATIC_FRAME'
def op(typ,a,b=None):
 n=nt.nodes.new('ShaderNodeMath');n.operation=typ
 if hasattr(a,'bl_idname'):nt.links.new(a,n.inputs[0])
 else:n.inputs[0].default_value=a
 if b is not None:
  if hasattr(b,'bl_idname'):nt.links.new(b,n.inputs[1])
  else:n.inputs[1].default_value=b
 return n.outputs[0]
def env(travel):
 age=op('SUBTRACT',op('SUBTRACT',clock.outputs[0],C['start']),op('MULTIPLY',travel,C['one_way_frames']));phase=op('DIVIDE',age,C['source_duration']);bounded=op('MINIMUM',op('MAXIMUM',phase,0),1);return op('POWER',op('SINE',op('MULTIPLY',bounded,math.pi)),2)
eo=env(route.outputs['Fac']);er=op('MULTIPLY',env(op('SUBTRACT',2,route.outputs['Fac'])),.75);alpha=op('MAXIMUM',eo,er);alpha=op('POWER',alpha,.65);nt.links.new(alpha,mix.inputs[0]);mat.surface_render_method='DITHERED';mat.use_transparency_overlap=False;me.materials.append(mat)
for f in range(1,C['frames']+1):clock.outputs[0].default_value=f;clock.outputs[0].keyframe_insert('default_value',frame=f)
# Preserve exact original face/wall positions; change cue timing only.
for source,name,start,end,power in [('EMISSION_ON_SAME_SENSOR','FIELD_EMISSION',8,38,2.2),('EXACT_WALL_CONTACT_RIPPLE','FIELD_WALL_CONTACT',20,50,3.8),('SAME_SENSOR_RECEIPT','FIELD_SENSOR_RECEIPT',32,64,3.2),('POST_RECEIPT_WALL_MEASUREMENT','FIELD_MEASUREMENT_AFTER_RECEIPT',68,96,2.8)]:
 old=bpy.data.objects[source];cue=old.copy();cue.data=old.data.copy();cue.animation_data_clear();cue.name=name;s.collection.objects.link(cue);m=old.data.materials[0].copy();m.node_tree.animation_data_clear();cue.data.materials.clear();cue.data.materials.append(m);emission=next(n for n in m.node_tree.nodes if n.type=='EMISSION');cue.scale=(1,1,1)
 for f in range(1,97):
  active=start<f<=end if 'MEASUREMENT' not in name else start<=f<=end;t=max(0,min(1,(f-start)/max(1,end-start)));value=power*(.45+.55*math.sin(math.pi*t)**2) if active else 0
  cue.hide_render=not active;cue.keyframe_insert('hide_render',frame=f);emission.inputs[1].default_value=value;emission.inputs[1].keyframe_insert('default_value',frame=f)
  if 'WALL_CONTACT' in name:cue.scale=(1+t,)*3;cue.keyframe_insert('scale',frame=f)
s.frame_start=1;s.frame_end=96;s.render.fps=24;s.render.resolution_x=640;s.render.resolution_y=360;s.eevee.taa_render_samples=16;s.frame_set(26);target=O/'S02_rolling-wave-field_v013.blend';bpy.ops.wm.save_as_mainfile(filepath=str(target),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(target));bench=[]
for f in [18,22,26,30,38,54]:
 s.frame_set(f);s.render.filepath=str(P/f'field_{f:03}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;bench.append({'frame':f,'seconds':dt});(T/'field-benchmarks_v013.json').write_text(json.dumps(bench,indent=2))
 if dt>=5:raise RuntimeError('STOP frame cap')
(T/'field-model_v013.json').write_text(json.dumps({'controls':C,'constant_height_normalization':scale,'raw_max_frame_span':maxspan,'checks':checks,'sensor_world':list(a),'wall_world':list(b),'camera':s.camera.name,'matrix':[list(r) for r in ob.matrix_world],'model':'authored multi-frequency outgoing plus0.5 delayed reflected field; strand-coordinated phase; sine-squared temporal envelope; smooth opacity; not measuredRF or physical medium displacement','prior_source':'v012 context preserved; no sourceCSV claim for new field','timing':{'outgoing_source':[8,38],'wall_arrival_tail':[20,50],'sensor_receipt':[32,62],'measurement_starts':68},'stored':'96 absolute shape samples, no handlers'},indent=2));print('FIELD_BENCH',json.dumps(bench))
