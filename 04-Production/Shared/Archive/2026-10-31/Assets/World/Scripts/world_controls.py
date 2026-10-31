"""A-WORLD instance API v001. Run from Blender; no handlers or geometry copies.

create_world(asset_dir) returns (placement, controls, instances). Camera/light/
timing are consumer-owned. Root is rigid placement only; do not scale it.
"""
import bpy
from pathlib import Path
def create_world(asset_dir,environment_version='v004',hardware_version='v002'):
 asset_dir=Path(asset_dir);scene=bpy.context.scene
 c=bpy.data.collections.new('LOCAL_WORLD_INSTANCES');scene.collection.children.link(c)
 placement=bpy.data.objects.new('WORLD_PLACEMENT',None);c.objects.link(placement)
 ctrl=bpy.data.objects.new('WORLD_CONTROL',None);c.objects.link(ctrl);ctrl.parent=placement
 for k,v in dict(travel_m=.5,rotation_rad=.4,variant=1,cutaway=1,show_hardware=1,show_open=1,show_casing=1,show_cement=1,show_formation=1,show_shoe=1,show_mud=1).items():
  ctrl[k]=v
  if k not in ['travel_m','rotation_rad']:ctrl.id_properties_ui(k).update(min=0,max=2 if k=='variant' else 1)
 ctrl['interface']='v001; metres, X longitudinal; variant0 nominal/1 irregular/2 spiral; optical mud proxy'
 def drive(o,path,expression,props,index=None):
  f=o.driver_add(path) if index is None else o.driver_add(path,index);d=f.driver;d.expression=expression
  for name,prop in props.items():
   v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+prop+'"]'
 def load(path,names):
  with bpy.data.libraries.load(str(path),link=True) as (a,b):b.collections=names
  return b.collections
 specs={}
 for v,name in enumerate(['NOMINAL','IRREGULAR','SPIRAL']):
  for cut in [False,True]:specs['WORLD_'+name+('_CUTAWAY' if cut else '_FULL')]=('(show==0) or (v!='+str(v)+') or (cut!='+str(int(cut))+')',dict(show='show_open',v='variant',cut='cutaway'))
 for name,prop in [('CASING','show_casing'),('CEMENT','show_cement')]:
  for cut in [False,True]:specs['WORLD_'+name+('_CUTAWAY' if cut else '_FULL')]=('(show==0) or (cut!='+str(int(cut))+')',dict(show=prop,cut='cutaway'))
 for name,prop in [('UPPER_FORMATION','show_formation'),('SHOE','show_shoe'),('MUD','show_mud')]:specs['WORLD_'+name]=('show==0',dict(show=prop))
 env=load(asset_dir/('WellAssembly/World_environment_'+environment_version+'.blend'),list(specs))
 hw=load(asset_dir/('BHA/BHA_film_'+hardware_version+'.blend'),['WORLD_HARDWARE'])
 instances={}
 for source in env+hw:
  o=bpy.data.objects.new(source.name+'_INSTANCE',None);o.instance_type='COLLECTION';o.instance_collection=source;o.parent=placement;c.objects.link(o);instances[source.name]=o
  expr,props=specs.get(source.name,('show==0',dict(show='show_hardware')))
  for path in ['hide_render','hide_viewport']:drive(o,path,expr,props)
  if source.name=='WORLD_HARDWARE':
   drive(o,'location','travel',dict(travel='travel_m'),0);drive(o,'rotation_euler','rot',dict(rot='rotation_rad'),0)
 ctrl.update_tag();bpy.context.view_layer.update()
 return placement,ctrl,instances
