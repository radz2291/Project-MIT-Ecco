"""Read-only saved-scene inspection; never saves or modifies the source file."""
import bpy, json, os, sys
from pathlib import Path
from mathutils import Vector
s = bpy.context.scene
objects = []
for o in s.objects:
    points = [o.matrix_world @ Vector(v) for v in o.bound_box] if o.type == 'MESH' else []
    objects.append(dict(name=o.name, type=o.type, dimensions=list(o.dimensions),
        location_world=list(o.matrix_world.translation), scale=list(o.scale),
        bounds_world=[[min(p[i] for p in points) for i in range(3)], [max(p[i] for p in points) for i in range(3)]] if points else None,
        vertices=len(o.data.vertices) if o.type=='MESH' else None,
        parent=o.parent.name if o.parent else None,
        custom_properties={k:str(o[k]) for k in o.keys()},
        animated=bool(o.animation_data), modifiers=[m.type for m in o.modifiers]))
result = dict(file=bpy.data.filepath, blender=bpy.app.version_string,
    units=dict(system=s.unit_settings.system, scale_length=s.unit_settings.scale_length, length_unit=s.unit_settings.length_unit),
    frames=[s.frame_start,s.frame_end], fps=s.render.fps/s.render.fps_base,
    camera=s.camera.name if s.camera else None, objects=objects,
    images=[dict(name=i.name,path=i.filepath,packed=bool(i.packed_file),exists=os.path.exists(bpy.path.abspath(i.filepath))) for i in bpy.data.images if i.source=='FILE'],
    libraries=[dict(path=l.filepath,exists=os.path.exists(bpy.path.abspath(l.filepath))) for l in bpy.data.libraries])
Path(sys.argv[sys.argv.index('--')+1]).write_text(json.dumps(result,indent=2),encoding='utf-8')
