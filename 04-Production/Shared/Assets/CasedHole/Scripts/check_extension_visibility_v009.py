"""Actual finite uphole-end rim visibility in the macro cased consumer."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';sys.path.insert(0,str(A/'Acoustics/Scripts'))
from acoustic_event_v002 import native_instance
scene_name=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'CasedSupport_v009.blend';version=Path(scene_name).stem.split('_')[-1]
bpy.ops.wm.open_mainfile(filepath=str(T/'Scenes'/scene_name),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();ext,m=native_instance('UPHOLE_UNIT_COLLAR_EXTENSION');points=[]
for v in ext.data.vertices:
 if abs(v.co.x+1)<1e-6:points.append(m@v.co)
for p in ext.data.polygons:
 if all(abs(ext.data.vertices[i].co.x+1)<1e-6 for i in p.vertices):points.append(m@p.center)
trees=[]
for i in bpy.context.evaluated_depsgraph_get().object_instances:
 o=i.object.original;matrix=i.matrix_world.copy()
 if o.type!='MESH' or o.hide_render or o.name.startswith('MUD_') or o.get('shared_package')=='Acoustics':continue
 trees.append((o.name,BVHTree.FromPolygons([matrix@v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])))
rays=[]
for point in points:
 uv=world_to_camera_view(s,s.camera,point)
 if not(0<=uv.x<=1 and 0<=uv.y<=1 and uv.z>s.camera.data.clip_start):continue
 d=point-s.camera.location;hits=[]
 for name,tree in trees:
  hit,n,face,dist=tree.ray_cast(s.camera.location,d.normalized(),d.length-.0001)
  if hit is not None:hits.append(dict(object=name,distance_m=dist,occlusion_margin_m=d.length-dist))
 hits.sort(key=lambda x:x['distance_m']);rays.append(dict(point=list(point),camera_projection=list(uv),blocked=bool(hits),first_occluder=hits[0] if hits else None))
events=json.loads((T/'Evidence/actual-cased-events_v009.json').read_text())['events'];event_rays=[]
for e in events:
 for label,target in [('cap',Vector(e['emitter_world_m'])),('contact',Vector(e['hit_world_m']))]:
  d=target-s.camera.location;hits=[]
  for name,tree in trees:
   hit,n,face,dist=tree.ray_cast(s.camera.location,d.normalized(),d.length-.00005)
   if hit is not None:hits.append(dict(object=name,occlusion_margin_m=d.length-dist))
  event_rays.append(dict(event_id=e['event_id'],target=label,occluders=hits))
out=dict(scene='04-Production/Records/Tasks/T-047/Scenes/'+scene_name,far_rim_vertex_and_facecentre_samples=len(points),projected_samples=len(rays),unoccluded_samples=sum(not r['blocked'] for r in rays),all_projected_samples_occluded=all(r['blocked'] for r in rays),rays=rays,actual_cap_contact_rays=event_rays,cap_contact_all_clear=not any(r['occluders'] for r in event_rays),limits='Actual full native rim vertices and cap face centres checked; body held stationary. Projection alone is not visibility. Render inspection still required.')
(T/('Evidence/extension-end-visibility_'+version+'.json')).write_text(json.dumps(out,indent=2),encoding='utf8');print('T47_EXTENSION_END',len(rays),out['unoccluded_samples'],out['all_projected_samples_occluded'],'cap/contact clear',out['cap_contact_all_clear'],flush=True)
