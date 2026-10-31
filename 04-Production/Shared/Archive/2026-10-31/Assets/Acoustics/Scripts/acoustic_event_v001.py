"""Native event adapter. Timing is illustrative; no calibrated acoustics.

Call from Blender after placing linked hardware/wall instances and updating the
depsgraph. The sampled emitter and contact are immutable world-space records.
"""
import bpy,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree

def native_instance(name):
 matches=[(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.original.name==name]
 if len(matches)!=1:raise ValueError(f'Expected exactly one {name}, got {len(matches)}')
 return matches[0]

def wall_tree(name):
 o,m=native_instance(name)
 if o.type!='MESH':raise TypeError(name+' must be mesh')
 return o,m,BVHTree.FromPolygons([m@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])

def sample_native_event(sensor_ref,wall_object_name,event_id,send_s,contact_s,receive_s,patch_lifetime_s=.65,emitter_surface_name=None):
 if not send_s<contact_s<receive_s:raise ValueError('Expected send < contact < receive')
 bpy.context.view_layer.update()
 sensor,pose=native_instance(sensor_ref);wall,wall_pose,tree=wall_tree(wall_object_name)
 reference=pose.translation.copy();origin=reference.copy();direction=(pose.to_3x3()@Vector((0,0,1))).normalized();surface=None
 # The retained temporary imaging cap is 2mm proud of the inherited reference.
 # Derive the visible face from native geometry, never move/source-edit the ref.
 capname=emitter_surface_name or f'TEMP | Imaging port {int(sensor_ref[-2:])} | removable acoustic cap'
 capmatches=[(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.original.name==capname]
 if len(capmatches)==1:
  cap,cp=capmatches[0];ct=BVHTree.FromPolygons([cp@v.co for v in cap.data.vertices],[list(p.vertices) for p in cap.data.polygons])
  facehit,fn,fi,fd=ct.ray_cast(reference+direction*.025,-direction,.05)
  if facehit is None:raise ValueError('Visible emitter surface not found')
  offset=(facehit-reference).dot(direction)
  if not 0<=offset<.025:raise ValueError('Emitter surface lies outside bounded reference search')
  origin=facehit;sl=Path(bpy.path.abspath(cap.library.filepath)).resolve() if cap.library else Path(bpy.data.filepath)
  surface=dict(object=cap.name,library=sl.as_posix(),sha256=hashlib.sha256(sl.read_bytes()).hexdigest(),face_index=fi,offset_from_reference_m=offset,status='retained temporary cap face, not newly certified transducer datum')
 elif emitter_surface_name:raise ValueError('Explicit emitter surface missing or duplicated')
 hit,normal,face,distance=tree.ray_cast(origin,direction,10)
 if hit is None:raise ValueError('No native wall hit')
 if normal.dot(direction)>0:normal=-normal
 library=Path(bpy.path.abspath(wall.library.filepath)).resolve() if wall.library else Path(bpy.data.filepath)
 emitter_pose=pose.copy();emitter_pose.translation=origin
 return dict(event_id=event_id,provenance='native_ray_intersection_illustrative_timing',emitter_ref=sensor_ref,receiver_ref=sensor_ref,emitter_local_m=list(sensor.location),reference_world_m=list(reference),reference_pose_world=[list(r) for r in pose],emitter_surface=surface,emitter_world_m=list(origin),emitter_pose_world=[list(r) for r in emitter_pose],direction_world=list(direction),hit_world_m=list(hit),normal_world=list(normal.normalized()),wall_source=dict(library=library.as_posix(),object=wall.name,version=library.stem,sha256=hashlib.sha256(library.read_bytes()).hexdigest(),face_index=face),send_s=float(send_s),contact_s=float(contact_s),receive_s=float(receive_s),patch_lifetime_s=float(patch_lifetime_s),opacity=.72,visible=True,standoff_m=float(distance),timing_kind='illustrative_not_acoustic_velocity',sample_policy='sampled native cap face plus unchanged reference; fixed contact retained during later assembly movement')

def validate_event(e):
 assert e['emitter_ref']==e['receiver_ref']
 assert e['send_s']<e['contact_s']<e['receive_s']
 for k in ['emitter_world_m','direction_world','hit_world_m','normal_world']:
  assert len(e[k])==3 and all(math.isfinite(v) for v in e[k])
 for k in ['direction_world','normal_world']:assert abs(Vector(e[k]).length-1)<1e-5
 assert 0<=e['opacity']<=1 and e['patch_lifetime_s']>0
 assert (Vector(e['hit_world_m'])-Vector(e['emitter_world_m'])).normalized().dot(Vector(e['direction_world']))>.99999
 return True
