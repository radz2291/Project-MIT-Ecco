import bpy, json
from pathlib import Path
p=Path(__file__).resolve().parents[3]
with bpy.data.libraries.load(str(p/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'),link=False) as (a,b):
    b.collections=['WELL_ASSEMBLY_v003']
bpy.context.scene.collection.children.link(b.collections[0])
r=bpy.data.objects['ASSEMBLY_CONTROL']
for k,v in dict(travel_m=2.07,rotation_rad=0.,variant=1,cutaway=0,show_open=1,show_casing=0,show_cement=0,show_hardware=1,show_proxies=0).items(): r[k]=v
r.update_tag();bpy.context.view_layer.update()
d={'refs':[{ 'name':o.name,'xyz':list(o.matrix_world.translation)} for o in bpy.data.objects if o.name.startswith('ECCO_SENSOR_REF_')], 'instances':[{ 'name':o.name,'loc':list(o.location),'type':o.type,'instance':o.instance_collection.name if o.instance_collection else None} for o in bpy.data.objects if o.instance_collection], 'libraries':[l.filepath for l in bpy.data.libraries]}
(Path(__file__).parent/'source-inspection.json').write_text(json.dumps(d,indent=2))
print(json.dumps(d))
