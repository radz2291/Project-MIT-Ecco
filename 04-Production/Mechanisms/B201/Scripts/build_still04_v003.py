"""Still04: wall-originating illustrative echo first touches the original sensor face."""
import bpy,math,json,hashlib,time
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
P=Path(__file__).resolve().parents[3];M=P/'Mechanisms/B201';E=P/'Records/Tasks/T-007/Evidence/Still_04';E.mkdir(parents=True,exist_ok=True)
src=M/'Scenes/B201_wall-interaction_still03_v013.blend';out=M/'Scenes/B201_returning-echo_still04_v003.blend';png=M/'Previews/Still_04/B201_returning-echo_still04_v003.png';png.parent.mkdir(parents=True,exist_ok=True)
assert not out.exists();r=json.loads((P/'Records/Tasks/T-007/Evidence/Still_03/build-render_still03_v013.json').read_text());assert hashlib.sha256(src.read_bytes()).hexdigest()==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;origin=Vector(r['origin']);wall=Vector(r['wall']);normal=(wall-origin).normalized()
# Inspect the evaluated accepted product instance, without changing its geometry/materials.
receiver=None
for inst in bpy.context.evaluated_depsgraph_get().object_instances:
 ob=inst.object
 if not inst.is_instance or ob.type!='MESH' or ob.name!='TEMP | Imaging port 1 | removable acoustic cap':continue
 me=ob.to_mesh();vs=[inst.matrix_world@v.co for v in me.vertices];tree=BVHTree.FromPolygons(vs,[list(f.vertices) for f in me.polygons]);near=tree.find_nearest(origin);receiver=near[0].copy();ob.to_mesh_clear();break
assert receiver is not None and (receiver-origin).length<.001
radius=(receiver-wall).length;propagation=(receiver-wall).normalized();ax=Vector((1,0,0));az=propagation.cross(ax).normalized()
collection=bpy.data.collections['STILL02_ILLUSTRATIVE_WAVEFRONT'];fronts=sorted([o for o in collection.objects if o.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_')],key=lambda o:o.name)
material=fronts[-1].data.materials[0].copy();material.name='Still04 thin cyan returning membrane'
# Slight readability lift; same thin cap, no refraction or thickness.
for node in material.node_tree.nodes:
 if node.bl_idname=='ShaderNodeMath' and node.operation=='MULTIPLY_ADD':node.inputs[1].default_value=.21;node.inputs[2].default_value=.035
for node in material.node_tree.nodes:
 if node.bl_idname=='ShaderNodeEmission':node.inputs[0].default_value=(.05,.55,.30,1);node.inputs[1].default_value=2.3
for ob in fronts:ob.hide_render=True
vs=[];fs=[];fade=[]
for i in range(65):
 theta=.60*i/64
 for j in range(160):
  phi=math.tau*j/160;vs.append(wall+radius*(propagation*math.cos(theta)+ax*math.sin(theta)*math.cos(phi)+az*math.sin(theta)*math.sin(phi)));fade.append(min(1,max(0,(.60-theta)/.10)))
for i in range(64):
 for j in range(160):
  k=i*160+j;q=i*160+(j+1)%160;fs.append((k,q,q+160,k+160))
me=bpy.data.meshes.new('Wall-originating spherical echo cap');me.from_pydata(vs,[],fs);me.update()
for f in me.polygons:f.use_smooth=True
a=me.color_attributes.new(name='BoundaryFade',type='FLOAT_COLOR',domain='CORNER')
for loop in me.loops:a.data[loop.index].color=(fade[loop.vertex_index],)*3+(1,)
ob=bpy.data.objects.new('RETURNING_ECHO_FIRST_RECEPTION',me);collection.objects.link(ob);me.materials.append(material)
ob['wave_origin_wall']=list(wall);ob['receiver_surface']=list(receiver);ob['radius_m']=radius;ob['meaning']='Illustrative reflected front expands from sampled wall toward original emitting sensor; not time-reversed outgoing geometry or acoustic simulation.'
# Tighter, weaker trailing reflections remain behind the leading reception front.
followers=[]
for idx,(lag,weight) in enumerate(((.0045,.32),(.009,.15)),1):
 follower_radius=radius-lag
 follower_mesh=me.copy();follower_mesh.name='Thin emerald echo follower '+str(idx)
 for v in follower_mesh.vertices:v.co=wall+(v.co-wall)*(follower_radius/radius)
 follower_material=material.copy();follower_material.name='Faint emerald echo follower '+str(idx)
 for node in follower_material.node_tree.nodes:
  if node.bl_idname=='ShaderNodeEmission':node.inputs[1].default_value=2.3*weight
 follower_mesh.materials.clear();follower_mesh.materials.append(follower_material)
 follower=bpy.data.objects.new('RETURNING_ECHO_FOLLOWER_'+str(idx),follower_mesh);collection.objects.link(follower);follower['radius_m']=follower_radius;follower['relative_strength']=weight
 followers.append({'radius_m':follower_radius,'lag_m':lag,'relative_strength':weight})
# Prior sampled location remains faint; no new scan or decorative events.
bpy.data.objects['ACOUSTIC_CONTACT_CONTROLLER']['scan_fade']=.07
# Local presentation override adds subtle reception on the actual sensor surface.
layer=s.view_layers['Approved model look'];mat=layer.material_override.copy();mat.name='Still04 preserved product look with restrained reception';layer.material_override=mat;n=mat.node_tree.nodes;l=mat.node_tree.links
shader=next(n for n in n if n.bl_idname=='ShaderNodeBsdfPrincipled');geo=n.new('ShaderNodeNewGeometry');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';l.new(geo.outputs['Position'],dist.inputs[0]);dist.inputs[1].default_value=receiver
def op(kind,a,b=None):
 node=n.new('ShaderNodeMath');node.operation=kind
 for i,v in enumerate((a,b)):
  if v is None:continue
  if isinstance(v,(int,float)):node.inputs[i].default_value=v
  else:l.new(v,node.inputs[i])
 return node.outputs[0]
weight=op('EXPONENT',op('MULTIPLY',op('POWER',op('DIVIDE',dist.outputs['Value'],.009),2),-1));l.new(op('MULTIPLY',weight,1.1),shader.inputs['Emission Strength']);shader.inputs['Emission Color'].default_value=(.035,.60,.26,1)
# Receive-state tint is limited to the same soft sensor mask; global metal look unchanged.
base=shader.inputs['Base Color'];tint=n.new('ShaderNodeMixRGB');tint.blend_type='MIX';tint.inputs[1].default_value=base.default_value;tint.inputs[2].default_value=(.035,.18,.095,1)
l.new(op('MULTIPLY',weight,.30),tint.inputs[0]);l.new(tint.outputs[0],base)
# Echo must respect product occlusion as well as the existing actual wall depth.
g=s.compositing_node_group;n=g.nodes;l=g.links;beauty=next(x for x in n if x.bl_idname=='CompositorNodeRLayers' and x.layer=='Approved model look');wallnode=next(x for x in n if x.bl_idname=='CompositorNodeRLayers' and x.layer=='Wall interaction');front=next(x for x in n if x.bl_idname=='CompositorNodeRLayers' and x.layer=='Illustrative outgoing pulse')
compare=next(x for x in n if x.bl_idname=='ShaderNodeMath' and x.operation=='LESS_THAN' and x.inputs[0].is_linked and x.inputs[0].links[0].from_node==front)
nearest=n.new('ShaderNodeMath');nearest.operation='MINIMUM';l.new(beauty.outputs['Depth'],nearest.inputs[0]);l.new(wallnode.outputs['Depth'],nearest.inputs[1]);l.new(nearest.outputs[0],compare.inputs[1])
s['review_scope']='Still04 first reception, same emitting sensor. Still03 v013 continuity preserved. No Still05, text, waveform, arrows or animation.'
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));s.frame_start=s.frame_end=1
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene;t=time.perf_counter();bpy.ops.render.render(write_still=True)
record={'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'parent_scene':str(src.relative_to(P)),'parent_scene_sha256':r['scene_sha256'],'inputs':r['inputs'],'emitter_reference':list(origin),'wall_origin':list(wall),'receiver_surface':list(receiver),'receiver_object':'TEMP | Imaging port 1 | removable acoustic cap','reference_to_surface_m':(receiver-origin).length,'return_radius_m':radius,'return_color':[.05,.55,.30],'return_emission_strength':2.3,'followers':followers,'packet_spacing_m':.0045,'cap_extent_radians':.60,'wall_patch_fade':.07,'sensor_response_radius_m':.009,'sensor_response_strength':1.1,'sensor_response_color':[.035,.60,.26],'return_body_opacity_floor':.035,'return_rim_coefficient':.21,'render_seconds':time.perf_counter()-t,'resolution':[1920,1080],'physical_time_claim':False,'wave_simulation':False,'animation_rendered':False,'visual_approval':'pending'}
(E/'build-render_still04_v003.json').write_text(json.dumps(record,indent=2));print('FIRST_RECEPTION_RENDER_PASS')
