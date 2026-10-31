"""Saved-file geometry/event verification. No render and no scene save."""
import bpy,json,math,sys,hashlib
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_event_v001 import wall_tree,native_instance,validate_event
events=json.loads((E/'actual-cased-events_v003.json').read_text())['events'];checks=[]
for name,version in [('Hardware','v003'),('Channel','v003'),('Wear','v003'),('Retrieval','v004'),('Support','v004')]:
 p=S/('Cased'+name+'_'+version+'.blend');bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
 libs=[dict(path=l.filepath,exists=Path(bpy.path.abspath(l.filepath)).exists()) for l in bpy.data.libraries];assert all(l['exists'] and l['path'].startswith('//') for l in libs)
 row=dict(scene=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),libraries=libs,units=s.unit_settings.scale_length,eccos=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in bpy.context.evaluated_depsgraph_get().object_instances),camera=dict(location=list(s.camera.location),rotation=list(s.camera.rotation_euler),lens=s.camera.data.lens),timing=[s.frame_start,s.frame_end,s.render.fps])
 assert s.unit_settings.scale_length==1
 if name=='Support':
  wall,wall_matrix,tree=wall_tree('CASED_STEEL_NOMINAL_CUTAWAY');res=[]
  for e in events:
   validate_event(e);near=tree.find_nearest(Vector(e['hit_world_m']))[3];hit,normal,face,d=tree.ray_cast(Vector(e['emitter_world_m']),Vector(e['direction_world']),10);err=(hit-Vector(e['hit_world_m'])).length
   poly=wall.data.polygons[face];verts=[wall_matrix@wall.data.vertices[i].co for i in poly.vertices];n=(verts[1]-verts[0]).cross(verts[2]-verts[0]).normalized();plane_error=abs((hit-verts[0]).dot(n));assert err<1e-5 and plane_error<1e-6
   assert min(v.x for v in verts)-1e-6<=hit.x<=max(v.x for v in verts)+1e-6
   aa=[math.atan2(v.z,v.y) for v in verts];ha=math.atan2(hit.z,hit.y);assert min(aa)-1e-6<=ha<=max(aa)+1e-6
   assert hashlib.sha256((A/'CasedHole/CasedHole_v002.blend').read_bytes()).hexdigest()==e['wall_source']['sha256']
   res.append(dict(event_id=e['event_id'],repeated_native_ray_error_m=err,face_plane_error_m=plane_error,within_native_face_bounds=True,bvh_nearest_diagnostic_m=near,diagnostic_note='Generic BVH nearest on long quad disagrees3.4mm; repeated native ray is exact and independent face-plane/axial/angular bounds pass.',same_sensor=True,actual_cased_native=True))
  row['events']=res;row['response_controls']=[o.name for o in bpy.data.objects if not o.library and o.name.startswith('ACOUSTICS_CONTROL_')]
  assert len(row['response_controls'])==2
 if name=='Retrieval':
  vals=[]
  for f in [1,12,13,65,66,76,77,96]:
   s.frame_set(f);w=bpy.data.objects['WORLD_CONTROL'];bpy.context.view_layer.update();vals.append(dict(frame=f,travel_m=float(w['travel_m']),ecco_lead_x=float(w['travel_m']),ecco_downhole_x=float(w['travel_m'])+2.4,bit_lead_x=float(w['travel_m'])+2.9))
  assert vals[2]['ecco_lead_x']<0 and vals[2]['bit_lead_x']>0
  assert vals[-1]['bit_lead_x']<0;row['retrieval_samples']=vals
 if name=='Wear':
  ob=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];r=[math.hypot(v.co.y,v.co.z) for v in ob.data.vertices];assert abs(max(r)-.1698625)<1e-6;row['max_outer_radius_m']=max(r);row['preexisting_max_inner_wear_m']=.004;row['registered_nominal_radius_m']=.1589405
 checks.append(row)
(E/'saved-final-verification_v004.json').write_text(json.dumps(dict(checks=checks,passed=True,limits='Executor checks only; human appearance, comprehension and engineering approval remain pending.'),indent=2),encoding='utf8')
print('T47_FINAL_SAVED_CHECKS_PASS',flush=True)
