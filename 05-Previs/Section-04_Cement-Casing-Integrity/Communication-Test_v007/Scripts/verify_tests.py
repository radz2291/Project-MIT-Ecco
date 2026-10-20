import bpy,json,math,hashlib,bmesh
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];R=B.parents[2]
baseline=R/'05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v006/Scenes/S04_cinematic-previs_v006.blend'
out={}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(baseline),use_scripts=False,load_ui=False)
fluid=next(o for o in bpy.context.scene.objects if 'Stationary organic fluid' in o.name)
bm=bmesh.new();bm.from_mesh(fluid.data);closed=all(e.is_manifold for e in bm.edges);bm.free()
rad=[math.hypot((fluid.matrix_world@v.co).y,(fluid.matrix_world@v.co).z) for v in fluid.data.vertices]
assert closed and min(rad)>.1698625-1e-6 and max(rad)<.22225+1e-6
out['original_channel']={'closed_manifold':closed,'radial_bounds_m':[min(rad),max(rad)],'relationship':'Outside fixed steel exterior, within cement annulus; fixed display section is a subset of this source volume'}
for c in 'BCD':
 folder=B/('Test-2_Inner-Wear' if c=='D' else 'Test-1_Matched-Response');p=folder/'Scenes'/f'S04_{c}_communication_v007.blend'
 bpy.ops.wm.open_mainfile(filepath=str(p),use_scripts=False,load_ui=False);s=bpy.context.scene
 libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
 assert all(x['path'].startswith('//') and x['exists'] for x in libs)
 source=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];display=bpy.data.objects['ACTUAL STEEL INNER SURFACE - fixed source section']
 coords={tuple(v.co) for v in source.data.vertices};assert all(tuple(v.co) in coords for v in display.data.vertices)
 assert not display.modifiers and not display.animation_data
 changes=[]
 for f in (1,32,72,120):
  s.frame_set(f);bpy.context.view_layer.update();changes.append((tuple(s.camera.location),tuple(s.camera.rotation_quaternion),tuple(bpy.data.objects['WORLD_CONTROL'].items())))
 assert all(x==changes[0] for x in changes)
 radii=[math.hypot(v.co.y,v.co.z) for v in source.data.vertices]
 assert abs(max(radii)-.1698625)<1e-6
 out[c]={'libraries':libs,'static_camera_and_control':True,'retained_steel_vertices_exact_source_subset':True,'no_display_modifiers':True,'outer_radius_m':max(radii),'native_sha256':digest(p)}
a=json.loads((B/'Records/camera-B.json').read_text());b=json.loads((B/'Records/camera-C.json').read_text())
delta=max(abs(x-y) for k in ['relative_eye','relative_target'] for x,y in zip(a[k],b[k]));assert delta<1e-6 and a['lens']==b['lens'] and a['actual_steel_contact_visible'] and b['actual_steel_contact_visible']
out['matched_composition']={'max_sensor_relative_camera_difference_m':delta,'same_lens':a['lens'],'actual_contact_visible_both':True,'same_send_contact_receive_seconds':[.6,1.2,1.8]}
out['source_hashes']={str(p.relative_to(R)):digest(p) for p in [baseline,R/'05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend',R/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend']}
(B/'Records/verification.json').write_text(json.dumps(out,indent=2));print('VERIFIED B C D')
