"""Intentional macro camera revision after finite far-rim coverage finding."""
import bpy,sys,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence';src=S/'CasedSupport_v009.blend';out=S/'CasedSupport_v010.blend';assert not out.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def keys():
 return {o.name:[(fc.data_path,fc.array_index,[list(k.co) for k in fc.keyframe_points]) for l in o.animation_data.action.layers for st in l.strips for b in st.channelbags for fc in b.fcurves] for o in bpy.data.objects if not o.library and o.animation_data and o.animation_data.action}
source_hash=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);before_keys=keys();before=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens);events=json.loads((E/'actual-cased-events_v009.json').read_text())['events'];e=events[0];origin=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);direction=Vector(e['direction_world']);s.camera.location=origin+Vector((-.05,0,0))+direction*.020;s.camera.rotation_euler=((origin+hit)/2-s.camera.location).to_track_quat('-Z','Y').to_euler();assert keys()==before_keys
after=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens);s['camera_revision']='v010 deliberate downhole-facing macro; source/events/controls/timing unchanged. Previous uphole-facing camera showed distant finite collar rim.'
for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);assert sha(src)==source_hash
(E/'intentional-camera-revision_v010.json').write_text(json.dumps(dict(source=src.relative_to(ROOT).as_posix(),source_sha256=source_hash,candidate=out.relative_to(ROOT).as_posix(),sha256=sha(out),before=before,after=after,all_animation_keys_preserved=True,timing=[s.frame_start,s.frame_end,s.render.fps],change='Only axial camera offset +.05→−.05m and look direction; addresses actual finite uphole-rim visibility. This follows completed separately documented migration camera preservation.',event_export='actual-cased-events_v009.json'),indent=2),encoding='utf8');print('T47_CAMERA10_SAVED',flush=True)
