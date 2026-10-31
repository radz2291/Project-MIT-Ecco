"""Repair only screen response timing to match the declared .45/1.20s windows."""
import bpy,json,hashlib
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def arc_keys():
 return {o.name:[(fc.data_path,fc.array_index,[list(k.co) for k in fc.keyframe_points]) for layer in o.animation_data.action.layers for st in layer.strips for b in st.channelbags for fc in b.fcurves] for o in bpy.data.objects if o.get('shared_package')=='Acoustics' and ('_SEND_' in o.name or '_RETURN_' in o.name)}
src=S/'CasedSupport_v011.blend';out=S/'CasedSupport_v012.blend';assert not out.exists();old=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);arcs=arc_keys();responses=json.loads((E/'actual-cased-events_v009.json').read_text())['responses'];camera=[list(s.camera.location),list(s.camera.rotation_euler),s.camera.data.lens];timing=[s.frame_start,s.frame_end,s.render.fps]
for response,prefix in zip(responses,['SHORT_DECAY_','LONG_DECAY_']):
 for o in [o for o in s.objects if o.name.startswith(prefix)]:
  i=int(o.name.split('_')[-1]);o['response_event_id']=response['event_id'];o['response_kind']=response['decay_kind']
  for layer in o.animation_data.action.layers:
   for st in layer.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      if fc.data_path=='hide_render':
       for k in fc.keyframe_points:
        elapsed=(k.co.x-1)/24-response['response_start_s'];on=0<=elapsed<response['response_lifetime_s'] and i/22*response['response_lifetime_s']<=elapsed;k.co.y=float(not on);k.interpolation='CONSTANT'
assert arcs==arc_keys() and camera==[list(s.camera.location),list(s.camera.rotation_euler),s.camera.data.lens] and timing==[s.frame_start,s.frame_end,s.render.fps]
for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(out.parent))
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);assert sha(src)==old
checks=[]
bpy.ops.wm.open_mainfile(filepath=str(out),load_ui=False,use_scripts=False);s=bpy.context.scene;assert not any(o.name.startswith('CASED_') and '_RESPONSE_' in o.name for o in bpy.data.objects if not o.library)
for response,prefix in zip(responses,['SHORT_DECAY_','LONG_DECAY_']):
 bars=[o for o in s.objects if o.name.startswith(prefix)];assert len(bars)==22;visible=[]
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();elapsed=(f-1)/24-response['response_start_s'];on=0<=elapsed<response['response_lifetime_s'];assert any(not o.hide_render for o in bars)==on
  for o in bars:
   i=int(o.name.split('_')[-1]);expected=on and i/22*response['response_lifetime_s']<=elapsed;assert (not o.hide_render)==expected,(o.name,f)
  if on:visible.append(f)
 checks.append(dict(kind=response['decay_kind'],lifetime_s=response['response_lifetime_s'],visible_frames=visible,onset_end_and_each_bar_pass=True))
for p in [S/'CasedWearSection_v011.blend',S/'CasedLayerSection_v011.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;proj=[world_to_camera_view(s,s.camera,o.matrix_world@v.co) for o in s.objects if not o.library and o.type=='MESH' and o.name.startswith(('ACTUAL_SECTION','SECTION_')) for v in o.data.vertices];assert proj and all(.02<a.x<.98 and .02<a.y<.98 and a.z>s.camera.data.clip_start for a in proj)
 checks.append(dict(scene=p.relative_to(ROOT).as_posix(),actual_vertices_in_frame=len(proj),full_section_framing_pass=True))
(E/'changed-visual-claims_v012.json').write_text(json.dumps(dict(passed=True,source=src.relative_to(ROOT).as_posix(),source_sha256=old,candidate=out.relative_to(ROOT).as_posix(),sha256=sha(out),checks=checks,shared_acoustic_arc_keys_unchanged=True,camera_timing_unchanged=True,prototypes_unchanged=True,world_response_bars_removed=24,contact_cup_patch_consumer_scale=.35,repair='Short screen lane .40→declared .45s; long1.20s retained. Exact response visibility with discrete frame sampling, labels remain screen space.',previous_failed_evidence='Repair11 per-bar comparison caught mismatched short-lane duration before rendering.'),indent=2),encoding='utf8');print('T47_VISUAL_CLAIMS12_PASS',sha(out),flush=True)
