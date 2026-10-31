import bpy,math,json,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';D=T/'Demos';D.mkdir(exist_ok=True);A=R/'04-Production/Shared/Assets';manifest=[]
def fresh(name):
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.name=name;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.eevee.taa_render_samples=4;s.eevee.use_raytracing=False;s.render.use_compositing=False;s.render.fps=24;s.world=bpy.data.worlds.new('DEMO dark background');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.006,.012,.02,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.3;return s

def controls(values):
 o=bpy.data.objects.new('DEMO CONTROLS — select then Object Custom Properties',None);bpy.context.scene.collection.objects.link(o)
 for k,(v,lo,hi,desc) in values.items():
  o[k]=v
  if isinstance(v,bool):o.id_properties_ui(k).update(description=desc)
  else:o.id_properties_ui(k).update(min=lo,max=hi,description=desc)
 return o

def drive(socket,ctl,key):
 d=socket.driver_add('default_value').driver;d.type='SCRIPTED';v=d.variables.new();v.name='value';v.targets[0].id=ctl;v.targets[0].data_path='["'+key+'"]';d.expression='value'

def frame(s,loc,target,scale):
 bpy.ops.object.camera_add(location=loc);c=bpy.context.object;c.name='DEMO viewing camera';c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.ortho_scale=scale;s.camera=c
 bpy.ops.object.light_add(type='AREA',location=(0,-6,8));l=bpy.context.object;l.name='DEMO soft light';l.data.energy=5000;l.data.shape='DISK';l.data.size=8
 for screen in bpy.data.screens:
  for area in screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False

def note(text):
 t=bpy.data.texts.new('README — SHARED ASSET DEMO');t.write(text)
 bpy.context.scene['README']=text

def save(name,ctl):
 bpy.ops.object.select_all(action='DESELECT');ctl.select_set(True);bpy.context.view_layer.objects.active=ctl
 p=D/name;bpy.ops.wm.save_as_mainfile(filepath=str(p));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(p));manifest.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})

def tree(name):
 g=bpy.data.node_groups.new(name,'GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');out=g.nodes.new('NodeGroupOutput');return g,out

def carrier(name,g):
 o=bpy.data.objects.new(name,bpy.data.meshes.new(name));bpy.context.scene.collection.objects.link(o);o.modifiers.new('Shared asset display adapter','NODES').node_group=g;return o

def crop(g,geometry,ctl):
 p=g.nodes.new('GeometryNodeInputPosition');sep=g.nodes.new('ShaderNodeSeparateXYZ');g.links.new(p.outputs[0],sep.inputs[0]);ab=g.nodes.new('ShaderNodeMath');ab.operation='ABSOLUTE';g.links.new(sep.outputs['Z'],ab.inputs[0]);gt=g.nodes.new('ShaderNodeMath');gt.operation='GREATER_THAN';g.links.new(ab.outputs[0],gt.inputs[0]);drive(gt.inputs[1],ctl,'Axial half window m');dele=g.nodes.new('GeometryNodeDeleteGeometry');dele.domain='POINT';g.links.new(geometry,dele.inputs['Geometry']);g.links.new(gt.outputs[0],dele.inputs['Selection']);return dele.outputs[0]

s=fresh('Digital environment — shared asset demo');s.frame_start=1;s.frame_end=1
with bpy.data.libraries.load(str(A/'WellAssembly/World_environment_v010.blend'),link=True) as (a,b):b.collections=['WORLD_FORMATION_IRREGULAR_CUTAWAY']
source=next(o for o in b.collections[0].objects if o.type=='MESH')
with bpy.data.libraries.load(str(A/'DigitalEnvironment/Digital_style_v001.blend'),link=True) as (a,b):b.materials=['Digital earth - charcoal layered solid']
soil=b.materials[0]
with bpy.data.libraries.load(str(A/'DigitalEnvironment/Digital_context_lines_v004.blend'),link=True) as (a,b):b.collections=['ECCO World-derived contextual cap lines v004']
lines=b.collections[0]
ctl=controls({'Axial half window m':(8.,.5,10.,'Local display crop only. World source is unchanged.'),'Show soil':(True,0,1,'Toggle actual linked physical World with shared dark-ground material.'),'Show contextual lines':(True,0,1,'Toggle linked approved derived cap-line collection.')})
for mode in ['soil','contextual lines']:
 g,out=tree('DEMO '+mode+' adapter')
 if mode=='soil':
  n=g.nodes.new('GeometryNodeObjectInfo');n.inputs['Object'].default_value=source;n.transform_space='ORIGINAL';tr=g.nodes.new('GeometryNodeTransform');tr.inputs['Rotation'].default_value=Matrix(((0,0,-1),(0,1,0),(1,0,0))).to_euler();g.links.new(n.outputs['Geometry'],tr.inputs[0]);m=g.nodes.new('GeometryNodeSetMaterial');m.inputs['Material'].default_value=soil;g.links.new(tr.outputs[0],m.inputs[0]);geo=m.outputs[0]
 else:
  n=g.nodes.new('GeometryNodeCollectionInfo');n.inputs['Collection'].default_value=lines;real=g.nodes.new('GeometryNodeRealizeInstances');g.links.new(n.outputs['Instances'],real.inputs[0]);geo=real.outputs[0]
 geo=crop(g,geo,ctl);sw=g.nodes.new('GeometryNodeSwitch');sw.input_type='GEOMETRY';drive(sw.inputs['Switch'],ctl,'Show '+mode);g.links.new(geo,sw.inputs['True']);g.links.new(sw.outputs[0],out.inputs[0]);carrier('DEMO linked '+mode,g)
frame(s,(1.4,-4,2),(0,0,.7),5.5);s.frame_set(1)
note('SHARED + DEMO ONLY. Two local empty carriers show linked World cutaway, shared dark-ground style and linked contextual cap lines. No section samples, cameras or whole section scenes. Select DEMO CONTROLS: toggle soil/lines or adjust axial display window. Context lines are derived, not live shape updates: run shared hash preflight before use; regenerate after World edits. Original World/style/context libraries are unchanged. Camera/light are demo-only framing. Native library controls remain editable at their shared sources.')
save('Digital_environment_demo_v005.blend',ctl)

s=fresh('Measurement reveal — two authored proxy shapes');s.frame_start=1;s.frame_end=84
with bpy.data.libraries.load(str(A/'MeasurementReveal/Measurement_reveal_v001.blend'),link=True) as (a,b):b.node_groups=['ECCO Stored Surface Reveal v001','ECCO Fine Surface Style v001']
rg,sg=b.node_groups
ctl=controls({'Start frame':(12.,1.,80.,'Stored display start; per-face receipt remains prior to display.'),'Stagger frames':(1.3,0.,5.,'Delay per authored row/order.'),'Settle frames':(10.,0.,30.,'Settle duration.'),'Arrival offset':(.035,0.,.1,'Small local-normal settle offset.'),'Point radius':(.0009,0.,.01,'Shared fine points radius.'),'Line radius':(.00025,0.,.005,'Shared fine lines radius.')})
for kind,xoff in [('Irregular',-.5),('Clean',.5)]:
 verts=[];faces=[];rows=28;cols=24
 for z in range(rows+1):
  for c in range(cols):
   a=2*math.pi*c/cols;r=.22*(1+.09*math.sin(z*.43+c*.3)) if kind=='Irregular' else .22;verts.append((xoff+r*math.cos(a),r*math.sin(a),(z/rows-.5)*2.4))
 for z in range(rows):
  for c in range(cols):faces.append((z*cols+c,z*cols+(c+1)%cols,(z+1)*cols+(c+1)%cols,(z+1)*cols+c))
 me=bpy.data.meshes.new(kind+' authored proxy cells');me.from_pydata(verts,[],faces);o=bpy.data.objects.new('DEMO '+kind+' proxy — not field data',me);s.collection.objects.link(o)
 for name in ['ecco_receipt_frame','ecco_reveal_order']:me.attributes.new(name,'FLOAT','FACE')
 for p in me.polygons:me.attributes['ecco_receipt_frame'].data[p.index].value=8;me.attributes['ecco_reveal_order'].data[p.index].value=p.index//cols+((p.index*11)%7)/7
 g,out=tree('DEMO '+kind+' reveal adapter');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');inp=g.nodes.new('NodeGroupInput');r=g.nodes.new('GeometryNodeGroup');r.node_tree=rg;f=g.nodes.new('GeometryNodeGroup');f.node_tree=sg;g.links.new(inp.outputs['Geometry'],r.inputs['Geometry']);g.links.new(r.outputs['Geometry'],f.inputs['Geometry']);g.links.new(f.outputs['Geometry'],out.inputs['Geometry'])
 for key in ['Start frame','Stagger frames','Settle frames','Arrival offset']:drive(r.inputs[key],ctl,key)
 for key in ['Point radius','Line radius']:drive(f.inputs[key],ctl,key)
 o.modifiers.new('Linked reveal then fine style','NODES').node_group=g;o['provenance']='Authored minimal cylinder proxy, not any section dataset. Receipt frame8; row order local.'
frame(s,(1,-5,1.2),(0,0,0),4.9);s.frame_set(34)
note('SHARED + DEMO ONLY. Two small independently authored proxy meshes, not S02/S03/S06 datasets. Same linked receipt/reveal/fine-style controls serve both. Receipt frame8; stored display begins only later. Scrub1(empty),20(early),34(partial),60(settled). DEMO CONTROLS exposes Start/Stagger/Settle/Arrival offset and fine point/line radii. Background, camera and light are demo framing only. No whole scene reused. Shared library is unchanged.')
save('Measurement_reveal_demo_v002.blend',ctl)
(T/'Evidence/demo-native-manifest.json').write_text(json.dumps(manifest,indent=2));print('DEMOS_BUILT',manifest)
