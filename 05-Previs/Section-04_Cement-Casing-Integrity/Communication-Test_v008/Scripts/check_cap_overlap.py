import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_C_capped-resonance_v008.blend'),use_scripts=False,load_ui=False)
d=Vector((0,math.cos(math.radians(39)),math.sin(math.radians(39))));t=Vector((0,-d.z,d.y));point=Vector((-1.5,0,0))+d*.195+t*.00005;eye=bpy.context.scene.camera.location;ray=(point-eye).normalized();rows=[]
for o in bpy.context.scene.objects:
 if o.type=='MESH' and not o.hide_render and (o.name.startswith('Cement ') or 'Stationary organic fluid' in o.name):
  vs=[o.matrix_world@v.co for v in o.data.vertices];tree=BVHTree.FromPolygons(vs,[tuple(p.vertices) for p in o.data.polygons]);hit,normal,face,dist=tree.ray_cast(eye,ray,1)
  rows.append(dict(object=o.name,hit=list(hit) if hit else None,distance=dist,error_to_channel_point=(hit-point).length if hit else None))
(B/'Records/cap-overlap.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
