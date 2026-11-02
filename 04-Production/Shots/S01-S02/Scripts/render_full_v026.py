"""Owner-requested full1080p v026 review render via official live Blender."""
import bpy,time,json,traceback,sys,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');P=Q/'Previews/Full-v026';P.mkdir(exist_ok=True)
assert bpy.data.filepath.endswith('S01-S02_production_v026.blend')
resume=globals().get('RESUME',False)
assert resume or not any(P.glob('frame_*.png')),'Preserve previous output; use a successor or explicit resume.'
assert not bpy.app.driver_namespace.get('ecco_full_v026_job',{}).get('status')=='running'
sys.path.insert(0,str(Q/'Scripts'));import final_render_visibility as display
window=bpy.context.window_manager.windows[0]
job={'status':'running','scene':bpy.data.filepath,'scene_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'first':1,'last':756,'next':1,'original_frame':bpy.context.scene.frame_current,'size':[1920,1080],'fps':24,'started':time.time(),'records':[],'cancel':False}
bpy.app.driver_namespace['ecco_full_v026_job']=job
if resume:
 job=json.loads((Q/'Notes/full_v026_render.json').read_text());assert job['scene_sha256']==hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()
 job['recoveries']=job.get('recoveries',[])+[{'at_frame':job['next'],'time':time.time(),'reason':'Blender crash in im.save_render; resume using persistent image/offscreen buffers'}];job['status']='running';job.pop('error',None);bpy.app.driver_namespace['ecco_full_v026_job']=job
from stable_full_export_v026 import Exporter
with bpy.context.temp_override(window=window):exporter=Exporter(*job['size'])
def record():
 job['elapsed_seconds']=time.time()-job['started'];tmp=Q/'Notes/full_v026_render.tmp';tmp.write_text(json.dumps(job,indent=2));tmp.replace(Q/'Notes/full_v026_render.json')
def tick():
 try:
  assert bpy.data.filepath==job['scene'],'Scene changed during export'
  if job['cancel']:job['status']='cancelled'
  else:
   with bpy.context.temp_override(window=window):
    for _ in range(4):
     f=job['next'];t=time.perf_counter();bpy.context.scene.frame_set(f);exporter.export(P/f'frame_{f:04}.png');dt=time.perf_counter()-t
     job['records'].append({'frame':f,'seconds':dt});job['next']=f+1
     assert dt<5,f'Frame{f} exceeded strict cap: {dt:.3f}s'
     if f==job['last']:job['status']='complete';break
 except Exception:job['status']='failed';job['error']=traceback.format_exc()
 record()
 if job['status']=='running':return .05
 exporter.close()
 if bpy.data.filepath==job['scene']:bpy.context.scene.frame_set(job['original_frame'])
record();bpy.app.timers.register(tick,first_interval=.1)
result={'started':True,'frames':[1,756],'fps':24,'size':job['size'],'output':str(P)}
