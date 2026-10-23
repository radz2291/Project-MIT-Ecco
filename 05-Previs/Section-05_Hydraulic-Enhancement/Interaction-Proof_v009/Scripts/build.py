"""One persistent three-fragment cohort: entry, redirection, exit."""
import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];OUT=B/'Scenes/S05_tracked-cuttings_v009.blend';s=bpy.context.scene
for d in ['Scenes','Previews','Records','Work/Frames']:(B/d).mkdir(parents=True,exist_ok=True)
assert not OUT.exists();assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v008'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();assert prior_hash=='0c3e0864eab93105494fe1790ff9f8a1bf97ab024fcb60b6387e6b4e8df6ac4f'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Tracked_Cuttings_v009'
bpy.data.collections['S05_INTERNAL_WISPS_v008'].hide_render=True;bpy.data.collections['S05_INTERNAL_WISPS_v008'].hide_viewport=True
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5)
routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text());ns=dict(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=OMEGA,routes=routes)
src=(B.parent/'Interaction-Proof_v006/Scripts/build.py').read_text();exec(src[src.index('def linear('):src.index("fx=bpy.data.collections.new")],ns);linear=ns['linear'];frame_at=ns['frame_at']
# Retain the accepted annulus; quiet the moving density texture for this test.
domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];original=domain.data.materials[0];quiet=original.copy();quiet.name='S05_v009_QuietAmberFluid';quiet.node_tree.animation_data_clear();vol=next(n for n in quiet.node_tree.nodes if n.type=='PRINCIPLED_VOLUME')
for link in list(vol.inputs['Density'].links):quiet.node_tree.links.remove(link)
vol.inputs['Density'].default_value=2.5;domain.data.materials[0]=quiet
fx=bpy.data.collections.new('S05_TRACKED_COHORT_v009');s.collection.children.link(fx);tracks=[]
for i,(dz,side,depth) in enumerate([(.022,-.005,-.002),(0,.006,.002),(-.022,-.002,.004)]):
 old=bpy.data.objects[f'S05_v007_SuspendedCutting_{i:02}'];old.hide_render=True;old.hide_viewport=True
 rock=old.copy();rock.data=old.data.copy();rock.animation_data_clear();rock.name=f'S05_v009_TrackedFragment_{i:02}';rock.hide_render=False;rock.hide_viewport=False;rock.parent=None;fx.objects.link(rock)
 heads=[]
 for f in range(1,73):
  t=(f-1)/24;z=.005+.17*t+dz;p,u,v,rr,rt=frame_at(z,t);p+=side*v+depth*u
  rock.location=p;rock.rotation_euler=(i*.7+.16*t,.4+i+.12*t,.3-.15*t);rock.scale=(1,1,1)
  for prop in ['location','rotation_euler']:rock.keyframe_insert(prop,frame=f)
  heads.append(list(p))
 linear(rock);tracks.append({'name':rock.name,'heads':heads,'axial_offset_m':dz,'side_offset_m':side,'depth_offset_m':depth,'support_diameter_mm':2*max(v.co.length for v in rock.data.vertices)*1000})
# Same fixed viewing direction; a modestly tighter fixed lens centres this passage.
cam=s.camera;cam.animation_data_clear();cam.data.lens=58
# Offset the fixed camera parallel to its image plane to centre the complete track.
s.frame_set(36);bpy.context.view_layer.update();mid=Vector((0,0,0))
for rec in tracks:mid+=Vector(rec['heads'][35])/3
local=cam.matrix_world.inverted()@mid;cam.location+=cam.matrix_world.to_quaternion()@Vector((local.x,local.y,0))
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
