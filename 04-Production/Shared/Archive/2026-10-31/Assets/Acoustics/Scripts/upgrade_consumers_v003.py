import bpy,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';S=T/'Scenes';E=T/'Evidence';sys.path.insert(0,str(HERE))
from build_sensing_v001 import animate_event,save,snapshot,dump
from acoustic_binding_v001 import make_controls
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(S/f'Sensing_reuse_{kind}_v001.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
 before=snapshot()
 resolved=[(l,Path(bpy.path.abspath(l.filepath)).resolve()) for l in bpy.data.libraries]
 for l,p in resolved:l.filepath=str(p)
 for l in list(bpy.data.libraries):
  if Path(l.filepath).name=='Acoustics_v001.blend':l.filepath=str(ROOT/'04-Production/Shared/Assets/Acoustics/Acoustics_v002.blend');l.reload()
 events=json.loads((E/f'events_{kind}_v001.json').read_text())['events'];col=bpy.data.collections['LOCAL_ACOUSTIC_EVENTS']
 for e in events:
  obs={o['shared_prototype']:o for o in col.objects if o.name.startswith(e['event_id'])}
  animate_event(e,obs,s.frame_end,24,None);make_controls(e,obs,col,s.frame_end)
 s.frame_set(20);after=snapshot();assert before==after
 save(S/f'Sensing_reuse_{kind}_v004.blend');dump(E/f'migration_{kind}_v004.json',dict(before=before,after=after,preserved=before==after,repairs='v002/v003 retained failed relocation evidence. Fresh v001 input, capture all absolute library paths before reload/remap. Endpoint taper and native opacity/visibility controls added.'))
