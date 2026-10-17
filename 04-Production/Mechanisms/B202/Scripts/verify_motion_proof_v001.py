"""Fresh-open verification of the exact T27 proof; agent checks, not MIT QA."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence'
sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct
M=read_json(E/'replay_manifest_v001.json');C=read_json(B/'acquisition_config_v009.json')
events=read_json(B/'Data/v009/irregular_layers_events_v009.json.gz');ps={p['sample_id']:p for p in reconstruct(events,C)}
bpy.ops.wm.open_mainfile(filepath=str(R/M['scene']));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];checks=[]
def check(name,ok,detail=None):
    checks.append({'check':name,'pass':bool(ok),'detail':detail});assert ok,(name,detail)
check('8 second playable timeline',s.frame_start==1 and s.frame_end==192 and s.render.fps==24)
for path,digest in M['source_hashes'].items():check('source preserved '+path,hashlib.sha256((R/path).read_bytes()).hexdigest()==digest)
for l in bpy.data.libraries:check('relative linked library resolves',l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file(),l.filepath)
check('same sensor receives every replayed event',all(e['sensor_id']==e['receiver_sensor_id'] for e in M['events']))
check('three sensors retained',set(e['sensor_id'] for e in M['events'])=={0,1,2})
cloud=bpy.data.objects['B202_v009_irregular_layers_acquired_points'];original=[tuple(v.co) for v in cloud.data.vertices]
check('point cloud unparented world registration',cloud.parent is None and (cloud.matrix_world.translation.length<1e-9))
check('entire point cloud inverse source binding',len(original)==len(ps) and max((Vector(a)-Vector(p['position_m'])).length for a,p in zip(original,ps.values()))<2e-6)
for seg in M['segments']:
    o=bpy.data.objects[seg['object']]
    check('contour endpoints inverse '+o.name,all((Vector(a)-Vector(ps[e]['position_m'])).length<2e-6 for a,e in zip(seg['positions'],seg['event_ids'])))
samples=[];previous_cutoff=-1.;previous_rot=-100
for row in M['timeline']:
    f=row['frame'];s.frame_set(f);bpy.context.view_layer.update();cutoff=c['event_time_s']
    check(f'frame {f} monotonic replay and clockwise +X rotation',cutoff>=previous_cutoff and c['rotation_rad']>=previous_rot)
    previous_cutoff=cutoff;previous_rot=c['rotation_rad']
    expected={e['id'] for e in M['events'] if e['receipt_frame']<=f}
    available={e['id'] for e in events if e['timestamp_s']<=cutoff}
    check(f'frame {f} no future/missing receipt events',available==expected)
    check(f'frame {f} points stay fixed',all((v.co-Vector(original[i])).length<1e-8 for i,v in enumerate(cloud.data.vertices)))
    visible=[seg for seg in M['segments'] if not bpy.data.objects[seg['object']].hide_render]
    check(f'frame {f} contour follows acquisition',all(set(seg['event_ids'])<=available for seg in visible))
    check(f'frame {f} geometry and amplitude independent',c['show_reconstruction']==1 and c['show_echo_strength']==0 and c['show_interpolated']==0)
    radius=bpy.data.objects['B202_v009_irregular_layers_radius'].evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=radius.to_mesh()
    at=mesh.attributes.get('ready_timestamp_s')
    check(f'frame {f} cached surface has no future means',not len(mesh.vertices) or (at is not None and all(v.value<=cutoff+1e-5 for v in at.data)))
    radius.to_mesh_clear()
    if f in (1,12,28,72,116,136,156,176,192):samples.append({'frame':f,'events':len(available),'contour_segments':len(visible),'tool_travel_m':c['travel_m'],'rotation_rad':c['rotation_rad'],'cutoff':cutoff})
check('no acquisition during axial transfers',all(M['timeline'][f-1]['event_count']==M['timeline'][f-2]['event_count'] for f in list(range(117,137))+list(range(177,193))))
s.frame_set(12);cue=bpy.data.objects['T27_first_event_roundtrip_cue'];check('first event wall contact',(cue.location-Vector(ps[events[0]['id']]['position_m'])).length<2e-6)
s.frame_set(27);check('same-sensor return endpoint',(cue.location-Vector(events[0]['sensor_origin_m'])).length<2e-6)
s.frame_set(192);check('camera has released sensor plane',abs(bpy.data.objects['T27_CAMERA_LOOK_TARGET'].location.x-(c['travel_m']+.730000019))>.35)
check('legacy artistic layers suppressed',all(bpy.data.collections[n].hide_render for n in ('B202_INFORMATION','B202_PHYSICAL_WALL')))
out={'status':'PASS','check_count':len(checks),'checks':checks,'sample_frames':samples,'test10_scope':'First gated 8s proof: actual saved animation timeline, monotonic event cutoff, inverse point persistence, coverage-linked contour and conservative surface reveal. Full sequence / real instrument validity / Radzi visual acceptance not claimed.','scene_sha256':hashlib.sha256((R/M['scene']).read_bytes()).hexdigest()}
(E/'verification_motion-proof_v001.json').write_text(json.dumps(out,indent=2));print('T27_PROOF_VERIFICATION_PASS',len(checks))
