import bpy,json
from pathlib import Path
from mathutils import Matrix
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Environment/Borehole';s=bpy.context.scene
assert 'World pixel guide controls' not in bpy.data.objects
temp=bpy.data.objects.get('TEMP viewport pixel guide')
if temp:bpy.data.objects.remove(temp,do_unlink=True)
old=bpy.data.objects.get('World motion reference grid')
if old:old.hide_render=True;old.hide_viewport=True;old['status']='Superseded surface-strip attempt; pixel-wire guides replace it.'
with bpy.data.libraries.load(str(B/'World_motion_grid_v002.blend'),link=True) as (a,b):
 b.objects=['WORLD_PIXEL_CUT_FACES','WORLD_PIXEL_SEABED','WORLD_PIXEL_BORE_RETAINED','WORLD_PIXEL_BORE_FRONT'];b.node_groups=['WORLD pixel guide controls v002']
group=b.node_groups[0];M=Matrix(json.loads((B/'World_interface_v014.json').read_text())['canonical_to_s02'])
col=bpy.data.collections.new('World motion guides — viewport pixels');s.collection.children.link(col);ctrl=bpy.data.objects.new('World pixel guide controls',None);col.objects.link(ctrl)
values={'Enabled':True,'Show cut faces':True,'Show seabed':True,'Show bore':True,'Depth spacing m':25.,'Radial spacing m':10.,'Seabed spacing m':10.,'Bore ring spacing m':1.}
for k,v in values.items():ctrl[k]=v
ctrl['Line width px']=1.2;ctrl['Line opacity']=.8;ctrl['Stroke shade']=.008;ctrl.id_properties_ui('Stroke shade').update(min=0.,max=1.);ctrl['meaning']='Edge-only guide data; draw using shared pixel_guides_viewport.py GPU overlay/export helper.'
entry=bpy.data.objects['ENTRY presentation controls'];records=[]
def driver(param,prop,owner):
 fc=param.driver_add('value');v=fc.driver.variables.new();v.name='control';v.type='SINGLE_PROP';v.targets[0].id=owner;v.targets[0].data_path='["'+prop+'"]';fc.driver.expression='control'
def input(m,name):
 ident=next(x.identifier for x in m.node_group.interface.items_tree if getattr(x,'in_out','')=='INPUT' and x.name==name);return getattr(m.properties.inputs,ident)
for source in b.objects:
 ob=bpy.data.objects.new(source.name.replace('WORLD_PIXEL','World pixel'),source.data);col.objects.link(ob);ob.matrix_world=M;ob.display_type='WIRE';ob.show_wire=True;ob.show_all_edges=True;ob.show_in_front=False;ob.color=(.08,.08,.08,1)
 m=ob.modifiers.new('Shared pixel guide spacing and visibility','NODES');m.node_group=group;input(m,'Component').value=int(source['component'])
 for prop in values:driver(input(m,prop),prop,ctrl)
 if 'BORE' in source.name:
  name='WORLD front closure presentation v001' if 'FRONT' in source.name else 'WORLD retained bore presentation v001';pose=ob.modifiers.new('Follow existing rock presentation','NODES');pose.node_group=bpy.data.node_groups[name]
  for prop in ['Bore scale','Front reveal']:driver(input(pose,prop),prop,entry)
 for channel in range(3):
  fc=ob.driver_add('color',channel);v=fc.driver.variables.new();v.name='shade';v.type='SINGLE_PROP';v.targets[0].id=ctrl;v.targets[0].data_path='["Stroke shade"]';fc.driver.expression='shade'
 records.append(ob.name)
s.frame_set(157);bpy.context.view_layer.update()
(Q/'Notes/pixel_grid_v005_install.json').write_text(json.dumps({'objects':records,'controls':ctrl.name,'defaults':values,'stroke':'GPU pixel overlay/export; edge-only mesh data, no faces/tubes/strips.','bore_behavior':'Linked original World presentation groups follow bore widening/front retraction.','source_module':'World_motion_grid_v002.blend'},indent=2));result={'installed':records,'controls':ctrl.name}
