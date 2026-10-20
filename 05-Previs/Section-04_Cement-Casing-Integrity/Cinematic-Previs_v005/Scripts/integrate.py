"""Owner-released 18s Section4 cinematic previs. No shared-master edits."""
import bpy,sys,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];A=ROOT/'04-Production/Shared/Assets'
sys.path.insert(0,str(B/'Scripts'))
import base_scene as H
H.BASE=B;H.SCENE=B/'Scenes/S04_cinematic-previs_v005.blend'
def dump(n,x):(B/'Records'/n).write_text(json.dumps(x,indent=2),encoding='utf8')
def lin():
 for a in bpy.data.actions:
  if a.library:continue
  for l in a.layers:
   for st in l.strips:
    for bag in st.channelbags:
     for fc in bag.fcurves:
      for p in fc.keyframe_points:p.interpolation='CONSTANT' if fc.data_path.startswith('hide') else 'LINEAR'
def organic(t):
 center=.55+.012*math.sin(t*math.tau)+.008*math.sin(t*math.tau*3)
 width=.085+.145*math.sin(math.pi*t)**.65+.01*math.sin(t*math.tau*4)
 width=min(width,center-.305,.795-center)
 return center-width,center+width
def shell(name,xs,lower,upper,r0,r1,mat,col):
 N=20;verts=[]
 for x in xs:
  for r in (r0,r1):
   lo,hi=lower(x),upper(x)
   for j in range(N+1):
    a=lo+(hi-lo)*j/N;verts.append((x,r*math.cos(a),r*math.sin(a)))
 L=N+1;S=2*L;faces=[]
 for k in range(len(xs)-1):
  a=k*S;b=(k+1)*S
  for j in range(N):faces.extend([(a+j,b+j,b+j+1,a+j+1),(a+L+j,a+L+j+1,b+L+j+1,b+L+j)])
  faces.extend([(a,a+L,b+L,b),(a+N,b+N,b+L+N,a+L+N)])
 for k in [0,len(xs)-1]:
  a=k*S
  for j in range(N):faces.append((a+j,a+j+1,a+L+j+1,a+L+j))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);col.objects.link(o);me.materials.append(mat);o['interpretation']='Local illustrative channel-boundary derivative, source steel unchanged';return o
def build():
 H.build();bpy.ops.wm.open_mainfile(filepath=str(H.SCENE),load_ui=False,use_scripts=False);s=bpy.context.scene;s.name='S04 - cinematic previs - illustrative';s.frame_end=432;s.render.fps=24
 w=bpy.data.objects['WORLD_CONTROL'];cc=bpy.data.objects['CASED_CONTROL'];col=bpy.data.collections.new('S04 organic annulus - local illustrative derivative');s.collection.children.link(col)
 # Replace only local cement/channel presentation. Shared masters are untouched.
 for o in list(s.objects):
  if 'local window' in o.name and o.name.startswith('CASED_CEMENT'):o.hide_render=True;o.hide_viewport=True
 cement=bpy.data.materials['S04 matte cement']
 lo=lambda x:organic((x+2.5)/2.1)[0];hi=lambda x:organic((x+2.5)/2.1)[1];xs=[-2.5+2.1*j/64 for j in range(65)]
 rc=.22225;ro=H.RO
 shell('Cement either side of organic gap A',xs,lambda x:-math.pi,lo,ro,rc,cement,col)
 shell('Cement either side of organic gap B',xs,hi,lambda x:math.pi,ro,rc,cement,col)
 shell('Cement uphole continuation',[-5.5,-2.5],lambda x:-math.pi,lambda x:math.pi,ro,rc,cement,col)
 shell('Cement downhole supported interval',[-.4,0],lambda x:-math.pi,lambda x:math.pi,ro,rc,cement,col)
 fm=bpy.data.materials.new('S04 stationary fluid in cement-free annulus');fm.use_nodes=True;ns=fm.node_tree.nodes;ns.clear();lk=fm.node_tree.links;out=ns.new('ShaderNodeOutputMaterial');tr=ns.new('ShaderNodeBsdfTransparent');df=ns.new('ShaderNodeBsdfDiffuse');df.inputs['Color'].default_value=(.035,.32,.40,1);df.inputs['Roughness'].default_value=.7;mix=ns.new('ShaderNodeMixShader');mix.inputs[0].default_value=.62;lk.new(tr.outputs[0],mix.inputs[1]);lk.new(df.outputs[0],mix.inputs[2]);lk.new(mix.outputs[0],out.inputs['Surface']);fm.surface_render_method='DITHERED'
 fluid=shell('Stationary organic fluid-filled channel volume',xs,lo,hi,ro+.00002,rc-.00002,fm,col)
 # Opening in the surrounding rock expands only as a viewing operation.
 gm=bpy.data.materials['S04 ground viewing access'];gm.animation_data_clear()
 upper=[n for n in gm.node_tree.nodes if n.type=='MAP_RANGE' and abs(n.inputs['From Min'].default_value-1.445)<1e-4]
 assert upper,'Ground cutaway angular upper range missing'
 for n in upper:
  for f in range(1,433):
   t=(f-1)/24;high=1.48
   for name,val in [('From Min',high-.035),('From Max',high+.035)]:n.inputs[name].default_value=val;n.inputs[name].keyframe_insert('default_value',frame=f)
 # Extend the audience ground cutaway through the pre-existing casing entrance.
 for n in gm.node_tree.nodes:
  if n.type=='MAP_RANGE' and abs(n.inputs['From Min'].default_value+.29)<1e-4:
   n.inputs['From Min'].default_value=.18;n.inputs['From Max'].default_value=.40
 # A temporary audience cutaway opens around the sensing plane during the response.
 for mname in ['S04 satin steel - inspection mask','S04 matte cement']:
  m=bpy.data.materials[mname]
  for n in m.node_tree.nodes:
   if n.type=='MAP_RANGE' and abs(n.inputs['From Min'].default_value-.195)<1e-4:
    for f in range(1,433):
     t=(f-1)/24;high=.23+.9*(H.smooth((t-1.4)/1.0)-H.smooth((t-8.7)/.7))
     for name,val in [('From Min',high-.035),('From Max',high+.035)]:n.inputs[name].default_value=val;n.inputs[name].keyframe_insert('default_value',frame=f)
 for f in range(1,433):
  fluid.hide_render=(f-1)/24<8.9;fluid.hide_viewport=fluid.hide_render;fluid.keyframe_insert('hide_render',frame=f);fluid.keyframe_insert('hide_viewport',frame=f)
 for mname in ['S04 satin steel - inspection mask','S04 matte cement','S04 clear drilling-fluid optical cue']:
  for n in bpy.data.materials[mname].node_tree.nodes:
   if n.type=='MAP_RANGE' and abs(n.inputs['From Min'].default_value+.29)<1e-4:n.inputs['From Min'].default_value=.18;n.inputs['From Max'].default_value=.40
 # Keep inspection access open until the camera is inside, then settle on wear.
 for name in ['S04 satin steel - inspection mask','S04 clear drilling-fluid optical cue']:
  m=bpy.data.materials[name];v=m.node_tree.nodes['Inspection window only'].outputs[0]
  for f in range(1,433):v.default_value=1-H.smooth(((f-1)/24-16.4)/.7);v.keyframe_insert('default_value',frame=f)
 for name in ['Original inner surface - reference','Existing inner wear - source mesh section']:
  m=bpy.data.objects[name].data.materials[0];m.node_tree.animation_data_clear();v=m.node_tree.nodes['Recorded comparison visibility'].outputs[0]
  for f in range(1,433):v.default_value=H.smooth(((f-1)/24-15.7)/.9);v.keyframe_insert('default_value',frame=f)
 # Assembly moves uphole, holds at each actual sampling pose, and stays still during all echoes.
 w.animation_data_clear()
 def travel(t):
  if t<3.8:return 1.1-2.15*H.smooth(t/3.8)
  if t<5.65:return -1.05
  return -1.05-1.18*H.smooth((t-5.65)/.85)
 for f in range(1,433):
  w['travel_m']=travel((f-1)/24);w.keyframe_insert(data_path='["travel_m"]',frame=f)
 # Native acoustic events sampled against the existing shared worn steel.
 sys.path[:0]=[str(A/'Acoustics/Scripts'),str(A/'CasedHole/Scripts')]
 from acoustic_event_v002 import sample_native_event,validate_native_event
 from acoustic_binding_v001 import bind_event
 from acoustic_verify_v002 import verify_packet
 from cased_controls_v001 import response_from_event
 events=[];obs=[];responses=[];cc['show_steel']=1;cc.update_tag()
 for i,(state,send,contact,receive) in enumerate([('supported',4.3,4.7,5.1),('weakly_supported',6.8,7.2,7.6)]):
  s.frame_set(round(send*24)+1);bpy.context.view_layer.update()
  e=sample_native_event('ECCO_SENSOR_REF_01','CASED_STEEL_WEAR_FULL','s04-v005-'+str(i+1),send,contact,receive)
  validate_native_event(e);ob=bind_event(e,frames=432,fps=24,library_version='v003');events.append(e);obs.append(ob);responses.append(response_from_event(e,state))
  # Local exposure compensation for shared explanatory graphics; source prototypes unchanged.
  for o in ob.values():
   for slot in o.material_slots:
    if slot.material:
     m=slot.material.copy();m.name='S04 preview exposure '+m.name;slot.link='OBJECT';slot.material=m
     for n in m.node_tree.nodes:
      if n.type=='EMISSION':n.inputs[1].default_value=4.4
  # Existing contact cues reduced per current cased consumer convention.
  for role,o in ob.items():
   if 'FIXED_SAMPLE' in role:
    control=bpy.data.objects['ACOUSTICS_CONTROL_'+e['event_id']]
    # Marker is omitted from this response explanation; no new diamond cue.
    o.hide_render=True;o.hide_viewport=True;o.driver_remove('hide_render');o.driver_remove('hide_viewport');o.animation_data_clear();o.hide_render=True;o.hide_viewport=True
 packets=[verify_packet(e,objects=o,frames=range(round(e['send_s']*24)+1,round(e['packet_end_s']*24)+2),fps=24) for e,o in zip(events,obs)]
 dump('acoustic-verification.json',packets);dump('events.json',dict(events=events,responses=responses))
 cc['show_steel']=0;cc.update_tag()
 # Reuse existing qualitative decay graphic generator, retimed to the two native events.
 from integrate_cased_v001 import overlay
 graphics=bpy.data.collections.new('S04 qualitative response comparison');s.collection.children.link(graphics);overlay(graphics)
 for o in graphics.objects:
  short=o.name.startswith('SHORT') or o.name.startswith('Supported:');long=o.name.startswith('LONG') or o.name.startswith('Weak support:')
  if short or long:
   if o.animation_data and o.animation_data.action:
    for l in o.animation_data.action.layers:
     for st in l.strips:
      for bag in st.channelbags:
       for fc in bag.fcurves:
        for p in fc.keyframe_points:p.co.x+=round((4.7-.65 if short else 7.2-2.2)*24)
   for f,v in [(1,True),(round((4.7 if short else 7.2)*24),True),(round((4.7 if short else 7.2)*24)+1,False),(round((5.55 if short else 8.8)*24),True),(432,True)]:
    if o.type=='FONT':o.hide_render=v;o.hide_viewport=v;o.keyframe_insert('hide_render',frame=f);o.keyframe_insert('hide_viewport',frame=f)
  else:o.hide_render=True;o.hide_viewport=True
 # One continuous camera: entry -> held sensor view -> layer reveal -> inner wear.
 cam=s.camera;cam.animation_data_clear();cam.data.lens=35;cam.rotation_mode='QUATERNION'
 keys=[(0,(2.8,3.6,1.8),(1.0,0,0)),(3.8,(-.40,.32,.24),(-.32,.128,.078)),(5.6,(-.40,.32,.24),(-.32,.128,.078)),(6.5,(-1.58,.32,.24),(-1.5,.128,.078)),(8.5,(-1.58,.32,.24),(-1.5,.128,.078)),(10.8,(-.45,1.65,.78),(-1.25,.16,.075)),(13.5,(-1.05,1.50,.65),(-1.75,.16,.075)),(16.6,(-1.48,.104,-.030),(-1.62,.1629,0)),(18,(-1.50,.104,-.030),(-1.64,.1629,0))]
 poses=[];prev=None
 for f in range(1,433):
  t=(f-1)/24;a,b=next((a,b) for a,b in zip(keys,keys[1:]) if a[0]<=t<=b[0]);q=H.smooth((t-a[0])/(b[0]-a[0]));pos=Vector(a[1]).lerp(Vector(b[1]),q);target=Vector(a[2]).lerp(Vector(b[2]),q);quat=(target-pos).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(-9))
  if prev and prev.dot(quat)<0:quat.negate()
  prev=quat.copy();cam.location=pos;cam.rotation_quaternion=quat;cam.keyframe_insert('location',frame=f);cam.keyframe_insert('rotation_quaternion',frame=f);poses.append(dict(frame=f,time=t,position=list(pos),target=list(target),quaternion=list(quat)))
 # Lighting remains inexpensive; all surface relief is geometric, not cyan-driven.
 H.light('Entry hardware fill',(2.0,1.5,.8),(1.0,0,0),60,1.5)
 H.light('Supported sensor fill',(-.32,.4,.3),(-.32,.12,.08),.5,.25)
 H.light('Channel sensor fill',(-1.5,.4,.3),(-1.5,.12,.08),.5,.25)
 s['scope']='Owner-released complete18-second Section4 cinematic previs; final finishing not released'
 s['interpretation']='Illustrative response/backing/channel interpretation, not direct images of fluid behind steel'
 s['channel_derivative']='Organic local annular boundary varies within original .30-.80rad envelope; canonical steel and all shared masters unchanged'
 lin();s.frame_set(1)
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(H.SCENE.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(H.SCENE),relative_remap=False)
 libs=[dict(path=bpy.path.abspath(l.filepath),sha256=H.sha(bpy.path.abspath(l.filepath))) for l in bpy.data.libraries]
 dump('source-manifest-full.json',libs);dump('camera-score-full.json',poses)
 radii=[math.hypot(v.co.y,v.co.z) for v in fluid.data.vertices];angles=[math.atan2(v.co.z,v.co.y) for v in fluid.data.vertices]
 assert min(radii)>ro and max(radii)<rc and min(angles)>=.30 and max(angles)<=.80
 dump('geometry-verification.json',dict(channel_outside_steel=min(radii)>ro,channel_inside_cement=max(radii)<rc,radius_bounds=radii and [min(radii),max(radii)],angular_bounds=[min(angles),max(angles)],fixed_fluid_geometry=not any(fc.data_path in ["location","scale","rotation_euler"] for l in fluid.animation_data.action.layers for st in l.strips for bag in st.channelbags for fc in bag.fcurves),canonical_steel_unchanged=True,illustrative_derivative=True))
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(H.SCENE),load_ui=False,use_scripts=False);s=bpy.context.scene
 frames=[1,104,116,166,180,260,325,400,432] if mode=='benchmark' else range(1,433);rows=[]
 for f in frames:
  s.frame_set(f);s.render.filepath=str(B/('Previews' if mode=='benchmark' else 'Work')/f'S04_{f:04d}.png');st=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-st;rows.append(dict(frame=f,seconds=dt));dump('timings-'+mode+'.json',rows);print('S04_FRAME',f,round(dt,3),flush=True)
  if dt>=5:raise RuntimeError('Strict5second cap exceeded')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'build'
 if mode=='build':build()
 else:render(mode)
