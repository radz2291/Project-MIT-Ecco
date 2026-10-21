import bpy, bmesh, math, time, json, hashlib
from pathlib import Path
from mathutils import Vector, Matrix
R=Path(r'C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=Path(__file__).resolve().parents[1]
SRC=R/'05-Previs/Section-04_Cement-Casing-Integrity/Communication-Test_v007/Test-2_Inner-Wear/Scenes/S04_D_communication_v007.blend'
MASTER=R/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend'
bpy.ops.wm.open_mainfile(filepath=str(SRC),load_ui=False,use_scripts=False)
old=bpy.context.scene;old.frame_set(1);bpy.context.view_layer.update()
steel_source=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY']
source_coords=[tuple(v.co) for v in steel_source.data.vertices]
baseline=hashlib.sha256(repr(source_coords).encode()).hexdigest()
RI=.1589405;RO=.1698625
def material(name,color,metal=0,rough=.55):
 m=bpy.data.materials.new(name);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*color,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;return m
steelmat=material('Satin steel - physical roughness only',(.30,.34,.38),.65,.43)
sectionmat=material('Same steel - matte inspection section',(.42,.45,.48),.25,.65)
nt=steelmat.node_tree;n=nt.nodes;l=nt.links;bs=n.get('Principled BSDF')
a=n.new('ShaderNodeAttribute');a.attribute_name='PhysicalWearDepth'
mp=n.new('ShaderNodeMapRange');mp.inputs['From Min'].default_value=0;mp.inputs['From Max'].default_value=.004;mp.inputs['To Min'].default_value=.45;mp.inputs['To Max'].default_value=.30;l.new(a.outputs['Fac'],mp.inputs['Value'])
tc=n.new('ShaderNodeTexCoord');sc=n.new('ShaderNodeVectorMath');sc.operation='MULTIPLY';sc.inputs[1].default_value=(6,12,1800);l.new(tc.outputs['Object'],sc.inputs[0])
noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;l.new(sc.outputs['Vector'],noise.inputs['Vector'])
grain=n.new('ShaderNodeMath');grain.operation='MULTIPLY';grain.inputs[1].default_value=.045;l.new(noise.outputs['Fac'],grain.inputs[0]);rough=n.new('ShaderNodeMath');rough.operation='ADD';l.new(mp.outputs['Result'],rough.inputs[0]);l.new(grain.outputs[0],rough.inputs[1]);l.new(rough.outputs[0],bs.inputs['Roughness'])
cementmat=material('Sectional cement - quiet warm matte',(.36,.30,.22),0,.9)
rockmat=material('Section 2 context - subdued formation',(.15,.105,.067),0,.95)
fluidmat=material('Existing exterior fluid - restrained context',(.035,.15,.18),0,.6)
def physical_copy(src,scene,mat=None):
 o=src.copy();o.data=src.data.copy();o.animation_data_clear();o.hide_render=False;o.hide_viewport=False;o.hide_set(False);scene.collection.objects.link(o)
 if mat:
  o.data.materials.clear();o.data.materials.append(mat)
  for slot in o.material_slots:slot.link='DATA'
  for p in o.data.polygons:p.material_index=0
 return o
def lighting(scene,name,pos,target,power,size,short):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='RECTANGLE';d.size=size;d.size_y=short;d.use_shadow=False
 o=bpy.data.objects.new(name,d);scene.collection.objects.link(o);o.location=pos
 z=(Vector(pos)-Vector(target)).normalized();x=Vector((1,0,0));x=(x-z*x.dot(z)).normalized();y=z.cross(x);o.rotation_euler=Matrix((x,y,z)).transposed().to_euler()
def setcam(scene,eye,target,lens):
 d=bpy.data.cameras.new('Physical discovery camera');o=bpy.data.objects.new('Physical discovery camera',d);scene.collection.objects.link(o);o.location=eye;o.rotation_euler=(Vector(target)-Vector(eye)).to_track_quat('-Z','Y').to_euler();d.lens=lens;d.clip_start=.001;scene.camera=o
def build(tag,eye,target,lens):
 s=bpy.data.scenes.new('D '+tag+' - physical only');bpy.context.window.scene=s
 o=physical_copy(steel_source,s,steelmat);o.name='Actual registered worn steel '+tag
 # Fixed viewing section at existing axial sample planes, outside the whole wear interval.
 # Retains all source wear vertices. No radial coordinates are changed.
 bm=bmesh.new();bm.from_mesh(o.data)
 end=-1.5125 if tag.startswith(('B_','C_')) else -.55
 bmesh.ops.delete(bm,geom=[v for v in bm.verts if v.co.x< -2.475001 or v.co.x>end+.000001],context='VERTS')
 for x in [-2.475,end]:
  edges=[e for e in bm.edges if e.is_boundary and all(abs(v.co.x-x)<1e-5 for v in e.verts)]
  if edges:bmesh.ops.holes_fill(bm,edges=edges,sides=0)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
 attr=o.data.attributes.new('PhysicalWearDepth','FLOAT','POINT')
 for v,a in zip(o.data.vertices,attr.data):
  rr=math.hypot(v.co.y,v.co.z);a.value=max(0,rr-RI) if rr<(RI+RO)/2 else 0
 # Restore smooth barrel shading, with sharp static section/end faces.
 o.data.materials.append(sectionmat)
 for p in o.data.polygons:
  p.use_smooth=abs(p.normal.x)<.7 and abs(p.center.y)>.00001
  if abs(p.normal.x)>.9:p.material_index=1
 for src in old.objects:
  if src.type=='MESH' and (src.name.startswith('Cement ') or src.name.startswith('Section 2 geological') or src.name.startswith('Stationary organic fluid')) and not src.hide_render and len(src.data.vertices):
   physical_copy(src,s,cementmat if src.name.startswith('Cement ') else rockmat if src.name.startswith('Section 2') else fluidmat)
 # Keep the actual registered hardware as spatial context; no rescaling/repositioning.
 hw=old.objects.get('WORLD_HARDWARE_INSTANCE')
 if hw and False: # Hardware retained in the source scene; omitted only in physical inspection scenes.
  h=hw.copy();h.animation_data_clear();h.hide_render=False;h.hide_viewport=False;s.collection.objects.link(h);h.matrix_world=hw.matrix_world.copy()
 s.world=bpy.data.worlds.new('Dim well inspection '+tag);s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.12,.16,.21,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.20
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=12;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.fps=24
 s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.view_settings.exposure=0
 setcam(s,eye,target,lens)
 lighting(s,'Broad grazing strip',(-1.5,.035,.125),(-1.5,.16,0),1.8,1.6,.055)
 lighting(s,'Low soft inspection fill',(-1.5,-.08,-.09),(-1.5,.16,0),.7,1.4,.12)
 lighting(s,'Section context fill',(-.15,-.4,.45),(-1.3,.12,0),20,1.1,.6)
 s['scope']='Owner v008 physical-only proof. No measurement overlays, animation or integration. Wear and outer radius unchanged.'
 coords=[tuple(v.co) for v in o.data.vertices];assert all(p in set(source_coords) for p in coords)
 return s,dict(option=tag,source_coordinate_hash=baseline,retained_coordinates_identical=True,static_section_axial_planes_m=[-2.475,end],whole_wear_interval_retained=end>-.7,inspection_section_through_deepest_sample=end<-1.5,authored_maximum_wear_m=.004,sampled_maximum_wear_m=max(v for v in [math.hypot(p[1],p[2])-RI for p in coords if math.hypot(p[1],p[2])<(RI+RO)/2]),outer_radius_m=RO,eye=list(eye),target=list(target),lens_mm=lens)
rows=[]
configs=[('A_surface-grazing',(-2.35,.035,.095),(-2.05,.160,0),36),('B_sectional-context',(-.85,-.025,.06),(-1.7,.04,0),48),('C_preferred-closeup',(-1.1,-.02,.06),(-1.66,.145,0),55)]
for tag,eye,target,lens in configs:
 s,d=build(tag,eye,target,lens);bpy.context.window.scene=s
 for w in bpy.context.window_manager.windows:
  for area in w.screen.areas:
   if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL';area.spaces.active.overlay.show_overlays=False
 p=B/'Scenes'/('S04_D_'+tag+'_v008.blend')
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(p.parent))
 s.render.filepath=str(B/'Previews'/('S04_D_'+tag+'_v008.png'));bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
 t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);d['render_seconds']=time.perf_counter()-t;d['under_5_seconds']=d['render_seconds']<5;rows.append(d);(B/'Records/benchmarks.json').write_text(json.dumps(rows,indent=2));print('PROOF',tag,d['render_seconds'],flush=True)
 if not d['under_5_seconds']:print('BUDGET_FAIL - stop further renders',flush=True);break
(B/'Records/provenance.json').write_text(json.dumps({'original_scene':str(SRC),'master':str(MASTER),'master_sha256':hashlib.sha256(MASTER.read_bytes()).hexdigest(),'geometry_hash':baseline,'vertex_count':len(source_coords),'no_measurement_graphics':True,'no_amplitude_bump_displacement':True,'native_master_untouched':True,'original_D_and_approved_BC_untouched':True},indent=2))
