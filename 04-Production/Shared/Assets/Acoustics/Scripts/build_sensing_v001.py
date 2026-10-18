"""T46 isolated shared acoustic master/reuse tests; no render without queue grant."""
import bpy,sys,math,json,hashlib,os,time
from pathlib import Path
from mathutils import Vector,Matrix
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];A=ROOT/'04-Production/Shared/Assets';DEST=A/'Acoustics';T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';S=T/'Scenes';P=T/'Previews'
sys.path.insert(0,str(HERE));from acoustic_event_v001 import sample_native_event,validate_event,native_instance,wall_tree
for p in [DEST,E,S,P]:p.mkdir(parents=True,exist_ok=True)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def save(path):
 assert not path.exists(),f'Preserve {path}'
 resolved=[(l,Path(bpy.path.abspath(l.filepath)).resolve()) for l in bpy.data.libraries]
 for l,p in resolved:l.filepath=bpy.path.relpath(str(p),start=str(path.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=False)

def mat(name,color):
 m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
 o=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(*color,1);em.inputs[1].default_value=1.1
 tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');info=n.new('ShaderNodeObjectInfo');l.new(info.outputs['Alpha'],mix.inputs[0]);l.new(tr.outputs[0],mix.inputs[1]);l.new(em.outputs[0],mix.inputs[2]);l.new(mix.outputs[0],o.inputs[0]);m.surface_render_method='BLENDED';return m
def curve(name,points,col,material,r=.0005):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.resolution_u=1;d.bevel_depth=r;d.bevel_resolution=2
 for pts in points:
  sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
  for q,p in zip(sp.points,pts):q.co=(*p,1)
 ob=bpy.data.objects.new(name,d);col.objects.link(ob);d.materials.append(material);return ob
def mesh(name,vs,fs,col,material):
 d=bpy.data.meshes.new(name);d.from_pydata(vs,[],fs);d.update();o=bpy.data.objects.new(name,d);col.objects.link(o);d.materials.append(material);return o
def master(version,width):
 bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.unit_settings.system='METRIC'
 c=bpy.data.collections.new('ACOUSTICS_MASTER');s.collection.children.link(c);c['version']=version;c['units']='metres';c['axis']='prototype +Z along propagation/normal; consumer supplies sampled world pose'
 cyan=mat('ACOUSTICS_CYAN_SEND',(.04,.60,.88));green=mat('ACOUSTICS_EMERALD_RETURN',(.025,.70,.32));white=mat('ACOUSTICS_CONTACT',(.38,.9,.77))
 # Three separately addressable arcs per leg. Bow retreats from the advancing apex.
 for role,m in [('SEND',cyan),('RETURN',green)]:
  for k in range(3):
   pts=[(u*.009,0,-.004*u*u) for u in [-1+j/12 for j in range(25)]]
   curve('ACOUSTICS_'+role+'_%02d'%(k+1),[pts],c,m,width)
 vs=[(0,0,.0025)];rings=5;segments=32
 for r in range(1,rings+1):
  q=r/rings
  for j in range(segments):
   a=j*math.tau/segments;vs.append((.010*q*math.cos(a),.010*q*math.sin(a),.0007+.0018*(1-q*q)))
 fs=[]
 for j in range(segments):fs.append((0,1+j,1+(j+1)%segments))
 for r in range(1,rings):
  for j in range(segments):a=1+(r-1)*segments+j;b=1+(r-1)*segments+(j+1)%segments;fs.append((a,b,b+segments,a+segments))
 mesh('ACOUSTICS_CONTACT_CUP',vs,fs,c,white)
 lines=[]
 for axis in [0,1]:
  for v in [-.006,-.003,0,.003,.006]:
   q=[]
   for j in range(13):u=-.007+j*.014/12;q.append((u,v,.0012) if axis==0 else (v,u,.0012))
   lines.append(q)
 curve('ACOUSTICS_FINE_PATCH',lines,c,green,.00010)
 bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=6,radius=.00075);ob=bpy.context.object;ob.name='ACOUSTICS_FIXED_SAMPLE'
 for cc in list(ob.users_collection):cc.objects.unlink(ob)
 c.objects.link(ob);ob.data.materials.append(white)
 c['limits']='Illustrative graphics and timing. No measured data, velocity, simulation, calibrated bond or thickness.'
 save(DEST/f'Acoustics_{version}.blend')

def templates(version):
 with bpy.data.libraries.load(str(DEST/f'Acoustics_{version}.blend'),link=True) as (a,b):b.objects=[n for n in a.objects if n.startswith('ACOUSTICS_')]
 return {o.name:o for o in b.objects}
def local_ob(name,template,col):
 ob=bpy.data.objects.new(name,template.data);col.objects.link(ob);ob['shared_prototype']=template.name;ob['shared_package']='Acoustics';ob.color=(1,1,1,0);ob.visible_shadow=False;return ob
def key(o,path,f):o.keyframe_insert(data_path=path,frame=f)
def event_objects(e,temp,col):
 obs={n:local_ob(e['event_id']+'_'+n,temp[n],col) for n in temp}
 n=Vector(e['normal_world']);quat=n.to_track_quat('Z','Y');d=Vector(e['direction_world']);beamq=d.to_track_quat('Z','Y')
 for name,o in obs.items():o.rotation_euler=(beamq if 'SEND' in name or 'RETURN' in name else quat).to_euler()
 return obs
def animate_event(e,obs,frames,fps,ctrl):
 source=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);d=Vector(e['direction_world']);n=Vector(e['normal_world']);dist=(hit-source).length
 tangent=Vector((0,-d.z,d.y)).normalized()
 def arc_rotation(axis):return Matrix((tangent,axis.cross(tangent),axis)).transposed().to_euler()
 for f in range(1,frames+1):
  t=(f-1)/fps
  for name,o in obs.items():
   alpha=0;location=hit+n*.0002;scale=1
   if 'SEND_' in name or 'RETURN_' in name:
    k=int(name[-2:])-1;returning='RETURN_' in name
    o.rotation_euler=arc_rotation(-d if returning else d)
    start=e['contact_s'] if returning else e['send_s'];end=e['receive_s'] if returning else e['contact_s'];lag=k*.07;u=(t-start-lag)/(end-start)
    # Each complete arc remains in fluid; apex never exceeds sampled endpoints.
    p=dist*max(0,min(1,u));location=hit-d*p if returning else source+d*p
    scale=min(1,p/.006,(dist-p)/.006)
    if 0<=u<1:
     alpha=e['opacity']*(1-.18*k)
   elif 'CONTACT_CUP' in name:
    dt=t-e['contact_s'];alpha=.34*max(0,1-dt/.22) if 0<=dt<.22 else 0
   elif 'FINE_PATCH' in name:
    dt=t-e['contact_s'];alpha=.40*max(0,1-dt/e['patch_lifetime_s']) if 0<=dt<e['patch_lifetime_s'] else 0
   elif 'FIXED_SAMPLE' in name:alpha=.72 if t>=e['contact_s'] else 0;scale=.4
   o.location=location;o.scale=(scale,)*3;o.color=(1,1,1,alpha);o.hide_render=alpha<.001;o.hide_viewport=alpha<.001
   for p in ['location','rotation_euler','scale','color','hide_render','hide_viewport']:key(o,p,f)
 for o in obs.values():
  if o.animation_data:
   for slot in o.animation_data.action.layers:
    for strip in slot.strips:
     for bag in strip.channelbags:
      for fc in bag.fcurves:
       for k in fc.keyframe_points:k.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'

def cue(s,col,e):
 cam=s.camera;depth=max(cam.data.clip_start*1.3,.012);corners=cam.data.view_frame(scene=s);hw=max(abs(p.x/p.z*depth) for p in corners);hh=max(abs(p.y/p.z*depth) for p in corners)
 def point(x,y):return ((x-.5)*2*hw,(y-.5)*2*hh,-depth)
 gray=mat('CUE_QUIET',(.33,.40,.44));white=mat('CUE_WHITE',(.73,.80,.83));cyan=bpy.data.materials['ACOUSTICS_CYAN_SEND'];green=bpy.data.materials['ACOUSTICS_EMERALD_RETURN']
 def ln(name,pts,m,w=.00009):
  o=curve(name,[[point(x,y) for x,y in pts]],col,m,w/.00009*2*hh/720);o.parent=cam;o.color=(1,1,1,.8);return o
 ln('SCHEMATIC_TIMING_BASE',[(.10,.12),(.43,.12)],gray)
 ln('SCHEMATIC_TX_PEAK',[(.13,.12),(.145,.16),(.16,.105),(.18,.12)],cyan)
 ln('SCHEMATIC_ECHO_PEAK',[(.34,.12),(.355,.15),(.37,.11),(.39,.12)],green)
 ln('SCHEMATIC_INTERVAL',[(.145,.095),(.145,.085),(.355,.085),(.355,.095)],gray,.00006)
 fontpath=Path('C:/Windows/Fonts/segoeui.ttf');font=bpy.data.fonts.load(str(fontpath))
 for name,body,x,y,size in [('CUE_TITLE','Echo arrival',.10,.19,2*hh*24*1.4/720),('CUE_PROVENANCE','Schematic timing',.10,.045,2*hh*14*1.4/720)]:
  d=bpy.data.curves.new(name,'FONT');d.body=body;d.font=font;d.size=size;ob=bpy.data.objects.new(name,d);col.objects.link(ob);ob.parent=cam;ob.location=point(x,y);d.materials.append(white);ob.color=(1,1,1,.9)
 # The graphic appears after contact, then echo; no numeric/calibrated signal.
 for o in list(col.objects):
  if o.parent!=cam:continue
  for f in range(1,s.frame_end+1):
   t=(f-1)/24;on=e['contact_s']+.12<=t<=e['receive_s']+.4
   if 'ECHO_PEAK' in o.name:on=on and t>=e['receive_s']
   o.hide_render=not on;o.hide_viewport=not on;key(o,'hide_render',f);key(o,'hide_viewport',f)

def snapshot():
 s=bpy.context.scene;ctrl=bpy.data.objects['WORLD_CONTROL']
 return dict(camera=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens),timing=[s.frame_start,s.frame_end,s.render.fps],world_control_animation=str([(fc.data_path,[(p.co.x,p.co.y) for p in fc.keyframe_points]) for layer in ctrl.animation_data.action.layers for strip in layer.strips for bag in strip.channelbags for fc in bag.fcurves]) if ctrl.animation_data else None)

def consumer(kind):
 bpy.ops.wm.open_mainfile(filepath=str(ROOT/'04-Production/Records/Tasks/T-044/Revision_v006/Scenes/downhole_A_cleanup_v010.blend'),load_ui=False,use_scripts=False)
 s=bpy.context.scene;ctrl=bpy.data.objects['WORLD_CONTROL'];ctrl.animation_data_clear();s.frame_end=96 if kind=='A' else 108
 ctrl['travel_m']=.5;ctrl['rotation_rad']=.4;ctrl.update_tag();bpy.context.view_layer.update()
 cam=s.camera;cam.location=(.92,-.34,.58) if kind=='A' else (1.57,-.29,.49);target=Vector((1.23,.07,.15));cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=55 if kind=='A' else 48;cam.data.clip_start=.01;cam.data.dof.use_dof=False
 c=bpy.data.collections.new('LOCAL_ACOUSTIC_EVENTS');s.collection.children.link(c);temp=templates('v001');events=[]
 shift=0 if kind=='A' else .25
 poses=[(.4,.5,.35+shift,.85+shift,1.35+shift),(.66,.515,2.25+shift,2.65+shift,3.05+shift)]
 for k,(rot,travel,send,contact,receive) in enumerate(poses):
  ctrl['rotation_rad']=rot;ctrl['travel_m']=travel;ctrl.update_tag();bpy.context.view_layer.update()
  e=sample_native_event('ECCO_SENSOR_REF_01','IRREGULAR_CUTAWAY',f't46-{kind.lower()}-{k+1:02d}',send,contact,receive);validate_event(e);events.append(e);animate_event(e,event_objects(e,temp,c),s.frame_end,24,ctrl)
 for f in range(1,s.frame_end+1):
  t=(f-1)/24;u=max(0,min(1,(t-(1.65+shift))/.45));u=u*u*(3-2*u);ctrl['rotation_rad']=.4+.26*u;ctrl['travel_m']=.5+.015*u
  for p in ['rotation_rad','travel_m']:ctrl.keyframe_insert(data_path='["'+p+'"]',frame=f)
 cue(s,c,events[0]);s['task']='T46 linked asset reuse behavior proof, not V3 movie shot';s['event_export']=rel(E/f'events_{kind}_v001.json');s['timing']='Illustrative seconds; no firing cadence/velocity claim';s.render.use_compositing=False
 s.frame_set(20);before=snapshot();save(S/f'Sensing_reuse_{kind}_v001.blend');dump(E/f'events_{kind}_v001.json',dict(contract='ecco-acoustic-event-v001',events=events))
 # Bounded immutable successor: only shared arc thickness +10%, local animation/camera untouched.
 for l in list(bpy.data.libraries):
  if Path(l.filepath).name=='Acoustics_v001.blend':l.filepath=str(DEST/'Acoustics_v002.blend');l.reload()
 after=snapshot();assert before==after
 save(S/f'Sensing_reuse_{kind}_v002.blend');dump(E/f'migration_{kind}_v002.json',dict(before=before,after=after,preserved=before==after,shared_revision='v001 0.45mm arc radius to v002 0.495mm; no other prototype geometry/behavior change'))
 print('CONSUMER',kind,events,flush=True)

if __name__=='__main__':
 args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['build']
 if args[0]=='build':
  for version,width in [('v001',.00045),('v002',.000495)]:
   if not (DEST/f'Acoustics_{version}.blend').exists():master(version,width)
  consumer('A');consumer('B')
