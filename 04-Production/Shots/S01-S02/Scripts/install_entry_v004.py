import bpy,json,hashlib
from pathlib import Path
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';B=R/'04-Production/Shared/Assets/Environment/Surface';s=bpy.context.scene
p=Q/'Scenes/S01-S02_production_v004.blend';assert not p.exists()
for lib in list(bpy.data.libraries):
 if Path(bpy.path.abspath(lib.filepath)).name=='Surface_descent_v007.blend':lib.filepath=str(B/'Surface_descent_v008.blend');lib.reload()
d=json.loads((B/'Surface_interface_v008.json').read_text());(Q/'Notes/surface_v008_build.json').write_text(json.dumps(d,indent=2))
s.name='S01-S02 continuous entry trial v004';s.frame_set(93)
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p));result={'saved':str(p),'restored_objects':len(d['restored_objects'])}
