"""Run in current v002 session through official Blender MCP after snapshot."""
import bpy,json,math
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Environment/Borehole'
s=bpy.context.scene
assert 'ENTRY presentation controls' not in bpy.data.objects
old=bpy.data.objects['Shared continuous World'];M=old.matrix_world.copy()
ctrl=bpy.data.objects.new('ENTRY presentation controls',None);s.collection.objects.link(ctrl);ctrl['Bore scale']=1.;ctrl['Front reveal']=0.
def curves(ad):return [fc for l in ad.action.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==ad.action_slot_handle for fc in bag.fcurves]
proxy=bpy.data.objects['Opening front 00 -1'];scale=next(fc for fc in curves(proxy.animation_data) if fc.data_path=='scale' and fc.array_index==0)
retract=next(fc for fc in curves(proxy.data.shape_keys.animation_data) if fc.data_path=='key_blocks["Retracted"].value')
nominal=scale.evaluate(152)
for f in range(1,170):
 ctrl['Bore scale']=scale.evaluate(f)/nominal;ctrl.keyframe_insert(data_path='["Bore scale"]',frame=f)
 ctrl['Front reveal']=min(1.,max(0.,retract.evaluate(f)));ctrl.keyframe_insert(data_path='["Front reveal"]',frame=f)
for fc in curves(ctrl.animation_data):
 for k in fc.keyframe_points:k.interpolation='LINEAR'
with bpy.data.libraries.load(str(B/'World_environment_v014.blend'),link=True) as (a,b):
 b.collections=['WORLD_DESCENT_CONNECTED','WORLD_DESCENT_FRONT_CLOSURE'];b.node_groups=['WORLD retained bore presentation v001','WORLD front closure presentation v001']
retained,front=b.collections;rg,fg=b.node_groups
local=bpy.data.collections.new('Sequence World closed to cutaway');s.collection.children.link(local);records=[]
for col,group in [(retained,rg),(front,fg)]:
 for source in col.all_objects:
  assert source.type=='MESH'
  ob=bpy.data.objects.new('SHOT WORLD | '+source.name,source.data);local.objects.link(ob);ob.matrix_world=M@source.matrix_world
  mod=ob.modifiers.new('Shared World presentation; shot controls','NODES');mod.node_group=group
  for name in ['Bore scale','Front reveal']:
   ident=next(i.identifier for i in group.interface.items_tree if getattr(i,'in_out','')=='INPUT' and i.name==name)
   param=getattr(mod.properties.inputs,ident);fc=param.driver_add('value');v=fc.driver.variables.new();v.name='control';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["'+name+'"]';fc.driver.expression='control'
  ob['source']='World v014 linked mesh; consumer-local presentation modifier.';records.append(ob.name)
old.hide_render=True;old.hide_viewport=True
for lib in list(bpy.data.libraries):
 if Path(bpy.path.abspath(lib.filepath)).name=='Surface_descent_v006.blend':
  lib.filepath=str(R/'04-Production/Shared/Assets/Environment/Surface/Surface_descent_v007.blend');lib.reload()
ctrl['meaning']='Illustrative camera accommodation/reveal. Nominal shared wall restored by141; not physical motion or measured bore expansion.'
s.frame_set(106);bpy.context.view_layer.update()
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
p=Q/'Scenes/S01-S02_production_v003.blend';assert not p.exists();bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p))
(Q/'Notes/entry_v003_binding.json').write_text(json.dumps({'native':str(p),'world':'World_environment_v014.blend','local_world_objects':records,'source_nominal_scale':nominal,'control_source':'Retained original previs action curves, sampled1..169; unchanged camera and event data.','scope':'Shot timing local; meshes and geometry groups linked. Prior sharedWorld instance retained disabled.'},indent=2))
result={'saved':str(p),'world_objects':len(records),'control_at106':{k:ctrl[k] for k in ['Bore scale','Front reveal']}}
