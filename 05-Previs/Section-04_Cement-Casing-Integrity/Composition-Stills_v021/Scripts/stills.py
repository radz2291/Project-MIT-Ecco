import bpy,sys,json,math,time,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];SRC=B.parent/'Cinematic-Previs_v020/Scenes/S04_sequential-camera_v020.blend';OUT=B/'Scenes/S04_approval-stills_v021.blend'
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def geometry(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
def quat(pos,target,roll):
 f=(target-pos).normalized();axis=Vector((1,0,0));right=(axis-f*axis.dot(f)).normalized();up=(-f).cross(right).normalized();return Matrix((right,up,-f)).transposed().to_quaternion()@Quaternion((0,0,1),math.radians(roll))
def light():
 d=bpy.data.lights.new('D physical wear grazing light - still proposal','SUN');d.energy=.45;d.angle=.4;d.use_shadow=False;o=bpy.data.objects.new(d.name,d);bpy.context.scene.collection.objects.link(o);o.location=(-1.76,.145,.08);o.rotation_euler=(Vector((-1.76,.161,0))-o.location).to_track_quat('-Z','Y').to_euler();return o
bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='S04 v021 - still approval only';before=geometry(s);source_cam=s.camera
depth_before=[x.value for x in bpy.data.objects['STEEL - capped true source section'].data.attributes['ComputedWearDepth_m'].data]
source_action=source_cam.animation_data.action
channel=bpy.data.objects['Stationary organic fluid-filled channel volume'];original=channel.data.materials[0];m=original.copy();m.name='Restrained slate cyan fluid - still proposal';channel.data.materials[0]=m;m.diffuse_color=(.055,.155,.185,1)
# Remap self-referencing display drivers after making the material local.
if m.node_tree.animation_data:
 for driver in m.node_tree.animation_data.drivers:
  for var in driver.driver.variables:
   for target in var.targets:
    if target.id==original:target.id=m
steel=bpy.data.objects['STEEL - capped true source section'];heat=steel.data.materials[0].copy();heat.name='Same computed-depth data with still-review switch';steel.data.materials[0]=heat;nt=heat.node_tree;out=next(n for n in nt.nodes if n.type=='OUTPUT_MATERIAL');mix=out.inputs['Surface'].links[0].from_node;factor=mix.inputs[0].links[0].from_socket
cap=steel.data.materials[1].copy();cap.name='Matte steel section - reaction readability proposal';steel.data.materials[1]=cap
for node in cap.node_tree.nodes:
 if node.type=='BSDF_PRINCIPLED':node.inputs['Roughness'].default_value=.70;node.inputs['Metallic'].default_value=.10;node.inputs['Base Color'].default_value=(.18,.23,.27,1)
switch=nt.nodes.new('ShaderNodeValue');switch.name='Still review - data display enabled';multiply=nt.nodes.new('ShaderNodeMath');multiply.operation='MULTIPLY';nt.links.new(factor,multiply.inputs[0]);nt.links.new(switch.outputs[0],multiply.inputs[1]);nt.links.new(multiply.outputs[0],mix.inputs[0])
graphics=bpy.data.collections.new('D measurement graphics - still-review visibility');s.collection.children.link(graphics)
for ob in s.objects:
 if ob.type=='CURVE' and ob.name.startswith('Station '):
  graphics.objects.link(ob)
  for c in list(ob.users_collection):
   if c!=graphics:c.objects.unlink(ob)
grazing=light();key=bpy.data.objects.get('Wide sectional softbox');fill=bpy.data.objects.get('Uphole fill');original_key=key.data.energy;original_fill=fill.data.energy
states=[('A1',1,'Casing mouth and approach'),('A2',40,'Tool entering the existing casing'),('B1',85,'Supported backing - contact'),('B2',104,'Supported backing - settled'),('C1',197,'Reduced backing - contact'),('C2',216,'Reduced backing - persistent response'),('D1',400,'Physical wear only'),('D2',400,'Same wear with reference and computed data')]
cameras={};rows=[]
for tag,frame,title in states:
 s.camera=source_cam;s.frame_set(frame);bpy.context.view_layer.update();d=source_cam.data.copy();d.animation_data_clear();cam=bpy.data.objects.new('Approval still '+tag,d);s.collection.objects.link(cam);cam.matrix_world=source_cam.matrix_world.copy();cam['source_frame']=frame;cam['purpose']=title
 if tag.startswith('A'):
  # Downhole now runs toward screen lower-right; uphole/casing reads upper-left.
  sample=json.loads((B.parent/'Cinematic-Previs_v020/Records/camera-score.json').read_text())[frame-1];cam.rotation_mode='QUATERNION';cam.rotation_quaternion=quat(Vector(sample['eye_m']),Vector(sample['target_m']),25)
 elif tag[0] in 'BC':d.lens=65
 else:
  cam.location=(-1.05,.055,.065);cam.rotation_mode='QUATERNION';cam.rotation_quaternion=quat(cam.location,Vector((-1.70,.160,-.015)),-13);d.lens=42;d.shift_x=.18
 cameras[tag]=cam
def setup(tag):
 frame=next(f for t,f,title in states if t==tag);s.frame_set(frame);s.camera=cameras[tag];isD=tag.startswith('D');graphics.hide_render=tag=='D1';graphics.hide_viewport=graphics.hide_render;switch.outputs[0].default_value=0 if tag=='D1' else 1;grazing.hide_render=not isD;grazing.hide_viewport=not isD;key.data.energy=original_key if tag.startswith('A') else 12;fill.data.energy=.7 if isD else original_fill;bpy.context.view_layer.update()
for tag,frame,title in states:
 setup(tag);s.render.filepath=str(B/'Previews'/f'S04_{tag}_v021.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
 rows.append({'id':tag,'title':title,'source_frame':frame,'seconds':elapsed,'camera_position_m':list(s.camera.location),'camera_quaternion':list(s.camera.matrix_world.to_quaternion()),'lens_mm':s.camera.data.lens,'geometry_unchanged':before==geometry(s),'data_display':tag!='D1','station_graphics':tag!='D1'})
 dump('stills.json',rows);print('STILL',tag,elapsed,flush=True)
 if elapsed>=5:raise RuntimeError('Frame cap exceeded')
assert before==geometry(s) and source_cam.animation_data.action==source_action
assert depth_before==[x.value for x in steel.data.attributes['ComputedWearDepth_m'].data]
setup('B1');s['scope']='Approval stills ONLY: natural A orientation; B/C65mm matched close-ups; muted channel; D grazing light/reframe with physical-only and overlay states. Source continuous animation is retained, not revised or rendered.'
s['source_camera']=source_cam.name;s['still_cameras']='; '.join(cameras);s['source_geometry_unchanged']=True
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
for w in bpy.context.window_manager.windows:
 w.scene=s
 for a in w.screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.shading.type='RENDERED'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
dump('verification.json',{'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'native':str(OUT),'physical_meshes_unchanged':True,'computed_depth_values_unchanged':True,'maximum_authored_loss_mm':1000*max(depth_before),'source_camera_action_preserved':True,'source_timing_unchanged':True,'B_C_magnification_vs_v020':65/42,'A_proposed_roll_degrees':25,'C_fluid_color_linear_RGBA':list(m.diffuse_color),'full_animation_rendered':False,'camera_path_integrated':False,'all_still_frames_under5s':all(x['seconds']<5 for x in rows),'human_approval':'pending'})
