import bpy,json
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B.parent/'Cinematic-Previs_v019/Scenes/S04_continuous-camera_v019.blend'),load_ui=False,use_scripts=False)
s=bpy.context.scene;w=bpy.data.objects['WORLD_CONTROL'];w.animation_data_clear();w['travel_m']=-4.5;w.update_tag();s.frame_set(300);bpy.context.view_layer.update();dep=bpy.context.evaluated_depsgraph_get();rows=[]
for inst in dep.object_instances:
 o=inst.object
 if not inst.is_instance or o.type!='MESH':continue
 vs=[inst.matrix_world@Vector(p) for p in o.bound_box]
 if len(o.data.vertices)>40:rows.append({'name':o.name,'bbox':[[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)]})
(B/'Records/hardware-clearance-inspection.json').write_text(json.dumps(rows,indent=2));print([r for r in rows if r['bbox'][0][1]>-2.5])
