import bpy,json,time,sys
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';P=T/'Previews';P.mkdir(exist_ok=True)
jobs=[('Reveal_two-shapes_v001',20),('Reveal_two-shapes_v001',45),('S03_shared-digital_v002',1),('S03_shared-digital_v002',120),('S06_shared-digital_v002',52),('S02_shared-reveal_v001',480)]
out=[]
for name,f in jobs:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{name}.blend'),load_ui=False);s=bpy.context.scene;s.frame_set(f);s.render.engine='BLENDER_WORKBENCH' if name.startswith('S02') else 'BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=8;s.render.image_settings.file_format='PNG';s.render.filepath=str(P/f'{name}_f{f:03}_refined.png');s.render.use_compositing=False;s.eevee.use_raytracing=False
 t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t;out.append({'scene':name,'frame':f,'seconds':elapsed,'pass':elapsed<5,'settings':'640x360 full render-to-file; Eevee8 except S02 Workbench; compositing/raytracing disabled; saved cameras unchanged'});(T/'Evidence/render-benchmarks.json').write_text(json.dumps(out,indent=2));print(out[-1],flush=True)
 if elapsed>=5:print('CAP_FAIL_STOP',flush=True);break
