import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene
frames=B/'Work/Frames';frames.mkdir(exist_ok=True)
record=B/'Records/render-timings.json';times=json.loads(record.read_text()) if record.exists() else []
for f in range(START,END+1):
 s.frame_set(f);s.render.filepath=str(frames/f'S05_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
 times.append({'frame':f,'seconds':dt});record.write_text(json.dumps(times,indent=2))
 assert dt<5, f'Frame {f} exceeded cap: {dt}'
result={'completed':END,'seconds_max':max(r['seconds'] for r in times),'frames_rendered':len(times)}
