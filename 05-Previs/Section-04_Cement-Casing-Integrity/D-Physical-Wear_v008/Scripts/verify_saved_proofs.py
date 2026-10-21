import bpy, json, math, os
from pathlib import Path
from mathutils.bvhtree import BVHTree
from mathutils import Vector
B=Path(__file__).resolve().parents[1];rows=[]
for file in sorted((B/'Scenes').glob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(file),load_ui=False,use_scripts=False)
 tag=file.stem.replace('S04_D_','').replace('_v008','');s=bpy.data.scenes['D '+tag+' - physical only']
 o=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'))
 src=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];coords={tuple(v.co) for v in src.data.vertices}
 bv=BVHTree.FromPolygons([v.co for v in src.data.vertices],[list(p.vertices) for p in src.data.polygons]);hit=bv.ray_cast(Vector((-1.5,0,0)),Vector((0,1,0)))[0]
 missing=[bpy.path.abspath(lib.filepath) for lib in bpy.data.libraries if not os.path.isfile(bpy.path.abspath(lib.filepath))]
 row=dict(file=str(file),scene=s.name,retained_vertices_exact=all(tuple(v.co) in coords for v in o.data.vertices),outer_vertices_fixed=all(abs(math.hypot(v.co.y,v.co.z)-.1698625)<2e-8 for v in o.data.vertices if math.hypot(v.co.y,v.co.z)>.167),wear_at_registered_x_minus_1_5_m=hit.y-.1589405,graphics=[x.name for x in s.objects if x.type in ['CURVE','FONT']],modifiers=[m.type for m in o.modifiers],missing_libraries=missing,render_resolution=[s.render.resolution_x,s.render.resolution_y],engine=s.render.engine)
 assert row['retained_vertices_exact'] and row['outer_vertices_fixed'] and not row['graphics'] and not row['modifiers'] and not missing
 rows.append(row)
(B/'Records/fresh-open-verification.json').write_text(json.dumps(rows,indent=2));print('VERIFIED',len(rows),flush=True)
