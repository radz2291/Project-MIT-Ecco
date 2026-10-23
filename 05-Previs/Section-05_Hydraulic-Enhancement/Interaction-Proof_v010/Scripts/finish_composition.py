import bpy,time,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;cam=s.camera
# Lens shift centres the entire trip while preserving the tested viewing position.
cam.data.shift_x=.0436877012252808;cam.data.shift_y=.0585434571849257
rows=[]
for f in [1,48,96]:
 s.frame_set(f);s.render.filepath=str(B/'Previews'/f'benchmark_{f:03}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});assert dt<5
s.frame_set(48);s.render.filepath='//../Work/Frames/S05_';s['proof_scope']='v010 combined 4-second moving annulus, trackable cohort, visible side deflection and available-passage motion cues; illustrative not CFD'
result={'benchmarks':rows,'resolution':[1280,720],'samples':8,'camera_location':list(cam.location),'camera_quaternion':list(cam.rotation_quaternion),'lens_mm':cam.data.lens,'lens_shift':[cam.data.shift_x,cam.data.shift_y]}
(B/'Records/benchmark.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
