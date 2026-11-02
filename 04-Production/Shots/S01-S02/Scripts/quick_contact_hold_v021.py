"""Hold the handshake patch until the first glitch tiles take over."""
import bpy,json,time
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');out=Q/'Scenes/Waveform_contact_hold_fast_v021.blend';assert not out.exists();assert 'contact_fast_v020' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_contact_hold_{int(time.time())}.blend'),copy=True,compress=True)
ob=bpy.data.objects['Handshake — subtle surface contact patch'];ob.animation_data_clear()
for f,v in [(304,0.),(305,.45),(306,1.),(322,1.),(323,0.)]:ob.scale=(v,v,v);ob.keyframe_insert('scale',frame=f)
for l in ob.animation_data.action.layers:
 for st in l.strips:
  for bag in st.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
bpy.context.scene.frame_set(320);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_contact_hold_v021.json').write_text(json.dumps({'scene':str(out),'change':'contact patch persists from handshake arrival305 through glitch onset322; one-frame handover, gone323','patch_size_mm':3,'pulse_and_tile_reveal':'unchanged from quickv020','preview':[300,353],'fps':24},indent=2));result={'saved':str(out),'hold_until':322}
