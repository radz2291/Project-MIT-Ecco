"""Flat-tail waveform, real housing endpoints and ordered scan cycles."""
import bpy,json,sys,time,hashlib
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';sys.path.insert(0,str(R/'04-Production/Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input,arrival_readouts
out=Q/'Scenes/S01-S02_production_v013.blend';assert not out.exists() or '--candidate-rebuild' in sys.argv;s=bpy.context.scene;assert 'v012' in bpy.data.filepath
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Session_before_v013_{int(time.time())}.blend'),copy=True,compress=True)
events=json.loads((Q/'Notes/integration_v002.json').read_text())['events'];bha=bpy.data.objects['BHA sequence assembly'];poses=[]
cam=s.camera;camera_samples=[]
for f in range(300,601):
 old=300+min(f-300,288)*228/288;s.frame_set(int(old),subframe=old-int(old));camera_samples.append((f,cam.matrix_world.copy(),cam.data.lens))
for obj in [cam,cam.data]:
 if obj.animation_data and obj.animation_data.action:
  obj.animation_data.action=obj.animation_data.action.copy()
  for layer in obj.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      for idx in range(len(fc.keyframe_points)-1,-1,-1):
       if fc.keyframe_points[idx].co.x>=300:fc.keyframe_points.remove(fc.keyframe_points[idx],fast=True)
for f,m,lens in camera_samples:
 cam.matrix_world=m;cam.data.lens=lens
 for prop in ['location','rotation_quaternion' if cam.rotation_mode=='QUATERNION' else 'rotation_euler','scale']:cam.keyframe_insert(prop,frame=f)
 cam.data.keyframe_insert('lens',frame=f)
s.frame_end=600
for e in events:s.frame_set(e['start']);poses.append(bha.matrix_world.copy())
early=[]
for f in [1,180,220]:s.frame_set(f);early.append((f,bha.matrix_world.copy()))
bha.animation_data_clear()
def posekey(f,m):
 loc,rot,scale=m.decompose();bha.location=loc;bha.rotation_quaternion=rot;bha.scale=scale
 for p in ['location','rotation_quaternion','scale']:bha.keyframe_insert(p,frame=f)
for f,m in early:posekey(f,m)
starts=[300+48*i for i in range(6)]
for st,m in zip(starts,poses):posekey(st,m);posekey(st+42,m)
posekey(600,poses[-1])
for layer in bha.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
with bpy.data.libraries.load(str(R/'04-Production/Shared/Assets/Effects/Waveform/Waveform_shared_v018.blend'),link=True) as (a,b):b.objects=['WF_MASTER_CONTROLS','WF_PULSE_FIELD']
ctrl,template=b.objects;s.collection.objects.link(ctrl);records=[];hidden=[]
for ob in s.objects:
 if ('localized contact contour' in ob.name or 'contact digital nodes' in ob.name or 'localized digital overlay dimple' in ob.name or (ob.type=='CURVE' and 'contact' in ob.name.lower())):
  ob.hide_render=True;ob.hide_set(True);hidden.append(ob.name)
wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];receipts=wall.data.attributes['ecco_receipt_frame'];order=wall.data.attributes['ecco_reveal_order']
for e,st,pose in zip(events,starts,poses):
 s.frame_set(st);dg=bpy.context.evaluated_depsgraph_get();B=Vector(e['wall']);direction=Vector((-B.x,-B.y,0)).normalized();hits=[]
 for ins in dg.object_instances:
  ob=ins.object
  if not ins.is_instance or ob.type!='MESH' or not ob.library or 'Hardware' not in ob.library.filepath or any(k in ob.name for k in ['REF','PLANE']):continue
  mat=ins.matrix_world;inv=mat.inverted();hit,co,n,idx=ob.ray_cast(inv@B,(inv.to_3x3()@direction).normalized())
  if hit:
   pt=mat@co;distance=(pt-B).dot(direction)
   if 0<distance<.1:hits.append((distance,pt,ob.name))
 assert hits,('no physical surface hit',e['event']);distance,A,name=min(hits,key=lambda x:x[0]);o=bpy.data.objects[e['object']];o.location=A;o.data=template.data;o.modifiers.clear();mod=o.modifiers.new('Flat-tail v018 — sequenced local controls','NODES');mod.node_group=template.modifiers[0].node_group
 axis=(B-A).normalized();side=axis.cross(Vector((0,0,1))).normalized()
 settings={'Start frame':float(st),'Use master style':False,'Pulse count override':1,'Pulse count':1,'Pulse width':1.,'Lead rest frames':2.,'Flat after age':6.,'Tail allowance':12.,'Ringing':0.,'Travel frames':6.,'Reflection delay':2.,'Loop':False,'Show markers':False,'Gap length m':(B-A).length,'Route axis':tuple(axis),'Transverse axis':tuple(side),'Up axis':(0,0,1)}
 for k,v in settings.items():set_input(mod,k,v)
 s.frame_set(st+10);read=arrival_readouts(o);assert abs(read['Return tail arrival']-(st+42))<.001
 # Tile appears as the main spike strikes:6 travel+2 flat lead+2.1 spike age.
 impact=st+10;count=0
 for p in wall.data.polygons:
  if 'Unified cell '+str(e['event'])==wall.data.materials[p.material_index].name or wall.data.materials[p.material_index].name.startswith('Unified cell '+str(e['event'])+' '):receipts.data[p.index].value=impact;order.data[p.index].value=0;count+=1
 assert count,('no tile faces',e['event'])
 # Endpoint must remain on the same held housing for the entire return.
 for f in [st+22,st+28,st+42]:s.frame_set(f);assert max(abs(bha.matrix_world[r][c]-pose[r][c]) for r in range(4) for c in range(4))<.0001
 records.append({'event':e['event'],'start':st,'impact_tile':impact,'return_start':st+22,'return_complete':st+42,'surface':name,'surface_hit':list(A),'wall':list(B),'gap':distance,'tile_faces':count,'landmarks':read})
s.frame_set(310);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/waveform_v013_install.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'events':records,'hidden_impact_objects':hidden,'shared':'v018 adds Lead rest frames and Flat after age, defaults0 preserve v017','timing':'6 cycles start300..540 every48; each holds BHA42frames then6frame turn; spike width restored1, duration14 includes flat lead2 and flat trailing region; tile at spike arrival; return ends before turn','camera':'frames1..299 retained; close-up path300..528 stretched to300..588 then held to600; BHA/tile cues retimed with owner authorization','scope':'authored illustrative scan, physical housing ray intersections, not certified sensor interface'},indent=2));result={'saved':str(out),'events':records}

