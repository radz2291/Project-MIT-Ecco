import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend'),use_scripts=False,load_ui=False)
out={}
for role,frame in [('SEND',305),('ECHO',314)]:
 o=bpy.data.objects[f'DW 1 {role} front0 core'];key=o.data.shape_keys.key_blocks.get('Frame'+str(frame));assert key
 coords=[o.matrix_world@p.co for p in key.data];origin=sum(coords,Vector())/len(coords);d=Vector((origin.x,origin.y,0)).normalized();u=Vector((0,0,1));v=d.cross(u).normalized()
 # Remove the packet's travel position while retaining the actual S02 fan shape.
 center=sum(coords,Vector())/len(coords);w0=(center-origin).dot(d)
 local=[[(p-origin).dot(u),(p-origin).dot(v),(p-origin).dot(d)-w0] for p in coords]
 out[role]=dict(source_object=o.name,source_frame=frame,source_color=list(o.data.materials[0].diffuse_color),bevel=o.data.bevel_depth,shape=local,source_propagation=list(d),extent=[max(p[i] for p in local)-min(p[i] for p in local) for i in range(3)])
(B/'Records/Section2-front-shapes.json').write_text(json.dumps(out,indent=2));print(json.dumps({k:{x:y for x,y in v.items() if x!='shape'} for k,v in out.items()},indent=2))

