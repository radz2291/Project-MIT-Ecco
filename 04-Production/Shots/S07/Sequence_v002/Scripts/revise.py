import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v001'
source=P/'Scenes/S07_Monumental-Precision_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;cam=s.camera;cd=cam.data;focus=bpy.data.objects['Camera focus target']
score=json.loads((P/'Records/camera-score.json').read_text())
def sm(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def span(f,a,b):return sm((f-a)/(b-a))
def pose(loc,target,roll):return (target-loc).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
entry=Vector((1.82,-.53,.54));entrytarget=Vector((1.13,0,0))
depart=Vector((1.72,-.59,.49));departtarget=Vector((1.11,0,0))
end=Vector(score[-1]['camera']);endtarget=Vector(score[-1]['target'])
for f in range(61,146):
 s.frame_set(f);g=span(f,61,100);p=span(f,94,146)
 loc=entry.lerp(depart,g).lerp(end,p);target=entrytarget.lerp(departtarget,g).lerp(endtarget,p);roll=(-18-6*g)*(1-p)-48*p
 cam.location=loc;cam.rotation_quaternion=pose(loc,target,roll);cd.shift_x=.16*p;focus.location=target;cd.dof.aperture_fstop=8+8*p
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cd.keyframe_insert('shift_x',frame=f);focus.keyframe_insert('location',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f)
 d=(loc-target).length
 for name,x,y in [('Product identification',.225,.018),('MIT logo placeholder',.225,-.016)]:
  o=bpy.data.objects[name];o.location=(x*d,y*d,-d);o.scale=(d,)*3;o.keyframe_insert('location',frame=f);o.keyframe_insert('scale',frame=f)
 score[f-1]={'frame':f,'camera':list(loc),'target':list(target),'roll_degrees':roll,'shift_x':cd.shift_x,'beat':'Second beauty angle' if f<95 else 'Retreat to original wide'}
for data in [cam,focus,cd]+[bpy.data.objects[x] for x in ['Product identification','MIT logo placeholder']]:
 ad=data.animation_data
 if not ad or not ad.action:continue
 for layer in ad.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:
      k.interpolation='CONSTANT' if int(k.co[0])==60 else 'LINEAR'
for name,f in [('Detail 1 | source shoulder',1),('Detail 2 | reverse three-quarter beauty',61),('Retreat',95),('Original wide and identity hold',146)]:s.timeline_markers.new(name,frame=f)
s['revision']='v002 adds a second beauty shot; deliberate cut f60 to61; original opening and final wide retained'
s.frame_set(192);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v002.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2))
(B/'Records/revision.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changed_frames':[61,145],'reused_frames':[[1,60],[146,192]],'duration_seconds':8,'purpose':'Add a reverse three-quarter pad beauty close-up before the full-product reveal','hardware_material_lighting_changes':False,'deliberate_cut_frame':61},indent=2))
print('REVISED v002')
