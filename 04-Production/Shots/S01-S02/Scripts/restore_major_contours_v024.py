"""Restore the original visible major-ring weight on the reveal-derived branch."""
import bpy,json,datetime,hashlib
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v023.blend')
out=Q/'Scenes/S01-S02_production_v024.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_major_contours_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
ob=bpy.data.objects['Shared fine measurement display'];wrapper=ob.modifiers[0].node_group.copy();ob.modifiers[0].node_group=wrapper;node=next(n for n in wrapper.nodes if n.type=='GROUP');g=node.node_tree.copy();node.node_tree=g
old=bpy.data.objects['ONE GRID - every fourth contour'];material=old.data.materials[0]
sm=next(n for n in g.nodes if n.type=='SET_MATERIAL' and n.inputs['Material'].default_value==material)
ctm=sm.inputs['Geometry'].links[0].from_node;profile=ctm.inputs['Profile Curve'].links[0].from_node
previous=profile.inputs['Radius'].default_value;profile.inputs['Radius'].default_value=old.data.bevel_depth
ob['Major contour radius m']=old.data.bevel_depth;ob['Major contours']='Original 2mm pale-cyan ring weight restored; generated from revealed wall at0.24m spacing.'
bpy.context.scene.frame_set(756);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/major_contours_v024.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v023.blend','original_reference_object':old.name,'previous_radius_m':previous,'restored_radius_m':old.data.bevel_depth,'material':material.name,'rgba':list(material.diffuse_color),'spacing_m':.24,'scope':'Only major contour curve profile thickness restored. Old independently timed curve objects stay disabled.','preserved':['v023gentlerevealvisible520','laterupwardsweep/camera','sixapprovedscans/blue/continuation/closedwide','finaldisplaycleanup','sharedmasters']},indent=2))
result={'saved':str(out),'radius_before':previous,'radius_restored':old.data.bevel_depth}
