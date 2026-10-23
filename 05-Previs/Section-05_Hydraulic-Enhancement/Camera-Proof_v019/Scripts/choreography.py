import bpy,math,json,time
from pathlib import Path
from mathutils import Vector
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;cam=s.camera
ns={'__file__':str(B/'Scripts/camera_study.py'),'MODE':'functions'};exec(compile((B/'Scripts/camera_study.py').read_text(),ns['__file__'],'exec'),ns)
pose=ns['pose']
def ease(q):
 q=max(0,min(1,q));return q*q*q*(10+q*(-15+q*6))
def mix(a,b,t):return [x+(y-x)*t for x,y in zip(a,b)]
# Arrivals chosen from actual rendered geometry before these paths were authored.
keys=[
 (1,[.78,-36,-.96,-.12,34,-14,-.03,0]),
 (84,[1.04,-18,-.53,.12,42,-23,-.03,0]),
 (120,[1.055,-17,-.52,.125,42,-23,-.03,0]),
 (121,[1.25,-17,.55,.30,46,-38,.025,.025]),
 (165,[1.06,12,.30,.25,50,-58,.025,.025]),
 (246,[1.06,12,.45,.40,50,-58,.025,.025]),
 (330,[1.10,8,1.03,.83,50,-58,.01,.015]),
 (402,[1.95,8,1.05,.42,46,-66,0,0]),
 (432,[1.95,8,1.05,.42,46,-66,0,0])]
cam.animation_data_clear();cam.data.animation_data_clear();rows=[];lastq=None
for f in range(1,433):
 s.frame_set(f)
 i=max(i for i,(kf,kp) in enumerate(keys) if kf<=f)
 if i==len(keys)-1:p=keys[i][1]
 else:
  a,pa=keys[i];b,pb=keys[i+1];p=mix(pa,pb,ease((f-a)/(b-a)))
 pose(*p)
 if lastq and cam.rotation_quaternion.dot(lastq)<0:cam.rotation_quaternion.negate()
 lastq=cam.rotation_quaternion.copy()
 for prop in ['location','rotation_quaternion']:cam.keyframe_insert(prop,frame=f)
 for prop in ['lens','shift_x','shift_y']:cam.data.keyframe_insert(prop,frame=f)
 rows.append({'frame':f,'seconds':(f-1)/24,'location':list(cam.location),'quaternion':list(cam.rotation_quaternion),'lens':cam.data.lens,'target':[0,0,p[3]],'parameters':p})
for id in [cam,cam.data]:
 id.animation_data.action.name='v019_CAMERA_'+('Object' if id==cam else 'Optics')
 for layer in id.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('A / rise through annulus',1),('A / sculptural arrival',84),('B / silhouette to passage CUT',121),('B / mechanism arrival',165),('B to C / follow departure',246),('C / downstream detail',330),('C / integrated arrival',402)]:s.timeline_markers.new(name,frame=f)
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.eevee.taa_render_samples=6
bench=[]
for label,f in [('entry',1),('A_arrival',96),('A_exit',120),('B_entry',121),('B_arrival',205),('B_departure',246),('C_entry',289),('C_detail',330),('C_arrival',420)]:
 s.frame_set(f);s.render.filepath=str(B/'Previews'/(label+'.png'));t=time.perf_counter();bpy.ops.render.render(write_still=True);secs=time.perf_counter()-t;assert secs<5
 bench.append({'label':label,'frame':f,'seconds':secs})
(B/'Records/arrival-benchmarks.json').write_text(json.dumps(bench,indent=2));(B/'Records/camera-transforms.json').write_text(json.dumps(rows))
s.render.resolution_x=960;s.render.resolution_y=540;s.render.resolution_percentage=100;s.eevee.taa_render_samples=4
s.frame_set(205);s.render.filepath='//../Previews/B_arrival.png'
s['production_scope']='v019 camera-only direction proof, 18s; approved v018 geometry/materials/hydraulic animation preserved. Not final production render.'
bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S05_camera-direction_v019.blend'))
result={'stills':bench,'playblast':[960,540,24,432],'camera_cut_frame':121,'motion':'Rise and settle; partial arc and observation; continuous lift then retreat/pivot to final held image.'}
