import bpy,json,hashlib
import numpy as np
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1]
def geometry_hash():
 h=hashlib.sha256()
 for me in sorted({o.data for o in bpy.context.scene.objects if o.type=='MESH'},key=lambda x:x.name):
  h.update(me.name.encode());a=np.empty(len(me.vertices)*3,dtype='f');me.vertices.foreach_get('co',a);h.update(a.tobytes());idx=np.empty(len(me.loops),dtype='i');me.loops.foreach_get('vertex_index',idx);h.update(idx.tobytes())
  for attr in me.color_attributes:
   a=np.empty(len(attr.data)*4,dtype='f');attr.data.foreach_get('color',a);h.update(a.tobytes())
 return h.hexdigest()
def shape_values():
 result=[]
 for f in range(1,289):
  bpy.context.scene.frame_set(f);result.append([k.value for name in ['A | reconstructed wall beginning to open','B | independent amplitude'] for k in bpy.data.objects[name].data.shape_keys.key_blocks])
 return result
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004.blend'));before=geometry_hash();shapes=shape_values();s=bpy.context.scene;s.frame_set(288);end=np.array(s.camera.matrix_world);texts=sorted(o.data.body for o in s.objects if o.type=='FONT')
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v004_polished.blend'));s=bpy.context.scene
assert before==geometry_hash();assert np.array_equal(shapes,shape_values());assert texts==sorted(o.data.body for o in s.objects if o.type=='FONT')
s.frame_set(288);assert np.allclose(np.array(s.camera.matrix_world),end,atol=1e-5)
assert not list(bpy.data.images) and not list(bpy.data.libraries)
assert s.frame_end==288 and s.render.fps==24
bounds=[]
for f in range(120,237):
 s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();uv=[]
 for name in (['A | reconstructed wall beginning to open'] if f<192 else ['A | reconstructed wall beginning to open','B | independent amplitude']):
  o=bpy.data.objects[name].evaluated_get(dg);v=np.empty(len(o.data.vertices)*3,dtype='f');o.data.vertices.foreach_get('co',v);v=v.reshape(-1,3);edge=np.concatenate((v[::97],v[96::97],v[:97],v[-97:]))
  uv.extend(world_to_camera_view(s,s.camera,o.matrix_world@Vector(x))[:2] for x in edge)
 uv=np.array(uv);bounds.append({'frame':f,'minimum':uv.min(0).tolist(),'maximum':uv.max(0).tolist()});assert uv.min()>.005 and uv.max()<.995,('Crop',f,uv.min(),uv.max())
for f,n in [(1,16),(90,32),(144,32),(145,16),(227,16),(228,48),(250,48),(259,16)]:s.frame_set(f);assert s.eevee.taa_render_samples==n
assert max(r['seconds'] for r in json.loads((B/'Records/polish-benchmark.json').read_text()))<5
result={'saved_polished_native_reopens':True,'all_mesh_positions_topology_and_colors_identical':True,'all_288_geometry_and_amplitude_shape_states_identical':True,'final_camera_identical':True,'text_inventory_unchanged':True,'no_external_images_or_libraries':True,'sample_schedule_saved_and_verified':True,'map_bounds_checked_every_frame_120_through_236':bounds,'geometry_sha256':before,'review':'Frame inspection and deterministic checks; not independent audience or client acceptance.'}
(B/'Records/polish-verification.json').write_text(json.dumps(result,indent=2));print('POLISH VERIFIED')
