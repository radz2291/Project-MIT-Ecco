import bpy,math,json,pathlib,hashlib,time,os,csv
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v010';O.mkdir(parents=True,exist_ok=True);P=T/'Previews/Ribbon_v010';P.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.frame_set(305)
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
# v007 is read-only input; remove only its pressure display from this new consumer.
for o in list(bpy.data.objects):
 if o.name.startswith('PRESSURE_'):o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
projection=json.loads((T/'event-projection.json').read_text());a=Vector(projection['frames']['300']['DW 1 SEND front0 core']['world']);b=Vector(projection['frames']['309']['DW 1 fixed native contact pin']['world']);axis=b-a
dep=bpy.context.evaluated_depsgraph_get()
for inst in dep.object_instances:
 if inst.object.name=='TEMP | Imaging port 2 | removable acoustic cap':
  M=inst.matrix_world.copy();coords=[M@v.co for v in inst.object.data.vertices];break
vertical=Vector((0,0,1));depth=axis.normalized().cross(vertical).normalized();height=max(p.dot(vertical) for p in coords)-min(p.dot(vertical) for p in coords);width=max(p.dot(depth) for p in coords)-min(p.dot(depth) for p in coords)
rows=list(csv.DictReader((R/'04-Production/Shared/Assets/Acoustics/PressureField_v005/Data/source_pulse.csv').open()));values=[float(r['amplitude']) for r in rows]
def sample(u):
 x=(.3125+.3125*max(0,min(1,u)))*(len(values)-1);i=min(int(x),len(values)-2);return values[i]*(1-(x-i))+values[i+1]*(x-i)
N=360;K=32
raw=[[sample(max(0,min(1,u+.025*v*math.sin(math.pi*u))))*(.65+.35*((v+1)/2)**.8)*math.sin(math.pi*u)**.3 for u in [i/N for i in range(N+1)]] for v in [-1+2*j/(K-1) for j in range(K)]]
low=min(map(min,raw));high=max(map(max,raw));scale=height/(high-low)
verts=[];faces=[];uv=[];strand=[]
# Fixed thin filaments. Depth spreads across sensor width, with tapered endpoints.
for j in range(K):
 v=-1+2*j/(K-1)
 for i in range(N+1):
  u=i/N;taper=math.sin(math.pi*u)**.65
  z=raw[j][i]*height*.5/(high if raw[j][i]>=0 else -low);center=axis*u+vertical*z+depth*(v*width*.5*taper)
  for q in range(4):
   ang=q*math.tau/4;verts.append(tuple(center+vertical*(math.cos(ang)*height*.0008)+depth*(math.sin(ang)*height*.0008)));uv.append(u);strand.append(j/(K-1))
  if i:
   k=(j*(N+1)+i)*4
   for q in range(4):faces.append((k-4+q,k-4+(q+1)%4,k+(q+1)%4,k+q))
mesh=bpy.data.meshes.new('RIBBON_FIXED_FILAMENT_MESH');mesh.from_pydata(verts,[],faces);mesh.update()
for name,data in [('route_u',uv),('strand_v',strand)]:
 att=mesh.attributes.new(name,'FLOAT','POINT');att.data.foreach_set('value',data)
ob=bpy.data.objects.new('RIBBON_FIXED_32_FILAMENTS',mesh);s.collection.objects.link(ob);ob.location=a
mat=bpy.data.materials.new('RIBBON_CYAN_VIOLET_EMISSION');mat.use_nodes=True;ns=mat.node_tree.nodes;ns.clear();links=mat.node_tree.links
out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');links.new(em.outputs[0],out.inputs[0]);attr=ns.new('ShaderNodeAttribute');attr.attribute_name='route_u';layer=ns.new('ShaderNodeAttribute');layer.attribute_name='strand_v'
ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.07,.025,.46,1);ramp.color_ramp.elements[1].color=(.025,.75,1,1);links.new(layer.outputs['Fac'],ramp.inputs[0]);links.new(ramp.outputs[0],em.inputs[0])
head=ns.new('ShaderNodeValue');head.name='Traveling light position only'
def mathnode(op,a,b=None):
 n=ns.new('ShaderNodeMath');n.operation=op
 if hasattr(a,'bl_idname'):links.new(a,n.inputs[0])
 else:n.inputs[0].default_value=a
 if b is not None:
  if hasattr(b,'bl_idname'):links.new(b,n.inputs[1])
  else:n.inputs[1].default_value=b
 return n.outputs[0]
x=mathnode('SUBTRACT',attr.outputs['Fac'],head.outputs[0]);x=mathnode('ABSOLUTE',x);x=mathnode('MULTIPLY',x,6);x=mathnode('SUBTRACT',1,x);x=mathnode('MAXIMUM',x,0);x=mathnode('POWER',x,2);gain=ns.new('ShaderNodeValue');gain.name='Outbound then weaker return';x=mathnode('MULTIPLY',x,gain.outputs[0]);x=mathnode('ADD',x,.8);strandgain=mathnode('POWER',layer.outputs['Fac'],4);strandgain=mathnode('MULTIPLY',strandgain,1.8);strandgain=mathnode('ADD',strandgain,.22);x=mathnode('MULTIPLY',x,strandgain);links.new(x,em.inputs[1]);mesh.materials.append(mat)
for f in range(298,325):
 h=(f-300)/9 if f<=309 else 1-(f-309)/9
 head.outputs[0].default_value=h;head.outputs[0].keyframe_insert('default_value',frame=f)
 gain.outputs[0].default_value=5 if f<=309 else 2.5;gain.outputs[0].keyframe_insert('default_value',frame=f)
# Soft optical glow, no geometry deformation.
g=bpy.data.node_groups.new('Ribbon optical bloom','CompositorNodeTree');g.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=g
rn=g.nodes.new('CompositorNodeRLayers');gl=g.nodes.new('CompositorNodeGlare');gl.inputs['Type'].default_value='Fog Glow';gl.inputs['Threshold'].default_value=.3;gl.inputs['Strength'].default_value=.7;go=g.nodes.new('NodeGroupOutput');g.links.new(rn.outputs['Image'],gl.inputs['Image']);g.links.new(gl.outputs['Image'],go.inputs['Image'])
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=32;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.frame_set(305)
context=O/'S02_ribbon-context_v010.blend';bpy.ops.wm.save_as_mainfile(filepath=str(context),relative_remap=True)
s.render.filepath=str(P/'context_305.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
record={'cap_name':'TEMP | Imaging port 2 | removable acoustic cap','cap_matrix':[list(r) for r in M],'full_height_m':height,'full_width_m':width,'peak_to_trough_m':(high-low)*scale,'path_start':list(a),'path_end':list(b),'filaments':K,'source_sample_csv':'PressureField_v005/Data/source_pulse.csv','display_window_s':[2.5e-6,5e-6],'taper':'sin(pi*u)**0.3; fixed artistic window' ,'mapping':'Assumed normalized pulse becomes artistic static height; depth strands have fixed sample offset. Not actual pressure displacement or measured ECCO waveform.','geometry_animation':False,'frame':305,'full_render_to_file_seconds':elapsed,'context_native':str(context),'context_camera':s.camera.name}
(T/'ribbon-build_v010.json').write_text(json.dumps(record,indent=2));print('RIBBON_BENCH',json.dumps(record))
if elapsed>=5:raise RuntimeError('STOP FRAME CAP')
# Isolated stage copy for reference look review; same ribbon geometry and dimensions.
for child in bpy.context.view_layer.layer_collection.children:child.exclude=True
for obj in s.collection.objects:
 if obj!=ob:obj.animation_data_clear();obj.hide_render=True
camdata=bpy.data.cameras.new('RIBBON_REVIEW_CAMERA');cam=bpy.data.objects.new('RIBBON_REVIEW_CAMERA',camdata);s.collection.objects.link(cam);cam.hide_render=False;target=a+axis*.5;cam.location=target+depth*.13+vertical*.035-axis.normalized()*.012;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=.095;camdata.clip_start=.001;s.camera=cam
s.world=bpy.data.worlds.new('RIBBON_BLACK_STAGE');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=0
bpy.ops.wm.save_as_mainfile(filepath=str(O/'Ribbon_dark-stage_v010.blend'),relative_remap=True)
s.render.filepath=str(P/'isolated_305.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;record['isolated_seconds']=elapsed;(T/'ribbon-build_v010.json').write_text(json.dumps(record,indent=2));print('ISOLATED_SECONDS',elapsed)
