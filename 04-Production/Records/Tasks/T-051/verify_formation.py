"""Independent read-only check of visible deformation on an anchored ribbon."""
import bpy, pathlib, sys, json, hashlib
import numpy as np
ROOT=pathlib.Path(__file__).resolve().parents[4]
args=sys.argv[sys.argv.index('--')+1:]
path=ROOT/args[0]; before=hashlib.sha256(path.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
s=bpy.context.scene; ob=bpy.data.objects['RIBBON_ANCHORED_FORMATION_32_FILAMENTS']
count=len(ob.data.vertices); route=np.empty(count)
ob.data.attributes['route_u'].data.foreach_get('value',route)
samples={}; records=[]; matrices=[]; cameras=[]; optics=[]
for frame in [1,25,50,70,90,120]:
    s.frame_set(frame); dg=bpy.context.evaluated_depsgraph_get()
    ev=ob.evaluated_get(dg); mesh=ev.to_mesh(); co=np.empty(count*3)
    mesh.vertices.foreach_get('co',co); ev.to_mesh_clear(); co=co.reshape(-1,3)
    samples[frame]=co
    matrices.append(np.array(ob.matrix_world)); camera=s.camera.evaluated_get(dg)
    cameras.append(np.array(camera.matrix_world))
    optics.append([camera.data.lens,camera.data.ortho_scale,camera.data.shift_x,camera.data.shift_y])
    records.append({'frame':frame,'geometry_sha256':hashlib.sha256(co.tobytes()).hexdigest(),
                    'height_m':float(np.ptp(co[:,2]))})
flat=samples[1]; full=samples[50]; delta=full[:,2]-flat[:,2]
valid=abs(delta)>1e-7
near=valid & (abs(route-.25)<.02); far=valid & (abs(route-.85)<.02)
growth=np.zeros(count); growth[valid]=(samples[25][valid,2]-flat[valid,2])/delta[valid]
ends=(route<1e-6)|(route>1-1e-6)
libs=[{'path':lib.filepath,'exists':pathlib.Path(bpy.path.abspath(lib.filepath)).exists()} for lib in bpy.data.libraries]
checks={
 'evaluated_geometry_changes':len({x['geometry_sha256'] for x in records})>3,
 'object_transform_fixed':all(np.allclose(m,matrices[0],atol=1e-8) for m in matrices),
 'route_xy_fixed':all(np.array_equal(co[:,:2],flat[:,:2]) for co in samples.values()),
 'endpoints_fixed_within_0_1_micrometre':all(np.allclose(co[ends],flat[ends],atol=1e-7,rtol=0) for co in samples.values()),
 'starts_flat':float(np.ptp(flat[:,2]))<.0001,
 'settles_to_identical_flat_end':np.array_equal(samples[120],flat),
 'progressive_not_uniform_growth':bool(np.median(growth[near])>.7 and abs(np.median(growth[far]))<.05),
 'full_height_matches_40mm_face':abs(float(np.ptp(full[:,2]))/.0400390625-1)<.01,
 'response_smaller_than_full':.01<float(np.ptp(samples[90][:,2]))/float(np.ptp(full[:,2]))<.7,
 'review_camera_fixed':all(np.allclose(c,cameras[0],atol=1e-8) for c in cameras),
 'review_camera_optics_fixed':all(np.allclose(v,optics[0],atol=1e-8) for v in optics),
 'relative_libraries_resolve':all(l['path'].startswith('//') and l['exists'] for l in libs),
 'saved_file_unchanged':hashlib.sha256(path.read_bytes()).hexdigest()==before,
}
record={'candidate':args[0],'sha256':before,'range':[s.frame_start,s.frame_end],
 'fps':s.render.fps,'records':records,'near_growth_f25':float(np.median(growth[near])),
 'far_growth_f25':float(np.median(growth[far])),
 'max_endpoint_deviation_m':max(float(np.max(abs(co[ends]-flat[ends]))) for co in samples.values()),
 'libraries':libs,'checks':checks,'all_pass':all(checks.values()),
 'scope':'Artistic review animation; not calibrated acoustic motion or original shot timing.'}
(ROOT/args[1]).write_text(json.dumps(record,indent=2))
print(json.dumps({'checks':checks,'all_pass':record['all_pass']}))
if not record['all_pass']:raise SystemExit(1)
