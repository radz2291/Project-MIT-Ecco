import bpy,pathlib,os,json
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');O=R/'04-Production/Shared/Assets/Acoustics/RibbonWaveform_v010';records=[]
for p in sorted(O.glob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(p))
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(os.path.normpath(bpy.path.abspath(lib.filepath)))
 records.append({'file':str(p),'libraries':[lib.filepath for lib in bpy.data.libraries]});bpy.ops.wm.save_as_mainfile(filepath=str(p))
(R/'04-Production/Records/Tasks/T-056/ribbon-relative-paths_v010.json').write_text(json.dumps(records,indent=2));print(json.dumps(records))
