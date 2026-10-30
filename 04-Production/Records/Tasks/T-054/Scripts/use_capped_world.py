import bpy,json
from pathlib import Path
from mathutils import Matrix
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';world=R/'04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend';records=[]
M=Matrix(((0,0,-1),(0,1,0),(1,0,0)))
for sid in ['S03','S06']:
 path=T/'Consumers'/f'{sid}_shared-digital_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
 with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_FORMATION_IRREGULAR_CUTAWAY']
 src=next(o for o in b.collections[0].objects if o.type=='MESH');ob=bpy.data.objects[sid+' | physical World live context'];g=ob.modifiers[0].node_group
 oi=next(n for n in g.nodes if n.bl_idname=='GeometryNodeObjectInfo');oi.inputs['Object'].default_value=src
 tr=next(n for n in g.nodes if n.bl_idname=='GeometryNodeTransform');tr.inputs['Rotation'].default_value=M.to_euler()
 delete=next(n for n in g.nodes if n.bl_idname=='GeometryNodeDeleteGeometry');g.links.new(g.nodes['Math.002'].outputs[0],delete.inputs['Selection'])
 ob['placement']='Canonical X→local Z,Y→local Y,Z→negative local X; no scaling. Existing source cutaway cap is preserved. Only axial window applied.'
 s=bpy.context.scene;s.frame_set(52 if sid=='S06' else 1);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());v=[x.co for x in ev.data.vertices]
 records.append({'section':sid,'collection':'WORLD_FORMATION_IRREGULAR_CUTAWAY','mapping':[list(r) for r in M],'face_count':len(ev.data.polygons),'bounds':[[min(x[i] for x in v),max(x[i] for x in v)] for i in range(3)],'material_polygon_counts':{str(i):sum(p.material_index==i for p in ev.data.polygons) for i in range(len(ev.data.materials))}})
 bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(path))
(T/'Evidence/capped-world-placement.json').write_text(json.dumps(records,indent=2));print('CAPPED_WORLD_DONE')
