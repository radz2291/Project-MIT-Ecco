"""Versioned entry presentation: central viewing access through subsea stack.
Illustrative camera opening only, not engineered internal equipment geometry.
Run background with Surface v006 loaded. Original file untouched.
"""
import bpy,json,hashlib,sys
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Surface';Q=R/'04-Production/Shots/S01-S02'
src=B/'Surface_descent_v006.blend';dst=B/'Surface_descent_v007.blend';assert not dst.exists() or '--replace-unpublished' in sys.argv
before=hashlib.sha256(src.read_bytes()).hexdigest();col=bpy.data.collections['SURFACE_RIG_SUBSEA_v004']
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.66,depth=145,location=(0,0,-55));cut=bpy.context.object;cut.name='BUILD_ONLY camera corridor'
changes=[]
for ob in list(col.all_objects):
 if ob.type!='MESH' or not ob.name.startswith(('SUBSEA_BOPStack','SUBSEA_Foundation','SUBSEA_RiserCoupling')):continue
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 m=ob.modifiers.new('Illustrative camera passage radius0.66m','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cut
 # Apply on original mesh before existing bevel/access modifiers; avoid baking them twice.
 while ob.modifiers.find(m.name)>0:bpy.ops.object.modifier_move_up(modifier=m.name)
 bpy.ops.object.modifier_apply(modifier=m.name)
 ob['camera_access']='Authored central viewing passage radius0.66m; not certified internal geometry. Outer equipment retained.';changes.append(ob.name)
bpy.data.objects.remove(cut,do_unlink=True)
col['entry_revision']='v007: central camera-access opening through subsea stack/foundation/couplings; equipment/ocean otherwise retained.'
txt=bpy.data.texts.new('README Surface v007');txt.write('Surface v007 entry presentation. Subsea stack, coupling and foundation have a0.66m central illustrative camera opening to prevent solid caps blocking descent. Not engineered internal equipment. Riser and outer forms retained. No shot actions or camera. Source v006 unchanged. Consumer S01-S02 v003 only; other consumers pinned.\n')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
assert hashlib.sha256(src.read_bytes()).hexdigest()==before
d={'native':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'predecessor_sha256':before,'camera_access_radius_m':.66,'modified_objects':changes,'consumers':['S01-S02 production v003'],'unchanged':'Riser, ocean and all other equipment; no source file overwrite; no other consumer migration.'}
(B/'Surface_interface_v007.json').write_text(json.dumps(d,indent=2));(Q/'Notes/surface_v007_build.json').write_text(json.dumps(d,indent=2));print('SURFACE_V007_READY',len(changes))
