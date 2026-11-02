import bpy,json,sys,math
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';A=R/'04-Production/Shared/Assets/Effects/Waveform';sys.path.insert(0,str(A/'Scripts'))
from pulse_asset_api import set_input
def coords(o,f):
 bpy.context.scene.frame_set(f);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=[tuple(x.co) for x in m.vertices];e.to_mesh_clear();return v
refs=[]
for version in ['v017','v018']:
 bpy.ops.wm.open_mainfile(filepath=str(A/f'Waveform_shared_{version}.blend'),use_scripts=False);refs.append(coords(bpy.data.objects['WF_PULSE_FIELD'],18))
assert refs[0]==refs[1],'compatibility defaults differ'
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v013.blend'),use_scripts=False);s=bpy.context.scene;assert s.frame_end==600
assert all(Path(bpy.path.abspath(x.filepath)).exists() for x in bpy.data.libraries)
o=bpy.data.objects['WF sequence event 1'];s.frame_set(318);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();ages=[x.value for x in m.attributes['wf17_age'].data];co=[x.co.copy() for x in m.vertices];flat=[]
for j in range(0,len(co)-3,4):
 if min(ages[j:j+4])>9:flat.append(abs(sum(v.z for v in co[j:j+4])/4))
assert flat and max(flat)<1e-8,('tail not flat',max(flat) if flat else None);e.to_mesh_clear()
assert all(x.hide_render for x in s.objects if 'localized contact contour' in x.name or 'contact digital nodes' in x.name)
rows=json.loads((Q/'Notes/waveform_v013_install.json').read_text())['events'];errors=[]
for row in rows:
 o=bpy.data.objects[f"WF sequence event {row['event']}"]
 for f in [row['return_start'],row['return_complete']]:
  s.frame_set(f);B=row['wall'];Apt=row['surface_hit'];hit=[]
  from mathutils import Vector
  d=(Vector(Apt)-Vector(B)).normalized()
  for ins in bpy.context.evaluated_depsgraph_get().object_instances:
   if ins.is_instance and ins.object.name==row['surface']:
    inv=ins.matrix_world.inverted();yes,p,n,i=ins.object.ray_cast(inv@Vector(B),(inv.to_3x3()@d).normalized())
    if yes:hit.append((ins.matrix_world@p-Vector(Apt)).length)
  assert hit and min(hit)<.0001;errors.append(min(hit))
(Q/'Notes/waveform_v013_verification.json').write_text(json.dumps({'default_v018_equals_v017':True,'flat_tail_ring_centers_count':len(flat),'max_flat_tail_offset_m':max(flat),'fresh_reopen_links':True,'hidden_impact_rings':True,'return_cap_ray_error_max_m':max(errors),'return_samples':len(errors),'scene_frames':600},indent=2));print('V013_VERIFY_PASS')
