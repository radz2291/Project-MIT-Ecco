"""T47 bounded shared variants and two reuse consumers. Never renders in build.

Run Blender background --python this.py -- build|verify|benchmark|demo
"""
import bpy,math,json,sys,time,hashlib,platform
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';BASE=A/'CasedHole';T=ROOT/'04-Production/Records/Tasks/T-047';E=T/'Evidence';SC=T/'Scenes';P=T/'Previews/v001'
for p in [BASE,E,SC,P]:p.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(BASE/'Scripts'));sys.path.insert(0,str(A/'World/Scripts'))
from cased_controls_v001 import create_cased,response_from_event,add_response
from formation_controls_v003 import create_world
RI=.1589405;RO=.1698625;RC=.22225;X0=-5.5;X1=0.;CH0=-2.5;CH1=-.4;ANG0=.30;ANG1=.80;WEAR=.004
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def clean():bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;return s
def col(n):c=bpy.data.collections.new(n);c.use_fake_user=True;return c
def mat(n,rgb,metal=0,rough=.45):
 m=bpy.data.materials.new(n);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*rgb,1);bs.inputs['Metallic'].default_value=metal;bs.inputs['Roughness'].default_value=rough;return m
def shell(n,c,m,x0,x1,ri,ro,a0,a1,wear=False):
 ni=40 if wear else 1;na=max(3,round(96*(a1-a0)/math.tau));vs=[];fs=[]
 for layer,r in enumerate([ri,ro]):
  for i in range(ni+1):
   x=x0+(x1-x0)*i/ni
   for j in range(na+1):
    a=a0+(a1-a0)*j/na;d=WEAR*math.exp(-((a/.28)**2))*max(0,math.cos((x+1.5)*math.pi/1.6))**2 if wear and layer==0 and abs(x+1.5)<.8 else 0
    vs.append((x,(r+d)*math.cos(a),(r+d)*math.sin(a)))
 size=(ni+1)*(na+1)
 for layer in range(2):
  for i in range(ni):
   for j in range(na):
    q=layer*size+i*(na+1)+j;face=(q,q+1,q+na+2,q+na+1);fs.append(face if layer==1 else face[::-1])
 for i in [0,ni]:
  for j in range(na):q=i*(na+1)+j;fs.append((q,q+size,q+size+1,q+1))
 for j in [0,na]:
  for i in range(ni):q=i*(na+1)+j;fs.append((q,q+na+1,q+na+1+size,q+size))
 me=bpy.data.meshes.new(n);me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new(n,me);c.objects.link(o);me.materials.append(m)
 for p in me.polygons:p.use_smooth=abs(p.normal.x)<.7 and abs(p.normal.dot(Vector((0,math.cos((a0+a1)/2),math.sin((a0+a1)/2)))))>.5
 o['basis']='T44 registered radii; X longitudinal metres; static pre-existing condition';o['ri_m']=ri;o['ro_m']=ro;return o
def line(n,pts,c,m,r=.0005):
 d=bpy.data.curves.new(n,'CURVE');d.dimensions='3D';d.bevel_depth=r;d.bevel_resolution=1;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,q in zip(sp.points,pts):p.co=(*q,1)
 o=bpy.data.objects.new(n,d);c.objects.link(o);d.materials.append(m);return o
def save(p):
 assert not p.exists(),p
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
def master(version,rough):
 s=clean();steel=mat('CASED_SATIN_STEEL',(.24,.29,.32),.78,rough);cement=mat('CASED_CEMENT',(.37,.29,.135),0,.8);channel=mat('CASED_CHANNEL_UNCLASSIFIED',(.025,.19,.33),0,.53);white=mat('CASED_NOMINAL_REFERENCE',(.75,.80,.82),0,.45)
 for cut in [False,True]:
  tag='CUTAWAY' if cut else 'FULL';a0,a1=(-math.pi/2,math.pi/2) if cut else (-math.pi/2,3*math.pi/2)
  for wear in [False,True]:
   c=col('CASED_STEEL_'+('WEAR' if wear else 'NOMINAL')+'_'+tag);shell('CASED_STEEL_'+('WEAR' if wear else 'NOMINAL')+'_'+tag,c,steel,X0,X1,RI,RO,a0,a1,wear)
  c=col('CASED_CEMENT_SUPPORTED_'+tag);shell('CASED_SUPPORTED_'+tag,c,cement,X0,X1,RO,RC,a0,a1)
  c=col('CASED_CEMENT_CHANNEL_'+tag)
  for n,xa,xb,aa,ab in [('UPHOLE',X0,CH0,a0,a1),('DOWNHOLE',CH1,X1,a0,a1),('LEFT',CH0,CH1,a0,ANG0),('RIGHT',CH0,CH1,ANG1,a1)]:shell('CASED_CEMENT_'+n+'_'+tag,c,cement,xa,xb,RO,RC,aa,ab)
  c=col('CASED_CHANNEL_'+tag);o=shell('CASED_EXTERIOR_CHANNEL_'+tag,c,channel,CH0,CH1,RO,RC,ANG0,ANG1);o['meaning']='Localized pre-existing exterior gap/weak support illustration; no chemical identification or flow'
  c=col('CASED_NOMINAL_REFERENCE_'+tag)
  for x in [-1.9,-1.5,-1.1]:line('REGISTERED_NOMINAL_INNER_CONTOUR',[(x,RI*math.cos(a0+(a1-a0)*j/96),RI*math.sin(a0+(a1-a0)*j/96)) for j in range(97)],c,white,.00045)
  line('REGISTERED_NOMINAL_AXIAL',[(x,RI,0) for x in [-2.3,-.7]],c,white,.00045)
 for c in bpy.data.collections:c['version']=version;c['units_axes']='metres; longitudinal +X';c['limits']='Illustrative support/channel and4mm inner wear, no bond/thickness inference; source OD unchanged'
 s['purpose']='T47 reusable layer master; no exploded display offset; source dimensions preserved';save(BASE/('CasedHole_'+version+'.blend'))
def settings(s):
 s.render.engine='BLENDER_EEVEE';s.eevee.taa_render_samples=16;s.eevee.use_raytracing=False;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.image_settings.compression=15;s.render.use_compositing=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast'
 w=bpy.data.worlds.new('CASED_REVIEW_LIGHT');w.use_nodes=True;w.node_tree.nodes['Background'].inputs[0].default_value=(.10,.13,.16,1);w.node_tree.nodes['Background'].inputs[1].default_value=.4;s.world=w
def light(c,n,pos,target,power,size):
 d=bpy.data.lights.new(n,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.use_shadow=False;o=bpy.data.objects.new(n,d);c.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def fixture():
 a=math.radians(39);return dict(event_id='T47_DECLARED_FIXTURE_001',provenance='declared_adapter_fixture',emitter_ref='ECCO_SENSOR_REF_01',receiver_ref='ECCO_SENSOR_REF_01',emitter_world_m=[-1.5,.10025183,.08118233],direction_world=[0,math.cos(a),math.sin(a)],hit_world_m=[-1.5,RI*math.cos(a),RI*math.sin(a)],normal_world=[0,-math.cos(a),-math.sin(a)],wall_source=dict(library=rel(BASE/'CasedHole_v002.blend'),object='CASED_STEEL_NOMINAL_CUTAWAY',version='v002',sha256=sha(BASE/'CasedHole_v002.blend')),send_s=.3,contact_s=.7,receive_s=1.1,patch_lifetime_s=.65,opacity=.8,visible=True)
def snapshot():
 s=bpy.context.scene;cam=s.camera;return dict(camera=dict(location=list(cam.location),rotation=list(cam.rotation_euler),lens=cam.data.lens,type=cam.data.type,ortho_scale=cam.data.ortho_scale),timing=[s.frame_start,s.frame_end,s.render.fps],controls={n:{k:float(v) for k,v in bpy.data.objects[n].items() if isinstance(v,(int,float))} for n in ['WORLD_CONTROL','CASED_CONTROL']})
def consumer(kind,version='v001'):
 s=clean();settings(s);root,w,inst=create_world(A);w['travel_m']=-2.23;w['rotation_rad']=0.;w['show_casing']=0;w['show_cement']=0;w['show_formation']=1;w['show_open']=0;w['show_mud']=1;w['show_shoe']=0;w.update_tag()
 cc,ci=create_cased(A,version);cc['channel']=int(kind=='B');cc['wear']=int(kind=='B');cc.update_tag()
 local=col('LOCAL_CASED_REUSE_'+kind);s.collection.children.link(local)
 d=bpy.data.cameras.new('CASED_CAMERA_'+kind);cam=bpy.data.objects.new(d.name,d);local.objects.link(cam);s.camera=cam
 if kind=='A':cam.location=(-1.05,-1.05,.61);target=(-1.5,0,0);d.lens=45;s.frame_end=72
 else:cam.location=(-1.48,-.71,.27);target=(-1.5,.10,.02);d.lens=55;s.frame_end=96
 cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();d.clip_start=.005;d.clip_end=100
 light(local,'CASED_KEY',(-1.5,-1.6,1.3),(-1.5,.08,0),90,1.5);light(local,'CASED_GRAZE',(-2,-.3,.45),(-1.5,.15,0),18,.25)
 # Show the groove/channel with quiet separate layer visibility; no appearance changes to source steel.
 if kind=='B':w['show_hardware']=0;w['show_mud']=0
 s['purpose']='T47 shared-package reuse test, not S04 film shot';s['limits']='Layer cutaway is explanatory. Support and4mm wear illustrative; no acoustic calibration, chemical classification or thickness result.'
 s['future_consumers']='S04-A/B/C/D';s['demo_kind']=kind
 save(SC/('CasedReuse_'+kind+'_'+version+'.blend'));dump(E/('consumer_'+kind+'_baseline_v001.json'),snapshot())
def propagate():
 rows=[]
 for kind in ['A','B']:
  old=SC/('CasedReuse_'+kind+'_v001.blend');bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False);before=snapshot()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  for l in list(bpy.data.libraries):
   if Path(l.filepath).name=='CasedHole_v001.blend':l.filepath=str(BASE/'CasedHole_v002.blend');l.reload()
  after=snapshot();assert before==after;save(SC/('CasedReuse_'+kind+'_v002.blend'));rows.append(dict(consumer=kind,before=before,after=after,preserved=True,revision='Master satin roughness .45→.39, same geometry and object names'))
 dump(E/'revision-propagation_v002.json',rows)
def verify():
 rows=[]
 for kind in ['A','B']:
  path=SC/('CasedReuse_'+kind+'_v002.blend');bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();libs=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath),exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries]
  assert all(l['exists'] and l['path'].startswith('//') for l in libs)
  ec=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in deps.object_instances);assert ec==(1 if kind=='A' else 0)
  for k in ['NOMINAL','WEAR']:
   ob=bpy.data.objects['CASED_STEEL_'+k+'_CUTAWAY'];rr=[math.hypot(v.co.y,v.co.z) for v in ob.data.vertices];assert abs(max(rr)-RO)<1e-6;assert min(rr)>=RI-1e-6
  rows.append(dict(scene=rel(path),sha256=sha(path),libraries=libs,snapshot=snapshot(),eccos=ec,steel_outer_radius_m=RO,nominal_inner_radius_m=RI,authored_preexisting_wear_max_m=WEAR,unit_scale=s.unit_settings.scale_length))
 dump(E/'saved-native-verification_v002.json',rows)
def render_samples():
 rows=[]
 for kind in ['A','B']:
  path=SC/('CasedReuse_'+kind+'_v002.blend');bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene
  for f in [1,48]:
   s.frame_set(f);s.render.filepath=str(P/('CasedReuse_'+kind+'_f%03d_v002.png'%f));start=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-start;rows.append(dict(scene=rel(path),frame=f,seconds=dt,under_5=dt<5,output=rel(Path(s.render.filepath))))
   dump(E/'benchmark_v002.json',dict(samples=rows,settings=dict(engine=s.render.engine,backend='VULKAN',samples=16,resolution=[1280,720],fps=24,color='AgX Medium High Contrast',compositor=False),cache='Normal pre-existing GPU driver caches; no warmup render. Known T44 empty-cache initialization12.55–25.13s remains unresolved. Process/file load excluded.',machine=platform.node()))
   if dt>=5:raise RuntimeError('Strict render cap failed; simplify before batch')
def build():master('v001',.45);master('v002',.39);consumer('A');consumer('B');propagate();dump(E/'declared-fixture_v001.json',fixture());verify()
mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'verify'
if mode=='build':build()
elif mode=='verify':verify()
elif mode=='benchmark':render_samples()
print('T47_'+mode.upper()+'_COMPLETE',flush=True)
