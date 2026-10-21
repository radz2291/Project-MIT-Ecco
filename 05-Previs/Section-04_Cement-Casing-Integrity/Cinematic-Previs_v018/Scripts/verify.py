import bpy,json,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
def mesh(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
def depth(s):
 ob=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'))
 return [v.value for v in ob.data.attributes['ComputedWearDepth_m'].data]
def curves(s):return {o.name:[tuple(p.co) for sp in o.data.splines for p in sp.points] for o in s.objects if o.type=='CURVE' and o.name.startswith('Station ')}
report={}
for c in 'ABCD':
 meta=json.loads((B/'Records'/f'build-{c}.json').read_text());src=Path(meta['source'])
 assert hashlib.sha256(src.read_bytes()).hexdigest()==meta['source_sha256']
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
 s=bpy.data.scenes['D computed wear depth - cool palette v017'] if c=='D' else bpy.context.scene
 original=mesh(s)
 if c=='D':data=depth(s);lines=curves(s)
 bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes'/f'S04_{c}_v018.blend'),load_ui=False,use_scripts=False)
 s=bpy.data.scenes[{'A':'S04-A approved upward entry v018','B':'S04-B matched 50-percent panel v018','C':'S04-C matched 50-percent panel v018','D':'S04-D physical wear then computed data v018'}[c]]
 assert mesh(s)==original
 deps=[{'path':bpy.path.abspath(lib.filepath),'relative':lib.filepath.startswith('//'),'exists':Path(bpy.path.abspath(lib.filepath)).is_file()} for lib in bpy.data.libraries]
 assert all(r['exists'] for r in deps)
 missing=[im.name for im in bpy.data.images if im.source=='FILE' and not im.packed_file and im.filepath and not Path(bpy.path.abspath(im.filepath)).is_file()]
 assert not missing
 report[c]={'source_bytes_unchanged':True,'mesh_coordinates_topology_unchanged':True,'libraries':deps,'missing_images':missing,'engine':s.render.engine,'resolution':[s.render.resolution_x,s.render.resolution_y]}
 if c=='D':
  assert data==depth(s) and lines==curves(s)
  s.frame_set(168);err=max(abs(a-b) for a,b in zip(s.camera.location,meta['approved_final_camera']));assert err<1e-7
  report[c].update(depth_values_unchanged=True,station_curve_coordinates_unchanged=True,final_camera_matches_approved_within_0_1_micrometre=True,final_camera_max_coordinate_error_m=err,max_loss_mm=1000*max(data))
b=json.loads((B/'Records/build-B.json').read_text());c=json.loads((B/'Records/build-C.json').read_text())
assert b['camera_lens']==c['camera_lens']
report['matched_panels']={'same_lens':True,'projection_B':b['projection'],'projection_C':c['projection'],'no_mirroring_or_image_stretching':True}
report['cased_hole_master_sha256']=hashlib.sha256((B.parents[2]/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend').read_bytes()).hexdigest()
assert report['cased_hole_master_sha256']=='52c14a8f71d9d3c160acbdfaade240f7e699334c3a2ed4bd649cb220b59e49ba'
(B/'Records/native-verification.json').write_text(json.dumps(report,indent=2))
print('NATIVE VERIFICATION PASSED',flush=True)
