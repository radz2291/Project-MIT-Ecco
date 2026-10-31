"""Shared A-WORLD v005 environment instances, compatible local controls."""
import bpy
from pathlib import Path
from world_controls import create_world as create_base
def create_world(asset_dir):
 root,ctrl,instances=create_base(asset_dir,environment_version='v005')
 old=instances.pop('WORLD_UPPER_FORMATION');col=old.users_collection[0];bpy.data.objects.remove(old,do_unlink=True)
 names=['WORLD_FORMATION_'+v+'_'+cut for v in ['NOMINAL','IRREGULAR','SPIRAL'] for cut in ['FULL','CUTAWAY']]
 with bpy.data.libraries.load(str(Path(asset_dir)/'WellAssembly/World_environment_v005.blend'),link=True) as (a,b):b.collections=names
 for source in b.collections:
  obj=bpy.data.objects.new(source.name+'_INSTANCE',None);obj.instance_type='COLLECTION';obj.instance_collection=source;obj.parent=root;col.objects.link(obj);instances[source.name]=obj
  v=['NOMINAL','IRREGULAR','SPIRAL'].index(source.name.split('_')[2]);cut=int(source.name.endswith('CUTAWAY'))
  for path in ['hide_render','hide_viewport']:
   d=obj.driver_add(path).driver;d.expression=f'(show==0) or (v!={v}) or (cut!={cut})'
   for name,prop in [('show','show_formation'),('v','variant'),('cut','cutaway')]:
    var=d.variables.new();var.name=name;var.type='SINGLE_PROP';var.targets[0].id=ctrl;var.targets[0].data_path='["'+prop+'"]'
 ctrl['interface']='v002 / environment v005; surrounding mass18m axial, 4.8m transverse; source bore dimensions fixed'
 ctrl.update_tag();bpy.context.view_layer.update();return root,ctrl,instances
