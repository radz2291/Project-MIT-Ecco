"""Fresh-open current T46 native/self-checks, including complete packet contract."""
import bpy,sys,json,math,hashlib,copy
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-046';E=T/'Evidence';S=T/'Scenes';sys.path.insert(0,str(HERE))
from acoustic_event_v002 import native_instance,wall_tree,validate_event,exact_one,sample_native_event
from acoustic_verify_v002 import verify_packet
checks=[];native=[];packets=[]
def check(n,p,d=None):checks.append(dict(name=n,passed=bool(p),detail=d))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
expected={A/'BHA/BHA_film_v007.blend':'b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1',A/'BHA/BHA_film_v006.blend':'923c931e52f6c1cf81eefbd8db530fc45f08ab1aa0b2d74ca607c01481d1e66d',A/'WellAssembly/World_environment_v009.blend':'addf69a41e677052b40992dbbed56355f9b65c5ba5e64f865e143f09d2288281'}
for path,h in expected.items():check('accepted source '+path.name,sha(path)==h)
for kind in ['A','B']:
 version='v009' if kind=='A' else 'v010'
 path=S/f'Sensing_reuse_{kind}_{version}.blend';bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
 libs=[]
 for l in bpy.data.libraries:
  p=Path(bpy.path.abspath(l.filepath)).resolve(strict=True);parent=Path(bpy.path.abspath(l.parent.filepath)).resolve(strict=True).as_posix() if l.parent else None
  libs.append(dict(path=l.filepath,resolved=p.as_posix(),parent=parent,sha256=sha(p)))
  check('relative actual dependency '+kind+' '+p.name,l.filepath.startswith('//') and p.is_file())
  if p in expected:check('frozen dependency hash '+kind+' '+p.name,sha(p)==expected[p])
 direct7=[r for r in libs if Path(r['resolved'])==A/'BHA/BHA_film_v007.blend' and r['parent'] is None]
 nested6=[r for r in libs if Path(r['resolved'])==A/'BHA/BHA_film_v006.blend' and r['parent']==(A/'BHA/BHA_film_v007.blend').as_posix()]
 check('only direct successor with nested frozenv006 '+kind,len(direct7)==1 and len(nested6)==1)
 deps=bpy.context.evaluated_depsgraph_get();instances=[(i.object.original,i.matrix_world.copy()) for i in deps.object_instances];names=[o.name for o,m in instances]
 for ob,expected_count in [('ECCO_HOUSING_SOURCE_MESH',1),('UPHOLE_UNIT_COLLAR_EXTENSION',1),('UPHOLE_SIMPLIFIED_CONNECTION',1)]:check('one native '+ob+' '+kind,names.count(ob)==expected_count,names.count(ob))
 check('six native bit blades '+kind,sum(n.startswith('PDC_INTEGRAL_BLADE') for n in names)==6)
 bad=[];materials=0
 for o,m in instances:
  if o.type!='MESH' or not o.library or not any(x in o.library.filepath for x in ['BHA','ECCO']):continue
  for material in o.data.materials:
   materials+=1
   if material is None or material.node_tree is None or not any(n.type=='OUTPUT_MATERIAL' and n.inputs['Surface'].is_linked for n in material.node_tree.nodes):bad.append((o.name,material.name if material else None))
 check('fresh linked hardware shader surfaces resolve '+kind,materials>0 and not bad,bad)
 poses=[native_instance(f'ECCO_SENSOR_REF_{i:02d}')[1] for i in [1,2,3]];angles=sorted(math.atan2(p.translation.z,p.translation.y) for p in poses);gaps=[(angles[(i+1)%3]-angles[i])%math.tau for i in range(3)]
 check('sensor plane retained '+kind,max(p.translation.x for p in poses)-min(p.translation.x for p in poses)<1e-5)
 check('120degree sensor references '+kind,max(abs(g-math.tau/3) for g in gaps)<1e-5)
 check('unscaled source references '+kind,all(abs(p.to_3x3().col[i].length-1)<1e-5 for p in poses for i in range(3)))
 migration=json.loads((E/f'migration_{kind}_v009.json').read_text());check('prior native preserved '+kind,sha(ROOT/migration['source'])==migration['source_sha256']);check('camera motion and timing retained '+kind,migration['camera_timing_controls_preserved'] and migration['camera_keys_preserved'])
 events=json.loads((E/f'events_{kind}_v003.json').read_text())['events'];sightlines=[]
 for event in events:
  packet=verify_packet(event);packets.append(packet);check('complete per-event sixfront packet '+event['event_id'],packet['all_pass'],[c for c in packet['checks'] if not c['passed']])
  s.frame_set(round(event['send_s']*24)+1);bpy.context.view_layer.update();trees=[]
  for i in bpy.context.evaluated_depsgraph_get().object_instances:
   o=i.object.original;m=i.matrix_world.copy()
   if o.type=='MESH' and o.library and (any(x in o.library.filepath for x in ['BHA','ECCO']) or o.name.startswith('UPHOLE_')) and not o.hide_render:trees.append((o.name,BVHTree.FromPolygons([m@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])))
  _,_,walltree=wall_tree(event['wall_source']['object']);trees.append(('actual sampled wall',walltree))
  for label,point in [('cap_exit',event['emitter_world_m']),('contact',event['hit_world_m'])]:
   target=Vector(point);delta=target-s.camera.matrix_world.translation;occluders=[]
   for name,tree in trees:
    p,n,fi,distance=tree.ray_cast(s.camera.matrix_world.translation,delta.normalized(),delta.length)
    if p is not None and delta.length-distance>.00005:occluders.append(dict(name=name,gap_m=delta.length-distance))
   check('actual combined sender/contact sightline '+event['event_id']+' '+label,not occluders,occluders);sightlines.append(dict(event_id=event['event_id'],target=label,occluders=occluders))
  # New uphole parts stay axially disjoint from the complete finite acoustic fan.
  uphole_max=-1e9;arc_min=1e9;sample_error=0
  for f in range(1,s.frame_end+1):
   s.frame_set(f);bpy.context.view_layer.update();t=(f-1)/24
   if t>=event['contact_s']:
    point=s.objects[event['event_id']+'_ACOUSTICS_FIXED_SAMPLE'];expected_point=Vector(event['hit_world_m'])+Vector(event['normal_world'])*.0002;sample_error=max(sample_error,(point.matrix_world.translation-expected_point).length)
   if not event['send_s']<=t<=event['packet_end_s']:continue
   deps=bpy.context.evaluated_depsgraph_get()
   for i in deps.object_instances:
    if i.object.original.name in ['UPHOLE_UNIT_COLLAR_EXTENSION','UPHOLE_SIMPLIFIED_CONNECTION']:uphole_max=max(uphole_max,max((i.matrix_world@v.co).x for v in i.object.original.data.vertices))
   for o in s.objects:
    if not o.name.startswith(event['event_id']) or o.hide_render or not ('SEND_' in o.name or 'RETURN_' in o.name):continue
    ev=o.evaluated_get(deps);me=ev.to_mesh();arc_min=min(arc_min,min((o.matrix_world@v.co).x for v in me.vertices));ev.to_mesh_clear()
  check('finite arc clearance from new continuation '+event['event_id'],arc_min-uphole_max>.001,dict(arc_min_x=arc_min,added_hardware_max_x=uphole_max,margin_m=arc_min-uphole_max));check('world fixed sample retained '+event['event_id'],sample_error<3e-6,sample_error)
  # Explicit negative cases address the missing/ambiguous-cap/source preflight.
  if event is events[0]:
   negatives=[]
   for name,fn in [('missing cap',lambda:exact_one([],event['emitter_surface']['object'])),('ambiguous cap',lambda:exact_one([1,2],event['emitter_surface']['object']))]:
    try:fn();negatives.append((name,False))
    except ValueError:negatives.append((name,True))
   for name,mutate in [('cap hash mismatch',lambda e:e['emitter_surface'].update(sha256='0'*64)),('wall hash mismatch',lambda e:e['wall_source'].update(sha256='0'*64)),('cap offset mismatch',lambda e:e['emitter_surface'].update(offset_from_reference_m=.003)),('unknown provenance',lambda e:e.update(provenance='unmarked'))]:
    invalid=copy.deepcopy(event);mutate(invalid)
    try:validate_event(invalid);negatives.append((name,False))
    except (AssertionError,ValueError):negatives.append((name,True))
   check('strict metadata/cap rejection cases '+kind,all(p for n,p in negatives),negatives)
 native.append(dict(path=str(path.relative_to(ROOT)).replace('\\','/'),sha256=sha(path),libraries=libs,frames=s.frame_end,sightlines=sightlines))
out=dict(checks=checks,packets=packets,all_pass=all(c['passed'] for c in checks),native=native,verification='Executor fresh-open self-checks, not independent verification or human acceptance')
(E/'native-verification_v010.json').write_text(json.dumps(out,indent=2));print('SENSING_VERIFY_V010',len(checks),sum(len(p['checks']) for p in packets),out['all_pass'],[c for c in checks if not c['passed']],flush=True)
