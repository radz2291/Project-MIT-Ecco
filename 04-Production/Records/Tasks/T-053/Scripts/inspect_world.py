import bpy,json,pathlib,math
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[5]
OUT=ROOT/'04-Production/Records/Tasks/T-053/Evidence'
sources=json.loads((ROOT/'04-Production/Records/Tasks/T-050/sources.json').read_text())
report={}
for item in sources:
 if item['id'] not in ['WORLD','FORMATION','CASED-FORMATION','CASING','S02','S03','S06']:continue
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/item['native']),load_ui=False)
 s=bpy.context.scene;s.frame_set(300 if item['id']=='S02' else s.frame_current)
 obs=[]
 for o in s.objects:
  if o.type!='MESH':continue
  if item['id'].startswith('S') and not any(x in o.name.lower() for x in ['authority','geological wall retained','ground','earth','strat','formation']):continue
  p=[o.matrix_world@v.co for v in o.data.vertices]
  obs.append(dict(name=o.name,vertices=len(p),bounds=[[min(v[i] for v in p),max(v[i] for v in p)] for i in range(3)] if p else [],matrix=[list(r) for r in o.matrix_world],materials=[m.name for m in o.data.materials if m],modifiers=[m.type for m in o.modifiers],custom={k:str(v) for k,v in o.items()}))
 cams=[]
 if s.camera:
  for f in sorted(set([s.frame_start,s.frame_end,*range(s.frame_start,s.frame_end+1,24)])):
   s.frame_set(f);o=s.camera;cams.append(dict(frame=f,matrix=[list(r) for r in o.matrix_world],lens=o.data.lens,clip=[o.data.clip_start,o.data.clip_end],type=o.data.type))
 report[item['id']]=dict(units=s.unit_settings.scale_length,objects=obs,cameras=cams,collections=[c.name for c in bpy.data.collections])
OUT.joinpath('world-source-inspection.json').write_text(json.dumps(report,indent=2))
print('WORLD_INSPECTION_SAVED')
