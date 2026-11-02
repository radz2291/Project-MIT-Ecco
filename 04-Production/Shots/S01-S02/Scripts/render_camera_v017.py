"""Fast camera proof: every second source frame, played at 12 FPS."""
import bpy,time,json,traceback
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=Q/'04-Production/Shots/S01-S02'
P=Q/'Previews/Camera-v017-verified';P.mkdir(exist_ok=True)
assert bpy.data.filepath.endswith('S01-S02_production_v017.blend')
assert not any(P.glob('preview_*.png'))
window=bpy.context.window_manager.windows[0]
with bpy.context.temp_override(window=window):
 exec(bpy.data.texts['START HERE — pixel guides'].as_string())
module=bpy.app.driver_namespace['ecco_pixel_module'];h=bpy.app.driver_namespace.pop(module.KEY,None)
if h:bpy.types.SpaceView3D.draw_handler_remove(h,'WINDOW')
frames=list(range(450,757,2));job={'status':'running','scene':bpy.data.filepath,'size':[640,360],'preview_fps':12,'source_fps':24,'index':0,'total':len(frames),'rows':[],'started':time.time()}
bpy.app.driver_namespace['camera_v017_job']=job
def tick():
 try:
  if job.get('cancel'):job['status']='cancelled';return None
  assert bpy.data.filepath==job['scene']
  with bpy.context.temp_override(window=window):
   f=frames[job['index']];t=time.perf_counter();bpy.context.scene.frame_set(f);module.export(P/f"preview_{job['index']:04}.png",640,360);dt=time.perf_counter()-t
   job['rows'].append({'frame':f,'seconds':dt});assert dt<5,dt;job['index']+=1
   if job['index']==len(frames):job['status']='complete';bpy.context.scene.frame_set(600);module.install()
 except Exception:job['status']='failed';job['error']=traceback.format_exc()
 job['wall_seconds']=time.time()-job['started'];(Q/'Notes/camera_v017_verified_render.json').write_text(json.dumps(job,indent=2))
 if job['status']=='running':return .02
bpy.app.timers.register(tick,first_interval=.1)
result={'started':True,'frames':len(frames),'preview_fps':12}
