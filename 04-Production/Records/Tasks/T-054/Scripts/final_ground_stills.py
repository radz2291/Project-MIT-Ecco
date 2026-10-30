import bpy,json,time
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';records=[]
for sid,f in [('S03',1),('S06',52)]:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{sid}_shared-digital_v002.blend'),load_ui=False);s=bpy.context.scene;s.frame_set(f);s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.eevee.use_raytracing=False;s.render.use_compositing=False;s.render.image_settings.file_format='PNG';s.render.filepath=str(T/'Previews'/f'{sid}_final-capped-ground_f{f:03}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start;records.append({'section':sid,'frame':f,'seconds':elapsed,'pass':elapsed<5,'settings':'640x360 Eevee8, no compositor/raytracing, full render-to-file'});(T/'Evidence/final-ground-timings.json').write_text(json.dumps(records,indent=2))
 if elapsed>=5:raise RuntimeError('Cap failed; stop')
print('GROUND_STILLS_DONE')
