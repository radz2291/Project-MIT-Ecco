"""T27 first gated motion proof; separate consumer, never modifies sources.
Discrete v009 poses are replayed at stations, with acquisition disabled in travel.
All contour endpoints are inverse-derived events; no truth-wall shortcut.
"""
import bpy,sys,math,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202'
E=R/'04-Production/Records/Tasks/T-027/Evidence';P=B/'Previews/MotionProof_v002'
P.mkdir(parents=True,exist_ok=True);(P/'Frames').mkdir(exist_ok=True)
sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct
C=read_json(B/'acquisition_config_v009.json');I=read_json(B/'Data/v009/index_v009.json')
events=read_json(B/'Data/v009/irregular_layers_events_v009.json.gz')
points=reconstruct(events,C);byid={p['sample_id']:p for p in points}
source=B/'Scenes/B202_measured-envelope_master_v009.blend'
out=B/'Scenes/B202-M_motion-proof_v002.blend'
assert not out.exists(),'Preserve existing candidate: version changes'
preserve=[source,R/'04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend',R/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend']
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before={p.relative_to(R).as_posix():hashfile(p) for p in preserve}
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL']
names=json.loads(c['v009_case_names']);c['data_case']=names.index('irregular_layers')
for k,v in {'show_tool':1,'show_nominal':0,'show_reconstruction':1,'show_echo_strength':0,'show_acquired_points':1,'show_interpolated':0,'event_time_s':-1.,'geometry_opacity':.35}.items():c[k]=v
col=bpy.data.collections.new('T27_MOTION_PROOF_v002');s.collection.children.link(col)
def smooth(x):x=max(0.,min(1.,x));return x*x*(3-2*x)
def lerp(a,b,t):return Vector(a).lerp(Vector(b),t)
def keyprop(k,v,f):c[k]=v;c.keyframe_insert(data_path='["'+k+'"]',frame=f)
start=events[0]['tool_pose']['rotation_xyz_rad'][0]
# All three sensors at an orientation are shown as one visually grouped replay.
# This explicitly changes display timing, never measurement positions/values.
def receipt(e):
    di=int(e['id'].split(':d')[1][:2]);ri=int(e['id'].split(':r')[1][:3])
    if di==0:return 28 if ri==0 else 36+ri*80/107
    if di==1:return 137+ri*39/107
    return 100000
timeline=[]
for f in range(1,193):
    if f<36:di=0;angle=start;travel=events[0]['tool_pose']['translation_m'][0]
    elif f<=116:di=0;angle=start+(f-36)/80*(107/108)*math.tau;travel=1.75-I['sensors'][0]['local_origin_m'][0]
    elif f<137:di=0;u=smooth((f-116)/21);angle=start+(107+u)/108*math.tau;travel=1.75-I['sensors'][0]['local_origin_m'][0]+.25*u
    elif f<=176:di=1;angle=start+math.tau+(f-137)/39*(107/108)*math.tau;travel=2.-I['sensors'][0]['local_origin_m'][0]
    else:di=1;u=smooth((f-176)/16);angle=start+math.tau+(107+u)/108*math.tau;travel=2.-I['sensors'][0]['local_origin_m'][0]+.25*u
    acquired=[e for e in events[:648] if receipt(e)<=f]
    # Blender stores custom properties/geometry attributes as float32. Bias by
    # 1us (well below the 10ms source spacing) so a receipt does not lose its
    # last record to a float32 round-down; the next source event stays hidden.
    cutoff=max((e['timestamp_s'] for e in acquired),default=-1.)+1e-6
    for k,v in [('rotation_rad',angle),('travel_m',travel),('event_time_s',cutoff)]:keyprop(k,v,f)
    timeline.append({'frame':f,'cutoff_s':cutoff,'event_count':len(acquired),'tool_travel_m':travel,'rotation_unwrapped_rad':angle,'acquisition_during_travel':False})
# Contour edges: each bin selects its earliest available valid inverse event.
# No bin averaging/future sample is used; interpolation only joins adjacent bins.
first={}
for e in events[:648]:
    if e['id'] not in byid:continue
    p=byid[e['id']];di=min(range(len(C['depths_m'])),key=lambda i:abs(C['depths_m'][i]-p['x_m']))
    ai=int(p['azimuth_rad']/math.tau*108)%108;first.setdefault((di,ai),(e,p))
mat=bpy.data.materials['B202 Circumference illustration']
segments=[]
def line(name,coords,material,radius=.0008):
    d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=radius;d.bevel_resolution=1
    sp=d.splines.new('POLY');sp.points.add(len(coords)-1)
    for p,v in zip(sp.points,coords):p.co=(*v,1)
    o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(material);return o
def appear(o,f):
    for attr in ('hide_render','hide_viewport'):
        setattr(o,attr,True);o.keyframe_insert(data_path=attr,frame=1)
        setattr(o,attr,False);o.keyframe_insert(data_path=attr,frame=math.ceil(f))
for di in range(2):
    for ai in range(108):
        pair=[first.get((di,j)) for j in (ai,(ai+1)%108)]
        if not all(pair):continue
        ready=max(receipt(x[0]) for x in pair)
        o=line(f'T27_registered_contour_d{di:02d}_a{ai:03d}',[x[1]['position_m'] for x in pair],mat)
        ids=[x[0]['id'] for x in pair];o['event_ids']=json.dumps(ids);o['meaning']='Interpolated edge between adjacent acquired event positions; not additional measurements.'
        appear(o,ready);segments.append({'object':o.name,'event_ids':ids,'receipt_frame':math.ceil(ready),'positions':[x[1]['position_m'] for x in pair]})
# A small travelling marker, not a spherical wave simulation. One first event.
e=events[0];p=byid[e['id']];origin=Vector(e['sensor_origin_m']);hit=Vector(p['position_m'])
bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.0032)
cue=bpy.context.object;cue.name='T27_first_event_roundtrip_cue'
for cl in list(cue.users_collection):cl.objects.unlink(cue)
col.objects.link(cue);cue.data.materials.append(mat)
cue['event_id']=e['id'];cue['same_sensor_return']=e['receiver_sensor_id']==e['sensor_id'];cue['scope']='Retimed illustrative locator, no acoustic scale/speed claim'
for f,pos in [(1,origin),(12,hit),(15,hit),(27,origin)]:cue.location=pos;cue.keyframe_insert(data_path='location',frame=f)
for attr in ('hide_render','hide_viewport'):
    setattr(cue,attr,False);cue.keyframe_insert(data_path=attr,frame=1);setattr(cue,attr,True);cue.keyframe_insert(data_path=attr,frame=28)
# Physical context: exact inherited T6 irregular wall mesh, cropped for access.
old=bpy.data.objects['B202_WALL_irregular'];me=old.data
faces=[tuple(p.vertices) for p in me.polygons if all(me.vertices[i].co.y>.07 for i in p.vertices)]
# Reverse inherited positive-Y half into the camera's far side by selecting the
# actual full profile mesh instead; no mirrored or rescaled physical geometry.
full=bpy.data.objects['B202_GEOMETRY_irregular'].data
faces=[tuple(p.vertices) for p in full.polygons if all(full.vertices[i].co.y<-.06 for i in p.vertices)]
used=sorted({i for face in faces for i in face});mp={v:i for i,v in enumerate(used)}
md=bpy.data.meshes.new('T27 sourced T6 context cutaway');md.from_pydata([full.vertices[i].co for i in used],[],[tuple(mp[i] for i in face) for face in faces]);md.update()
rock=bpy.data.objects.new('T27_T6_IRREGULAR_CONTEXT',md);col.objects.link(rock);md.materials.append(bpy.data.materials['B202 Physical wall context'])
rock['provenance']='Exact v008 stored T6 irregular mesh positions; only presentation cutaway, no truth-to-data binding'
# Camera and target are separate, densely baked to avoid Euler target snaps.
cd=bpy.data.cameras.new('T27 proof camera');cam=bpy.data.objects.new('T27_PROOF_CAMERA',cd);col.objects.link(cam);s.camera=cam
target=bpy.data.objects.new('T27_CAMERA_LOOK_TARGET',None);col.objects.link(target)
track=cam.constraints.new('TRACK_TO');track.target=target;track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
cd.lens=48;cd.clip_start=.005;cd.clip_end=200
score=[(1,(1.40,.60,.24),(1.75,.08,.0)),(36,(1.40,.60,.24),(1.75,.08,.0)),(105,(.78,.40,.33),(1.75,0.,0.)),(138,(.72,.60,.45),(1.80,0.,0.)),(192,(1.12,1.45,.88),(1.86,0.,0.))]
camera_records=[]
for f in range(1,193):
    a,b=next((a,b) for a,b in zip(score,score[1:]) if a[0]<=f<=b[0]);u=smooth((f-a[0])/(b[0]-a[0]))
    cam.location=lerp(a[1],b[1],u);target.location=lerp(a[2],b[2],u)
    cam.keyframe_insert(data_path='location',frame=f);target.keyframe_insert(data_path='location',frame=f)
    camera_records.append({'frame':f,'location':list(cam.location),'target':list(target.location),'lens_mm':cd.lens})
# Broad local light keeps the emitting side readable along the camera move.
ld=bpy.data.lights.new('T27 sensor-side softbox','AREA');lo=bpy.data.objects.new(ld.name,ld);col.objects.link(lo);lo.location=(1.5,1.8,1.2);ld.energy=90;ld.shape='DISK';ld.size=2
lo.rotation_euler=(Vector((1.8,0,0))-lo.location).to_track_quat('-Z','Y').to_euler()
s.frame_start=1;s.frame_end=192;s.render.fps=24;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100
s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=12;s.render.image_settings.file_format='PNG';s.render.film_transparent=False
s['T27_scope']='D2/D3 first proof only, 8s illustrative discrete-station replay. No acquisition during axial travel; full continuous-drilling sequence pending review.'
s['T27_data_source']='Data/v009/irregular_layers_events_v009.json.gz';s['T27_fixture_timing']='Authored display retiming; all event IDs, values, poses preserved. 3 sensor events grouped per orientation.'
s['T27_replay_manifest']='//../../../Records/Tasks/T-027/Evidence/replay_manifest_v002.json'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
# The loaded source contains no keyframes; our baked values are linear and hide
# keys constant. Dense keys describe the deliberately sampled replay exactly.
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
s.frame_set(1);s.render.filepath=str(P/'Frames/frame_');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
manifest={'version':'v002','case':'irregular_layers','scene':out.relative_to(R).as_posix(),'source_hashes':before,'source_index_hash':hashfile(B/'Data/v009/index_v009.json'),'event_file_hash':hashfile(B/'Data/v009/irregular_layers_events_v009.json.gz'),'timeline':timeline,'camera':camera_records,'segments':segments,'events':[{'id':e['id'],'sensor_id':e['sensor_id'],'receiver_sensor_id':e['receiver_sensor_id'],'receipt_frame':math.ceil(receipt(e)),'recorded_timestamp_s':e['timestamp_s']} for e in events[:648]],'limitations':['Discrete depth-station replay; no acquisition during axial transitions.','Three original sensor events visually grouped at each orientation.','Acoustic marker is illustrative slowed timing. No calibrated ENP3 cadence.','Two depth sections only; full geometry/amplitude demonstration waits for owner proof review.']}
(E/'replay_manifest_v002.json').write_text(json.dumps(manifest,indent=2))
assert before=={p.relative_to(R).as_posix():hashfile(p) for p in preserve}
for f in (1,12,28,72,116,156,192):s.frame_set(f);s.render.filepath=str(P/f'proof_{f:04d}.png');bpy.ops.render.render(write_still=True)
print('T27_BUILD_PROOF_PASS')
