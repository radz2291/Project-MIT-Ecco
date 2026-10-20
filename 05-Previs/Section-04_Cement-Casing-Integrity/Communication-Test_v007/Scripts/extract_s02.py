import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1]
p=R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False);s=bpy.context.scene
out={}
for name in ['DW 1 SEND front0 core','DW 1 ECHO front0 core','DW 1 localized contact contour 0.012','DW 1 contact digital nodes 0.012']:
 o=bpy.data.objects.get(name)
 if not o:continue
 paths=[];visible=[]
 if o.animation_data and o.animation_data.action:
  for l in o.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      paths.append(fc.data_path)
      if fc.data_path=='hide_render':visible=[f for f in range(241,441) if fc.evaluate(f)<.5]
 frame=visible[len(visible)//2] if visible else 327;s.frame_set(frame);bpy.context.view_layer.update()
 coords=[list(o.matrix_world@Vector(p.co[:3])) for sp in o.data.splines for p in sp.points] if o.type=='CURVE' else [list(o.matrix_world@v.co) for v in o.data.vertices]
 sensors=[list(i.matrix_world.translation) for i in bpy.context.evaluated_depsgraph_get().object_instances if i.object.original.name=='ECCO_SENSOR_REF_01']
 out[name]=dict(frame=frame,visible_frames=visible,object_paths=list(set(paths)),data_animated=bool(o.data.animation_data),coordinates=coords[:160],sensor_world=sensors,bevel_depth=o.data.bevel_depth if o.type=='CURVE' else None,color=list(o.data.materials[0].diffuse_color))
(B/'Records/S02-visual-reference.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{x:y for x,y in v.items() if x!='coordinates'} for k,v in out.items()},indent=2))
