import bpy,json,os
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_D_physical-comparison_v009.blend'),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only']
missing=[bpy.path.abspath(l.filepath) for l in bpy.data.libraries if not os.path.isfile(bpy.path.abspath(l.filepath))]
d={'comparison_curves':len([o for o in s.objects if o.type=='CURVE']),'missing_libraries':missing,'numeric_text_objects':[o.name for o in s.objects if o.type=='FONT'],'scope':s.get('scope')}
assert not missing and d['comparison_curves']==28 and not d['numeric_text_objects']
(B/'Records/fresh-open.json').write_text(json.dumps(d,indent=2));print('VERIFIED',flush=True)
