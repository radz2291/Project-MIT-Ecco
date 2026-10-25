import bpy,json,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];R=B.parents[3];build=json.loads((B/'Records/build.json').read_text())
src=R/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
assert hashlib.sha256(src.read_bytes()).hexdigest()==build['source_sha256']
def digest(o):
 me=o.data;v=np.empty(len(me.vertices)*3,dtype='f');me.vertices.foreach_get('co',v)
 ix=np.empty(len(me.loops),dtype='i');me.loops.foreach_get('vertex_index',ix)
 return {'vertices':len(me.vertices),'faces':len(me.polygons),'vertex_sha256':hashlib.sha256(v.tobytes()).hexdigest(),'topology_sha256':hashlib.sha256(ix.tobytes()).hexdigest()}
bpy.ops.wm.open_mainfile(filepath=str(src));expected={o.name:{'mesh':digest(o),'matrix':np.array(o.matrix_world)} for o in bpy.data.objects if o.type=='MESH' and 'CUTTER' not in o.name}
native=B/'Scenes/S07_Monumental-Precision_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(native));s=bpy.context.scene
assert s.frame_start==1 and s.frame_end==192 and s.render.fps==24
assert len([o for o in bpy.data.objects if o.get('S07_source_object')])==len(expected)
assert not bpy.data.libraries
assert all(im.packed_file for im in bpy.data.images if im.source=='FILE')
assert all(font.packed_file for font in bpy.data.fonts if font.filepath and font.filepath!='<builtin>')
mesh_checks={};baseline=None;camera_positions=[];clearance=[];final_bounds=None
for f in range(1,193):
 s.frame_set(f);bpy.context.view_layer.update()
 for name,x in expected.items():
  o=bpy.data.objects[name];assert np.allclose(np.array(o.matrix_world),x['matrix'],atol=1e-7),('hardware moved',name,f)
  if f==1:assert digest(o)==x['mesh'];mesh_checks[name]=x['mesh']
 pos=s.camera.matrix_world.translation;camera_positions.append(list(pos));clearance.append((pos.y**2+pos.z**2)**.5-.153)
 if f>=146:
  camera_state=np.array(list(pos)+list(s.camera.rotation_quaternion))
  if baseline is None:baseline=camera_state
  else:assert np.max(abs(camera_state-baseline))<1e-6
 if f==192:
  points=[]
  for name in expected:
   o=bpy.data.objects[name]
   points.extend(world_to_camera_view(s,s.camera,o.matrix_world@Vector(v)) for v in o.bound_box)
  final_bounds={'xmin':min(p.x for p in points),'xmax':max(p.x for p in points),'ymin':min(p.y for p in points),'ymax':max(p.y for p in points)}
  assert final_bounds['xmin']>.04 and final_bounds['xmax']<.65 and final_bounds['ymin']>.035 and final_bounds['ymax']<.96,final_bounds
assert min(clearance)>.1
brand=bpy.data.collections['S07 EDITABLE BRANDING'];assert sorted(o.data.body for o in brand.objects)==['ECCO ENP3','MIT LOGO']
s06=R/'04-Production/Studies/S06_Report-Recreation_v004';approval=json.loads((s06/'Records/closure-verification.json').read_text())
for a in approval['artifacts']:
 assert hashlib.sha256((s06/a['path']).read_bytes()).hexdigest()==a['sha256'],'S06 changed'
bench=json.loads((B/'Records/benchmark.json').read_text());assert max(x['seconds'] for x in bench)<5
result={'saved_native_reopened':True,'native_sha256':hashlib.sha256(native.read_bytes()).hexdigest(),'source_unchanged':True,'S06_approved_artifacts_unchanged':True,'geometry':mesh_checks,'all_192_frames_hardware_stationary':True,'unchanged_source_matrices':True,'final_camera_stationary_from_frame':146,'final_product_bounds_normalized':final_bounds,'minimum_camera_to_source_radius_clearance_m':min(clearance),'external_libraries':0,'all_file_images_and_fonts_packed':True,'editable_branding':['ECCO ENP3','MIT LOGO'],'benchmark_max_seconds':max(x['seconds'] for x in bench),'scope':'Technical and executor visual checks; owner playback review pending'}
(B/'Records/verification.json').write_text(json.dumps(result,indent=2));print('VERIFIED',json.dumps({k:v for k,v in result.items() if k!='geometry'}),flush=True)
