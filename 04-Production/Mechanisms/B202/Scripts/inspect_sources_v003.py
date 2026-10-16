import bpy,json
from pathlib import Path
root=Path(__file__).resolve().parents[4]
bpy.ops.wm.open_mainfile(filepath=str(root/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'))
rig=bpy.data.objects['ASSEMBLY_CONTROL']
rig['variant']=1;rig['cutaway']=0;rig.update_tag();bpy.context.view_layer.update()
wall=bpy.data.objects['IRREGULAR_FULL']
ev=wall.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
out={'objects':[o.name for o in bpy.context.scene.objects],'wall_vertices':len(me.vertices),'wall_sample':[list(v.co) for v in list(me.vertices)[:4]],'rig':dict(rig.items()),'libraries':[bpy.path.abspath(x.filepath) for x in bpy.data.libraries],'sensor_refs':[{ 'name':o.name,'location':list(o.matrix_world.translation)} for o in bpy.data.objects if 'SENSOR_REF_' in o.name]}
ev.to_mesh_clear()
(root/'04-Production/Records/Tasks/T-008/Evidence/source-inspection_v003.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
