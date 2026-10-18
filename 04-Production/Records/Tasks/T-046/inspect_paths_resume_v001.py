import bpy,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];T=ROOT/'04-Production/Records/Tasks/T-046'
bpy.ops.wm.open_mainfile(filepath=str(T/'Scenes/Sensing_reuse_A_v008.blend'),load_ui=False,use_scripts=False)
rows=[]
for l in bpy.data.libraries:
 a=bpy.path.abspath(l.filepath);b=bpy.path.abspath(l.filepath,library=l.parent)
 rows.append(dict(name=l.name,filepath=l.filepath,parent=l.parent.name if l.parent else None,scene_abspath=a,scene_exists=Path(a).exists(),parent_abspath=b,parent_exists=Path(b).exists()))
(T/'Evidence/nested-path-inspection_resume_v001.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
