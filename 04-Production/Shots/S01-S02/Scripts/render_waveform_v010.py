"""Live pixel-guide proof; benchmark before two native-speed event clips."""
import bpy,time,json,traceback
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');P=Q/'Previews/Waveform-v010';P.mkdir(exist_ok=True)
exec(bpy.data.texts['START HERE — pixel guides'].as_string());module=bpy.app.driver_namespace['ecco_pixel_module']
handle=bpy.app.driver_namespace.pop(module.KEY,None)
if handle:bpy.types.SpaceView3D.draw_handler_remove(handle,'WINDOW')
frames=[305,497,523]+list(range(299,337))+list(range(489,529));previous=Q/'Notes/waveform_v010_render.json'
job=json.loads(previous.read_text()) if previous.exists() else {'status':'running','index':0,'rows':[],'scene':bpy.data.filepath}
assert job['scene']==bpy.data.filepath;job['status']='running';bpy.app.driver_namespace['wave_v010_job']=job
def tick():
 try:
  assert bpy.data.filepath==job['scene'];f=frames[job['index']];t=time.perf_counter();bpy.context.scene.frame_set(f);module.export(P/f'frame_{f:04}.png',1920,1080);dt=time.perf_counter()-t;job['rows'].append({'frame':f,'seconds':dt});assert dt<5,('render cap',dt);job['index']+=1
  if job['index']==len(frames):job['status']='complete';bpy.context.scene.frame_set(305)
 except Exception:job['status']='failed';job['error']=traceback.format_exc()
 (Q/'Notes/waveform_v010_render.json').write_text(json.dumps(job,indent=2))
 if job['status']=='running':return .05
bpy.app.timers.register(tick,first_interval=.1)
result={'started':True,'frames':len(frames)}
