"""T44 owner-requested bounded geometry/shading/static-fluid correction.

Previous candidates are immutable. Run in isolated background Blender.
"""
import bpy, math, sys, json, hashlib, time, runpy
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4];ASSET=ROOT/'04-Production/Shared/Assets'
TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v006'
E=REV/'Evidence';SCENES=REV/'Scenes';P=TASK/'Previews/Revision_v006'
for p in [E,SCENES,P]:p.mkdir(parents=True,exist_ok=True)
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['inspect']
sys.argv=['script','--','noop'];B=runpy.run_path(str(HERE/'build_world_t44.py'))
F=runpy.run_path(str(HERE/'build_formation_revision_v005.py'))
R=.155575
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
def normals(o):
 # Analytic loop normals keep cap/cut-edge normals separate without moving vertices.
 m=o.data;m.update();ns=[];cyl=0
 for p in m.polygons:
  c=p.center;r=math.hypot(c.y,c.z);dot=(p.normal.y*c.y+p.normal.z*c.z)/r if r else 0
  curved=abs(dot)>.8 and abs(p.normal.x)<.1
  p.use_smooth=curved
  if curved:cyl+=1
  for vi in p.vertices:
   v=m.vertices[vi].co;rr=math.hypot(v.y,v.z)
   ns.append((0,math.copysign(1,dot)*v.y/rr,math.copysign(1,dot)*v.z/rr) if curved else tuple(p.normal))
 m.normals_split_custom_set(ns);return cyl
def recmesh(o):
 m=o.data
 return dict(vertices=len(m.vertices),polygons=len(m.polygons),coordinates=hashlib.sha256(b''.join(__import__('struct').pack('3f',*v.co) for v in m.vertices)).hexdigest(),faces=hashlib.sha256(str([tuple(p.vertices) for p in m.polygons]).encode()).hexdigest(),smooth=sum(p.use_smooth for p in m.polygons),custom_normals=m.has_custom_normals)
def cylinder(name,center,axis,r,depth,col,material):
 bpy.ops.mesh.primitive_cylinder_add(vertices=32,radius=r,depth=depth,location=center)
 o=bpy.context.object;o.name=name;o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
 for c in list(o.users_collection):c.objects.unlink(o)
 col.objects.link(o);B['assign'](o,material)
 for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
 be=o.modifiers.new('Small manufactured edge','BEVEL');be.width=.00045;be.segments=2
 return o
def hardware():
 src=ASSET/'BHA/BHA_film_v002.blend';openfile(src);c=bpy.data.collections['WORLD_HARDWARE']
 for o in list(c.objects):
  if o.name.startswith(('GENERIC_BIT','GENERIC_CUTTER')):bpy.data.objects.remove(o,do_unlink=True)
 steel=B['mat']('WORLD_PDC_Steel',(.24,.29,.32),.78,.40)
 web=B['mat']('WORLD_PDC_Web',(.115,.145,.16),.73,.43)
 carbide=B['mat']('WORLD_PDC_Carbide',(.20,.22,.23),.8,.31)
 diamond=B['mat']('WORLD_PDC_DiamondTable',(.018,.028,.031),.6,.23)
 throat=B['mat']('WORLD_PDC_NozzleThroat',(.008,.012,.014),.1,.65)
 # Smaller central web leaves genuinely deep open junk courses between integral blades.
 body=B['lathe']('PDC_WEB_AND_SHANK',[(2.9,.03571875),(2.9,.104775),(2.925,.104775),(2.93,.099),(2.975,.099),(2.99,.107),(3.025,.112),(3.09,.108),(3.15,.092),(3.185,.074),(3.192,.012),(3.17,.0)],c,web,n=96)
 body['reference']='SLB The Defining Series: Bits, 2016, Figure2; six-blade PDC morphology, not a manufacturer replica or MIT bit selection'
 body['simplifications']='Authored crown/profile/cutter count, hidden unthreaded pin, no internal hydraulic network or validated bit-to-sub fit.'
 body['gauge_diameter_m']=2*R
 # Shoulder joint and wrench flats remain inside the sourced collar envelope.
 ring=B['lathe']('PDC_ADAPTER_SHOULDER',[(2.90,.099),(2.9,.104775),(2.914,.104775),(2.918,.099)],c,steel,n=96)
 stations=[(.012,3.195),(.025,3.202),(.042,3.211),(.062,3.22),(.083,3.225),(.103,3.219),(.121,3.202),(.137,3.178),(.148,3.154),(R,3.13)]
 for k in range(6):
  vs=[];fs=[]
  for r,x in stations:
   a=k*math.tau/6+.44*(r/R)**1.15
   half=min(.35,(.014+.018*r/R)/(2*r))
   back=3.027-.03*(r/R)**2
   for xx,aa in [(back,a-half),(x,a-half),(x,a+half),(back,a+half)]:vs.append((xx,r*math.cos(aa),r*math.sin(aa)))
  for i in range(len(stations)-1):
   for j in range(4):q=i*4+j;t=i*4+(j+1)%4;fs.append((q,t,t+4,q+4))
  fs.extend([(0,3,2,1),tuple(range(len(vs)-4,len(vs)))])
  o=B['mesh']('PDC_INTEGRAL_BLADE_%02d'%(k+1),vs,fs,c,steel)
  # Recalculate outside normals and keep geometric crown corners readable.
  import bmesh
  bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free()
  be=o.modifiers.new('Blade edge easing','BEVEL');be.width=.0008;be.segments=2
  for j,(r,x) in enumerate(stations[1:-1]):
   # Dark compact faces face the leading side; the carbide substrate is visible.
   a=k*math.tau/6+.44*(r/R)**1.15-min(.35,(.014+.018*r/R)/(2*r))
   axis=Vector((.62,math.sin(a),-math.cos(a))).normalized();center=Vector((x-.004,r*math.cos(a),r*math.sin(a)))
   cylinder('PDC_COMPACT_%02d_%02d'%(k+1,j+1),center,axis,.007,.009,c,carbide)
   cylinder('PDC_TABLE_%02d_%02d'%(k+1,j+1),center+axis*.0047,axis,.0068,.0012,c,diamond)
  # Gauge hardfacing pads on the blade flank; all surfaces stay within gauge.
  a=k*math.tau/6+.44;pad=B['lathe']('PDC_GAUGE_PAD_%02d'%(k+1),[(3.015,R-.001),(3.12,R-.001)],c,carbide,n=8,sector=(a-.072,a+.072))
  # Six recessed socket/nozzle mouths in the exposed fluid-course floor.
  a=k*math.tau/6+.67;rr=.074;center=Vector((3.173,rr*math.cos(a),rr*math.sin(a)))
  nozzle=B['lathe']('PDC_NOZZLE_%02d'%(k+1),[(-.005,.006),(.002,.006),(.003,.009),(-.004,.010),(-.005,.006)],c,carbide,n=32)
  # The helper lathe is alongX; place it directly on the shallow cone web.
  nozzle.location=center
  cylinder('PDC_NOZZLE_BORE_%02d'%(k+1),center+Vector((-.004,0,0)),(1,0,0),.0058,.0008,c,throat)
 c['revision']='v003; six-blade steel-body PDC visual study, genuine junk spaces, 48 two-part cutters, six recessed nozzle mouths; 12.25in gauge retained'
 c['technical_status']='Provisional visual assembly only; no selected client bit, thread/connection fit or hydraulic qualification.'
 out=ASSET/'BHA/BHA_film_v003.blend';B['save'](out)
 dump(E/'hardware-build_v006.json',dict(source=rel(src),source_sha256=sha(src),output=rel(out),sha256=sha(out),reference='https://www.slb.com/resource-library/oilfield-review/defining-series/defining-bits',figure='Figure2',gauge_diameter_m=2*R,axial_envelope_m=[2.9,3.24],blades=6,cutters=48,nozzles=6,exact_client_bit=False,thread_fit_verified=False))
 print('CLEANUP_HARDWARE_PASS',flush=True)
def environment():
 src=ASSET/'WellAssembly/World_environment_v005.blend';openfile(src);checks=[]
 for name in ['CASING_CUTAWAY','CASING_FULL']:
  o=bpy.data.objects[name];before=recmesh(o);n=normals(o);after=recmesh(o)
  assert before['coordinates']==after['coordinates'] and before['faces']==after['faces']
  checks.append(dict(object=name,before=before,after=after,cylindrical_faces=n,cause='Flat face shading on source cylindrical tessellation; radial winding checked correct. No modifier or texture-bump cause.',fix='Analytic radial corner normals on cylindrical surfaces only; flat rim/cut faces retained; no coordinate/topology edits.'))
 steel=bpy.data.materials['WORLD_CasingSteel'];bs=next(n for n in steel.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Roughness'].default_value=.43
 # Replace the flat rectangular fluid section with a bounded curved optical rear skin.
 mud=bpy.data.collections['WORLD_MUD']
 for o in list(mud.objects):bpy.data.objects.remove(o,do_unlink=True)
 fm=B['mat']('WORLD_StaticFluid_v006',(.045,.066,.058),0,.17)
 ns=fm.node_tree.nodes;lk=fm.node_tree.links;bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED')
 bs.inputs['IOR'].default_value=1.4;bs.inputs['Coat Weight'].default_value=.35;bs.inputs['Coat Roughness'].default_value=.11
 tc=ns.new('ShaderNodeTexCoord');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=32;noise.inputs['Detail'].default_value=2
 lk.new(tc.outputs['Object'],noise.inputs['Vector']);bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.15;bump.inputs['Distance'].default_value=.00018
 lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],bs.inputs['Normal'])
 layer=ns.new('ShaderNodeLayerWeight');layer.inputs['Blend'].default_value=.3
 ramp=ns.new('ShaderNodeMapRange');ramp.inputs['From Min'].default_value=0;ramp.inputs['From Max'].default_value=1;ramp.inputs['To Min'].default_value=.12;ramp.inputs['To Max'].default_value=.30
 lk.new(layer.outputs['Facing'],ramp.inputs['Value']);lk.new(ramp.outputs['Result'],bs.inputs['Alpha']);fm.surface_render_method='DITHERED'
 vs=[];fs=[];nx=256;na=96
 for i in range(nx+1):
  x=-5.5+11.5*i/nx
  for j in range(na+1):
   a=-math.pi/2+.012+((math.pi-.024)*j/na)
   rr=(.1589405 if x<0 else F['radius'](x,a,1))-.00045-.0001*(1+math.sin(31*x+5*a))
   vs.append((x,rr*math.cos(a),rr*math.sin(a)))
 for i in range(nx):
  for j in range(na):q=i*(na+1)+j;fs.append((q,q+1,q+na+2,q+na+1))
 o=B['mesh']('MUD_CURVED_REAR_OPTICAL_SKIN',vs,fs,mud,fm)
 for poly in o.data.polygons:poly.use_smooth=True
 o['status']='Static curved rear-half fluid optical surface, within registered bore and outside max12in ECCO envelope. Gentle thickness-opacity/meniscus cue; not a calibrated filled volume, air surface, CFD or moving flow.'
 o['supported_variant']='Irregular approval/reuse context; other variant-specific fluid skins require regeneration before release.'
 root=bpy.data.collections['WORLD_ENV'];root['revision']='v006; accepted formation mass unchanged; casing normals/static fluid look correction'
 out=ASSET/'WellAssembly/World_environment_v006.blend';B['save'](out)
 dump(E/'environment-build_v006.json',dict(source=rel(src),source_sha256=sha(src),output=rel(out),sha256=sha(out),steel_diagnosis=checks,fluid='Curved rear bore optical skin replaces flat cut-plane band; no physical simulation.',formation_geometry_changed=False))
 print('CLEANUP_ENVIRONMENT_PASS',flush=True)
def relink():
 targets={'World_environment_v005.blend':ASSET/'WellAssembly/World_environment_v006.blend','BHA_film_v002.blend':ASSET/'BHA/BHA_film_v003.blend'}
 for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
 for old,new in targets.items():
  matches=[l for l in bpy.data.libraries if Path(l.filepath).name==old]
  for l in matches:l.filepath=str(new);l.reload()
def views():
 old=TASK/'Revision_v005/Scenes'
 files={'downhole_A':'downhole_A_v006.blend','downhole_B':'downhole_B_v006.blend','layers':'layers_v010.blend','BHA_detail':'BHA_detail_v006.blend','Reuse_A':'Reuse_A_formation_v005.blend','Reuse_B':'Reuse_B_formation_v005.blend'}
 for name,filename in files.items():
  src=old/filename;openfile(src);before=B['snapshot']();relink();s=bpy.context.scene
  # Consumer-owned lighting follows the explicit feedback; camera/timing/control values preserved.
  if name.startswith('downhole'):
   bpy.data.objects['SOFT_COOL_KEY'].data.energy=19;bpy.data.objects['SOFT_COOL_KEY'].data.size=.85
   bpy.data.objects['WET_WARM_EDGE'].data.energy=8;bpy.data.objects['WET_WARM_EDGE'].data.size=.65
   bpy.data.objects['FORMATION_FILL'].data.energy=11
   s.view_settings.exposure=-1.20
  elif name=='BHA_detail':
   bpy.data.objects['BIT_KEY'].data.energy=45;bpy.data.objects['BIT_KEY'].data.size=1.1
   bpy.data.objects['BIT_EDGE'].data.energy=28;bpy.data.objects['BIT_EDGE'].data.size=.75
  after=B['snapshot']()
  assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_cleanup_v006.blend');B['save'](out)
  dump(E/(name+'_migration_v006.json'),dict(source=rel(src),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True))
 print('CLEANUP_VIEWS_PASS',flush=True)
def finish():
 openfile(ASSET/'BHA/BHA_film_v003.blend')
 for o in bpy.data.collections['WORLD_HARDWARE'].objects:
  if o.name.startswith('PDC_NOZZLE'):o.location.x+=.018
  if o.name.startswith('PDC_INTEGRAL_BLADE'):
   for p in o.data.polygons:p.use_smooth=True
   o.data.set_sharp_from_angle(angle=.65)
   o.modifiers[0].harden_normals=True
   w=o.modifiers.new('Blade face normals','WEIGHTED_NORMAL');w.keep_sharp=True;w.weight=30
 bpy.data.collections['WORLD_HARDWARE']['revision']='v004; v003 PDC study with softened blade normals and exposed recessed nozzle mouths'
 B['save'](ASSET/'BHA/BHA_film_v004.blend')
 openfile(ASSET/'WellAssembly/World_environment_v006.blend')
 shoe=bpy.data.objects['ILLUSTRATIVE_SHOE_RIM'];shoe.hide_render=True;shoe.hide_viewport=True
 shoe['correction']='Duplicate coplanar inner/outer surfaces overlap source casing atX[-.07,0]. Retained as hidden provisional geometry; source casing end provides flush shoe-boundary context. No exact shoe hardware claim.'
 mud=bpy.data.collections['WORLD_MUD'];fm=bpy.data.materials['WORLD_StaticFluid_v006'];fm.name='WORLD_StaticFluid_v007'
 bs=next(n for n in fm.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Base Color'].default_value=(.12,.18,.155,1);bs.inputs['Roughness'].default_value=.13;bs.inputs['Coat Weight'].default_value=.6
 mp=next(n for n in fm.node_tree.nodes if n.type=='MAP_RANGE');mp.inputs['To Min'].default_value=.08;mp.inputs['To Max'].default_value=.16
 # A conservative optical shell remains inside every supported lower bore variant.
 rear=bpy.data.objects['MUD_CURVED_REAR_OPTICAL_SKIN']
 for v in rear.data.vertices:
  x=v.co.x;a=math.atan2(v.co.z,v.co.y);rr=(.1589405 if x<0 else R)-.0006-.0001*(1+math.sin(31*x+5*a));v.co.y=rr*math.cos(a);v.co.z=rr*math.sin(a)
 rear['supported_variant']='Nominal-bounded optical rear skin within all nominal/irregular/spiral bores; not a full fluid-domain mesh.'
 vs=[];fs=[];nx=256;nz=64
 for i in range(nx+1):
  x=-5.5+11.5*i/nx;rr=(.1589405 if x<0 else R)-.00055
  for j in range(nz+1):
   z=rr*(-1+2*j/nz);t=z/rr;y=-.012*math.sqrt(max(0,1-t*t))*(1+.03*math.sin(23*x+4*t))
   vs.append((x,y,z))
 for i in range(nx):
  for j in range(nz):q=i*(nz+1)+j;fs.append((q,q+nz+1,q+nz+2,q+1))
 o=B['mesh']('MUD_CURVED_OPTICAL_CUT',vs,fs,mud,fm)
 for p in o.data.polygons:p.use_smooth=True
 o['status']='Curved translucent optical cut face within every bore; tool naturally occludes it. This intentionally exposed fluid section is not a free air/liquid surface or CFD. Static micro-normal treatment only.'
 bpy.data.collections['WORLD_ENV']['revision']='v007; accepted formation/source-layer meshes fixed; smooth steel, duplicate shoe overlap hidden, static curved fluid cut/reflections'
 B['save'](ASSET/'WellAssembly/World_environment_v007.blend')
 for name in ['downhole_A','downhole_B','layers','BHA_detail','Reuse_A','Reuse_B']:
  openfile(SCENES/(name+'_cleanup_v006.blend'));before=B['snapshot']()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  for old,new in [('BHA_film_v003.blend',ASSET/'BHA/BHA_film_v004.blend'),('World_environment_v006.blend',ASSET/'WellAssembly/World_environment_v007.blend')]:
   for l in list(bpy.data.libraries):
    if Path(l.filepath).name==old:l.filepath=str(new);l.reload()
  if name.startswith('downhole'):
   c=bpy.data.collections['LOCAL_APPROVAL'];B['light']('FLUID_GRAZE',(1.2,-.22,.27),(1.7,0,.10),4,.38,c,(.55,.78,.72))
  after=B['snapshot']();assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_cleanup_v007.blend');B['save'](out)
  dump(E/(name+'_migration_v007.json'),dict(source=rel(SCENES/(name+'_cleanup_v006.blend')),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True))
 # Additional face-angle inspection makes nozzle/cutter layout judgeable; reuse cameras stay intact.
 openfile(SCENES/'BHA_detail_cleanup_v007.blend');s=bpy.context.scene;cam=s.camera
 cam.location=(4.35,-.72,.43);cam.rotation_euler=(Vector((3.60,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=58
 s['purpose']='Additional static bit-face inspection; inherited side-view and reuse-test cameras remain unchanged'
 B['save'](SCENES/'BHA_face_cleanup_v007.blend')
 print('CLEANUP_FINISH_PASS',flush=True)
def inspect(name,version='v006'):
 path=SCENES/(name+'_cleanup_'+version+'.blend');openfile(path);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
 deps=bpy.context.evaluated_depsgraph_get()
 rec=dict(path=rel(path),sha256=sha(path),libraries=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries],camera=B['snapshot']()['camera'],timing=B['snapshot']()['timing'],eccos=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in deps.object_instances),blades=sum(i.object.original.name.startswith('PDC_INTEGRAL_BLADE') for i in deps.object_instances))
 assert all(l['exists'] and l['path'].startswith('//') for l in rec['libraries'])
 if name!='layers':assert rec['eccos']==1 and rec['blades']==6
 dump(E/(name+'_fresh-open_'+version+'.json'),rec);return path
def polish():
 openfile(ASSET/'BHA/BHA_film_v004.blend');c=bpy.data.collections['WORLD_HARDWARE']
 for o in c.objects:
  if o.name.startswith('PDC_INTEGRAL_BLADE'):
   k=int(o.name[-2:])-1
   for v in o.data.vertices:
    r=math.hypot(v.co.y,v.co.z);center=k*math.tau/6+.44*(r/R)**1.15
    a=math.atan2(v.co.z,v.co.y);delta=(a-center+math.pi)%math.tau-math.pi;a=center+1.6*delta
    v.co.y=r*math.cos(a);v.co.z=r*math.sin(a)
   o.data.update();o.modifiers[0].width=.0023;o.modifiers[0].segments=3
  elif o.name.startswith(('PDC_COMPACT_','PDC_TABLE_')):
   k=int(o.name.split('_')[-2])-1;v=o.location;r=math.hypot(v.y,v.z)
   shift=-.6*min(.35,(.014+.018*r/R)/(2*r))
   a=math.atan2(v.z,v.y)+shift;v.y=r*math.cos(a);v.z=r*math.sin(a);o.rotation_euler.rotate_axis('Z',0)
   # Rotate cutter axes about the longitudinal axis with their leading-edge positions.
   from mathutils import Matrix
   o.rotation_euler=(Matrix.Rotation(shift,3,'X')@o.rotation_euler.to_matrix()).to_euler()
  elif o.name=='PDC_WEB_AND_SHANK':
   o.data.set_sharp_from_angle(angle=.6)
   for p in o.data.polygons:
    if abs(p.normal.x)>.98:p.use_smooth=False
 c['revision']='v005; broader integral blades/edge radii, matched leading cutters and distinct nozzle/junk spaces; documented provisional PDC study'
 B['save'](ASSET/'BHA/BHA_film_v005.blend')
 openfile(ASSET/'WellAssembly/World_environment_v007.blend');m=bpy.data.materials['WORLD_StaticFluid_v007'];m.name='WORLD_StaticFluid_v008';m.surface_render_method='BLENDED'
 bpy.data.collections['WORLD_ENV']['revision']='v008; v007 native overlap/normals correction with noise-free blended static fluid optics; accepted formation unchanged'
 B['save'](ASSET/'WellAssembly/World_environment_v008.blend')
 for name in ['downhole_A','downhole_B','layers','BHA_detail','BHA_face','Reuse_A','Reuse_B']:
  openfile(SCENES/(name+'_cleanup_v007.blend'));before=B['snapshot']()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  for old,new in [('BHA_film_v004.blend',ASSET/'BHA/BHA_film_v005.blend'),('World_environment_v007.blend',ASSET/'WellAssembly/World_environment_v008.blend')]:
   for l in list(bpy.data.libraries):
    if Path(l.filepath).name==old:l.filepath=str(new);l.reload()
  after=B['snapshot']();assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_cleanup_v008.blend');B['save'](out)
  dump(E/(name+'_migration_v008.json'),dict(source=rel(SCENES/(name+'_cleanup_v007.blend')),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True))
 print('CLEANUP_POLISH_PASS',flush=True)
def render(name,tag='working',version='v006'):
 path=inspect(name,version);s=bpy.context.scene;s.render.filepath=str(P/(name+'_'+tag+'_'+version+'.png'))
 start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
 dump(E/(name+'_'+tag+'_benchmark_'+version+'.json'),dict(scene=rel(path),output=rel(Path(s.render.filepath)),seconds=elapsed,under_5=elapsed<5,engine=s.render.engine,backend='VULKAN',resolution=[s.render.resolution_x,s.render.resolution_y],samples=s.eevee.taa_render_samples,measurement='Complete first render(write_still=True) in fresh process; process/file loading excluded; no warmup render',cache='Normal pre-existing driver disk caches',known_limit='Prior empty-cache startup12.55-25.13s remains unresolved; this timing does not establish cold-machine compliance.'))
 print('CLEANUP_RENDER',name,elapsed,elapsed<5,flush=True)
def fluid_fast():
 openfile(ASSET/'WellAssembly/World_environment_v008.blend')
 old=bpy.data.materials['WORLD_StaticFluid_v008'];m=B['mat']('WORLD_StaticFluid_v009',(.10,.155,.135),0,.15)
 bs=next(n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Alpha'].default_value=.14;bs.inputs['IOR'].default_value=1.4;bs.inputs['Coat Weight'].default_value=.35;bs.inputs['Coat Roughness'].default_value=.12;m.surface_render_method='BLENDED'
 for o in bpy.data.collections['WORLD_MUD'].objects:
  if o.type=='MESH':B['assign'](o,m)
 # One optical cut surface; overlapping rear skin is retained but not rendered.
 bpy.data.objects['MUD_CURVED_REAR_OPTICAL_SKIN'].hide_render=True;bpy.data.objects['MUD_CURVED_REAR_OPTICAL_SKIN'].hide_viewport=True
 bpy.data.collections['WORLD_ENV']['revision']='v009; simple continuously blended curved static fluid section, no shader noise/angle graph or duplicate transparent overdraw. v008 first-shader6.45s failure retained.'
 B['save'](ASSET/'WellAssembly/World_environment_v009.blend')
 for name in ['downhole_A','downhole_B','layers','BHA_detail','BHA_face','Reuse_A','Reuse_B']:
  openfile(SCENES/(name+'_cleanup_v008.blend'));before=B['snapshot']()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  for l in list(bpy.data.libraries):
   if Path(l.filepath).name=='World_environment_v008.blend':l.filepath=str(ASSET/'WellAssembly/World_environment_v009.blend');l.reload()
  after=B['snapshot']();assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_cleanup_v009.blend');B['save'](out)
  dump(E/(name+'_migration_v009.json'),dict(source=rel(SCENES/(name+'_cleanup_v008.blend')),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True))
 print('CLEANUP_FAST_FLUID_PASS',flush=True)
def gauge_joint():
 openfile(ASSET/'BHA/BHA_film_v005.blend');c=bpy.data.collections['WORLD_HARDWARE']
 o=bpy.data.objects['PDC_ADAPTER_SHOULDER'];o.hide_render=True;o.hide_viewport=True;o['correction']='Redundant coincident shoulder overlay hidden; same joint envelope supplied by web/shank.'
 for o in c.objects:
  if o.name.startswith('PDC_GAUGE_PAD'):
   for v in o.data.vertices:
    rr=math.hypot(v.co.y,v.co.z);v.co.y*=R/rr;v.co.z*=R/rr
   o.data.update();o['nominal_gauge_radius_m']=R
  elif o.name in ['UPHOLE_COLLAR','DOWNHOLE_COLLAR']:normals(o)
 c['revision']='v006; v005 six-blade PDC with exact12.25in gauge pads and redundant joint overlay hidden; source ECCO unchanged'
 B['save'](ASSET/'BHA/BHA_film_v006.blend')
 for name in ['downhole_A','downhole_B','layers','BHA_detail','BHA_face','Reuse_A','Reuse_B']:
  openfile(SCENES/(name+'_cleanup_v009.blend'));before=B['snapshot']()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  for l in list(bpy.data.libraries):
   if Path(l.filepath).name=='BHA_film_v005.blend':l.filepath=str(ASSET/'BHA/BHA_film_v006.blend');l.reload()
  after=B['snapshot']();assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_cleanup_v010.blend');B['save'](out)
  dump(E/(name+'_migration_v010.json'),dict(source=rel(SCENES/(name+'_cleanup_v009.blend')),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True))
 print('CLEANUP_GAUGE_JOINT_PASS',flush=True)
mode=ARGS[0]
if mode=='hardware':hardware()
elif mode=='environment':environment()
elif mode=='views':views()
elif mode=='finish':finish()
elif mode=='polish':polish()
elif mode=='fluid_fast':fluid_fast()
elif mode=='gauge_joint':gauge_joint()
elif mode=='render':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working')
elif mode=='render7':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v007')
elif mode=='render8':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v008')
elif mode=='render9':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v009')
elif mode=='render10':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v010')
elif mode=='inspect':inspect(ARGS[1])
