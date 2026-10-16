"""Still03 wall contact; preserve approved Still02c v001 wave treatment."""
import bpy,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_03'
src=M/'Scenes/B201_spreading-pulse_still02c_v001.blend';out=M/'Scenes/B201_wall-interaction_still03_v010.blend';png=M/'Previews/Still_03/B201_wall-interaction_still03_v010.png'
assert not out.exists(),'Version before overwriting'
ref=json.loads((P/'Records/Tasks/T-007/Evidence/Still_02c/build-render_still02c_v001.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==ref['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;origin=Vector(ref['origin']);wall=Vector(ref['wall_reference']);normal=(wall-origin).normalized();distance=(wall-origin).length
# Editable smooth wave envelopes matching owner reference; illustrative, not simulation.
fronts=sorted([o for o in s.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
wavecollection=bpy.data.collections['STILL02_ILLUSTRATIVE_WAVEFRONT']
for o in fronts:bpy.data.objects.remove(o,do_unlink=True)
az=Vector((0,-normal.z,normal.y));ax=Vector((1,0,0))
waveparams=[(.011,.004,.018),(.025,.006,.025),(distance-.008,.008,.032)]
for idx,(travel,depth,radius) in enumerate(waveparams):
 vs=[];fs=[]
 for i in range(65):
  theta=math.pi*i/64
  for j in range(128):
   phi=math.tau*j/128
   vs.append(origin+normal*(travel+depth*math.cos(theta))+ax*(radius*math.sin(theta)*math.cos(phi))+az*(radius*math.sin(theta)*math.sin(phi)))
 for i in range(64):
  for j in range(128):
   k=i*128+j;q=i*128+(j+1)%128;fs.append((k,q,q+128,k+128))
 me=bpy.data.meshes.new('Smooth acoustic envelope');me.from_pydata(vs,[],fs);me.update()
 for f in me.polygons:f.use_smooth=True
 ob=bpy.data.objects.new('OUTGOING_WAVEFRONT_ILLUSTRATION_'+str(idx+1),me);wavecollection.objects.link(ob)
 ob['travel_m']=travel;ob['depth_m']=depth;ob['spread_radius_m']=radius
 mat=bpy.data.materials.new('Soft cyan transparent envelope '+str(idx));mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();l=mat.node_tree.links
 geo=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(geo.outputs['Normal'],dot.inputs[0]);l.new(geo.outputs['Incoming'],dot.inputs[1])
 ab=n.new('ShaderNodeMath');ab.operation='ABSOLUTE';l.new(dot.outputs['Value'],ab.inputs[0])
 inv=n.new('ShaderNodeMath');inv.operation='SUBTRACT';inv.inputs[0].default_value=1;l.new(ab.outputs[0],inv.inputs[1])
 power=n.new('ShaderNodeMath');power.operation='POWER';power.inputs[1].default_value=3;l.new(inv.outputs[0],power.inputs[0])
 scale=n.new('ShaderNodeMath');scale.operation='MULTIPLY_ADD';scale.inputs[1].default_value=.30;scale.inputs[2].default_value=.008;l.new(power.outputs[0],scale.inputs[0])
 tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(.25,.60,1,1);em.inputs[1].default_value=1.5
 mix=n.new('ShaderNodeMixShader');l.new(scale.outputs[0],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);outn=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],outn.inputs[0]);me.materials.append(mat)
# Query actual T6 irregular wall, retaining only a small explanatory cutaway.
source=bpy.data.objects['T6_IRREGULAR_VIEW_WINDOW'];me=source.data
verts=[source.matrix_world@v.co for v in me.vertices];faces=[]
# Reconstruct continuous T6 wall from preserved full sampling grid, without a plate edge.
for i in range(len(verts)//181-1):
 for j in range(180):
  k=i*181+j;faces.append((k,k+1,k+182,k+181))
bvh=BVHTree.FromPolygons(verts,faces)
angle=math.atan2(normal.z,normal.y);xs=[2.45+1.5*i/60 for i in range(61)];angles=[angle-math.pi+math.tau*j/180 for j in range(181)]
verts=[];faces=[];weights=[];errors=[]
for x in xs:
 for a in angles:
  p,n,i,d=bvh.ray_cast(Vector((x,0,0)),Vector((0,math.cos(a),math.sin(a))));assert p is not None
  verts.append(p);weights.append(math.exp(-((p-wall).length/.0045)**2));errors.append(bvh.find_nearest(p)[3])
for i in range(60):
 for j in range(180):
  k=i*181+j;faces.append((k,k+1,k+182,k+181))
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
# Smooth spatial falloff evaluated per shading point, not coarse vertex interpolation.
dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';l.new(geometry.outputs['Position'],dist.inputs[0]);dist.inputs[1].default_value=wall
ratio=n.new('ShaderNodeMath');ratio.operation='DIVIDE';ratio.inputs[1].default_value=.003;l.new(dist.outputs['Value'],ratio.inputs[0])
square=n.new('ShaderNodeMath');square.operation='MULTIPLY';l.new(ratio.outputs[0],square.inputs[0]);l.new(ratio.outputs[0],square.inputs[1])
neg=n.new('ShaderNodeMath');neg.operation='MULTIPLY';neg.inputs[1].default_value=-1;l.new(square.outputs[0],neg.inputs[0])
fall=n.new('ShaderNodeMath');fall.operation='EXPONENT';l.new(neg.outputs[0],fall.inputs[0])
strength=n.new('ShaderNodeMath');strength.operation='MULTIPLY';strength.inputs[1].default_value=2.5;l.new(fall.outputs[0],strength.inputs[0]);l.new(strength.outputs[0],shader.inputs['Emission Strength']);shader.inputs['Emission Color'].default_value=(.1,.5,1,1);l.new(shader.outputs[0],output.inputs['Surface']);mesh.materials.append(mat)
# Wall is opaque, with its own material; never inherit the product metal override.
for layer in s.view_layers:layer.layer_collection.children[collection.name].exclude=True
layer=s.view_layers.new('Wall interaction');layer.material_override=None
for c in layer.layer_collection.children:c.exclude=c.name not in (collection.name,'B201_REVIEW_CAMERA','STILL01_LIGHTING')
# Compose opaque model/wall first, then depth-mask transparent waves against the wall.
g=s.compositing_node_group;g.nodes.clear();n=g.nodes;l=g.links
beauty=n.new('CompositorNodeRLayers');beauty.scene=s;beauty.layer='Approved model look'
wallnode=n.new('CompositorNodeRLayers');wallnode.scene=s;wallnode.layer='Wall interaction'
front=n.new('CompositorNodeRLayers');front.scene=s;front.layer='Illustrative outgoing pulse'
s.view_layers['Approved model look'].use_pass_z=True;s.view_layers['Wall interaction'].use_pass_z=True;s.view_layers['Illustrative outgoing pulse'].use_pass_z=True
s.view_layers['Illustrative outgoing pulse'].pass_alpha_threshold=0
black=n.new('CompositorNodeRGB');black.outputs[0].default_value=(0,0,0,1)
base=n.new('CompositorNodeAlphaOver');l.new(black.outputs[0],base.inputs['Background']);l.new(beauty.outputs['Image'],base.inputs['Foreground'])
wallcompare=n.new('ShaderNodeMath');wallcompare.operation='LESS_THAN';l.new(wallnode.outputs['Depth'],wallcompare.inputs[0]);l.new(beauty.outputs['Depth'],wallcompare.inputs[1])
wallalpha=n.new('ShaderNodeMath');wallalpha.operation='MULTIPLY';l.new(wallnode.outputs['Alpha'],wallalpha.inputs[0]);l.new(wallcompare.outputs[0],wallalpha.inputs[1])
wallset=n.new('CompositorNodeSetAlpha');l.new(wallnode.outputs['Image'],wallset.inputs['Image']);l.new(wallalpha.outputs[0],wallset.inputs['Alpha'])
opaque=n.new('CompositorNodeAlphaOver');l.new(base.outputs[0],opaque.inputs['Background']);l.new(wallset.outputs[0],opaque.inputs['Foreground'])
compare=n.new('ShaderNodeMath');compare.operation='LESS_THAN';l.new(front.outputs['Depth'],compare.inputs[0]);l.new(wallnode.outputs['Depth'],compare.inputs[1])
alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';l.new(front.outputs['Alpha'],alpha.inputs[0]);l.new(compare.outputs[0],alpha.inputs[1])
setalpha=n.new('CompositorNodeSetAlpha');l.new(front.outputs['Image'],setalpha.inputs['Image']);l.new(alpha.outputs[0],setalpha.inputs['Alpha'])
glow=n.new('CompositorNodeGlare');glow.inputs['Type'].default_value='Fog Glow';glow.inputs['Quality'].default_value='High';glow.inputs['Size'].default_value=.07;glow.inputs['Strength'].default_value=.25;l.new(setalpha.outputs[0],glow.inputs['Image'])
over=n.new('CompositorNodeAlphaOver');l.new(opaque.outputs[0],over.inputs['Background']);l.new(glow.outputs[0],over.inputs['Foreground'])
output=n.new('NodeGroupOutput');l.new(over.outputs[0],output.inputs['Image'])
# Camera inside the annular gap looking along the tool, wall on screen right.
azimuth=Vector((0,-normal.z,normal.y))
s.camera.location=Vector((2.70,0,0))+normal*.150+azimuth*.008
target=origin+normal*.022
forward=(target-s.camera.location).normalized();right=(normal-forward*normal.dot(forward)).normalized();up=right.cross(forward).normalized()
rotation=Matrix((right,up,-forward)).transposed();s.camera.rotation_euler=rotation.to_euler();s.camera.data.lens=27;s.camera.data.clip_start=.002
# Local motivated soft light within the gap; approved product material unchanged.
light=bpy.data.lights.new('Gap soft illumination','AREA');light.energy=.12;light.shape='DISK';light.size=.08
lo=bpy.data.objects.new('Gap soft illumination',light);bpy.data.collections['STILL01_LIGHTING'].objects.link(lo);lo.location=Vector((2.70,0,0))+normal*.155
lo.rotation_euler=(origin+normal*.024-lo.location).to_track_quat('-Z','Y').to_euler();light.color=(.72,.84,1)
s['review_scope']='Still03 wall interaction proposal only. No echo/chart/motion; owner explicitly overrides T26 dependency for original T7 workflow.'
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));s.frame_start=s.frame_end=1
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene
t=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-t
record={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'approved_source_sha256':ref['scene_sha256'],'inputs':ref['inputs'],'origin':list(origin),'wall':list(wall),'standoff_m':distance,'wave_envelopes':waveparams,'representation':'Three closed curved illustrative envelopes; authored spread and axial depth, not acoustic simulation','wall_correspondence_max_m':max(errors),'wall_vertices':len(verts),'camera_unchanged':False,'camera':{'location':list(s.camera.location),'rotation':list(s.camera.rotation_euler),'lens_mm':s.camera.data.lens},'wall_reconstruction':'Full retained T6 sampling grid; removed viewing-window faces restored from their original retained vertices','render_seconds':elapsed,'resolution':[1920,1080],'animation_rendered':False,'visual_approval':'pending','rock_texture':'Authored surface shading, not geological/material identification','contact_glow':'Illustrative arrival emphasis, not physical emitted light'}
(E/'build-render_still03_v010.json').write_text(json.dumps(record,indent=2));print('WALL_STILL_RENDER_PASS',elapsed)
