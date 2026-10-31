import bpy,json,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-051';records=[];sources=json.loads((T/'Evidence/environment-demo-build.json').read_text())
for entry in sources:
 p=R/entry['path'];bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);rec={'path':entry['path'],'native_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256((R/entry['source']).read_bytes()).hexdigest(),'libraries':[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries],'local_actions':[a.name for a in bpy.data.actions if not a.library],'local_objects':[o.name for o in bpy.data.objects if not o.library],'scenes':[]}
 assert rec['source_sha256']==entry['source_sha256'];assert rec['native_sha256']==entry['sha256'];assert all(l['exists'] for l in rec['libraries'])
 for s in bpy.data.scenes:
  bpy.context.window.scene=s;s.frame_set(s.frame_current);dg=bpy.context.evaluated_depsgraph_get();objects=[]
  for o in s.objects:
   if o.type=='MESH':
    ev=o.evaluated_get(dg);objects.append({'name':o.name,'library':o.library.filepath if o.library else None,'raw_vertices':len(o.data.vertices),'evaluated_vertices':len(ev.data.vertices),'bounds_camera':[list(world_to_camera_view(s,s.camera,ev.matrix_world@Vector(c))) for c in ev.bound_box]})
  rec['scenes'].append({'name':s.name,'camera':s.camera.name if s.camera else None,'camera_location':list(s.camera.location),'camera_ortho_scale':s.camera.data.ortho_scale,'frame_range':[s.frame_start,s.frame_end],'mesh_objects':objects})
 records.append(rec)
(T/'Evidence/environment-demo-independent-054.json').write_text(json.dumps(records,indent=2));print('ROOT_DEMOS_LINK_HASH_CAMERA_CHECKS_PASS',[(r['path'],len(r['local_actions']),len(r['scenes'])) for r in records])
