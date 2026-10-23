import bpy,math,json,time,hashlib
from pathlib import Path
from mathutils import Vector,Quaternion
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_combined-interaction_v010.blend'
assert Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v009' and not OUT.exists()
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();assert prior_hash=='5be13c8476c297362cb03ca0fe619313a4c6165b6619868a15991f913bef1b84'
bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_Combined_Interaction_v010';s.frame_end=96;s.eevee.taa_render_samples=8
# Restore the exact animated fluid material from v008, not a reconstruction.
v8=B.parent/'Interaction-Proof_v008/Scenes/S05_internal-flow_v008.blend'
with bpy.data.libraries.load(str(v8),link=False) as (src,dst):dst.materials=['S05_v007_SectionedFluid']
material=dst.materials[0];assert material;domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];domain.data.materials[0]=material
# Extend original linear animation at its established rate rather than freeze at frame 72.
def curves(id):
 if id.animation_data and id.animation_data.action:
  for layer in id.animation_data.action.layers:
   for strip in layer.strips:
    for bag in strip.channelbags:
     yield from bag.fcurves
for id in [material.node_tree,domain]:
 for fc in curves(id):fc.extrapolation='LINEAR'
# Reuse actual linked steel and v004 open-passage route, with v006 partial angular influence.
s.frame_set(1);bpy.context.view_layer.update();vv=[];ff=[]
for o in bpy.data.collections['S05_LINKED_HARDWARE'].objects:
 off=len(vv);vv.extend(o.matrix_world@v.co for v in o.data.vertices);ff.extend([[off+i for i in p.vertices] for p in o.data.polygons])
tree=BVHTree.FromPolygons(vv,ff);R=.155575;OMEGA=-math.radians(5);routes=json.loads((B.parent/'Interaction-Proof_v004/Records/planned-routes.json').read_text());ns=dict(bpy=bpy,math=math,Vector=Vector,tree=tree,R=R,OMEGA=OMEGA,routes=routes)
src=(B.parent/'Interaction-Proof_v006/Scripts/build.py').read_text();exec(src[src.index('def linear('):src.index("fx=bpy.data.collections.new")],ns);frame_at=ns['frame_at'];linear=ns['linear']
oldgroup=bpy.data.collections['S05_TRACKED_COHORT_v009'];oldgroup.hide_render=True;oldgroup.hide_viewport=True
fx=bpy.data.collections.new('S05_TRACKED_COHORT_v010');s.collection.children.link(fx);tracks=[]
# Outer-passage placement uses existing space only. Each finite rock is checked later.
for i,(dz,side,depth) in enumerate([(.022,-.004,.0005),(0,.005,.003),(-.022,-.001,.0045)]):
 old=bpy.data.objects[f'S05_v009_TrackedFragment_{i:02}'];rock=old.copy();rock.data=old.data.copy();rock.animation_data_clear();rock.name=f'S05_v010_TrackedFragment_{i:02}';fx.objects.link(rock);rock.hide_render=False;rock.hide_viewport=False;heads=[]
 for f in range(1,97):
  t=(f-1)/24;z=-.005+.135*t+dz;p,u,v,rr,rt=frame_at(z,t);p+=side*v+depth*u
  rock.location=p;rock.rotation_euler=(i*.7+.16*t,.4+i+.12*t,.3-.15*t);rock.scale=(1,1,1)
  for prop in ['location','rotation_euler']:rock.keyframe_insert(prop,frame=f)
  heads.append(list(p))
 linear(rock);tracks.append({'name':rock.name,'heads':heads,'offsets_m':[dz,side,depth]})
cam=s.camera;cam.animation_data_clear();cam.data.lens=49;az=math.radians(-10);target=Vector((0,0,.26));cam.location=(1.12*math.cos(az),1.12*math.sin(az),.33);cam.rotation_quaternion=(target-cam.location).to_track_quat('-Z','Y')@Quaternion((0,0,1),math.radians(-48))
s.frame_set(48);bpy.context.view_layer.update();s.render.filepath=str(B/'Previews/composition-test.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
result={'prior_v009_sha256':prior_hash,'render_seconds':dt,'tracks':tracks,'fluid_material_restored_from':str(v8),'frames':96,'fps':24,'camera_azimuth_deg':-10,'proof':'Combined moving fluid and persistent tracked cohort; illustrative, not CFD'}
(B/'Records/setup.json').write_text(json.dumps(result,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
