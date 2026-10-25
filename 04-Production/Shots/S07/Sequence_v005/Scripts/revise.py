import bpy,json,math,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];P=B.parent/'Sequence_v002'
for folder in ['Scenes','Records','Previews','Cache']:(B/folder).mkdir(exist_ok=True)
source=P/'Scenes/S07_Monumental-Precision_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(source))
s=bpy.context.scene;cam=s.camera;cd=cam.data;focus=bpy.data.objects['Camera focus target']
for data in [cam,cd,focus]:data.animation_data_clear()
brand=bpy.data.collections.get('S07 EDITABLE BRANDING')
if brand:
 for o in list(brand.objects):bpy.data.objects.remove(o,do_unlink=True)
 bpy.data.collections.remove(brand)
def sm(t):t=max(0,min(1,t));return t*t*t*(t*(t*6-15)+10)
def pose(p,t,roll):return (t-p).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(roll))
old=json.loads((P/'Records/camera-score.json').read_text());end=Vector(old[-1]['camera']);center=Vector((1.2,0,0))
wide_a=center+(end-center)*.96;wide_b=center+(end-center)*1.07
shots=[
 {'id':'S07-A','frames':[1,60],'p0':(.84,-.66,.31),'p1':(1.11,-.825,.438),'t0':(.78,0,.015),'t1':(1.22,0,0),'roll':[-24,-30],'fstop':8},
 {'id':'S07-B','frames':[61,120],'p0':(1.82,-.53,.54),'p1':(1.60,-.67,.46),'t0':(1.13,0,0),'t1':(1.02,0,0),'roll':[-18,-24],'fstop':8},
 {'id':'S07-C','frames':[121,192],'p0':list(wide_a),'p1':list(wide_b),'t0':list(center),'t1':list(center),'roll':[-45,-48],'fstop':16}]
score=[]
for shot in shots:
 a,b=shot['frames']
 for f in range(a,b+1):
  u=(f-a)/(b-a);p=Vector(shot['p0']).lerp(Vector(shot['p1']),u);t=Vector(shot['t0']).lerp(Vector(shot['t1']),u);roll=shot['roll'][0]*(1-u)+shot['roll'][1]*u
  q=pose(p,t,roll);cam.location=p;cam.rotation_quaternion=q;focus.location=t;cd.shift_x=0;cd.shift_y=0;cd.dof.aperture_fstop=shot['fstop']
  cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);focus.keyframe_insert('location',frame=f);cd.keyframe_insert('shift_x',frame=f);cd.keyframe_insert('shift_y',frame=f);cd.dof.keyframe_insert('aperture_fstop',frame=f)
  score.append({'frame':f,'shot':shot['id'],'camera':list(p),'target':list(t),'quaternion':list(q),'roll_degrees':roll,'fade_to_black':sm((f-164)/26)})
ng=bpy.data.node_groups.new('S07 v005 | direct product entry and final fade','CompositorNodeTree');ng.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=ng
rl=ng.nodes.new('CompositorNodeRLayers');rl.scene=s;fade=ng.nodes.new('ShaderNodeMix');fade.name='Final fade to nothingness';fade.data_type='RGBA';fade.inputs[7].default_value=(0,0,0,1);out=ng.nodes.new('NodeGroupOutput');ng.links.new(rl.outputs['Image'],fade.inputs[6]);ng.links.new(fade.outputs[2],out.inputs['Image']);rl.location=(-280,0);out.location=(260,0)
for f in range(1,193):fade.inputs[0].default_value=sm((f-164)/26);fade.inputs[0].keyframe_insert('default_value',frame=f)
for data in [cam,cd,focus,ng]:
 for layer in data.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='CONSTANT' if data!=ng and round(k.co[0]) in (60,120) else 'LINEAR'
for m in list(s.timeline_markers):s.timeline_markers.remove(m)
for name,f in [('SHOT 1 | moving detail',1),('CUT | SHOT 2 | moving reverse beauty',61),('CUT | SHOT 3 | moving full hero',121),('Fade to black',164),('Black endpoint',190)]:s.timeline_markers.new(name,frame=f)
s['revision']='v005 | v002-based three-shot edit; constant camera translation in every shot; direct moving product entry; no branding; centered wide fade'
s.frame_set(150);bpy.ops.wm.save_as_mainfile(filepath=str(B/'Scenes/S07_Monumental-Precision_v005.blend'))
(B/'Records/camera-score.json').write_text(json.dumps(score,indent=2));(B/'Records/shot-definitions.json').write_text(json.dumps(shots,indent=2))
(B/'Records/revision.json').write_text(json.dumps({'source':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'frames':192,'fps':24,'cut_frames':[61,121],'camera_motion':'Constant straight-line translation per shot; no eased starts or stops','opening':'Direct product image from frame one; old S06 plate dissolve removed','branding_removed':True,'black_endpoint_frame':190,'unchanged':'Actual geometry, stationary hardware, v002 materials and light rig'},indent=2));print('v005 BUILT')
