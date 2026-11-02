"""Fast owner-review variant; first exchange only, no full-shot migration."""
import bpy,json,sys,time
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input
out=Q/'Scenes/Waveform_pulse_fast_v016.blend';assert not out.exists();assert 'v015' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_fast_pulse_{int(time.time())}.blend'),copy=True,compress=True)
m=bpy.data.objects['WF sequence event 1'].modifiers[0]
p={'Travel frames':18.,'Return travel override':18.,'Tail allowance':16.,'Reflection delay':8.,'Pulse width':1.5,'Spike width':.65,'Height m':.0075,'Pre dip':.12,'Undershoot':.28,'Rebound':.10,'Dispersion':.25,'Strand phase offset':.22,'Amplitude breath':.22,'Breath period frames':32.}
for k,v in p.items():set_input(m,k,v)
# First impact: setup8+travel18+1.5*2.1*1.25 ~=30frames.
w=bpy.data.objects['ONE WALL - old history and current cells share topology']
for poly in w.data.polygons:
 if w.data.materials[poly.material_index].name.startswith('Unified cell 1 '):w.data.attributes['ecco_receipt_frame'].data[poly.index].value=329
for mat in bpy.data.materials:
 if mat.name.startswith('Unified cell 1 ') and mat.animation_data and mat.animation_data.action:
  for l in mat.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for key in fc.keyframe_points:key.co.x-=11;key.handle_left.x-=11;key.handle_right.x-=11
s=bpy.context.scene;s.frame_start=300;s.frame_end=395;s.frame_set(323);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_pulse_v016.json').write_text(json.dumps({'scene':str(out),'scope':'First exchange4second review, whole scene migration pending pulse approval','settings':p,'beam':'unchanged5frameopening,cyan/violet,continuous,nodots','frames':[300,395],'fps':24,'tile_impact':330},indent=2));result={'saved':str(out)}
