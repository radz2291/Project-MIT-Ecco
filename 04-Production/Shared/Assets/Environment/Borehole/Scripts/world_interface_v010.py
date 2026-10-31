# ECCO_RUNTIME_PATH_MIGRATION_20261031
"""Select physical geometry without sharing shot cameras, measured samples or animation."""
import bpy,json
from pathlib import Path
from mathutils import Matrix

def link_variant(asset_root,collection_name,placement=None,name='World physical instance'):
    asset_root=Path(asset_root)
    path=asset_root/'Environment/Borehole/World_environment_v010.blend'
    with bpy.data.libraries.load(str(path),link=True) as (available,loaded):
        if collection_name not in available.collections:raise ValueError(collection_name)
        loaded.collections=[collection_name]
    obj=bpy.data.objects.new(name,None)
    obj.instance_type='COLLECTION';obj.instance_collection=loaded.collections[0]
    bpy.context.scene.collection.objects.link(obj)
    if placement is not None:obj.matrix_world=Matrix(placement)
    obj['variant']=collection_name
    obj['rule']='Use exactly one competing physical wall at each placement; visibility and placement are local.'
    return obj

def s02_placement(asset_root):
    return json.loads((Path(asset_root)/'Environment/Borehole/World_interface_v010.json').read_text())['canonical_to_s02']
