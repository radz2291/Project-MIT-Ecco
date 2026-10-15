"""Create/reopen a local linked consumer to verify portable collection reference."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';MASTER=ROOT/'Shared/Assets/ECCO/ECCO_master_v001.blend'
if '--verify' not in sys.argv:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    with bpy.data.libraries.load(str(MASTER),link=True,relative=True) as (src,dst):dst.collections=['ECCO_MASTER_v001']
    collection=dst.collections[0]
    bpy.context.scene.collection.children.link(collection)
    bpy.ops.wm.save_as_mainfile(filepath=str(TASK/'Evidence/library-consumer_v001.blend'),relative_remap=True)
else:
    library=next(iter(bpy.data.libraries));collection=bpy.data.collections['ECCO_MASTER_v001']
    result={'relative_path':library.filepath,'resolves':Path(bpy.path.abspath(library.filepath)).resolve()==MASTER.resolve(),'linked_collection':collection.library is not None,'objects':len(collection.all_objects),'has_housing':'ECCO_HOUSING_SOURCE_MESH' in collection.all_objects,'camera_excluded':not any(o.type=='CAMERA' for o in collection.all_objects)}
    result['all_pass']=result['relative_path'].startswith('//') and all(result[k] for k in ['resolves','linked_collection','has_housing','camera_excluded'])
    (TASK/'Evidence/library-check_v001.json').write_text(json.dumps(result,indent=2),encoding='utf-8');assert result['all_pass'],result
    print('LIBRARY_CHECK',result)
