import bpy,json,pathlib
root=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco')
out={}
for o in bpy.data.objects:
 if o.name.startswith('DW 1') and o.animation_data and o.animation_data.action:
  a=o.animation_data.action
  curves=[]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      curves.append({'path':fc.data_path,'index':fc.array_index,'keys':[[round(k.co.x,3),round(k.co.y,6)] for k in fc.keyframe_points]})
  out[o.name]=curves
(root/'04-Production/Records/Tasks/T-056/event-timing.json').write_text(json.dumps(out,indent=2))
