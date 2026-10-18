"""T44 isolated uphole candidate. Rendering/integration requires T45 queue ownership."""
import bpy,sys,runpy,json,time,math,hashlib,struct
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[5];ASSET=ROOT/'04-Production/Shared/Assets';WORLD=ASSET/'World';TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v007';E=REV/'Evidence';SCENES=REV/'Scenes';P=TASK/'Previews/Revision_v007'
for p in [E,SCENES,P]:p.mkdir(parents=True,exist_ok=True)
CANDIDATE=REV/'CandidateMaster/BHA_film_v007.blend';CANDIDATE.parent.mkdir(parents=True,exist_ok=True)
ARGS=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else ['noop']
sys.argv=['script','--','noop'];B=runpy.run_path(str(WORLD/'Scripts/build_world_t44.py'));C=runpy.run_path(str(WORLD/'Scripts/build_cleanup_v006.py'));sys.path.insert(0,str(HERE))
from continuation_controls_v001 import attach_continuation
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
def snapshot():return B['snapshot']()
def meshhash(o):
 h=hashlib.sha256()
 for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
 for f in o.data.polygons:h.update(str(tuple(f.vertices)).encode())
 return h.hexdigest()
def hardware_instance():return next(o for o in bpy.data.objects if not o.library and o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.name=='WORLD_HARDWARE')
def master():
 s=B['clean']();c=B['coll']('WORLD_HARDWARE');s.collection.children.link(c)
 old=B['linkcoll'](ASSET/'BHA/BHA_film_v006.blend',['WORLD_HARDWARE'])[0]
 B['instance'](old,c,'ACCEPTED_BHA_v006_LINK')
 c['revision']='v007; accepted BHAv006 nested unchanged; canonical continuation/joint components in same file; use attach_continuation to add local length/show controls'
 steel=B['mat']('BHA_ContinuationSteel',(.34,.38,.42),.88,.38)
 dark=B['mat']('BHA_ConnectionSteel',(.24,.28,.31),.80,.40)
 ext=B['coll']('WORLD_UPHOLE_EXTENSION');joint=B['coll']('WORLD_UPHOLE_JOINT')
 o=B['tube']('UPHOLE_UNIT_COLLAR_EXTENSION',-1.,0.,.03571875,.104775,ext,steel);C['normals'](o)
 o['dimensions']='Unit longitudinal length1m; consumer scalesX only. OD8.25in/ID2.8125in inherited generic collar reference; not selected drillstring specification.'
 o['interface']='Near end anchored to original source collar endX-1.5m. Default added length12m; no exact thread fit.'
 # Raised exterior sleeve avoids coplanar overlap with the inherited collar skin.
 q=B['lathe']('UPHOLE_SIMPLIFIED_CONNECTION', [(-1.58,.1048),(-1.575,.107),(-1.445,.107),(-1.44,.1048)],joint,dark,n=96)
 for p in q.data.polygons:p.use_smooth=True
 q['status']='Illustrative raised connection shoulder across original collar/continuation join. No threads/pin-box identity or fit certification.'
 preview=B['coll']('BHA_CONTINUITY_PREVIEW');s.collection.children.unlink(c);s.collection.children.link(preview)
 hw=B['instance'](c,preview,'PREVIEW_HARDWARE');hw.empty_display_size=.1
 attach_continuation(ASSET,hw,source_collections=[ext,joint])
 c['collections']='WORLD_HARDWARE + WORLD_UPHOLE_EXTENSION + WORLD_UPHOLE_JOINT; preview composition provided separately'
 path=CANDIDATE;B['save'](path)
 dump(E/'master-build_v007.json',dict(path=rel(path),sha256=sha(path),source=rel(ASSET/'BHA/BHA_film_v006.blend'),source_sha256=sha(ASSET/'BHA/BHA_film_v006.blend'),default_length_m=12,original_join_x_m=-1.5,far_endpoint_x_m=-13.5,outer_radius_m=.104775,inner_radius_m=.03571875,connection_outer_radius_m=.107,provisional=True))
 print('CONTINUITY_MASTER_PASS',flush=True)
def migrate():
 for k in ['A','B']:
  src=TASK/'Revision_v006/Scenes'/f'Reuse_{k}_cleanup_v010.blend';openfile(src);s=bpy.context.scene;s.frame_set(1);before=snapshot()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  target=[l for l in bpy.data.libraries if Path(l.filepath).name=='BHA_film_v006.blend'];assert len(target)==1
  target[0].filepath=str(CANDIDATE);target[0].reload()
  hw=hardware_instance();attach_continuation(ASSET,hw,master_path=CANDIDATE);s.frame_set(1);bpy.context.view_layer.update();after=snapshot()
  retained={n:after['local_controls'][n] for n in before['local_controls']}
  assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==retained
  out=SCENES/f'Reuse_{k}_continuity_v001.blend';B['save'](out)
  dump(E/f'migration_{k}_v007.json',dict(source=rel(src),output=rel(out),before=before,after=after,existing_camera_timing_controls_preserved=True,new_controls=['UPHOLE_CONTINUATION_CONTROL.length_m','UPHOLE_CONTINUATION_CONTROL.show'],procedure='Reload sole hardware successor; add linked canonical extension/joint instances parented to same hardware; new local length/show controls, no copied meshes'))
 print('CONTINUITY_MIGRATION_PASS',flush=True)
def views():
 for name,loc,target,lens in [('connection_wide',(2.1,-7.0,2.6),(-1.3,0,0),42),('furthest_uphole',(-3.4,-4.5,1.8),(-4.2,0,0),43)]:
  openfile(SCENES/'Reuse_B_continuity_v001.blend');s=bpy.context.scene;s.frame_set(1)
  # Separate static inspection scenes; original two proof consumers stay unchanged.
  cam=s.camera;cam.animation_data_clear();cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=lens
  s.frame_start=1;s.frame_end=1;s.render.film_transparent=False;s.view_settings.exposure=-.7
  col=hwcol=hardware_instance().users_collection[0]
  B['light']('CONTINUITY_KEY',(-2.6,-3,2.5),(-2,0,0),140,3,col,(.7,.83,1));B['light']('CONTINUITY_EDGE',(-4.5,.1,1.2),(-3,0,0),55,2,col,(1,.72,.45))
  s['purpose']='T44 static wider/travel-envelope continuity inspection, not an actual V3 shot. Accepted environment unchanged.'
  B['save'](SCENES/(name+'_v001.blend'))
 print('CONTINUITY_VIEWS_PASS',flush=True)
def publish():
 openfile(CANDIDATE);canonical=ASSET/'BHA/BHA_film_v007.blend';B['save'](canonical)
 dump(E/'canonical-master_v007.json',dict(path=rel(canonical),sha256=sha(canonical),candidate_sha256=sha(CANDIDATE),length_default_m=12,geometry='Accepted BHAv006 nested unchanged; new canonical collar continuation/joint only',gate='Ready for inspection/integration; human approval pending'))
 for name in ['Reuse_A_continuity','Reuse_B_continuity','connection_wide','furthest_uphole']:
  src=SCENES/(name+'_v001.blend');openfile(src);before=snapshot()
  for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
  targets=[l for l in bpy.data.libraries if Path(l.filepath).resolve()==CANDIDATE.resolve()];assert len(targets)==1
  targets[0].filepath=str(canonical);targets[0].reload();after=snapshot()
  assert before['camera']==after['camera'] and before['timing']==after['timing'] and before['local_controls']==after['local_controls']
  out=SCENES/(name+'_v002.blend');B['save'](out)
  dump(E/(name+'_canonical-migration_v007.json'),dict(source=rel(src),output=rel(out),camera_timing_all_controls_preserved=True,source_sha256=sha(src),output_sha256=sha(out)))
 print('CONTINUITY_PUBLISH_PASS',flush=True)
def inspect(path):
 openfile(path);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();hw=hardware_instance();ctrl=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL'];end=bpy.data.objects['UPHOLE_FAR_ENDPOINT']
 deps=bpy.context.evaluated_depsgraph_get();endpoint=end.evaluated_get(deps).matrix_world.translation
 p=world_to_camera_view(s,s.camera,endpoint);join=hw.matrix_world@Vector((-1.5,0,0));j=world_to_camera_view(s,s.camera,join)
 rec=dict(path=rel(path),sha256=sha(path),libraries=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries],eccos=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in deps.object_instances),extension_meshes=sum(i.object.original.name=='UPHOLE_UNIT_COLLAR_EXTENSION' for i in deps.object_instances),far_endpoint_world=list(endpoint),endpoint_camera=list(p),join_world=list(join),join_camera=list(j),length_m=ctrl['length_m'],camera=snapshot()['camera'],timing=snapshot()['timing'])
 assert rec['eccos']==1 and rec['extension_meshes']==1 and all(x['exists'] and x['path'].startswith('//') for x in rec['libraries'])
 assert not(0<=p.x<=1 and 0<=p.y<=1 and p.z>0),'Exposed far endpoint in intended view'
 dump(E/(path.stem+'_fresh-open.json'),rec);return rec
def wide_refine():
 openfile(SCENES/'connection_wide_v002.blend');s=bpy.context.scene;cam=s.camera
 cam.location=(0,-8,2.2);cam.rotation_euler=(Vector((-.5,0,0))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=34
 B['save'](SCENES/'connection_wide_v003.blend');print('CONTINUITY_WIDE_REFINE_PASS',flush=True)
def render(name,version='v001'):
 path=SCENES/(name+'_'+version+'.blend') if not name.startswith('Reuse') else SCENES/(name+'_continuity_'+version+'.blend');inspect(path);s=bpy.context.scene;s.render.filepath=str(P/(name+'_'+version+'.png'))
 start=time.perf_counter();bpy.ops.render.render(write_still=True);elapsed=time.perf_counter()-start
 dump(E/(name+'_'+version+'_benchmark_v007.json'),dict(scene=rel(path),output=rel(Path(s.render.filepath)),seconds=elapsed,under_5=elapsed<5,engine=s.render.engine,backend='VULKAN',resolution=[s.render.resolution_x,s.render.resolution_y],samples=s.eevee.taa_render_samples,measurement='First full render-to-file in fresh process; normal existing disk GPU caches, no warmup render; process/file loading excluded',known_limit='Original empty-cache startup12.55-25.13s remains unresolved.'))
 print('CONTINUITY_RENDER',name,elapsed,elapsed<5,flush=True)
mode=ARGS[0]
if mode=='master':master()
elif mode=='migrate':migrate()
elif mode=='views':views()
elif mode=='publish':publish()
elif mode=='wide_refine':wide_refine()
elif mode=='render':render(ARGS[1])
elif mode=='render2':render(ARGS[1],'v002')
elif mode=='render3':render(ARGS[1],'v003')
