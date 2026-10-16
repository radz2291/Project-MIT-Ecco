"""Still05: reception becomes a measured wall position; minimal native graphics."""
import bpy,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_05';E.mkdir(parents=True,exist_ok=True)
src=M/'Scenes/B201_returning-echo_still04_v003.blend';out=M/'Scenes/B201_waveform-connection_still05_v001.blend';png=M/'Previews/Still_05/B201_waveform-connection_still05_v001.png';png.parent.mkdir(parents=True,exist_ok=True)
assert not out.exists();r=json.loads((P/'Records/Tasks/T-007/Evidence/Still_04/build-render_still04_v003.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene
receiver=Vector(r['receiver_surface']);wall=Vector(r['wall_origin'])
for o in s.objects:
 if o.name.startswith('RETURNING_ECHO_'):o.hide_render=True
# The emerald receive-state and faint blue wall patch remain exactly as Still04.
coll=bpy.data.collections.new('STILL05_MEASUREMENT_GRAPHICS');s.collection.children.link(coll)
def material(name,color,strength):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=color;e.inputs[1].default_value=strength;output=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],output.inputs[0]);return m
neutral=material('Quiet measurement ivory',(.55,.66,.67,1),1.0);muted=material('Muted timing trace',(.20,.28,.30,1),.8);blue=material('Pulse sent cyan',(.14,.48,.83,1),1.1);green=material('Echo received emerald',(.07,.58,.32,1),1.1)
W,H=1920,1080;depth=.045;frame=s.camera.data.view_frame(scene=s);scale=depth/-frame[0].z;fw=(max(v.x for v in frame)-min(v.x for v in frame))*scale;fh=(max(v.y for v in frame)-min(v.y for v in frame))*scale;pixel=fh/H
def screen(x,y):return s.camera.matrix_world@Vector(((x/W-.5)*fw,(.5-y/H)*fh,-depth))
def curve(name,points,mat,width):
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';cu.resolution_u=1;cu.bevel_depth=width;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(len(points)-1)
 for p,q in zip(sp.points,points):p.co=(*q,1)
 ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);cu.materials.append(mat);return ob
def line(name,pixels,mat=muted,width=.65):return curve(name,[screen(*p) for p in pixels],mat,pixel*width)
font=bpy.data.fonts.load('C:/Windows/Fonts/segoeuil.ttf')
def text(name,body,x,y,px,mat):
 cu=bpy.data.curves.new(name,'FONT');cu.body=body;cu.font=font;cu.align_x='CENTER';cu.size=px*pixel/.72;cu.space_character=1.0;ob=bpy.data.objects.new(name,cu);coll.objects.link(ob);ob.location=screen(x,y);ob.rotation_euler=s.camera.rotation_euler;cu.materials.append(mat);return ob
# Actual spatial endpoints, not an arbitrary screen-space distance estimate.
measurement=curve('SENSOR_TO_WALL_MEASUREMENT',[receiver,wall],neutral,.00008);measurement['start_receiver_surface']=list(receiver);measurement['end_actual_wall']=list(wall);measurement['meaning']='Sensor-to-wall distance, spatial geometry correspondence; no numerical value shown'
q0=world_to_camera_view(s,s.camera,receiver);q1=world_to_camera_view(s,s.camera,wall);mid=((q0.x+q1.x)*W/2,(1-(q0.y+q1.y)/2)*H)
text('DISTANCE_LABEL','Sensor-to-wall distance',mid[0],mid[1]+58,24,neutral)
# Compact illustrative signal support; no axis, scale, numeric timing or formula.
left,right=860,1270;sent,received=915,1205;baseline=330
line('WAVEFORM_BASELINE',[(left,baseline),(right,baseline)],muted,.55)
for name,cx,amp,mat in (('PULSE_SENT_TRACE',sent,17,blue),('ECHO_RECEIVED_TRACE',received,12,green)):
 points=[]
 for i in range(101):
  u=-3+6*i/100;points.append((cx+u*10,baseline-amp*math.exp(-u*u*.8)*math.sin(u*5)))
 ob=line(name,points,mat,.85);ob['illustrative_signal']=True;ob['not_amplitude_or_distance_data']=True
text('PULSE_SENT_LABEL','Pulse sent',sent,280,20,blue);text('ECHO_RECEIVED_LABEL','Echo received',received,280,20,green)
line('TWO_WAY_TIMING_BRACKET',[(sent,368),(sent,380),(received,380),(received,368)],neutral,.55)
text('DELTA_T_LABEL','Δt',(sent+received)/2,415,23,neutral)
for layer in s.view_layers:layer.layer_collection.children[coll.name].exclude=True
layer=s.view_layers.new('Minimal measurement graphics');layer.material_override=None
for c in layer.layer_collection.children:c.exclude=c.name not in (coll.name,'B201_REVIEW_CAMERA')
g=s.compositing_node_group;n=g.nodes;l=g.links;output=next(x for x in n if x.bl_idname=='NodeGroupOutput');previous=output.inputs['Image'].links[0].from_socket
graphic=n.new('CompositorNodeRLayers');graphic.scene=s;graphic.layer=layer.name;over=n.new('CompositorNodeAlphaOver');l.new(previous,over.inputs['Background']);l.new(graphic.outputs['Image'],over.inputs['Foreground']);l.new(over.outputs[0],output.inputs['Image'])
s['review_scope']='Still05: echo return time becomes known wall position. No formula, numbers, amplitude scale or academic explanation; illustrative trace only. No animation.'
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));s.frame_start=s.frame_end=1
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;t=time.perf_counter();bpy.ops.render.render(write_still=True)
record={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'parent_scene':str(src.relative_to(P)),'parent_scene_sha256':r['scene_sha256'],'inputs':r['inputs'],'receiver_surface':list(receiver),'wall_origin':list(wall),'labels':['Pulse sent','Echo received','Δt','Sensor-to-wall distance'],'waveform':'Illustrative event timing support, not measured signal, amplitude scale or numeric travel time','font_dependency':'C:/Windows/Fonts/segoeuil.ttf (existing system font, not redistributed)','spatial_measurement':'Native curve anchored to actual receiver and wall coordinates','camera_unchanged':True,'sensor_response_unchanged':True,'wall_patch_fade':.07,'render_seconds':time.perf_counter()-t,'resolution':[1920,1080],'formula_shown':False,'numbers_shown':False,'animation_rendered':False,'visual_approval':'pending'}
(E/'build-render_still05_v001.json').write_text(json.dumps(record,indent=2));print('WALL_POSITION_RENDER_PASS')
