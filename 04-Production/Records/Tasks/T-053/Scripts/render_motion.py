import bpy,pathlib,json,time
ROOT=pathlib.Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-053';P=T/'Previews';F=P/'MotionFrames';F.mkdir(exist_ok=True)
records=[]
for name,frames in [('T44_open',[1]),('S02',[241,300,360,420,450,480,505,528])]:
 bpy.ops.wm.open_mainfile(filepath=str(T/'Scenes'/f'{name}_World_v010.blend'),load_ui=False)
 s=bpy.context.scene;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
 s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.render_aa='8';s.render.image_settings.file_format='PNG'
 for i,f in enumerate(frames):
  s.frame_set(f);s.render.filepath=str((P/f'T44_open_f{f:03d}_World_v010.png') if name!='S02' else F/f'{i:03d}.png')
  t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
  records.append(dict(consumer=name,frame=f,seconds_full_render_to_file=elapsed,pass_under_5=elapsed<5,output=s.render.filepath))
  (T/'Evidence/motion-benchmarks.json').write_text(json.dumps(records,indent=2))
  print('FRAME',name,f,elapsed,flush=True)
  if elapsed>=5:raise RuntimeError('Budget failed; no further batch')
