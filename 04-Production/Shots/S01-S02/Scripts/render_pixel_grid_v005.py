"""Run in connected Blender; export scene depth plus fixed-pixel guide strokes."""
import bpy,time,json,types
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';P=Q/'Previews/Pixel-grid-v005';P.mkdir(exist_ok=True)
source=R/'04-Production/Shared/Assets/Environment/Borehole/Scripts/pixel_guides_viewport.py'
module=types.ModuleType('ecco_pixel_guides');exec(compile(source.read_text(),str(source),'exec'),module.__dict__)
bpy.app.driver_namespace['ecco_pixel_module']=module;module.install();s=bpy.context.scene;records=[]
for f in globals().get('pixel_frames',[80,95,106,138,157]):
 s.frame_set(f);t=time.perf_counter();module.export(P/f'pixel_v005_{f:04}.png',480,270);seconds=time.perf_counter()-t
 records.append({'frame':f,'seconds':seconds});(Q/'Notes'/globals().get('pixel_record','pixel_grid_v005_benchmarks.json')).write_text(json.dumps(records,indent=2))
 if seconds>=5:raise RuntimeError('Stop: render-to-file cap failed')
result={'renders':records,'method':'GPUOffScreen scene depth plus fixed-pixel POLYLINE_UNIFORM_COLOR strokes'}
