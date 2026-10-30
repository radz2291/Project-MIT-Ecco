import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';world=R/'04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend'
bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S06_shared-digital_v002.blend'),load_ui=False);s=bpy.context.scene;s.frame_set(52);o=bpy.data.objects['S06 | physical World live context'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());verts=[v.co for v in ev.data.vertices];out={'candidate_faces':len(ev.data.polygons),'candidate_bounds':[[min(v[i] for v in verts),max(v[i] for v in verts)] for i in range(3)],'materials':[]}
for m in ev.data.materials:
 if not m:continue
 out['materials'].append({'name':m.name,'nodes':[{'name':n.name,'type':n.type,'inputs':{x.name:float(x.default_value) for x in n.inputs if hasattr(x,'default_value') and isinstance(x.default_value,(int,float))}} for n in m.node_tree.nodes if n.type in ['MIX_SHADER','BSDF_PRINCIPLED','VALUE','GROUP']]})
with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_FORMATION_IRREGULAR_CUTAWAY']
src=next(o for o in b.collections[0].objects if o.type=='MESH');v=[src.matrix_world@x.co for x in src.data.vertices];out['cutaway']={'name':src.name,'bounds':[[min(x[i] for x in v),max(x[i] for x in v)] for i in range(3)],'polygons':len(src.data.polygons),'planar_caps_by_axis':{str(i):sum(1 for p in src.data.polygons if abs(p.normal[i])>.999) for i in range(3)}}
(T/'Evidence/context-diagnosis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
