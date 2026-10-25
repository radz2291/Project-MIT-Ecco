import bpy,json
from pathlib import Path
B=Path(__file__).resolve().parents[1];P=B.parents[1]
path=P/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
with bpy.data.libraries.load(str(path),link=False) as (a,b):b.collections=['ECCO_MASTER_v002']
col=b.collections[0];bpy.context.scene.collection.children.link(col)
print(json.dumps([{'name':o.name,'type':o.type,'parent':o.parent.name if o.parent else None,'loc':list(o.location),'scale':list(o.scale),'dims':list(o.dimensions),'hide':o.hide_render,'materials':[m.name for m in o.data.materials] if o.type=='MESH' else []} for o in col.all_objects],indent=2))
