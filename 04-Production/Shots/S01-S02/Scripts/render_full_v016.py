"""Live Blender: asynchronous, bounded-cost 640x360 whole-sequence playblast.

Poll bpy.app.driver_namespace['ecco_full_v016_job']; set cancel=True to stop.
One frame per timer tick keeps the bridge responsive. No overwrite of scene.
"""
import bpy,time,json,traceback
from pathlib import Path

Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
P=Q/'Previews/Full-v016';P.mkdir(exist_ok=True)
assert not bpy.app.driver_namespace.get('ecco_full_v016_job',{}).get('status')=='running'
assert not any(P.glob('frame_*.png')), 'Preserve existing output; use a new version or explicit resume'
exec(bpy.data.texts['START HERE — pixel guides'].as_string())
module=bpy.app.driver_namespace['ecco_pixel_module']
handle=bpy.app.driver_namespace.pop(module.KEY,None)
if handle:bpy.types.SpaceView3D.draw_handler_remove(handle,'WINDOW')
job={'status':'running','scene':bpy.data.filepath,'first':1,'last':756,'next':1,
     'original_frame':bpy.context.scene.frame_current,'size':[640,360],
     'fps':24,'started':time.time(),'records':[],'cancel':False}
bpy.app.driver_namespace['ecco_full_v016_job']=job

def tick(job=job,module=module):
    try:
        if bpy.data.filepath!=job['scene']:raise RuntimeError('Scene changed during export')
        if job['cancel']:
            job['status']='cancelled'
        else:
            f=job['next'];started=time.perf_counter()
            bpy.context.scene.frame_set(f)
            module.export(P/f'frame_{f:04}.png',*job['size'])
            seconds=time.perf_counter()-started
            job['records'].append({'frame':f,'seconds':seconds})
            job['next']=f+1
            if seconds>=5:raise RuntimeError(f'Frame{f} exceeded render cap: {seconds:.3f}s')
            if f==job['last']:job['status']='complete'
    except Exception:
        job['status']='failed';job['error']=traceback.format_exc()
    job['elapsed_seconds']=time.time()-job['started']
    (Q/'Notes/full_v016_render.json').write_text(json.dumps(job,indent=2))
    if job['status']=='running':return .05
    if bpy.data.filepath==job['scene']:
        bpy.context.scene.frame_set(job['original_frame'])
        module.install()
    return None

bpy.app.timers.register(tick,first_interval=.1)
result={'started':True,'output':str(P),'frames':[1,756],'size':job['size']}

