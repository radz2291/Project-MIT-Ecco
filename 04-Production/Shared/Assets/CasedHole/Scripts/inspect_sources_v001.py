import bpy,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
ASSET=ROOT/'04-Production/Shared/Assets'
OUT=ROOT/'04-Production/Records/Tasks/T-047/Evidence/source-inspection_v001.json'
sources=[ASSET/'BHA/BHA_film_v006.blend',ASSET/'WellAssembly/World_environment_v009.blend',ASSET/'ECCO/ECCO_film_v002.blend']+[ROOT/f'04-Production/Mechanisms/B203/Scenes/B203_{k}_v002.blend' for k in ['retrieval','support','channel','wear']]
rows=[]
for p in sources:
 bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
 objs=[]
 for o in bpy.data.objects:
  if o.library:continue
  if o.type=='MESH':
   v=[o.matrix_world@v.co for v in o.data.vertices];bb=[[min(q[i] for q in v),max(q[i] for q in v)] for i in range(3)] if v else None
  else:bb=None
  objs.append(dict(name=o.name,type=o.type,bounds=bb,location=list(o.location),scale=list(o.scale),props={k:str(v) for k,v in o.items()}))
 rows.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),collections=[c.name for c in bpy.data.collections],objects=objs,libraries=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath)) for l in bpy.data.libraries]))
OUT.write_text(json.dumps(rows,indent=2),encoding='utf8')
print('SOURCE_INSPECTION_SAVED',OUT)
