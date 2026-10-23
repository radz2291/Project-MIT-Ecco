"""Full annular fluid representation, static composition study first."""
import bpy,math,json,time,bmesh
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
import numpy as np
B=Path(__file__).resolve().parents[1];OUT=B/'Scenes/S05_fluid-volume_v007.blend';s=bpy.context.scene
for d in ['Scenes','Previews','Records','Work/Frames']:(B/d).mkdir(parents=True,exist_ok=True)
assert not OUT.exists()
assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v006'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Fluid_Representation_v007'
bpy.data.collections['S05_FOCUSED_PASSAGE_v006'].hide_render=True;bpy.data.collections['S05_FOCUSED_PASSAGE_v006'].hide_viewport=True
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));h=tree.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(h.x,h.y) if h else .105
NZ=151;NA=240;Z0=-.09;Z1=.66;zs=np.linspace(Z0,Z1,NZ);angles=np.arange(NA)*math.tau/NA
raw=np.array([[surface(float(z),float(a)) for a in angles] for z in zs]);robust=raw.copy()
for dz in [-1,0,1]:
 for da in [-1,0,1]:robust=np.maximum(robust,np.roll(raw[np.clip(np.arange(NZ)+dz,0,NZ-1)],da,axis=1))
inner=robust+.001;outer=R-.001;assert inner.max()<outer
fx=bpy.data.collections.new('S05_ANNULAR_FLUID_v007');s.collection.children.link(fx)
def transparent_surface(name,alpha,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
 out=n.new('ShaderNodeOutputMaterial');tr=n.new('ShaderNodeBsdfTransparent');bs=n.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Roughness'].default_value=.24;bs.inputs['Specular IOR Level'].default_value=.25
 mix=n.new('ShaderNodeMixShader');mix.inputs[0].default_value=alpha;l.new(tr.outputs[0],mix.inputs[1]);l.new(bs.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface'])
 return m,out
fluid,out=transparent_surface('S05_v007_SectionedFluid',.12,(.50,.26,.055));n=fluid.node_tree.nodes;l=fluid.node_tree.links
vol=n.new('ShaderNodeVolumePrincipled');vol.inputs['Density'].default_value=9;vol.inputs['Color'].default_value=(.72,.45,.13,1);vol.inputs['Anisotropy'].default_value=.05;l.new(vol.outputs[0],out.inputs['Volume'])
inner_mat,_=transparent_surface('S05_v007_InnerFluidInterface',0,(.5,.3,.1))
cut_mat,_=transparent_surface('S05_v007_FluidSectionFace',.32,(.56,.32,.08))
verts=[]
for outer_layer in [False,True]:
 for j,z in enumerate(zs):
  for i,a in enumerate(angles):
   r=outer if outer_layer else inner[j,i];verts.append((r*math.cos(a),r*math.sin(a),z))
N=NZ*NA;faces=[];mats=[]
for layer in [0,1]:
 for j in range(NZ-1):
  for i in range(NA):
   a=layer*N+j*NA+i;b=layer*N+j*NA+(i+1)%NA;c=b+NA;d=a+NA;faces.append((a,b,c,d) if layer else (d,c,b,a));mats.append(0 if layer else 1)
for j in [0,NZ-1]:
 for i in range(NA):
  a=j*NA+i;b=j*NA+(i+1)%NA;faces.append((a,b,b+N,a+N));mats.append(2)
me=bpy.data.meshes.new('S05_v007_TrueAnnulus');me.from_pydata(verts,[],faces)
for m in [fluid,inner_mat,cut_mat]:me.materials.append(m)
for p,mi in zip(me.polygons,mats):p.material_index=mi;p.use_smooth=mi!=2
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
o=bpy.data.objects.new('S05_v007_AnnularFluidDomain',me);fx.objects.link(o);o['representation']='Full finite annular fluid domain; outer boundary is illustrative section, not free liquid surface.'
o.rotation_euler.z=-math.radians(5)*35/24
# Distinct matte stones, within the inherited geometry-aware route.
ns={};path=B.parent/'Interaction-Proof_v006/Scripts/build.py';src=path.read_text();start=src.index('def linear(');end=src.index("fx=bpy.data.collections.new")
ns.update(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=-math.radians(5),routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text()));exec(src[start:end],ns)
for name,color in [('Body',(.065,.052,.038)),('Light',(.25,.20,.13)),('Dark',(.025,.020,.016))]:
 m=bpy.data.materials.new('S05_v007_Cutting'+name);m.diffuse_color=(*color,1);m.use_nodes=True;p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=.94
rocksource=bpy.data.objects['S05_v005_Rock_54'];rocks=[]
for i,z in enumerate([.015,.205,.445]):
 rock=rocksource.copy();rock.data=rocksource.data.copy();rock.animation_data_clear();rock.parent=None;rock.name=f'S05_v007_SuspendedCutting_{i:02}';fx.objects.link(rock);rock.hide_render=False;rock.hide_viewport=False
 scale=[.0065,.0075,.006][i]/max(v.co.length for v in rock.data.vertices)
 for v in rock.data.vertices:v.co*=scale
 rock.data.materials.clear()
 for k in ['Body','Light','Dark']:rock.data.materials.append(bpy.data.materials['S05_v007_Cutting'+k])
 p,u,v,rr,rt=ns['frame_at'](z,35/24);rock.location=p;rock.scale=(1,1,1);rock.rotation_euler=(i*.7,.4+i,.3);rocks.append({'name':rock.name,'location':list(p),'support_radius_m':[.0065,.0075,.006][i]})
s.frame_set(36);bpy.context.view_layer.update();s.render.filepath=str(B/'Previews/fluid-treatment_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
record={'stage':'Static representation test; no motion built yet','seconds':dt,'grid':[NZ,NA],'inner_margin_m':.001,'outer_margin_m':.001,'z_range':[Z0,Z1],'camera_preserved':True,'rocks':rocks}
(B/'Records/still-build.json').write_text(json.dumps(record,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT));result=record
