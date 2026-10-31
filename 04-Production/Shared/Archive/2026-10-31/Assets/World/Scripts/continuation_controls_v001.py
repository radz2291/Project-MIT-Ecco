"""Canonical T44 continuation instances; linked geometry, local length/visibility.

Parenting to the existing hardware instance preserves travel, spin and placement.
No source housing/collar vertices or existing camera/timing controls are edited.
"""
import bpy
from pathlib import Path

def attach_continuation(asset_dir,hardware_instance,length_m=12.,source_collections=None,master_path=None):
 if 'UPHOLE_CONTINUATION_CONTROL' in bpy.data.objects:raise RuntimeError('Continuation already attached')
 if source_collections is None:
  p=Path(master_path) if master_path else Path(asset_dir)/'BHA/BHA_film_v007.blend'
  with bpy.data.libraries.load(str(p),link=True) as (a,b):b.collections=['WORLD_UPHOLE_EXTENSION','WORLD_UPHOLE_JOINT']
  sources=b.collections
 else:sources=source_collections
 col=hardware_instance.users_collection[0]
 ctrl=bpy.data.objects.new('UPHOLE_CONTINUATION_CONTROL',None);col.objects.link(ctrl);ctrl.parent=hardware_instance
 ctrl['length_m']=float(length_m);ctrl['show']=1
 ctrl['interface']='T44 continuationv001; metres, length0.25..40m; static simplified collar continuation, no exact client thread fit'
 ctrl.id_properties_ui('length_m').update(min=.25,max=40,soft_min=1,soft_max=24,description='Added uphole length beyond source collar endX-1.5m; transverse diameter remains fixed')
 ctrl.id_properties_ui('show').update(min=0,max=1,description='Zero for isolated hero/product views')
 def drive(o,path,expression,props,index=None):
  d=(o.driver_add(path) if index is None else o.driver_add(path,index)).driver;d.expression=expression
  for name,(target,data_path) in props.items():
   v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=target;v.targets[0].data_path=data_path
 out={}
 for source in sources:
  o=bpy.data.objects.new(source.name+'_INSTANCE',None);col.objects.link(o);o.instance_type='COLLECTION';o.instance_collection=source;o.parent=hardware_instance
  if source.name=='WORLD_UPHOLE_EXTENSION':
   o.location.x=-1.5
   drive(o,'scale','max(.25,min(40,L))',{'L':(ctrl,'["length_m"]')},0)
  for field in ['hide_render','hide_viewport']:
   drive(o,field,'(show==0) or hidden',{'show':(ctrl,'["show"]'),'hidden':(hardware_instance,field)})
  out[source.name]=o
 endpoint=bpy.data.objects.new('UPHOLE_FAR_ENDPOINT',None);col.objects.link(endpoint);endpoint.parent=hardware_instance;endpoint.empty_display_size=.08
 drive(endpoint,'location','-1.5-max(.25,min(40,L))',{'L':(ctrl,'["length_m"]')},0)
 ctrl.update_tag();bpy.context.view_layer.update();return ctrl,out,endpoint
