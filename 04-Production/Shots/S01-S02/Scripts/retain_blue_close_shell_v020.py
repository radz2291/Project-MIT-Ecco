"""Retain acquired blue patches and close the presentation cutaway during pullback."""
import bpy,json,hashlib,datetime
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v019.blend')
out=Q/'Scenes/S01-S02_production_v020.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_persistent_blue_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
s=bpy.context.scene;wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];changed=[]
for mat in wall.data.materials:
 if not mat.name.startswith('Approved tile glitch '):continue
 mat.animation_data.action=mat.animation_data.action.copy()
 for layer in mat.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     if fc.data_path!='diffuse_color' or fc.array_index!=3:continue
     peak=max(k.co.y for k in fc.keyframe_points);first_peak=min(k.co.x for k in fc.keyframe_points if abs(k.co.y-peak)<1e-6)
     for i in range(len(fc.keyframe_points)-1,-1,-1):
      if fc.keyframe_points[i].co.x>first_peak:fc.keyframe_points.remove(fc.keyframe_points[i],fast=True)
     fc.keyframe_points.insert(s.frame_end,peak)
     for k in fc.keyframe_points:
      if k.co.x>=first_peak:k.interpolation='CONSTANT'
     fc.extrapolation='CONSTANT';fc.update()
     changed.append({'material':mat.name,'opacity':peak,'holds_from':first_peak})
assert len(changed)==24,len(changed)
mod=wall.modifiers['Shot camera viewing wedge — inspection cutaway']
angle=next(x for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name=='Viewing half angle degrees');angle.min_value=0
angle_id=angle.identifier;enabled_id=next(x.identifier for x in mod.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name=='Enabled')
for f,v in [(1,30.),(474,30.),(540,0.),(756,0.)]:
 p=getattr(mod.properties.inputs,angle_id);p.value=v;p.keyframe_insert('value',frame=f)
for f,v in [(1,True),(539,True),(540,False),(756,False)]:
 p=getattr(mod.properties.inputs,enabled_id);p.value=v;p.keyframe_insert('value',frame=f)
for layer in wall.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    if angle_id in fc.data_path:
     for k in fc.keyframe_points:k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
    elif enabled_id in fc.data_path:
     for k in fc.keyframe_points:k.interpolation='CONSTANT'
wall['Recorded blue opacity']=.4;wall['Shell closure frames']='474–540; fully closed for wide shot';wall['Persistence']='Acquired panel alpha holds at its established 0.4 peak; RGB settles to approved blue; no fade-out.'
s.frame_set(756);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v019.blend','material_changes':changed,'shell_closes':[474,540],'wide_cutaway_enabled':False,'scope':'Local measurement material opacity and shot cutaway input animation only.','unchanged':['beam/pulse/contact and tile geometry/reveal timing','camera and BHA motion','v019 glitch-derived edge fix','final-display cleanup','shared masters'],'reason':'Owner requests connected shell in wide view and persistent blue records after send/receive.'}
(Q/'Notes/persistent_blue_v020.json').write_text(json.dumps(record,indent=2))
result={'saved':str(out),'held_blue_materials':len(changed),'closure_frames':[474,540]}
