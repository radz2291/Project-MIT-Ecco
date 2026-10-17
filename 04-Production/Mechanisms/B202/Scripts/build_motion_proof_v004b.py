"""Bounded response to T27 discussion b94637dc; all 13 v009 stations retimed.
Continuous sourced enclosing cutaway replaces disconnected patch. No new events.
"""
import bpy,sys,json,math,hashlib,bmesh
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];B=R/'04-Production/Mechanisms/B202';E=R/'04-Production/Records/Tasks/T-027/Evidence';P=B/'Previews/MotionProof_v004b'
P.mkdir(exist_ok=True);(P/'Frames').mkdir(exist_ok=True);sys.path.insert(0,str(B/'Scripts'))
from acquisition_core_v009 import read_json,reconstruct
C=read_json(B/'acquisition_config_v009.json');events=read_json(B/'Data/v009/irregular_layers_events_v009.json.gz');points=reconstruct(events,C);byid={p['sample_id']:p for p in points}
source=B/'Scenes/B202_measured-envelope_master_v009.blend';out=B/'Scenes/B202-M_motion-proof_v004b.blend';assert not out.exists()
hashfile=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
sources=[source,B/'Scenes/B202-M_motion-proof_v003.blend',R/'04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend',R/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend']
hashes={p.relative_to(R).as_posix():hashfile(p) for p in sources}
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;c=bpy.data.objects['B202_CONTROL'];names=json.loads(c['v009_case_names']);c['data_case']=names.index('irregular_layers')
for k,v in {'show_tool':1,'show_nominal':0,'show_reconstruction':1,'show_echo_strength':0,'show_acquired_points':1,'show_interpolated':0,'event_time_s':-1.,'geometry_opacity':.75}.items():c[k]=v
col=bpy.data.collections.new('T27_v004b_ENCLOSING_WELL_AND_REPLAY');s.collection.children.link(col)
def smooth(x):x=max(0,min(1,x));return x*x*(3-2*x)
def key(k,v,f):c[k]=v;c.keyframe_insert(data_path='["'+k+'"]',frame=f)
def group(e):return int(e['id'].split(':d')[1][:2]),int(e['id'].split(':r')[1][:3])
def receipt(e):
    di,ri=group(e)
    return (34 if ri==0 else 37+ri*59/107) if di==0 else 101+(di-1)*15+ri*10/107
start=events[0]['tool_pose']['rotation_xyz_rad'][0];timeline=[]
for f in range(1,337):
    if f<=36:di=0;ri=0.;angle=start;travel=events[0]['tool_pose']['translation_m'][0];phase='first_event'
    elif f<=96:di=0;ri=(f-37)/59*107;angle=start+ri/108*math.tau;travel=events[0]['tool_pose']['translation_m'][0];phase='circumference'
    elif f<=276:
        # 4 display frames of axial transfer, then 11 of station acquisition.
        di=min(12,1+(f-97)//15);local=f-(97+(di-1)*15)
        base=events[di*324]['tool_pose']['translation_m'][0]
        if local<4:
            u=smooth((local+1)/4);travel=base-.25+.25*u;angle=start+(di-1)*math.tau+(107+u)/108*math.tau;phase='transfer'
        else:ri=(local-4)/10*107;travel=base;angle=start+di*math.tau+ri/108*math.tau;phase='depth_replay'
    else:
        u=smooth((f-276)/48);travel=events[-1]['tool_pose']['translation_m'][0]+.55*u;angle=start+12*math.tau+107/108*math.tau+.5*u;phase='release_hold'
    acquired=[e for e in events if receipt(e)<=f];cutoff=max((e['timestamp_s'] for e in acquired),default=-1)+1e-6
    for k,v in [('rotation_rad',angle),('travel_m',travel),('event_time_s',cutoff)]:key(k,v,f)
    timeline.append({'frame':f,'phase':phase,'event_count':len(acquired),'cutoff_s':cutoff,'travel_m':travel,'rotation_rad':angle})
# Full enclosing source wall: exact inner vertices, plus authored rock exterior
# and cut faces to communicate a solid cutaway, never a floating thin sheet.
full=bpy.data.objects['B202_GEOMETRY_irregular'].data
inner=[tuple(v.co) for v in full.vertices]
def keep(face):
    centre=sum((full.vertices[i].co for i in face),Vector())/len(face);a=math.atan2(centre.z,centre.y)%math.tau
    return not (a<1.4 or a>math.tau-.4)
innerfaces=[tuple(p.vertices) for p in full.polygons if keep(p.vertices)]
outer=[]
for x,y,z in inner:
    a=math.atan2(z,y);ca,sa=math.cos(a),math.sin(a);scale=.34/max(abs(ca),abs(sa));outer.append((x,scale*ca,scale*sa))
nv=len(inner);allfaces=list(innerfaces)+[tuple(i+nv for i in reversed(f)) for f in innerfaces];edges={}
for face in innerfaces:
    for a,b in zip(face,face[1:]+face[:1]):edges.setdefault(tuple(sorted((a,b))),[]).append((a,b))
for pairs in edges.values():
    if len(pairs)==1:a,b=pairs[0];allfaces.append((a,b,b+nv,a+nv))
me=bpy.data.meshes.new('T27 exact T6 interior with authored solid-rock exterior');me.from_pydata(inner+outer,[],allfaces);me.update()
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
rock=bpy.data.objects.new('T27_CONTINUOUS_ENCLOSING_ROCK_CUTAWAY',me);col.objects.link(rock)
rock['source_inner_vertex_count']=nv;rock['source']='B202_GEOMETRY_irregular from accepted T6 v003, unchanged inner coordinates. Outer square .68m and cut faces are presentation rock mass.'
mat=bpy.data.materials.new('T27 matte rock / presentation-only exterior');mat.use_nodes=True;tree=mat.node_tree;bs=tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.095,.062,.037,1);bs.inputs['Roughness'].default_value=.9
noise=tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=20;bump=tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.12;bump.inputs['Distance'].default_value=.002;tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);tree.links.new(bump.outputs['Normal'],bs.inputs['Normal'])
mix=tree.nodes.new('ShaderNodeMixShader');tr=tree.nodes.new('ShaderNodeBsdfTransparent');tree.links.new(tr.outputs[0],mix.inputs[1]);tree.links.new(bs.outputs[0],mix.inputs[2]);tree.links.new(mix.outputs[0],tree.nodes.get('Material Output').inputs[0]);mat.surface_render_method='DITHERED';me.materials.append(mat)
for f,v in [(1,1),(170,1),(276,0),(336,0)]:mix.inputs[0].default_value=v;mix.inputs[0].keyframe_insert(data_path='default_value',frame=f)
# Sparse contour context at four sampled sections; world-fixed actual inverse
# endpoints and adjacent-bin coverage only. Other points retain their event IDs.
first={}
for e in events:
    p=byid[e['id']];di,_=group(e);ai=int(p['azimuth_rad']/math.tau*108)%108;first.setdefault((di,ai),(e,p))
line_mat=bpy.data.materials['B202 Circumference illustration'].copy();line_mat.name='T27 restrained measured contours'
segments=[]
for di in (0,4,8,12):
    for ai in range(108):
        pair=[first.get((di,j)) for j in (ai,(ai+1)%108)]
        if not all(pair):continue
        d=bpy.data.curves.new(f'T27_v004b_contour_d{di}_a{ai}','CURVE');d.dimensions='3D';d.bevel_depth=.0006;d.bevel_resolution=1;sp=d.splines.new('POLY');sp.points.add(1)
        for p,x in zip(sp.points,pair):p.co=(*x[1]['position_m'],1)
        o=bpy.data.objects.new(d.name,d);col.objects.link(o);d.materials.append(line_mat);ready=math.ceil(max(receipt(x[0]) for x in pair));ids=[x[0]['id'] for x in pair];o['source_event_ids']=json.dumps(ids)
        for attr in ('hide_render','hide_viewport'):
            setattr(o,attr,True);o.keyframe_insert(data_path=attr,frame=1);setattr(o,attr,False);o.keyframe_insert(data_path=attr,frame=ready)
        segments.append({'object':o.name,'receipt_frame':ready,'event_ids':ids})
# The original evidence point cloud remains, with conservative receipt cutoff.
# Marker footprint is presentation, not enlarged physical geometry/accuracy.
ng=bpy.data.node_groups['B202_v009_Acquired_Point_Display'];next(n for n in ng.nodes if n.bl_idname=='GeometryNodeMeshIcoSphere').inputs['Radius'].default_value=.0021
e=events[1];origin=Vector(e['sensor_origin_m']);hit=Vector(byid[e['id']]['position_m'])
bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.0025);cue=bpy.context.object;cue.name='T27_v004b_first_same_sensor_return'
for cl in list(cue.users_collection):cl.objects.unlink(cue)
col.objects.link(cue);cue.data.materials.append(line_mat);cue['event_id']=e['id']
for f,v in [(1,origin),(14,hit),(18,hit),(32,origin)]:cue.location=v;cue.keyframe_insert(data_path='location',frame=f)
for attr in ('hide_render','hide_viewport'):
    setattr(cue,attr,False);cue.keyframe_insert(data_path=attr,frame=1);setattr(cue,attr,True);cue.keyframe_insert(data_path=attr,frame=34)
cd=bpy.data.cameras.new('T27 v004b camera');cam=bpy.data.objects.new(cd.name,cd);col.objects.link(cam);target=bpy.data.objects.new('T27_v004b_GAZE',None);col.objects.link(target);con=cam.constraints.new('TRACK_TO');con.target=target;con.track_axis='TRACK_NEGATIVE_Z';con.up_axis='UP_Y';cd.lens=42;cd.clip_start=.005;s.camera=cam
score=[(1,(1.35,.75,.65),(1.75,-.05,.06)),(34,(1.35,.75,.65),(1.75,-.05,.06)),(90,(.75,.46,.34),(1.90,0,0)),(144,(1.05,.85,.62),(2.4,0,0)),(230,(.5,2.,1.15),(3.05,0,0)),(300,(.5,2.,1.15),(3.05,0,0)),(336,(.40,1.9,1.08),(3.05,0,0))]
camera=[]
for f in range(1,337):
    a,b=next((a,b) for a,b in zip(score,score[1:]) if a[0]<=f<=b[0]);u=smooth((f-a[0])/(b[0]-a[0]));cam.location=Vector(a[1]).lerp(Vector(b[1]),u);target.location=Vector(a[2]).lerp(Vector(b[2]),u)
    cam.keyframe_insert(data_path='location',frame=f);target.keyframe_insert(data_path='location',frame=f);camera.append({'frame':f,'location':list(cam.location),'target':list(target.location),'lens_mm':42})
ld=bpy.data.lights.new('T27 cutaway broad light','AREA');lo=bpy.data.objects.new(ld.name,ld);col.objects.link(lo);lo.location=(2.5,2.5,2.5);ld.energy=180;ld.size=4;lo.rotation_euler=(Vector((3,0,0))-lo.location).to_track_quat('-Z','Y').to_euler()
# Source white nominal references clarify true irregularity without exaggeration.
ref=bpy.data.objects['B202_v009_WHITE_NOMINAL'];refx=ref.data.splines[0].points[0].co.x
for x in (2.5,3.5,4.5):
    o=ref.copy();o.data=ref.data.copy();o.animation_data_clear();o.name=f'T27_v004b_WHITE_NOMINAL_{x}';col.objects.link(o);o.location.x=x-refx;o.data.bevel_depth=.00065;o['meaning']='White nominal bit-size reference; not an acquired contour or gauge bit.'
    for attr in ('hide_render','hide_viewport'):
        setattr(o,attr,True);o.keyframe_insert(data_path=attr,frame=1);setattr(o,attr,False);o.keyframe_insert(data_path=attr,frame=240)
ico=next(n for n in ng.nodes if n.bl_idname=='GeometryNodeMeshIcoSphere')
for f,value in [(1,.0021),(220,.0021),(300,.0007),(336,.0007)]:ico.inputs['Radius'].default_value=value;ico.inputs['Radius'].keyframe_insert(data_path='default_value',frame=f)
# Low-cost greyscale hardware, semantic geometry only, no premium finishing.
s.frame_start=1;s.frame_end=336;s.render.fps=24;s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.render.image_settings.file_format='PNG'
s['T27_v004b_scope']='14s bounded revision proof, 13 existing v009 stations/4212 events retimed; none regenerated. Acquisition paused during station transfers. Rock opacity is explanatory presentation, not physical disappearance.'
for action in bpy.data.actions:
    for slot in action.slots:
        for layer in action.layers:
            for strip in layer.strips:
                bag=strip.channelbag(slot)
                if bag:
                    for fc in bag.fcurves:
                        for k in fc.keyframe_points:k.interpolation='CONSTANT' if 'hide_' in fc.data_path else 'LINEAR'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.frame_set(1);s.render.filepath=str(P/'Frames/frame_');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
manifest={'version':'v004b','scene':out.relative_to(R).as_posix(),'case':'irregular_layers','source_hashes':hashes,'provenance':'All 4212 existing v009 events at 13 stations retimed, none regenerated. Original values/poses/IDs/masks retained. Three events per orientation grouped.','timeline':timeline,'camera':camera,'segments':segments,'events':[{'id':e['id'],'sensor_id':e['sensor_id'],'receiver_sensor_id':e['receiver_sensor_id'],'receipt_frame':math.ceil(receipt(e)),'timestamp_s':e['timestamp_s']} for e in events],'depth_span_m':3.,'rock_inner_source_vertices':nv,'review_comment_id':'b94637dc-0785-4585-92f4-967b433bdda2'}
(E/'replay_manifest_v004b.json').write_text(json.dumps(manifest,indent=2));assert hashes=={p.relative_to(R).as_posix():hashfile(p) for p in sources}
for f in (1,14,72,144,240,336):s.frame_set(f);s.render.filepath=str(P/f'proof_{f:04d}.png');bpy.ops.render.render(write_still=True)
print('T27_V004_BUILD_PASS')

