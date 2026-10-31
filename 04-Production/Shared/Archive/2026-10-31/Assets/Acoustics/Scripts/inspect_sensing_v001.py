import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
E=ROOT/'04-Production/Records/Tasks/T-046/Evidence'
out={}
for name,path in [('world','04-Production/Records/Tasks/T-044/Revision_v006/Scenes/downhole_A_cleanup_v010.blend'),('b201','04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_refinement_v006.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/path),load_ui=False,use_scripts=False)
 s=bpy.context.scene;s.frame_set(1)
 deps=bpy.context.evaluated_depsgraph_get()
 instances=[]
 for i in deps.object_instances:
  o=i.object.original
  if any(p in o.name for p in ['SENSOR_REF','CASING','OPENHOLE','WALL','NOMINAL','IRREGULAR']):
   instances.append(dict(name=o.name,type=o.type,matrix=[list(r) for r in i.matrix_world],vertices=len(o.data.vertices) if o.type=='MESH' else None))
 out[name]=dict(path=path,sha256=hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),instances=instances,camera=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens),objects=[o.name for o in s.objects],libraries=[l.filepath for l in bpy.data.libraries])
(E/'source-inspection_v001.json').write_text(json.dumps(out,indent=2))
print('SENSING_INSPECT',[(k,len(v['instances'])) for k,v in out.items()])
