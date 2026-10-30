import bpy,json,time,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';P=T/'Previews';P.mkdir(exist_ok=True)
jobs=[('Reveal_two-shapes_v001',20),('Reveal_two-shapes_v001',45),('S03_shared-digital_v001',1),('S03_shared-digital_v001',120),('S06_shared-digital_v001',52),('S02_shared-reveal_v001',480)]
out=[]
for name,f in jobs:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{name}.blend'),load_ui=False);s=bpy.context.scene;s.frame_set(f);s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.render.image_settings.file_format='PNG';s.render.filepath=str(P/f'{name}_f{f:03}.png')
 t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;out.append({'scene':name,'frame':f,'seconds':elapsed,'pass':elapsed<5,'settings':'640x360 Eevee8 full render-to-file'});(T/'Evidence/render-benchmarks.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
 if elapsed>=5:print('CAP_FAIL_STOP',flush=True);break
