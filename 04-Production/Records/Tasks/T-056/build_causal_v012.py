import bpy,numpy as np,math,pathlib,json,time,os,csv,hashlib
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v012';O.mkdir(parents=True,exist_ok=True);P=T/'Previews/Ribbon_v012';P.mkdir(parents=True,exist_ok=True);s=bpy.context.scene
old=bpy.data.objects['RIBBON_ANCHORED_FORMATION_32_FILAMENTS'];old.hide_render=True;old.hide_viewport=True
p=json.loads((T/'ribbon-build_v010.json').read_text());a=Vector(p['path_start']);b=Vector(p['path_end']);axis=b-a;D=axis.length;direction=axis.normalized();up=Vector((0,0,1));depth=direction.cross(up).normalized();N=240;K=32;width=.44
u=np.repeat(np.tile(np.linspace(0,1,N+1),K),4);v=np.repeat(np.repeat(np.linspace(-1,1,K),N+1),4);q=np.tile(np.arange(4),K*(N+1));base=np.outer(u,np.array(axis));radius=.000022;offset=np.outer(np.cos(q*math.tau/4)*radius,np.array(up))+np.outer(np.sin(q*math.tau/4)*radius,np.array(depth));faces=[]
for j in range(K):
 for i in range(1,N+1):
  k=(j*(N+1)+i)*4
  for z in range(4):faces.append((k-4+z,k-4+(z+1)%4,k+(z+1)%4,k+z))
rows=list(csv.DictReader((R/'04-Production/Shared/Assets/Acoustics/PressureField_v005/Data/source_pulse.csv').open()));samples=np.array([float(x['amplitude']) for x in rows]);st=np.linspace(0,1,len(samples))
def state(f,echo=False):
 front=(f-(66 if echo else 18))/(36 if echo else 30);travel=1-u if echo else u;phase=(front-travel)/width;inside=(phase>0)&(phase<1);clip=np.clip(phase,0,1);envelope=np.sin(np.pi*clip)**1.2;profile=np.interp(.3125+.3125*clip,st,samples)*envelope;profile*=inside
 reference=np.interp(.3125+.3125*np.linspace(0,1,2001),st,samples)*np.sin(np.pi*np.linspace(0,1,2001))**1.2
 profile=np.where(profile>=0,profile/max(reference),profile/abs(min(reference)))
 amp=.02001953125 if not echo else .010009765625
 # Display shape grows locally as the finite sampled packet passes; no object translation.
 z=profile*amp*(.75+.25*(v+1)/2);spread=(.0200000042 if not echo else .0100000021)*v*envelope*inside
 coords=base+np.outer(z,np.array(up))+np.outer(spread,np.array(depth))+offset
 return front,phase,coords
packets=[]
def mathnode(nt,op,a,b=None):
 n=nt.nodes.new('ShaderNodeMath');n.operation=op
 if hasattr(a,'bl_idname'):nt.links.new(a,n.inputs[0])
 else:n.inputs[0].default_value=a
 if b is not None:
  if hasattr(b,'bl_idname'):nt.links.new(b,n.inputs[1])
  else:n.inputs[1].default_value=b
 return n.outputs[0]
for echo in [False,True]:
 name='RETURN_FINITE_PACKET' if echo else 'OUTGOING_FINITE_PACKET';me=bpy.data.meshes.new(name);me.from_pydata(base+offset,[],faces);me.update();att=me.attributes.new('route_u','FLOAT','POINT');att.data.foreach_set('value',u);at=me.attributes.new('strand_v','FLOAT','POINT');at.data.foreach_set('value',(v+1)/2);ob=bpy.data.objects.new(name,me);s.collection.objects.link(ob);ob.location=a;ob.shape_key_add(name='Anchored domain');me.shape_keys.use_relative=False
 for i,f in enumerate(range(1,170)):
  key=ob.shape_key_add(name=f'Sampled_field_f{f:03}');key.interpolation='KEY_LINEAR';key.data.foreach_set('co',state(f,echo)[2].reshape(-1));me.shape_keys.eval_time=key.frame;me.shape_keys.keyframe_insert('eval_time',frame=f)
 mat=bpy.data.materials.new(name+'_signed_sample_display');mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');mix=nt.nodes.new('ShaderNodeMixShader');tr=nt.nodes.new('ShaderNodeBsdfTransparent');em=nt.nodes.new('ShaderNodeEmission');nt.links.new(tr.outputs[0],mix.inputs[1]);nt.links.new(em.outputs[0],mix.inputs[2]);nt.links.new(mix.outputs[0],out.inputs[0]);lay=nt.nodes.new('ShaderNodeAttribute');lay.attribute_name='strand_v';ramp=nt.nodes.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=((.19,.035,.65,1) if echo else (.025,.13,.65,1));ramp.color_ramp.elements[1].color=((.25,.48,1,1) if echo else (.03,.9,1,1));nt.links.new(lay.outputs['Fac'],ramp.inputs[0]);nt.links.new(ramp.outputs[0],em.inputs[0]);em.inputs[1].default_value=4 if not echo else 3
 route=nt.nodes.new('ShaderNodeAttribute');route.attribute_name='route_u';head=nt.nodes.new('ShaderNodeValue');head.name='Causal_front_route_coordinate';travel=mathnode(nt,'SUBTRACT',1,route.outputs['Fac']) if echo else route.outputs['Fac'];phase=mathnode(nt,'DIVIDE',mathnode(nt,'SUBTRACT',head.outputs[0],travel),width);low=mathnode(nt,'GREATER_THAN',phase,0);high=mathnode(nt,'LESS_THAN',phase,1);mask=mathnode(nt,'MULTIPLY',low,high);nt.links.new(mask,mix.inputs[0]);mat.surface_render_method='DITHERED';mat.use_transparency_overlap=False;me.materials.append(mat)
 for f in range(1,170):head.outputs[0].default_value=state(f,echo)[0];head.outputs[0].keyframe_insert('default_value',frame=f)
 packets.append(ob)
# Local circular cues on actual face planes, not arrows or HUD.
def cue(name,center,radius,color,events,solid=False):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.bevel_depth=.00007 if not solid else .00014;cu.bevel_resolution=1;sp=cu.splines.new('POLY');sp.points.add(63)
 for j,pt in enumerate(sp.points):ang=j*math.tau/64;pt.co=(*(depth*(radius*math.cos(ang))+up*(radius*math.sin(ang))),1)
 sp.use_cyclic_u=True;ob=bpy.data.objects.new(name,cu);s.collection.objects.link(ob);ob.location=center;mat=bpy.data.materials.new(name+'_light');mat.use_nodes=True;nt=mat.node_tree;nt.nodes.clear();em=nt.nodes.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1);out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(em.outputs[0],out.inputs[0]);cu.materials.append(mat)
 for f in range(1,169):
  gain=0;scale=1
  for start,end,strength,expand in events:
   if start<=f<=end:
    t=(f-start)/max(1,end-start);gain=max(gain,strength*(math.sin(math.pi*t)**.6 if expand else min(1,(f-start+1)/5)));scale=1+expand*t
  ob.hide_render=gain==0;ob.keyframe_insert('hide_render',frame=f);ob.scale=(scale,scale,scale);ob.keyframe_insert('scale',frame=f);em.inputs[1].default_value=gain;em.inputs[1].keyframe_insert('default_value',frame=f)
 return ob
wall=b-direction*.00012;sensor=a-direction*.0004
cue('EMISSION_ON_SAME_SENSOR',sensor,.017,(.03,.6,1),[(17,31,2.5,.1)])
cue('EXACT_WALL_CONTACT_RIPPLE',wall,.0018,(.1,.9,1),[(48,66,5,1.3)])
cue('SAME_SENSOR_RECEIPT',sensor,.017,(.3,.4,1),[(102,122,4,.08)])
cue('POST_RECEIPT_WALL_MEASUREMENT',wall,.0011,(.05,1,.55),[(124,168,2.8,0)],True)
s.frame_start=1;s.frame_end=168;s.render.fps=24;s.render.resolution_x=640;s.render.resolution_y=360;s.eevee.taa_render_samples=16;s.frame_set(36);target=O/'S02_causal-waveform-review_v012.blend';bpy.ops.wm.save_as_mainfile(filepath=str(target),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(target));records=[]
for f,label in [(36,'outgoing'),(54,'contact'),(84,'return'),(114,'receipt'),(140,'measurement')]:
 s.frame_set(f);s.render.filepath=str(P/f'{label}_{f:03}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'event':label,'seconds':dt});(T/'causal-benchmarks_v012.json').write_text(json.dumps(records,indent=2))
 if dt>=5:raise RuntimeError('Frame cap exceeded')
(T/'causal-timeline_v012.json').write_text(json.dumps({'source_context':'v011 fixed native305 review tableau','camera':s.camera.name,'sensor_world_m':list(a),'wall_world_m':list(b),'gap_m':D,'packet_width_fraction':width,'outgoing':{'start':18,'leading_wall_contact':48,'tail_at_wall':61.2},'wall_response':[48,66],'echo':{'start_at_wall':66,'leading_sensor_receipt':102,'tail_at_sensor':117.84},'sensor_reception_cue':[102,122],'measurement_mark':[124,168],'geometry':'sampled local height and transverse envelope on immutable route coordinates; no object motion','profile':'authored window of assumed400kHz pulse; artistic height field, not calibrated displacement/propagation','duration_s':7,'stored_animation':'absolute shape keys each frame, animated eval_time; shader masks outside finite support; no runtime handlers'},indent=2));print('V012_BENCH',json.dumps(records))
