"""Independent saved-scene checks of packet direction and acquisition ordering."""
import bpy, pathlib, json, hashlib, numpy as np
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=pathlib.Path(__file__).resolve().parents[4]
rel='04-Production/Shared/Assets/Acoustics/RibbonWaveform_v012/S02_causal-waveform-review_v012.blend'
path=ROOT/rel; digest=hashlib.sha256(path.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
s=bpy.context.scene
timeline=json.loads((ROOT/'04-Production/Records/Tasks/T-056/causal-timeline_v012.json').read_text())
a=Vector(timeline['sensor_world_m']); b=Vector(timeline['wall_world_m'])
axis=np.array((b-a).normalized()); width=timeline['packet_width_fraction']
names=['OUTGOING_FINITE_PACKET','RETURN_FINITE_PACKET']
cues=['EMISSION_ON_SAME_SENSOR','EXACT_WALL_CONTACT_RIPPLE','SAME_SENSOR_RECEIPT','POST_RECEIPT_WALL_MEASUREMENT']
frames=[1,17,19,25,30,36,37,40,42,47,49,54,62,65,67,72,84,90,100,103,114,118,123,124,168]
records={}; baseline={}; matrix_baseline={}; domain_fixed=True; objects_fixed=True
def cue_visible(name):
    ob=bpy.data.objects[name]
    em=next(n for n in ob.data.materials[0].node_tree.nodes if n.type=='EMISSION')
    return bool(not ob.hide_render and em.inputs[1].default_value>1e-5)
for frame in frames:
    s.frame_set(frame); dg=bpy.context.evaluated_depsgraph_get(); state={}
    for name in names:
        ob=bpy.data.objects[name]; n=len(ob.data.vertices); route=np.empty(n)
        ob.data.attributes['route_u'].data.foreach_get('value',route)
        ev=ob.evaluated_get(dg); mesh=ev.to_mesh(); co=np.empty(n*3)
        mesh.vertices.foreach_get('co',co); ev.to_mesh_clear(); co=co.reshape(-1,3)
        axial=co@axis; mat=np.array(ob.matrix_world)
        if name not in baseline:baseline[name]=axial; matrix_baseline[name]=mat
        domain_fixed &= bool(np.allclose(axial,baseline[name],atol=1e-7,rtol=0))
        objects_fixed &= bool(np.allclose(mat,matrix_baseline[name],atol=1e-8,rtol=0))
        nt=ob.data.materials[0].node_tree
        head=nt.nodes['Causal_front_route_coordinate'].outputs[0].default_value
        travel=1-route if name.startswith('RETURN') else route
        phase=(head-travel)/width; active=(phase>0)&(phase<1)
        centroid=None; projected=None; support=None
        if active.any():
            centroid=float(route[active].mean()); support=[float(route[active].min()),float(route[active].max())]
            p=ob.matrix_world@Vector(co[active].mean(axis=0))
            projected=list(world_to_camera_view(s,s.camera,p))
        state[name]={'visible_support':support,'centroid_u':centroid,'projected_centroid':projected,
                     'height_m':float(np.ptp(co[active,2])) if active.any() else 0,
                     'geometry_sha256':hashlib.sha256(co.tobytes()).hexdigest()}
    state['cues']={name:cue_visible(name) for name in cues}
    records[frame]=state
out=lambda f:records[f][names[0]]
echo=lambda f:records[f][names[1]]
cv=lambda f,n:records[f]['cues'][n]
lib=[{'path':x.filepath,'exists':pathlib.Path(bpy.path.abspath(x.filepath)).exists()} for x in bpy.data.libraries]
same_face=np.allclose(bpy.data.objects[cues[0]].location,bpy.data.objects[cues[2]].location,atol=1e-8,rtol=0)
same_wall=np.allclose(bpy.data.objects[cues[1]].location,bpy.data.objects[cues[3]].location,atol=1e-8,rtol=0)
checks={
 'packet_objects_stationary':objects_fixed,
 'axial_route_coordinates_fixed':domain_fixed,
 'geometry_really_changes':len({out(f)['geometry_sha256'] for f in frames})>5,
 'empty_gap_at_start_and_end':all(records[f][n]['visible_support'] is None for f in [1,168] for n in names),
 'outgoing_begins_at_sensor':out(19)['visible_support'][1]<.05,
 'outgoing_moves_sensor_to_wall':out(25)['centroid_u']<out(36)['centroid_u']<out(47)['centroid_u'],
 'outgoing_moves_right_to_left_on_screen':out(25)['projected_centroid'][0]>out(36)['projected_centroid'][0]>out(47)['projected_centroid'][0],
 'no_wall_response_before_contact':not any(cv(f,cues[1]) for f in frames if f<48),
 'wall_response_visible_at_contact':cv(54,cues[1]),
 'no_echo_before_wall_interaction':all(echo(f)['visible_support'] is None for f in frames if f<66),
 'echo_begins_at_wall':echo(67)['visible_support'][0]>.95,
 'echo_moves_back_to_sensor':echo(72)['centroid_u']>echo(84)['centroid_u']>echo(100)['centroid_u'],
 'echo_moves_left_to_right_on_screen':echo(72)['projected_centroid'][0]<echo(84)['projected_centroid'][0]<echo(100)['projected_centroid'][0],
 'same_sensor_emits_and_receives':bool(same_face),
 'receipt_cue_not_early':not any(cv(f,cues[2]) for f in frames if f<102),
 'echo_reaches_sensor_with_receipt_cue':echo(103)['visible_support'][0]<1e-6 and cv(114,cues[2]),
 'measurement_only_after_complete_reception':all(not cv(f,cues[3]) for f in frames if f<124) and echo(118)['visible_support'] is None and cv(124,cues[3]),
 'measurement_at_same_wall_spot':bool(same_wall),
 'outgoing_reaches_face_height':abs(out(37)['height_m']/.0400390625-1)<.02,
 'echo_smaller_than_outgoing':.4<echo(90)['height_m']/out(37)['height_m']<.6,
 'relative_links_resolve':all(x['path'].startswith('//') and x['exists'] for x in lib),
 'saved_candidate_unchanged':hashlib.sha256(path.read_bytes()).hexdigest()==digest,
}
result={'candidate':rel,'sha256':digest,'checks':checks,'all_pass':all(checks.values()),'samples':records,
        'libraries':lib,'scope':'Illustrative causal review, not calibrated acoustic propagation.'}
(ROOT/'04-Production/Records/Tasks/T-051/Evidence/causal-v012-independent.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'checks':checks,'all_pass':result['all_pass']}))
if not result['all_pass']:raise SystemExit(1)
