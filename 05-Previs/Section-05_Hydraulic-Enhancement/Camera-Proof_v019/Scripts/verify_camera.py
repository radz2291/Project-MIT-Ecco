import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;cam=s.camera
ns={'__file__':str(B/'Scripts/camera_study.py'),'MODE':'functions'};exec(compile((B/'Scripts/camera_study.py').read_text(),ns['__file__'],'exec'),ns)
baseline=json.loads((B/'Records/source-baseline.json').read_text());content=json.loads((B/'Records/content-preservation.json').read_text())
assert content['equal'],content['differences']
assert hashlib.sha256(Path(baseline['source']).read_bytes()).hexdigest()==baseline['source_sha256']
s.frame_set(151);bpy.context.view_layer.update()
def bvh(objects):
 vs=[];fs=[]
 for o in objects:
  n=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend([[n+i for i in p.vertices] for p in o.data.polygons])
 return BVHTree.FromPolygons(vs,fs)
steel=bvh(bpy.data.collections['S05_LINKED_HARDWARE'].objects);wall=bvh([bpy.data.objects['S05_FixedHalfBorehole']])
rows=json.loads((B/'Records/camera-transforms.json').read_text());bad=[];margins=[];up=[];steps=[];angles=[];rockviews=[];prev=None
root=bpy.data.objects['S05_COMMON_AXIAL_ROTATION']
rocks=[o for o in s.objects if o.name.startswith('S05_v018_Cutting_0_')]
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update();origin=cam.matrix_world.translation;target=Vector(rows[f-1]['target']);direction=(target-origin).normalized()
 inv=Matrix.Rotation(-root.rotation_euler.z,4,'Z');steelhit=steel.ray_cast(inv@origin,inv.to_3x3()@direction,20);wallhit=wall.ray_cast(origin,direction,20)
 if wallhit[0] and (not steelhit[0] or wallhit[3]<steelhit[3]-.0001):bad.append({'frame':f,'issue':'wall occludes main axis target'})
 clearance=min(steel.find_nearest(inv@origin)[3],wall.find_nearest(origin)[3]);margins.append(clearance)
 if clearance<cam.data.clip_start+.01:bad.append({'frame':f,'issue':'camera near clipping solid'})
 a=world_to_camera_view(s,cam,target);b=world_to_camera_view(s,cam,target+Vector((0,0,.02)));up.append(b.y-a.y)
 if b.y<=a.y:bad.append({'frame':f,'issue':'screen flow direction inverted'})
 if prev and f!=121:
  steps.append((origin-prev[0]).length);angles.append(cam.rotation_quaternion.rotation_difference(prev[1]).angle)
 prev=(origin.copy(),cam.rotation_quaternion.copy())
 if 165<=f<=246:
  visible=0
  for rock in rocks:
   p=rock.matrix_world.translation;ray=(p-origin);dist=ray.length;direc=ray.normalized();h=steel.ray_cast(inv@origin,inv.to_3x3()@direc,dist);w=wall.ray_cast(origin,direc,dist);ndc=world_to_camera_view(s,cam,p)
   if 0<=ndc.x<=1 and 0<=ndc.y<=1 and (not h[0] or h[3]>=dist-.012) and (not w[0] or w[3]>=dist-.012):visible+=1
  rockviews.append({'frame':f,'visible_core_fragments':visible})
record={'source_unchanged':True,'noncamera_content_matches':True,'items_compared':content['items_compared'],'camera_samples':432,'failures':bad,'min_camera_solid_distance_m':min(margins),'upward_flow_screen_direction_all_frames':min(up)>0,'largest_noncut_position_step_m':max(steps),'largest_noncut_orientation_step_deg':math.degrees(max(angles)),'intentional_cut':121,'core_observation_frames_with_at_least_one_visible_rock':sum(r['visible_core_fragments']>0 for r in rockviews),'core_observation_frame_count':len(rockviews),'rock_visibility':rockviews,'inherited_geometry_clearance_record':'../Full-Previs_v018/Records/geometry-verification.json and supply-geometry-verification.json; unchanged mesh and animation content preserves existing sampled evidence','limits':'Camera target ray is not a guarantee that every edge of every object is visible. Physical stage mapping remains illustrative, not certified.'}
(B/'Records/camera-verification.json').write_text(json.dumps(record,indent=2));assert not bad,bad[:5]
s.frame_set(205)
result={k:v for k,v in record.items() if k!='rock_visibility'}
