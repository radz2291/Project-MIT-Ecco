import bpy,json,sys,time,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import get_input,set_input,arrival_readouts
out=Q/'Scenes/S01-S02_production_v014.blend';assert not out.exists()
assert 'v013' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Session_before_v014_{int(time.time())}.blend'),copy=True,compress=True)
with bpy.data.libraries.load(str(R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v019.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,template=b.objects;bpy.context.scene.collection.objects.link(ctrl);rows=[]
for i in range(1,7):
 o=bpy.data.objects[f'WF sequence event {i}'];m=o.modifiers[0];before={}
 for x in m.node_group.interface.items_tree:
  if getattr(x,'in_out','')!='INPUT' or x.socket_type=='NodeSocketGeometry':continue
  v=get_input(m,x.name);before[x.name]=tuple(v) if x.socket_type in ['NodeSocketVector','NodeSocketColor'] else v
 o.data=template.data;m.node_group=template.modifiers[0].node_group
 for k,v in before.items():set_input(m,k,v)
 for k,v in {'Beam mode':True,'Beam opening frames':1.,'Beam setup frames':3.,'Beam closing frames':1.,'Lead rest frames':0.,'Tail allowance':10.,'Show markers':False}.items():set_input(m,k,v)
 start=get_input(m,'Start frame');bpy.context.scene.frame_set(int(start+10));read=arrival_readouts(o)
 wall=bpy.data.objects['ONE WALL - old history and current cells share topology']
 for p in wall.data.polygons:
  if wall.data.materials[p.material_index].name.startswith('Unified cell '+str(i)+' ') or wall.data.materials[p.material_index].name=='Unified cell '+str(i):wall.data.attributes['ecco_receipt_frame'].data[p.index].value=start+11
 rows.append({'event':i,'beam_start':start,'fully_connected':start+1,'pulse_launch':start+3,'tile_impact':start+11,'feedback_launch':start+21,'feedback_pulse_arrival':start+29,'exchange_complete':start+37,'beam_closed':start+38,'tool_moves':start+42,'readouts':read})
bpy.context.scene.frame_set(312);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/waveform_v014_install.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'events':rows,'color':'cyan outgoing/handshake; violet return; continuous beam changes color at return launch','camera_BHA':'retainedv013, holds until after closure','shared':'v019 optional Beam mode, default false preserves previous mode'},indent=2));result={'saved':str(out),'first':rows[0]}
