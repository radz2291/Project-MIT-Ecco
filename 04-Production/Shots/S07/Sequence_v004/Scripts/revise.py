import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion,Matrix
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v003'
for folder in ['Scenes','Records','Previews','Cache']:(B/folder).mkdir(exist_ok=True)
source=P/'Scenes/S07_Monumental-Precision_v003.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
s=bpy.context.scene;cam=s.camera;cd=cam.data;focus=bpy.data.objects['Camera focus target'];old=json.loads((P/'Records/camera-score.json').read_text())
for data in [cam,cd,focus]:data.animation_data_clear()
def sm(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def span(f,a,b):return sm((f-a)/(b-a))
def align(p,t):
 back=(p-t).normalized();axis=Vector((1,0,0));right=(axis-back*axis.dot(back)).normalized();up=back.cross(right)
 return Matrix((right,up,back)).transposed().to_quaternion()
start=old[35];sp=Vector(start['camera']);st=Vector(start['target']);sq=Quaternion(start['quaternion']);aq=align(sp,st);delta=aq.inverted()@sq
initial_roll=2*math.atan2(delta.z,delta.w)
end=Vector((.15,5.3,3.3));endt=Vector((1.2,0,0));endr=math.hypot(end.y,end.z);enda=math.atan2(end.z,-end.y);score=[]
previous_q=None
for f in range(1,193):
 bg=span(f,1,86);orbit=span(f,36,98);travel=span(f,44,114);pull=span(f,114,156)
 bp=Vector((.84,-.66,.31)).lerp(Vector((1.20,-.88,.48)),bg);bt=Vector((.78,0,.015)).lerp(Vector((1.36,0,0)),bg)
 radius=math.hypot(bp.y,bp.z)*(1-orbit)+.82*orbit
 angle=math.atan2(bp.z,-bp.y)*(1-orbit)+math.radians(155)*orbit
 x=bp.x*(1-travel)-.20*travel;tx=bt.x*(1-travel)+.20*travel
 radius=radius*(1-pull)+endr*pull;angle=angle*(1-pull)+enda*pull;x=x*(1-pull)+end.x*pull
 p=Vector((x,-radius*math.cos(angle),radius*math.sin(angle)));t=Vector((tx,0,bt.z*(1-travel))).lerp(endt,pull)
 roll=initial_roll*(1-orbit)+math.radians(-22)*orbit;roll=roll*(1-pull)+math.radians(-48)*pull
 q=align(p,t)@Quaternion((0,0,1),roll)
 if f<=36:
  row=old[f-1];p=Vector(row['camera']);t=Vector(row['target']);q=Quaternion(row['quaternion']);roll=math.radians(row['roll_degrees'])
 if previous_q is not None and q.dot(previous_q)<0:q.negate()
 previous_q=q.copy();cam.location=p;cam.rotation_quaternion=q;cd.shift_x=0;cd.shift_y=0;focus.location=t;cd.dof.aperture_fstop=8+8*pull
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cd.keyframe_insert('shift_x',frame=f);cd.keyframe_insert('shift_y',frame=f);focus.keyframe_insert('location',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f)
 score.append({'frame':f,'camera':list(p),'target':list(t),'quaternion':list(q),'roll_degrees':math.degrees(roll),'azimuth_degrees':math.degrees(angle),'fade_to_black':span(f,164,190)})
for data in [cam,cd,focus]:
 for layer in data.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('S06 handoff',1),('Leave pads and crest shoulder',36),('Rear face reveal',76),('Travel past rear hardware',94),('End collar arrival',114),('Centered rear hero',156),('Fade to black',164),('Black endpoint',190)]:s.timeline_markers.new(name,frame=f)
s['revision']='v004 continuous rear-face traverse and collar reveal; centered hero and fade to black'
s.frame_set(160);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v004.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2))
(B/'Records/revision.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'duration':8,'frames':192,'continuous_product_camera':True,'branding_removed':True,'camera_change':'Crest pad shoulder, cross to positive-Y rear face, track toward collar, retreat from rear side','black_endpoint_frame':190,'unchanged':'hardware geometry, materials, lights, first 36 camera frames and S06 handoff'},indent=2))
print('v004 BUILT')
