import bpy,time,json,sys
from pathlib import Path
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S02_shared-descent_v001.blend'),load_ui=False);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.display.render_aa='32';s.render.image_settings.file_format='PNG'
records=[]
for label,frames in [('subsea',range(60,121,2)),('destination',range(228,277,2))]:
 dest=T/'Frames'/label;dest.mkdir(parents=True,exist_ok=True)
 for index,f in enumerate(frames):
  s.frame_set(f);s.render.filepath=str(dest/f'{index:04}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
  records.append({'clip':label,'frame':f,'seconds':elapsed,'pass':elapsed<5});print(label,f,elapsed,flush=True)
  if elapsed>=5:
   (T/'Evidence/motion-timings.json').write_text(json.dumps(records,indent=2));raise RuntimeError('Frame cap failed')
(T/'Evidence/motion-timings.json').write_text(json.dumps(records,indent=2))
