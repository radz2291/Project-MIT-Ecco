import bpy,json,pathlib
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056'
result={}
for key,path in [('S02','05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'),('S04','04-Production/Shots/S04/S04-A/Previs_v033/Scenes/S04_continuous_ABCD_v033.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(R/path));s=bpy.context.scene;items=[]
 for ob in bpy.data.objects:
  if not any(w in ob.name.upper() for w in ['SEND','ECHO','OUTGOING','RETURN']):continue
  if not ob.animation_data or not ob.animation_data.action:continue
  a=ob.animation_data.action;curves=[]
  for layer in a.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path in ['location','hide_render','hide_viewport']:curves.append([fc.data_path,fc.array_index,[[p.co.x,p.co.y] for p in fc.keyframe_points]])
  if curves:items.append({'name':ob.name,'matrix':[list(r) for r in ob.matrix_world],'curves':curves})
 result[key]={'source':path,'camera':s.camera.name,'range':[s.frame_start,s.frame_end],'fps':s.render.fps,'objects':items}
(T/'consumer-source-events_v014.json').write_text(json.dumps(result,indent=2));print('SAVED_EVENT_INSPECTION')
