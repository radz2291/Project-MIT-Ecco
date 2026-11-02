"""Shot-local bore fit and native contour build. Run via official Blender MCP."""
import bpy, math, json, sys, hashlib, datetime
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v024.blend')
out=Q/'Scenes/S01-S02_production_v025.blend';assert not out.exists()
if bpy.data.is_dirty:
 bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_v025_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
wall=bpy.data.objects['ONE WALL - old history and current cells share topology']
anchor=Vector((0,0,-729.5));verts=[];faces=[]
sources=['SHOT WORLD | WORLD_S02_PHYSICAL_CUTAWAY_MESH']+[f'SHOT WORLD | WORLD_FRONT_UNIT_05_HALF_{i}' for i in range(2)]
for name in sources:
 o=bpy.data.objects[name];off=len(verts)
 verts.extend(o.matrix_world@v.co-anchor for v in o.data.vertices)
 faces.extend(tuple(off+i for i in p.vertices) for p in o.data.polygons)
bvh=BVHTree.FromPolygons(verts,faces)
wall.data=wall.data.copy();wall.data.name='S01-S02 measurement fitted to physical World v025'
old_positions=[v.co.copy() for v in wall.data.vertices]
clearance=.004;deltas=[];missing=[]
for v in wall.data.vertices:
 p=wall.matrix_world@v.co;r=math.hypot(p.x,p.y);d=Vector((p.x/r,p.y/r,0));origin=Vector((0,0,p.z))-anchor
 hit,n,idx,dist=bvh.ray_cast(origin,d,.6)
 if hit is None:missing.append(v.index);continue
 radius=dist-clearance/max(.25,abs(n.dot(d)))
 target=origin+d*radius
 for _ in range(4):
  near,normal,_,distance=bvh.find_nearest(target)
  if distance>=clearance-.00005:break
  radius-=(clearance-distance)/max(.25,abs(normal.dot(d)));target=origin+d*radius
 p.x=d.x*radius;p.y=d.y*radius
 v.co=wall.matrix_world.inverted()@p;deltas.append((v.co-old_positions[v.index]).length)
assert not missing,missing[:10]
wall.data.update();wall['Physical wall clearance m']=clearance
wall['Fit source']='World retained physical wall plus actual front closure unit05; radial projection with normal-distance clearance'
# Keep each beam and breathing contact cue attached to its newly fitted tile.
sys.path.insert(0,str(Q.parents[1]/'Shared/Assets/Effects/Waveform/Scripts'))
from pulse_asset_api import set_input
events=json.loads((Q/'Notes/approved_v016_integration.json').read_text())['events'];targets=[]
for e in events:
 ob=bpy.data.objects[f"WF sequence event {e['event']}"];A=Vector(e['source']);oldB=Vector(e['target'])
 polygons=[tuple(wall.data.polygons[i].vertices) for i in e['faces']]
 patch_bvh=BVHTree.FromPolygons([wall.matrix_world@v.co-A for v in wall.data.vertices],polygons)
 hit=patch_bvh.ray_cast(Vector(),(oldB-A).normalized(),.3);assert hit[0] is not None,e['event']
 B=A+hit[0];axis=(B-A).normalized();side=axis.cross(Vector((0,0,1))).normalized();up=side.cross(axis).normalized()
 for name,value in {'Gap length m':(B-A).length,'Route axis':tuple(axis),'Transverse axis':tuple(side),'Up axis':tuple(up)}.items():set_input(ob.modifiers[0],name,value)
 cue=bpy.data.objects[f"Contact patch event {e['event']}"];n=Vector((B.x,B.y,0)).normalized();cue.location=B-n*.00012
 targets.append({'event':e['event'],'source':list(A),'target':list(B),'target_shift_mm':(B-oldB).length*1000,'gap_m':(B-A).length})
# Native contour timing: capture tile birth before edge conversion, then grow
# profile thickness and opacity over four frames, two frames behind blue onset.
overlay=bpy.data.objects['Shared fine measurement display'];wrapper=overlay.modifiers[0].node_group.copy();overlay.modifiers[0].node_group=wrapper
groupnode=next(n for n in wrapper.nodes if n.type=='GROUP');g=groupnode.node_tree.copy();groupnode.node_tree=g;g.name='S01-S02 fitted contours with trailing build v025'
N=g.nodes;L=g.links
def node(kind,label):
 n=N.new(kind);n.label=label;return n
def mathnode(op,a,b=None):
 n=node('ShaderNodeMath',op);n.operation=op
 for i,x in enumerate([a,b]):
  if x is None:continue
  if isinstance(x,(float,int)):n.inputs[i].default_value=x
  else:L.new(x,n.inputs[i])
 return n.outputs[0]
def attr(name):
 n=node('GeometryNodeInputNamedAttribute',name);n.data_type='FLOAT';n.inputs['Name'].default_value=name;return n.outputs['Attribute']
birth=mathnode('ADD',mathnode('MAXIMUM',1,mathnode('ADD',attr('ecco_receipt_frame'),1)),attr('ecco_reveal_order'))
mtc=N['Mesh to Curve.001'];source=mtc.inputs['Mesh'].links[0].from_socket
store=node('GeometryNodeStoreNamedAttribute','Tile birth retained on contour points');store.data_type='FLOAT';store.domain='POINT';store.inputs['Name'].default_value='ecco_contour_birth'
L.new(source,store.inputs['Geometry']);L.new(birth,store.inputs['Value']);L.new(store.outputs['Geometry'],mtc.inputs['Mesh'])
time=node('GeometryNodeInputSceneTime','Native contour clock')
lag=node('ShaderNodeValue','Contour delay frames');lag.outputs[0].default_value=2
duration=node('ShaderNodeValue','Contour build frames');duration.outputs[0].default_value=4
u=mathnode('MINIMUM',1,mathnode('MAXIMUM',0,mathnode('DIVIDE',mathnode('SUBTRACT',mathnode('SUBTRACT',time.outputs['Frame'],attr('ecco_contour_birth')),lag.outputs[0]),duration.outputs[0])))
smooth=mathnode('MULTIPLY',mathnode('MULTIPLY',u,u),mathnode('SUBTRACT',3,mathnode('MULTIPLY',2,u)))
ctm=N['Curve to Mesh.001'];L.new(smooth,ctm.inputs['Scale'])
sm=N['Set Material.003'];full=sm.inputs['Material'].default_value;destinations=[link.to_socket for link in sm.outputs['Geometry'].links]
for link in list(sm.outputs['Geometry'].links):L.remove(link)
geometry=sm.outputs['Geometry'];phase=mathnode('FLOOR',mathnode('MULTIPLY',u,4))
for i in range(4):
 mat=full.copy();mat.name=f'Contour soft build {i}/4 v025';mat.diffuse_color=tuple(full.diffuse_color[:3])+(full.diffuse_color[3]*i/4,)
 eq=node('ShaderNodeMath',f'Opacity phase {i}');eq.operation='COMPARE';L.new(phase,eq.inputs[0]);eq.inputs[1].default_value=i;eq.inputs[2].default_value=.1
 stage=node('GeometryNodeSetMaterial',f'Contour opacity {i}/4');stage.inputs['Material'].default_value=mat;L.new(geometry,stage.inputs['Geometry']);L.new(eq.outputs[0],stage.inputs['Selection']);geometry=stage.outputs['Geometry']
for dest in destinations:L.new(geometry,dest)
overlay['Contour delay frames']=2;overlay['Contour build frames']=4
overlay['Contour rings enabled']=True
for n,prop in [(lag,'Contour delay frames'),(duration,'Contour build frames')]:
 fc=n.outputs[0].driver_add('default_value');v=fc.driver.variables.new();v.name='control';v.type='SINGLE_PROP';v.targets[0].id=overlay;v.targets[0].data_path='["'+prop+'"]';fc.driver.expression='max(0.001,control)' if n==duration else 'control'
enabled=node('ShaderNodeValue','Contour rings enabled');fc=enabled.outputs[0].driver_add('default_value');v=fc.driver.variables.new();v.name='enabled';v.type='SINGLE_PROP';v.targets[0].id=overlay;v.targets[0].data_path='["Contour rings enabled"]';fc.driver.expression='enabled'
L.new(mathnode('MULTIPLY',smooth,enabled.outputs[0]),ctm.inputs['Scale'])
overlay['Contour controls']='Object custom properties: Contour rings enabled, Contour delay frames, Contour build frames. Local Curve Circle.001 profile controls2mm thickness. Revealed segments persist.'
bpy.context.scene.frame_set(756);bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
record={'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v024.blend','fit_sources':sources,'minimum_normal_clearance_m':clearance,'vertices':len(deltas),'max_vertex_move_mm':max(deltas)*1000,'mean_vertex_move_mm':sum(deltas)/len(deltas)*1000,'retargeted_beams':targets,'contour_delay_frames':2,'contour_build_frames':4,'contour_radius_m':.002,'preserved':['camera and scan timings','early upward onset520','blue colors and extent','closed shell','shared masters unchanged']}
(Q/'Notes/refinements_v025.json').write_text(json.dumps(record,indent=2))
result={'saved':str(out),'vertices':len(deltas),'max_move_mm':record['max_vertex_move_mm'],'targets':targets,'ring_delay':2,'ring_build':4}
