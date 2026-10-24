import bpy,json,time
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_journey_v001.blend'))
s=bpy.context.scene;s.render.resolution_x=1280;s.render.resolution_y=720
times=[]
for f,name in [(49,'01_Sculptural'),(132,'02_Transformation'),(276,'03_Information')]:
    s.frame_set(f);s.render.filepath=str(B/f'Previews/S06_arrival_{name}.png')
    t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t
    times.append({'frame':f,'name':name,'seconds':sec,'resolution':[1280,720]})
    (B/'Records/delivery-still-timings.json').write_text(json.dumps(times,indent=2))
    if sec>=5:raise RuntimeError('Still render cap exceeded')
