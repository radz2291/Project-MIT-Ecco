"""Verify editable appended well rig retains a relative external ECCO library."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006';ASSET=ROOT/'Shared/Assets/WellAssembly'
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(ASSET/'WellAssembly_variants_v003.blend'),link=False) as (src,dst):dst.collections=['WELL_ASSEMBLY_v003']
bpy.context.scene.collection.children.link(dst.collections[0])
rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig['variant']=2;rig['travel_m']=.8;rig['rotation_rad']=.75;rig.update_tag()
bpy.context.view_layer.update()
assert rig.library is None and bpy.data.collections['ECCO_MASTER_v002'].library is not None
out=TASK/'Evidence/editable-consumer_v003.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out));rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig.update_tag();bpy.context.view_layer.update()
checks={'local_editable_rig':rig.library is None,'linked_ECCO_retained':bpy.data.collections['ECCO_MASTER_v002'].library is not None,
        'source_relative_link_resolves':all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries),
        'appended_spiral_selected':not bpy.data.objects['SPIRAL_CUTAWAY'].hide_render,
        'travel_control':abs(bpy.data.objects['ASSEMBLY_TRAVEL_X'].location.x-.8)<1e-6,
        'rotation_control':abs(bpy.data.objects['ASSEMBLY_ROTATION_X'].rotation_euler.x-.75)<1e-6}
result={'all_pass':all(checks.values()),'checks':checks,'consumer_sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
(TASK/'Evidence/editable-consumer-checks_v003.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['all_pass'],result
print('EDITABLE_CONSUMER_PASS',checks)
