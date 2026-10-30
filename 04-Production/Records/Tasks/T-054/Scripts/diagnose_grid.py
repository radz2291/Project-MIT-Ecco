import bpy,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S03_shared-digital_v002.blend'),load_ui=False);bpy.context.scene.frame_set(1);dep=bpy.context.evaluated_depsgraph_get();target=bpy.data.objects['S03 | physical World live context'];tree=BVHTree.FromObject(target,dep);out=[]
for name in ['Luminous geological strata','Subordinate formation survey grid','HUD - actual S02 soil section contours']:
 o=bpy.data.objects[name];ev=o.evaluated_get(dep);me=ev.to_mesh();samples=[]
 for spline in o.data.splines:
  ps=[Vector(p.co[:3]) for p in spline.points]
  for a,b in zip(ps,ps[1:]):
   for t in [0,.25,.5,.75,1]:
    p=o.matrix_world@(a.lerp(b,t));hit=tree.ray_cast(Vector((p.x,-.7,p.z)),Vector((0,1,0)),50);samples.append(bool(hit[0]))
 out.append({'name':name,'hidden':o.hide_render,'mesh_vertices':len(me.vertices),'mesh_polygons':len(me.polygons),'raw_splines':len(o.data.splines),'tested_rays':len(samples),'hits':sum(samples),'material_factors':[{n.name:[x.default_value for x in n.inputs if hasattr(x,'default_value') and isinstance(x.default_value,(float,int))] for n in m.node_tree.nodes if n.type=='MIX_SHADER'} for m in o.data.materials if m and m.node_tree]});ev.to_mesh_clear()
(T/'Evidence/grid-diagnosis.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
