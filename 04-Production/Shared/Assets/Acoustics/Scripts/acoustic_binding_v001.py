"""Public effect-only shared-library binding. Native keyframes; no handlers.

Bind one actual/declared event after validating its provenance. Hardware and wall
are owned by the caller; this module never instantiates either.
"""
import bpy
from build_sensing_v001 import templates,event_objects,animate_event
from acoustic_event_v002 import validate_event

def bind_event(event,collection=None,frames=None,fps=24,library_version='v003'):
 validate_event(event)
 if collection is None:
  collection=bpy.data.collections.new('LOCAL_ACOUSTIC_EVENTS_'+event['event_id'])
  bpy.context.scene.collection.children.link(collection)
 temp=templates(library_version)
 obs=event_objects(event,temp,collection)
 animate_event(event,obs,frames or bpy.context.scene.frame_end,fps,None)
 make_controls(event,obs,collection,frames or bpy.context.scene.frame_end)
 return obs

def make_controls(event,objects,collection,frames):
 ctrl=bpy.data.objects.new('ACOUSTICS_CONTROL_'+event['event_id'],None);collection.objects.link(ctrl)
 ctrl['opacity']=1.0;ctrl['visible']=int(event['visible']);ctrl.id_properties_ui('opacity').update(min=0,max=1)
 ctrl['event_id']=event['event_id'];ctrl['emitter_ref']=event['emitter_ref'];ctrl['receiver_ref']=event['receiver_ref']
 for prop in ['send_s','contact_s','receive_s','patch_lifetime_s','packet_end_s','hold_emitter_until_s']:ctrl[prop]=event[prop]
 ctrl['timing_reference']=event['timing_reference']
 ctrl['timing_edit']='Event timing/lifetime are published metadata. Edit event JSON and rebind to regenerate native keyframes.'
 gains={o.name:[] for o in objects.values()}
 for f in range(1,frames+1):
  bpy.context.scene.frame_set(f)
  for o in objects.values():gains[o.name].append(o.color[3])
 for o in objects.values():
  for f,a in enumerate(gains[o.name],1):o['event_gain']=a;o.keyframe_insert(data_path='["event_gain"]',frame=f)
  for path,index,expr in [('color',3,'gain*opacity*visible'),('hide_render',None,'gain*opacity*visible<0.001'),('hide_viewport',None,'gain*opacity*visible<0.001')]:
   fc=o.driver_add(path) if index is None else o.driver_add(path,index);d=fc.driver;d.expression=expr
   for n,ob,prop in [('gain',o,'event_gain'),('opacity',ctrl,'opacity'),('visible',ctrl,'visible')]:
    v=d.variables.new();v.name=n;v.targets[0].id=ob;v.targets[0].data_path='["'+prop+'"]'
 return ctrl
