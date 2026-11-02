"""Restore original authored tile flicker, retaining approved signal v017."""
import bpy,json,re,time,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');out=Q/'Scenes/Waveform_reveal_fast_v018.blend';assert not out.exists();assert 'fast_v017' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Before_reveal_v018_{int(time.time())}.blend'),copy=True,compress=True)
s=bpy.context.scene;o=bpy.data.objects['WF sequence event 1']
def waveform_hash():
 s.frame_set(315);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();h=hashlib.sha256(str([tuple(v.co) for v in me.vertices]).encode()).hexdigest();e.to_mesh_clear();return h
before=waveform_hash();w=bpy.data.objects['ONE WALL - old history and current cells share topology'];names=sorted({w.data.materials[p.material_index].name for p in w.data.polygons if w.data.materials[p.material_index].name.startswith('Unified cell 1 ')})
with bpy.data.libraries.load(str(Q/'Scenes/S01-S02_production_v007.blend'),link=False) as (a,b):b.materials=list(names)
for name,source in zip(names,b.materials):
 assert source and source.animation_data and source.animation_data.action,name
 target=bpy.data.materials[name];target.diffuse_color=tuple(source.diffuse_color);target.animation_data_clear();target.animation_data_create();action=source.animation_data.action.copy();target.animation_data.action=action;target.animation_data.action_slot=action.slots[0]
 for l in action.layers:
  for st in l.strips:
   for bag in st.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      k.co.x=322+(k.co.x-318)*.5;k.handle_left.x=322+(k.handle_left.x-318)*.5;k.handle_right.x=322+(k.handle_right.x-318)*.5
groups={}
for p in w.data.polygons:
 name=w.data.materials[p.material_index].name
 if name.startswith('Unified cell 1 '):
  group=int(re.search(r'reveal(\d+)',name)[1]);w.data.attributes['ecco_reveal_order'].data[p.index].value=group*1.5;groups[group]=groups.get(group,0)+1
assert waveform_hash()==before
s.frame_set(325);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/quick_reveal_v018.json').write_text(json.dumps({'scene':str(out),'scope':'Surface-only first-exchange review; approved v017 signal unchanged','original_reveal_source':'S01-S02_production_v007.blend current-cell diffuse actions','material_timing':'old impact318 maps322, original flicker timing scaled.5','tile_groups':groups,'geometry_stagger_offsets':[0,1.5,3,4.5],'settle_per_tile_frames':4,'signal_geometry_hash_315_unchanged':before,'preview':[300,353],'fps':24},indent=2));result={'saved':str(out),'groups':groups}
