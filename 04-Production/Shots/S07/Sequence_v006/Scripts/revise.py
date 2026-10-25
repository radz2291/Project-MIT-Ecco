import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v005'
for folder in ['Scenes','Records','Previews','Cache']:(B/folder).mkdir(exist_ok=True)
source=P/'Scenes/S07_Monumental-Precision_v005.blend';bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;cam=s.camera;cd=cam.data;focus=bpy.data.objects['Camera focus target']
score=json.loads((P/'Records/camera-score.json').read_text());center=Vector((1.2,0,0));base=(Vector(score[-1]['camera'])-center)/1.07
def pull(f):
 if f>=156:return 1.03+.04*(f-156)/36
 u=(f-121)/35
 if u<=.22:q=1.3*u
 else:
  t=(u-.22)/.78;q0=1.3*.22;m0=1.3*.78;m1=(.04/36/.69*35)*.78
  q=(2*t**3-3*t*t+1)*q0+(t**3-2*t*t+t)*m0+(-2*t**3+3*t*t)+(t**3-t*t)*m1
 return .34+.69*q
for f in range(121,193):
 scale=pull(f);progress=min(1,(scale-.34)/.69);p=center+base*scale;roll=-42-6*progress;q=(center-p).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
 cam.location=p;cam.rotation_quaternion=q;focus.location=center;cd.shift_x=0;cd.shift_y=0;cd.dof.aperture_fstop=10+6*progress
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);focus.keyframe_insert('location',frame=f);cd.keyframe_insert('shift_x',frame=f);cd.keyframe_insert('shift_y',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f)
 row=score[f-1];row.update({'camera':list(p),'target':list(center),'quaternion':list(q),'roll_degrees':roll,'pullback_scale':scale})
for data in [cam,cd,focus]:
 for layer in data.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT' if round(k.co[0]) in [60,120] else 'LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('SHOT 1 | unchanged',1),('SHOT 2 | unchanged',61),('SHOT 3 | close moving pullback',121),('Pullback settles into full hero',156),('Fade to black',164),('Black endpoint',190)]:s.timeline_markers.new(name,frame=f)
s['revision']='v006 | first two shots preserved; third shot begins close at moving speed, strong retreat then gentle hero drift; no logo and black ending'
s.frame_set(160);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v006.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2));(B/'Records/revision.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'changed_frames':[121,192],'unchanged_frames':[1,120],'duration':8,'frames':192,'cut_frames':[61,121],'third_shot':'Linear moving entry for first eight frames, strong pullback easing into slow hero drift','source_geometry_material_lighting_changes':False,'branding_removed':True,'black_endpoint_frame':190},indent=2));print('v006 BUILT')
