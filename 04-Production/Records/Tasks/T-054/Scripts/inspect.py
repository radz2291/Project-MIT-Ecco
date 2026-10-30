import bpy,json
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054'
sources=json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text())
out={}
for src in sources:
 if src['id'] not in ['S02','S03','S06']:continue
 bpy.ops.wm.open_mainfile(filepath=str(R/src['native']),load_ui=False)
 obs=[]
 for o in bpy.data.objects:
  if not any(k in o.name.lower() for k in ['earth','ground','strata','survey grid','one wall','indexed','reconstructed wall','rock sectional','fixed borehole']):continue
  bb=[o.matrix_world@Vector(c) for c in o.bound_box]
  mats=[]
  for m in o.data.materials if o.data and hasattr(o.data,'materials') else []:
   if not m:continue
   mats.append({'name':m.name,'diffuse':list(m.diffuse_color),'animated':bool(m.animation_data),'nodes':[(n.name,n.type) for n in m.node_tree.nodes] if m.node_tree else []})
  obs.append({'name':o.name,'bounds':[[min(v[i] for v in bb),max(v[i] for v in bb)] for i in range(3)],'verts':len(o.data.vertices) if o.type=='MESH' else None,'polys':len(o.data.polygons) if o.type=='MESH' else None,'materials':mats[:12],'material_count':len(mats),'modifiers':[(m.name,m.type,m.node_group.name if m.type=='NODES' and m.node_group else '') for m in o.modifiers]})
 out[src['id']]=obs
(T/'Evidence/selected-inspection.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))
