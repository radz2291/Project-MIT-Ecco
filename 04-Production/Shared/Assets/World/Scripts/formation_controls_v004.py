"""T44 connected BHA successor, preserved environment and local world controls."""
import bpy
from pathlib import Path
from formation_controls_v003 import create_world as create_previous
from continuation_controls_v001 import attach_continuation

def create_world(asset_dir):
 root,ctrl,instances=create_previous(asset_dir)
 lib=next(l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).name=='BHA_film_v006.blend')
 lib.filepath=str(Path(asset_dir)/'BHA/BHA_film_v007.blend');lib.reload()
 continuation,parts,endpoint=attach_continuation(asset_dir,instances['WORLD_HARDWARE'])
 instances.update(parts)
 ctrl['interface']='v004; BHAv007 with local UPHOLE_CONTINUATION_CONTROL.length_m/show; environmentv009 and existing controls unchanged'
 ctrl.update_tag();bpy.context.view_layer.update();return root,ctrl,instances
