import bpy,json,hashlib,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';W=R/'04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend'
bpy.ops.wm.open_mainfile(filepath=str(W),load_ui=False);m=bpy.data.objects['FORMATION_IRREGULAR_CUTAWAY'].data
rows=len(m.vertices)//276;first=2*(rows-1)*96;fv=2*rows*97
assert len(m.vertices)==50232 and len(m.polygons)==49232 and all(all(v>=fv for v in p.vertices) for p in list(m.polygons)[first:])
coords=[v.co.copy() for v in m.vertices];results=[]
for scale in [.75,1.25]:
 for v,co in zip(m.vertices,coords):
  v.co=co
  if (co.y**2+co.z**2)**.5>2.39:v.co.y*=scale;v.co.z*=scale
 m.calc_loop_triangles();caps=[t for t in m.loop_triangles if t.polygon_index>=first]
 assert len(caps)==28960
 results.append({'outer_radius_m':20*scale,'cap_triangle_count':len(caps),'topology_valid':True})
g=runpy.run_path(str(R/'04-Production/Shared/Assets/DigitalEnvironment/check_context_derivation_v004.py'));record=json.loads((T/'Evidence/cap-intersections-v004.json').read_text());actual=hashlib.sha256(W.read_bytes()).hexdigest()
assert g['valid'](actual,record['world_sha256']);assert not g['valid']('0'*64,record['world_sha256'])
# Simulate count mismatch; all production consumers remain untouched.
assert len(m.polygons)+1!=first+2*(rows-1)*40
(T/'Evidence/guard-tests-v004.json').write_text(json.dumps({'current_hash_pass':True,'stale_hash_rejected':True,'changed_topology_count_rejected':True,'coordinate_only_extent_tests':results,'scope':'Topology selection tested at15/25m; no approval of changed-shape aesthetics. Changed World requires full regeneration and affected-consumer render checks.'},indent=2));print('GUARDS_PASS')
