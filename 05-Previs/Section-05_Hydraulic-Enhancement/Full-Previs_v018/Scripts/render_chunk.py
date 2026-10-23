import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
frames=Path('D:/MIT-ECCO-Render-Recovery/S05-v018-RenderCache/Frames');frames.mkdir(parents=True,exist_ok=True)
record=B/'Records/render-timings.json';times=json.loads(record.read_text()) if record.exists() else []
for f in range(START,END+1):
 assert not any(r['frame']==f for r in times),'Frame already recorded'
 s.frame_set(f);s.render.filepath=str(frames/f'S05_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
 times.append({'frame':f,'seconds':dt});record.write_text(json.dumps(times,indent=2));assert dt<5,('Frame exceeded budget',f,dt)
result={'completed':END,'frames_rendered':len(times),'seconds_max':max(r['seconds'] for r in times)}
