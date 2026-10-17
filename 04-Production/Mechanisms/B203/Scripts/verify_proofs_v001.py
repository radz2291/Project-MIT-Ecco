"""Fresh-open source, motion and authored geometry checks; no render mutations."""
import bpy,json,math,hashlib
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];PROD=BASE.parents[1];EVID=PROD/'Records/Tasks/T-009/Evidence'
result=[]
for name in ('retrieval','support','channel','wear'):
    path=BASE/f'Scenes/B203_{name}_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(path))
    s=bpy.context.scene;assert s.frame_end==144 and s.render.fps==24
    row={'case':name,'fresh_open':True,'libraries':[]}
    for lib in bpy.data.libraries:
        absolute=Path(bpy.path.abspath(lib.filepath));assert absolute.is_file() and lib.filepath.startswith('//')
        row['libraries'].append({'relative':lib.filepath,'sha256':hashlib.sha256(absolute.read_bytes()).hexdigest()})
    if name=='retrieval':
        # Evaluate actual instanced ECCO bounds through the dependency graph, including closures.
        s.frame_set(144);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
        points=[]
        from mathutils import Vector
        for inst in deps.object_instances:
            if inst.is_instance and inst.object.type=='MESH' and inst.object.name!='ECCO_CUTTER_PREVIEW_ONLY':
                points.extend(inst.matrix_world@v.co for v in inst.object.data.vertices)
        assert points
        maxr=max(math.hypot(v.y,v.z) for v in points);xrange=[min(v.x for v in points),max(v.x for v in points)]
        assert maxr<12.515*.0254/2 and xrange[1]<0
        row.update(actual_instance_max_radius_m=maxr,actual_product_x_range=xrange,positive_nominal_clearance_m=12.515*.0254/2-maxr)
    if name=='channel':
        obj=bpy.data.objects['Authored_axial_channel'];blue=[p for p in obj.data.polygons if p.material_index==1]
        assert blue
        coords=[obj.data.vertices[v].co for p in blue for v in p.vertices]
        ar=[math.atan2(v.z,v.y) for v in coords];xs=[v.x for v in coords]
        assert max(ar)-min(ar)<1 and max(xs)-min(xs)>2
        row.update(axial_channel=True,angular_span_rad=[min(ar),max(ar)],axial_span_m=[min(xs),max(xs)],map_mask='same axial [-1.2,1.2], angular [.25,.85] bounds; finite mesh/map cell resolution')
    if name=='wear':
        obj=bpy.data.objects['Unchanged_outer_casing'];vs=obj.data.vertices;size=len(vs)//2
        outer=[math.hypot(v.co.y,v.co.z) for v in list(vs)[size:]];inner=[math.hypot(v.co.y,v.co.z) for v in list(vs)[:size]]
        assert max(outer)-min(outer)<1e-6 and max(inner)<min(outer) and max(inner)>min(inner)+.0039
        row.update(outer_radius_range_m=[min(outer),max(outer)],inner_radius_range_m=[min(inner),max(inner)],outside_unchanged=True)
    result.append(row)
(EVID/'fresh-open-verification_v001.json').write_text(json.dumps(result,indent=2))
print('FRESH_OPEN_VERIFICATION_PASS')
