"""One-event sharedv016 candidate proof; other five events remain pinnedv015."""
import bpy,json
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';target=Q/'Scenes/S01-S02_production_v009.blend';assert not target.exists()
with bpy.data.libraries.load(str(R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v016.blend'),link=True) as (a,b):b.node_groups=['WF_FIELD_LIVE_v016'];b.meshes=['WF_PARAMETER_DOMAIN']
ob=bpy.data.objects['WF sequence event 1'];mod=ob.modifiers['Shared waveform; local event binding'];before={}
for x in mod.node_group.interface.items_tree:
 if getattr(x,'in_out','')!='INPUT' or x.socket_type=='NodeSocketGeometry':continue
 v=getattr(mod.properties.inputs,x.identifier).value;before[x.name]=list(v) if x.socket_type in ['NodeSocketVector','NodeSocketColor'] else v
mod.node_group=b.node_groups[0];ob.data=b.meshes[0]
changes={'Motion Preset 0 Organic 1 Short':1,'Contact Frame':309.,'Receipt Frame':318.,'Radius Override':1.}
for x in mod.node_group.interface.items_tree:
 if getattr(x,'in_out','')=='INPUT' and x.socket_type!='NodeSocketGeometry' and x.name in {**before,**changes}:
  getattr(mod.properties.inputs,x.identifier).value=changes.get(x.name,before.get(x.name))
ob['waveform_trial']='v016 Short Event candidate; only event1 upgraded; camera, event landmarks and reveal unchanged.'
ob.update_tag(refresh={'OBJECT','DATA','TIME'});bpy.context.view_layer.update();bpy.context.scene.frame_set(312)
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(target),compress=True)
(Q/'Notes/waveform_v009_install.json').write_text(json.dumps({'scene':str(target),'object':ob.name,'before':before,'changes':changes,'other_events':'2–6 remain v015','camera':'original v007 action unchanged'},indent=2))
result={'saved':str(target),'event1_group':mod.node_group.name,'changes':changes}
