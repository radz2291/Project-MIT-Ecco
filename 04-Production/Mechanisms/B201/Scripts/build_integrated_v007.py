"""B2 on-model pulse/echo scene. Isolated Blender only; no master edits.

All signal shapes, colors, time and traces are illustrative. T6 evaluated wall
coordinates and T5 surface-ray origins determine the actual geometry of paths.
"""
import bpy,math,json,hashlib,time,sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';R=P/'Records/Tasks/T-007/Evidence/v007'
OUT=M/'Scenes/B201_integrated_v007.blend';FR=M/'Previews/v007/Frames'
if OUT.exists():raise RuntimeError('Refuse overwrite: preserve edited scene, version before rebuild')
sources=[P/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend',P/'Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend']
hashes={str(p.relative_to(P)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
assert hashes['Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend']=='704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7'
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
with bpy.data.libraries.load(str(sources[0]),link=False) as (a,b):b.collections=['WELL_ASSEMBLY_v003']
s.collection.children.link(b.collections[0]);rig=bpy.data.objects['ASSEMBLY_CONTROL']
for k,v in dict(travel_m=2.07,rotation_rad=0.,variant=1,cutaway=0,show_open=1,show_casing=0,show_cement=0,show_hardware=1,show_proxies=0).items():rig[k]=v
rig.update_tag();bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get()
wall=bpy.data.objects['IRREGULAR_FULL'];evaluated=wall.evaluated_get(dg)
def wallhit(a):
 d=Vector((0,math.cos(a),math.sin(a)));p,n,i,dist=wall_bvh.ray_cast(Vector((2.8,0,0)),d);assert p is not None;return p,d,n
# Reuse exact evaluated T6 vertices, removing a front viewing window only.
me=evaluated.to_mesh();verts=[v.co.copy() for v in me.vertices];faces=[]
wall_bvh=BVHTree.FromPolygons(verts,[list(f.vertices) for f in me.polygons])
for f in me.polygons:
 mid=sum((verts[i] for i in f.vertices),Vector())/len(f.vertices);a=math.degrees(math.atan2(mid.z,mid.y))%360
 if 2.0<=mid.x<=4.9 and not 165<a<270:faces.append(list(f.vertices))
evaluated.to_mesh_clear()
def coll(n):c=bpy.data.collections.new(n);s.collection.children.link(c);return c
env=coll('B201_REGISTERED_WALL_CUTAWAY');fx=coll('B201_PULSE_ECHO');history=coll('B201_CONTACT_HISTORY');gfx=coll('B201_SPATIAL_GRAPHICS');review=coll('B201_REVIEW_CAMERA')
mesh=bpy.data.meshes.new('T6 exact evaluated cutaway vertices');mesh.from_pydata(verts,[],faces);mesh.update()
viewwall=bpy.data.objects.new('T6_IRREGULAR_VIEW_WINDOW',mesh);env.objects.link(viewwall);viewwall.color=(.12,.16,.18,1)
viewwall['provenance']='T6 v003 evaluated IRREGULAR_FULL; retained exact vertices/faces. Front window165..270degrees, X2.0..4.9m. Explanatory removal only.'
for poly in mesh.polygons:poly.use_smooth=True
rig['show_open']=0;rig.update_tag();bpy.context.view_layer.update()
control=bpy.data.objects.new('B201_CONTROL',None);fx.objects.link(control)
for k,v in dict(signals=1.,wall=1.,waveforms=1.,contact_history=1.,contact_hold_frames=120.,signal_radius_m=.0025,spot_radius_m=.008).items():control[k]=v
control['interpretation']='Illustrative signal/time/glyph. No calibrated acoustic face/field data/RPM.'
control['geometry_edit']='Rebuild/version/reverify after changing source geometry or acquisition angles.'
def driver(o,path,expr,vars=None,index=None):
 fc=o.driver_add(path) if index is None else o.driver_add(path,index);d=fc.driver;d.type='SCRIPTED';d.expression=expr
 for name,prop in (vars or {}).items():
  v=d.variables.new();v.name=name;v.type='SINGLE_PROP';v.targets[0].id=control;v.targets[0].data_path='["'+prop+'"]'
 return fc
driver(viewwall,'hide_render','v<.5',{'v':'wall'})
def link(o,c):
 for cc in list(o.users_collection):cc.objects.unlink(o)
 c.objects.link(o)
def ball(n,r,color,c=fx):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=r);o=bpy.context.object;o.name=n;link(o,c);o.color=(*color,1);return o
def curve(n,pts,width,color,c=gfx):
 data=bpy.data.curves.new(n,'CURVE');data.dimensions='3D';data.bevel_depth=width;data.bevel_resolution=2;sp=data.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,q in zip(sp.points,pts):p.co=(*q,1)
 o=bpy.data.objects.new(n,data);c.objects.link(o);o.color=(*color,1);return o
def show(o,condition,group='waveforms'):
 for path in ('hide_render','hide_viewport'):driver(o,path,f'not ({condition}) or v<.5',{'v':group})
 for axis in range(3):driver(o,'scale',f'1 if ({condition}) and v>=.5 else 0',{'v':group},axis)
def linear(o):
 if o.animation_data and o.animation_data.action:
  for fc in o.animation_data.action.layers[0].strips[0].channelbag(o.animation_data.action_slot).fcurves:
   for k in fc.keyframe_points:k.interpolation='LINEAR'
ref=bpy.data.objects['ECCO_SENSOR_REF_01'];base=ref.matrix_world.translation;ba=math.atan2(base.z,base.y);db=Vector((0,math.cos(ba),math.sin(ba)))
surface=0.;hitname=None
for o in bpy.data.collections['ECCO_MASTER_v002'].all_objects:
 if o.type!='MESH' or o.hide_render:continue
 inv=o.matrix_world.inverted();ok,p,n,i=o.ray_cast(inv@(Vector((.73,0,0))+db*.25),(inv.to_3x3()@(-db)).normalized())
 if ok:
  p=o.matrix_world@p;radius=p.y*db.y+p.z*db.z
  if radius>surface:surface=radius;hitname=o.name
assert .12<surface<.153
events=[]
for j,deg in enumerate((114,122,130,138,146,154)):
 start=1+j*72;a=math.radians(deg);rot=a-ba
 for f in (start,start+59):rig['rotation_rad']=rot;rig.keyframe_insert(data_path='["rotation_rad"]',frame=f)
 wallp,d,normal=wallhit(a);origin=Vector((2.8,0,0))+d*(surface+.0004);distance=(wallp-origin).length;leg=round(distance/.0025)
 emit=start+10;contact=emit+leg;receive=contact+leg;assert receive<start+58
 for k,v in {f'emit_{j+1}':emit,f'leg_{j+1}':leg}.items():control[k]=float(v)
 var={'e':f'emit_{j+1}','d':f'leg_{j+1}'}
 tx=ball(f'TX_{j+1}',.0025,(.28,.88,1.));echo=ball(f'ECHO_{j+1}',.0025,(1.,.64,.25));marker=ball(f'EMITTER_{j+1}',.002,(.34,.86,1.))
 for o,expr in [(tx,'min(max((frame-e)/d,0),1)'),(echo,'1-min(max((frame-e-d)/d,0),1)')]:
  for axis in range(3):driver(o,'location',f'{origin[axis]:.10f}+({wallp[axis]-origin[axis]:.10f})*({expr})',var,axis)
 for o,cond in [(tx,'frame>=e and frame<e+d'),(echo,'frame>=e+d and frame<=e+2*d')]:
  for path in ('hide_render','hide_viewport'):driver(o,path,f'not ({cond}) or v<.5',{**var,'v':'signals'})
  for axis in range(3):driver(o,'scale',f'rad/.0025 if ({cond}) and v>=.5 else 0',{**var,'rad':'signal_radius_m','v':'signals'},axis)
 marker.location=origin;show(marker,f'{start}<=frame<={receive+7}','signals')
 spot=ball(f'WALL_CONTACT_{j+1}',.008,(.57,.85,.86));spot.location=wallp
 driver(spot,'hide_render','frame<e+d or frame>e+d+12 or v<.5',{**var,'v':'signals'})
 for axis in range(3):driver(spot,'scale','rad/.008*min(max(0,1-(frame-e-d)/12),1) if frame>=e+d and v>=.5 else 0',{**var,'rad':'spot_radius_m','v':'signals'},axis)
 # A tiny retained wall mark carries discovery; no full measured ring is implied.
 mark=ball(f'CONTACT_AFTERMARK_{j+1}',.0014,(.26,.46,.49),history);mark.location=wallp
 driver(mark,'hide_render','frame<e+d or frame>e+d+h or v<.5',{**var,'h':'contact_hold_frames','v':'contact_history'})
 for axis in range(3):driver(mark,'scale','1 if e+d<=frame<=e+d+h and v>=.5 else 0',{**var,'h':'contact_hold_frames','v':'contact_history'},axis)
 events.append(dict(cycle=j+1,start=start,angle_rad=a,rotation_rad=rot,emit=emit,contact=contact,receive=receive,leg_frames=leg,origin=list(origin),wall=list(wallp),wall_normal=list(normal),standoff_m=distance,surface=hitname))
linear(rig)
# A representative static film view; exact framing is checked on saved renders.
bpy.ops.object.camera_add(location=(1.85,-1.55,.18));cam=bpy.context.object;cam.name='B201_FILM_VIEW';link(cam,review)
target=Vector((3.05,-.02,.04));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',math.radians(-12))
cam.data.type='ORTHO';cam.data.ortho_scale=1.15;cam.data.clip_start=.03;cam.data.clip_end=30;s.camera=cam
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=432
s.render.engine='BLENDER_WORKBENCH';s.display.shading.light='STUDIO';s.display.shading.studiolight_rotate_z=.4;s.display.shading.color_type='OBJECT';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.cavity_type='BOTH'
s.world=bpy.data.worlds.new('B201 neutral dark field');s.world.color=(.012,.019,.027);s.display.shading.background_type='WORLD';s.view_settings.view_transform='Standard'
bpy.context.view_layer.update();q=cam.rotation_euler.to_quaternion();right=q@Vector((1,0,0));up=q@Vector((0,1,0));forward=q@Vector((0,0,-1))
def screen(x,y,depth=1.4):return cam.location+forward*depth+right*((x/1280-.5)*1.15)+up*((.5-y/720)*1.15*720/1280)
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf');font.pack()
def text(n,body,x,y,size,color=(.68,.76,.79),condition=None):
 d=bpy.data.curves.new(n,'FONT');d.body=body;d.font=font;d.size=size*1.15/1280;d.space_character=1.04
 o=bpy.data.objects.new(n,d);gfx.objects.link(o);o.location=screen(x,y);o.rotation_euler=cam.rotation_euler;o.color=(*color,1)
 if condition:show(o,condition)
 return o
text('B2 review caption','B201 / PROPOSED ENGINEERING SCENE',44,44,15)
text('Meaning','One pulse. One returning echo.',44,89,29,condition='frame>=217')
text('Illustrative provenance','Illustrative signals + timing / not field data',44,687,17)
text('Origin limit','Documented sensor reference / acoustic face unverified',44,662,15)
text('Graphic meaning','Round-trip time',763,402,20,condition='frame>=217')
text('Formula','Stand-off = c_mud × Δt / 2',763,633,18,condition='frame>=253')
text('Correction caveat','Mud velocity + sensor offset / eccentricity required',763,656,14,condition='frame>=253')
for j,e in enumerate(events[3:]):
 y=450+j*62;x0=794;scale=7.0;delay=e['receive']-e['emit'];pts=[]
 for k in range(401):
  t=-3+k*53/400;val=21*math.exp(-(t/.65)**2)-7*math.exp(-((t-1.3)/.75)**2)+16*math.exp(-((t-delay)/.75)**2)-5*math.exp(-((t-delay-1.4)/.9)**2)
  pts.append(screen(x0+t*scale,y-val))
 trace=curve(f'EVENT_TRACE_{j+4}',pts,.0009,(.28,.83,.91));show(trace,f'frame>={e["start"]}')
 driver(trace.data,'bevel_factor_end','min(max((frame-e+3)/53,0),1)',{'e':f'emit_{j+4}'})
 baseline=curve(f'TRACE_BASE_{j+4}',[screen(x0-21,y),screen(x0+350,y)],.00035,(.18,.28,.32));show(baseline,f'frame>={e["start"]}')
 text(f'Trace ID{j}',chr(65+j),763,y+4,14,condition=f'frame>={e["start"]}')
 text(f'Tx label{j}','Tx',x0-6,y+22,13,condition=f'frame>={e["emit"]}')
 text(f'Echo label{j}','Echo',x0+delay*scale-15,y+22,13,(.85,.61,.33),f'frame>={e["receive"]}')
 bracket=curve(f'ROUND_TRIP_{j+4}',[screen(x0,y-29),screen(x0+delay*scale,y-29)],.00065,(.89,.64,.34));show(bracket,f'frame>={e["receive"]}')
 text(f'Delta t{j}','Δt',1173,y-25,13,(.89,.64,.34),f'frame>={e["receive"]}')
 leader=curve(f'EMITTER_TO_TRACE_{j+4}',[Vector(e['origin']),screen(710,431),screen(x0-21,y)],.00035,(.25,.39,.43));show(leader,f'{e["emit"]}<=frame<={e["receive"]+10}')
 text(f'Explanation phase{j}','Echo received',995,377,16,(.87,.66,.38),f'{e["receive"]}<=frame<={e["start"]+59}')
s['direction_contract']='//../direction.md';s['candidate']='B2 proposed model-integrated v007; not client-approved';s['graphics']='Editable spatial explanatory layer; no instrument/field-data display claim'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
s.render.image_settings.file_format='PNG';s.render.filepath='//../Previews/v007/Frames/frame_'
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
projection=[]
for e in events:
 a=world_to_camera_view(s,cam,Vector(e['origin']));b=world_to_camera_view(s,cam,Vector(e['wall']))
 projection.append(dict(cycle=e['cycle'],origin=list(a),wall=list(b),gap_px=math.hypot((a.x-b.x)*1280,(a.y-b.y)*720)))
evidence=dict(inputs=hashes,scene_sha256=hashlib.sha256(OUT.read_bytes()).hexdigest(),events=events,projection=projection,wall_vertices=len(verts),wall_faces=len(faces),camera={'location':list(cam.location),'rotation_euler':list(cam.rotation_euler),'projection':'ORTHO','ortho_scale':cam.data.ortho_scale},blender=bpy.app.version_string)
(R/'build_v007.json').write_text(json.dumps(evidence,indent=2));print('INTEGRATED_BUILD_PASS')
if '--stills' in sys.argv:
 for frame in (1,24,36,90,160,240,260,330,400,432):
  s.frame_set(frame);bpy.context.view_layer.update();s.render.filepath=str(M/f'Previews/v007/B201_frame_{frame:04}_v007.png');bpy.ops.render.render(write_still=True)
if '--render' in sys.argv:
 bpy.ops.wm.open_mainfile(filepath=str(OUT));t=time.perf_counter();bpy.ops.render.render(animation=True);evidence['render_seconds']=time.perf_counter()-t
 (R/'render_v007.json').write_text(json.dumps(evidence,indent=2));print('INTEGRATED_RENDER_PASS',evidence['render_seconds'])
