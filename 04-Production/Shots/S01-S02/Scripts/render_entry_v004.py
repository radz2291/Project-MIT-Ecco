import bpy,time,json
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=480;s.render.resolution_y=270;s.render.resolution_percentage=100;s.display.render_aa='OFF';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.shading.color_type='MATERIAL';s.render.image_settings.file_format='PNG';records=[]
for f in globals().get('entry_frames',[85,91,93,94,95,97,105]):
 s.frame_set(f);s.render.filepath=str(Q/'Previews/Entry-v004'/f'entry_v004_{f:04}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;records.append({'frame':f,'seconds':dt});(Q/'Notes'/globals().get('entry_record','entry_v004_benchmarks.json')).write_text(json.dumps(records,indent=2))
 if dt>=5:raise RuntimeError('Stop: render-to-file cap failed')
result={'renders':records}
