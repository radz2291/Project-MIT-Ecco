"""Consumer API. Linked geometry owns dimensions; local instances own visibility.

No handlers or automatic execution. Run create_cased after create_world.
"""
import bpy
from pathlib import Path

def create_cased(asset_dir,version='v002'):
 p=Path(asset_dir)/'CasedHole'/('CasedHole_'+version+'.blend')
 names=['CASED_'+k+'_'+cut for k in ['STEEL_NOMINAL','STEEL_WEAR','CEMENT_SUPPORTED','CEMENT_CHANNEL','CHANNEL','NOMINAL_REFERENCE'] for cut in ['FULL','CUTAWAY']]
 with bpy.data.libraries.load(str(p),link=True) as (a,b):
  assert all(n in a.collections for n in names);b.collections=names
 c=bpy.data.collections.new('LOCAL_CASED_INSTANCES');bpy.context.scene.collection.children.link(c)
 ctrl=bpy.data.objects.new('CASED_CONTROL',None);c.objects.link(ctrl)
 defaults=dict(cutaway=1,show_steel=1,show_cement=1,show_channel=1,show_reference=1,wear=0,channel=0)
 for k,v in defaults.items():ctrl[k]=v;ctrl.id_properties_ui(k).update(min=0,max=1)
 ctrl['interface']='v001; metres/+X; no source scale override; channel/wear geometry master-owned'
 ctrl['channel_x0_m']=-2.5;ctrl['channel_x1_m']=-.4;ctrl['channel_angle_min_rad']=.30;ctrl['channel_angle_max_rad']=.80
 ctrl['wear_depth_m']=.004;ctrl['bounds_edit']='Republish immutable master through build_cased_v001.py; these informational bounds do not change linked geometry.'
 out={}
 for source in b.collections:
  o=bpy.data.objects.new(source.name+'_INSTANCE',None);c.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=source
  k=source.name.removeprefix('CASED_').removesuffix('_CUTAWAY').removesuffix('_FULL');cut=int(source.name.endswith('CUTAWAY'))
  expr=f'(cut!={cut})';props={'cut':'cutaway'}
  if k.startswith('STEEL'):expr+=' or (show==0) or (wear!='+str(int(k.endswith('WEAR')))+')';props.update(show='show_steel',wear='wear')
  elif k.startswith('CEMENT'):expr+=' or (show==0) or (channel!='+str(int(k.endswith('CHANNEL')))+')';props.update(show='show_cement',channel='channel')
  elif k=='CHANNEL':expr+=' or (show==0) or (channel==0)';props.update(show='show_channel',channel='channel')
  else:expr+=' or (show==0) or (wear==0)';props.update(show='show_reference',wear='wear')
  for path in ['hide_render','hide_viewport']:
   d=o.driver_add(path).driver;d.expression=expr
   for name,prop in props.items():
    v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+prop+'"]'
  out[source.name]=o
 ctrl.update_tag();bpy.context.view_layer.update();return ctrl,out

def response_from_event(event,support_state):
 """Casing-only qualitative adapter; no pulse, waveform, or material inference."""
 assert support_state in ['supported','weakly_supported']
 assert event['emitter_ref']==event['receiver_ref']
 assert event['send_s']<event['contact_s']<event['receive_s']
 return dict(event_id=event['event_id'],support_state=support_state,decay_kind='short_qualitative' if support_state=='supported' else 'long_qualitative',response_start_s=event['contact_s'],provenance=event['provenance'])

def add_response(event,support_state,col,fps=24):
 """Small contact-local schematic bars; authored amplitude/lifetime, no scale."""
 import math
 from mathutils import Vector
 response=response_from_event(event,support_state)
 mat=bpy.data.materials.get('CASED_QUALITATIVE_RESPONSE') or bpy.data.materials.new('CASED_QUALITATIVE_RESPONSE');mat.diffuse_color=(.20,.72,.56,1);mat.use_nodes=True
 bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.20,.72,.56,1);bs.inputs['Emission Color'].default_value=(.1,.5,.3,1);bs.inputs['Emission Strength'].default_value=.4
 hit=Vector(event['hit_world_m']);normal=Vector(event['normal_world']).normalized();axis=Vector((1,0,0));tangent=normal.cross(axis).normalized()
 start=event['contact_s'];duration=.45 if support_state=='supported' else 1.20
 response.update(response_lifetime_s=duration,response_end_s=start+duration,frame_sampling='Visible exactly when contact_s <= (frame-1)/fps < response_end_s; one-frame quantization only.')
 for i in range(12):
  data=bpy.data.curves.new('LOCAL_DECAY_BAR','CURVE');data.dimensions='3D';data.bevel_depth=.00055;data.bevel_resolution=0;sp=data.splines.new('POLY');sp.points.add(1)
  a=hit+normal*.001+axis*(i*.005-.0275);h=.010*math.exp(-i*(.33 if support_state=='supported' else .095))
  for p,q in zip(sp.points,[a-tangent*h,a+tangent*h]):p.co=(*q,1)
  ob=bpy.data.objects.new('CASED_'+support_state+'_RESPONSE_'+str(i),data);col.objects.link(ob);data.materials.append(mat);ob['event_id']=event['event_id'];ob['meaning']='Schematic contact-local decay; arbitrary amplitudes/time, no bond or thickness value'
  for f in range(1,bpy.context.scene.frame_end+1):
   ob.hide_render=not(start<=(f-1)/fps<start+duration);ob.keyframe_insert(data_path='hide_render',frame=f)
 return response
