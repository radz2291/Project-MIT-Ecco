"""Strict native-cap event sampler and declared three-front packet timing.

Required common send/contact/receive seconds describe the leading front. Each
following front lags by0.07s; the packet finishes at receive_s+0.14s. Hold the
actual emitting surface until packet_end_s. Timing is illustrative.
"""
import bpy,math,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
LAGS=(0.,.07,.14)

def exact_one(matches,label):
 if len(matches)!=1:raise ValueError(f'Expected exactly one {label}, got {len(matches)}; no reference fallback permitted')
 return matches[0]

def native_instance(name):
 return exact_one([(i.object.original,i.matrix_world.copy()) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.original.name==name],name)

def source_path(o):
 p=Path(bpy.path.abspath(o.library.filepath) if o.library else bpy.data.filepath).resolve(strict=True)
 if not p.is_file():raise ValueError('Native source file unavailable')
 return p

def source_meta(o,face):
 p=source_path(o)
 parent=o.library.parent if o.library else None
 parent_path=Path(bpy.path.abspath(parent.filepath)).resolve(strict=True).as_posix() if parent else None
 return dict(library=p.as_posix(),object=o.name,version=p.stem,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),face_index=int(face),library_parent=parent_path,library_filepath_exposed=o.library.filepath if o.library else bpy.data.filepath,resolution_policy='Blender exposed paths normalized to current consumer; strict actual path exists/hash, no basename fallback')

def wall_tree(name):
 o,m=native_instance(name)
 if o.type!='MESH':raise TypeError(name+' must be mesh')
 return o,m,BVHTree.FromPolygons([m@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])

def declare_packet(e):
 e['timing_reference']='send_s/contact_s/receive_s are leading-front times; three fronts lag0/.07/.14s'
 e['arc_phases']=[dict(arc_index=i+1,lag_s=lag,send_s=e['send_s']+lag,contact_s=e['contact_s']+lag,receive_s=e['receive_s']+lag) for i,lag in enumerate(LAGS)]
 e['packet_intervals']=dict(send_start_s=e['send_s'],last_send_launch_s=e['send_s']+LAGS[-1],send_end_s=e['contact_s']+LAGS[-1],contact_first_s=e['contact_s'],contact_last_s=e['contact_s']+LAGS[-1],return_start_s=e['contact_s'],return_end_s=e['receive_s']+LAGS[-1])
 e['packet_end_s']=e['receive_s']+LAGS[-1];e['hold_emitter_until_s']=e['packet_end_s']
 return e

def sample_native_event(sensor_ref,wall_object_name,event_id,send_s,contact_s,receive_s,patch_lifetime_s=.65,emitter_surface_name=None):
 if not send_s<contact_s<receive_s:raise ValueError('Expected leading send<contact<receive')
 bpy.context.view_layer.update();sensor,pose=native_instance(sensor_ref)
 reference=pose.translation.copy();direction=(pose.to_3x3()@Vector((0,0,1))).normalized()
 capname=emitter_surface_name or f'TEMP | Imaging port {int(sensor_ref[-2:])} | removable acoustic cap'
 cap,cp=native_instance(capname)
 if cap.type!='MESH':raise TypeError('Emitter cap must be actual native mesh')
 ct=BVHTree.FromPolygons([cp@v.co for v in cap.data.vertices],[list(p.vertices) for p in cap.data.polygons])
 origin,capnormal,capface,_=ct.ray_cast(reference+direction*.025,-direction,.05)
 if origin is None:raise ValueError('Native cap exit unavailable')
 offset=(origin-reference).dot(direction)
 if not math.isfinite(offset) or not 0<=offset<.025:raise ValueError('Cap exit outside bounded reference search')
 capmeta=source_meta(cap,capface);capmeta.update(offset_from_reference_m=offset,status='retained temporary cap face; provisional graphical emission exit, not certified transducer datum')
 wall,_,tree=wall_tree(wall_object_name);hit,normal,face,distance=tree.ray_cast(origin,direction,10)
 if hit is None:raise ValueError('No native first wall hit')
 if normal.dot(direction)>0:normal=-normal
 emitter_pose=pose.copy();emitter_pose.translation=origin
 e=dict(event_id=event_id,provenance='native_ray_intersection_illustrative_timing',emitter_ref=sensor_ref,receiver_ref=sensor_ref,emitter_local_m=list(sensor.location),reference_world_m=list(reference),reference_pose_world=[list(r) for r in pose],emitter_surface=capmeta,emitter_world_m=list(origin),emitter_pose_world=[list(r) for r in emitter_pose],direction_world=list(direction),hit_world_m=list(hit),normal_world=list(normal.normalized()),wall_source=source_meta(wall,face),send_s=float(send_s),contact_s=float(contact_s),receive_s=float(receive_s),patch_lifetime_s=float(patch_lifetime_s),opacity=.72,visible=True,standoff_m=float(distance),timing_kind='illustrative_not_acoustic_velocity',sample_policy='native temporary-cap exit; unchanged reference; fixed contact; emitter held through final lagged return')
 declare_packet(e);validate_event(e);return e

def _vector(v,n):return isinstance(v,(list,tuple)) and len(v)==n and all(isinstance(x,(int,float)) and math.isfinite(x) for x in v)
def validate_source(s):
 assert all(k in s for k in ['library','object','version','sha256','face_index'])
 assert all(isinstance(s[k],str) and s[k] for k in ['library','object','version','sha256'])
 assert isinstance(s['face_index'],int) and s['face_index']>=0
 assert len(s['sha256'])==64 and all(c in '0123456789abcdef' for c in s['sha256'])
 p=Path(s['library']).resolve(strict=True);assert p.is_file() and p.stem==s['version']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],'Actual source hash mismatch'
 return True

def validate_event(e):
 assert isinstance(e['event_id'],str) and e['event_id']
 assert e['provenance'] in ['native_ray_intersection_illustrative_timing','declared_adapter_fixture']
 assert e['emitter_ref']==e['receiver_ref'] and isinstance(e['emitter_ref'],str) and e['emitter_ref']
 for k in ['emitter_world_m','reference_world_m','emitter_local_m','direction_world','hit_world_m','normal_world']:assert _vector(e[k],3),k
 for k in ['reference_pose_world','emitter_pose_world']:assert len(e[k])==4 and all(_vector(r,4) for r in e[k])
 for k in ['send_s','contact_s','receive_s','patch_lifetime_s','opacity','standoff_m','packet_end_s','hold_emitter_until_s']:assert isinstance(e[k],(float,int)) and math.isfinite(e[k]),k
 assert e['send_s']<e['contact_s']<e['receive_s'] and 0<=e['opacity']<=1 and e['patch_lifetime_s']>0 and isinstance(e['visible'],bool)
 for k in ['direction_world','normal_world']:assert abs(Vector(e[k]).length-1)<1e-5
 delta=Vector(e['hit_world_m'])-Vector(e['emitter_world_m']);assert delta.length>0 and delta.normalized().dot(Vector(e['direction_world']))>.99999
 assert abs(delta.length-e['standoff_m'])<3e-6
 assert Vector(e['normal_world']).dot(Vector(e['direction_world']))<0
 validate_source(e['wall_source']);validate_source(e['emitter_surface'])
 assert isinstance(e['emitter_surface']['status'],str) and e['emitter_surface']['status']
 offset=e['emitter_surface']['offset_from_reference_m'];assert math.isfinite(offset) and 0<=offset<.025
 face_delta=Vector(e['emitter_world_m'])-Vector(e['reference_world_m']);assert (face_delta-Vector(e['direction_world'])*offset).length<3e-6
 assert len(e['arc_phases'])==3
 for i,(a,lag) in enumerate(zip(e['arc_phases'],LAGS)):
  assert a['arc_index']==i+1 and abs(a['lag_s']-lag)<1e-9
  for k in ['send_s','contact_s','receive_s']:assert abs(a[k]-(e[k]+lag))<1e-9
 assert abs(e['packet_end_s']-(e['receive_s']+.14))<1e-9 and e['hold_emitter_until_s']>=e['packet_end_s']
 assert e['timing_reference'].startswith('send_s/contact_s/receive_s are leading-front times')
 expected=declare_packet(dict(e))['packet_intervals']
 assert set(e['packet_intervals'])==set(expected)
 assert all(abs(e['packet_intervals'][k]-v)<1e-9 for k,v in expected.items())
 return True

def validate_native_event(e,tolerance=3e-6):
 validate_event(e)
 fresh=sample_native_event(e['emitter_ref'],e['wall_source']['object'],e['event_id'],e['send_s'],e['contact_s'],e['receive_s'],e['patch_lifetime_s'],e['emitter_surface']['object'])
 for k in ['emitter_world_m','reference_world_m','hit_world_m','normal_world','direction_world','emitter_local_m']:assert (Vector(fresh[k])-Vector(e[k])).length<tolerance,k
 for k in ['wall_source','emitter_surface']:
  for field in ['library','object','version','sha256','face_index']:assert fresh[k][field]==e[k][field],(k,field)
 assert abs(fresh['emitter_surface']['offset_from_reference_m']-e['emitter_surface']['offset_from_reference_m'])<tolerance
 return True
