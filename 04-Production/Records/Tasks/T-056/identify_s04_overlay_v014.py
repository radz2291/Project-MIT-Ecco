import bpy,json,pathlib
T=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-056');s=bpy.context.scene;s.frame_set(95);rows=[]
for o in s.objects:
 if o.hide_render or o.type not in ['MESH','CURVE']:continue
 if not(-.4<o.matrix_world.translation.x<-.2):continue
 mats=[(m.name,list(m.diffuse_color)) for m in o.data.materials if m]
 if any(c[2]>c[0]*1.2 for _,c in mats):rows.append({'object':o.name,'materials':mats,'location':list(o.matrix_world.translation),'collections':[(c.name,c.hide_render) for c in o.users_collection]})
(T/'s04-frame95-source-overlays_v014.json').write_text(json.dumps(rows,indent=2));print('CYAN_OBJECTS',json.dumps(rows))
