import bpy,math,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B.parent/'Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'),use_scripts=False,load_ui=False)
o=bpy.data.objects['Section 2 geological surroundings - outside cement'];vs=[o.matrix_world@v.co for v in o.data.vertices];tree=BVHTree.FromPolygons(vs,[tuple(p.vertices) for p in o.data.polygons]);rows=[]
for x in [-2,-1.5,-1,-.32,0]:
 for a in [0,.2,.68,1,2,3,4,5]:
  d=Vector((0,math.cos(a),math.sin(a)));hit=tree.ray_cast(Vector((x,0,0)),d,2)[0];rows.append({'x':x,'a':a,'r':math.hypot(hit.y,hit.z) if hit else None})
(B/'Records/formation-source.json').write_text(json.dumps({'vertices':len(vs),'faces':len(o.data.polygons),'bounds':[[min(v[i] for v in vs),max(v[i] for v in vs)] for i in range(3)],'rays':rows,'properties':dict(o.items())},indent=2));print(json.dumps(rows))
