"""Native cap-exit registration, exact hidden endpoints, annular sightline."""
import bpy,sys,json,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';S=T/'Scenes';E=T/'Evidence';sys.path.insert(0,str(HERE))
from acoustic_event_v001 import sample_native_event
from build_sensing_v001 import animate_event,save,dump,cue
from acoustic_binding_v001 import make_controls
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(S/f'Sensing_reuse_{kind}_v005.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;col=bpy.data.collections['LOCAL_ACOUSTIC_EVENTS'];old=json.loads((E/f'events_{kind}_v001.json').read_text())['events'];events=[]
 # Remove old local opacity drivers/controllers only; shared data remains linked.
 for o in list(col.objects):
  if o.name.startswith('ACOUSTICS_CONTROL_'):bpy.data.objects.remove(o,do_unlink=True)
  elif o.get('shared_package')=='Acoustics':
   if o.animation_data:o.animation_data_clear()
 for e in old:
  s.frame_set(round(e['send_s']*24)+1);bpy.context.view_layer.update()
  event=sample_native_event(e['emitter_ref'],e['wall_source']['object'],e['event_id'],e['send_s'],e['contact_s'],e['receive_s'],e['patch_lifetime_s']);events.append(event)
  obs={o['shared_prototype']:o for o in col.objects if o.name.startswith(event['event_id'])};animate_event(event,obs,s.frame_end,24,None);make_controls(event,obs,col,s.frame_end)
 # Camera is derived from real annular gap, avoiding housing/rock sightline.
 poses=[];dx,dr,lens=(-.05,.020,30) if kind=='A' else (.060,.018,32)
 for event in events:
  ref=Vector(event['reference_world_m']);d=Vector(event['direction_world']);src=Vector(event['emitter_world_m']);hit=Vector(event['hit_world_m']);poses.append((ref+Vector((dx,0,0))+d*dr,(src+hit)*.5))
 cam=s.camera;cam.data.lens=lens
 for o in list(s.objects):
  if o.parent==cam:bpy.data.objects.remove(o,do_unlink=True)
 cue(s,col,events[0])
 shift=0 if kind=='A' else .25
 for f in range(1,s.frame_end+1):
  t=(f-1)/24;u=max(0,min(1,(t-(1.65+shift))/.45));u=u*u*(3-2*u);loc=poses[0][0].lerp(poses[1][0],u);target=poses[0][1].lerp(poses[1][1],u);cam.location=loc;cam.rotation_euler=(target-loc).to_track_quat('-Z','Y').to_euler();cam.keyframe_insert(data_path='location',frame=f);cam.keyframe_insert(data_path='rotation_euler',frame=f)
 # Exact native product sightlines for the visible cap exit and true wall contact.
 rays=[]
 for event in events:
  s.frame_set(round(event['send_s']*24)+1);bpy.context.view_layer.update();trees=[]
  for i in bpy.context.evaluated_depsgraph_get().object_instances:
   ob=i.object.original;m=i.matrix_world.copy()
   if ob.type=='MESH' and ob.library and 'ECCO' in ob.library.filepath and not ob.hide_render:trees.append((ob.name,BVHTree.FromPolygons([m@v.co for v in ob.data.vertices],[list(p.vertices) for p in ob.data.polygons])))
  for name,target in [('cap_exit',Vector(event['emitter_world_m'])),('wall_contact',Vector(event['hit_world_m']))]:
   delta=target-cam.location;occluders=[]
   for ob,tree in trees:
    p,n,face,dist=tree.ray_cast(cam.location,delta.normalized(),delta.length)
    if p is not None and delta.length-dist>.00005:occluders.append(dict(object=ob,blocked_by_m=delta.length-dist))
   rays.append(dict(event=event['event_id'],target=name,camera=list(cam.location),point=list(target),occluders=occluders))
 s.frame_set(17);s['event_export']=str((E/f'events_{kind}_v002.json').relative_to(ROOT)).replace('\\','/')
 save(S/f'Sensing_reuse_{kind}_v006.blend');dump(E/f'events_{kind}_v002.json',dict(contract='ecco-acoustic-event-v001',extension='native temporary-cap exit registration; source reference remains separate',events=events));dump(E/f'sightlines_{kind}_v006.json',dict(rays=rays,all_clear=not any(r['occluders'] for r in rays),camera_method='Actual reference + axial offset plus radial distance inside annulus; look at native cap-exit/wall midpoint; follows between held events only'))
 print('SENSING_SIGHTLINES',kind,not any(r['occluders'] for r in rays),rays,flush=True)
