"""Bipolar pulse and tighter exchange timing, first-event review only."""
import bpy,json,sys,time
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input
out=Q/'Scenes/Waveform_pulse_fast_v017.blend';assert not out.exists();assert 'fast_v016' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_pulse_v017_{int(time.time())}.blend'),copy=True,compress=True)
o=bpy.data.objects['WF sequence event 1'];m=o.modifiers[0]
settings={'Beam setup frames':6.,'Beam closing frames':3.,'Travel frames':12.,'Return travel override':12.,'Tail allowance':9.,'Reflection delay':1.,'Pulse width':1.3,'Spike width':.5,'Height m':.0085,'Pre dip':.2,'Undershoot':1.,'Rebound':.08,'Dispersion':.15,'Flat after age':5.,'Head fade':.8,'Tail fade':1.2}
for k,v in settings.items():set_input(m,k,v)
w=bpy.data.objects['ONE WALL - old history and current cells share topology']
for p in w.data.polygons:
 if w.data.materials[p.material_index].name.startswith('Unified cell 1 '):w.data.attributes['ecco_receipt_frame'].data[p.index].value=321
for n in w.modifiers[0].node_group.nodes:
 if n.type=='GROUP' and 'Settle frames' in n.inputs:n.inputs['Settle frames'].default_value=4
for mat in bpy.data.materials:
 if mat.name.startswith('Unified cell 1 ') and mat.animation_data and mat.animation_data.action:
  for l in mat.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      points=list(fc.keyframe_points);values=[k.co.y for k in points]
      for k,f in zip(points,[321,324,326]):k.co.x=f;k.handle_left.x=f;k.handle_right.x=f
s=bpy.context.scene;s.frame_start=300;s.frame_end=353;s.frame_set(315);bpy.context.view_layer.update();e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=e.to_mesh();centers=[sum(v.co.z for v in mesh.vertices[i:i+4])/4 for i in range(0,len(mesh.vertices),4)];extrema=[min(centers),max(centers)];e.to_mesh_clear();assert extrema[0]<-.001 and extrema[1]>.001,extrema
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_pulse_v017.json').write_text(json.dumps({'scene':str(out),'scope':'First-exchange quick review only, full scene remainsv015','settings':settings,'beam_opening_frames':5,'frames':[300,353],'fps':24,'duration_seconds':2.25,'signed_amplitude_at315_m':extrema,'timing':{'pulse_launch':306,'impact_tile':322,'tile_settled':326,'feedback_launch':328,'feedback_complete':349,'beam_closed':352}},indent=2));result={'saved':str(out),'signed_amplitude':extrema}
