"""Actual finite continuation rim visibility over every saved consumer frame."""
import bpy,json,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-046'
version=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'v009';rows=[]
for kind in ['A','B']:
 actual='v009' if kind=='A' else version
 bpy.ops.wm.open_mainfile(filepath=str(T/f'Scenes/Sensing_reuse_{kind}_{actual}.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;cache={};results=[];unblocked=[];sample_count=0;projected=0
 for f in range(1,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();opaque=[];ext=None
  for i in deps.object_instances:
   o=i.object.original;m=i.matrix_world.copy()
   if o.type!='MESH' or o.hide_render or not o.library or o.name.startswith('MUD_'):continue
   if o.name=='UPHOLE_UNIT_COLLAR_EXTENSION':ext=(o,m)
   key=o.as_pointer()
   if key not in cache:
    ev=i.object;me=ev.to_mesh();cache[key]=BVHTree.FromPolygons([v.co.copy() for v in me.vertices],[list(p.vertices) for p in me.polygons]);ev.to_mesh_clear()
   opaque.append((o.name,m,m.inverted(),cache[key]))
  assert ext is not None;ob,m=ext;xmin=min(v.co.x for v in ob.data.vertices);points=[v.co.copy() for v in ob.data.vertices if abs(v.co.x-xmin)<1e-6]
  points += [p.center.copy() for p in ob.data.polygons if all(abs(ob.data.vertices[i].co.x-xmin)<1e-6 for i in p.vertices)]
  camera=s.camera.matrix_world.translation;local_visible=0;local_unblocked=0
  for p in points:
   sample_count+=1;point=m@p;uv=world_to_camera_view(s,s.camera,point)
   if not (0<=uv.x<=1 and 0<=uv.y<=1 and s.camera.data.clip_start<uv.z<s.camera.data.clip_end):continue
   projected+=1;local_visible+=1;delta=point-camera;blocked=False;closest=None
   for name,om,inv,tree in opaque:
    a=inv@camera;b=inv@point;d=b-a
    if d.length<1e-9:continue
    hit,n,face,dist=tree.ray_cast(a,d.normalized(),d.length)
    if hit is not None:
     world=om@hit;distance=(world-camera).length
     if distance<delta.length-.0001:blocked=True;closest=dict(object=name,margin_m=delta.length-distance);break
   if not blocked:unblocked.append(dict(frame=f,point_world=list(point),uv=list(uv)));local_unblocked+=1
  results.append(dict(frame=f,projected=local_visible,unoccluded=local_unblocked))
  if local_unblocked:break
 row=dict(kind=kind,scene=f'Scenes/Sensing_reuse_{kind}_{actual}.blend',rim_vertex_facecentre_samples=sample_count,projected=projected,unoccluded=len(unblocked),all_outside_or_opaque_occluded=not unblocked,unoccluded_examples=unblocked[:25],frames=results,method='All finite far-rim vertices/end-facecentres, every saved frame unless failed frame found. Camera clipping plus actual evaluated opaque mesh BVH ray occlusion; static local mesh caches, current rigid matrices.')
 rows.append(row);print('SENSING_RIM',kind,projected,len(unblocked),flush=True)
(T/f'Evidence/extension-visibility_{version}.json').write_text(json.dumps(rows,indent=2))
