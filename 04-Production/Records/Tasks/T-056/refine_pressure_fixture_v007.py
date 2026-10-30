import bpy,pathlib,json,os
ROOT=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');OUT=ROOT/'04-Production/Shared/Assets/Acoustics/PressureField_v007';OUT.mkdir(parents=True,exist_ok=True)
s=bpy.context.scene
for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
for name in ['Proof_Key','Proof_Fill']:bpy.data.objects[name].data.energy*=.35
s.world.node_tree.nodes['Background'].inputs[1].default_value*=.5
s.eevee.taa_render_samples=16
ctrl=bpy.data.objects['PRESSURE_MODEL_CONTROL_v005'];ctrl['sample_metadata_json']=(ROOT/'04-Production/Shared/Assets/Acoustics/PressureField_v005/Data/source_pulse.json').read_text();ctrl['fixture_revision']='v007: illumination reduced 1.515 stops, emission unchanged;16samples'
path=OUT/'S02_pressure-field-proof_v007.blend';bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=True)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
bpy.ops.wm.save_as_mainfile(filepath=str(path))
