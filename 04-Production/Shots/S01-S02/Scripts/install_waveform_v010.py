"""Bind approved v017 to all six actual shot events, retaining completed-tail cues."""
import bpy,json,sys,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input,arrival_readouts
target=Q/'Scenes/S01-S02_production_v010.blend';assert not target.exists()
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v007.blend'))
s=bpy.context.scene
def camera():
 out=[]
 for f in range(1,529):s.frame_set(f);out.append([list(row) for row in s.camera.matrix_world]+[[s.camera.data.lens]])
 return out
baseline=camera();wall=bpy.data.objects['ONE WALL - old history and current cells share topology']
def wallhash(f):
 s.frame_set(f);e=wall.evaluated_get(bpy.context.evaluated_depsgraph_get());m=e.to_mesh();v=hashlib.sha256(str(([tuple(v.co) for v in m.vertices],[p.material_index for p in m.polygons])).encode()).hexdigest();e.to_mesh_clear();return v
samples=[299,309,318,360,402,450,498,524];before={f:wallhash(f) for f in samples}
with bpy.data.libraries.load(str(R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v017.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,template=b.objects;s.collection.objects.link(ctrl);events=json.loads((Q/'Notes/integration_v002.json').read_text())['events'];checks=[]
for event in events:
 o=bpy.data.objects[event['object']];o.data=template.data;o.modifiers.clear();m=o.modifiers.new('Approved v017 — shot event controls','NODES');m.node_group=template.modifiers[0].node_group
 # Three-frame complete train, matching original local packet duration. Preserve
 # old contact/receipt as TAIL completion, rather than cutting the train at its head.
 duration=min(3.,(event['contact']-event['start'])/2,(event['receipt']-event['echo_start'])/2);speed=20/duration
 p={'Start frame':float(event['start']),'Follow scene FPS':False,'Speed':speed,'Loop':False,'Travel frames':(event['contact']-event['start']-duration)*speed,'Return travel override':(event['receipt']-event['echo_start']-duration)*speed,'Reflection delay':(event['echo_start']-event['contact'])*speed,'Gap length m':event['settings']['Gap Length m'],'Route axis':event['settings']['Route Axis'],'Transverse axis':event['settings']['Transverse Axis'],'Up axis':event['settings']['Up Axis']}
 for n,v in p.items():set_input(m,n,v)
 s.frame_set(event['start']+2);read=arrival_readouts(o)
 for key,want in [('Send tail arrival',event['contact']),('Return start',event['echo_start']),('Return tail arrival',event['receipt'])]:assert abs(read[key]-want)<.001,(event['event'],key,read)
 for f,active in [(event['start']-1,False),(event['start']+2,True),(event['echo_start']+2,True),(event['receipt']+1,False)]:
  s.frame_set(f);e=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=e.to_mesh();n=len(me.vertices);e.to_mesh_clear();assert bool(n)==active,(event['event'],f,n)
 checks.append({'event':event['event'],'settings':p,'landmarks':read});o['waveform_version']='approved sharedv017, all pulse tails complete before measurement cue'
assert camera()==baseline,'camera changed'
assert all(wallhash(f)==before[f] for f in samples),'measurement geometry changed'
s.frame_set(305);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(target));assert all(Path(bpy.path.abspath(x.filepath)).exists() for x in bpy.data.libraries)
(Q/'Notes/waveform_v010_install.json').write_text(json.dumps({'scene':str(target),'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'events':checks,'camera_all528':'exact evaluated equality to v007','measurement_sample_hashes':before,'fresh_reopen_links':'all resolve','master':'linked v017; unchanged defaults','timing':'3-frame train; outgoing and reflected TAIL completion retain contact and receipt cues; head reaches earlier; camera not retimed'},indent=2))
print('V010_INSTALLED')
