import bpy,json
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';p=T/'Consumers/S03_shared-digital_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
target=bpy.data.objects['S03 | physical World live context'];records=[]
for name in ['Luminous geological strata','Subordinate formation survey grid']:
 o=bpy.data.objects[name];o.location.y-=.7;m=o.modifiers.new('Project context styling onto shared soil cap','SHRINKWRAP');m.target=target;m.wrap_method='PROJECT';m.wrap_mode='ABOVE_SURFACE';m.use_project_x=False;m.use_project_y=True;m.use_project_z=False;m.use_positive_direction=True;m.use_negative_direction=False;m.offset=.003
 records.append({'object':name,'target':target.name,'operation':'local Y -0.7m projection start; positive-Y ray to live World cap; offset0.003m','does_not_change':'local reconstruction data, labels, camera/timing'})
bpy.ops.wm.save_as_mainfile(filepath=str(p));(T/'Evidence/context-grid-projection.json').write_text(json.dumps(records,indent=2));print('GRID_PROJECTED')
