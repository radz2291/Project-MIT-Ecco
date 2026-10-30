import bpy,pathlib,json,time,sys
ROOT=pathlib.Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-053';P=T/'Previews';P.mkdir(exist_ok=True)
jobs=[('S02',528),('T44_layers',1)]
results=[]
for name,frame in jobs:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Scenes'/f'{name}_World_v010.blend'),load_ui=False)
 s=bpy.context.scene;s.frame_set(frame)
 s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
 s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True
 s.display.shading.cavity_type='BOTH';s.display.render_aa='8'
 s.render.image_settings.file_format='PNG';s.render.filepath=str(P/f'{name}_f{frame:03d}_World_v010.png')
 t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
 results.append(dict(consumer=name,frame=frame,engine=s.render.engine,resolution=[960,540],aa='8',seconds_full_render_to_file=elapsed,pass_under_5=elapsed<5,output=s.render.filepath))
 (T/'Evidence/render-benchmarks.json').write_text(json.dumps(results,indent=2))
 print('BENCHMARK',name,elapsed,flush=True)
