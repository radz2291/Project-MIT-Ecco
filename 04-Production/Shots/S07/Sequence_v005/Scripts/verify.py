import bpy,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];R=B.parents[3];build=json.loads((B.parent/'Sequence_v001/Records/build.json').read_text());src=Path(build['source'])
assert hashlib.sha256(src.read_bytes()).hexdigest()==build['source_sha256']
def digest(o):
 me=o.data;v=np.empty(len(me.vertices)*3,dtype='f');me.vertices.foreach_get('co',v);ix=np.empty(len(me.loops),dtype='i');me.loops.foreach_get('vertex_index',ix)
 return {'vertices':len(me.vertices),'faces':len(me.polygons),'vertex_sha256':hashlib.sha256(v.tobytes()).hexdigest(),'topology_sha256':hashlib.sha256(ix.tobytes()).hexdigest()}
bpy.ops.wm.open_mainfile(filepath=str(src));expected={o.name:{'mesh':digest(o),'matrix':np.array(o.matrix_world)} for o in bpy.data.objects if o.type=='MESH' and 'CUTTER' not in o.name}
native=B/'Scenes/S07_Monumental-Precision_v005.blend';bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene
assert (s.frame_start,s.frame_end,s.render.fps)==(1,192,24)
assert len([o for o in bpy.data.objects if o.get('S07_source_object')])==len(expected)
assert not bpy.data.libraries
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
assert all(font.packed_file for font in bpy.data.fonts if font.filepath and font.filepath!='<builtin>')
assert not any(o.type=='FONT' for o in bpy.data.objects)
mesh_checks={};positions=[];quaternions=[];clearance=[];bounds={}
for f in range(1,193):
 s.frame_set(f);bpy.context.view_layer.update()
 for name,x in expected.items():
  o=bpy.data.objects[name];assert np.allclose(np.array(o.matrix_world),x['matrix'],atol=1e-7),(name,f)
  if f==1:assert digest(o)==x['mesh'];mesh_checks[name]=x['mesh']
 pos=s.camera.matrix_world.translation;positions.append(list(pos));quaternions.append(list(s.camera.rotation_quaternion));clearance.append((pos.y**2+pos.z**2)**.5-.153)
 if f in [60,61,120,121,160,192]:
  points=[]
  for name in expected:
   o=bpy.data.objects[name];points.extend(world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box)
  b={'xmin':min(p.x for p in points),'xmax':max(p.x for p in points),'ymin':min(p.y for p in points),'ymax':max(p.y for p in points)};bounds[str(f)]=b
  if f>=121:
   assert b['xmin']>.03 and b['xmax']<.97 and b['ymin']>.03 and b['ymax']<.97,b
   assert abs((b['xmin']+b['xmax'])/2-.5)<.025
assert min(clearance)>.1
fade=s.compositing_node_group.nodes['Final fade to nothingness'];assert fade.inputs[6].links[0].from_node.bl_idname=='CompositorNodeRLayers'
for f,val in [(1,0),(61,0),(121,0),(164,0),(190,1),(192,1)]:
 s.frame_set(f);assert abs(fade.inputs[0].default_value-val)<1e-6
shot_results=[];poses=np.array(positions)
for a,b in [(1,60),(61,120),(121,192)]:
 d=np.diff(poses[a-1:b],axis=0);speed=np.linalg.norm(d,axis=1)
 assert min(speed)>.001
 assert np.max(np.abs(d-d[0]))<2e-6,'Camera translation not linear'
 shot_results.append({'frames':[a,b],'start_speed_m_per_frame':float(speed[0]),'end_speed_m_per_frame':float(speed[-1]),'constant_translation':True,'moving_on_first_interval':True})
assert np.linalg.norm(poses[120]-poses[119])>3
b=bounds['120'];c=bounds['121'];ratio=((b['xmax']-b['xmin'])*(b['ymax']-b['ymin']))/((c['xmax']-c['xmin'])*(c['ymax']-c['ymin']));assert ratio>4
for f in [60,120]:
 s.frame_set(f,subframe=.5);bpy.context.view_layer.update();assert np.allclose(s.camera.matrix_world.translation,poses[f-1],atol=1e-6),'Cut interpolation smeared'
rev=json.loads((B/'Records/revision.json').read_text());assert hashlib.sha256(Path(rev['source']).read_bytes()).hexdigest()==rev['source_sha256']
s06=R/'04-Production/Studies/S06_Report-Recreation_v004';approval=json.loads((s06/'Records/closure-verification.json').read_text())
for a in approval['artifacts']:assert hashlib.sha256((s06/a['path']).read_bytes()).hexdigest()==a['sha256']
bench=json.loads((B/'Records/benchmark.json').read_text());assert max(x['seconds'] for x in bench)<5
result={'saved_native_reopened':True,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'source_unchanged':True,'v002_native_unchanged':True,'S06_approved_artifacts_unchanged':True,'geometry':mesh_checks,'all_192_frames_hardware_stationary':True,'shot_motion_checks':shot_results,'cut_frames':[61,121],'cut_interpolation_held_until_next_frame':True,'second_to_third_projected_bbox_area_ratio':ratio,'opening_is_direct_product_no_fade':True,'branding_objects':0,'final_fade_to_black':True,'projected_bounds':bounds,'minimum_camera_clearance_m':min(clearance),'external_libraries':0,'all_file_images_and_fonts_packed':True,'benchmark_max_seconds':max(x['seconds'] for x in bench),'scope':'Technical and executor visual checks; owner playback review pending'}
(B/'Records/verification.json').write_text(json.dumps(result,indent=2));print('VERIFIED',json.dumps({k:v for k,v in result.items() if k!='geometry'}),flush=True)
