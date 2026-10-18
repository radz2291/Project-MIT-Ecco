"""Linked A-FLOW geometry and local controls. Blender5.2, metres/+X downhole layout.

No handler, custom driver namespace, simulation cache or source-geometry copy.
"""
import bpy, math
from pathlib import Path

DEFAULTS=dict(phase=0.0,speed=.16,density=10,cuttings_visible=1,flow_visible=1,stage_emphasis=0,operating_mode=0)

def drive(owner,path,expression,ctrl,props,index=None):
 f=owner.driver_add(path) if index is None else owner.driver_add(path,index)
 d=f.driver;d.expression=expression
 for name,prop in props.items():
  v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+prop+'"]'
 return d

def create_flow(library_path,placement=None,name='FLOW'):
 """Return(root,control,local wrappers); path/particle geometry remains linked.

 operating_mode0=circulation-only,1=off. Other drilling modes are not constructed.
 stage_emphasis0=all,1=lower,2=middle,3=upper. All paths remain active.
 phase cycles; speed authored path cycles/s; density0..10 moving matte cuttings.
 """
 with bpy.data.libraries.load(str(library_path),link=True) as (a,b):b.collections=['HYDRAULICS_GEOMETRY']
 source=b.collections[0];col=bpy.data.collections.new(name+'_LOCAL_WRAPPERS');bpy.context.scene.collection.children.link(col)
 root=bpy.data.objects.new(name+'_PLACEMENT',None);col.objects.link(root);root.parent=placement
 ctrl=bpy.data.objects.new(name+'_CONTROL',None);col.objects.link(ctrl);ctrl.parent=root
 for k,v in DEFAULTS.items():ctrl[k]=v;ctrl.property_overridable_library_set('["'+k+'"]',True)
 ctrl['interface']='A-FLOWv001; illustrative circulation-only; phase cycles, speed cycles/s, density0..10; emphasis0all/1lower/2middle/3upper; mode0circulation/1off'
 for k in ['phase','speed']:ctrl.id_properties_ui(k).update(min=0,max=100 if k=='phase' else 1)
 for k in ['density','cuttings_visible','flow_visible','stage_emphasis','operating_mode']:ctrl.id_properties_ui(k).update(min=0,max=10 if k=='density' else 3 if k=='stage_emphasis' else 1)
 wrappers=[];paths=[]
 for src in sorted([o for o in source.objects if o.name.startswith('FLOW_PATH_')],key=lambda o:o.name):
  o=bpy.data.objects.new(name+'_'+src.name,src.data);col.objects.link(o);o.parent=root;o['source_object']=src.name;o['source_geometry']='linked immutable curve data'
  for p in ['hide_render','hide_viewport']:drive(o,p,'(vis==0) or (mode!=0)',ctrl,dict(vis='flow_visible',mode='operating_mode'))
  paths.append(o);wrappers.append(o)
 mesh=source.objects['CUTTING_GEOMETRY'].data
 for i,path in enumerate(paths):
  for j in range(3):
   # Follow Path evaluates the target's world placement; an additional parent
   # would apply assembly translation twice. Constraint owns particle placement.
   o=bpy.data.objects.new(name+'_CUTTING_%02d_%02d'%(i,j),mesh);col.objects.link(o)
   parameter=bpy.data.objects.new(name+'_PARAMETER_%02d_%02d'%(i,j),None);col.objects.link(parameter);parameter.parent=root;parameter['t']=0.0
   drive(parameter,'["t"]',f'(phase+(frame-1)/24*speed+{i*.037+j/3:.8f})%1',ctrl,dict(phase='phase',speed='speed'))
   c=o.constraints.new('FOLLOW_PATH');c.target=path;c.use_fixed_location=True;c.use_curve_follow=False
   drive(c,'offset_factor','v',parameter,dict(v='t'))
   for p in ['hide_render','hide_viewport']:drive(o,p,f'(vis==0) or (mode!=0) or (density<={i})',ctrl,dict(vis='cuttings_visible',mode='operating_mode',density='density'))
   # Modest emphasis follows spatial windows, never sequential activation.
   o['phase_offset']=i*.037+j/3
   match='(emphasis==1 and .32<=t<=.425) or (emphasis==2 and .425<t<=.66) or (emphasis==3 and .66<t<=.85)'
   for axis in range(3):
    dr=drive(o,'scale',f'1.0 if emphasis==0 or {match} else 0.85',ctrl,dict(emphasis='stage_emphasis'),axis)
    v=dr.variables.new();v.name='t';v.type='SINGLE_PROP';v.targets[0].id=parameter;v.targets[0].data_path='["t"]'
   wrappers.append(o)
 if source.objects.get('FLOW_TRACER_GEOMETRY'):
  wrappers.extend(add_tracers(source,root,ctrl,paths,col,name))
 ctrl.update_tag();bpy.context.view_layer.update();return root,ctrl,wrappers

def add_tracers(source,root,ctrl,paths,col,name='FLOW'):
 """Small axial amber dashes convey continuous travel, distinct from matte cuttings."""
 mesh=source.objects['FLOW_TRACER_GEOMETRY'].data;objects=[]
 for i,path in enumerate(paths):
  for j in range(2):
   helper=bpy.data.objects.new(name+'_TRACER_PARAMETER_%02d_%02d'%(i,j),None);col.objects.link(helper);helper['t']=0.0
   drive(helper,'["t"]',f'(phase+(frame-1)/24*speed+{i*.043+j/2+.15:.8f})%1',ctrl,dict(phase='phase',speed='speed'))
   o=bpy.data.objects.new(name+'_TRACER_%02d_%02d'%(i,j),mesh);col.objects.link(o)
   c=o.constraints.new('FOLLOW_PATH');c.target=path;c.use_fixed_location=True;drive(c,'offset_factor','v',helper,dict(v='t'))
   for p in ['hide_render','hide_viewport']:drive(o,p,'(vis==0) or (mode!=0)',ctrl,dict(vis='flow_visible',mode='operating_mode'))
   objects.append(o)
 return objects
