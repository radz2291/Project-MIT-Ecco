import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(BASE/'Scenes/B202_measured-envelope_master_v008.blend'),link=False) as (src,dst):dst.collections=['B202_MEASURED_ENVELOPE_v008']
bpy.context.scene.collection.children.link(dst.collections[0]);c=bpy.data.objects['B202_CONTROL'];c['show_tool']=1;c['travel_m']=2.1;c['rotation_rad']=.3;c.update_tag();bpy.context.view_layer.update()
checks=[]
checks.append({'check':'appended hardware/sensors follow remapped controller','pass':all(abs(bpy.data.objects[f'B202_SENSOR_REF_{i:02d}'].matrix_world.translation.x-2.83)<1e-5 for i in range(1,4))})
deps=[]
for o in bpy.context.scene.objects:
    if o.animation_data:
        for d in o.animation_data.drivers:
            for v in d.driver.variables:deps.extend(t.id for t in v.targets if t.id)
checks.append({'check':'appended object drivers remap to local controller','pass':len(deps)>0 and all(x==c for x in deps)})
checks.append({'check':'appended relative product source resolves','pass':all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)})
out={'passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks,'note':'Appended collection tested in fresh unsaved scene; no animation or persistent test consumer created.'};(E/'append-reuse_v008.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert all(x['pass'] for x in checks)
