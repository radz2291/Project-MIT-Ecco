import bpy,time,json,sys
from pathlib import Path
T=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S02_shared-descent_v002.blend'),load_ui=False);s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.display.render_aa='32';s.render.image_settings.file_format='PNG'
motion='motion' in sys.argv;frames=list(range(60,121,2)) if motion else [94,96]
dest=T/'Frames/subsea-v002' if motion else T/'Previews';dest.mkdir(parents=True,exist_ok=True);records=[]
for index,f in enumerate(frames):
 s.frame_set(f);s.render.filepath=str(dest/(f'{index:04}.png' if motion else f'S02_cutaway_f{f:03}_v002.png'))
 t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;records.append({'frame':f,'seconds':elapsed,'pass':elapsed<5})
 if elapsed>=5:break
(T/'Evidence'/('cutaway-motion-timings.json' if motion else 'cutaway-benchmarks.json')).write_text(json.dumps(records,indent=2))
print('DONE',len(records),max(r['seconds'] for r in records))
