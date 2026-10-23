import bpy,math,json,time,bmesh,numpy as np
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff)
def surface(z,a):
 u=Vector((math.cos(a),math.sin(a),0));h=tree.ray_cast(Vector((0,0,z))+u*.18,-u,.18)[0]
 return math.hypot(h.x,h.y) if h else .105
NZ=301;NA=240;zs=np.linspace(-.45,1.05,NZ);angles=np.arange(NA)*math.tau/NA
raw=np.array([[surface(float(z),float(a)) for a in angles] for z in zs]);robust=raw.copy()
for dz in [-1,0,1]:
 for da in [-1,0,1]:robust=np.maximum(robust,np.roll(raw[np.clip(np.arange(NZ)+dz,0,NZ-1)],da,axis=1))
inner=robust+.001;outer=.154575;assert inner.max()<outer
verts=[]
for layer in [0,1]:
 for j,z in enumerate(zs):
  for i,a in enumerate(angles):
   r=outer if layer else inner[j,i];verts.append((r*math.cos(a),r*math.sin(a),z))
N=NZ*NA;faces=[];mats=[]
for layer in [0,1]:
 for j in range(NZ-1):
  for i in range(NA):
   a=layer*N+j*NA+i;b=layer*N+j*NA+(i+1)%NA;c=b+NA;d=a+NA;faces.append((a,b,c,d) if layer else (d,c,b,a));mats.append(0 if layer else 1)
for j in [0,NZ-1]:
 for i in range(NA):
  a=j*NA+i;b=j*NA+(i+1)%NA;faces.append((a,b,b+N,a+N));mats.append(2)
me=bpy.data.meshes.new('S05_v007_ContinuousAnnularDomain');me.from_pydata(verts,[],faces)
for name in ['S05_v007_SectionedFluid','S05_v007_InnerFluidInterface','S05_v007_FluidSectionFace']:me.materials.append(bpy.data.materials[name])
for p,mi in zip(me.polygons,mats):p.material_index=mi;p.use_smooth=mi!=2
bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
o=bpy.data.objects['S05_v007_AnnularFluidDomain'];o.data=me
for name,alpha in [('S05_v007_SectionedFluid',.025),('S05_v007_FluidSectionFace',0)]:
 m=bpy.data.materials[name];next(n for n in m.node_tree.nodes if n.type=='MIX_SHADER').inputs[0].default_value=alpha
m=bpy.data.materials['S05_v007_SectionedFluid'];next(n for n in m.node_tree.nodes if n.type=='PRINCIPLED_VOLUME').inputs['Density'].default_value=6
for name,color in [('Body',(.16,.145,.12)),('Light',(.40,.35,.27)),('Dark',(.040,.035,.028))]:
 m=bpy.data.materials['S05_v007_Cutting'+name];p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1)
for i in range(3):
 rock=bpy.data.objects[f'S05_v007_SuspendedCutting_{i:02}'];fac=[.0075,.008,.007][i]/max(v.co.length for v in rock.data.vertices)
 for v in rock.data.vertices:v.co*=fac
s.eevee.taa_render_samples=48;s.frame_set(36);s.render.filepath=str(B/'Previews/fluid-treatment_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
result={'seconds':dt,'grid':[NZ,NA],'z_range':[-.45,1.05],'surface_mix':.025,'density':6,'render_samples':48,'cutting_support_diameters_mm':[15,16,14]}
(B/'Records/still-refinement.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
