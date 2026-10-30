import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent
S={s['id']:R/s['native'] for s in json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text())}
out={}
for key in ['SURFACE','SURFACE-ORIGINAL','S01','S02']:
 bpy.ops.wm.open_mainfile(filepath=str(S[key]),load_ui=False)
 s=bpy.context.scene;s.frame_set(1)
 cols=['SURFACE_REUSED_RIG','03_SUBSEA']
 objects=list(bpy.data.collections.get(cols[0] if key=='SURFACE' else cols[1]).all_objects) if key in ['SURFACE','SURFACE-ORIGINAL'] else [o for o in s.objects if not o.library and not o.name.startswith(('Cutaway earth','Opening front','Earth seam','Formation rear','DW','Stored','S02','TEMP'))]
 records=[]
 for o in objects:
  pts=[o.matrix_world@Vector(v) for v in o.bound_box] if o.type=='MESH' else [o.matrix_world.translation]
  records.append({'name':o.name,'type':o.type,'bounds':[[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)],'parent':o.parent.name if o.parent else None,'animation':bool(o.animation_data),'collections':[c.name for c in o.users_collection]})
 out[key]={'objects':records,'units':s.unit_settings.scale_length,'camera':s.camera.name if s.camera else None,'frames':[s.frame_start,s.frame_end]}
(T/'Evidence/source-inspection.json').write_text(json.dumps(out,indent=2))
for k,v in out.items():
 objs=[o for o in v['objects'] if o['type']=='MESH'];print(k,len(objs),'bounds',[[min(o['bounds'][i][0] for o in objs),max(o['bounds'][i][1] for o in objs)] for i in range(3)])
