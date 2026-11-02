"""Upgrade the current shot to additive shared guidev003; preserve source scene."""
import bpy,json
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Environment/Borehole'
with bpy.data.libraries.load(str(B/'World_motion_grid_v003.blend'),link=True) as (source,target):
    target.meshes=['WORLD_PIXEL_CUT_FACES','WORLD_PIXEL_SEABED','WORLD_PIXEL_BORE_RETAINED','WORLD_PIXEL_BORE_FRONT']
    target.node_groups=['WORLD pixel guide controls v003']
meshes={m.name:m for m in target.meshes};group=target.node_groups[0]
c=bpy.data.objects['World pixel guide controls']
values={'Enabled':True,'Show cut faces':True,'Show seabed':True,'Show bore':True,'Depth spacing m':20.,'Radial spacing m':5.,'Seabed spacing m':10.,'Bore ring spacing m':4.,'Bore lengthwise spacing deg':90.}
for k,v in values.items():c[k]=v
for ob in bpy.context.scene.objects:
    if not ob.name.startswith('World pixel_'):continue
    name=ob.name.replace('World pixel_','WORLD_PIXEL_');ob.data=meshes[name]
    old=ob.modifiers['Shared pixel guide spacing and visibility'];ob.modifiers.remove(old)
    mod=ob.modifiers.new('Shared pixel guide spacing and visibility','NODES');mod.node_group=group
    # Spacing must run before the original World pose/reveal modifier.
    ob.modifiers.move(len(ob.modifiers)-1,0)
    for socket in group.interface.items_tree:
        if getattr(socket,'in_out','')!='INPUT' or socket.socket_type=='NodeSocketGeometry':continue
        param=getattr(mod.properties.inputs,socket.identifier)
        if socket.name=='Component':param.value=2 if 'BORE' in ob.name else (1 if 'SEABED' in ob.name else 0)
        elif socket.name in values:
            param.value=values[socket.name];fc=param.driver_add('value');v=fc.driver.variables.new();v.name='control';v.type='SINGLE_PROP';v.targets[0].id=c;v.targets[0].data_path='["'+socket.name+'"]';fc.driver.expression='control'
c.update_tag();bpy.context.view_layer.update()
exec(bpy.data.texts['START HERE — pixel guides'].as_string())
bpy.ops.file.make_paths_relative()
bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v006.blend'),compress=True)
result={'scene':bpy.data.filepath,'controls':values}
