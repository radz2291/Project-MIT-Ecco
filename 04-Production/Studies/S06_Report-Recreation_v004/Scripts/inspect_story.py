import bpy,json
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_ABC_study_v004.blend'))
for s in bpy.data.scenes:
    print('SCENE',s.name,len(s.objects))
    for o in s.objects:
        if o.type=='MESH' and ('same' in o.name or 'reconstructed' in o.name or 'geometry' in o.name or 'source' in o.name.lower()):
            print(o.name,'scenes',[x.name for x in o.users_scene], 'scale',list(o.scale),'keys',[(k.name,k.value) for k in o.data.shape_keys.key_blocks] if o.data.shape_keys else [])
