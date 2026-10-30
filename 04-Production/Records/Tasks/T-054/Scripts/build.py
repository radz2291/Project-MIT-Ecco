"""Shared styling/reveal; local data and source scene files remain unchanged."""
import bpy, json, math, hashlib
from pathlib import Path
from mathutils import Matrix,Vector
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';A=R/'04-Production/Shared/Assets'
S={x['id']:R/x['native'] for x in json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text())}
D=A/'DigitalEnvironment'; V=A/'MeasurementReveal';D.mkdir(exist_ok=True);V.mkdir(exist_ok=True)
STYLE=D/'Digital_style_v001.blend';REVEAL=V/'Measurement_reveal_v001.blend'

def save(p):
 bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p))

# Exact source materials; no reconstruction/data materials are exported.
bpy.ops.wm.open_mainfile(filepath=str(S['S03']),load_ui=False)
names=['Digital earth - charcoal layered solid','HUD restrained cyan contours','Luminous geological strata','Subordinate formation survey grid']
mats={bpy.data.materials[n] for n in names}
for m in mats:m.use_fake_user=True
bpy.data.libraries.write(str(STYLE),mats,path_remap='RELATIVE',fake_user=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(STYLE),link=True) as (a,b):b.materials=list(names)
mat=dict(zip(names,b.materials))

def socket(g,name,typ,side='INPUT',value=None):
 s=g.interface.new_socket(name=name,in_out=side,socket_type=typ)
 if value is not None:s.default_value=value
 return s

def mathnode(g,op,a=None,b=None):
 n=g.nodes.new('ShaderNodeMath');n.operation=op
 for ix,v in enumerate([a,b]):
  if v is None:continue
  if isinstance(v,(int,float)):n.inputs[ix].default_value=v
  else:g.links.new(v,n.inputs[ix])
 return n.outputs[0]

g=bpy.data.node_groups.new('ECCO Stored Surface Reveal v001','GeometryNodeTree');g.use_fake_user=True
socket(g,'Geometry','NodeSocketGeometry');socket(g,'Geometry','NodeSocketGeometry','OUTPUT')
for name,val in [('Start frame',1),('Stagger frames',1),('Settle frames',10),('Arrival offset',.006)]:socket(g,name,'NodeSocketFloat',value=val)
i=g.nodes.new('NodeGroupInput');o=g.nodes.new('NodeGroupOutput');l=g.links
time=g.nodes.new('GeometryNodeInputSceneTime')
receipt=g.nodes.new('GeometryNodeInputNamedAttribute');receipt.data_type='FLOAT';receipt.inputs['Name'].default_value='ecco_receipt_frame'
order=g.nodes.new('GeometryNodeInputNamedAttribute');order.data_type='FLOAT';order.inputs['Name'].default_value='ecco_reveal_order'
start=mathnode(g,'MAXIMUM',i.outputs['Start frame'],mathnode(g,'ADD',receipt.outputs['Attribute'],1))
arrival=mathnode(g,'ADD',start,mathnode(g,'MULTIPLY',order.outputs['Attribute'],i.outputs['Stagger frames']))
elapsed=mathnode(g,'SUBTRACT',time.outputs['Frame'],arrival)
delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='FACE';l.new(i.outputs['Geometry'],delete.inputs['Geometry']);l.new(mathnode(g,'LESS_THAN',elapsed,0),delete.inputs['Selection'])
progress=mathnode(g,'MINIMUM',mathnode(g,'MAXIMUM',mathnode(g,'DIVIDE',elapsed,i.outputs['Settle frames']),0),1)
offset=mathnode(g,'MULTIPLY',mathnode(g,'SUBTRACT',1,progress),i.outputs['Arrival offset'])
normal=g.nodes.new('GeometryNodeInputNormal');scale=g.nodes.new('ShaderNodeVectorMath');scale.operation='SCALE';l.new(normal.outputs[0],scale.inputs[0]);l.new(offset,scale.inputs['Scale'])
pos=g.nodes.new('GeometryNodeSetPosition');l.new(delete.outputs[0],pos.inputs['Geometry']);l.new(scale.outputs['Vector'],pos.inputs['Offset']);l.new(pos.outputs[0],o.inputs['Geometry'])
g['meaning']='Stored display only. Local receipt frame + 1 minimum; no additional acquisition. Order and receipt attributes stay on local sample mesh.'
g['source']='S02 v011 staggered arrival and ten-frame settle; reusable topology-independent implementation'

style=bpy.data.node_groups.new('ECCO Fine Surface Style v001','GeometryNodeTree');style.use_fake_user=True
socket(style,'Geometry','NodeSocketGeometry');socket(style,'Geometry','NodeSocketGeometry','OUTPUT')
socket(style,'Point radius','NodeSocketFloat',value=.0009);socket(style,'Line radius','NodeSocketFloat',value=.00025)
si=style.nodes.new('NodeGroupInput');so=style.nodes.new('NodeGroupOutput');sl=style.links
edges=style.nodes.new('GeometryNodeMeshToCurve');sl.new(si.outputs[0],edges.inputs['Mesh'])
circle=style.nodes.new('GeometryNodeCurvePrimitiveCircle');circle.inputs['Resolution'].default_value=3;sl.new(si.outputs['Line radius'],circle.inputs['Radius'])
cm=style.nodes.new('GeometryNodeCurveToMesh');sl.new(edges.outputs[0],cm.inputs['Curve']);sl.new(circle.outputs[0],cm.inputs['Profile Curve'])
sm=style.nodes.new('GeometryNodeSetMaterial');sm.inputs['Material'].default_value=mat['HUD restrained cyan contours'];sl.new(cm.outputs[0],sm.inputs[0])
pts=style.nodes.new('GeometryNodeMeshToPoints');pts.mode='VERTICES';sl.new(si.outputs[0],pts.inputs['Mesh'])
ico=style.nodes.new('GeometryNodeMeshIcoSphere');ico.inputs['Subdivisions'].default_value=1;sl.new(si.outputs['Point radius'],ico.inputs['Radius'])
ip=style.nodes.new('GeometryNodeInstanceOnPoints');sl.new(pts.outputs[0],ip.inputs['Points']);sl.new(ico.outputs[0],ip.inputs['Instance'])
ri=style.nodes.new('GeometryNodeRealizeInstances');sl.new(ip.outputs[0],ri.inputs[0]);pm=style.nodes.new('GeometryNodeSetMaterial');pm.inputs['Material'].default_value=mat['HUD restrained cyan contours'];sl.new(ri.outputs[0],pm.inputs[0])
# Delicate translucent fill, separate from section amplitude colors.
fill=bpy.data.materials.new('ECCO translucent display fill v001');fill.use_nodes=True;fill.diffuse_color=(.025,.19,.3,.12)
bs=fill.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.025,.19,.3,1);bs.inputs['Alpha'].default_value=.12;bs.inputs['Roughness'].default_value=.4
fm=style.nodes.new('GeometryNodeSetMaterial');fm.inputs['Material'].default_value=fill;sl.new(si.outputs[0],fm.inputs[0])
join=style.nodes.new('GeometryNodeJoinGeometry')
for n in [sm,pm,fm]:sl.new(n.outputs[0],join.inputs[0])
sl.new(join.outputs[0],so.inputs[0])
bpy.data.libraries.write(str(REVEAL),{g,style},path_remap='RELATIVE',fake_user=True)

# A canonical digital World wrapper references live physical meshes, not copies.
world=A/'WellAssembly/World_environment_v010.blend'
with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_S02_PHYSICAL_CUTAWAY']
src=next(o for o in b.collections[0].objects if o.type=='MESH')
mesh=bpy.data.meshes.new('Digital World empty carrier');obj=bpy.data.objects.new('Digital World | linked physical authority',mesh);bpy.context.scene.collection.objects.link(obj)
wg=bpy.data.node_groups.new('Digital World source wrapper v001','GeometryNodeTree');socket(wg,'Geometry','NodeSocketGeometry','OUTPUT')
oi=wg.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=src;oi.transform_space='ORIGINAL'
ms=wg.nodes.new('GeometryNodeSetMaterial');ms.inputs['Material'].default_value=mat[names[0]];wg.links.new(oi.outputs['Geometry'],ms.inputs[0]);wo=wg.nodes.new('NodeGroupOutput');wg.links.new(ms.outputs[0],wo.inputs[0]);obj.modifiers.new('World live shape / separate digital look','NODES').node_group=wg
obj['source_rule']='World v010 canonical X coordinates. Local display transforms/windows belong to consumers. No measured data in this file.'
save(D/'Digital_world_v001.blend')

# Native proof: two local illustrative shape cases using same linked reveal/style.
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(REVEAL),link=True) as (a,b):b.node_groups=['ECCO Stored Surface Reveal v001','ECCO Fine Surface Style v001']
rg,sg=b.node_groups
for variant,xoff in [('irregular',-.5),('clean',.5)]:
 verts=[];faces=[];rows=40;cols=24
 for z in range(rows+1):
  for c in range(cols+1):
   a=2*math.pi*c/cols;r=.18*(1+.09*math.sin(z*.43+c*.3)) if variant=='irregular' else .18
   verts.append((xoff+r*math.cos(a),r*math.sin(a),(z/rows-.5)*2.4))
 for z in range(rows):
  for c in range(cols):
   q=z*(cols+1)+c;faces.append((q,q+1,q+cols+2,q+cols+1))
 me=bpy.data.meshes.new(variant+' local illustrative samples');me.from_pydata(verts,[],faces);ob=bpy.data.objects.new(variant+' | receipt then stored reveal',me);bpy.context.scene.collection.objects.link(ob)
 for name in ['ecco_receipt_frame','ecco_reveal_order']:me.attributes.new(name,'FLOAT','FACE')
 for p in me.polygons:
  row=p.index//cols;col=p.index%cols;me.attributes['ecco_receipt_frame'].data[p.index].value=1;me.attributes['ecco_reveal_order'].data[p.index].value=row+((row*17+col*11+row*col*3)%7)/7
 for name,group in [('Receipt before recording',rg),('Fine points lines and fill',sg)]:ob.modifiers.new(name,'NODES').node_group=group
 ob['provenance']='Authored shape test only, not field samples. Same display accepts distinct local shapes.'
s=bpy.context.scene;s.frame_start=1;s.frame_end=60;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.fps=24
bpy.ops.object.camera_add(location=(3,-5,2));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=3.1;s.camera=cam
s.world=bpy.data.worlds.new('Reveal proof world');s.world.color=(.015,.015,.015);bpy.ops.object.light_add(type='AREA',location=(1,-2,4));bpy.context.object.data.energy=400;bpy.context.object.data.shape='DISK';bpy.context.object.data.size=5
s.frame_set(35);save(T/'Consumers/Reveal_two-shapes_v001.blend')

# S03/S06 actual integration copies: shared exact source materials; local data untouched.
mapping=[]
for sid in ['S03','S06']:
 bpy.ops.wm.open_mainfile(filepath=str(S[sid]),load_ui=False)
 with bpy.data.libraries.load(str(STYLE),link=True) as (a,b):b.materials=list(names)
 linked=dict(zip(names,b.materials));changed=[]
 if sid=='S03':
  for ob in bpy.data.objects:
   if not ob.data or not hasattr(ob.data,'materials'):continue
   for slot in ob.material_slots:
    if slot.material and slot.material.name in linked:
     replacement=linked[slot.material.name];slot.link='OBJECT';slot.material=replacement;changed.append(ob.name)
 else:
  # S06 local material opacity/color attributes and every keyframe remain local.
  for ob in bpy.data.objects:
   if ob.name.startswith(('A depth contour','A length contour')):
    for slot in ob.material_slots:
     if not slot.material:continue
     local=slot.material.copy();local.name='T054 local opacity | '+ob.name
     # shared material referenced as provenance; original animated transparency retained.
     local['shared_style_library']='Digital_style_v001.blend';local['shared_contour_source']='HUD restrained cyan contours'
     slot.link='OBJECT';slot.material=local;changed.append(ob.name)
 # Reference World collection retained without rendering a duplicate physical shell.
 with bpy.data.libraries.load(str(world),link=True) as (a,b):b.collections=['WORLD_S02_IRREGULAR_AUTHORITY']
 bpy.context.scene['shared_world_authority']='World_environment_v010.blend; canonical X, section samples independent'
 bpy.context.scene['integration_scope']='Linked style; section data and camera unchanged. Physical-context replacement requires scene-specific window adapter.'
 out=T/'Consumers'/f'{sid}_shared-digital_v001.blend';save(out);mapping.append({'baseline':str(S[sid].relative_to(R)),'candidate':str(out.relative_to(R)),'changed':changed})
(T/'Evidence/consumer-mappings.json').write_text(json.dumps(mapping,indent=2));print('BUILD_DONE')
