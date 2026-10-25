import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v002';A=B.parent/'Sequence_v001'
for folder in ['Scenes','Records','Previews','Cache']: (B/folder).mkdir(exist_ok=True)
source=P/'Scenes/S07_Monumental-Precision_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene;cam=s.camera;cd=cam.data;focus=bpy.data.objects['Camera focus target']
old=json.loads((A/'Records/camera-score.json').read_text())
def sm(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def span(f,a,b):return sm((f-a)/(b-a))
def pose(p,t,r):return (t-p).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(r))
# One continuous trajectory: preserve the first approach, arc to reverse detail,
# briefly glide on that face, then retreat to the centered full-product pose.
end=Vector(old[-1]['camera']);endt=Vector(old[-1]['target']);score=[]
for f in range(1,193):
 s.frame_set(f);base=old[f-1];arc=span(f,36,84);glide=span(f,36,104);pull=span(f,96,148)
 second=Vector((1.82,-.53,.54)).lerp(Vector((1.72,-.59,.49)),glide)
 secondt=Vector((1.13,0,0)).lerp(Vector((1.11,0,0)),glide)
 # Smooth close glide remains differentiable throughout the arc blend.
 bg=span(f,1,86)
 bp=Vector((.84,-.66,.31)).lerp(Vector((1.20,-.88,.48)),bg)
 bt=Vector((.78,0,.015)).lerp(Vector((1.36,0,0)),bg)
 p=bp.lerp(second,arc).lerp(end,pull)
 t=bt.lerp(secondt,arc).lerp(endt,pull)
 roll=((-24-9*bg)*(1-arc)+(-18-6*glide)*arc)*(1-pull)-48*pull
 cam.location=p;cam.rotation_quaternion=pose(p,t,roll);cd.shift_x=0;cd.shift_y=0;focus.location=t;cd.dof.aperture_fstop=8+8*pull
 cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);cd.keyframe_insert('shift_x',frame=f);cd.keyframe_insert('shift_y',frame=f);focus.keyframe_insert('location',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f)
 score.append({'frame':f,'camera':list(p),'target':list(t),'quaternion':list(cam.rotation_quaternion),'roll_degrees':roll,'fade_to_black':span(f,164,190)})
brand=bpy.data.collections.get('S07 EDITABLE BRANDING')
if brand:
 for o in list(brand.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.collections.remove(brand)
ng=s.compositing_node_group;out=next(n for n in ng.nodes if n.bl_idname=='NodeGroupOutput');previous=out.inputs['Image'].links[0].from_socket
fade=ng.nodes.new('ShaderNodeMix');fade.name='Final fade to nothingness';fade.label='Fade entire image to black | f164-190';fade.data_type='RGBA';fade.inputs[7].default_value=(0,0,0,1)
ng.links.new(previous,fade.inputs[6]);ng.links.new(fade.outputs[2],out.inputs['Image']);fade.location=(20,80);out.location=(260,80)
for f in range(1,193):fade.inputs[0].default_value=span(f,164,190);fade.inputs[0].keyframe_insert('default_value',frame=f)
for data in [cam,cd,focus,ng]:
 ad=data.animation_data
 if not ad or not ad.action:continue
 for layer in ad.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('S06 editorial handoff',1),('Continuous arc to second detail',36),('Second beauty arrival',84),('Retreat',96),('Centered hero',148),('Fade to black',164),('Black endpoint',190)]:s.timeline_markers.new(name,frame=f)
s['revision']='v003 continuous product camera, centered full hero, no branding, fade to black for owner logo in post'
s.frame_set(160);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v003.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2))
(B/'Records/revision.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'duration':8,'frames':192,'continuous_product_camera':True,'branding_removed':True,'final_centering':'Zero lens shift; original full silhouette and scale','black_endpoint_frame':190,'unchanged':'source hardware/materials/lights and S06 editorial handoff'},indent=2))
print('v003 BUILT')
