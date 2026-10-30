import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';p=T/'Consumers/S03_shared-digital_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False);target=bpy.data.objects['S03 | physical World live context'];records=[]
for name in ['Luminous geological strata','Subordinate formation survey grid']:
 old=bpy.data.objects[name];verts=[];edges=[]
 for spline in old.data.splines:
  points=[old.matrix_world@Vector(q.co[:3]) for q in spline.points]
  if spline.use_cyclic_u:points.append(points[0])
  last=None
  for a,b in zip(points,points[1:]):
   count=max(1,math.ceil((b-a).length/.025))
   for j in range(count):
    q=a.lerp(b,j/count);index=len(verts);verts.append((q.x,-.7,q.z))
    if last is not None:edges.append((last,index))
    last=index
  if points:
   q=points[-1];index=len(verts);verts.append((q.x,-.7,q.z))
   if last is not None:edges.append((last,index))
 me=bpy.data.meshes.new(name+' sampled context carrier');me.from_pydata(verts,edges,[]);ob=bpy.data.objects.new(name+' | live shared cap',me);bpy.context.scene.collection.objects.link(ob)
 g=bpy.data.node_groups.new(name+' live ray projection','GeometryNodeTree');g.interface.new_socket(name='Geometry',in_out='INPUT',socket_type='NodeSocketGeometry');g.interface.new_socket(name='Geometry',in_out='OUTPUT',socket_type='NodeSocketGeometry');i=g.nodes.new('NodeGroupInput');out=g.nodes.new('NodeGroupOutput');l=g.links
 oi=g.nodes.new('GeometryNodeObjectInfo');oi.inputs['Object'].default_value=target;oi.transform_space='RELATIVE';pos=g.nodes.new('GeometryNodeInputPosition');ray=g.nodes.new('GeometryNodeRaycast');ray.data_type='FLOAT';l.new(oi.outputs['Geometry'],ray.inputs['Target Geometry']);l.new(pos.outputs[0],ray.inputs['Source Position']);ray.inputs['Ray Direction'].default_value=(0,1,0);ray.inputs['Ray Length'].default_value=50
 add=g.nodes.new('ShaderNodeVectorMath');add.operation='ADD';l.new(ray.outputs['Hit Position'],add.inputs[0]);add.inputs[1].default_value=(0,-.003,0)
 setp=g.nodes.new('GeometryNodeSetPosition');l.new(i.outputs[0],setp.inputs[0]);l.new(add.outputs[0],setp.inputs['Position'])
 nothit=g.nodes.new('FunctionNodeBooleanMath');nothit.operation='NOT';l.new(ray.outputs['Is Hit'],nothit.inputs[0]);delete=g.nodes.new('GeometryNodeDeleteGeometry');delete.domain='POINT';l.new(setp.outputs[0],delete.inputs[0]);l.new(nothit.outputs[0],delete.inputs['Selection'])
 curve=g.nodes.new('GeometryNodeMeshToCurve');l.new(delete.outputs[0],curve.inputs['Mesh']);circle=g.nodes.new('GeometryNodeCurvePrimitiveCircle');circle.inputs['Resolution'].default_value=3;circle.inputs['Radius'].default_value=old.data.bevel_depth or .0008;cm=g.nodes.new('GeometryNodeCurveToMesh');l.new(curve.outputs[0],cm.inputs['Curve']);l.new(circle.outputs[0],cm.inputs['Profile Curve']);sm=g.nodes.new('GeometryNodeSetMaterial');sm.inputs['Material'].default_value=old.data.materials[0];l.new(cm.outputs[0],sm.inputs[0]);l.new(sm.outputs[0],out.inputs[0]);ob.modifiers.new('World-dependent context projection','NODES').node_group=g
 old.hide_render=True;ob['source_context_curve']=name;ob['rule']='Same context polyline composition, sampled25mm, rays+Yfrom-.7m to World cap, misses removed, surface offset3mm. No data geometry modified.'
 records.append({'source':name,'carrier':ob.name,'sample_points':len(verts),'edges':len(edges),'radius':circle.inputs['Radius'].default_value})
bpy.context.scene.frame_set(1);dep=bpy.context.evaluated_depsgraph_get()
for rec in records:rec['evaluated_faces']=len(bpy.data.objects[rec['carrier']].evaluated_get(dep).data.polygons)
bpy.ops.wm.save_as_mainfile(filepath=str(p));(T/'Evidence/live-grid-carriers.json').write_text(json.dumps(records,indent=2));print('LIVE_GRID_DONE')
