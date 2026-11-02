import bpy,time,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=480;s.render.resolution_y=270;s.render.resolution_percentage=100;s.display.render_aa='OFF';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.color_type='MATERIAL';s.render.image_settings.file_format='PNG'
timings=[]
for f in globals().get('entry_frames',[1,80,94,97,106,120,132,152]):
 s.frame_set(f);s.render.filepath=str(Q/'Previews/Entry-v003'/f'entry_v003_{f:04}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start;timings.append({'frame':f,'seconds':elapsed})
 (Q/'Notes'/globals().get('entry_record','entry_v003_benchmark.json')).write_text(json.dumps(timings,indent=2))
 if elapsed>=5:raise RuntimeError('Stop: full render-to-file cap failed')
result={'timings':timings}
