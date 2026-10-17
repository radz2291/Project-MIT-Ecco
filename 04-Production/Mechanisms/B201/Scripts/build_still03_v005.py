"""Still03 wall contact; preserve approved Still02c v001 wave treatment."""
import bpy,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_03'
src=M/'Scenes/B201_spreading-pulse_still02c_v001.blend';out=M/'Scenes/B201_wall-interaction_still03_v005.blend';png=M/'Previews/Still_03/B201_wall-interaction_still03_v005.png'
assert not out.exists(),'Version before overwriting'
ref=json.loads((P/'Records/Tasks/T-007/Evidence/Still_02c/build-render_still02c_v001.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==ref['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;origin=Vector(ref['origin']);wall=Vector(ref['wall_reference']);normal=(wall-origin).normalized();distance=(wall-origin).length
# Advance the same approved curved fronts to the contact pose; no animation.
fronts=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
for o,old,new in zip(fronts,(.024,.033,.042),(.028,.037,distance)):
 for v in o.data.vertices:v.co=origin+(v.co-origin)*(new/old)
 o['contact_pose_radius_m']=new
# Query actual T6 irregular wall, retaining only a small explanatory cutaway.
source=bpy.data.objects['T6_IRREGULAR_VIEW_WINDOW'];me=source.data
verts=[source.matrix_world@v.co for v in me.vertices];faces=[]
# Reconstruct continuous T6 wall from preserved full sampling grid, without a plate edge.
for i in range(len(verts)//181-1):
 for j in range(180):
  k=i*181+j;faces.append((k,k+1,k+182,k+181))
bvh=BVHTree.FromPolygons(verts,faces)
angle=math.atan2(normal.z,normal.y);xs=[2.45+1.5*i/60 for i in range(61)];angles=[angle-.7+1.4*j/64 for j in range(65)]
verts=[];faces=[];weights=[];errors=[]
for x in xs:
 for a in angles:
  p,n,i,d=bvh.ray_cast(Vector((x,0,0)),Vector((0,math.cos(a),math.sin(a))));assert p is not None
  verts.append(p);weights.append(math.exp(-((p-wall).length/.0045)**2));errors.append(bvh.find_nearest(p)[3])
for i in range(60):
 for j in range(64):
  k=i*65+j;faces.append((k,k+1,k+66,k+65))
collection=bpy.data.collections.new('STILL03_WALL_CONTACT');s.collection.children.link(collection)
mesh=bpy.data.meshes.new('T6 ray-corresponding wall section');mesh.from_pydata(verts,[],faces);mesh.update()
for f in mesh.polygons:f.use_smooth=True
attribute=mesh.color_attributes.new(name='ContactWeight',type='FLOAT_COLOR',domain='CORNER')
for loop in mesh.loops:attribute.data[loop.index].color=(weights[loop.vertex_index],)*3+(1,)
o=bpy.data.objects.new('T6_WALL_CONTACT_SECTION',mesh);collection.objects.link(o);o['provenance']='Ray sampled on preserved T6 v003 evaluated cutaway surface; explanatory cutaway only.'
mat=bpy.data.materials.new('Subdued rock with illustrative localized acoustic contact');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();l=mat.node_tree.links
output=n.new('ShaderNodeOutputMaterial');shader=n.new('ShaderNodeBsdfPrincipled');shader.inputs['Base Color'].default_value=(.045,.035,.025,1);shader.inputs['Roughness'].default_value=.92
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=200;noise.inputs['Detail'].default_value=3
bump=n.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.5;bump.inputs['Distance'].default_value=.0015;l.new(noise.outputs['Fac'],bump.inputs['Height']);l.new(bump.outputs['Normal'],shader.inputs['Normal'])
geometry=n.new('ShaderNodeNewGeometry');l.new(geometry.outputs['Position'],noise.inputs['Vector'])
ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].color=(.018,.012,.009,1);ramp.color_ramp.elements[1].color=(.20,.14,.085,1);l.new(noise.outputs['Fac'],ramp.inputs['Fac']);l.new(ramp.outputs['Color'],shader.inputs['Base Color'])
# Continuous surface extends beyond the frame; no visible cutaway thickness.
weight=n.new('ShaderNodeVertexColor');weight.layer_name='ContactWeight';multiply=n.new('ShaderNodeMath');multiply.operation='MULTIPLY';multiply.inputs[1].default_value=2.5;l.new(weight.outputs['Color'],multiply.inputs[0]);l.new(multiply.outputs[0],shader.inputs['Emission Strength']);shader.inputs['Emission Color'].default_value=(.02,.45,1,1);l.new(shader.outputs[0],output.inputs['Surface']);mesh.materials.append(mat)
# Wall is opaque, with its own material; never inherit the product metal override.
for layer in s.view_layers:layer.layer_collection.children[collection.name].exclude=True
layer=s.view_layers.new('Wall interaction');layer.material_override=None
for c in layer.layer_collection.children:c.exclude=c.name not in (collection.name,'B201_REVIEW_CAMERA','STILL01_LIGHTING')
g=s.compositing_node_group;n=g.nodes;l=g.links;output=next(x for x in n if x.type=='GROUP_OUTPUT');previous=output.inputs['Image'].links[0].from_socket;l.remove(output.inputs['Image'].links[0])
wallnode=n.new('CompositorNodeRLayers');wallnode.scene=s;wallnode.layer=layer.name
over=n.new('CompositorNodeAlphaOver');over.inputs['Factor'].default_value=1;l.new(previous,over.inputs['Background']);l.new(wallnode.outputs['Image'],over.inputs['Foreground']);l.new(over.outputs['Image'],output.inputs['Image'])
# Camera inside the annular gap looking along the tool, wall on screen right.
forward=Vector((1,0,0));right=normal;up=right.cross(forward).normalized()
s.camera.location=Vector((2.67,0,0))+normal*.153
rotation=Matrix((right,up,-forward)).transposed();s.camera.rotation_euler=rotation.to_euler();s.camera.data.lens=42;s.camera.data.clip_start=.002
# Local motivated soft light within the gap; approved product material unchanged.
light=bpy.data.lights.new('Gap soft illumination','AREA');light.energy=.5;light.shape='DISK';light.size=.08
lo=bpy.data.objects.new('Gap soft illumination',light);bpy.data.collections['STILL01_LIGHTING'].objects.link(lo);lo.location=Vector((2.70,0,0))+normal*.155
lo.rotation_euler=(origin+normal*.024-lo.location).to_track_quat('-Z','Y').to_euler();light.color=(.72,.84,1)
s['review_scope']='Still03 wall interaction proposal only. No echo/chart/motion; owner explicitly overrides T26 dependency for original T7 workflow.'
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));s.frame_start=s.frame_end=1
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(out))
t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
record={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'approved_source_sha256':ref['scene_sha256'],'inputs':ref['inputs'],'origin':list(origin),'wall':list(wall),'standoff_m':distance,'front_radii_m':[.028,.037,distance],'wall_correspondence_max_m':max(errors),'wall_vertices':len(verts),'camera_unchanged':False,'camera':{'location':list(s.camera.location),'rotation':list(s.camera.rotation_euler),'lens_mm':s.camera.data.lens},'wall_reconstruction':'Full retained T6 sampling grid; removed viewing-window faces restored from their original retained vertices','render_seconds':elapsed,'resolution':[1920,1080],'animation_rendered':False,'visual_approval':'pending','rock_texture':'Authored surface shading, not geological/material identification','contact_glow':'Illustrative arrival emphasis, not physical emitted light'}
(E/'build-render_still03_v005.json').write_text(json.dumps(record,indent=2));print('WALL_STILL_RENDER_PASS',elapsed)
