"""Owner-requested exact demo timing trial; no old-window compression."""
import bpy,json,sys,time,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input,arrival_readouts
target=Q/'Scenes/S01-S02_production_v011.blend';assert not target.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Session_before_v011_{int(time.time())}.blend'),copy=True,compress=True)
if Path(bpy.data.filepath).name!='S01-S02_production_v010.blend':bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v010.blend'))
manifest=json.loads((R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_interface_v017.json').read_text());events=json.loads((Q/'Notes/integration_v002.json').read_text())['events'];checks=[]
for event in events:
 o=bpy.data.objects[event['object']];m=o.modifiers[0]
 for k,v in manifest['timing'].items():set_input(m,k,v)
 set_input(m,'Start frame',float(event['start']))
 for k,v in {'Use master style':True,'Pulse count override':0,'Strand count override':0,'Strand separation override':-1.,'Strength multiplier':1.,'Width multiplier':1.,'Radius multiplier':1.,'Show markers':True}.items():set_input(m,k,v)
 bpy.context.scene.frame_set(event['start']+13);read=arrival_readouts(o)
 assert abs(read['Send head arrival']-(event['start']+16))<.001
 assert abs(read['Return tail arrival']-(event['start']+74))<.001
 checks.append({'event':event['event'],'start':event['start'],'landmarks':read})
 o['waveform_version']='v017 exact approved demo timing; only start/placement adapted'
bpy.context.scene.frame_set(313);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
(Q/'Notes/waveform_v011_install.json').write_text(json.dumps({'scene':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'events':checks,'configuration':'exact v017 approved demo timing including Speed1,Travel16,Train20,Delay2,Loop96; only scene start/placement differ','measurement':'old reveal cues retained for this visual trial; no longer synchronized with longer return. Needs timing decision after waveform review.','camera':'unchanged from v010'},indent=2))
result={'saved':str(target),'event1':checks[0]}
