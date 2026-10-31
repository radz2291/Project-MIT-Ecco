"""Read-only native source/morphology inspection for T48. No rendering."""
import bpy, math, json, hashlib, struct
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[5]
ASSET=ROOT/'04-Production/Shared/Assets'
E=ROOT/'04-Production/Records/Tasks/T-048/Evidence'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(name,d): (E/name).write_text(json.dumps(d,indent=2),encoding='utf-8')
records=[]
for rel in ['ECCO/ECCO_film_v002.blend','BHA/BHA_film_v006.blend','WellAssembly/World_environment_v009.blend']:
 p=ASSET/rel;bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 d=dict(path=str(p.relative_to(ROOT)).replace('\\','/'),sha256=sha(p),collections=list(bpy.data.collections.keys()),objects=[])
 for o in bpy.data.objects:
  q=dict(name=o.name,type=o.type,location=list(o.location),rotation=list(o.rotation_euler),dimensions=list(o.dimensions),library=o.library.filepath if o.library else None)
  if o.type=='MESH':
   pts=[o.matrix_world@v.co for v in o.data.vertices]
   q.update(vertices=len(pts),bounds=[[min(v[i] for v in pts),max(v[i] for v in pts)] for i in range(3)],axis_max_radius=max(math.hypot(v.y,v.z) for v in pts))
  d['objects'].append(q)
 if rel.startswith('ECCO/'):
  o=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];bv=BVHTree.FromPolygons([o.matrix_world@v.co for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons],all_triangles=False)
  rows=[]
  for i in range(241):
   x=i*.01;r=[]
   for j in range(72):
    a=j*math.tau/72;u=Vector((0,math.cos(a),math.sin(a)))
    hit=bv.ray_cast(Vector((x,0,0))+u*.2,-u,.2)
    if hit[0] is not None:r.append(math.hypot(hit[0].y,hit[0].z))
   rows.append(dict(x_m=x,min_radius_m=min(r) if r else None,max_radius_m=max(r) if r else None,intersections=len(r)))
  dump('native-radial-profile_v001.json',dict(method='Outer ray intersections every10mm X /5deg azimuth; no function identification from geometry alone',rows=rows))
 records.append(d)
dump('native-source-inspection_v001.json',records)
print('T48_READ_ONLY_INSPECTION_SAVED')
