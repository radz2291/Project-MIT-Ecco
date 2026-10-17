import bpy,json
from mathutils import Vector
bpy.ops.wm.open_mainfile(filepath='C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Mechanisms/B201/Scenes/B201_wall-interaction_still03_v001.blend')
e=json.load(open('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Records/Tasks/T-007/Evidence/Still_03/build-render_still03_v001.json'));w=Vector(e['wall']);o=bpy.data.objects['T6_WALL_CONTACT_SECTION'];near=min(o.data.vertices,key=lambda v:(v.co-w).length);print('NEAREST',list(near.co),'WALL',list(w),'ERROR',(near.co-w).length);print('WALLSOURCE',bpy.data.objects['IRREGULAR_FULL'].matrix_world)
