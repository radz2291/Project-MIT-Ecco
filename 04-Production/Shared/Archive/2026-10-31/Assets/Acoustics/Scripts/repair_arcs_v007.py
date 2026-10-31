"""Thin readable fan orientation; preserve true endpoints and camera/timing."""
import bpy,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';S=T/'Scenes';E=T/'Evidence';A=ROOT/'04-Production/Shared/Assets/Acoustics';sys.path.insert(0,str(HERE))
from build_sensing_v001 import master,animate_event,save,dump,snapshot
from acoustic_binding_v001 import make_controls
def anim(o):return str([(fc.data_path,fc.array_index,[(p.co.x,p.co.y) for p in fc.keyframe_points]) for layer in o.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]) if o.animation_data else None
if not (A/'Acoustics_v003.blend').exists():master('v003',.00012)
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(S/f'Sensing_reuse_{kind}_v006.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;before=snapshot();beforecam=anim(s.camera)
 resolved=[(l,Path(bpy.path.abspath(l.filepath)).resolve()) for l in bpy.data.libraries]
 for l,p in resolved:l.filepath=str(p)
 for l in list(bpy.data.libraries):
  if Path(l.filepath).name=='Acoustics_v002.blend':l.filepath=str(A/'Acoustics_v003.blend');l.reload()
 col=bpy.data.collections['LOCAL_ACOUSTIC_EVENTS']
 for o in list(col.objects):
  if o.name.startswith('ACOUSTICS_CONTROL_'):bpy.data.objects.remove(o,do_unlink=True)
  elif o.get('shared_package')=='Acoustics':o.animation_data_clear()
 events=json.loads((E/f'events_{kind}_v002.json').read_text())['events']
 for e in events:
  obs={o['shared_prototype']:o for o in col.objects if o.name.startswith(e['event_id'])};animate_event(e,obs,s.frame_end,24,None);make_controls(e,obs,col,s.frame_end)
 s.frame_set(17);after=snapshot();aftercam=anim(s.camera);assert before==after and beforecam==aftercam
 save(S/f'Sensing_reuse_{kind}_v007.blend');dump(E/f'migration_{kind}_v007.json',dict(before=before,after=after,preserved=before==after,camera_keys_preserved=beforecam==aftercam,camera_animation=aftercam,shared_revision='v003 arcs0.12mm radius; local fan faces along-X macro camera. True event positions/timings/camera unchanged.'))
