import bpy,pathlib,json,time
from mathutils import Vector
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';s=bpy.context.scene;s.frame_set(36);p=json.loads((T/'ribbon-build_v010.json').read_text());a=Vector(p['path_start']);b=Vector(p['path_end']);direction=(b-a).normalized();dep=bpy.context.evaluated_depsgraph_get()
for inst in dep.object_instances:
 if inst.object.name=='TEMP | Imaging port 2 | removable acoustic cap':
  points=[inst.matrix_world@v.co for v in inst.object.data.vertices];break
front=max((v-a).dot(direction) for v in points);center=a+direction*(front+.00012)
for n in ['EMISSION_ON_SAME_SENSOR','SAME_SENSOR_RECEIPT']:bpy.data.objects[n].location=center
s.frame_set(114);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath);s.render.filepath=str(T/'Previews/Ribbon_v012/receipt_114.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;(T/'causal-sensor-cue_v012.json').write_text(json.dumps({'source_face':'TEMP | Imaging port 2 | removable acoustic cap','sensor_path_anchor':list(a),'frontmost_face_offset_from_anchor_m':front,'cue_center':list(center),'surface_clearance_m':.00012,'render_seconds':dt},indent=2));print('CUE',front,dt)

extra=[]
for f,name in [(1,'quiet_001'),(24,'departure_024')]:
 s.frame_set(f);s.render.filepath=str(T/'Previews/Ribbon_v012'/f'{name}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;extra.append({'frame':f,'seconds':elapsed})
 if elapsed>=5:raise RuntimeError('Frame cap exceeded')
(T/'causal-quiet-departure-bench_v012.json').write_text(json.dumps(extra,indent=2))
