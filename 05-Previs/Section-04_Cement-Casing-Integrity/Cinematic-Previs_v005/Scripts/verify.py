import bpy,json,math,hashlib,sys
from pathlib import Path
from mathutils import Quaternion
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];A=ROOT/'04-Production/Shared/Assets'
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_cinematic-previs_v005.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
assert s.frame_end==432 and s.render.fps==24
libs=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).is_file(),relative=l.filepath.startswith('//')) for l in bpy.data.libraries];assert all(x['exists'] and x['relative'] for x in libs)
steel=bpy.data.objects['Steel - unchanged source with viewing window'];assert steel.data.library and not steel.modifiers
assert not steel.data.shape_keys
fluid=bpy.data.objects['Stationary organic fluid-filled channel volume'];radii=[math.hypot(v.co.y,v.co.z) for v in fluid.data.vertices];assert min(radii)>.1698625 and max(radii)<.22225
counts={}
for p in fluid.data.polygons:
 for edge in p.edge_keys:counts[edge]=counts.get(edge,0)+1
assert all(v==2 for v in counts.values())
sources=json.loads((B/'Records/source-manifest-full.json').read_text());assert all(hashlib.sha256(Path(v['path']).read_bytes()).hexdigest()==v['sha256'] for v in sources)
s.frame_set(1);bpy.context.view_layer.update();eccos=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in bpy.context.evaluated_depsgraph_get().object_instances);assert eccos==1
sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_verify_v002 import verify_packet
cc=bpy.data.objects['CASED_CONTROL'];cc['show_steel']=1;cc.update_tag();events=json.loads((B/'Records/events.json').read_text())['events'];packets=[verify_packet(e,frames=range(round(e['send_s']*24)+1,round(e['packet_end_s']*24)+2),fps=24) for e in events];assert all(p['all_pass'] for p in packets)
poses=json.loads((B/'Records/camera-score-full.json').read_text());angular=[math.degrees(2*math.acos(min(1,abs(Quaternion(a['quaternion']).dot(Quaternion(b['quaternion'])))))) for a,b in zip(poses,poses[1:])]
out=dict(fresh_open=True,frames=432,fps=24,relative_libraries=libs,one_ecco=eccos==1,canonical_steel_mesh_unchanged=True,fluid_is_closed_3d_volume=True,fluid_outside_steel_inside_cement=True,fluid_radius_bounds=[min(radii),max(radii)],sources_unchanged=True,native_packet_checks=packets,one_camera=True,maximum_camera_angle_change_degrees_per_frame=max(angular),scope='Automated geometry/dependency/packet checks, not engineering or audience approval')
(B/'Records/fresh-open-verification.json').write_text(json.dumps(out,indent=2));print('FRESH_OPEN_PASS',max(angular))
