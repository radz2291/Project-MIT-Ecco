import bpy,json,hashlib,time,numpy as np
from pathlib import Path
B=Path(__file__).resolve().parents[1];current=B/'Scenes/S05_tracked-cuttings_v009.blend';prior=B.parent/'Interaction-Proof_v008/Scenes/S05_internal-flow_v008.blend'
def signature():
 d=bpy.data.objects['S05_v007_AnnularFluidDomain'];a=np.empty(len(d.data.vertices)*3,dtype=np.float32);d.data.vertices.foreach_get('co',a)
 return {'volume_vertices':hashlib.sha256(a.tobytes()).hexdigest(),'volume_faces':hashlib.sha256(str([list(p.vertices) for p in d.data.polygons]).encode()).hexdigest(),'hardware':[(o.name,o.data.name,list(o.scale),o.data.library.filepath if o.data.library else None) for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects]}
s=bpy.context.scene;s.frame_set(36);s.render.filepath='//../Work/Frames/S05_';bpy.ops.wm.save_as_mainfile(filepath=str(current));native_hash=hashlib.sha256(current.read_bytes()).hexdigest();new=signature()
bpy.ops.wm.open_mainfile(filepath=str(prior));old=signature();assert old==new
bpy.ops.wm.open_mainfile(filepath=str(current));assert signature()==new
s=bpy.context.scene;s.frame_set(36);s.render.filepath=str(B/'Work/reopened-frame36.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
result={'native_sha256':native_hash,'fluid_geometry_and_linked_hardware_match_v008':True,'volume_vertex_sha256':new['volume_vertices'],'reopened_render_seconds':dt,'libraries':[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries],'authorized_differences':'Stationary camera shifted and lens 58mm; fluid material copied and density quieted; three tracked fragments replace staggered flow groups; 8 render samples.'}
assert all(l['exists'] and l['relative'] for l in result['libraries'])
(B/'Records/native-preservation.json').write_text(json.dumps(result,indent=2))
