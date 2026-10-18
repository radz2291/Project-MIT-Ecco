"""Rebind cased actual-cap events with strict T46 packet/source contract."""
import bpy,sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
sys.path.insert(0,str(A/'Acoustics/Scripts'));sys.path.insert(0,str(A/'CasedHole/Scripts'))
from acoustic_event_v002 import sample_native_event,validate_event,validate_native_event
from acoustic_binding_v001 import bind_event
from cased_controls_v001 import add_response
from integrate_cased_v001 import overlay
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
src=S/'CasedSupport_v008.blend';out=S/'CasedSupport_v009.blend';assert not out.exists();before_hash=sha(src)
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);camera=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens);timing=[s.frame_start,s.frame_end,s.render.fps];c=bpy.data.collections['LOCAL_CASED_RESPONSE']
for ob in list(c.objects):bpy.data.objects.remove(ob,do_unlink=True)
events=[];responses=[]
for k,state,send,contact,receive in [(1,'supported',.25,.65,1.05),(2,'weakly_supported',1.8,2.2,2.6)]:
 s.frame_set(1);e=sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_NOMINAL_CUTAWAY','t47-cased-native-%02d'%k,send,contact,receive,emitter_surface_name='TEMP | Imaging port 1 | removable acoustic cap');validate_event(e);validate_native_event(e);events.append(e);bind_event(e,c,s.frame_end,24,'v003');responses.append(add_response(e,state,c))
overlay(c);s.frame_set(1);assert camera==dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens) and timing==[s.frame_start,s.frame_end,s.render.fps]
s['event_export']='04-Production/Records/Tasks/T-047/Evidence/actual-cased-events_v009.json';s['timing_reference']='Leading-front seconds with declared lagged three-front packets; actual cap held through final return. Qualitative response has explicit independently sampled lifetime.'
for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);assert sha(src)==before_hash
(E/'actual-cased-events_v009.json').write_text(json.dumps(dict(contract='ecco-acoustic-event-v001',extension='T46 strict native cap + three-front packet intervals',events=events,responses=responses,acoustic_library='Acoustics_v003.blend',acoustic_library_sha256=sha(A/'Acoustics/Acoustics_v003.blend'),fixture_replaced=True),indent=2),encoding='utf8')
(E/'strict-rebind-migration_v009.json').write_text(json.dumps(dict(source=src.relative_to(ROOT).as_posix(),source_sha256=before_hash,candidate=out.relative_to(ROOT).as_posix(),sha256=sha(out),camera=camera,timing=timing,camera_timing_preserved=True,limits='Packet/source metadata stricter; geometry/prototypes/camera unchanged. Response visibility now exactly samples declared contact/end seconds.'),indent=2),encoding='utf8')
print('T47_STRICT_REBIND_PASS',flush=True)
