"""B201 mechanism proof. Run in isolated Blender; preserves both accepted masters.

Axial section is a camera clipping operation, not invented internal anatomy.
The wall profile is sampled directly from T6's evaluated irregular full wall.
All signal/time graphics are schematic and intentionally slowed.
"""
import bpy, math, json, hashlib, time, sys
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[3]
MECH=ROOT/'Mechanisms/B201'; REC=ROOT/'Records/Tasks/T-007'
OUT=MECH/'Scenes/B201_pulse-echo_v002.blend'
if OUT.exists(): raise RuntimeError('Refuse candidate overwrite; create a new version')
source=ROOT/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
product=ROOT/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend'
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,product]}
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene
with bpy.data.libraries.load(str(source),link=False) as (a,b): b.collections=['WELL_ASSEMBLY_v003']
s.collection.children.link(b.collections[0])
r=bpy.data.objects['ASSEMBLY_CONTROL']
for k,v in dict(travel_m=2.07,rotation_rad=0.,variant=1,cutaway=0,show_casing=0,show_cement=0,show_open=1,show_hardware=1,show_proxies=0).items():r[k]=v
r.update_tag();bpy.context.view_layer.update()
wall=bpy.data.objects['IRREGULAR_FULL']
dg=bpy.context.evaluated_depsgraph_get()
refs=[bpy.data.objects[f'ECCO_SENSOR_REF_{i:02}'] for i in range(1,4)]
caps=[o for o in bpy.data.objects if o.library and 'TEMP |' in o.name]
evidence={'inputs':hashes,'blender':bpy.app.version_string,'sensor_references':[{ 'name':o.name,'position':list(o.matrix_world.translation)} for o in refs], 'closures':[o.name for o in caps]}
fx=bpy.data.collections.new('B201_SCHEMATIC_EFFECTS');s.collection.children.link(fx)
def move(o):
    for c in list(o.users_collection):c.objects.unlink(o)
    fx.objects.link(o)
def ball(name,size,color):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=size)
    o=bpy.context.object;o.name=name;o.color=(*color,1);move(o);return o
def line(name,pts,width,color):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2
    p=c.splines.new('POLY');p.points.add(len(pts)-1)
    for q,v in zip(p.points,pts):q.co=(*v,1)
    o=bpy.data.objects.new(name,c);fx.objects.link(o);o.color=(*color,1);return o
def key(o,frame,pos=None,scale=None):
    if pos is not None:o.location=pos;o.keyframe_insert(data_path='location',frame=frame)
    if scale is not None:o.scale=(scale,)*3;o.keyframe_insert(data_path='scale',frame=frame)
def curves(action,slot):
    return action.layers[0].strips[0].channelbag(slot).fcurves
def linear(o):
    if o.animation_data:
        for fc in curves(o.animation_data.action,o.animation_data.action_slot):
            for k in fc.keyframe_points:k.interpolation='LINEAR'
# T6 wall raycast in source metres; hit and pulse exist on the same sensor plane.
def wall_point(angle):
    d=Vector((0,math.cos(angle),math.sin(angle)))
    ok,p,n,idx=wall.evaluated_get(dg).ray_cast(Vector((2.8,0,0)),d)
    assert ok
    return p,d
# Draw a section line from actual T6 evaluated geometry (source mesh hidden only in consumer).
profile=[wall_point(2*math.pi*j/192)[0] for j in range(193)]
wall.hide_render=True
line('T6_EVALUATED_WALL_SECTION',profile,.0015,(.30,.34,.39))
events=[]
for cycle in range(6):
    start=1+cycle*72;rot=math.radians(cycle*32)
    r['rotation_rad']=rot;r.keyframe_insert(data_path='["rotation_rad"]',frame=start)
    r.keyframe_insert(data_path='["rotation_rad"]',frame=start+59)
    # Use inherited reference 01, rotated by the actual assembly control.
    base=refs[0].matrix_world.translation
    a=math.atan2(base.z,base.y)+rot
    hit,d=wall_point(a)
    rim=Vector((2.8,math.hypot(base.y,base.z)*d.y,math.hypot(base.y,base.z)*d.z))
    # Find exterior of accepted plugged hardware along this same radial ray.
    # Cast each linked mesh from outside inward and retain outermost intersection.
    outer=0.;outer_name=None
    for o in bpy.data.collections['ECCO_MASTER_v002'].all_objects:
        if o.type!='MESH' or o.hide_render:continue
        inv=o.matrix_world.inverted();origin=Vector((.73,0,0))+d*.25
        ok,p,n,idx=o.ray_cast(inv@origin,(inv.to_3x3()@(-d)).normalized())
        if ok:
            wp=o.matrix_world@p;rr=wp.y*d.y+wp.z*d.z
            if rr>outer:outer=rr;outer_name=o.name
    # Re-evaluate at unrotated sensor angle for source exterior, then rotate outward origin.
    # The meshes above are source coordinates; repeat at base angle when rotation !=0.
    db=Vector((0,math.cos(a-rot),math.sin(a-rot)))
    outer=0.;outer_name=None
    for o in bpy.data.collections['ECCO_MASTER_v002'].all_objects:
        if o.type!='MESH' or o.hide_render:continue
        inv=o.matrix_world.inverted();origin=Vector((.73,0,0))+db*.25
        ok,p,n,idx=o.ray_cast(inv@origin,(inv.to_3x3()@(-db)).normalized())
        if ok:
            wp=o.matrix_world@p;rr=wp.y*db.y+wp.z*db.z
            if rr>outer:outer=rr;outer_name=o.name
    assert .12<outer<.153,(outer,outer_name)
    origin=Vector((2.8,0,0))+d*(outer+.0004)
    distance=(hit-origin).length
    assert distance>.002
    leg=round(distance/.003) # Authoring speed 3mm/frame; never displayed as physical speed.
    emit=start+10;contact=emit+leg;receive=contact+leg
    assert receive<start+59
    outgoing=ball(f'TX_{cycle+1}',.0023,(.2,.8,1.));echo=ball(f'ECHO_{cycle+1}',.0023,(1.,.68,.23))
    spot=ball(f'WALL_FLASH_{cycle+1}',.005,(.6,.88,1.))
    sensor=ball(f'EMITTER_REFERENCE_{cycle+1}',.0028,(.2,.8,1.))
    for o in (outgoing,echo,spot,sensor):key(o,1,scale=0);key(o,432,scale=0)
    key(sensor,start,origin,1);key(sensor,start+59,scale=1);key(sensor,start+60,scale=0)
    key(outgoing,emit-1,origin,0);key(outgoing,emit,origin,1);key(outgoing,contact,hit,1);key(outgoing,contact+1,scale=0)
    key(echo,contact-1,hit,0);key(echo,contact,hit,1);key(echo,receive,origin,1);key(echo,receive+1,scale=0)
    key(spot,contact-1,hit,0);key(spot,contact,hit,1);key(spot,contact+4,scale=1);key(spot,contact+9,scale=0)
    for o in (outgoing,echo,spot,sensor):linear(o)
    events.append(dict(cycle=cycle+1,start=start,angle_rad=a,rotation_rad=rot,emit=emit,contact=contact,receive=receive,origin=list(origin),wall=list(hit),rim=list(rim),source_surface=outer_name,surface_radius_m=outer,illustrative_standoff_m=distance,leg_frames=leg))
linear(r)
# Consumer-only exact section, capped by Boolean intersection of supplied meshes.
# This makes the axial section readable without fabricating internal components.
bpy.ops.mesh.primitive_cube_add(size=1,location=(.73,0,0))
cutter=bpy.context.object;cutter.name='B201_SECTION_VOLUME';cutter.dimensions=(.024,.5,.5)
bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
section_names=[]
for src in list(bpy.data.collections['ECCO_MASTER_v002'].all_objects):
    if src.type!='MESH' or src.hide_render:continue
    mesh=src.data.copy();mesh.transform(src.matrix_world)
    o=bpy.data.objects.new('SECTION | '+src.name,mesh);fx.objects.link(o);o.color=(.42,.46,.51,1)
    bpy.context.view_layer.objects.active=o;o.select_set(True)
    mod=o.modifiers.new('Exact source section','BOOLEAN');mod.operation='INTERSECT';mod.solver='EXACT';mod.object=cutter
    bpy.ops.object.modifier_apply(modifier=mod.name)
    o.parent=bpy.data.objects['ASSEMBLY_ROTATION_X'];section_names.append(o.name)
    o.select_set(False)
bpy.data.objects.remove(cutter,do_unlink=True)
r['show_hardware']=0;r.update_tag()
evidence['display_section']=section_names
bpy.ops.object.camera_add(location=(1.07,0,0))
cam=bpy.context.object;cam.name='B201_AXIAL_SECTION_CAMERA';cam.rotation_euler=Vector((1,0,0)).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=.415
cam.data.clip_start=.1;cam.data.clip_end=3;s.camera=cam
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_shadows=False;s.display.shading.show_cavity=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('B201_WORLD');s.world.color=(.024,.032,.047)
s.view_settings.view_transform='Standard'
s.render.resolution_x=700;s.render.resolution_y=700;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=432;s.render.image_settings.file_format='PNG'
s.render.filepath='//../Previews/Frames/raw_'
s['meaning']='Standalone conceptual pulse/echo proof. Slowed schematic time; illustrative waveform, not measured data.'
s['sensor_limit']='Marker on exterior visual cap along inherited recess reference; not a calibrated transducer face. O04.'
s['acquisition']='Step-and-hold stations expose round trips; inter-station whole-tool rotation. No operating RPM claim.'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
evidence.update(events=events,scene_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),camera={'position':list(cam.location),'rotation':list(cam.rotation_euler),'clip':[cam.data.clip_start,cam.data.clip_end],'ortho_scale':cam.data.ortho_scale})
(REC/'Evidence/build_v002.json').write_text(json.dumps(evidence,indent=2))
print('B201_BUILD_PASS')
if '--render' in sys.argv:
    bpy.ops.wm.open_mainfile(filepath=str(OUT));t=time.perf_counter();bpy.ops.render.render(animation=True)
    evidence['render_seconds']=time.perf_counter()-t
    (REC/'Evidence/render_v002.json').write_text(json.dumps(evidence,indent=2))

