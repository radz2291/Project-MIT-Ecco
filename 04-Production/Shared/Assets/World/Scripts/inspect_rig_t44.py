import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5]
FOLDER=Path(r'C:\Users\RZ1\Desktop\RZ\261006-Rolladice\IntoTheInvisible')
out=[]
for name in ['IntoTheInvisible_Shot01.blend','IntoTheInvisible_Materials.blend']:
 p=FOLDER/name;h=hashlib.sha256(p.read_bytes()).hexdigest();bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 rows=[]
 for c in bpy.data.collections:
  vs=[o.matrix_world@Vector(v) for o in c.all_objects if o.type=='MESH' for v in o.bound_box]
  rows.append(dict(name=c.name,objects=len(c.all_objects),verts=sum(len(o.data.vertices) for o in c.all_objects if o.type=='MESH'),bounds=[[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]] if vs else None))
 out.append(dict(path=str(p),sha256=h,unchanged=h==hashlib.sha256(p.read_bytes()).hexdigest(),collections=rows,objects=[dict(name=o.name,type=o.type,collections=[c.name for c in o.users_collection],vertices=len(o.data.vertices) if o.type=='MESH' else 0) for o in bpy.data.objects],images=[dict(name=i.name,path=i.filepath,packed=bool(i.packed_file)) for i in bpy.data.images if i.source=='FILE'],libraries=[l.filepath for l in bpy.data.libraries]))
p=ROOT/'04-Production/Records/Tasks/T-044/Evidence/rig-source-inspection_v001.json';p.write_text(json.dumps(out,indent=2),encoding='utf-8');print('RIG_INSPECT_PASS')
