"""Update only unpublished demo overview framing and version the World inspection demo."""
import bpy
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');D=R/'04-Production/Shared/Demos'
bpy.context.preferences.filepaths.save_version=0
p=D/'Surface_descent_demo_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
o=bpy.data.objects.get('Main solid building')
if o and not o.library:bpy.data.objects.remove(o,do_unlink=True)
for sc in bpy.data.scenes:
    sc.display.render_aa='8'
    sc.render.resolution_x=450 if sc.name=='World — layered descent' else 800
    sc.render.resolution_y=800 if sc.name=='World — layered descent' else 450
s=bpy.data.scenes['World — layered descent'];c=s.camera;c.location=(370,-720,-460)
c.rotation_euler=(Vector((0,0,-510))-c.location).to_track_quat('-Z','Y').to_euler();c.data.ortho_scale=1160
bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True,relative_remap=False)
previous=D/'World_demo_v001.blend'
if not previous.exists():previous=R/'04-Production/Shared/Archive/2026-10-31/Demos/World_demo_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(previous),load_ui=False)
for l in list(bpy.data.libraries):
    if Path(l.filepath).name=='World_environment_v010.blend':
        l.filepath=str(R/'04-Production/Shared/Assets/Environment/Borehole/World_environment_v011.blend');l.reload()
for t in bpy.data.texts:
    if t.name.startswith('README'):
        txt=t.as_string().replace('Shared/Assets/WellAssembly/World_environment_v010.blend','Shared/Assets/Environment/Borehole/World_environment_v011.blend')
        t.clear();t.write(txt+'\nRegional descent and connected destination are demonstrated in Surface_descent_demo_v002.blend.\n')
out=D/'World_demo_v002.blend'
for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True,relative_remap=False)
bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True,relative_remap=False)
