import bpy,json,time,hashlib
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];OUT=B/'Scenes/S05_tracked-cuttings_v009.blend';s=bpy.context.scene;cam=s.camera;fx=bpy.data.collections['S05_TRACKED_COHORT_v009']
prior=B.parent/'Interaction-Proof_v008/Scenes/S05_internal-flow_v008.blend';prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest()
tracks=[]
for o in fx.objects:
 heads=[]
 for f in range(1,73):
  s.frame_set(f);heads.append(list(o.location))
 tracks.append({'name':o.name,'heads':heads})
# Centre all projected vertices across the complete trip, not just its midpoint.
points=[]
for f in range(1,73):
 s.frame_set(f);bpy.context.view_layer.update()
 for o in fx.objects:points.extend(o.matrix_world@v.co for v in o.data.vertices)
def get_bounds():
 ps=[world_to_camera_view(s,cam,p) for p in points]
 return [min(p.x for p in ps),min(p.y for p in ps),max(p.x for p in ps),max(p.y for p in ps)]
for iteration in range(5):
 bounds=get_bounds();delta=Vector(((bounds[0]+bounds[2])/2-.5,(bounds[1]+bounds[3])/2-.5,0))
 depth=sum(-(cam.matrix_world.inverted()@p).z for p in points)/len(points)
 width=depth*cam.data.sensor_width/cam.data.lens
 cam.location+=cam.matrix_world.to_quaternion()@Vector((delta.x*width,delta.y*width*720/1280,0));bpy.context.view_layer.update()
bounds=get_bounds()
assert min(bounds[:2])>.05 and max(bounds[2:])<.95,bounds
s.eevee.taa_render_samples=8
s.frame_set(36);s.render.filepath=str(B/'Previews/interaction_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-t
s['proof_scope']='v009 three persistent matte fragments tracked from entry around one turning pad through upward exit; quiet accepted annulus; stationary camera; illustrative not CFD'
result={'render_seconds':seconds,'prior_v008_sha256':prior_hash,'fragments':tracks,'full_track_screen_bounds':bounds,'camera_location':list(cam.location),'camera_quaternion':list(cam.rotation_quaternion),'lens_mm':58,'duration_s':3,'frames':72,'fps':24,'motion':'Same three objects, no spawn, hiding, scaling, reset or recycled loop. Uniform upward progression at authored .17 m/s, geometry-derived angular bend and partial rotation influence.','quiet_fluid':'Copied material with constant density 2.5; source volume concept, mesh and amber retained. Original material remains in file.','phases':'Approach about 0-0.7s; pad-side turn about 0.7-2.1s; continued upward exit about 2.1-3s.'}
(B/'Records/build.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
