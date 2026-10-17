"""T41 isolated 12s method test. Run with installed Blender --background.
No edits to source masters; effects and timing are synthetic illustrations.
"""
import bpy, math, json, hashlib, time, sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view

BASE=Path(__file__).resolve().parents[1]
P=BASE.parents[2]
E=P/'Records/Tasks/T-041/Evidence'
OUT=BASE/'Scenes/S02_previs_T041_v003.blend'
for folder in (E,OUT.parent,BASE/'Previews/Frames'):folder.mkdir(parents=True,exist_ok=True)
if OUT.exists():raise RuntimeError('Version edited candidates; refusing scene overwrite')
sources=[P/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend',P/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend']
hashes={str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
assert hashes[str(sources[1].relative_to(P))]=='704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1
with bpy.data.libraries.load(str(sources[0]),link=False) as (a,b):b.collections=['WELL_ASSEMBLY_v003']
s.collection.children.link(b.collections[0]);rig=bpy.data.objects['ASSEMBLY_CONTROL']
for k,v in dict(travel_m=2.07,rotation_rad=0.,variant=1,cutaway=0,show_open=1,show_casing=0,show_cement=0,show_hardware=1,show_proxies=0).items():rig[k]=v
rig.update_tag();bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
wall=bpy.data.objects['IRREGULAR_FULL'].evaluated_get(dg);me=wall.to_mesh()
bvh=BVHTree.FromPolygons([v.co.copy() for v in me.vertices],[list(p.vertices) for p in me.polygons]);wall.to_mesh_clear()
X=2.8
def hit(a,x=X):
    p,n,i,d=bvh.ray_cast(Vector((x,0,0)),Vector((0,math.cos(a),math.sin(a))))
    assert p is not None
    return p
def collection(n):
    c=bpy.data.collections.new(n);s.collection.children.link(c);return c
env=collection('T41_EXPLANATORY_WALL_WINDOW');fx=collection('T41_SYNTHETIC_PULSE_ECHO');data=collection('T41_SYNTHETIC_WALL_READINGS');gfx=collection('T41_EDITORIAL_INFORMATION');cams=collection('T41_CAMERA_AND_GAZE')
def move(o,c):
    for cc in list(o.users_collection):cc.objects.unlink(o)
    c.objects.link(o)
def curve(n,pts,width,color,c=fx):
    q=bpy.data.curves.new(n,'CURVE');q.dimensions='3D';q.bevel_depth=width;q.bevel_resolution=1
    sp=q.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,v in zip(sp.points,pts):p.co=(*v,1)
    o=bpy.data.objects.new(n,q);c.objects.link(o);o.color=(*color,1);return o
def ball(n,r,color,c=fx):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=r)
    o=bpy.context.object;o.name=n;move(o,c);o.color=(*color,1);return o
def visible(o,start,end=288):
    for f,v in [(0,True),(start,False),(end+1,True)]:
        o.hide_render=v;o.hide_viewport=v
        o.keyframe_insert(data_path='hide_render',frame=f);o.keyframe_insert(data_path='hide_viewport',frame=f)
def linear(o):
    if not o.animation_data or not o.animation_data.action:return
    ac=o.animation_data.action
    for layer in ac.layers:
        for strip in layer.strips:
            bag=strip.channelbag(o.animation_data.action_slot)
            if bag:
                for fc in bag.fcurves:
                    for k in fc.keyframe_points:k.interpolation='LINEAR' if fc.data_path not in ('hide_render','hide_viewport') else 'CONSTANT'
def smooth(t):return t*t*(3-2*t)
def rotation(f):
    if f<=72:return math.radians(99-6*smooth(max(0,(f-1)/71)))
    if f<=168:return math.radians(93-8*smooth((f-72)/96))
    if f<=260:return math.radians(85-120*smooth((f-168)/92))
    return math.radians(-35)
# Retain exact evaluated T6 coordinates; remove near-side rock for CGI access.
verts=[];faces=[];nx=30;na=96
for i in range(nx+1):
    x=2.22+i*1.45/nx
    for j in range(na+1):verts.append(hit(2*math.pi*j/na,x))
for i in range(nx):
    for j in range(na):
        angle=(j+.5)*360/na
        if 92<angle<268:continue
        z=i*(na+1)+j;faces.append((z,z+1,z+na+2,z+na+1))
q=bpy.data.meshes.new('T6 evaluated exact wall coordinates');q.from_pydata(verts,[],faces);q.update()
o=bpy.data.objects.new('T41_T6_ROCK_CUTAWAY',q);env.objects.link(o);o.color=(.085,.115,.14,1)
o['source']='T6 v003 exact evaluated surface. Removed near hemisphere is an illustrative window, not physical transparency.'

patchverts=[];patchfaces=[]
for ii in range(13):
    xx=2.775+ii*.05/12
    for jj in range(25):patchverts.append(hit(math.radians(121+jj*22/24),xx))
for ii in range(12):
    for jj in range(24):
        zz=ii*25+jj
        if ((ii-5.5)/6)**2+((jj-11.5)/12)**2<1:patchfaces.append((zz,zz+1,zz+26,zz+25))
pm=bpy.data.meshes.new('Exact T6 contact surface');pm.from_pydata(patchverts,[],patchfaces);pm.update()
po=bpy.data.objects.new('T41_RETAINED_ROCK_AT_CONTACT',pm);env.objects.link(po);po.color=(.20,.28,.32,1)
visible(po,1,168)

rig['show_open']=0;rig.update_tag()
# Source local recess references + surface ray check; no acoustic face invented.
refs=[]
for i in range(1,4):
    ref=bpy.data.objects[f'ECCO_SENSOR_REF_{i:02d}'];p=ref.matrix_world.translation;a=math.atan2(p.z,p.y);d=Vector((0,math.cos(a),math.sin(a)))
    surface=0;name=None
    for obj in bpy.data.collections['ECCO_MASTER_v002'].all_objects:
        if obj.type!='MESH' or obj.hide_render:continue
        inv=obj.matrix_world.inverted();ok,h,n,idx=obj.ray_cast(inv@(Vector((.73,0,0))+d*.25),(inv.to_3x3()@(-d)).normalized())
        if ok:
            h=obj.matrix_world@h;r=h.y*d.y+h.z*d.z
            if r>surface:surface=r;name=obj.name
    assert .12<surface<.153
    refs.append(dict(index=i,source_angle=a,radius=surface+.0005,ray_surface=name,source_xyz=list(p)))
def origin(i,f):
    r=refs[i];a=r['source_angle']+rotation(f)
    return Vector((X,r['radius']*math.cos(a),r['radius']*math.sin(a)))
for f in range(1,289):
    rig['rotation_rad']=rotation(f);rig.keyframe_insert(data_path='["rotation_rad"]',frame=f)
linear(rig)
for i in range(3):
    mark=ball(f'RECESS_REFERENCE_GLYPH_{i+1}',.0035,(.38,.78,.83))
    mark['limit']='Illustrative glyph over inherited recess; not new hardware or calibrated face'
    for f in range(1,289):mark.location=origin(i,f);mark.keyframe_insert(data_path='location',frame=f)
    linear(mark)
# Deliberate camera arrivals; keyed gaze is independent of position.
camdata=bpy.data.cameras.new('T41_42mm_PERSPECTIVE');cam=bpy.data.objects.new(camdata.name,camdata);cams.objects.link(cam);s.camera=cam
camdata.lens=42;camdata.sensor_width=36;camdata.clip_start=.015;camdata.clip_end=50
target=bpy.data.objects.new('T41_GAZE_TARGET',None);cams.objects.link(target)
track=cam.constraints.new('TRACK_TO');track.target=target;track.track_axis='TRACK_NEGATIVE_Z';track.up_axis='UP_Y'
poses=[(1,(2.23,-.26,.25),(2.80,-.10,.105)),(65,(2.26,-.25,.24),(2.80,-.10,.105)),(92,(2.29,-.25,.24),(2.80,-.10,.105)),(155,(2.29,-.25,.24),(2.80,-.10,.105)),(255,(1.78,-.30,.26),(2.80,0,.045)),(288,(1.78,-.30,.26),(2.80,0,.045))]
for f,loc,gaze in poses:
    cam.location=loc;cam.keyframe_insert(data_path='location',frame=f)
    target.location=gaze;target.keyframe_insert(data_path='location',frame=f)
for ob in (cam,target):
    for layer in ob.animation_data.action.layers:
        for strip in layer.strips:
            for fc in strip.channelbag(ob.animation_data.action_slot).fcurves:
                for k in fc.keyframe_points:k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
camera_samples=[]
# Camera-local coordinates yield an editable calm editorial layer.
depth=.27;width=depth*36/42;height=width*9/16
def screen(x,y):return Vector(((x/640-.5)*width,(.5-y/360)*height,-depth))
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf');font.pack()
def text(n,body,x,y,size,start=1,end=288,color=(.76,.84,.87)):
    q=bpy.data.curves.new(n,'FONT');q.body=body;q.font=font;q.size=size*width/640
    o=bpy.data.objects.new(n,q);gfx.objects.link(o);o.parent=cam;o.location=screen(x,y);o.color=(*color,1);visible(o,start,end);return o
def screenline(n,points,w,col,start,end):
    o=curve(n,[screen(*p) for p in points],w*width/640,col,gfx);o.parent=cam;visible(o,start,end);return o
text('Provenance','T41 / PREVIS     Illustrative ultrasound · synthetic timing',18,23,12)
text('A message','Sound reaches the wall',18,51,22,1,72)
text('B message','Returning time reveals distance',18,51,22,73,168)
text('C message','Repeated echoes reveal the surrounding shape',18,51,20,169,288)
text('Camera and matter note','CGI rock/mud cutaway · provisional acoustic-face origin',18,348,11)
text('Velocity correction','Mud velocity correction + sensor position required',18,320,13,86,168)
text('C rotating note','Wall-fixed outline / x-ray data overlay',18,316,14,169,288)

panelverts=[screen(x,y)+Vector((0,0,-.001)) for x,y in [(12,211),(365,211),(365,331),(12,331)]]
pm=bpy.data.meshes.new('Quiet waveform backing');pm.from_pydata(panelverts,[],[(0,1,2,3)]);pm.update()
po=bpy.data.objects.new('T41_WAVEFORM_READING_FIELD',pm);gfx.objects.link(po);po.parent=cam;po.color=(.015,.028,.038,1);visible(po,73,168)

# First three contact glimpses; three B responses; then 3-sector sparse scan.
events=[]
for j,(emit,leg) in enumerate([(12,10),(43,4),(56,4),(81,11),(118,6),(143,7)]):
    events.append(dict(id=f'PRINCIPLE_{j+1}',sensor=0,emit=emit,contact=emit+leg,receive=emit+2*leg,kind='readable_principle',trace=j-3 if j>=3 else None))
for i in range(3):
    for j in range(37):
        emit=round(168+92*j/36)
        events.append(dict(id=f'SCAN_{i+1}_{j:02d}',sensor=i,emit=emit,contact=emit+3,receive=emit+6,kind='sparse_illustrative_scan',trace=None))
for e in events:
    i=e['sensor'];a=refs[i]['source_angle']+rotation(e['emit']);wallp=hit(a);src=origin(i,e['emit']);dst=origin(i,e['receive'])
    e.update(angle=a,origin=list(src),wall=list(wallp),receiver=list(dst),standoff_m=(wallp-src).length)
    for phase,color,f0,f1,p0,p1 in [('TX',(.23,.86,1),e['emit'],e['contact'],src,wallp),('ECHO',(1,.61,.22),e['contact'],e['receive'],wallp,dst)]:
        pulse=ball(e['id']+'_'+phase,.0028 if e['kind']=='readable_principle' else .0016,color)
        pulse.location=p0;pulse.keyframe_insert(data_path='location',frame=f0)
        pulse.location=p1;pulse.keyframe_insert(data_path='location',frame=f1);visible(pulse,f0,f1);linear(pulse)
    spot=ball(e['id']+'_CONTACT',.006 if e['kind']=='readable_principle' else .0025,(.44,.85,.91));spot.location=wallp;visible(spot,e['contact'],e['contact']+3)
    dot=ball(e['id']+'_WALL_RECORD',.0015,(.20,.73,.86),data);dot.location=wallp;visible(dot,e['receive']);dot['meaning']='Synthetic wall position, revealed only after echo reception; world-fixed'
    if e['kind']=='readable_principle':
        path=curve(e['id']+'_SENSOR_WALL_RELATION',[src,wallp],.00045,(.2,.35,.4));visible(path,e['emit'],e['receive']+3)
        if e['trace'] is not None:
            row=e['trace'];x=40;y=250+row*21;delay=e['receive']-e['emit'];scale=7.0
            pts=[]
            for k in range(161):
                t=-2+k*30/160
                value=10*math.exp(-(t/.6)**2)-4*math.exp(-((t-1)/.7)**2)+8*math.exp(-((t-delay)/.7)**2)-3*math.exp(-((t-delay-1)/.8)**2)
                pts.append(screen(x+t*scale,y-value))
            trace=curve(e['id']+'_SYNTHETIC_TRACE',pts,.65*width/640,(.26,.82,.90),gfx);trace.parent=cam;visible(trace,e['emit'],168)
            for f,v in [(e['emit']-2,0.),(e['emit']+28,1.)]:trace.data.bevel_factor_end=v;trace.data.keyframe_insert(data_path='bevel_factor_end',frame=f)
            text(e['id']+'_TX_LABEL','Tx',x-3,y+14,9,e['emit'],168)
            text(e['id']+'_RX_LABEL','Echo',x+delay*scale-8,y+14,9,e['receive'],168,(.94,.67,.36))
            if row==0:
                screenline('TWO_WAY_TIME',[(x,y-20),(x+delay*scale,y-20)],.65,(.94,.67,.36),e['receive'],168)
                text('TIME_MEANING','Two-way time',224,y-16,12,e['receive'],168,(.94,.67,.36))
                # Spatial leader's endpoint follows the same moving sensor until receipt.
                lead=curve('SENSOR_TO_TIME_RECORD',[src,src],.0004,(.24,.42,.47),gfx);visible(lead,e['emit'],e['receive']+9)
                for f in range(e['emit'],e['receive']+10):
                    s.frame_set(f);bpy.context.view_layer.update();end=cam.matrix_world@screen(340,245)
                    for point,co in zip(lead.data.splines[0].points,[origin(i,min(f,e['receive'])),end]):
                        point.co=(*co,1);point.keyframe_insert(data_path='co',frame=f)
# Incremental sector arcs follow exact wall intersections. No unsampled full ring.
for i in range(3):
    sector=[e for e in events if e['kind']=='sparse_illustrative_scan' and e['sensor']==i]
    for prev,nxt in zip(sector,sector[1:]):
        points=[hit(prev['angle']+(nxt['angle']-prev['angle'])*j/4) for j in range(5)]
        arc=curve(f'WALL_ARC_{i}_{nxt["id"]}',points,.0011,(.20,.73,.86),data);visible(arc,nxt['receive']);arc['meaning']='Interpolated between adjacent synthetic samples of same evaluated T6 wall'
for ob in data.objects:ob.show_in_front=True
for ob in gfx.objects:
    ob.show_in_front=True
    if ob.type=='FONT':ob.color=(.93,.96,.98,1)
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=288
s.display.shading.light='STUDIO';s.display.shading.color_type='OBJECT';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH';s.display.shading.show_specular_highlight=True
s.display.shading.background_type='WORLD';s.world=bpy.data.worlds.new('T41 charcoal field');s.world.color=(.008,.014,.022);s.view_settings.view_transform='Standard'
s['authority']='Isolated T41 experiment. Does not approve production B2/B3 or replace T14/T33/T40.'
s['epistemic_kind']='All signals, time and wall samples illustrative. T6 geometry synthetic. Acoustic faces unverified.'
s['source_contract']='//../direction.md';s['source_refs']=json.dumps(refs)
for f,label in [(1,'A / entry'),(22,'A / first contact'),(33,'A / echo reception'),(73,'B / measurement'),(103,'B / two-way interval'),(169,'C / scan'),(266,'C / completed ring'),(288,'C / handoff')]:s.timeline_markers.new(label,frame=f)
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
for f in [1,22,32,72,81,92,103,130,157,169,210,242,266,288]:
    s.frame_set(f);bpy.context.view_layer.update()
    camera_samples.append(dict(frame=f,location=list(cam.matrix_world.translation),matrix=[list(r) for r in cam.matrix_world],lens=camdata.lens,gaze=list(target.location)))
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
record=dict(scene=str(OUT.relative_to(P)),sources=hashes,refs=refs,events=events,camera_samples=camera_samples,frames=288,fps=24,size=[640,360],wall_x=X,rotation_radians=[rotation(1),rotation(168),rotation(260)],source_mesh_geometry_unchanged=True,viewpoint_convention='+X treated as downhole for test only; mesh end identity unverified',limitations=['Not acoustic simulation','No calibrated acquisition/RPM/TOF','Mud sensor unlocated; correction required but not fabricated','No independent human comprehension or MIT engineering review'])
(E/'build_v003.json').write_text(json.dumps(record,indent=2))
print('T41_BUILD_SAVED',str(OUT))
