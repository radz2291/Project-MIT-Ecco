import bpy,pathlib,json,hashlib,math
ROOT=pathlib.Path(__file__).resolve().parents[5];T=ROOT/'04-Production/Records/Tasks/T-053';A=ROOT/'04-Production/Shared/Assets'
sources=json.loads((ROOT/'04-Production/Records/Tasks/T-050/sources.json').read_text());s02=next(x for x in sources if x['id']=='S02')
bpy.ops.wm.open_mainfile(filepath=str(ROOT/s02['native']),load_ui=False)
wall=bpy.data.objects['S02 WALL AUTHORITY full irregular inner surface']
expected=[(v.co.z+735,v.co.x,v.co.y) for v in wall.data.vertices]
radius=[math.hypot(v.co.x,v.co.y) for v in wall.data.vertices]
bpy.ops.wm.open_mainfile(filepath=str(A/'WellAssembly/World_environment_v010.blend'),load_ui=False)
actual=bpy.data.objects['WORLD_S02_IRREGULAR_AUTHORITY_MESH']
error=max(max(abs(v.co[i]-p[i]) for i in range(3)) for v,p in zip(actual.data.vertices,expected));assert error<.00001
checks=[]
for x in sources:
 if x['id'] in ['WORLD','FORMATION','CASED-FORMATION','CASING','S02']:
  h=hashlib.sha256((ROOT/x['native']).read_bytes()).hexdigest();assert h==x['sha256'];checks.append(dict(id=x['id'],hash=h,unchanged=True))
out=dict(exact_authority_vertex_count=len(expected),max_coordinate_error_m=error,source_radius_range_m=[min(radius),max(radius)],inner_mesh_unchanged=True,illustrative_geometry=True,engineering_fit_certified=False,source_checks=checks,missing_libraries=[l.filepath for l in bpy.data.libraries if not pathlib.Path(bpy.path.abspath(l.filepath)).exists()])
(T/'Evidence/geometry-verification.json').write_text(json.dumps(out,indent=2));print('GEOMETRY PASS',error,min(radius),max(radius))
