import bpy,sys,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-046';bpy.ops.wm.open_mainfile(filepath=str(T/'Scenes/Sensing_reuse_A_v005.blend'),load_ui=False,use_scripts=False)
bpy.context.scene.frame_set(17);deps=bpy.context.evaluated_depsgraph_get();trees=[]
for i in deps.object_instances:
 o=i.object.original;m=i.matrix_world.copy()
 if o.type=='MESH' and o.library and 'ECCO' in o.library.filepath and not o.hide_render:
  trees.append((o.name,BVHTree.FromPolygons([m@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])))
e=json.loads((T/'Evidence/events_A_v001.json').read_text())['events'][0];src=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);x=Vector((1,0,0))
candidates=[('v005',bpy.context.scene.camera.location.copy())]
for dx in [-.15,-.10,-.07,.07,.10,.15]:
 for dr in [.008,.012,.017]:candidates.append((f'inside_{dx}_{dr}',src+x*dx+d*dr))
for dx in [-.03,-.02,0,.02,.03]:
 for dr in [.008,.014,.020]:candidates.append((f'near_{dx}_{dr}',src+x*dx+d*dr))
rows=[]
for name,cam in candidates:
 out=[]
 for key,target in [('emitter',src),('contact',hit)]:
  delta=target-cam;hits=[]
  for ob,tree in trees:
   p,normal,face,dist=tree.ray_cast(cam,delta.normalized(),delta.length)
   if p is not None:hits.append((ob,dist,delta.length-dist))
  out.append(dict(target=key,distance=delta.length,occluders=sorted(hits,key=lambda p:p[1])[:3]))
 rows.append(dict(name=name,camera=list(cam),targets=out))
(T/'Evidence/sightlines_v001.json').write_text(json.dumps(rows,indent=2))
print('CLEAR_OR_NEAR',json.dumps([r for r in rows if r['targets'][0]['occluders']==[] or r['name'].startswith('near')]))
for n,tree in trees:
 if 'Imaging port 1' in n:
  print('CAP_RADIAL_RAY',n,tree.ray_cast(src+d*.025,-d,.05))
