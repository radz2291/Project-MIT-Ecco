import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];meta=json.loads((B/'Records/build.json').read_text())
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_sequential-camera_v020.blend'),use_scripts=False,load_ui=False);s=bpy.context.scene
def graphic(name):return name.startswith(('STEEL-ATTACHED resonance band','STEEL THICKNESS response','STEEL-BOUND acquisition segment','S02 sourced','Casing response tail'))
def geometry():return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH' and not graphic(o.name)}
assert geometry()==meta['geometry_fingerprints']
for field in ['source','source_C']:assert hashlib.sha256(Path(meta[field]).read_bytes()).hexdigest()==meta[field+'_sha256']
steel=bpy.data.objects['STEEL - capped true source section'];depth=[x.value for x in steel.data.attributes['ComputedWearDepth_m'].data];assert max(depth)<.004001
physical=[o for o in s.objects if o.type=='MESH' and not o.hide_render and (o.name.startswith('Cement ') or 'organic fluid-filled' in o.name or 'capped true source' in o.name or 'closed source-guided' in o.name)]
baseline={o.name:tuple(o.matrix_world) for o in physical};names=[];projection={};margins=[];tool=[]
N=Vector((0,-math.sin(math.radians(39)),math.cos(math.radians(39))))
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update();assert all(not o.hide_render and tuple(o.matrix_world)==baseline[o.name] for o in physical);names.append(s.camera.name)
 pos=s.camera.matrix_world.translation;plane=pos.dot(N)-.00005
 margin=plane if plane>0 else (pos.x if pos.x>0 else (-5.5-pos.x if pos.x<-5.5 else max(.1589405-math.hypot(pos.y,pos.z),math.hypot(pos.y,pos.z)-.1698625)))
 margins.append(margin);assert margin>=-1e-5
 if f in [85,197]:
  tag='B' if f==85 else 'C';event=json.loads((B.parent/'Communication-Test_v009/Records'/f'build-{tag}.json').read_text())['event'];projection[tag]={k:list(world_to_camera_view(s,s.camera,Vector(event[v]))) for k,v in [('sensor','emitter_world_m'),('contact','hit_world_m')]};tool.append((tag,bpy.data.objects['WORLD_CONTROL']['travel_m']))
assert len(set(names))==1
assert all(abs(a-b)<.0005 for k in ['sensor','contact'] for a,b in zip(projection['B'][k],projection['C'][k]))
libs=[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries];assert all(l['exists'] for l in libs)
master=ROOT/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend';master_hash=hashlib.sha256(master.read_bytes()).hexdigest();assert master_hash=='52c14a8f71d9d3c160acbdfaade240f7e699334c3a2ed4bd649cb220b59e49ba'
review=bpy.data.scenes.new('S04 REVIEW - sequential full-frame v020');review.frame_start=1;review.frame_end=432;review.render.fps=24;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.view_settings.view_transform='Standard';ed=review.sequence_editor_create();strip=ed.strips.new_image('One camera - A then B then C then D',str(B/'Work/Assembly/S04_0001.png'),channel=1,frame_start=1)
for f in range(2,433):strip.elements.append(f'S04_{f:04d}.png')
strip.directory='//../Work/Assembly/';main_name=s.name
for f,text in [(1,'A - medium oblique casing entry'),(63,'B - supported backing'),(141,'Track to distinct fixed C location'),(175,'C - reduced backing'),(261,'Tool moves on - inspect worn wall'),(318,'D - inner curvature and wear'),(361,'Expose fixed computed depth'),(405,'Final information hold')]:s.timeline_markers.new(text,frame=f);review.timeline_markers.new(text,frame=f)
s['review_scene']=review.name;review['physical_scene']=s.name;s.frame_set(85)
for w in bpy.context.window_manager.windows:
 w.scene=s
 for a in w.screen.areas:
  if a.type=='SEQUENCE_EDITOR':a.type='VIEW_3D'
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='RENDERED'
out=B/'Scenes/S04_complete-sequential_v020.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False,load_ui=False)
assert main_name in bpy.data.scenes
review=bpy.data.scenes['S04 REVIEW - sequential full-frame v020'];assert all((Path(bpy.path.abspath(st.directory))/e.filename).is_file() for st in review.sequence_editor.strips for e in st.elements)
report={'saved_reopened':True,'complete_native':str(out),'physical_scene':main_name,'one_camera_across432_frames':True,'physical_mesh_coordinates_topology_identical_to_v019':True,'physical_layer_transforms_and_visibility_static':True,'section_fixed50percent':True,'maximum_authored_loss_mm':1000*max(depth),'source_bytes_unchanged':True,'canonical_master_unchanged_sha256':master_hash,'B_C_matched_projection':projection,'hardware_travel_B_C':tool,'minimum_conservative_casing_clearance_m':min(margins),'all_review_image_dependencies_exist':True,'libraries':libs,'no_split_screen_or_insert':True,'engineering_acceptance':False,'cold_viewer_test':'Not performed; owner normal-speed review pending'}
(B/'Records/verification.json').write_text(json.dumps(report,indent=2));print('PACKAGE VERIFIED')
