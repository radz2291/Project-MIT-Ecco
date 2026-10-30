import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent/'Evidence'
sources=json.loads((ROOT/'04-Production/Records/Tasks/T-050/sources.json').read_text())
records=[]
for src in sources:
    if src['id'] not in ['ECCO-film','BHA','S07','S05','S02']: continue
    bpy.ops.wm.open_mainfile(filepath=str(ROOT/src['native']))
    s=bpy.context.scene
    records.append({'id':src['id'],'path':src['native'],'units':s.unit_settings.scale_length,'libraries':[{'name':l.name,'path':l.filepath} for l in bpy.data.libraries], 'collections':[c.name for c in bpy.data.collections], 'camera':s.camera.name if s.camera else None,'engine':s.render.engine,'samples':s.eevee.taa_render_samples,'resolution':[s.render.resolution_x,s.render.resolution_y], 'objects':[{'name':o.name,'type':o.type,'library':o.library.filepath if o.library else None,'data':o.data.name if o.data else None,'parent':o.parent.name if o.parent else None,'dimensions':list(o.dimensions),'materials':[m.name if m else None for m in o.data.materials] if hasattr(o.data,'materials') else [],'properties':{k:str(o[k]) for k in o.keys()}} for o in bpy.data.objects if src['id'] in ['ECCO-film','BHA'] or any(k in o.name.lower() for k in ['ecco','housing','satin','metal'])], 'materials':[{'name':m.name,'nodes':[{'name':n.name,'type':n.type,'inputs':{i.name:list(i.default_value) if hasattr(i.default_value,'__len__') else i.default_value for i in n.inputs if hasattr(i,'default_value') and i.type in ['VALUE','RGBA','VECTOR']}} for n in m.node_tree.nodes] if m.node_tree else []} for m in bpy.data.materials if src['id'] in ['ECCO-film','BHA','S07']]})
(OUT/'source-inspection.json').write_text(json.dumps(records,indent=2))
print('INSPECTED',[(r['id'],len(r['objects']),len(r['materials'])) for r in records])
