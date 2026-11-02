"""Hide non-final previs geometry and the unselected point overlay; retain approved effects."""
import bpy,json,sys,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
sys.path.insert(0,str(Q/'Scripts'))
from final_render_visibility import establish_final_visibility
from final_surface_lines_v018 import configure
assert bpy.data.filepath.endswith('S01-S02_production_v017.blend')
out=Q/'Scenes/S01-S02_production_v018.blend';assert not out.exists()
configure()
newly_hidden=establish_final_visibility()
text=bpy.data.texts.new('START HERE — final display')
text.write("""# Final display exports must respect render visibility.
# Approved: physical BHA/well, waveform, active contact patch, tile reveal and environment motion grid.
# Excluded: old previs target plates/history helpers, old waves/impact rings and extra point overlay.
# Saved display state also hides exclusions for interactive review.
import bpy,sys
from pathlib import Path
folder=Path(bpy.path.abspath('//../Scripts'))
if str(folder) not in sys.path:sys.path.insert(0,str(folder))
import final_render_visibility as final_display
final_display.establish_final_visibility()
# In a Blender window, render a still using:
# final_display.export(absolute_png_path,1920,1080)
""")
bpy.context.scene['Final display profile']='v018: render-intent visibility, no extra measurement point overlay; use START HERE — final display'
bpy.context.scene.frame_set(315)
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v017.blend','newly_hidden_from_viewport_exports':newly_hidden,'extra_measurement_point_overlay_enabled':False,'preserved':['physical BHA/well/environment','all six shared v021 beam/pulse/contact/tile exchanges','v017 camera pullback474–720 and wide hold720–756','owner-requested environment pixel motion grids'],'export_rule':'Use final_render_visibility.export; render-hidden objects and render-disabled collections cannot leak into viewport stills.','shared_masters_modified':False,'scope':'Display visibility only; camera, topology and approved animation values unchanged.','review':'Two stills for owner confirmation; final appearance acceptance pending.'}
(Q/'Notes/final_display_v018.json').write_text(json.dumps(record,indent=2))
result={'saved':str(out),'newly_hidden':len(newly_hidden),'names':newly_hidden}
