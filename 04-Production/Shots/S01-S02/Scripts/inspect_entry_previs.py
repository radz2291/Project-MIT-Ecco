"""Read-only native previs inspection. Run Blender background with source file loaded."""
import bpy,json,math
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
s=bpy.context.scene
front=bpy.data.objects['Opening front 00 -1'];rear=bpy.data.objects['Formation rear 00']
frames=[90,94,97,106,112,114,120,122,126,132,141,152]
samples=[];retraction=[];radii=[]
for f in range(80,153):
 s.frame_set(f);value=front.data.shape_keys.key_blocks['Retracted'].value
 retraction.append([f,value]);radii.append([f,.65*rear.scale.x])
 if f in frames:
  samples.append({'frame':f,'camera_position':list(s.camera.matrix_world.translation),'camera_radius_m':math.hypot(s.camera.matrix_world.translation.x,s.camera.matrix_world.translation.y),'lens_mm':s.camera.data.lens,'closed_bore_radius_m':.65*rear.scale.x,'front_retraction':value,'camera_matrix':[list(row) for row in s.camera.matrix_world]})
d={'source':bpy.data.filepath,'range':[s.frame_start,s.frame_end],'fps':s.render.fps,'samples':samples,'front_retraction_first_nonzero':next(f for f,v in retraction if v>1e-6),'front_retraction_first_complete':next(f for f,v in retraction if v>=1-1e-6),'radius_first_decrease':next(f for f,v in radii if v<.65-1e-6),'radius_settled_m':radii[-1][1],'notes':'Actual native state; source file never saved. Product missing-library warnings do not affect this entry environment/camera inspection.'}
(Q/'Notes/entry_previs_native.json').write_text(json.dumps(d,indent=2));print('ENTRY_INSPECTION',json.dumps({k:v for k,v in d.items() if k!='samples'}))
