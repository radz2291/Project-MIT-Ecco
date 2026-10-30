import bpy,pathlib,json,math,time,os,hashlib,numpy as np
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';O=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v011';O.mkdir(parents=True,exist_ok=True);P=T/'Previews/Ribbon_v011';P.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene;s.frame_set(305);ob=bpy.data.objects['RIBBON_FIXED_32_FILAMENTS'];ob.name='RIBBON_ANCHORED_FORMATION_32_FILAMENTS';source_camera=bpy.data.objects['CAM_S01_Continuous'];snapshot=[(o,o.matrix_world.copy(),o.hide_render,o.hide_viewport) for o in s.objects if not o.library and o!=source_camera and o!=ob]
# Freeze this review-only context tableau at native305; preserve original camera action separately.
for o,m,h,v in snapshot:o.animation_data_clear()
for o,m,h,v in snapshot:o.matrix_world=m;o.hide_render=h;o.hide_viewport=v
for mat in bpy.data.materials:
 if not mat.library and mat!=ob.data.materials[0]:mat.animation_data_clear()
mesh=ob.data;n=len(mesh.vertices);full=np.empty(n*3);mesh.vertices.foreach_get('co',full);full=full.reshape(-1,3);basis=full.copy();radius=.0400390625*.0008;ring=np.tile(np.cos(np.arange(4)*math.tau/4)*radius,n//4);basis[:,2]=ring;profile=full[:,2]-ring;mesh.vertices.foreach_set('co',basis.reshape(-1));ob.shape_key_add(name='Flat anchored ribbon');route=np.empty(n);mesh.attributes['route_u'].data.foreach_get('value',route);centers=np.linspace(0,1,17);keys=[]
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def field(u,f):
 outgoing=smooth((f-(8+28*u))/12)*(1-smooth((f-54)/16))
 delay=65+20*(1-u);age=f-delay
 echo=.52*smooth(age/9)*(1-smooth((f-105)/15))*math.cos(max(0,age-12)*.055)
 return max(-1,min(1,outgoing+echo))
for k,c in enumerate(centers):
 key=ob.shape_key_add(name=f'Local_height_{k:02}');key.slider_min=-1;key.slider_max=1;v=basis.copy();weight=np.maximum(0,1-np.abs(route-c)*16);v[:,2]+=profile*weight;key.data.foreach_set('co',v.reshape(-1));keys.append(key)
 for f in range(1,121):key.value=field(float(c),f);key.keyframe_insert('value',frame=f)
# Replace traveling-shader spotlight by modest whole-ribbon exposure; formation is geometry.
mat=mesh.materials[0];nt=mat.node_tree;nt.animation_data_clear();em=next(n for n in nt.nodes if n.type=='EMISSION')
for link in list(em.inputs[1].links):nt.links.remove(link)
for f in range(1,121):
 activity=max(abs(field(float(u),f)) for u in centers);em.inputs[1].default_value=.03+2.2*activity;em.inputs[1].keyframe_insert('default_value',frame=f)
ob['motion']='Local delayed height growth and weaker return; anchored route and object transform';ob['display_model']='Artistic formation using v010 cropped modeled pulse profile; not physical particle displacement';s.frame_start=1;s.frame_end=120;s.render.fps=24;s.render.resolution_x=640;s.render.resolution_y=360;s.eevee.taa_render_samples=16
s.frame_set(50)
def save(p):
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=True)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
 bpy.ops.wm.save_as_mainfile(filepath=str(p))
save(O/'S02_ribbon-formation-review_v011.blend')
records=[]
def render(f,name):
 s.frame_set(f);s.render.filepath=str(P/name);t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'file':name,'seconds':dt})
 if dt>=5:raise RuntimeError('Frame cap exceeded')
render(50,'context_full_050.png')
for child in bpy.context.view_layer.layer_collection.children:child.exclude=True
for o in s.collection.objects:
 if o!=ob:o.hide_render=True
p=json.loads((T/'ribbon-build_v010.json').read_text());a=Vector(p['path_start']);b=Vector(p['path_end']);axis=b-a;depth=axis.normalized().cross(Vector((0,0,1))).normalized();target=(a+b)*.5;camdata=bpy.data.cameras.new('FORMATION_REVIEW_CAMERA');cam=bpy.data.objects.new('FORMATION_REVIEW_CAMERA',camdata);s.collection.objects.link(cam);cam.location=target+depth*.13+Vector((0,0,.035))-axis.normalized()*.012;cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();camdata.type='ORTHO';camdata.ortho_scale=.095;camdata.clip_start=.001;s.camera=cam;s.world=bpy.data.worlds.new('FORMATION_BLACK');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[1].default_value=0;s.render.resolution_x=960;s.render.resolution_y=540;s.eevee.taa_render_samples=32;save(O/'Ribbon_formation-dark_v011.blend')
for f,name in [(1,'isolated_flat_001.png'),(25,'isolated_growing_025.png'),(50,'isolated_full_050.png')]:render(f,name)
(T/'ribbon-benchmarks_v011.json').write_text(json.dumps(records,indent=2))
checks=[]
for f in [1,25,50,70,90,120]:
 s.frame_set(f);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());co=np.empty(n*3);ev.data.vertices.foreach_get('co',co);co=co.reshape(-1,3);checks.append({'frame':f,'geometry_sha256':hashlib.sha256(co.tobytes()).hexdigest(),'matrix':[list(r) for r in ob.matrix_world],'height_m':float(np.ptp(co[:,2])),'near_height_factor':field(.25,f),'far_height_factor':field(.85,f),'endpoint_z_max_m':float(np.max(abs(co[(route<1e-6)|(route>1-1e-6),2])))})
(T/'ribbon-geometry_v011.json').write_text(json.dumps({'checks':checks,'geometry_changes':len(set(x['geometry_sha256'] for x in checks))>1,'matrices_fixed':all(x['matrix']==checks[0]['matrix'] for x in checks),'timeline':'1–120 at24fps,5sec; source context frozen at native305 for review only; original source camera action retained','profile':'v010 2.5–5us artistic display window; seventeen local height controls','formation':'delayed growth f8+28u,12frame rise; crest48–54; settle54–70; weaker return65+20(1-u), decay105–120','source_camera_preserved':source_camera.name},indent=2));print('BENCHMARKS',json.dumps(records));print('GEOMETRY',json.dumps(checks))
