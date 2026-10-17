import bpy,json
from pathlib import Path
from mathutils import Vector
r=Path.cwd();bpy.ops.wm.open_mainfile(filepath=str(r/'04-Production/Mechanisms/B202/Scenes/B202_measured-envelope_master_v009.blend'))
c=bpy.data.objects['B202_CONTROL'];c['show_tool']=1;c['travel_m']=0;c.update_tag();bpy.context.view_layer.update()
pts=[o.matrix_world@Vector(v) for o in bpy.context.scene.objects if o.name.startswith('B202_PRESENTATION_') for v in o.bound_box]
print('TOOL_BOUNDS',[(min(p[i] for p in pts),max(p[i] for p in pts)) for i in range(3)])
