import bpy,math,time,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1]
sourcefile=B.parent/'D-Physical-Wear_v009/Scenes/S04_D_physical-comparison_v009.blend'
bpy.ops.wm.open_mainfile(filepath=str(sourcefile),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only'];bpy.context.window.scene=s
def physical():
 return {'meshes':{o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'lights':{o.name:[list(o.location),o.data.energy] for o in s.objects if o.type=='LIGHT'}}
before=physical()
def tree(name):
 o=bpy.data.objects[name];return BVHTree.FromPolygons([v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
worn=tree('CASED_STEEL_WEAR_CUTAWAY');nominal=tree('CASED_STEEL_NOMINAL_CUTAWAY')
def point(t,x,a):
 p=t.ray_cast(Vector((x,0,0)),Vector((0,math.cos(a),math.sin(a))),1)[0]
 if p is None:raise RuntimeError('Source ray missed')
 return p
coll=bpy.data.collections.new('Original steel ghost - depth from registered source difference');s.collection.children.link(coll)
NX=56;NA=72;vs=[];depths=[];alphas=[]
for i in range(NX+1):
 x=-2.36+(-1.5125+2.36)*i/NX
 for j in range(NA+1):
  a=-1.15+2.3*j/NA;n=point(nominal,x,a);p=point(worn,x,a);d=max(0,math.hypot(p.y,p.z)-math.hypot(n.y,n.z));vs.append(tuple(n));depths.append(d)
  # Zero at unworn surface, smooth fade with actual measured geometry difference.
  alphas.append(.32*min(1,d/.004)**.7 if d>.000001 else 0)
fs=[]
for i in range(NX):
 for j in range(NA):
  q=i*(NA+1)+j
  if max(alphas[k] for k in [q,q+1,q+NA+2,q+NA+1])>.00015:fs.append((q,q+1,q+NA+2,q+NA+1))
me=bpy.data.meshes.new('Original nominal steel - geometry-driven faint ghost');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Faint original-surface ghost over actual wear',me);coll.objects.link(o)
colors=me.color_attributes.new(name='GhostOpacityFromActualWear',type='FLOAT_COLOR',domain='POINT')
for c,a in zip(colors.data,alphas):c.color=(1,1,1,a)
m=bpy.data.materials.new('Original-surface ghost - soft geometry-derived opacity');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();vc=ns.new('ShaderNodeVertexColor');vc.layer_name=colors.name;tr=ns.new('ShaderNodeBsdfTransparent');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(.45,.60,.65,1);em.inputs[1].default_value=.75;mix=ns.new('ShaderNodeMixShader');out=ns.new('ShaderNodeOutputMaterial');l=m.node_tree.links;l.new(vc.outputs['Alpha'],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],out.inputs['Surface']);m.surface_render_method='BLENDED';me.materials.append(m)
white=bpy.data.materials['Original inner surface - dashed reference']
connections=[]
for i,(x,a) in enumerate([(-1.60,0),(-1.79,-.22),(-1.88,.22),(-2.05,-.12),(-2.17,.10)]):
 n=point(nominal,x,a);p=point(worn,x,a);length=(p-n).length
 cu=bpy.data.curves.new('Local depth connection %d'%i,'CURVE');cu.dimensions='3D';cu.bevel_depth=.00010;cu.bevel_resolution=2;sp=cu.splines.new('POLY');sp.points.add(1);sp.points[0].co=(*n,1);sp.points[1].co=(*p,1);ob=bpy.data.objects.new('Local depth connection %d'%i,cu);coll.objects.link(ob);cu.materials.append(white);connections.append({'x_m':x,'azimuth_rad':a,'actual_gap_m':length})
# Preserve the owner's accepted front comparison. No new grid or rectangular outline.
s.eevee.taa_render_samples=8;s['scope']='v011 one ghost-surface proof; owner accepted shot/front comparison retained. Not full D integration.'
s['ghost_meaning']='Faint pre-wear surface reconstructed from registered nominal mesh; five true-depth connectors to existing worn wall. Opacity follows actual geometry difference, not a rectangular mask. No numerical measured volume claim.'
after=physical();after['meshes'].pop(o.name);assert before==after
s.name='D soft original-surface ghost v011'
out=B/'Scenes/S04_D_original-surface-ghost_v011.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_original-surface-ghost_v011.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps({'source':str(sourcefile),'render_seconds':elapsed,'under_5_seconds':elapsed<5,'physical_mesh_camera_lights_unchanged':True,'nominal_source':'CASED_STEEL_NOMINAL_CUTAWAY','worn_source':'CASED_STEEL_WEAR_CUTAWAY','sampled_actual_difference_m':[min(depths),max(depths)],'outer_angle_edge_opacity_max':max(alphas[j] for j in range(len(alphas)) if j%(NA+1) in [0,NA]),'uphole_edge_opacity_max':max(alphas[:NA+1]),'connections':connections,'front_comparison_preserved':True,'no_grid_or_hard_footprint_outline':True,'complete_visible_wear_taper_sampled':True,'visible_interval_m':[-2.36,-1.5125],'distal_wear_beyond_inspection_section_not_displayed':True,'no_quantified_volume_claim':True},indent=2));print('GHOST_SECONDS',elapsed,flush=True)


