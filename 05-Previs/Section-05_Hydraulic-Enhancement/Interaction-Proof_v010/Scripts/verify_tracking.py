import bpy,math,json
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in list(bpy.data.collections['S05_LINKED_HARDWARE'].objects):
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vv,ff);rocks=list(bpy.data.collections['S05_TRACKED_COHORT_v010'].objects);previous={};bounds=[1,1,0,0];occlusions=[];pair_hits=[];max_step=0;min_up=1
for f in [1+i*.5 for i in range(191)]:
 s.frame_set(int(f),subframe=f-int(f));bpy.context.view_layer.update();inv=Matrix.Rotation(math.radians(5)*(f-1)/24,4,'Z');cam=inv@s.camera.matrix_world.translation;trees=[]
 for o in rocks:
  assert not o.hide_render and not o.hide_viewport and o.parent is None
  assert max(abs(q-1) for q in o.scale)<1e-7
  point=o.matrix_world.translation;local=inv@point;ray=local-cam;hit=steel.ray_cast(cam,ray.normalized(),ray.length)[0]
  if hit is not None:occlusions.append([f,o.name])
  if o.name in previous:
   delta=point-previous[o.name];min_up=min(min_up,delta.z);max_step=max(max_step,delta.length)
  previous[o.name]=point.copy();verts=[o.matrix_world@v.co for v in o.data.vertices]
  for v in verts:
   q=world_to_camera_view(s,s.camera,v);assert q.z>0;bounds=[min(bounds[0],q.x),min(bounds[1],q.y),max(bounds[2],q.x),max(bounds[3],q.y)]
  trees.append(BVHTree.FromPolygons(verts,[list(p.vertices) for p in o.data.polygons]))
 for i in range(3):
  for j in range(i+1,3):
   if trees[i].overlap(trees[j]):pair_hits.append([f,i,j])
assert not occlusions and not pair_hits,(occlusions,pair_hits)
assert min_up>0 and max_step<.015 and min(bounds[:2])>.05 and max(bounds[2:])<.95
result={'persistent_objects':[o.name for o in rocks],'time_samples':191,'steel_occluded_centers':occlusions,'fragment_pair_intersections':pair_hits,'screen_bounds_all_vertices':bounds,'minimum_upward_half_frame_step_m':min_up,'maximum_half_frame_displacement_m':max_step,'no_hide_scale_parenting_or_respawn':True,'limit':'Center-ray visibility against steel and frame coverage, not a perceptual comprehension test.'}
# Screen-space deflection from straight axial travel, measured without overlays.
s.frame_set(1);p0=Vector((0,0,.2));q0=world_to_camera_view(s,s.camera,p0);q1=world_to_camera_view(s,s.camera,p0+Vector((0,0,.2)));axis=Vector(((q1.x-q0.x)*1280,(q1.y-q0.y)*720));axis.normalize();side=Vector((-axis.y,axis.x));xy=[];angles=[];world=[]
for f in range(1,97):
 s.frame_set(f);bpy.context.view_layer.update();p=rocks[1].matrix_world.translation;world.append(p.copy());angles.append(math.degrees(math.atan2(p.y,p.x)));q=world_to_camera_view(s,s.camera,p);xy.append(Vector((q.x*1280,q.y*720)))
lateral=[q.dot(side) for q in xy];chord=xy[-1]-xy[0];normal=Vector((-chord.y,chord.x)).normalized();bend=max(abs((q-xy[0]).dot(normal)) for q in xy)
result['screen_lateral_span_pixels']=max(lateral)-min(lateral);result['screen_bend_from_endpoint_chord_pixels']=bend;result['angular_range_degrees']=[min(angles),max(angles)];result['frames']=96
(B/'Records/tracking-verification.json').write_text(json.dumps(result,indent=2));s.frame_set(36)
