"""Add sparse internal motion cues to the accepted v007 annular fluid."""
import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OUT=B/'Scenes/S05_internal-flow_v008.blend';s=bpy.context.scene
for d in ['Scenes','Previews','Records','Work/Frames']:(B/d).mkdir(parents=True,exist_ok=True)
assert not OUT.exists();assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v007'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();assert prior_hash=='b1cf584c5e8a1d611717bb5d32739f445c103d63277f4046694772a04114202c'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Internal_Flow_v008'
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5)
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text());ns=dict(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=OMEGA,routes=routes)
src=(B.parent/'Interaction-Proof_v006/Scripts/build.py').read_text();exec(src[src.index('def linear('):src.index("fx=bpy.data.collections.new")],ns);linear=ns['linear'];frame_at=ns['frame_at']
fx=bpy.data.collections.new('S05_INTERNAL_WISPS_v008');s.collection.children.link(fx)
m=bpy.data.materials.new('S05_v008_SoftAmberWisp');m.use_nodes=True;m.surface_render_method='BLENDED';m.show_transparent_back=False;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
out=n.new('ShaderNodeOutputMaterial');transparent=n.new('ShaderNodeBsdfTransparent');diff=n.new('ShaderNodeBsdfDiffuse');diff.inputs['Color'].default_value=(.78,.55,.27,1);diff.inputs['Roughness'].default_value=.75
attr=n.new('ShaderNodeAttribute');attr.attribute_name='wisp_opacity';mix=n.new('ShaderNodeMixShader');l.new(attr.outputs['Fac'],mix.inputs[0]);l.new(transparent.outputs[0],mix.inputs[1]);l.new(diff.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])
g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';l.new(g.outputs['Normal'],dot.inputs[0]);l.new(g.outputs['Incoming'],dot.inputs[1]);a=n.new('ShaderNodeMath');a.operation='ABSOLUTE';l.new(dot.outputs['Value'],a.inputs[0]);mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';l.new(a.outputs[0],mul.inputs[0]);l.new(attr.outputs['Fac'],mul.inputs[1]);l.new(mul.outputs[0],mix.inputs[0])
NR=25;SIDES=10;summary=[]
for group,z36 in enumerate([.015,.205,.445]):
 for lane,(tangent_offset,radial_offset,length) in enumerate([(-.005,-.003,.052),(0,.004,.065),(.005,0,.046)]):
  states=[]
  for f in range(1,73):
   t=(f-1)/24;head=z36+.20*(t-35/24)-.024-lane*.004;verts=[]
   for j in range(NR):
    u01=j/(NR-1);z=head-length*u01;p,u,v,rr,rt=frame_at(z,t)
    p+=tangent_offset*v+radial_offset*u
    taper=max(.018,math.sin(math.pi*u01)**.8)
    for k in range(SIDES):
     a=math.tau*k/SIDES;verts.append(p+taper*(.00125*math.cos(a)*u+.0024*math.sin(a)*v))
   states.append(verts)
  faces=[(j*SIDES+k,j*SIDES+(k+1)%SIDES,(j+1)*SIDES+(k+1)%SIDES,(j+1)*SIDES+k) for j in range(NR-1) for k in range(SIDES)]
  faces.extend([tuple(reversed(range(SIDES))),tuple((NR-1)*SIDES+k for k in range(SIDES))])
  me=bpy.data.meshes.new(f'S05_v008_WispMesh_{group}_{lane}');me.from_pydata(states[0],[],faces);me.materials.append(m)
  alpha=me.attributes.new('wisp_opacity','FLOAT','POINT')
  for j in range(NR):
   for k in range(SIDES):alpha.data[j*SIDES+k].value=.58*math.sin(math.pi*j/(NR-1))**.65
  o=bpy.data.objects.new(f'S05_v008_Wisp_{group}_{lane}',me);fx.objects.link(o)
  for p in me.polygons:p.use_smooth=True
  o.shape_key_add(name='Basis');me.shape_keys.use_relative=False
  for f,verts in enumerate(states[1:],2):
   key=o.shape_key_add(name=f'Frame_{f:03}')
   for v,co in zip(key.data,verts):v.co=co
  for key in me.shape_keys.key_blocks:key.interpolation='KEY_LINEAR'
  for f in [1,72]:me.shape_keys.eval_time=(f-1)*10;me.shape_keys.keyframe_insert('eval_time',frame=f)
  linear(me.shape_keys);summary.append({'name':o.name,'group':group,'length_m':length,'tangent_offset_m':tangent_offset,'radial_offset_m':radial_offset})
# Keep sizes and trajectories; increase matte facet separation and rough texture.
for name,color in [('Body',(.045,.039,.031)),('Light',(.35,.30,.22)),('Dark',(.009,.008,.006))]:
 old=bpy.data.materials['S05_v007_Cutting'+name];new=old.copy();new.name='S05_v008_Cutting'+name;p=new.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.96
 noise=new.node_tree.nodes.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=420;noise.inputs['Detail'].default_value=2;bump=new.node_tree.nodes.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.3;bump.inputs['Distance'].default_value=.00025;new.node_tree.links.new(noise.outputs['Fac'],bump.inputs['Height']);new.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
 for o in bpy.data.collections['S05_ANNULAR_FLUID_v007'].objects:
  if 'Cutting' in o.name:
   for slot in o.material_slots:
    if slot.material==old:slot.material=new
s.frame_set(36);s.render.filepath=str(B/'Previews/interaction_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-t
s['proof_scope']='v008 accepted v007 annulus with three groups of non-emissive internal wisps, same-scale matte cuttings and independent upward transport; three-second illustrative proof'
result={'render_seconds':seconds,'prior_v007_sha256':prior_hash,'preserved':['fluid domain geometry and shading','camera','hardware','borehole','rotation','cutting sizes and trajectories'],'groups':3,'wisps':summary,'paired_transport':'Each group trails one cutting by 24 mm plus its lane offset. Positions follow the same geometry-aware field, not hardware parenting.','limits':'Illustrative motion cues within the accepted volume; not resolved fluid dynamics or measured transport.'}
(B/'Records/build.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
