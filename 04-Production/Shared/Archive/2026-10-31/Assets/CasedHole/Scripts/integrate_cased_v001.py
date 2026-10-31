"""T47 cased-native event integration and bounded inspection/demo cameras.

Preserves all previous candidates. Build mode has no renders. Render mode must
be granted by T45 master; whole render-to-file cap is checked before continuing.
"""
import bpy,sys,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence';P=T/'Previews/v003';P.mkdir(exist_ok=True,parents=True)
sys.path.insert(0,str(A/'CasedHole/Scripts'));sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_event_v001 import sample_native_event,validate_event
from acoustic_binding_v001 import bind_event
from cased_controls_v001 import add_response,response_from_event
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def rel(p):return p.relative_to(ROOT).as_posix()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
def save(p):
 assert not p.exists(),p
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
def aim(pos,target,lens):
 cam=bpy.context.scene.camera;cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens;cam.data.clip_start=.003
def lights(scale=.4):
 for o in bpy.data.objects:
  if not o.library and o.type=='LIGHT':o.data.energy*=scale;o.data.size*=1.3
def overlay(col):
 s=bpy.context.scene;cam=s.camera;depth=.006;corners=cam.data.view_frame(scene=s);hw=max(abs(p.x/p.z*depth) for p in corners);hh=max(abs(p.y/p.z*depth) for p in corners)
 def point(x,y):return ((x-.5)*2*hw,(y-.5)*2*hh,-depth)
 m=bpy.data.materials.new('CASED_SCREEN_QUIET');m.use_nodes=True;ns=m.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');em=ns.new('ShaderNodeEmission');em.inputs[0].default_value=(.58,.75,.69,1);em.inputs[1].default_value=.9;m.node_tree.links.new(em.outputs[0],out.inputs[0])
 font=bpy.data.fonts.load('C:/Windows/Fonts/segoeui.ttf')
 rows=[('Supported: short decay',.28,.65,.45,True),('Weak support: long decay',.12,2.20,1.20,False)]
 for label,y,contact,duration,short in rows:
  d=bpy.data.curves.new('QUALITATIVE_RESPONSE_LABEL','FONT');d.body=label;d.font=font;d.size=.00012;o=bpy.data.objects.new(label,d);col.objects.link(o);o.parent=cam;o.location=point(.07,y+.047);d.materials.append(m)
  for i in range(22):
   d=bpy.data.curves.new('QUALITATIVE_DECAY_BAR','CURVE');d.dimensions='3D';d.bevel_depth=.0000025;sp=d.splines.new('POLY');sp.points.add(1);h=.017*math.exp(-i*(.24 if short else .065));x=.07+i*.014
   for p,q in zip(sp.points,[point(x,y-h),point(x,y+h)]):p.co=(*q,1)
   o=bpy.data.objects.new(('SHORT' if short else 'LONG')+'_DECAY_'+str(i),d);col.objects.link(o);o.parent=cam;d.materials.append(m)
   for f in range(1,s.frame_end+1):
    elapsed=(f-1)/24-contact;on=0<=elapsed<=duration and i/22*duration<=elapsed;o.hide_render=not on;o.keyframe_insert(data_path='hide_render',frame=f)
 d=bpy.data.curves.new('RESPONSE_PROVENANCE','FONT');d.body='Illustrative response / no calibrated values';d.font=font;d.size=.00008;o=bpy.data.objects.new(d.name,d);col.objects.link(o);o.parent=cam;o.location=point(.07,.035);d.materials.append(m)
def build():
 # New bounded inspection views; originals and failed readability evidence preserved.
 openfile(S/'CasedReuse_A_v002.blend');lights(.32);save(S/'CasedHardware_v003.blend')
 openfile(S/'CasedReuse_B_v002.blend');w=bpy.data.objects['WORLD_CONTROL'];w['show_formation']=0;w.update_tag();cc=bpy.data.objects['CASED_CONTROL'];cc['wear']=0;cc['show_reference']=0;cc.update_tag();aim((-.8,1.1,.78),(-1.4,.12,.05),50);lights(.25);save(S/'CasedChannel_v003.blend')
 openfile(S/'CasedReuse_B_v002.blend');cc=bpy.data.objects['CASED_CONTROL'];cc['channel']=0;cc['show_cement']=0;cc['show_reference']=1;cc.update_tag();w=bpy.data.objects['WORLD_CONTROL'];w['show_formation']=0;w.update_tag();aim((-2.13,-.09,.045),(-1.35,.156,.0),47);lights(.28);save(S/'CasedWear_v003.blend')
 # Later upward retrieval, physical axis/order preserved. Whole hardware moves.
 openfile(S/'CasedHardware_v003.blend');s=bpy.context.scene;s.frame_end=96;w=bpy.data.objects['WORLD_CONTROL'];w['show_open']=1;w['show_mud']=0;w['show_formation']=0;w.update_tag();aim((1.1,-5.7,3.1),(-.6,0,0),47)
 for f,v in [(1,.5),(96,-3.8)]:w['travel_m']=v;w.keyframe_insert(data_path='["travel_m"]',frame=f)
 for layer in w.animation_data.action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for fc in bag.fcurves:
     for k in fc.keyframe_points:k.interpolation='LINEAR'
 s['condition']='Later uphole retrieval toward negativeX. Casing exists before motion. ECCO leading mesh end crosses boundary before lower bit.';s.frame_set(1);save(S/'CasedRetrieval_v003.blend')
 # Real A-SENSING event sampled from this actual cased context; no open-hole relabel.
 openfile(S/'CasedHardware_v003.blend');s=bpy.context.scene;s.frame_end=96;s.frame_set(1);w=bpy.data.objects['WORLD_CONTROL'];w['travel_m']=-2.23;w['rotation_rad']=0;w.update_tag();bpy.context.view_layer.update();c=bpy.data.collections.new('LOCAL_CASED_RESPONSE');s.collection.children.link(c);events=[];responses=[]
 for k,state,send,contact,receive in [(1,'supported',.25,.65,1.05),(2,'weakly_supported',1.8,2.2,2.6)]:
  e=sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_NOMINAL_CUTAWAY','t47-cased-native-%02d'%k,send,contact,receive);validate_event(e);events.append(e);bind_event(e,c,96,24,'v002');responses.append(add_response(e,state,c))
 cc=bpy.data.objects['CASED_CONTROL']
 for f,v in [(1,0),(42,0),(43,1),(96,1)]:cc['channel']=v;cc.keyframe_insert(data_path='["channel"]',frame=f)
 overlay(c);s['event_provenance']='Actual T46 native ray intersection with linked T47 steel; immutable sampled points; timing illustrative.';s['response_limits']='Casing-local qualitative adapter only; no physical material vibration, bond strength, fluid classification or wall thickness result.';s.frame_set(1);save(S/'CasedSupport_v003.blend');dump(E/'actual-cased-events_v003.json',dict(contract='ecco-acoustic-event-v001',events=events,responses=responses,fixture_replaced=True,binding='A-SENSING acoustic_binding_v001.bind_event'))
 dump(E/'retrieval-order_v003.json',dict(travel_start_m=.5,travel_end_m=-3.8,frames=96,fps=24,leading_ecco_end_local_x=0,lower_bit_min_local_x=2.9,leading_ecco_entry_frame=1+95*.5/4.3,full_ecco_inside_frame=1+95*2.9/4.3,lower_bit_entry_frame=1+95*3.4/4.3,source_scale=1,limits='Authored longitudinal motion, no loaded passage/drift/connection or deployment certification'))
 verify()
def verify():
 rows=[]
 for name in ['Hardware','Channel','Wear','Retrieval','Support']:
  p=S/('Cased'+name+'_v003.blend');openfile(p);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();libs=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries];assert all(l['exists'] and l['path'].startswith('//') for l in libs)
  rows.append(dict(scene=rel(p),sha256=sha(p),libraries=libs,unit_scale=s.unit_settings.scale_length,camera=list(s.camera.location),timing=[s.frame_start,s.frame_end,s.render.fps],eccos=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in bpy.context.evaluated_depsgraph_get().object_instances)))
 dump(E/'integrated-native-verification_v003.json',rows)
def response_repair():
 openfile(S/'CasedSupport_v003.blend');events=json.loads((E/'actual-cased-events_v003.json').read_text())['events']
 for o in bpy.data.objects:
  if not o.library and o.name.startswith(('CASED_supported_RESPONSE_','CASED_weakly_supported_RESPONSE_')):
   e=next(e for e in events if e['event_id']==o['event_id']);o.location+=Vector(e['normal_world'])*.002
 save(S/'CasedSupport_v004.blend');dump(E/'response-placement-repair_v004.json',dict(source='CasedSupport_v003.blend',candidate='CasedSupport_v004.blend',repair='Contact-local response bars moved2mm toward fluid, from hit-normal1mm to hit+normal1mm. Acoustic event/prototypes/geometry/camera/timing unchanged.'))
def retrieval_fluid():
 openfile(S/'CasedRetrieval_v003.blend');w=bpy.data.objects['WORLD_CONTROL'];w['show_mud']=1;w.update_tag();save(S/'CasedRetrieval_v004.blend');dump(E/'retrieval-fluid_v004.json',dict(source='CasedRetrieval_v003.blend',candidate='CasedRetrieval_v004.blend',repair='Restored accepted static optical fluid in retrieval context; camera/timing/source-scale unchanged. Static optical approximation, no circulation claim.'))
def extra_light(name,pos,target,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.use_shadow=False;o=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def inspection_repair():
 openfile(S/'CasedChannel_v003.blend');aim((-.7,2.7,1.65),(-1.5,.12,.02),45);extra_light('EXTERIOR_CHANNEL_KEY',(-1.5,.95,.65),(-1.5,.16,.06),65,.65);save(S/'CasedChannel_v005.blend')
 openfile(S/'CasedWear_v003.blend');extra_light('INNER_GROOVE_KEY',(-1.9,-.06,.06),(-1.5,.16,0),7,.10);save(S/'CasedWearGraze_v005.blend')
 # Actual full native-mesh section: linear edge intersection at X=-1.5.
 openfile(S/'CasedWear_v003.blend');s=bpy.context.scene;w=bpy.data.objects['WORLD_CONTROL'];cc=bpy.data.objects['CASED_CONTROL']
 for k in ['show_hardware','show_open','show_formation','show_mud']:w[k]=0
 for k in ['show_steel','show_cement','show_channel','show_reference']:cc[k]=0
 w.update_tag();cc.update_tag();source=bpy.data.objects['CASED_STEEL_WEAR_FULL'];groups={}
 for v in source.data.vertices:
  r=math.hypot(v.co.y,v.co.z)
  if r>.169:continue
  a=math.atan2(v.co.z,v.co.y)%math.tau
  if a>math.tau-1e-5:a=0
  groups.setdefault(round(a,6),{})[round(v.co.x,6)]=r
 section=[]
 for a,byx in sorted(groups.items()):
  xs=sorted(byx);lo=max(x for x in xs if x<=-1.5);hi=min(x for x in xs if x>=-1.5);r=byx[lo] if hi==lo else byx[lo]+(byx[hi]-byx[lo])*(-1.5-lo)/(hi-lo);section.append((a,r))
 c=bpy.data.collections.new('DERIVED_NATIVE_SECTION');s.collection.children.link(c);m=bpy.data.materials.new('SECTION_STEEL');m.diffuse_color=(.25,.31,.34,1);m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.25,.31,.34,1);bs.inputs['Roughness'].default_value=.7
 verts=[]
 for a,r in section:verts.extend([(-1.5,r*math.cos(a),r*math.sin(a)),(-1.5,.1698625*math.cos(a),.1698625*math.sin(a))])
 faces=[(2*j,2*j+1,(2*((j+1)%len(section)))+1,2*((j+1)%len(section))) for j in range(len(section))];me=bpy.data.meshes.new('ACTUAL_SECTION_X_MINUS_1_5');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(me.name,me);c.objects.link(o);me.materials.append(m);o['source_mesh']=source.name;o['source_library']='CasedHole_v002.blend';o['derivation']='Actual longitudinal mesh-edge intersections atX-1.5; same metre scale, fixed outer contour, no depth exaggeration'
 for name,rgb,points in [('NOMINAL_INNER_REFERENCE',(.82,.86,.88),[(-1.5005,.1589405*math.cos(a),.1589405*math.sin(a)) for a,r in section]),('ACTUAL_PREEXISTING_INNER_EDGE',(.1,.65,.45),[(-1.501,r*math.cos(a),r*math.sin(a)) for a,r in section])]:
  mm=bpy.data.materials.new(name);mm.use_nodes=True;nodes=mm.node_tree.nodes;nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');em.inputs[0].default_value=(*rgb,1);em.inputs[1].default_value=.9;mm.node_tree.links.new(em.outputs[0],out.inputs[0]);d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=.00055;sp=d.splines.new('POLY');sp.points.add(len(points));
  for p,q in zip(sp.points,points+[points[0]]):p.co=(*q,1)
  ob=bpy.data.objects.new(name,d);c.objects.link(ob);d.materials.append(mm)
 cam=s.camera;aim((-2,0,0),(-1.5,0,0),50);cam.data.type='ORTHO';cam.data.ortho_scale=.43;extra_light('SECTION_LIGHT',(-2,-.2,.3),(-1.5,0,0),50,.5);save(S/'CasedWearSection_v005.blend');dump(E/'native-section_v005.json',dict(source_mesh=source.name,source_hash=sha(A/'CasedHole/CasedHole_v002.blend'),section_x_m=-1.5,nominal_radius_m=.1589405,outer_radius_m=.1698625,max_section_inner_radius_m=max(r for a,r in section),angular_samples=len(section),actual_geometry_scale=1,interpretation='Known authored pre-existing wear section; white nominal and emerald actual edge, no inferred measured metal loss/thickness.'))
def support_rebind():
 openfile(S/'CasedSupport_v004.blend');s=bpy.context.scene;s.frame_set(1);c=bpy.data.collections.get('LOCAL_CASED_RESPONSE')
 for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
 events=[];responses=[]
 for k,state,send,contact,receive in [(1,'supported',.25,.65,1.05),(2,'weakly_supported',1.8,2.2,2.6)]:
  e=sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_NOMINAL_CUTAWAY','t47-cased-native-%02d'%k,send,contact,receive);validate_event(e);events.append(e);bind_event(e,c,96,24,'v002');responses.append(add_response(e,state,c))
 e=events[0];source=Vector(e['emitter_world_m']);hit=Vector(e['hit_world_m']);radial=Vector(e['direction_world']);aim(source+Vector((.05,0,0))+radial*.020,(source+hit)/2,30);overlay(c);s.frame_set(1);save(S/'CasedSupport_v005.blend');dump(E/'actual-cased-events_v005.json',dict(contract='ecco-acoustic-event-v001',events=events,responses=responses,fixture_replaced=True,binding='A-SENSING public native-capface sample + bind_event',native_source_note='Inherited reference retained; emitter endpoint derives actual provisional removable cap, not engineering certification.'))
def thin_rebind():
 openfile(S/'CasedSupport_v005.blend');s=bpy.context.scene;s.frame_set(1);c=bpy.data.collections['LOCAL_CASED_RESPONSE'];before=dict(camera=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens,timing=[s.frame_start,s.frame_end,s.render.fps]);d=json.loads((E/'actual-cased-events_v005.json').read_text())
 for o in list(c.objects):bpy.data.objects.remove(o,do_unlink=True)
 for e,response in zip(d['events'],d['responses']):bind_event(e,c,96,24,'v003');add_response(e,response['support_state'],c)
 overlay(c);s.frame_set(1);after=dict(camera=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens,timing=[s.frame_start,s.frame_end,s.render.fps]);assert before==after;save(S/'CasedSupport_v006.blend');d['acoustic_library']='Acoustics_v003.blend';d['acoustic_library_sha256']=sha(A/'Acoustics/Acoustics_v003.blend');d['migration']='0.12mm thin arcs, circumferential fan orientation; cap events/camera/timing unchanged';dump(E/'actual-cased-events_v006.json',d);dump(E/'thin-binding-migration_v006.json',dict(before=before,after=after,preserved=True))
def render(mode):
 rows=[]
 cases=[('Hardware',[1]),('Channel',[1]),('Wear',[1]),('Retrieval',[1,48,96]),('Support',[1,18,56,76])] if mode=='benchmark' else [('Retrieval',range(1,97)),('Support',range(1,97))]
 if mode=='benchmark-independent':cases=cases[:0]+[('Hardware',[1]),('Channel',[1]),('Wear',[1]),('Retrieval',[1,48,96])]
 if mode=='benchmark-repaired':cases=[('Channel',[1]),('WearGraze',[1]),('WearSection',[1]),('Support',[1,18,56,76])]
 if mode=='benchmark-conditions':cases=[('Channel',[1]),('WearGraze',[1]),('WearSection',[1])]
 if mode=='benchmark-support':cases=[('Support',[1,12,18,56,76])]
 for name,frames in cases:
  ver='v006' if name=='Support' and (S/'CasedSupport_v006.blend').exists() else ('v005' if mode in ['benchmark-repaired','benchmark-conditions'] or (name=='Support' and (S/'CasedSupport_v005.blend').exists()) else ('v004' if name=='Retrieval' else 'v003'));p=S/('Cased'+name+'_'+ver+'.blend');openfile(p);s=bpy.context.scene
  for f in frames:
   s.frame_set(f);folder=(P/'Frames'/name) if mode=='demo' else P;folder.mkdir(exist_ok=True,parents=True);tag='v006' if mode=='benchmark-support' else ('v005' if mode in ['benchmark-repaired','benchmark-conditions'] else 'v003');out=folder/('Cased'+name+'_f%03d_'%f+tag+'.png');s.render.filepath=str(out);st=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-st;rows.append(dict(scene=rel(p),frame=f,seconds=dt,under_5=dt<5,output=rel(out)));dump(E/(mode+'_v003.json'),dict(samples=rows,settings=dict(engine='EEVEE',backend='VULKAN',resolution=[1280,720],samples=16,fps=24,compositor=False,color='AgX Medium High Contrast'),cache='Normal preexisting driver caches; no warmup render; T44 empty-cache initialization12.55–25.13s remains unresolved; process/file loading excluded.'))
   if dt>=5:raise RuntimeError('Render cap failed; stop before continuing')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'verify'
 if mode=='build':build()
 elif mode=='verify':verify()
 elif mode=='repair':response_repair()
 elif mode=='retrieval-fluid':retrieval_fluid()
 elif mode=='inspection-repair':inspection_repair()
 elif mode=='support-rebind':support_rebind()
 elif mode=='thin-rebind':thin_rebind()
 else:render(mode)
 print('T47_INTEGRATED_'+mode.upper()+'_COMPLETE',flush=True)
