"""Check saved native controls without modifying the production file."""
import bpy,json,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
p=Q/'Scenes/S01-S02_production_v025.blend';bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False)
ob=bpy.data.objects['Shared fine measurement display'];g=next(n.node_tree for n in ob.modifiers[0].node_group.nodes if n.type=='GROUP');rows=[]
for prop,value,expected in [('Contour rings enabled',False,0),('Contour delay frames',3,3),('Contour build frames',5,5)]:
 original=ob[prop];ob[prop]=value;ob.update_tag();bpy.context.scene.frame_set(620);bpy.context.view_layer.update()
 n=next(n for n in g.nodes if n.label==prop);actual=n.outputs[0].default_value;assert abs(actual-expected)<.0001,(prop,actual)
 rows.append({'property':prop,'test_value':value,'driven_value':actual});ob[prop]=original;ob.update_tag();bpy.context.scene.frame_set(756)
record={'cold_reopen':True,'scene_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'native_control_tests':rows,'source_file_modified':False}
(Q/'Notes/refinements_v025_controls.json').write_text(json.dumps(record,indent=2));print(json.dumps(record))
