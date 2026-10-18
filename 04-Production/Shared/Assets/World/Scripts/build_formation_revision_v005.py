"""Owner-requested T44 formation coverage and approval-image revision.

Use isolated Blender; sources/previous candidates are immutable. Native output
never overwrites a prior candidate. Static approval views are not film shots.
"""
import bpy,math,sys,json,hashlib,time,runpy,platform,os
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];PROD=ROOT/'04-Production';ASSET=PROD/'Shared/Assets';TASK=PROD/'Records/Tasks/T-044'
REV=TASK/'Revision_v005';SCENES=REV/'Scenes';E=REV/'Evidence';P=TASK/'Previews/Revision_v005'
for path in [SCENES,E,P,ASSET/'Formation']:path.mkdir(parents=True,exist_ok=True)
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['library']
sys.argv=['script','--','noop'];B=runpy.run_path(str(HERE/'build_world_t44.py'));sys.path.insert(0,str(HERE))
def dump(path,data):path.write_text(json.dumps(data,indent=2),encoding='utf-8')
def rel(path):return path.relative_to(ROOT).as_posix()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def rockmat(name,macro=False):
 m=B['mat'](name,(.065,.047,.032),.04,.48)
 ns=m.node_tree.nodes;lk=m.node_tree.links;bs=next(n for n in ns if n.type=='BSDF_PRINCIPLED');bs.inputs['Coat Weight'].default_value=.24;bs.inputs['Coat Roughness'].default_value=.22
 tc=ns.new('ShaderNodeTexCoord');tex=ns.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=1.3 if macro else 52;tex.inputs['Detail'].default_value=3;tex.inputs['Roughness'].default_value=.75
 lk.new(tc.outputs['Object'],tex.inputs['Vector'])
 ramp=ns.new('ShaderNodeValToRGB');r=ramp.color_ramp;r.elements[0].position=.15;r.elements[0].color=(.014,.012,.010,1);r.elements[1].position=.85;r.elements[1].color=(.18,.12,.065,1)
 lk.new(tex.outputs['Fac'],ramp.inputs[0])
 wave=ns.new('ShaderNodeTexWave');wave.wave_type='BANDS';wave.bands_direction='X';wave.inputs['Scale'].default_value=.13 if macro else 4.2;wave.inputs['Distortion'].default_value=2.2;wave.inputs['Detail Scale'].default_value=.7
 lk.new(tc.outputs['Object'],wave.inputs['Vector']);mix=ns.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.28;lk.new(ramp.outputs['Color'],mix.inputs[1]);lk.new(wave.outputs['Color'],mix.inputs[2]);lk.new(mix.outputs['Color'],bs.inputs['Base Color'])
 bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.44;bump.inputs['Distance'].default_value=.08 if macro else .003
 lk.new(tex.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],bs.inputs['Normal'])
 return m
def radius(x,a,variant):
 if x<0:return .22225
 r=.155575
 if variant==1:r+=.0254*math.exp(-((x-2.8)/.95)**2)*(.55+.45*math.cos(3*a+.7*x))
 if variant==2:r+=.0254*(1+math.cos(a-math.tau*x/1.8))/2
 return r
def mass(name,col,material,variant=1,full=False,extent=2.4,x0=-8.,x1=10.,macro=False):
 # A rectangular surrounding formation cross-section, with a dimensioned bore.
 # Fine bore dimensions are left to the exact T6 inner surfaces; mass sits0.7mm behind them.
 nx=180;na=96;nr=40;verts=[];faces=[];mats=[]
 xs=[x0+(x1-x0)*i/nx for i in range(nx+1)]
 if x0<0<x1:xs=[x for x in xs if abs(x)>1e-5]+[-1e-7,0.]
 xs=sorted(set(round(x,8) for x in xs));nx=len(xs)-1
 start=0 if full else -math.pi/2;end=math.tau if full else math.pi/2
 def v(p):verts.append(p);return len(verts)-1
 def face(ids):faces.append(ids)
 for outer in [False,True]:
  for i in range(nx+1):
   x=xs[i]
   for j in range(na+1):
    a=start+(end-start)*j/na;r=extent/max(abs(math.cos(a)),abs(math.sin(a))) if outer else radius(x,a,0 if macro else variant)+.0007
    v((x,r*math.cos(a),r*math.sin(a)))
 size=(nx+1)*(na+1)
 for layer in [0,1]:
  for i in range(nx):
   for j in range(na):
    q=layer*size+i*(na+1)+j;f=(q,q+1,q+na+2,q+na+1);face(f if layer==0 else tuple(reversed(f)))
 if not full:
  for side in [-1,1]:
   base=len(verts)
   for i in range(nx+1):
    x=xs[i];rin=radius(x,side*math.pi/2,0 if macro else variant)+.0007
    for j in range(nr+1):
     t=(j/nr)**1.65;z=rin+(extent-rin)*t
     # Cut-face relief is outside the bore; no inward clearance change.
     amp=.48 if macro else .075
     relief=amp*(1-math.exp(-(z-rin)/(.8 if macro else .045)))*(.58+.22*math.sin(x*(.7 if macro else 18)+z*9)+.20*math.sin(x*(2 if macro else 41)-z*23))
     v((x,-relief,side*z))
   for i in range(nx):
    for j in range(nr):q=base+i*(nr+1)+j;face((q,q+1,q+nr+2,q+nr+1))
 obj=B['mesh'](name,verts,faces,col,material)
 for poly in obj.data.polygons:poly.use_smooth=True
 obj['status']='Illustrative surrounding rock mass, not measured geology. Registered bore nominal dimensions retained; outer cut-face relief lies outside bore.'
 obj['supported_extent']=f'X[{x0},{x1}]m, transverse rectangular half-width{extent}m. Outer bounds kept outside immersive camera frusta.'
 obj['grid_rows']=nx+1;obj['grid_angles']=na+1
 return obj
def library():
 src=ASSET/'WellAssembly/World_environment_v004.blend';before=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
 root=bpy.data.collections['WORLD_ENV'];alias=bpy.data.collections['WORLD_UPPER_FORMATION']
 for o in list(alias.objects):bpy.data.objects.remove(o,do_unlink=True)
 rock=rockmat('FORMATION_WetMineral_v005')
 for name in ['NOMINAL_FULL','NOMINAL_CUTAWAY','IRREGULAR_FULL','IRREGULAR_CUTAWAY','SPIRAL_FULL','SPIRAL_CUTAWAY']:
  B['assign'](bpy.data.objects[name],rock)
 groups=[]
 for v,name in enumerate(['NOMINAL','IRREGULAR','SPIRAL']):
  for full in [False,True]:
   c=B['coll']('WORLD_FORMATION_'+name+('_FULL' if full else '_CUTAWAY'));groups.append(c)
   mass('FORMATION_'+name+('_FULL' if full else '_CUTAWAY'),c,rock,v,full)
   if v==1 and not full:alias.children.link(c)
 # A cinematic cut-section of the fluid domain. Hardware occludes it naturally.
 mud=bpy.data.collections['WORLD_MUD']
 for o in list(mud.objects):bpy.data.objects.remove(o,do_unlink=True)
 fm=B['mat']('FORMATION_MudSection_v005',(.095,.105,.055),.02,.22);bs=next(n for n in fm.node_tree.nodes if n.type=='BSDF_PRINCIPLED');bs.inputs['Alpha'].default_value=.42;bs.inputs['Coat Weight'].default_value=.6;bs.inputs['Coat Roughness'].default_value=.12;fm.surface_render_method='DITHERED'
 vs=[];fs=[];n=192
 for i in range(n+1):
  x=-5.5+11.5*i/n;rr=.1589405 if x<0 else radius(x,math.pi/2,1)-.0004
  vs.extend([(x,-.0005,-rr),(x,-.0005,rr)])
 for i in range(n):q=i*2;fs.append((q,q+2,q+3,q+1))
 o=B['mesh']('MUD_CINEMATIC_SECTION',vs,fs,mud,fm);o['status']='Static optical fluid section. Not a CFD domain; opaque hardware hides the interior portion. No flow or acoustic effects.'
 root['revision']='v005 surrounding formation coverage; prior v004 preserved';root['formation_extent']='X-8..10m, transverse half-width2.4m; six nominal/irregular/spiral/full/cut collections'
 root['control_contract']='world_controls v001 compatible alias WORLD_UPPER_FORMATION now has irregular rear mass; formation_controls_v002 selects all variants with show_formation/variant/cutaway'
 out=ASSET/'WellAssembly/World_environment_v005.blend';B['save'](out)
 dump(E/'formation-build_v005.json',dict(path=rel(out),sha256=sha(out),source_v004_sha256=before,source_unchanged=sha(src)==before,registered_hole_radius_m=.155575,upper_host_radius_m=.22225,source_wall_geometry_changed=False,formation_extent=dict(x=[-8,10],transverse_half_width=2.4),geology='authored illustrative',groups=[c.name for c in groups]))
 print('FORMATION_LIBRARY_PASS',flush=True)
def macro():
 src=ASSET/'Surface/Surface_context_v002.blend';before=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False)
 surf=bpy.data.collections['WORLD_SURFACE']
 if 'QUIET_SEA' in bpy.data.objects:bpy.data.objects.remove(bpy.data.objects['QUIET_SEA'],do_unlink=True)
 water=B['mat']('SURFACE_SectionWater',(.025,.065,.095),.35,.34,.035)
 B['box']('SEA_REAR_SECTION',(0,400,-.2),(1600,800,.15),surf,water)
 surf['revision']='v003; identical rig geometry/layout, intentional front water section removed for ground context'
 B['save'](ASSET/'Surface/Surface_context_v003.blend')
 s=B['clean']();c=B['coll']('WORLD_GROUND_CONTEXT');s.collection.children.link(c);rock=rockmat('FORMATION_MacroStrata',True)
 mass('ILLUSTRATIVE_EARTH_CONTEXT',c,rock,0,False,45.,-20,25,True)
 steel=B['mat']('CONTEXT_Casing',(.16,.21,.25),.65,.48);cement=B['mat']('CONTEXT_Cement',(.30,.24,.15),0,.82)
 B['tube']('CONTEXT_CASING',-20,0,.1589405,.1698625,c,steel,True);B['tube']('CONTEXT_CEMENT',-20,0,.1698625,.22225,c,cement,True)
 a=B['empty']('DOWNHOLE_DATUM_X0',c);a['placement']='Place at surface worldZ-60m and rotate+90degY. Illustrative local context, no actual well depth.'
 # The exposed route is inside the deliberate water/earth section, never seen through opaque earth.
 B['tube']('ILLUSTRATIVE_RISER',-60,-20,.16,.20,c,steel,True)
 c['extent']='LocalX[-20,25]m maps worldZ[-40,-85]m atZ-60; transverse90m square rear section'
 c['source_truth']='Registered T6 nominal radii; macro extents/water depth/strata/riser arrangement are authored composition, not deployment evidence'
 out=ASSET/'Formation/Formation_context_v001.blend';B['save'](out);dump(E/'context-build_v005.json',dict(path=rel(out),sha256=sha(out),surface_source_unchanged=sha(src)==before,macro_extent=[[-20,25],[-45,45],[-45,45]],illustrative_placement_z=-60))
 print('FORMATION_CONTEXT_PASS',flush=True)
def camera(s,c,loc,target,lens,roll=0):
 d=bpy.data.cameras.new('APPROVAL_CAMERA');o=bpy.data.objects.new(d.name,d);c.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();o.rotation_euler.rotate_axis('Z',roll);d.lens=lens;d.clip_start=.005;d.clip_end=2500;s.camera=o;return o
def views():
 from formation_controls_v002 import create_world
 # Five separately viewable approval images, each a saved static consumer.
 for name in ['downhole_A','downhole_B','layers','BHA_detail','wide_context']:
  s=B['clean']();B['settings'](s);s['consumer']='T44 formation approval '+name;s['purpose']='Representative shared-asset approval still; not a film-shot production scene'
  c=B['coll']('LOCAL_APPROVAL');s.collection.children.link(c);s.frame_end=1;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.055,.07,.09,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.18
  s.render.image_settings.color_mode='RGBA';s.render.film_transparent=name.startswith('downhole') or name=='layers'
  if name=='wide_context':
   surface=B['linkcoll'](ASSET/'Surface/Surface_context_v003.blend',['WORLD_SURFACE'])[0];B['instance'](surface,c,'SURFACE_LINK')
   ground=B['linkcoll'](ASSET/'Formation/Formation_context_v001.blend',['WORLD_GROUND_CONTEXT'])[0];o=B['instance'](ground,c,'GROUND_CONTEXT_LINK',(0,0,-60));o.rotation_euler.y=math.pi/2
   camera(s,c,(120,-190,80),(0,0,-10),42)
   B['light']('WARM_HORIZON',(-70,-70,100),(0,0,-15),900000,85,c,(1,.69,.38));B['light']('SKY_FILL',(30,-50,85),(0,0,-10),500000,90,c,(.48,.69,1))
   s.world.node_tree.nodes['Background'].inputs[0].default_value=(.16,.095,.048,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.5
  else:
   placement,ctrl,instances=create_world(ASSET);ctrl['travel_m']=.5;ctrl['rotation_rad']=.4
   if name.startswith('downhole'):
    for k in ['show_casing','show_cement','show_shoe']:ctrl[k]=0
    if name=='downhole_A':camera(s,c,(.72,-.78,.32),(1.58,.035,.015),42,-.12)
    else:camera(s,c,(.95,-.72,.38),(1.73,.035,.03),42,-.12)
    B['light']('SOFT_COOL_KEY',(1.3,-.65,.7),(1.6,.02,0),26,1.4,c,(.64,.80,1));B['light']('WET_WARM_EDGE',(2.15,-.05,.5),(1.6,.05,0),18,.9,c,(1,.68,.38));B['light']('FORMATION_FILL',(.7,-.7,-.25),(1.6,0,0),14,1.2,c,(.42,.6,.65))
   elif name=='layers':
    ctrl['travel_m']=-.8;camera(s,c,(.85,-1.8,.8),(-.12,.03,.04),56,-.12)
    B['light']('LAYER_KEY',(.15,-1.0,1.1),(0,0,0),75,2,c,(.72,.84,1));B['light']('LAYER_EDGE',(-.8,-.4,.5),(0,0,0),30,1.1,c,(1,.72,.40))
   else:
    for k in ['show_open','show_casing','show_cement','show_formation','show_shoe','show_mud']:ctrl[k]=0
    camera(s,c,(4.1,-1.7,.8),(3.15,0,0),58,-.12)
    B['light']('BIT_KEY',(3.1,-1.0,1.0),(3.2,0,0),65,1.4,c,(.73,.86,1));B['light']('BIT_EDGE',(3.65,.5,.5),(3.2,0,0),45,1,c,(1,.72,.42));B['light']('BIT_FILL',(2.5,-1,-.3),(3.2,0,0),18,1,c,(.4,.55,.7))
   ctrl.update_tag();bpy.context.view_layer.update()
  s['cutaway']='Intentional water/earth section' if name=='wide_context' else 'Rear-half ground/well and fluid section; source bore dimensions unchanged' if name!='BHA_detail' else 'Hardware-only inspection; bit/adapters illustrative'
  B['save'](SCENES/(name+'_v005.blend'))
 print('FORMATION_VIEWS_PASS',flush=True)
def migrate():
 for k in ['A','B']:
  src=TASK/'ReuseTests'/f'Reuse_{k}_after_v004.blend';bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);before=B['snapshot']()
  targets=[l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).name=='World_environment_v004.blend'];assert len(targets)==1
  targets[0].filepath=str(ASSET/'WellAssembly/World_environment_v005.blend');targets[0].reload()
  # Resolve other paths relative to the original consumer before Save As.
  for lib in bpy.data.libraries:
   if lib not in targets:lib.filepath=bpy.path.abspath(lib.filepath)
  s=bpy.context.scene;s.frame_set(1);after=B['snapshot']()
  assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/f'Reuse_{k}_formation_v005.blend';B['save'](out)
  dump(E/f'migration_{k}_v005.json',dict(source=rel(src),output=rel(out),before=before,after=after,preserved_camera_timing_controls=True,procedure='One environment library path/reload, then Save As with relative paths; no duplicated formation or product edits'))
 print('FORMATION_MIGRATION_PASS',flush=True)
def inspect(path):
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 rec=dict(path=rel(path),sha256=sha(path),libraries=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries],units=s.unit_settings.scale_length,mesh_instances=sum(1 for i in deps.object_instances if i.object.original.name=='ECCO_HOUSING_SOURCE_MESH'),camera=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens),cutaway=s.get('cutaway','Preserved reuse-test view'))
 assert all(l['exists'] and l['path'].startswith('//') for l in rec['libraries'])
 if 'wide_context' not in path.stem and 'layers' not in path.stem:assert rec['mesh_instances']==1
 dump(E/(path.stem+'_fresh-open.json'),rec);return rec
def refine_views():
 for name in ['downhole_A','downhole_B','layers','BHA_detail','wide_context']:
  bpy.ops.wm.open_mainfile(filepath=str(SCENES/(name+'_v005.blend')),load_ui=False,use_scripts=False);s=bpy.context.scene
  if name.startswith('downhole'):s.view_settings.exposure=-1.15
  elif name=='layers':
   s.view_settings.exposure=-.55
   cam=s.camera;cam.location=(.75,-1.12,.72);cam.rotation_euler=(Vector((-.08,.015,.02))-cam.location).to_track_quat('-Z','Y').to_euler();cam.rotation_euler.rotate_axis('Z',-.12);cam.data.lens=55
   ctrl=bpy.data.objects['WORLD_CONTROL'];ctrl['travel_m']=-1.5;ctrl.update_tag();bpy.context.view_layer.update()
  elif name=='BHA_detail':s.view_settings.exposure=-.45
  else:
   cam=s.camera;cam.location=(130,-230,80);cam.rotation_euler=(Vector((0,0,-8))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=35;s.view_settings.exposure=-.3
  B['save'](SCENES/(name+'_v006.blend'))
 print('FORMATION_REFINE_PASS',flush=True)
def finish_context_layers():
 old=ASSET/'Formation/Formation_context_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
 c=bpy.data.collections['WORLD_GROUND_CONTEXT'];obj=bpy.data.objects['ILLUSTRATIVE_EARTH_CONTEXT'];coords=[v.co.copy() for v in obj.data.vertices]
 nx=len(set(round(v.x,7) for v in coords));na=96;size=nx*(na+1);vs=[];fs=[]
 for row in [0,nx-1]:
  base=len(vs)
  for j in range(na+1):vs.extend([coords[row*(na+1)+j],coords[size+row*(na+1)+j]])
  for j in range(na):q=base+j*2;fs.append((q,q+1,q+3,q+2))
 B['mesh']('CONTEXT_SEAFLOOR_AND_BASE_CAPS',vs,fs,c,obj.data.materials[0])
 c['revision']='v002; visible seafloor/base caps added; dimensioned bore remains open'
 new=ASSET/'Formation/Formation_context_v002.blend';B['save'](new)
 bpy.ops.wm.open_mainfile(filepath=str(SCENES/'wide_context_v006.blend'),load_ui=False,use_scripts=False)
 target=[l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).name=='Formation_context_v001.blend'][0];target.filepath=str(new);target.reload();B['save'](SCENES/'wide_context_v007.blend')
 bpy.ops.wm.open_mainfile(filepath=str(SCENES/'layers_v006.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;cam=s.camera
 cam.location=(.65,-.12,.04);cam.rotation_euler=(Vector((-.08,.025,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=38;s.view_settings.exposure=-.7
 ctrl=bpy.data.objects['WORLD_CONTROL'];ctrl['show_hardware']=0;ctrl['show_mud']=0;ctrl.update_tag();bpy.context.view_layer.update();s['cutaway']='Axial casing-shoe section; hardware and optical mud hidden to inspect steel/cement/formation at actual scale'
 B['save'](SCENES/'layers_v007.blend');print('FORMATION_CONTEXT_LAYERS_PASS',flush=True)
def render(name,attempt='working',version='v005'):
 path=SCENES/(name+'_'+version+'.blend');rec=inspect(path);s=bpy.context.scene;s.render.filepath=str(P/(name+'_'+attempt+'_'+version+'.png'))
 start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
 data=dict(scene=rel(path),output=rel(Path(s.render.filepath)),seconds=elapsed,under_5=elapsed<5,cold='first full render in fresh process, normal existing driver caches; no warmup excluded',engine=s.render.engine,backend='VULKAN (explicit launch flag)',resolution=[s.render.resolution_x,s.render.resolution_y],samples=s.eevee.taa_render_samples,compositor=s.render.use_compositing,color_management=[s.view_settings.view_transform,s.view_settings.look],gpu='GTX1060 3GB / driver560.94',measurement='perf_counter around complete render(write_still=True); process/file loading excluded',known_limit='Previous uncached initialization12.55–25.13s retained; cache/driver/backend changes invalidate release')
 dump(E/(name+'_'+attempt+'_benchmark_'+version+'.json'),data);print('FORMATION_RENDER',name,elapsed,elapsed<5,flush=True)
def finish_layers():
 bpy.ops.wm.open_mainfile(filepath=str(SCENES/'layers_v007.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;cam=s.camera
 cam.location=(.9,-.36,.22);cam.rotation_euler=(Vector((0,.025,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=32
 B['save'](SCENES/'layers_v008.blend')
def cased_section():
 s=B['clean']();c=B['coll']('WORLD_CASED_FORMATION_SECTION');s.collection.children.link(c);mat=rockmat('FORMATION_CasedSection_v005')
 obj=mass('CASED_FORMATION_MASS',c,mat,0,False,2.4,-8.,-1e-7,False)
 coords=[v.co.copy() for v in obj.data.vertices];nx=len(set(round(v.x,7) for v in coords));na=96;size=nx*(na+1);vs=[];fs=[]
 for j in range(na+1):vs.extend([coords[(nx-1)*(na+1)+j],coords[size+(nx-1)*(na+1)+j]])
 for j in range(na):q=j*2;fs.append((q,q+1,q+3,q+2))
 B['mesh']('CASED_FORMATION_END_SECTION',vs,fs,c,mat);c['status']='Reusable upper-host-only intentional end section; lower formation hidden for layer inspection; physical radii unchanged'
 asset=ASSET/'Formation/Formation_cased-section_v001.blend';B['save'](asset)
 bpy.ops.wm.open_mainfile(filepath=str(SCENES/'layers_v008.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene;ctrl=bpy.data.objects['WORLD_CONTROL']
 ctrl['show_formation']=0;ctrl['show_open']=0;ctrl['show_hardware']=0;ctrl['show_mud']=0;ctrl.update_tag();bpy.context.view_layer.update()
 local=bpy.data.collections['LOCAL_APPROVAL'];lib=B['linkcoll'](asset,['WORLD_CASED_FORMATION_SECTION'])[0];B['instance'](lib,local,'CASED_SECTION_LINK')
 cam=s.camera;cam.location=(.85,-.40,.30);cam.rotation_euler=(Vector((-.03,.035,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=38
 s['cutaway']='Cased-host end section; lower formation, tool and optical mud intentionally hidden. Steel/cement/upper host/shoe at registered scale.'
 B['save'](SCENES/'layers_v009.blend');print('FORMATION_CASED_SECTION_PASS',flush=True)
def cased_section_fixed():
 s=B['clean']();c=B['coll']('WORLD_CASED_FORMATION_SECTION');s.collection.children.link(c);mat=rockmat('FORMATION_CasedSection_v005')
 obj=mass('CASED_FORMATION_MASS',c,mat,0,False,2.4,-8.,-1e-7,False)
 coords=[v.co.copy() for v in obj.data.vertices];nx=obj['grid_rows'];na=obj['grid_angles']-1;size=nx*(na+1);vs=[];fs=[]
 for j in range(na+1):vs.extend([coords[(nx-1)*(na+1)+j],coords[size+(nx-1)*(na+1)+j]])
 for j in range(na):q=j*2;fs.append((q,q+1,q+3,q+2))
 B['mesh']('CASED_FORMATION_END_SECTION',vs,fs,c,mat);c['status']='Reusable upper-host-only intentional end section; lower formation hidden for layer inspection; physical radii unchanged'
 asset=ASSET/'Formation/Formation_cased-section_v002.blend';B['save'](asset)
 bpy.ops.wm.open_mainfile(filepath=str(SCENES/'layers_v009.blend'),load_ui=False,use_scripts=False);s=bpy.context.scene
 target=[l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).name=='Formation_cased-section_v001.blend'][0];target.filepath=str(asset);target.reload()
 c=bpy.data.collections['LOCAL_APPROVAL'];B['light']('SECTION_FACE_FILL',(.6,-.3,.6),(0,.14,0),24,1.2,c,(.75,.85,1))
 B['save'](SCENES/'layers_v010.blend');print('FORMATION_CASED_FIXED_PASS',flush=True)
mode=ARGS[0]
if mode=='library':library()
elif mode=='macro':macro()
elif mode=='views':views()
elif mode=='migrate':migrate()
elif mode=='render':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working')
elif mode=='refine':refine_views()
elif mode=='render6':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v006')
elif mode=='finish_context_layers':finish_context_layers()
elif mode=='render7':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v007')
elif mode=='finish_layers':finish_layers()
elif mode=='render8':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v008')
elif mode=='cased_section':cased_section()
elif mode=='render9':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v009')
elif mode=='cased_fixed':cased_section_fixed()
elif mode=='render10':render(ARGS[1],ARGS[2] if len(ARGS)>2 else 'working','v010')
elif mode=='inspect':inspect(SCENES/ARGS[1])
