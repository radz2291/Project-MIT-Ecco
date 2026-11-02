"""Disposable3s anchored sharp-pulse proof, no shared source amendment."""
import bpy,math,time,json,numpy as np
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';P=Q/'Previews/Waveform-direction-v003';P.mkdir(exist_ok=True)
s=bpy.context.scene
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/Waveform_session_before_quick_pulse.blend'),copy=True,compress=True)
for child in s.view_layers[0].layer_collection.children:child.exclude=True
for ob in list(s.collection.objects):
 if not ob.library:ob.hide_render=True;ob.hide_set(True)
col=bpy.data.collections.new('QUICK anchored evolving waveform');s.collection.children.link(col)
axis=Vector((.3583680987,-.9335803986,0));side=Vector((-.9335803986,-.3583680987,0));up=Vector((0,0,1));gap=.0245758537
strands,samples=5,145
def coordinates(step):
 vs=[]
 for strand in range(strands):
  v=2*strand/(strands-1)-1
  for k in range(samples):
   u=k/(samples-1);env=math.sin(math.pi*u)**2
   signal=0.
   for onset,gain,width in [(3,1.,1.),(18,.75,1.12),(36,.9,.87)]:
    age=((step-onset-16*u)%72)/((1+.35*u)*width)+.10*v
    pulse=-.16*math.exp(-((age-1.3)/.45)**2)+math.exp(-((age-2.1)/.27)**2)-.45*math.exp(-((age-2.7)/.4)**2)+.18*math.exp(-((age-4.3)/.9)**2)
    tail=.08*math.sin(math.tau*(age-5)/2.4)*math.exp(-(age-5)/2.4) if 5<age<12 else 0
    signal+=gain*(pulse+tail)
   z=.011*env*signal/(1+.25*u)
   y=.0015*v*math.sqrt(env);radius=.00008*(.15+.85*math.sqrt(env))
   for ring in range(4):
    a=ring*math.tau/4;vs.append(axis*(gap*u)+side*(y+radius*math.cos(a))+up*(z+radius*math.sin(a)))
 return vs
faces=[]
for strand in range(strands):
 for k in range(samples-1):
  i=(strand*samples+k)*4
  for ring in range(4):faces.append((i+ring,i+(ring+1)%4,i+4+(ring+1)%4,i+4+ring))
mesh=bpy.data.meshes.new('Anchored domain — axis coordinates never move');mesh.from_pydata(coordinates(0),[],faces);mesh.update();field=bpy.data.objects.new('QUICK live bends — stationary field',mesh);col.objects.link(field)
for j in range(strands):
 t=j/(strands-1);m=bpy.data.materials.new('QUICK cyan violet '+str(j));m.diffuse_color=(.08*(1-t)+.02*t,.12*(1-t)+.85*t,.8*(1-t)+1*t,1);mesh.materials.append(m)
for p in mesh.polygons:p.material_index=p.index//((samples-1)*4)
field.shape_key_add(name='Basis');mesh.shape_keys.use_relative=False
for step in range(1,73):
 key=field.shape_key_add(name=f'Bends {step:02}');key.interpolation='KEY_LINEAR';key.data.foreach_set('co',np.array(coordinates(step),dtype=np.float32).reshape(-1))
keys=mesh.shape_keys;keys.eval_time=0;keys.keyframe_insert(data_path='eval_time',frame=1);keys.eval_time=keys.key_blocks[-1].frame;keys.keyframe_insert(data_path='eval_time',frame=73)
for layer in keys.animation_data.action.layers:
 for strip in layer.strips:
  for bag in strip.channelbags:
   for fc in bag.fcurves:
    for k in fc.keyframe_points:k.interpolation='LINEAR'
for end in [0,1]:
 bpy.ops.mesh.primitive_torus_add(major_radius=.011,minor_radius=.00015,major_segments=48,minor_segments=6,location=axis*(end*gap));ob=bpy.context.object;ob.name='QUICK fixed anchor '+str(end);ob.rotation_mode='QUATERNION';ob.rotation_quaternion=Vector((0,0,1)).rotation_difference(axis)
 for prev in list(ob.users_collection):prev.objects.unlink(ob)
 col.objects.link(ob);ob.data.materials.append(mesh.materials[-1])
data=bpy.data.cameras.new('QUICK camera');data.type='ORTHO';data.ortho_scale=.055;data.clip_start=.0001;camera=bpy.data.objects.new(data.name,data);col.objects.link(camera);target=axis*gap*.5;camera.location=target+side*.09+up*.025-axis*.007;camera.rotation_euler=(target-camera.location).to_track_quat('-Z','Y').to_euler();s.camera=camera
s.frame_start=1;s.frame_end=72;s.render.fps=24;s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=False;s.display.shading.show_cavity=False;s.display.render_aa='8';s.view_settings.view_transform='Standard';s.frame_set(14)
for area in bpy.context.screen.areas:
 if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.overlay.show_overlays=False
bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/Waveform_direction_quick_v003.blend'),compress=True)
rows=[]
for f in range(1,73):
 t=time.perf_counter();s.frame_set(f);s.render.filepath=str(P/f'frame_{f:04}.png');bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt})
 if dt>=5:raise RuntimeError('Render cap failed')
s.frame_set(14);(Q/'Notes/wave_direction_quick_v003.json').write_text(json.dumps({'proof':'Three sharp pulses using the user-selected v002 profile. Slight variations in gain, width and spacing; anchored evolving domain and quiet tail. Disposable proof; shared masters unchanged.','frames':72,'fps':24,'rows':rows},indent=2));result={'frames':72,'max_seconds':max(x['seconds'] for x in rows),'native':bpy.data.filepath}
