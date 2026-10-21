import bpy,json,time,hashlib,bmesh,math
from pathlib import Path
B=Path(__file__).resolve().parents[1];P=B.parent
S3=P.parent/'Section-03_The-Earth-Revealed/v036/Scenes/S03_second-last-nominal-label_v036.blend'
ANGLE=P/'D-Physical-Wear_v017/Scenes/S04_D_cool-wear-depth_v017.blend'
SRC=P/'Cinematic-Previs_v022/Scenes/S04_complete_v022.blend'
def digest(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
bpy.ops.wm.open_mainfile(filepath=str(S3),load_ui=False,use_scripts=False);s=bpy.context.scene
ref={'file':str(S3),'sha256':hashlib.sha256(S3.read_bytes()).hexdigest(),'view_transform':s.view_settings.view_transform,'look':s.view_settings.look,'world_color':list(s.world.color) if s.world else None,'world_backgrounds':[{'color':list(n.inputs['Color'].default_value),'strength':n.inputs['Strength'].default_value} for n in s.world.node_tree.nodes if n.type=='BACKGROUND'] if s.world and s.world.use_nodes else []}
bpy.ops.wm.open_mainfile(filepath=str(ANGLE),load_ui=False,use_scripts=False);s=bpy.context.scene;c=s.camera;matrix=c.matrix_world.copy();lens=c.data.lens;shift=(c.data.shift_x,c.data.shift_y)
lights=[{'name':o.name,'type':o.data.type,'color':list(o.data.color),'energy':o.data.energy,'matrix':[list(r) for r in o.matrix_world],'size':getattr(o.data,'size',1),'size_y':getattr(o.data,'size_y',1),'shape':getattr(o.data,'shape','DISK')} for o in s.objects if o.type=='LIGHT' and not o.hide_render]
bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 D scientific stage stills v026';s.frame_set(400);bpy.context.view_layer.update();before=digest(s)
steel=bpy.data.objects['STEEL - capped true source section'];depth=[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data]
for o in s.objects:
 if o.type=='MESH' and o!=steel or o.type=='CURVE' and not o.name.startswith('Station '):
  o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
 if o.type=='LIGHT':o.hide_render=True;o.hide_viewport=True
for r in lights:
 d=bpy.data.lights.new('Stage - '+r['name'],r['type']);d.color=r['color'];d.energy=r['energy'];d.use_shadow=False
 if r['type']=='AREA':d.shape=r['shape'];d.size=r['size'];d.size_y=r['size_y']
 o=bpy.data.objects.new(d.name,d);s.collection.objects.link(o)
 from mathutils import Matrix
 o.matrix_world=Matrix(r['matrix'])
s.world=bpy.data.worlds.new('S03-related quiet blue-grey stage');s.world.use_nodes=True;bg=s.world.node_tree.nodes.get('Background');bg.inputs[0].default_value=(.018,.035,.052,1);bg.inputs[1].default_value=.45
s.view_settings.view_transform=ref['view_transform']
try:s.view_settings.look=ref['look']
except:pass
c=s.camera;c.animation_data_clear();c.data=c.data.copy();c.data.animation_data_clear();c.matrix_world=matrix;c.data.lens=lens;c.data.shift_x=shift[0];c.data.shift_y=shift[1]
housing=bpy.data.objects['ECCO unchanged source housing - D technical transparency'];housing.data=housing.data.copy()
toolmeshes=[];memo={};wireobjects=[];wire_edges=0
def local_display(col):
 if col in memo:return memo[col]
 new=bpy.data.collections.new(col.name+' stage display');memo[col]=new
 for ob in col.objects:
  if ob.type=='MESH':
   cp=ob.copy();cp.data=ob.data.copy();new.objects.link(cp);toolmeshes.append(cp)
   bm=bmesh.new();bm.from_mesh(cp.data);bm.normal_update();edges=[e for e in bm.edges if e.is_boundary or e.is_manifold and e.calc_face_angle(0)>math.radians(40)]
   if edges:
    cu=bpy.data.curves.new(cp.name+' design edges','CURVE');cu.dimensions='3D';sc=max(1e-6,cp.matrix_world.to_scale().length/math.sqrt(3));cu.bevel_depth=.00010/sc;cu.bevel_resolution=0;cu.resolution_u=1
    for e in edges:
     sp=cu.splines.new('POLY');sp.points.add(1)
     for p,v in zip(sp.points,e.verts):p.co=(*v.co,1)
    wo=bpy.data.objects.new(cu.name,cu);new.objects.link(wo);wo.parent=cp;wireobjects.append(wo)
   bm.free()
  elif ob.instance_collection:
   cp=ob.copy();cp.instance_collection=local_display(ob.instance_collection);new.objects.link(cp)
  else:new.objects.link(ob)
 for ch in col.children:new.children.link(local_display(ch))
 return new
inst=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];inst.instance_collection=local_display(inst.instance_collection)
def material(name,body,edge):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.surface_render_method='BLENDED';m.use_transparency_overlap=False;n=m.node_tree;n.nodes.clear();out=n.nodes.new('ShaderNodeOutputMaterial');tr=n.nodes.new('ShaderNodeBsdfTransparent');bs=n.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Base Color'].default_value=(.10,.22,.29,1);bs.inputs['Roughness'].default_value=.75;bs.inputs['Metallic'].default_value=.1
 lw=n.nodes.new('ShaderNodeLayerWeight');power=n.nodes.new('ShaderNodeMath');power.operation='POWER';power.inputs[1].default_value=2;n.links.new(lw.outputs['Fresnel'],power.inputs[0]);mul=n.nodes.new('ShaderNodeMath');mul.operation='MULTIPLY';mul.inputs[1].default_value=edge;n.links.new(power.outputs[0],mul.inputs[0]);add=n.nodes.new('ShaderNodeMath');add.operation='ADD';add.inputs[1].default_value=body;add.use_clamp=True;n.links.new(mul.outputs[0],add.inputs[0]);mix=n.nodes.new('ShaderNodeMixShader');n.links.new(add.outputs[0],mix.inputs[0]);n.links.new(tr.outputs[0],mix.inputs[1]);n.links.new(bs.outputs[0],mix.inputs[2]);n.links.new(mix.outputs[0],out.inputs['Surface'])
 return m
wiremat=bpy.data.materials.new('Desaturated cyan CAD design-edge display');wiremat.use_nodes=True;wiremat.surface_render_method='BLENDED';wn=wiremat.node_tree;wn.nodes.clear();wout=wn.nodes.new('ShaderNodeOutputMaterial');wtr=wn.nodes.new('ShaderNodeBsdfTransparent');wem=wn.nodes.new('ShaderNodeEmission');wem.inputs[0].default_value=(.10,.32,.40,1);wem.inputs[1].default_value=.6;wmix=wn.nodes.new('ShaderNodeMixShader');wn.links.new(wtr.outputs[0],wmix.inputs[1]);wn.links.new(wem.outputs[0],wmix.inputs[2]);wn.links.new(wmix.outputs[0],wout.inputs['Surface'])
for ob in wireobjects:ob.data.materials.append(wiremat)
rows=[];s.eevee.taa_render_samples=8
for tag,title,body,edge in [('A','Soft transparent tool',.055,0),('B','Contour wireframe look',0,.8),('C','Ghost plus contour edges',.025,.55)]:
 m=material('D '+title,body,0);wmix.inputs[0].default_value=0 if tag=='A' else (1 if tag=='B' else .5)
 for ob in toolmeshes:
  if len(ob.data.materials)==0:ob.data.materials.append(m)
  for i in range(len(ob.data.materials)):ob.data.materials[i]=m
 s['scope']='Stage4 look proofs only. Exact v017 review angle; focused stage borrowing S03 white/cyan/blue-grey vocabulary. Tool transparency/contour shader is explanatory, not deformation.'
 s.render.filepath=str(B/'Previews'/f'S04_D_{tag}_raw_v026.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
 if dt>=5:raise RuntimeError('Frame cap exceeded')
 assert before==digest(s) and depth==[v.value for v in steel.data.attributes['ComputedWearDepth_m'].data]
 out=B/'Scenes'/f'S04_D_{tag}_v026.blend'
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
 rows.append({'id':tag,'title':title,'body_opacity':body,'edge_factor':edge,'seconds':dt,'native':str(out)})
(B/'Records/proof.json').write_text(json.dumps({'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'angle_source':str(ANGLE),'angle_source_sha256':hashlib.sha256(ANGLE.read_bytes()).hexdigest(),'camera_matrix':[list(r) for r in matrix],'lens_mm':lens,'camera_shift':shift,'section3_inspection':ref,'physical_meshes_unchanged':True,'computed_values_unchanged':True,'max_authored_wear_mm':1000*max(depth),'hidden_surroundings':'Soil, cement, channel and fluid context presentation only; fixed steel geometry retained.','wireframe_method':'View-dependent surface contour shading on real housing, not a dense triangulation mesh.','movie_integration':False,'options':rows},indent=2))
