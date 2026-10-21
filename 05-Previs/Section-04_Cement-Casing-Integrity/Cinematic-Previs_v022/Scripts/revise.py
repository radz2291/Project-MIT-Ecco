import bpy,math,json,time,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix,Quaternion
from bpy_extras.object_utils import world_to_camera_view
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];P=B.parent
SRC=P/'Composition-Stills_v021/Scenes/S04_approval-stills_v021.blend'
OUT=B/'Scenes/S04_continuous-camera_v022.blend'
PHI=math.radians(39);FACTOR=3.5
def dump(n,v):(B/'Records'/n).write_text(json.dumps(v,indent=2))
def sm(t):
 t=max(0,min(1,t));return t*t*t*(t*(6*t-15)+10)
def curves(action):
 for l in action.layers:
  for st in l.strips:
   for bag in st.channelbags:yield from bag.fcurves
def graphic(n):return n.startswith(('STEEL-ATTACHED resonance band','STEEL THICKNESS response','STEEL-BOUND acquisition segment','S02 sourced','Casing response tail'))
def geo(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH' and not graphic(o.name)}
def quat(pos,target,roll):
 f=(target-pos).normalized();a=Vector((1,0,0));right=(a-f*a.dot(f)).normalized();up=(-f).cross(right).normalized();return Matrix((right,up,-f)).transposed().to_quaternion()@Quaternion((0,0,1),math.radians(roll))
def build():
 bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='S04 continuous A B C D v022';before=geo(s)
 cam=bpy.data.objects[s['source_camera']];s.camera=cam
 for o in list(s.objects):
  if o.name.startswith('Approval still '):bpy.data.objects.remove(o,do_unlink=True)
 # Enlarge explanatory footprint, never radial steel thickness or physical geometry.
 changed=[];data_seen=set();radial_error=0
 for o in s.objects:
  if not graphic(o.name):continue
  if o.data in data_seen:o.data=o.data.copy()
  data_seen.add(o.data)
  if o.type=='CURVE':
   for sp in o.data.splines:
    for p in sp.points:p.co.x*=FACTOR
    for p in sp.bezier_points:
     p.co.x*=FACTOR;p.handle_left.x*=FACTOR;p.handle_right.x*=FACTOR
   o.data.bevel_depth*=1.7
  elif o.type=='MESH':
   xc=-1.5 if sum(v.co.x for v in o.data.vertices)/len(o.data.vertices)<-.9 else -.31999993324279785
   for v in o.data.vertices:
    p=v.co;r=math.hypot(p.y,p.z);a=math.atan2(p.z,p.y);d=(a-PHI+math.pi)%(2*math.pi)-math.pi
    p.x=xc+FACTOR*(p.x-xc)
    # Surface footprints expand around the same cylindrical wall; exposed
    # thickness faces remain at the section plane and retain true thickness.
    if abs(d)>.003:
     a=PHI+FACTOR*d;p.y=r*math.cos(a);p.z=r*math.sin(a)
    radial_error=max(radial_error,abs(math.hypot(p.y,p.z)-r))
   o.data.update()
  o['v022_display_footprint_multiplier']=FACTOR;changed.append(o.name)
 # Original fixed computed field, source contours and event envelopes retained.
 steel=bpy.data.objects['STEEL - capped true source section'];depth=[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]
 nt=steel.data.materials[0].node_tree;nt.nodes['Still review - data display enabled'].outputs[0].default_value=1
 col=bpy.data.collections['D measurement graphics - still-review visibility'];col.hide_render=False;col.hide_viewport=False
 grazing=bpy.data.objects['D physical wear grazing light - still proposal'];grazing.hide_render=False;grazing.hide_viewport=False
 # Existing v020 journey, with v021 lens scale and a left-third D arrival.
 score=json.loads((P/'Cinematic-Previs_v020/Records/camera-score.json').read_text())
 cam.animation_data_clear();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION'
 deye=Vector((-1.05,.055,.065));dtar=Vector((-1.70,.160,-.015));dq=quat(deye,dtar,-10)
 cam.location=deye;cam.rotation_quaternion=dq;cam.data.lens=38;cam.data.shift_x=0;cam.data.shift_y=0;bpy.context.view_layer.update()
 patch=Vector((-1.70,.162,0));q0=world_to_camera_view(s,cam,patch);cam.data.shift_x=.1;bpy.context.view_layer.update();q1=world_to_camera_view(s,cam,patch)
 dshift=(1/3-q0.x)/((q1.x-q0.x)/.1);cam.data.shift_x=dshift;bpy.context.view_layer.update()
 final_projection=list(world_to_camera_view(s,cam,patch));previous=None;actual=[]
 # Retain ECCO beside the wear: the bit is not the detecting instrument.
 # Scan three existing axial profiles while the active sensor faces the worn
 # inner wall. Geometry and computed values stay fixed; only acquisition is exposed.
 world=bpy.data.objects['WORLD_CONTROL'];world.animation_data_clear()
 # Local collection branch only: ghost surrounding ECCO housing in D while
 # preserving the real source mesh and a solid region around the sensor port.
 localhousing=None
 def contains(col):return any(o.name=='ECCO_HOUSING_SOURCE_MESH' or (o.instance_collection and contains(o.instance_collection)) for o in col.all_objects)
 def clone_branch(col):
  nonlocal localhousing
  has=contains(col)
  if not has:return col
  new=bpy.data.collections.new(col.name+' v022 local display')
  for o in col.objects:
   if o.name=='ECCO_HOUSING_SOURCE_MESH':
    localhousing=o.copy();localhousing.data=o.data.copy();localhousing.name='ECCO unchanged source housing - D technical transparency';new.objects.link(localhousing)
   elif o.instance_collection and contains(o.instance_collection):
    cp=o.copy();cp.instance_collection=clone_branch(o.instance_collection);new.objects.link(cp)
   else:new.objects.link(o)
  for child in col.children:new.children.link(clone_branch(child))
  return new
 inst=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];inst.instance_collection=clone_branch(inst.instance_collection)
 # Collection instances may hold the housing in a nested object instance.
 if localhousing is None:
  raise RuntimeError('Housing branch not found for local display override')
 oldmat=localhousing.data.materials[0];ghost=oldmat.copy();ghost.name='ECCO D explanatory transparent housing';gn=ghost.node_tree;gout=next(n for n in gn.nodes if n.type=='OUTPUT_MATERIAL');source= gout.inputs['Surface'].links[0].from_socket
 tr=gn.nodes.new('ShaderNodeBsdfTransparent');gmix=gn.nodes.new('ShaderNodeMixShader');opacity=gn.nodes.new('ShaderNodeValue');opacity.name='Housing opacity - sensor remains solid';gn.links.new(tr.outputs[0],gmix.inputs[1]);gn.links.new(source,gmix.inputs[2]);gn.links.new(opacity.outputs[0],gmix.inputs[0]);gn.links.new(gmix.outputs[0],gout.inputs['Surface'])
 ghost.surface_render_method='BLENDED';ghost.use_transparency_overlap=False
 localhousing.data.materials[0]=ghost;localhousing.data.materials.append(oldmat)
 port=Vector((.730000019,.100251831,.081182331));portfaces=0
 for p in localhousing.data.polygons:
  if (localhousing.matrix_world@p.center-port).length<.038:p.material_index=len(localhousing.data.materials)-1;portfaces+=1
 assert portfaces>0
 expose=nt.nodes['Expose fixed recorded depth'];nt.animation_data_clear()
 pos=nt.nodes.new('ShaderNodeNewGeometry');sep=nt.nodes.new('ShaderNodeSeparateXYZ');nt.links.new(pos.outputs['Position'],sep.inputs[0])
 front=nt.nodes.new('ShaderNodeValue');front.name='ECCO axial acquisition front'
 passed=nt.nodes.new('ShaderNodeMath');passed.operation='GREATER_THAN';nt.links.new(sep.outputs['X'],passed.inputs[0]);nt.links.new(front.outputs[0],passed.inputs[1])
 startmask=nt.nodes.new('ShaderNodeMath');startmask.operation='LESS_THAN';nt.links.new(sep.outputs['X'],startmask.inputs[0]);startmask.inputs[1].default_value=-1.499
 both=nt.nodes.new('ShaderNodeMath');both.operation='MULTIPLY';nt.links.new(passed.outputs[0],both.inputs[0]);nt.links.new(startmask.outputs[0],both.inputs[1])
 mix=nt.nodes['Mix Shader'];oldfac=mix.inputs[0].links[0].from_socket;gate=nt.nodes.new('ShaderNodeMath');gate.operation='MULTIPLY';nt.links.new(oldfac,gate.inputs[0]);nt.links.new(both.outputs[0],gate.inputs[1]);nt.links.new(gate.outputs[0],mix.inputs[0])
 profiles=[o for o in s.objects if o.type=='CURVE' and o.name.startswith('Station ')]
 for o in profiles:o.animation_data_clear()
 tree=BVHTree.FromPolygons([steel.matrix_world@v.co for v in steel.data.vertices],[tuple(p.vertices) for p in steel.data.polygons])
 dwaves=[]
 for kind,color in [('SEND',(.06,.85,1,1)),('ECHO',(.10,.85,.58,1))]:
  template=bpy.data.objects['S02 sourced '+kind+' front 0']
  for i in range(3):
   o=bpy.data.objects.new('D sensor '+kind+' '+str(i),template.data.copy());s.collection.objects.link(o)
   m=bpy.data.materials.new(o.name+' display');m.diffuse_color=color;m.use_nodes=True;n=m.node_tree;n.nodes.clear();out=n.nodes.new('ShaderNodeOutputMaterial');em=n.nodes.new('ShaderNodeEmission');em.inputs[0].default_value=color;em.inputs[1].default_value=.8;n.links.new(em.outputs[0],out.inputs['Surface']);o.data.materials.clear();o.data.materials.append(m);o.rotation_euler.x=-PHI;dwaves.append((kind,i,o))
 sensorrows=[]
 key=bpy.data.objects['Wide sectional softbox'];fill=bpy.data.objects['Uphole fill']
 key.data.animation_data_clear();fill.data.animation_data_clear();grazing.data.animation_data_clear()
 for frame in range(1,433):
  old=score[frame-1];pos=Vector(old['eye_m']);tar=Vector(old['target_m']);roll=old['roll_degrees'];lens=old['lens_mm'];shift=0
  if frame<=63:roll=25+(-18-25)*sm((frame-1)/62);lens=32+(65-32)*sm((frame-1)/62)
  elif frame<=261:lens=65
  else:
   u=sm((frame-261)/57);start=score[260];endeye=deye;endtar=dtar
   waypoint=Vector((-1.24,0,0))+Vector((0,math.cos(PHI),math.sin(PHI)))*.148+Vector((0,-math.sin(PHI),math.cos(PHI)))*.025
   if frame<=290:pos=Vector(start['eye_m']).lerp(waypoint,sm((frame-261)/29))
   else:pos=waypoint.lerp(endeye,sm((frame-290)/28)) if frame<318 else endeye
   tar=Vector(start['target_m']).lerp(endtar,u);roll=-18+8*u;lens=65+(38-65)*u;shift=dshift*u
  q=quat(pos,tar,roll)
  if previous and previous.dot(q)<0:q.negate()
  previous=q.copy();cam.location=pos;cam.rotation_quaternion=q;cam.data.lens=lens;cam.data.shift_x=shift;cam.data.shift_y=0
  cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_quaternion',frame=frame);cam.data.keyframe_insert('lens',frame=frame);cam.data.keyframe_insert('shift_x',frame=frame)
  a=sm((frame-40)/23);d=sm((frame-261)/57);key.data.energy=22+(12-22)*a;fill.data.energy=8+(.7-8)*d;grazing.data.energy=.45*d
  for ob in [key,fill,grazing]:ob.data.keyframe_insert('energy',frame=frame)
  oldmotion=[(1,.25),(63,-1.05),(141,-1.05),(175,-2.23),(261,-2.23)]
  if frame<=261:
   ma,mb=next(((a,b) for a,b in zip(oldmotion,oldmotion[1:]) if a[0]<=frame<=b[0]),(oldmotion[-2],oldmotion[-1]));u=sm((frame-ma[0])/(mb[0]-ma[0]));travel=ma[1]+(mb[1]-ma[1])*u
  else:travel=-2.23-.45*sm((frame-318)/97)
  rot=-PHI*sm((frame-261)/39);world['travel_m']=travel;world['rotation_rad']=rot;world.keyframe_insert(data_path='["travel_m"]',frame=frame);world.keyframe_insert(data_path='["rotation_rad"]',frame=frame)
  sx=travel+.7300000190734863;front.outputs[0].default_value=sx;front.outputs[0].keyframe_insert('default_value',frame=frame)
  expose.outputs[0].default_value=.35*sm((frame-318)/10);expose.outputs[0].keyframe_insert('default_value',frame=frame)
  opacity.outputs[0].default_value=1-.88*sm((frame-261)/39);opacity.outputs[0].keyframe_insert('default_value',frame=frame)
  for o in profiles:
   coords=[p.co.x for sp in o.data.splines for p in sp.points];px=sum(coords)/len(coords)
   o.hide_render=frame<318 or px<sx or px<-2.0;o.hide_viewport=o.hide_render;o.keyframe_insert('hide_render',frame=frame);o.keyframe_insert('hide_viewport',frame=frame)
  emitter=Vector((sx,.129,0));hit=tree.ray_cast(emitter,Vector((0,1,0)),.1)[0]
  if frame>=300:assert hit is not None
  for kind,i,o in dwaves:
   active=False;v=0
   for begin in [318,350,382]:
    p=frame-begin-i
    if 0<=p<=15:
     active=(p<=7 if kind=='SEND' else p>=8);v=p/7 if kind=='SEND' else (p-8)/7
     if active:break
   o.hide_render=not active;o.hide_viewport=not active
   o.location=emitter.lerp(hit if hit else emitter,max(0,min(1,v if kind=='SEND' else 1-v)))
   o.scale=(1,1,1) if active else (0,0,0)
   for path in ['location','scale','hide_render','hide_viewport']:o.keyframe_insert(path,frame=frame)
  if frame in [302,330,350,380,400,415]:sensorrows.append({'frame':frame,'sensor_x_m':sx,'tool_rotation_rad':rot,'ray_hit_m':list(hit) if hit else None,'wall_radial_range_m':hit.y if hit else None})
  actual.append({'frame':frame,'eye_m':list(pos),'target_m':list(tar),'lens_mm':lens,'roll_degrees':roll,'shift_x':shift})
 for ob in [cam,cam.data,key.data,fill.data,grazing.data,world,nt,gn]+profiles+[o for k,i,o in dwaves]:
  for f in curves(ob.animation_data.action):
   for k in f.keyframe_points:k.interpolation='CONSTANT' if f.data_path.startswith('hide') else 'LINEAR'
 assert before==geo(s)
 s['scope']='Owner released full 18second render after v021: effect footprint3.5x, D graphics on left third, continuous camera, fixed half cutaway, unchanged physical geometry and computed wear.'
 s['display_limits']='Enlarged illustrative wavefront width and casing-bound reaction footprint; not physical wave amplitude, penetration depth, calibrated time or field data.'
 s.frame_start=1;s.frame_end=432;s.render.fps=24;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.compression=10
 s.frame_set(85)
 for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(OUT.parent))
 for w in bpy.context.window_manager.windows:
  w.scene=s
  for a in w.screen.areas:
   if a.type=='VIEW_3D':a.spaces.active.region_3d.view_perspective='CAMERA'
 bpy.ops.wm.save_as_mainfile(filepath=str(OUT),relative_remap=False)
 dump('build.json',{'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'native':str(OUT),'physical_meshes_unchanged':True,'physical_hashes':before,'effect_footprint_scale':FACTOR,'wavefront_stroke_scale':1.7,'enlarged_graphic_count':len(changed),'maximum_effect_radial_error_m':radial_error,'computed_maximum_wear_mm':1000*max(depth),'D_patch_center_projection':final_projection,'D_shift_x':dshift,'source_event_timing_preserved':True,'one_continuous_camera':cam.name,'fixed_half_section':True})
 dump('camera-score.json',actual)
 dump('D-sensor-acquisition.json',{'sensor':'ECCO_SENSOR_REF_01','scan_starts_at_frame':318,'rotation_degrees':-39,'axial_scan_m':[-1.5,-1.95],'samples':sensorrows,'housing_display':'Local non-destructive material override transitions to12percent opacity during D; solid source material retained within38mm of sensor reference. No well cutaway animation.','solid_sensor_region_faces':portfaces,'method':'Display follows actual tool axial position; illustrative pulses intersect unchanged inner steel. Fixed computed geometry field exposed behind sensor only in selected deeper scan region. No calibrated wear measurement or wall-thickness claim.'})
def render(mode):
 bpy.ops.wm.open_mainfile(filepath=str(OUT),use_scripts=False,load_ui=False);s=bpy.context.scene;rows=[]
 frames=[1,40,78,85,94,104,158,190,197,206,216,290,318,350,400,432] if mode=='bench' else range(1,433)
 if mode=='resume':
  prior=json.loads((B/'Records/timings-render.json').read_text());rows=[r for r in prior if r['frame']<=261];frames=range(max(r['frame'] for r in rows)+1,433)
 if mode!='bench':assert max(r['seconds'] for r in json.loads((B/'Records/timings-bench.json').read_text()))<5
 for f in frames:
  s.frame_set(f);s.render.filepath=str(B/('Previews' if mode=='bench' else 'Work/Frames')/f'S04_{f:04d}.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;rows.append({'frame':f,'seconds':dt});dump('timings-'+('render' if mode=='resume' else mode)+'.json',rows);print('FRAME',f,dt,flush=True)
  if dt>=5:raise RuntimeError('Frame time budget exceeded')
if __name__=='__main__':
 mode=sys.argv[sys.argv.index('--')+1]
 if mode=='build':build()
 else:render(mode)
