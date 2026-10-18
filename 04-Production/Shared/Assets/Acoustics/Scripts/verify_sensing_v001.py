"""Fresh-open native verification, no rendering."""
import bpy,sys,json,math,hashlib
from pathlib import Path
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';S=T/'Scenes';sys.path.insert(0,str(HERE))
from acoustic_event_v001 import native_instance,wall_tree,validate_event,sample_native_event
checks=[];native=[]
def check(name,p,detail=None):checks.append(dict(name=name,passed=bool(p),detail=detail))
for kind in ['A','B']:
 path=S/f'Sensing_reuse_{kind}_v008.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene
 check('relative/resolved libraries '+kind,all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries))
 check('Acoustics v003 linked '+kind,any(Path(l.filepath).name=='Acoustics_v003.blend' for l in bpy.data.libraries))
 events=json.loads((E/f'events_{kind}_v002.json').read_text())['events']
 s.frame_set(1);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
 names=[i.object.original.name for i in deps.object_instances]
 check('single product '+kind,names.count('ECCO_HOUSING_SOURCE_MESH')==1)
 poses=[native_instance(f'ECCO_SENSOR_REF_{i:02d}')[1] for i in [1,2,3]]
 check('one sensor plane '+kind,max(m.translation.x for m in poses)-min(m.translation.x for m in poses)<1e-5)
 angles=sorted(math.atan2(m.translation.z,m.translation.y) for m in poses)
 gaps=[(angles[(i+1)%3]-angles[i])%math.tau for i in range(3)]
 check('120 degree references '+kind,max(abs(g-math.tau/3) for g in gaps)<1e-5,gaps)
 _,_,tree=wall_tree('IRREGULAR_CUTAWAY');max_penetration=0;max_sensor_error=0;max_envelope_penetration=0;min_face_margin=1;active_legs={'SEND':0,'RETURN':0}
 for e in events:
  check('event valid '+e['event_id'],validate_event(e))
  origin=Vector(e['emitter_world_m']);direction=Vector(e['direction_world']);hit=Vector(e['hit_world_m']);normal=Vector(e['normal_world'])
  actual=tree.ray_cast(origin,direction)[0];check('native first hit '+e['event_id'],(actual-hit).length<2e-6)
  # Inspect saved curve centerline vertices against first wall intersection each frame.
  for f in range(1,s.frame_end+1):
   s.frame_set(f);bpy.context.view_layer.update();t=(f-1)/24
   if e['send_s']<=t<=e['receive_s']:
    sensor=native_instance(e['receiver_ref'])[1].translation;max_sensor_error=max(max_sensor_error,(sensor-Vector(e.get('reference_world_m',e['emitter_world_m']))).length)
   for o in s.objects:
    if not o.name.startswith(e['event_id']):continue
    if 'FIXED_SAMPLE' in o.name and t>=e['contact_s']:
     check('fixed sample '+e['event_id']+' '+str(f),(o.location-(hit+normal*.0002)).length<2e-6)
    if o.hide_render or not ('SEND_' in o.name or 'RETURN_' in o.name):continue
    active_legs['SEND' if 'SEND_' in o.name else 'RETURN']+=1
    for sp in o.data.splines:
     for v in sp.points:
      p=o.matrix_world@Vector(v.co[:3]);delta=p-origin
      if delta.length<1e-7:continue
      wh,_,_,dist=tree.ray_cast(origin,delta.normalized(),10)
      if wh is not None:max_penetration=max(max_penetration,delta.length-dist)
    ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
    for v in mesh.vertices:
     p=o.matrix_world@v.co;delta=p-origin;min_face_margin=min(min_face_margin,delta.dot(direction))
     if delta.length<1e-7:continue
     wh,_,_,distance=tree.ray_cast(origin,delta.normalized(),10)
     if wh is not None:max_envelope_penetration=max(max_envelope_penetration,delta.length-distance)
    ev.to_mesh_clear()
  check('sensor stationary during event '+e['event_id'],max_sensor_error<2e-6,max_sensor_error)
 check('no visible arc centerline beyond wall '+kind,max_penetration<.00002,max_penetration)
 check('no finite arc envelope beyond wall '+kind,max_envelope_penetration<.00002,max_envelope_penetration)
 check('no finite arc envelope behind native emitter cap exit '+kind,min_face_margin>=-.00002,min_face_margin)
 check('saved send and return arcs actually visible '+kind,all(v>0 for v in active_legs.values()),active_legs)
 check('shared migration camera/timing preserved '+kind,json.loads((E/f'migration_{kind}_v004.json').read_text())['preserved'])
 check('clear actual cap/contact sightlines '+kind,json.loads((E/f'sightlines_{kind}_v006.json').read_text())['all_clear'])
 native.append(dict(path=str(path.relative_to(ROOT)).replace('\\','/'),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),libraries=[dict(path=l.filepath,resolved=bpy.path.abspath(l.filepath)) for l in bpy.data.libraries],camera=list(s.camera.location),frames=s.frame_end,max_arc_penetration_m=max_penetration))
out=dict(checks=checks,all_pass=all(x['passed'] for x in checks),native=native,kind='executor self-checks, not independent verification or human acceptance')
(E/'native-verification_v001.json').write_text(json.dumps(out,indent=2));print('SENSING_NATIVE',len(checks),out['all_pass'],[x for x in checks if not x['passed']],flush=True)
