import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Effects/Waveform';sys.path.insert(0,str(B/'Scripts'))
from pulse_asset_api import get_input,arrival_readouts
def coords(ob,f):
 bpy.context.scene.frame_set(f);e=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();v=[tuple(x.co) for x in me.vertices];e.to_mesh_clear();return v
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/Waveform_active_patch_fast_v022.blend'),use_scripts=False);ref={f:coords(bpy.data.objects['WF sequence event 1'],f) for f in [301,305,310,315,322,328,335,349,352]}
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v016.blend'),use_scripts=False);s=bpy.context.scene;assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries);errors=[]
for f,v in ref.items():
 actual=coords(bpy.data.objects['WF sequence event 1'],f);assert len(v)==len(actual);errors.extend((Vector(a)-Vector(b)).length for a,b in zip(actual,v))
assert max(errors)<1e-6,max(errors)
data=json.loads((Q/'Notes/approved_v016_integration.json').read_text());rows=[]
for r in data['events']:
 i=r['event'];start=r['start'];o=bpy.data.objects[f'WF sequence event {i}'];m=o.modifiers[0];assert m.node_group.library and 'v021' in m.node_group.library.filepath
 s.frame_set(start+15);marks=arrival_readouts(o);assert abs(marks['Return tail arrival']-(start+49))<.001
 pose=None
 for f in [start+28,start+49,start+52]:
  s.frame_set(f);p=[tuple(v) for v in bpy.data.objects['BHA sequence assembly'].matrix_world];assert pose is None or pose==p;pose=p
 assert not coords(o,start-1) and not coords(o,start+53)
 patch=bpy.data.objects[f'Contact patch event {i}'];s.frame_set(start+15);assert patch.scale.x>0 and not patch.hide_render;s.frame_set(start+23);assert max(patch.scale)<.000001
 rows.append({'event':i,'shared_version':'v021','center_error_mm':r['center_error_mm'],'returns_before_turn':True,'patch_holds_and_hands_over':True})
s.frame_set(315);s.frame_start=300;s.frame_end=353;s.name='APPROVED EXCHANGE — first target fixture';demo=R/'04-Production/Shared/Demos/Beam_exchange_approved_demo_v021.blend';assert not demo.exists();bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(demo),use_scripts=False);assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
(Q/'Notes/approved_v016_verification.json').write_text(json.dumps({'reopen_links':True,'first_event_matches_approved_sample_frames':len(ref),'max_position_error_m':max(errors),'six_event_checks':rows,'demo':str(demo),'demo_sha256':hashlib.sha256(demo.read_bytes()).hexdigest(),'demo_relative_links_resolve':True,'production_unchanged_by_demo_save':True},indent=2));print('APPROVED_SIX_EVENTS_PASS')
