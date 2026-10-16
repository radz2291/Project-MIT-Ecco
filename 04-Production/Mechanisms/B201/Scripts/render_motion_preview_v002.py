import bpy,json,time,hashlib
from pathlib import Path
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Motion_v002'
r=json.loads((E/'build.json').read_text());scene=P/r['scene'];assert hashlib.sha256(scene.read_bytes()).hexdigest()==r['scene_sha256']
assert json.loads((E/'verification.json').read_text())['passed']
bpy.ops.wm.open_mainfile(filepath=str(scene));s=bpy.context.scene;bpy.context.window.view_layer=s.view_layers['FAST model and mechanism'];folder=M/'Previews/Motion_v002/Frames';folder.mkdir(exist_ok=True,parents=True);times=[];started=time.perf_counter()
for f in range(s.frame_start,s.frame_end+1):
 s.frame_set(f);s.render.filepath=str(folder/f'frame_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);times.append({'frame':f,'seconds':time.perf_counter()-t})
 if f%12==0 or f==s.frame_end:
  (E/'render-progress.json').write_text(json.dumps({'frames_rendered':f,'target_frames':s.frame_end,'elapsed_seconds':time.perf_counter()-started,'mean_frame_seconds':sum(x['seconds'] for x in times)/len(times),'max_frame_seconds':max(x['seconds'] for x in times)},indent=2));print('PROGRESS',f,s.frame_end,round(times[-1]['seconds'],3),flush=True)
(E/'render-times.json').write_text(json.dumps(times,indent=2));print('ANIMATION_FRAMES_PASS',len(times),flush=True)
