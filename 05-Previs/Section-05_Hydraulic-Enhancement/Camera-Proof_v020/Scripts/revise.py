import bpy,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'Camera-Proof_v019';s=bpy.context.scene;cam=s.camera
source=Path(bpy.data.filepath);assert source.name=='S05_camera-direction_v019.blend'
(B/'Records/source-baseline.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_continuous-camera_v020.blend'))
s.frame_set(151);bpy.context.view_layer.update();vs=[];fs=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vs);vs.extend(o.matrix_world@v.co for v in o.data.vertices);fs.extend([[off+i for i in p.vertices] for p in o.data.polygons])
steel=BVHTree.FromPolygons(vs,fs);a=math.radians(-30);radial=Vector((math.cos(a),math.sin(a),0))
hit=steel.ray_cast(Vector((0,0,.04))+radial*.18,-radial,.18);assert hit[0] is not None
landmark=hit[0];root=bpy.data.objects['S05_COMMON_AXIAL_ROTATION'];prior=json.loads((OLD/'Records/camera-transforms.json').read_text())
def ease(q):
 q=max(0,min(1,q));return q*q*q*(10+q*(-15+q*6))
def mix(a,b,t):return [x+(y-x)*t for x,y in zip(a,b)]
entry=[1.10,-30,-.44,42,-23,.045,0]
arrival=[1.02,-12,-.20,44,-28,.045,0]
bridge=[1.06,12,.30,50,-58,.025,.025]
cam.animation_data_clear();cam.data.animation_data_clear();rows=[]
for f in range(1,433):
 s.frame_set(f);bpy.context.view_layer.update()
 if f<165:
  tracking=Matrix.Rotation(root.rotation_euler.z,4,'Z')@landmark
  if f<=72:p=mix(entry,arrival,ease((f-1)/71));target=tracking;blend=0
  else:
   blend=ease((f-72)/93);p=mix(arrival,bridge,blend);target=tracking.lerp(Vector((0,0,.25)),blend)
  d,az,z,lens,roll,sx,sy=p;az=math.radians(az);cam.location=(d*math.cos(az),d*math.sin(az),z)
  cam.rotation_mode='QUATERNION';cam.rotation_quaternion=(target-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
  cam.data.lens=lens;cam.data.shift_x=sx;cam.data.shift_y=sy
  params=[d,math.degrees(az),z,target.z,lens,roll,sx,sy]
 else:
  r=prior[f-1];cam.location=r['location'];cam.rotation_quaternion=r['quaternion'];cam.data.lens=r['lens'];cam.data.shift_x=r['parameters'][6];cam.data.shift_y=r['parameters'][7];target=Vector(r['target']);params=r['parameters'];blend=1
 for prop in ['location','rotation_quaternion']:cam.keyframe_insert(prop,frame=f)
 for prop in ['lens','shift_x','shift_y']:cam.data.keyframe_insert(prop,frame=f)
 rows.append({'frame':f,'seconds':(f-1)/24,'location':list(cam.location),'quaternion':list(cam.rotation_quaternion),'lens':cam.data.lens,'target':list(target),'parameters':params,'gaze_transfer_to_B':blend})
for id in [cam,cam.data]:
 id.animation_data.action.name='v020_CAMERA_CONTINUOUS'
 for layer in id.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('A / track actual lower steel feature',1),('A to B / continuous attention transfer',72),('B / retained interaction arrival',165),('B to C / retained follow',246),('C / retained detail',330),('C / retained final arrival',402)]:s.timeline_markers.new(name,frame=f)
(B/'Records/camera-transforms.json').write_text(json.dumps(rows))
(B/'Records/focus-landmark.json').write_text(json.dumps({'zero_rotation_surface_point':list(landmark),'actual_source_surface':True,'source_face_index':hit[2],'description':'Ray-selected source steel point at world Z0.04m in the lower morphological working region; tracked with connected hardware rotation through frame72, then gaze blends toward B. Functional face identity remains illustrative.'},indent=2))
s.render.resolution_x=960;s.render.resolution_y=540;s.eevee.taa_render_samples=4
bench=[]
for label,f in [('A_entry',1),('A_track',48),('A_arrival',72),('transfer_96',96),('transfer_120',120),('transfer_121',121),('transfer_144',144),('B_arrival',165)]:
 s.frame_set(f);s.render.filepath=str(B/'Previews'/(label+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);sec=time.perf_counter()-t;assert sec<5;bench.append({'frame':f,'seconds':sec})
(B/'Records/benchmark.json').write_text(json.dumps(bench,indent=2));s.frame_set(72);s.render.filepath='//../Previews/A_arrival.png'
s['production_scope']='v020 continuous camera proof. A tracks real steel landmark then transfers focus continuously into retained B; frame165 onward retains v019 exactly. Hydraulic content unchanged.'
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_continuous-camera_v020.blend'))
result={'landmark':list(landmark),'cut_frames':[],'retained_frames':'165-432','benchmarks':bench}
