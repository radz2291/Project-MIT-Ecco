"""Read-only background inspection of frozen B101 v001; no file save or scene edit."""
import bpy,json,math,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
o=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH']
bpy.context.view_layer.update()
points=[o.matrix_world@v.co for v in o.data.vertices]
closures=bpy.data.collections.get('ECCO_TEMPORARY_CLOSURES')
if closures:
    points += [obj.matrix_world@v.co for obj in closures.objects if obj.type=='MESH' for v in obj.data.vertices]
result={'blender':bpy.app.version_string,'file':str(Path(bpy.data.filepath).relative_to(ROOT.parent)).replace('\\','/'),
        'sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),
        'housing_vertices':len(o.data.vertices),'envelope_vertices_including_closures':len(points),'housing_dimensions_m':list(o.dimensions),
        'maximum_axis_diameter_m':2*max(math.hypot(v.y,v.z) for v in points),
        'axis':'source X; not certified pin/box datum',
        'closures_included':len(closures.objects) if closures else 0,
        'status':'Measurement only. O04/O14 unresolved; this does not validate T5 closure placement.'}
version='v002' if closures else 'v001'
(ROOT/f'Records/Tasks/T-006/Evidence/product-inspection_{version}.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result))
