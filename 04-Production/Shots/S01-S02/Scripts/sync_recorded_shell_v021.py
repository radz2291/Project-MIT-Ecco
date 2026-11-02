"""One settled blue, camera-led upward history, and a continuation beyond the crop."""
import bpy,bmesh,json,math,bisect,datetime,hashlib
from pathlib import Path
from mathutils import Vector
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v020.blend')
out=Q/'Scenes/S01-S02_production_v021.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_shell_sync_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
s=bpy.context.scene;wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];me=wall.data;events=json.loads((Q/'Notes/approved_v016_integration.json').read_text())['events'];current={i for e in events for i in e['faces']}
s.frame_set(756)
history=[p for p in me.polygons if me.materials[p.material_index].name.startswith('PIXEL history')]
rgba=tuple(sum(me.materials[p.material_index].diffuse_color[k] for p in history)/len(history) for k in range(4))
blue=bpy.data.materials.new('Recorded shell — common settled blue');blue.diffuse_color=rgba
me.materials.append(blue);blue_idx=len(me.materials)-1;base=min(p.center.z for p in history)-.0075;old_top=max(v.co.z for v in me.vertices)
# Follow the actual camera: front stays near the upper/right picture area,
# then exits beyond the crop by the end of the pullback.
front=[];r=max(math.hypot(v.co.x,v.co.y) for v in me.vertices)
for f in range(474,721):
 s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();cam=s.camera.evaluated_get(dg);proj=cam.calc_matrix_camera(dg,x=1920,y=1080)@cam.matrix_world.inverted();p=(f-474)/246;t=max(0.,min(1.,(p-.6)/.4));bound=.88+.24*t*t*(3-2*t);best=base
 for j in range(501):
  z=base+j*.03
  for a in range(8):
   clip=proj@Vector((r*math.cos(a*math.tau/8),r*math.sin(a*math.tau/8),z,1))
   if clip.w>0:
    x=.5+.5*clip.x/clip.w;y=.5+.5*clip.y/clip.w
    if -.12<=x<=bound and -.12<=y<=bound:best=max(best,z);break
 blend=min(1.,(f-474)/24);blend=blend*blend*(3-2*blend);best=base+(best-base)*blend
 front.append(max(front[-1] if front else base,best))
new_top=max(old_top,front[-1]+.24);steps=math.ceil((new_top-old_top)/.015)
original_faces=len(me.polygons);old_centers={i:me.polygons[i].center.copy() for i in current}
bm=bmesh.new();bm.from_mesh(me);top_edges=[e for e in bm.edges if all(abs(v.co.z-old_top)<.0001 for v in e.verts)];assert len(top_edges)==128,len(top_edges)
for step in range(steps):
 result=bmesh.ops.extrude_edge_only(bm,edges=top_edges);verts=[x for x in result['geom'] if isinstance(x,bmesh.types.BMVert)];
 for v in verts:v.co.z=old_top+(step+1)*.015
 new_vertices=set(verts);top_edges=[x for x in result['geom'] if isinstance(x,bmesh.types.BMEdge) and all(v in new_vertices for v in x.verts)]
 for face in [x for x in result['geom'] if isinstance(x,bmesh.types.BMFace)]:face.material_index=blue_idx;face.smooth=True
bm.to_mesh(me);bm.free();me.update()
assert all((me.polygons[i].center-v).length<1e-5 for i,v in old_centers.items())
births=[]
for p in me.polygons:
 if p.index in current:continue
 if p.index<original_faces and not me.materials[p.material_index].name.startswith('PIXEL history'):continue
 birth=474+bisect.bisect_left(front,p.center.z)-2 if p.center.z<=front[-1] else 100000
 birth=max(474,birth);p.material_index=blue_idx;me.attributes['ecco_receipt_frame'].data[p.index].value=-2000;me.attributes['ecco_reveal_order'].data[p.index].value=birth-1
 births.append(birth)
# Preserve the acquired-patch glitch, then settle to the very same blue as history.
for e in events:
 mats={me.materials[me.polygons[i].material_index] for i in e['faces']}
 for mat in mats:
  s.frame_set(e['start']+31);sample=tuple(mat.diffuse_color);mat.animation_data.action=mat.animation_data.action.copy()
  for layer in mat.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     for fc in bag.fcurves:
      if fc.data_path!='diffuse_color':continue
      for i in range(len(fc.keyframe_points)-1,-1,-1):
       if fc.keyframe_points[i].co.x>=e['start']+31:fc.keyframe_points.remove(fc.keyframe_points[i],fast=True)
      k=fc.keyframe_points.insert(e['start']+31,sample[fc.array_index]);k.interpolation='BEZIER';k.handle_left_type='AUTO_CLAMPED';k.handle_right_type='AUTO_CLAMPED'
      for f in [e['start']+39,756]:k=fc.keyframe_points.insert(f,rgba[fc.array_index]);k.interpolation='CONSTANT'
      fc.extrapolation='CONSTANT';fc.update()
# All line/fill geometry follows the evaluated wall. Remove the old history clock.
for name in ['ONE GRID - settled shared cell boundaries','ONE GRID - every fourth contour']:
 ob=bpy.data.objects[name]
 if ob.animation_data:
  ob.animation_data.action=ob.animation_data.action.copy()
  for l in ob.animation_data.action.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      if fc.data_path in ['hide_render','hide_viewport']:fc.mute=True
 ob.hide_render=True;ob.hide_viewport=True;ob.hide_set(True)
# Retain coarse grid/contour readability, generated from revealed geometry itself.
overlay=bpy.data.objects['Shared fine measurement display'];wrapper=overlay.modifiers[0].node_group.copy();overlay.modifiers[0].node_group=wrapper;sn=next(n for n in wrapper.nodes if n.type=='GROUP');g=sn.node_tree.copy();g.name='Recorded shell — camera-synced lines and fill';sn.node_tree=g
def op(kind,a,b=None):
 n=g.nodes.new('ShaderNodeMath');n.operation=kind
 for socket,value in zip(n.inputs,[a,b]):
  if value is None:continue
  if isinstance(value,(int,float)):socket.default_value=value
  else:g.links.new(value,socket)
 return n.outputs[0]
pos=g.nodes.new('GeometryNodeInputPosition');sep=g.nodes.new('ShaderNodeSeparateXYZ');g.links.new(pos.outputs[0],sep.inputs[0]);z=op('SUBTRACT',sep.outputs['Z'],base-.06);angle=op('ARCTAN2',sep.outputs['Y'],sep.outputs['X'])
def near_multiple(value,period):
 q=op('DIVIDE',value,period);return op('LESS_THAN',op('ABSOLUTE',op('SUBTRACT',q,op('ROUND',q))),.025)
grid=op('MAXIMUM',near_multiple(z,.06),near_multiple(angle,math.tau/32))
# Retain all original tile edges on the six scan patches; only history uses the coarse grid.
receipt=g.nodes.new('GeometryNodeInputNamedAttribute');receipt.data_type='FLOAT';receipt.inputs['Name'].default_value='ecco_receipt_frame'
scan=op('MULTIPLY',op('GREATER_THAN',receipt.outputs['Attribute'],299),op('LESS_THAN',receipt.outputs['Attribute'],1000));grid=op('MAXIMUM',grid,scan)
mtc=next(n for n in g.nodes if n.type=='MESH_TO_CURVE');g.links.new(grid,mtc.inputs['Selection'])
# Stronger circumferential contour every fourth coarse row, also reveal-derived.
ring=g.nodes.new('GeometryNodeMeshToCurve');g.links.new(mtc.inputs['Mesh'].links[0].from_socket,ring.inputs['Mesh']);g.links.new(near_multiple(z,.24),ring.inputs['Selection'])
profile=g.nodes.new('GeometryNodeCurvePrimitiveCircle');profile.inputs['Resolution'].default_value=4;profile.inputs['Radius'].default_value=.0002
ctm=g.nodes.new('GeometryNodeCurveToMesh');g.links.new(ring.outputs[0],ctm.inputs['Curve']);g.links.new(profile.outputs[0],ctm.inputs['Profile Curve'])
sm=g.nodes.new('GeometryNodeSetMaterial');sm.inputs['Material'].default_value=bpy.data.objects['ONE GRID - every fourth contour'].data.materials[0];g.links.new(ctm.outputs[0],sm.inputs['Geometry']);join=next(n for n in g.nodes if n.type=='JOIN_GEOMETRY');g.links.new(sm.outputs[0],join.inputs['Geometry'])
wall['Recorded blue opacity']=rgba[3];wall['Upward reveal']='Actual camera projection 474–720; exits crop at end';wall['Recorded shell top m']=max(v.co.z for v in me.vertices)
s.frame_set(756);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/shell_sync_v021.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'common_settled_rgba':rgba,'old_top_z':old_top,'new_top_z':max(v.co.z for v in me.vertices),'extension_rings':steps,'original_faces':original_faces,'new_faces':len(me.polygons),'front_samples':[{'frame':474+i,'z':front[i]} for i in range(0,len(front),12)],'front_final_z':front[-1],'camera_pull':[474,720],'reveal_rule':'Camera-projected upper/right .88 crop frontier grows beyond1.12crop; monotonic height and native4frame settling.','current_faces_preserved':96,'unchanged':['six scan events/beam/pulse/contact timing','camera motion','closed wide cutaway','final-display exclusions','shared masters'],'legacy_history_grid_disabled':True},indent=2))
result={'saved':str(out),'rgba':rgba,'old_top':old_top,'new_top':max(v.co.z for v in me.vertices),'front_end':front[-1],'faces':len(me.polygons)}
