"""Fast camera/reveal proof: 12FPS sampling at original playback speed."""
import bpy,json,time,sys,traceback
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');sys.path.insert(0,str(Q/'Scripts'))
import final_render_visibility as display
P=Q/'Previews/Early-onset-v023';P.mkdir(exist_ok=True);assert not any(P.glob('preview_*.png'))
frames=list(range(508,573,2));window=bpy.context.window_manager.windows[0]
job={'status':'running','scene':bpy.data.filepath,'index':0,'total':len(frames),'fps':12,'size':[960,540],'rows':[],'started':time.time()};bpy.app.driver_namespace['early_onset_v023_job']=job
def tick():
 try:
  assert bpy.data.filepath==job['scene']
  with bpy.context.temp_override(window=window):
   f=frames[job['index']];bpy.context.scene.frame_set(f);t=time.perf_counter();display.export(P/f"preview_{job['index']:04}.png",960,540);dt=time.perf_counter()-t;assert dt<5,dt;job['rows'].append({'frame':f,'seconds':dt});job['index']+=1
   if job['index']==len(frames):job['status']='complete';bpy.context.scene.frame_set(756)
 except Exception:job['status']='failed';job['error']=traceback.format_exc()
 job['wall_seconds']=time.time()-job['started'];(Q/'Notes/early_onset_v023_motion.json').write_text(json.dumps(job,indent=2))
 if job['status']=='running':return .05
bpy.app.timers.register(tick,first_interval=.1)
result={'started':True,'frames':len(frames),'fps':12}


