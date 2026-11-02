"""Cheap working proof; each render includes file-write timing and enforces cap."""
import bpy,time,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=globals().get('proof_width',640);s.render.resolution_y=globals().get('proof_height',360);s.render.resolution_percentage=100;s.display.render_aa=globals().get('proof_aa','5')
s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.color_type='MATERIAL';s.render.image_settings.file_format='PNG'
timings=[]
frames=globals().get('proof_frames',[305,314,450,528])
for f in frames:
 s.frame_set(f);s.render.filepath=str(Q/'Previews'/f'integrated_v002_f{f:04}.png');start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
 timings.append({'frame':f,'seconds':elapsed});(Q/'Notes'/globals().get('proof_record','benchmarks_v002.json')).write_text(json.dumps(timings,indent=2))
 if elapsed>=5:raise RuntimeError('Render-to-file exceeded cap; stop and reduce working cost')
result={'renders':timings}
