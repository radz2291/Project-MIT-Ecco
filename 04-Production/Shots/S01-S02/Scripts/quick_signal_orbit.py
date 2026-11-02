"""One perspective360 orbit, two native-speed send/return cycles."""
import bpy,math,time,json
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';P=Q/'Previews/Waveform-direction-v006';P.mkdir(exist_ok=True);s=bpy.context.scene
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/f'Scenes/Pulse_session_before_orbit_{int(time.time())}.blend'),copy=True,compress=True)
def curves(ad):
 return [fc for l in ad.action.layers for st in l.strips for bag in st.channelbags if bag.slot_handle==ad.action_slot.handle for fc in bag.fcurves]
fields=[o for o in s.objects if o.visible_get() and any(m.type=='NODES' and m.name=='Finite head / tail window' for m in o.modifiers)]
assert len(fields)==2
base=fields[0].modifiers['Finite head / tail window'].node_group;loop=base.copy();loop.name='QUICK repeat96frame finite packet'
tm=next(n for n in loop.nodes if n.bl_idname=='GeometryNodeInputSceneTime');consumers=[l.to_socket for l in list(loop.links) if l.from_socket==tm.outputs['Frame']]
def mathnode(operation,a,b):
 n=loop.nodes.new('ShaderNodeMath');n.operation=operation
 for j,v in enumerate([a,b]):
  if isinstance(v,(int,float)):n.inputs[j].default_value=v
  else:loop.links.new(v,n.inputs[j])
 return n.outputs[0]
wrapped=mathnode('ADD',1,mathnode('MODULO',mathnode('SUBTRACT',tm.outputs['Frame'],1),96))
for socket in consumers:loop.links.new(wrapped,socket)
for ob in fields:
 ob.modifiers['Finite head / tail window'].node_group=loop
 for fc in curves(ob.data.shape_keys.animation_data):
  if not any(m.type=='CYCLES' for m in fc.modifiers):fc.modifiers.new('CYCLES')
for ob in s.objects:
 if ob.visible_get() and ob.name.startswith(('SEND HEAD','SEND TAIL','RETURN HEAD','RETURN TAIL')):
  for fc in curves(ob.animation_data):
   if not any(m.type=='CYCLES' for m in fc.modifiers):fc.modifiers.new('CYCLES')
axis=Vector((.3583680987,-.9335803986,0));side=Vector((-.9335803986,-.3583680987,0));up=Vector((0,0,1));target=axis*(.0245758537/2)+up*.002
data=bpy.data.cameras.new('QUICK perspective360');data.type='PERSP';data.lens=45;data.sensor_width=36;data.clip_start=.0001;data.clip_end=10.;camera=bpy.data.objects.new(data.name,data);s.collection.objects.link(camera);camera.rotation_mode='QUATERNION';last=None
for f in range(1,193):
 a=math.pi/2+math.tau*(f-1)/191;camera.location=target+.10*(axis*math.cos(a)+side*math.sin(a))+up*.035;q=(target-camera.location).to_track_quat('-Z','Y')
 if last is not None and last.dot(q)<0:q.negate()
 camera.rotation_quaternion=q;last=q.copy();camera.keyframe_insert(data_path='location',frame=f);camera.keyframe_insert(data_path='rotation_quaternion',frame=f)
for fc in curves(camera.animation_data):
 for k in fc.keyframe_points:k.interpolation='LINEAR'
s.camera=camera;s.frame_start=1;s.frame_end=192;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.frame_set(18)
bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes/Waveform_direction_quick_v006.blend'),compress=True)
rows=[]
for f in range(1,193):
 t=time.perf_counter();s.frame_set(f);s.render.filepath=str(P/f'frame_{f:04}.png');bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt})
 (Q/'Notes/wave_direction_quick_v006.json').write_text(json.dumps({'proof':'One perspective360 orbit over8seconds; two repeats of unchanged96frame cyan-send/violet-return cycle. Native animation, no runtime script. Shared assets unchanged.','frames':192,'fps':24,'rows':rows},indent=2))
 if dt>=5:raise RuntimeError('Render cap failed')
s.frame_set(18);result={'native':bpy.data.filepath,'frames':192,'max_seconds':max(x['seconds'] for x in rows)}
