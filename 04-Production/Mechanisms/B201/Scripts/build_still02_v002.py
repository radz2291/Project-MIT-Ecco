"""Outgoing-pulse still only; keep approved Still01 camera/light/geometry."""
import bpy,json,hashlib,time,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';R=P/'Records/Tasks/T-007/Evidence/Still_02'
src=M/'Scenes/B201_sensor-origin_still01_v004.blend';out=M/'Scenes/B201_outgoing-pulse_still02_v002.blend';png=M/'Previews/Still_02/B201_outgoing-pulse_still02_v002.png'
if out.exists():raise RuntimeError('Refuse overwrite; version edited proposal')
reference=json.loads((P/'Records/Tasks/T-007/Evidence/Still_01/build-render_still01_v004.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==reference['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
event=json.loads((P/'Records/Tasks/T-007/Evidence/v011/build_v011.json').read_text())['events'][0]
origin=Vector(event['origin']);wall=Vector(event['wall']);normal=(wall-origin).normalized();tangent=Vector((1,0,0))
distance=.020;half_width=.0012;half_angle=1.4;front_radius=.018
camera_q=s.camera.rotation_euler.to_quaternion();camera_right=camera_q@Vector((1,0,0));camera_up=camera_q@Vector((0,1,0))
tangent=(camera_right-normal*camera_right.dot(normal)).normalized();vertical=normal.cross(tangent).normalized()
if vertical.dot(camera_up)<0:vertical=-vertical
center=origin+normal*distance
assert distance+half_width < (wall-origin).length
collection=bpy.data.collections.new('STILL02_ILLUSTRATIVE_WAVEFRONT');s.collection.children.link(collection)
verts=[];alpha=[];faces=[];bands=8;steps=96
for i in range(bands+1):
 u=i/bands;r=front_radius+(u-.5)*2*half_width
 for j in range(steps+1):
  v=j/steps;theta=(v-.5)*2*half_angle
  verts.append(center+tangent*(r*math.sin(theta))+vertical*(r*math.cos(theta)))
  alpha.append(math.sin(math.pi*v)**.65 * math.sin(math.pi*u)**1.3)
for i in range(bands):
 for j in range(steps):
  z=i*(steps+1)+j;faces.append((z,z+1,z+steps+2,z+steps+1))
mesh=bpy.data.meshes.new('Single bowed signal front / no physical part');mesh.from_pydata(verts,[],faces);mesh.update()
attribute=mesh.color_attributes.new(name='SignalOpacity',type='FLOAT_COLOR',domain='CORNER')
for loop in mesh.loops:attribute.data[loop.index].color=(1,1,1,alpha[loop.vertex_index])
pulse=bpy.data.objects.new('OUTGOING_WAVEFRONT_ILLUSTRATION',mesh);collection.objects.link(pulse)
pulse['meaning']='Single illustrative acoustic front, not a calibrated beam or manufactured part.'
pulse['origin_reference']='ECCO_SENSOR_REF_01, current held whole-tool pose'
pulse['outward_distance_m']=distance
mat=bpy.data.materials.new('Still02 cyan front with soft transparent edges');mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear();link=mat.node_tree.links
output=nodes.new('ShaderNodeOutputMaterial');mix=nodes.new('ShaderNodeMixShader');transparent=nodes.new('ShaderNodeBsdfTransparent');emission=nodes.new('ShaderNodeEmission');color=nodes.new('ShaderNodeVertexColor');color.layer_name='SignalOpacity'
emission.inputs['Color'].default_value=(.04,.65,1.,1);emission.inputs['Strength'].default_value=3.0
link.new(color.outputs['Alpha'],mix.inputs[0]);link.new(transparent.outputs[0],mix.inputs[1]);link.new(emission.outputs[0],mix.inputs[2]);link.new(mix.outputs[0],output.inputs['Surface']);mesh.materials.append(mat)
# Separate explanatory emission from approved whole-layer metal shading.
beauty=s.view_layers[0];beauty.name='Approved model look';beauty.layer_collection.children[collection.name].exclude=True
signal=s.view_layers.new('Illustrative outgoing pulse');signal.material_override=None
for c in signal.layer_collection.children:c.exclude=c.name not in (collection.name,'B201_REVIEW_CAMERA')
s.render.film_transparent=True;s.render.use_compositing=True
s.use_nodes=True;group=bpy.data.node_groups.new('Still02 model + signal composition','CompositorNodeTree');s.compositing_node_group=group
group.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');n=group.nodes;links=group.links
base=n.new('CompositorNodeRLayers');base.scene=s;base.layer=beauty.name
front=n.new('CompositorNodeRLayers');front.scene=s;front.layer=signal.name
black=n.new('CompositorNodeRGB');black.outputs[0].default_value=(0,0,0,1)
background=n.new('CompositorNodeAlphaOver');background.inputs['Factor'].default_value=1
links.new(black.outputs[0],background.inputs['Background']);links.new(base.outputs['Image'],background.inputs['Foreground'])
glow=n.new('CompositorNodeGlare');glow.inputs['Type'].default_value='Fog Glow';glow.inputs['Quality'].default_value='High';glow.inputs['Size'].default_value=.07;glow.inputs['Strength'].default_value=.25
links.new(front.outputs['Image'],glow.inputs['Image'])
over=n.new('CompositorNodeAlphaOver');over.inputs['Factor'].default_value=1
links.new(background.outputs['Image'],over.inputs['Background']);links.new(glow.outputs['Image'],over.inputs['Foreground'])
final=n.new('NodeGroupOutput');links.new(over.outputs[0],final.inputs['Image'])
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));s.frame_start=1;s.frame_end=1
s['review_scope']='Still02 outgoing pulse proposal only. Still01 visually approved; no animation/wall contact/return/trace approval.'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;bpy.context.view_layer.update()
t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
cam=s.camera;projection=[list(world_to_camera_view(s,cam,p)) for p in (origin,origin+normal*distance,wall)]
record={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'render_seconds':elapsed,'resolution':[1920,1080],'engine':s.render.engine,'samples':s.cycles.samples,'approved_input_scene_sha256':reference['scene_sha256'],'approved_input_image_sha256':reference['image_sha256'],'inputs':reference['inputs'],'camera':{'location':list(cam.location),'rotation':list(cam.rotation_euler),'lens_mm':cam.data.lens},'origin':list(origin),'wall_reference':list(wall),'direction':list(normal),'distance_m':distance,'wavefront_radius_m':front_radius,'wavefront_half_width_m':half_width,'wavefront_half_angle_rad':half_angle,'plane_tangent':list(tangent),'plane_vertical':list(vertical),'projection_origin_front_wall':projection,'source_hashes_unchanged':all(hashlib.sha256((P/rel).read_bytes()).hexdigest()==h for rel,h in reference['inputs'].items()),'animation_rendered':False,'human_approval':'Still01v004 approved by Radzi; Still02v002 pending','layers':'Approved source geometry/lighting kept separate from illustrative emission; all use same camera.'}
(R/'build-render_still02_v002.json').write_text(json.dumps(record,indent=2));print('STILL02_RENDER_PASS',elapsed)
