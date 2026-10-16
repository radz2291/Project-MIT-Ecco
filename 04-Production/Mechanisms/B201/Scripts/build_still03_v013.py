"""Approved spherical-cap membrane + wall-attached digital sampling illustration."""
import bpy, math, json, hashlib, time
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[3]; M=P/'Mechanisms/B201'; E=P/'Records/Tasks/T-007/Evidence/Still_03'
src=M/'Scenes/B201_wall-interaction_still03_v010.blend'; out=M/'Scenes/B201_wall-interaction_still03_v013.blend'; png=M/'Previews/Still_03/B201_wall-interaction_still03_v013.png'
assert not out.exists()
r=json.loads((E/'build-render_still03_v010.json').read_text())
assert hashlib.sha256(src.read_bytes()).hexdigest()==r['scene_sha256']
bpy.ops.wm.open_mainfile(filepath=str(src)); s=bpy.context.scene
origin=Vector(r['origin']); wall=Vector(r['wall']); normal=(wall-origin).normalized(); distance=(wall-origin).length
ax=Vector((1,0,0)); az=Vector((0,-normal.z,normal.y))
coll=bpy.data.collections['STILL02_ILLUSTRATIVE_WAVEFRONT']
for ob in list(coll.objects):
 if ob.name.startswith('OUTGOING_WAVEFRONT_ILLUSTRATION_'):bpy.data.objects.remove(ob,do_unlink=True)
controller=bpy.data.objects.new('ACOUSTIC_CONTACT_CONTROLLER',None);s.collection.objects.link(controller);controller.location=wall
controller['scan_radius_x_m']=.012;controller['scan_radius_y_m']=.019;controller['cell_size_m']=.0015;controller['scan_opacity']=.8;controller['scan_fade']=1.0
controller['meaning']='Illustrative localized acquisition, not a measured rock image from a single ping'
radii=[.026,.036,distance+.002]
controller['leading_radius_m']=radii[-1]
controller['contact_band_m']=.00065
for idx,radius in enumerate(radii):
 vs=[];fs=[];values=[]
 for i in range(65):
  theta=.65*i/64
  for j in range(160):
   phi=math.tau*j/160
   vs.append(origin+radius*(normal*math.cos(theta)+ax*math.sin(theta)*math.cos(phi)+az*math.sin(theta)*math.sin(phi)))
   values.append(min(1,max(0,(.65-theta)/.10)))
 for i in range(64):
  for j in range(160):
   k=i*160+j;q=i*160+(j+1)%160;fs.append((k,q,q+160,k+160))
 me=bpy.data.meshes.new('Thin spherical cap membrane');me.from_pydata(vs,[],fs);me.update()
 for f in me.polygons:f.use_smooth=True
 attr=me.color_attributes.new(name='BoundaryFade',type='FLOAT_COLOR',domain='CORNER')
 for loop in me.loops:attr.data[loop.index].color=(values[loop.vertex_index],)*3+(1,)
 ob=bpy.data.objects.new('OUTGOING_WAVEFRONT_ILLUSTRATION_'+str(idx+1),me);coll.objects.link(ob);ob['radius_m']=radius;ob['sphere_origin']=list(origin);ob['contact_controller']=controller.name
 mat=bpy.data.materials.new('Thin restrained cyan membrane');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();l=mat.node_tree.links
 geo=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(geo.outputs['Normal'],dot.inputs[0]);l.new(geo.outputs['Incoming'],dot.inputs[1])
 def op(kind,a=None,b=None):
  node=n.new('ShaderNodeMath');node.operation=kind
  for i,v in enumerate((a,b)):
   if v is not None:
    if isinstance(v,(int,float)):node.inputs[i].default_value=v
    else:l.new(v,node.inputs[i])
  return node.outputs[0]
 facing=op('SUBTRACT',1,op('ABSOLUTE',dot.outputs['Value']));alpha=op('MULTIPLY_ADD',op('POWER',facing,2),.19)
 # Third multiply-add input supplies almost invisible center opacity.
 alpha.node.inputs[2].default_value=.025
 fade=n.new('ShaderNodeVertexColor');fade.layer_name='BoundaryFade';alpha=op('MULTIPLY',alpha,fade.outputs['Color'])
 tr=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(.18,.55,1,1);em.inputs[1].default_value=2.6
 mix=n.new('ShaderNodeMixShader');l.new(alpha,mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);output=n.new('ShaderNodeOutputMaterial');l.new(mix.outputs[0],output.inputs[0]);me.materials.append(mat)
# Shader-driven pattern is evaluated directly on actual irregular rock: no floating plane.
section=bpy.data.objects['T6_WALL_CONTACT_SECTION'];mat=section.data.materials[0];n=mat.node_tree.nodes;l=mat.node_tree.links
shader=next(x for x in n if x.bl_idname=='ShaderNodeBsdfPrincipled');geometry=next(x for x in n if x.bl_idname=='ShaderNodeNewGeometry')
for link in list(shader.inputs['Emission Strength'].links):l.remove(link)
def op(kind,a=None,b=None):
 node=n.new('ShaderNodeMath');node.operation=kind
 for i,v in enumerate((a,b)):
  if v is not None:
   if isinstance(v,(int,float)):node.inputs[i].default_value=v
   else:l.new(v,node.inputs[i])
 return node.outputs[0]
def control(prop):
 node=n.new('ShaderNodeValue');node.label=prop;d=node.outputs[0].driver_add('default_value').driver;v=d.variables.new();v.name='v';v.targets[0].id=controller;v.targets[0].data_path='["'+prop+'"]';d.expression='v';return node.outputs[0]
sub=n.new('ShaderNodeVectorMath');sub.operation='SUBTRACT';l.new(geometry.outputs['Position'],sub.inputs[0]);sub.inputs[1].default_value=wall
for i in range(3):
 d=sub.inputs[1].driver_add('default_value',i).driver;v=d.variables.new();v.name='v';v.targets[0].id=controller;v.targets[0].data_path='location['+str(i)+']';d.expression='v'
coords=[]
for axis in (ax,az):
 dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(sub.outputs[0],dot.inputs[0]);dot.inputs[1].default_value=axis;coords.append(dot.outputs['Value'])
x,y=coords;rx=control('scan_radius_x_m');ry=control('scan_radius_y_m');cell=control('cell_size_m')
ellipse=op('ADD',op('POWER',op('DIVIDE',x,rx),2),op('POWER',op('DIVIDE',y,ry),2))
# Irregular influence and two cell scales, modulated by rock relief and stable noise.
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=330;noise.inputs['Detail'].default_value=2.5;l.new(geometry.outputs['Position'],noise.inputs['Vector'])
warp=op('ADD',op('MULTIPLY',noise.outputs['Fac'],.85),.55)
mask=op('EXPONENT',op('MULTIPLY',op('POWER',op('MULTIPLY',ellipse,warp),2),-1.6))
# Wave/rock intersection controls both the activation footprint and the bright contact band.
rad=n.new('ShaderNodeVectorMath');rad.operation='DISTANCE';l.new(geometry.outputs['Position'],rad.inputs[0]);rad.inputs[1].default_value=origin
signed=op('SUBTRACT',control('leading_radius_m'),rad.outputs['Value'])
arrived=op('MINIMUM',op('MAXIMUM',op('ADD',op('DIVIDE',signed,.0012),.5),0),1)
band=op('EXPONENT',op('MULTIPLY',op('POWER',op('DIVIDE',signed,control('contact_band_m')),2),-1))
def cells(cellscale):
 gx=op('DIVIDE',x,cellscale);gy=op('DIVIDE',y,cellscale);lines=[]
 for c in (gx,gy):
  f=op('FRACT',c);near=op('MINIMUM',f,op('SUBTRACT',1,f));lines.append(op('LESS_THAN',near,.045))
 grid=op('MAXIMUM',*lines)
 seed=op('ADD',op('MULTIPLY',op('FLOOR',gx),12.9898),op('MULTIPLY',op('FLOOR',gy),78.233))
 random=op('FRACT',op('MULTIPLY',op('SINE',seed),43758.5453));active=op('GREATER_THAN',random,.47)
 brightness=op('ADD',op('MULTIPLY',random,.75),.25)
 return op('MULTIPLY',op('ADD',op('MULTIPLY',grid,.85),.07),op('MULTIPLY',active,brightness))
coarse=cells(cell);fine=cells(op('MULTIPLY',cell,.5))
pattern=op('ADD',coarse,op('MULTIPLY',fine,op('GREATER_THAN',noise.outputs['Fac'],.52)))
relief=op('ADD',op('MULTIPLY',noise.outputs['Fac'],.65),.35)
activation=op('MULTIPLY',op('MULTIPLY',pattern,arrived),relief)
# Narrow curved luminous seam precisely where the membrane intersects the actual rock.
combined=op('ADD',activation,op('MULTIPLY',band,.38))
effect=op('MULTIPLY',op('MULTIPLY',mask,combined),control('scan_opacity'));effect=op('MULTIPLY',effect,control('scan_fade'))
l.new(op('MULTIPLY',effect,3.5),shader.inputs['Emission Strength']);shader.inputs['Emission Color'].default_value=(.10,.5,1,1)
section['effect']='Localized irregular digital acquisition patch on actual rock; illustrative, not measured data';section['contact_controller']=controller.name
s['review_scope']='Approved effect concepts implemented; exact contact still only. Camera/geometry preserved from v010. No echo/text/motion.'
s.render.filepath=bpy.path.relpath(str(png),start=str(out.parent));bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False);bpy.ops.wm.open_mainfile(filepath=str(out));s=bpy.context.scene
t=time.perf_counter();bpy.ops.render.render(write_still=True)
record={**r,'scene':str(out.relative_to(P)),'image':str(png.relative_to(P)),'scene_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'image_sha256':hashlib.sha256(png.read_bytes()).hexdigest(),'parent_scene_sha256':r['scene_sha256'],'front_radii_m':radii,'camera_unchanged':True,'camera_unchanged_from':'Still03 v010','representation':'Thin source-centered spherical-cap membranes + wall-conforming procedural digital scan illustration','render_seconds':time.perf_counter()-t,'peak_advance_m':.002,'activation':'Cells only within leading spherical arrival envelope; curved contact band is the actual sphere-rock intersection','patch_radii_m':[.012,.019],'cell_size_m':.0015,'contact_controller':'ACOUSTIC_CONTACT_CONTROLLER','contact_glow':'Digital acquisition illustration on actual rock, not physical emitted light','visual_approval':'pending'}
record.pop('wave_envelopes',None)
(E/'build-render_still03_v013.json').write_text(json.dumps(record,indent=2));print('CONTACT_STILL_RENDER_PASS')
