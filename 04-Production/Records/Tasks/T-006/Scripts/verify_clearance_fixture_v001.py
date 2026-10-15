"""Fresh-open inspection fixture checks, including evaluated collection instances."""
import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
build=json.loads((TASK/'Evidence/clearance-fixture-build_v001.json').read_text())
scene=bpy.context.scene
root=bpy.data.objects['FIXTURE_TRAVEL_X'];rot=bpy.data.objects['FIXTURE_ROTATION_X']
instance=bpy.data.objects['LINKED_ACCEPTED_T5_v002']
libraries=[{'stored':l.filepath,'resolved':bpy.path.abspath(l.filepath),
            'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
rows=[];rmax=0;placement_error=0;closure_counts=[]
for frame in (1,25,49,73,96):
    scene.frame_set(frame);bpy.context.view_layer.update()
    meshes=[{'object':i.object.original,'matrix':i.matrix_world.copy()} for i in bpy.context.evaluated_depsgraph_get().object_instances
            if i.is_instance and i.object.type=='MESH' and
            (i.object.name=='ECCO_HOUSING_SOURCE_MESH' or 'TEMP' in i.object.name or
             any(c.name=='ECCO_TEMPORARY_CLOSURES' for c in i.object.original.users_collection))]
    housing=next(i for i in meshes if i['object'].name=='ECCO_HOUSING_SOURCE_MESH')
    expected=rot.matrix_world @ housing['object'].matrix_world
    placement_error=max(placement_error,max(abs(housing['matrix'][r][c]-expected[r][c])
                                           for r in range(4) for c in range(4)))
    radii=[];axial=[]
    for item in meshes:
        for v in item['object'].data.vertices:
            p=item['matrix']@v.co;radii.append(math.hypot(p.y,p.z));axial.append(p.x)
    max_r=max(radii);rmax=max(rmax,max_r)
    closure_counts.append(len(meshes)-1)
    rows.append({'frame':frame,'rotation_x_rad':rot.rotation_euler.x,'travel_m':root.location.x,
                 'mesh_instances':len(meshes),'max_radius_m':max_r,
                 'axial_bounds_m':[min(axial),max(axial)],
                 'minimum_boundary_gap_m':build['boundary_id_m']/2-max_r})
checks={'saved_fixture_hash_matches_render':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==build['fixture_sha256'],
        'source_hash_matches':all(hashlib.sha256(Path(r['resolved']).read_bytes()).hexdigest()==build['source_sha256'] for r in libraries),
        'relative_links_resolve':bool(libraries) and all(r['stored'].startswith('//') and r['exists'] for r in libraries),
        'nine_closures_in_all_sampled_frames':all(n==9 for n in closure_counts),
        'evaluated_instance_matches_control':placement_error<1e-6,
        'positive_sampled_radial_clearance':all(r['minimum_boundary_gap_m']>0 for r in rows),
        'whole_turn':abs(rows[-1]['rotation_x_rad']-2*math.pi)<1e-6,
        '100mm_test_travel':abs(rows[-1]['travel_m']-.1)<1e-6,
        'swept_axial_bounds_in_fixture':min(r['axial_bounds_m'][0] for r in rows)>=-1e-6 and max(r['axial_bounds_m'][1] for r in rows)<2.500001,
        'render_frames_exist':all((TASK/f'Previews/clearance-frames_v001/frame_{i:04d}.png').is_file() for i in range(1,97))}
result={'all_pass':all(checks.values()),'checks':checks,'frames_checked':rows,
        'matrix_error':placement_error,'libraries':libraries,
        'all_frame_reasoning':'Pure rotation about X preserves radius; X-only travel preserves radius. Sampled evaluated geometry checks these declared interfaces. No eccentric/deviated operating case is certified.',
        'limit':'Published minimum-ID boundary only; no BHA/bit, casing wall, cement, shoe, deviation or selected deployment validation'}
(TASK/'Evidence/clearance-fixture-verification_v001.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['all_pass'],result
print(json.dumps(result,indent=2))
