import bpy,json
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];P=B.parent
out={}
for c,path in [('A','Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'),('B','Communication-Test_v009/Scenes/S04_B_formation-acquisition_v009.blend'),('D','D-Physical-Wear_v017/Scenes/S04_D_cool-wear-depth_v017.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(P/path),load_ui=False,use_scripts=False)
 s=bpy.data.scenes['D computed wear depth - cool palette v017'] if c=='D' else bpy.context.scene
 s.frame_set(1);rows=[]
 for o in s.objects:
  if o.hide_render or o.type not in ['MESH','EMPTY','CAMERA']:continue
  row={'name':o.name,'type':o.type,'loc':list(o.location),'parent':o.parent.name if o.parent else None,'anim':bool(o.animation_data),'props':{k:str(v) for k,v in o.items() if k!='_RNA_UI'}}
  if o.type=='MESH':
   vs=[o.matrix_world@Vector(p) for p in o.bound_box];row.update(vertices=len(o.data.vertices),bounds=[[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)],materials=[m.name if m else '' for m in o.data.materials])
  rows.append(row)
 cams=[]
 for f in ([1,60,96] if c=='A' else [1]):
  s.frame_set(f);cam=s.camera;cams.append({'frame':f,'pos':list(cam.matrix_world.translation),'quat':list(cam.matrix_world.to_quaternion()),'lens':cam.data.lens,'sensor':cam.data.sensor_fit})
 out[c]={'scene':s.name,'objects':rows,'cameras':cams,'render':s.render.engine}
(B/'Records/inspection.json').write_text(json.dumps(out,indent=2))
