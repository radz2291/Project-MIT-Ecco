import bpy
from pathlib import Path
R=Path(__file__).resolve().parents[5]
for path in ['DigitalEnvironment/Digital_style_v001.blend','MeasurementReveal/Measurement_reveal_v001.blend']:
 bpy.ops.wm.open_mainfile(filepath=str(R/'04-Production/Shared/Assets'/path),load_ui=False)
 for g in bpy.data.node_groups:
  if g.name.startswith('ECCO'):
   print('GROUP',g.name)
   for n in g.nodes:print(n.name,n.bl_idname,[(i.name,list(i.default_value) if hasattr(i.default_value,'__len__') else i.default_value) for i in n.inputs if hasattr(i,'default_value')],[(o.name,list(o.default_value) if hasattr(o.default_value,'__len__') else o.default_value) for o in n.outputs if n.bl_idname=='ShaderNodeRGB'])
