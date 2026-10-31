"""T46 accepted T44v007 migration and strict packet publication. No rendering."""
import bpy,json,sys,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';S=T/'Scenes';sys.path.insert(0,str(HERE));sys.path.insert(0,str(A/'World/Scripts'))
from continuation_controls_v001 import attach_continuation
from build_sensing_v001 import save,snapshot,animate_event,dump
from acoustic_event_v002 import sample_native_event,validate_native_event
from acoustic_binding_v001 import make_controls
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def anim(o):return str([(fc.data_path,fc.array_index,[(p.co.x,p.co.y,p.interpolation) for p in fc.keyframe_points]) for layer in o.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]) if o.animation_data else None
assert sha(A/'BHA/BHA_film_v007.blend')=='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1'
for kind in ['A','B']:
 source=S/f'Sensing_reuse_{kind}_v008.blend';bpy.ops.wm.open_mainfile(filepath=str(source),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(17);before=snapshot();camera_keys=anim(s.camera);oldhash=sha(source)
 oldlibraries=[dict(name=l.name,path=bpy.path.abspath(l.filepath),parent=l.parent.name if l.parent else None) for l in bpy.data.libraries]
 resolved=[(l,Path(bpy.path.abspath(l.filepath)).resolve(strict=True)) for l in bpy.data.libraries]
 for l,p in resolved:l.filepath=str(p)
 direct=[l for l in bpy.data.libraries if not l.parent and Path(l.filepath).name=='BHA_film_v006.blend'];assert len(direct)==1
 direct[0].filepath=str(A/'BHA/BHA_film_v007.blend');direct[0].reload()
 hardware=[o for o in s.objects if o.instance_collection and o.instance_collection.name=='WORLD_HARDWARE'];assert len(hardware)==1
 attach_continuation(A,hardware[0]);bpy.context.view_layer.update()
 col=bpy.data.collections['LOCAL_ACOUSTIC_EVENTS']
 for o in list(col.objects):
  if o.name.startswith('ACOUSTICS_CONTROL_'):bpy.data.objects.remove(o,do_unlink=True)
  elif o.get('shared_package')=='Acoustics':o.animation_data_clear()
 previous=json.loads((E/f'events_{kind}_v002.json').read_text())['events'];events=[]
 for e in previous:
  s.frame_set(round(e['send_s']*24)+1);bpy.context.view_layer.update()
  event=sample_native_event(e['emitter_ref'],e['wall_source']['object'],e['event_id'],e['send_s'],e['contact_s'],e['receive_s'],e['patch_lifetime_s']);validate_native_event(event);events.append(event)
  obs={o['shared_prototype']:o for o in col.objects if o.name.startswith(e['event_id'])};animate_event(event,obs,s.frame_end,24,None);make_controls(event,obs,col,s.frame_end)
 s.frame_set(17);after=snapshot();assert before==after and camera_keys==anim(s.camera);assert oldhash==sha(source)
 s['event_export']=str((E/f'events_{kind}_v003.json').relative_to(ROOT)).replace('\\','/');s['upstream_release']='a08d0ecfbd6f3241298f506b3ea42613388b3baf / BHAv007 with nestedv006 preserved'
 save(S/f'Sensing_reuse_{kind}_v009.blend')
 dump(E/f'events_{kind}_v003.json',dict(contract='ecco-acoustic-event-v001',adapter='acoustic_event_v002',timing='leading front; per-front phases and packet end explicit',events=events))
 dump(E/f'migration_{kind}_v009.json',dict(source=str(source.relative_to(ROOT)).replace('\\','/'),source_sha256=oldhash,source_preserved=sha(source)==oldhash,before=before,after=after,camera_timing_controls_preserved=before==after,camera_keys_preserved=camera_keys==anim(s.camera),camera_animation=camera_keys,old_libraries=oldlibraries,procedure='Only direct BHAv006→v007; nestedv006 source retained; attach canonical continuation to existing hardware; strict cap sources and lagged packet timing; same local motion/camera'))
 print('SENSING_MIGRATED',kind,flush=True)
