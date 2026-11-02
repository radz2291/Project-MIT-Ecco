"""Single outgoing/reflected pulse with a broader lead-in and longer tail."""
import bpy,json,sys,time,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input,arrival_readouts
target=Q/'Scenes/S01-S02_production_v012.blend';assert not target.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Session_before_v012_{int(time.time())}.blend'),copy=True,compress=True)
assert Path(bpy.data.filepath).name=='S01-S02_production_v011.blend'
settings={'Use master style':False,'Pulse count override':1,'Pulse count':1,'Pulse width':1.6,'Tail allowance':12.,'Head fade':1.2,'Tail fade':2.4,'Loop':False}
checks=[]
for i in range(1,7):
 o=bpy.data.objects[f'WF sequence event {i}'];m=o.modifiers[0]
 for k,v in settings.items():set_input(m,k,v)
 start=next(x for x in m.node_group.interface.items_tree if x.name=='Start frame');f=getattr(m.properties.inputs,start.identifier).value;bpy.context.scene.frame_set(round(f+10));checks.append({'event':i,'landmarks':arrival_readouts(o)})
 o['waveform_version']='v012 single send/reflection, wider lead-in and extended tail; shared master unchanged'
bpy.context.scene.frame_set(310);bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
(Q/'Notes/waveform_v012_install.json').write_text(json.dumps({'scene':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'settings':settings,'events':checks,'shared_master':'v017 unchanged; instance style copies start at approved defaults','camera_and_measurement':'unchanged from v011; old cues pending synchronization','semantics':'one pulse each direction per event; no looping, one spike retains pre-dip/undershoot/rebound/ringing; width1.6 lengthens approach and response, train12 extends trailing baseline'},indent=2))
result={'saved':str(target),'settings':settings,'first':checks[0]}
