import bpy,json,math,re
from pathlib import Path
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1]
results={}
for label,p,frame in [('S02',R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend',339),('S04',R/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend',180)]:
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(frame);bpy.context.view_layer.update()
 names=[o for o in s.objects if re.search('wavefront|outgoing|return|signal|impact|echo|contact|sensor|pulse|SEND|RETURN',o.name,re.I)]
 rows=[]
 for o in names[:90]:rows.append(dict(name=o.name,type=o.type,location=list(o.matrix_world.translation),scale=list(o.scale),hidden=o.hide_render,materials=[m.name for m in o.data.materials if m] if o.type in ['MESH','CURVE'] else [],animated=bool(o.animation_data)))
 d=dict(path=str(p),engine=s.render.engine,frame=frame,objects=rows,matching_objects=len(names),camera_location=list(s.camera.location),camera_lens=s.camera.data.lens)
 if label=='S04':
  steel=bpy.data.objects['Steel - unchanged source with viewing window'];pts=[v.co for v in steel.data.vertices]
  bins={}
  for v in pts:
   radius=math.hypot(v.y,v.z)
   if radius<.169:
    a=math.atan2(v.z,v.y);bins.setdefault(round(a,3),[]).append((v.x,radius))
  center=min(bins,key=abs);d['wear_profile']=sorted(bins[center]);d['steel_smooth_faces']=sum(p.use_smooth for p in steel.data.polygons);d['steel_faces']=len(steel.data.polygons);d['shader_mask_materials']=len([m for m in bpy.data.materials if m.animation_data]);d['helper_named_objects']=[o.name for o in s.objects if re.search('helper|contact wall',o.name,re.I)]
 else:
  d['relevant_materials']=[dict(name=m.name,diffuse=list(m.diffuse_color),nodes=[n.name for n in m.node_tree.nodes] if m.node_tree else [],animated=bool(m.animation_data)) for m in bpy.data.materials if re.search('wavefront|impact|contact|echo|outbound|return|digital',m.name,re.I)][:45]
 results[label]=d
(B/'Records/input-inspection.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2)[:15000])
