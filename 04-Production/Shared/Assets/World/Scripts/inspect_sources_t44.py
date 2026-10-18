"""T44 read-only native source inspection. Run in background Blender."""
import bpy, json, hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5]
TASK=ROOT/'04-Production/Records/Tasks/T-044'
OUT=TASK/'Evidence/source-inspection_v001.json'
OUT.parent.mkdir(parents=True,exist_ok=True)
records=[]
for rel in ['04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend','04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend']:
 p=ROOT/rel; before=hashlib.sha256(p.read_bytes()).hexdigest()
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 s=bpy.context.scene
 rows=[]
 for o in bpy.data.objects:
  bounds=None
  if o.type=='MESH':
   vs=[o.matrix_world@Vector(v) for v in o.bound_box]
   bounds=[[min(v[k] for v in vs) for k in range(3)],[max(v[k] for v in vs) for k in range(3)]]
  rows.append(dict(name=o.name,type=o.type,parent=o.parent.name if o.parent else None,library=o.library.filepath if o.library else None,location=list(o.location),scale=list(o.scale),bounds=bounds,vertices=len(o.data.vertices) if o.type=='MESH' else 0,materials=[m.name if m else None for m in o.data.materials] if o.type=='MESH' else [],props={k:str(o[k]) for k in o.keys()},instance=o.instance_collection.name if o.instance_collection else None))
 records.append(dict(path=rel,sha256=before,unchanged=before==hashlib.sha256(p.read_bytes()).hexdigest(),units=s.unit_settings.scale_length,objects=rows,collections=[dict(name=c.name,library=c.library.filepath if c.library else None,children=[q.name for q in c.children],objects=[o.name for o in c.objects]) for c in bpy.data.collections],libraries=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath),exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries]))
OUT.write_text(json.dumps(dict(blender=bpy.app.version_string,sources=records),indent=2),encoding='utf-8')
print('T44_INSPECT_PASS',str(OUT),flush=True)
