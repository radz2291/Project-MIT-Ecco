"""An active contact patch that persists until tile handover."""
import bpy,json,time
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');out=Q/'Scenes/Waveform_active_patch_fast_v022.blend';assert not out.exists();assert 'hold_fast_v021' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_active_patch_{int(time.time())}.blend'),copy=True,compress=True)
ob=bpy.data.objects['Handshake — subtle surface contact patch'];ob.animation_data_clear();mat=ob.data.materials[0];mat.animation_data_clear();base=(.17,.43,.46)
keys=[(304,0.),(305,.45)]+[(f,1. if ((f-306)//2)%2==0 else .78) for f in range(306,323,2)]+[(323,0.)]
for f,v in keys:
 ob.scale=(v,v,v);ob.keyframe_insert('scale',frame=f);gain=.83+.17*v;mat.diffuse_color=tuple(c*gain for c in base)+(1.,);mat.keyframe_insert('diffuse_color',frame=f)
for obj in [ob,mat]:
 for l in obj.animation_data.action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
bpy.context.scene.frame_set(316);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_active_patch_v022.json').write_text(json.dumps({'scene':str(out),'change':'gentle continuous size/brightness breathing on contact patch; persists until glitch','size_range_mm':[2.34,3.0],'breath_period_frames':4,'visible_from':305,'holds_through':322,'gone':323,'beam_pulse_glitch':'unchanged from quickv021','preview':[300,353],'fps':24},indent=2));result={'saved':str(out)}
