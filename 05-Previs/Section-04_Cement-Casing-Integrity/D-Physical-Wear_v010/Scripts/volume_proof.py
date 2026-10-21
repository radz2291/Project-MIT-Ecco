import bpy,math,time,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1]
old=B.parent/'D-Physical-Wear_v009/Scenes/S04_D_physical-comparison_v009.blend'
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only'];bpy.context.window.scene=s
original_meshes={o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
cam=[list(r) for r in s.camera.matrix_world];lens=s.camera.data.lens
source=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];tree=BVHTree.FromPolygons([v.co for v in source.data.vertices],[list(p.vertices) for p in source.data.polygons])
RI=.1589405;X0=-2.10;X1=-1.5125;A0=-.35;A1=.35;NX=32;NA=48
coll=bpy.data.collections.new('Illustrative missing-steel inspection volume');s.collection.children.link(coll)
def radius(x,a):
 d=Vector((0,math.cos(a),math.sin(a)));p=tree.ray_cast(Vector((x,0,0)),d,1)[0]
 if p is None:raise RuntimeError('Source wall missing')
 return math.hypot(p.y,p.z)
def xyz(x,a,r):return (x,r*math.cos(a),r*math.sin(a))
vs=[];depths=[]
for layer in range(2):
 for i in range(NX+1):
  x=X0+(X1-X0)*i/NX
  for j in range(NA+1):
   a=A0+(A1-A0)*j/NA;r=radius(x,a);depths.append(r-RI)
   assert r>RI
   vs.append(xyz(x,a,RI if layer==0 else r))
size=(NX+1)*(NA+1);idx=lambda i,j:i*(NA+1)+j;faces=[]
for i in range(NX):
 for j in range(NA):
  q=(idx(i,j),idx(i+1,j),idx(i+1,j+1),idx(i,j+1));faces.append(tuple(reversed(q)));faces.append(tuple(k+size for k in q))
for i in [0,NX]:
 for j in range(NA):q=idx(i,j);faces.append((q,q+1,q+1+size,q+size))
for j in [0,NA]:
 for i in range(NX):q=idx(i,j);q2=idx(i+1,j);faces.append((q,q2,q2+size,q+size))
mesh=bpy.data.meshes.new('Exact radial gap between nominal and source wall');mesh.from_pydata(vs,[],faces);mesh.update();o=bpy.data.objects.new('Missing-steel volume - local illustrative reconstruction',mesh);coll.objects.link(o)
mat=bpy.data.materials.new('Quiet translucent cyan - explanatory missing steel');mat.use_nodes=True;ns=mat.node_tree.nodes;ns.clear();tr=ns.new('ShaderNodeBsdfTransparent');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(.025,.45,.60,1);em.inputs[1].default_value=.7;mix=ns.new('ShaderNodeMixShader');mix.inputs[0].default_value=.10;out=ns.new('ShaderNodeOutputMaterial');li=mat.node_tree.links;li.new(tr.outputs[0],mix.inputs[1]);li.new(em.outputs[0],mix.inputs[2]);li.new(mix.outputs[0],out.inputs['Surface']);mesh.materials.append(mat)
clear=bpy.data.materials.new('Actual wall boundary - no duplicate shading');clear.use_nodes=True;cn=clear.node_tree.nodes;cn.clear();ct=cn.new('ShaderNodeBsdfTransparent');co=cn.new('ShaderNodeOutputMaterial');clear.node_tree.links.new(ct.outputs[0],co.inputs['Surface']);mesh.materials.append(clear)
for i in range(NX*NA):mesh.polygons[i*2+1].material_index=1
if hasattr(mat,'surface_render_method'):mat.surface_render_method='BLENDED'
cyan=bpy.data.materials['Existing worn inner surface - cyan profile'];white=bpy.data.materials['Original inner surface - dashed reference']
def line(name,pts,m,width=.00009):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=1;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,c);coll.objects.link(ob);c.materials.append(m)
for k in range(1,6):
 x=X1+(X0-X1)*k/5
 line('Depth contour %d - actual source wall'%k,[xyz(x,A0+(A1-A0)*j/NA,radius(x,A0+(A1-A0)*j/NA)-.00004) for j in range(NA+1)],cyan)
for a in [A0,0,A1]:
 line('Axial reconstructed boundary %.2f'%a,[xyz(X0+(X1-X0)*i/NX,a,RI-.00004) for i in range(NX+1)],white,.00007)
for name in ['Original-current comparison bracket','Original bracket tick','Current bracket tick']:
 ob=s.objects.get(name)
 if ob:ob.hide_render=True;ob.hide_viewport=True
s['scope']='Owner requested 3D-volume graphic after accepting v009 composite. One still only, same shot/steel. No calibrated volume number or direct volumetric sensing claim.'
s['volume_scope']='Local sampled inspection portion, not the whole worn volume. Nominal reference boundary to actual source inner wall, fixed recorded geometry.'
assert cam==[list(r) for r in s.camera.matrix_world] and lens==s.camera.data.lens
assert all(hashlib.sha256(repr(([tuple(v.co) for v in bpy.data.objects[n].data.vertices],[tuple(p.vertices) for p in bpy.data.objects[n].data.polygons])).encode()).hexdigest()==h for n,h in original_meshes.items())
out=B/'Scenes/S04_D_volume-comparison_v010.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.eevee.taa_render_samples=8
s.render.filepath=str(B/'Previews/S04_D_volume-comparison_v010.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps(dict(render_seconds=elapsed,under_5_seconds=elapsed<5,physical_meshes_unchanged=True,camera_unchanged=True,inspection_volume_x_m=[X0,X1],inspection_volume_azimuth_rad=[A0,A1],sampled_gap_m=[min(depths),max(depths)],volume_source='Nominal RI to radial ray hits on actual registered source mesh',radial_scale=1,no_numeric_volume_claim=True,previous_comparison_bracket_hidden=True,source=str(old)),indent=2));print('VOLUME_SECONDS',elapsed,flush=True)



