"""T47 preflight4 against saved reconciled natives; no rendering or saves."""
import bpy,sys,json,math,hashlib,itertools
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_event_v002 import validate_event,validate_native_event,native_instance,wall_tree
checks=[]
def check(name,passed,detail=None):
 checks.append(dict(name=name,passed=bool(passed),detail=detail))
 if not passed:print('T47_CHECK_FAILED',name,detail,flush=True)
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def update():bpy.context.view_layer.update();bpy.context.view_layer.update()
# Every independent layer-selection/visibility Boolean, both render and viewport.
p=S/'CasedReuse_A_v008.blend';openfile(p);s=bpy.context.scene;s.frame_set(1);c=bpy.data.objects['CASED_CONTROL'];keys=['cutaway','show_steel','show_cement','show_channel','show_reference','wear','channel'];truth=[]
instances=[o for o in s.objects if o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.name.startswith('CASED_')];check('exact twelve linked layer instances',len(instances)==12,len(instances))
for values in itertools.product([0,1],repeat=len(keys)):
 params=dict(zip(keys,values))
 for k,v in params.items():c[k]=v
 c.update_tag();update();bad=[]
 for o in instances:
  name=o.instance_collection.name;k=name.removeprefix('CASED_').removesuffix('_CUTAWAY').removesuffix('_FULL');visible=params['cutaway']==int(name.endswith('CUTAWAY'))
  if k.startswith('STEEL'):visible=visible and bool(params['show_steel']) and params['wear']==int(k.endswith('WEAR'))
  elif k.startswith('CEMENT'):visible=visible and bool(params['show_cement']) and params['channel']==int(k.endswith('CHANNEL'))
  elif k=='CHANNEL':visible=visible and bool(params['show_channel']) and bool(params['channel'])
  else:visible=visible and bool(params['show_reference']) and bool(params['wear'])
  if o.hide_render==visible or o.hide_viewport==visible:bad.append(name)
 truth.append(dict(parameters=params,passed=not bad,failures=bad))
check('complete'+str(len(truth))+'-state layer render/viewport truth table',all(x['passed'] for x in truth),dict(states=len(truth),instance_checks=len(truth)*len(instances)*2));dump(E/'layer-truth-table_v009.json',dict(scene=p.relative_to(ROOT).as_posix(),sha256=sha(p),states=truth))
# Saved actual cased acoustic/response candidate after revised T44 migration.
p=S/'CasedSupport_v009.blend';openfile(p);s=bpy.context.scene;data=json.loads((E/'actual-cased-events_v009.json').read_text());s.frame_set(1);update();libs=[dict(path=l.filepath,resolved=str(Path(bpy.path.abspath(l.filepath)).resolve()),sha256=sha(Path(bpy.path.abspath(l.filepath)).resolve())) for l in bpy.data.libraries];check('all relative libraries resolve',all(x['path'].startswith('//') for x in libs));check('accepted BHA007 exact hash',any(x['sha256']=='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1' for x in libs))
active_sources=sorted({o.data.library.filepath for o in bpy.data.objects if o.get('shared_package')=='Acoustics' and o.data and o.data.library});check('active acoustic data use v003 only',bool(active_sources) and all('Acoustics_v003.blend' in x for x in active_sources),active_sources)
wall,wm,tree=wall_tree('CASED_STEEL_NOMINAL_CUTAWAY');event_rows=[];phase_rows=[];response_rows=[]
for e,response in zip(data['events'],data['responses']):
 s.frame_set(1);update();check('strict source/packet contract '+e['event_id'],validate_event(e));check('fresh native cap/wall registration '+e['event_id'],validate_native_event(e));origin=Vector(e['emitter_world_m']);direction=Vector(e['direction_world']);hit=Vector(e['hit_world_m']);normal=Vector(e['normal_world']);distance=(hit-origin).length
 fresh,n,face,dist=tree.ray_cast(origin,direction,10);v=[wm@wall.data.vertices[i].co for i in wall.data.polygons[face].vertices];fn=(v[1]-v[0]).cross(v[2]-v[0]).normalized();plane=abs((hit-v[0]).dot(fn));a=math.atan2(hit.z,hit.y);angles=[math.atan2(q.z,q.y) for q in v];bounded=min(q.x for q in v)-1e-6<=hit.x<=max(q.x for q in v)+1e-6 and min(angles)-1e-6<=a<=max(angles)+1e-6;nearest=tree.find_nearest(hit)[3];check('bounded actual casing face '+e['event_id'],plane<1e-6 and bounded and (fresh-hit).length<3e-6)
 arcs=[(role,phase,bpy.data.objects[e['event_id']+'_ACOUSTICS_'+role+'_%02d'%phase['arc_index']]) for role in ['SEND','RETURN'] for phase in e['arc_phases']];observed={(role,phase['arc_index']):[] for role,phase,ob in arcs};max_beyond_wall=0.;min_cap_margin=1.;max_origin_error=0.;max_cap_error=0.;max_endpoint_error=0.;worldbars=[o for o in s.objects if o.get('event_id')==e['event_id'] and o.name.startswith('CASED_') and '_RESPONSE_' in o.name];check('twelve casing-local response bars '+e['event_id'],len(worldbars)==12,len(worldbars));response_visible=[]
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);update();t=(f-1)/s.render.fps
  if e['send_s']<=t<=e['hold_emitter_until_s']:
   cap=__import__('acoustic_event_v002').sample_native_event(e['emitter_ref'],e['wall_source']['object'],'verify-held-cap',e['send_s'],e['contact_s'],e['receive_s'],e['patch_lifetime_s'],e['emitter_surface']['object']);max_cap_error=max(max_cap_error,(Vector(cap['emitter_world_m'])-origin).length)
  for role,phase,o in arcs:
   begin=phase['send_s'] if role=='SEND' else phase['contact_s'];end=phase['contact_s'] if role=='SEND' else phase['receive_s'];gain=float(o.color[3]);visible=not o.hide_render and gain>.001 and max(o.scale)>1e-8;check('arc phase hidden outside leg '+o.name+' f'+str(f),not visible or begin-1e-8<=t<end+1e-8)
   u=max(0,min(1,(t-begin)/(end-begin)));expected=origin+direction*distance*u if role=='SEND' else hit-direction*distance*u;max_origin_error=max(max_origin_error,(o.location-expected).length)
   if t>=end and role=='RETURN':max_endpoint_error=max(max_endpoint_error,(o.location-origin).length)
   if not visible:continue
   observed[(role,phase['arc_index'])].append(f);ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=ev.to_mesh()
   for q in mesh.vertices:
    pos=o.matrix_world@q.co;delta=pos-origin;min_cap_margin=min(min_cap_margin,delta.dot(direction))
    if delta.length<1e-8:continue
    wh,_,_,wall_distance=tree.ray_cast(origin,delta.normalized(),10)
    if wh is not None:max_beyond_wall=max(max_beyond_wall,delta.length-wall_distance)
   ev.to_mesh_clear()
  on=response['response_start_s']<=t<response['response_end_s'];actual=all(not o.hide_render for o in worldbars);check('response onset/end '+e['event_id']+' f'+str(f),actual==on)
  if actual:response_visible.append(f)
 for role,phase,o in arcs:
  frames=observed[(role,phase['arc_index'])];begin=phase['send_s'] if role=='SEND' else phase['contact_s'];end=phase['contact_s'] if role=='SEND' else phase['receive_s'];check('individual working arc '+o.name,bool(frames),frames);phase_rows.append(dict(event_id=e['event_id'],role=role,arc_index=phase['arc_index'],declared_seconds=[begin,end],visible_frames=frames))
 check('complete finite tube envelope before wall '+e['event_id'],max_beyond_wall<.00002,max_beyond_wall);check('complete finite tube envelope outside native cap '+e['event_id'],min_cap_margin>=-.00002,min_cap_margin);check('all arc apex phases registered '+e['event_id'],max_origin_error<3e-6,max_origin_error);check('same emitter held through final packet '+e['event_id'],max_cap_error<3e-6,max_cap_error);check('return endpoint same cap after receive '+e['event_id'],max_endpoint_error<3e-6,max_endpoint_error)
 response_rows.append(dict(event_id=e['event_id'],start_s=response['response_start_s'],end_s=response['response_end_s'],lifetime_s=response['response_lifetime_s'],visible_frames=response_visible,first_visible_s=(response_visible[0]-1)/24,last_visible_s=(response_visible[-1]-1)/24));event_rows.append(dict(event_id=e['event_id'],bounded_face_plane_error_m=plane,within_face_bounds=bounded,bvh_nearest_diagnostic_m=nearest,max_finite_arc_wall_penetration_m=max_beyond_wall,min_finite_arc_cap_margin_m=min_cap_margin,packet_end_s=e['packet_end_s'],hold_emitter_until_s=e['hold_emitter_until_s']))
# Current macro camera must see native cap/contact despite the longer uphole hardware.
s.frame_set(1);update();opaque=[]
for i in bpy.context.evaluated_depsgraph_get().object_instances:
 ob=i.object.original;m=i.matrix_world.copy()
 if ob.type=='MESH' and ob.library and 'ECCO' in ob.library.filepath and not ob.hide_render:opaque.append((ob.name,BVHTree.FromPolygons([m@v.co for v in ob.data.vertices],[list(p.vertices) for p in ob.data.polygons])))
rays=[]
for e in data['events']:
 for label,target in [('cap',Vector(e['emitter_world_m'])),('contact',Vector(e['hit_world_m']))]:
  d=target-s.camera.location;blocked=[]
  for n,bvh in opaque:
   pnt,_,_,dist=bvh.ray_cast(s.camera.location,d.normalized(),d.length)
   if pnt is not None and d.length-dist>.00005:blocked.append(dict(object=n,margin_m=d.length-dist))
  rays.append(dict(event=e['event_id'],target=label,blocked=blocked))
check('native macro cap/contact rays clear',not any(r['blocked'] for r in rays),rays)
dump(E/'preflight4-native_v009.json',dict(passed=all(x['passed'] for x in checks),checks=checks,libraries=libs,event_evidence=event_rows,arc_phases=phase_rows,response_windows=response_rows,source_scene='04-Production/Records/Tasks/T-047/Scenes/CasedSupport_v009.blend',source_sha256=sha(S/'CasedSupport_v009.blend'),status='Executor checks, not independent/human acceptance',limits='Full-BVH nearest diagnostic retained; bounded face evidence is authoritative for contact registration. Timing/amplitudes qualitative.'))
print('T47_PREFLIGHT4',len(checks),all(x['passed'] for x in checks),flush=True)
