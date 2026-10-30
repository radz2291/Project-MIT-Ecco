import bpy,json,hashlib,pathlib
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');s=bpy.context.scene;o=bpy.data.objects['RIBBON_FIXED_32_FILAMENTS'];mat=o.data.materials[0];records=[]
for f in [298,300,305,309,314,318,324]:
 s.frame_set(f);bpy.context.view_layer.update();geo={'matrix':[list(r) for r in o.matrix_world],'vertices':[list(v.co) for v in o.data.vertices]};records.append({'frame':f,'geometry_sha256':hashlib.sha256(json.dumps(geo).encode()).hexdigest(),'head':mat.node_tree.nodes['Traveling light position only'].outputs[0].default_value,'gain':mat.node_tree.nodes['Outbound then weaker return'].outputs[0].default_value})
result={'records':records,'fixed_geometry_pass':len(set(r['geometry_sha256'] for r in records))==1,'moving_light_pass':len(set(r['head'] for r in records))>1,'camera':s.camera.name,'object_action':bool(o.animation_data),'mesh_action':bool(o.data.animation_data)};(T/'ribbon-invariance_v010.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

import os
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
s.frame_set(305);bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
