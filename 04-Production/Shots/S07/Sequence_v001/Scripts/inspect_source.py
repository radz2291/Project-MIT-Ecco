import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1]
R=B.parents[3]
for p in ('Records','Scenes','Cache','Previews','Graphics'): (B/p).mkdir(exist_ok=True)
src=R/'04-Production/Shared/Assets/ECCO/ECCO_film_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(src))
out={'source':str(src),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'collections':[c.name for c in bpy.data.collections],'objects':[]}
for o in bpy.data.objects:
 d={'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale)}
 if o.type=='MESH':
  ps=[o.matrix_world@Vector(v) for v in o.bound_box]
  d.update(vertices=len(o.data.vertices),faces=len(o.data.polygons),bounds=[[min(v[i] for v in ps),max(v[i] for v in ps)] for i in range(3)],materials=[m.name if m else None for m in o.data.materials])
 out['objects'].append(d)
(B/'Records/source-inspection.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
