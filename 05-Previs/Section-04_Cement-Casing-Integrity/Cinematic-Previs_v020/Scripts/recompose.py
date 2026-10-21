import bpy,sys,json,math,time,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];P=B.parent;SRC=P/'Cinematic-Previs_v019/Scenes/S04_continuous-camera_v019.blend';CSRC=P/'Cinematic-Previs_v019/Scenes/S04_C_comparison-window_v019.blend';OUT=B/'Scenes/S04_sequential-camera_v020.blend'
PHI=math.radians(39);R=Vector((0,math.cos(PHI),math.sin(PHI)));N=Vector((0,-math.sin(PHI),math.cos(PHI)))
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def fc(action):
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:yield from bag.fcurves
def graphic(name):return name.startswith(('STEEL-ATTACHED resonance band','STEEL THICKNESS response','STEEL-BOUND acquisition segment','S02 sourced','Casing response tail'))
def ids(objects):
 found=set()
 for o in objects:
  found.add(o)
  if o.data:
   found.add(o.data)
   if hasattr(o.data,'materials'):
    for m in o.data.materials:
     if m:found.add(m)
 return found
def retime(objects,origin,start,rate):
 copied={};count=0
 for item in ids(objects):
  if not item.animation_data or not item.animation_data.action:continue
  old=item.animation_data.action
  if old not in copied:
   a=old.copy();copied[old]=a
   for curve in fc(a):
    for k in curve.keyframe_points:
     k.co.x=start+(k.co.x-origin)*rate;k.handle_left.x=start+(k.handle_left.x-origin)*rate;k.handle_right.x=start+(k.handle_right.x-origin)*rate
   count+=1
  item.animation_data.action=copied[old]
 return count
def geometry(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH' and not graphic(o.name)}
def camera_quat(pos,target,roll):
 f=(target-pos).normalized();axis=Vector((1,0,0));right=(axis-f*axis.dot(f)).normalized();up=(-f).cross(right).normalized();return Matrix((right,up,-f)).transposed().to_quaternion()@Quaternion((0,0,1),math.radians(roll))
def build():
 bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='S04 sequential A B C D - one camera v020';s.frame_set(1);before=geometry(s)
 effectsB=[o for o in s.objects if graphic(o.name)];bcount=retime(effectsB,121,63,.64)
 with bpy.data.libraries.load(str(CSRC),link=False) as (a,b):b.objects=[n for n in a.objects if graphic(n)]
 effectsC=[o for o in b.objects if o]
 for o in effectsC:s.collection.objects.link(o)
 ccount=retime(effectsC,1,175,.64)
 # Existing authored geometry and fixed 50% section remain identical.
 assert before==geometry(s)
 w=bpy.data.objects['WORLD_CONTROL'];w.animation_data_clear();motion=[(1,.25),(63,-1.05),(141,-1.05),(175,-2.23),(261,-2.23),(316,-5.8),(432,-5.8)]
 for frame in range(1,433):
  a,b=next(((a,b) for a,b in zip(motion,motion[1:]) if a[0]<=frame<=b[0]),(motion[-2],motion[-1]));u=sm((frame-a[0])/(b[0]-a[0]));w['travel_m']=(1-u)*a[1]+u*b[1];w.keyframe_insert(data_path='["travel_m"]',frame=frame)
 for curve in fc(w.animation_data.action):
  for k in curve.keyframe_points:k.interpolation='LINEAR'
 # Remove transparent face-sorting artifacts in the inexpensive channel proxy.
 channel=bpy.data.objects['Stationary organic fluid-filled channel volume'];m=channel.data.materials[0].copy();channel.data.materials[0]=m;c=list(m.diffuse_color);c[3]=1;m.diffuse_color=c
 # Section faces carry plain steel, never the inner-surface loss-data layer.
 steel=bpy.data.objects['STEEL - capped true source section'];base=steel.data.materials[0];cap=base.copy();cap.name='Plain stationary steel cut faces v020';nt=cap.node_tree;out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');mix=out.inputs['Surface'].links[0].from_node;plain=mix.inputs[1].links[0].from_socket;nt.links.new(plain,out.inputs['Surface']);steel.data.materials.append(cap)
 for p in steel.data.polygons:
  if abs(p.normal.dot(N))>.99 or abs(p.normal.x)>.99:p.material_index=1
 # Compose complete wide arrivals before joining them: no half-frame camera shift.
 def eye(x):return Vector((x-.15,0,0))+R*.35+N*.45
 def target(x):return Vector((x,0,0))+R*.145
 poses=[(1,Vector((.85,0,0))+R*.70+N*1.05,Vector((.10,0,0))+R*.04,32,-18),
        (63,eye(-.32),target(-.32),42,-18),(141,eye(-.32),target(-.32),42,-18),
        (175,eye(-1.5),target(-1.5),42,-18),(261,eye(-1.5),target(-1.5),42,-18),
        (318,Vector((-1.1,-.02,.06)),Vector((-1.87,.12,-.025)),38,-13),
        (432,Vector((-1.1,-.02,.06)),Vector((-1.87,.12,-.025)),38,-13)]
 cam=s.camera;cam.animation_data_clear();cam.data=cam.data.copy();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION';cam.data.shift_x=0;cam.data.sensor_fit='HORIZONTAL';score=[];previous=None
 for frame in range(1,433):
  a,b=next(((a,b) for a,b in zip(poses,poses[1:]) if a[0]<=frame<=b[0]),(poses[-2],poses[-1]));u=sm((frame-a[0])/(b[0]-a[0]));pos=a[1].lerp(b[1],u);tar=a[2].lerp(b[2],u);roll=(1-u)*a[4]+u*b[4];q=camera_quat(pos,tar,roll)
  if previous and previous.dot(q)<0:q.negate()
  previous=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=(1-u)*a[3]+u*b[3]
  cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame);cam.data.keyframe_insert('lens',frame=frame)
  score.append({'frame':frame,'eye_m':list(pos),'target_m':list(tar),'lens_mm':cam.data.lens,'roll_degrees':roll})
 for item in [cam,cam.data]:
  for curve in fc(item.animation_data.action):
   for k in curve.keyframe_points:k.interpolation='LINEAR'
 s['scope']='Owner revision: improve ALL camera compositions, full-frame B followed by C, faster illustrative response/travel, one continuous camera, permanent fixed half section. No split screen or comparison insert.'
 s['director_application']='Authored diagonal wide arrivals; same relative B/C view; faster axial tracking reveals two fixed backing locations; move tool clear before D so complete curvature can be inspected. Preserve source-derived engineering geometry.'
 s.frame_start=1;s.frame_end=432;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.compression=10
 s.frame_set(1)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
 dump('build.json',{'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'source_C':str(CSRC),'source_C_sha256':hashlib.sha256(CSRC.read_bytes()).hexdigest(),'physical_meshes_unchanged':True,'fixed_section_unchanged':True,'B_effect_objects':len(effectsB),'C_effect_objects':len(effectsC),'B_retimed_actions':bcount,'C_retimed_actions':ccount,'B_source_time_scale':.64,'C_source_time_scale':.64,'B_source_start_frame':63,'C_source_start_frame':175,'hardware_motion':motion,'camera':cam.name,'split_screen':False,'C_overlay':False,'channel_proxy_alpha':1,'cut_faces_plain_steel':True,'geometry_fingerprints':before})
 dump('camera-score.json',score)
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 frames=[1,63,85,141,158,175,198,240,290,318,400] if mode=='bench' else (range(175,262) if mode=='patch' else range(1,433))
 if mode in ['render','patch']:
  check=json.loads((B/'Records/timings-bench.json').read_text());assert len(check)>=4 and max(x['seconds'] for x in check)<5
 for frame in frames:
  s.frame_set(frame);s.render.filepath=str(B/('Previews' if mode=='bench' else 'Work/Frames')/f'S04_{frame:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':frame,'seconds':dt});dump('timings-'+mode+'.json',rows);print('FRAME',frame,dt,flush=True)
  if dt>=5:raise RuntimeError('Strict frame cap exceeded')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
