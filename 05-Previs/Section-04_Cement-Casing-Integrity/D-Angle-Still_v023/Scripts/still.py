import bpy,json,math,time,hashlib,sys
from pathlib import Path
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];SRC=B.parent/'Cinematic-Previs_v022/Scenes/S04_complete_v022.blend'
def geo(s):return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'}
def pose(eye,target):
 f=(target-eye).normalized();r=Vector((0,1,0));r=(r-f*r.dot(f)).normalized();u=(-f).cross(r).normalized();return Matrix((r,u,-f)).transposed().to_quaternion()
bpy.ops.wm.open_mainfile(filepath=str(SRC),use_scripts=False,load_ui=False);s=bpy.context.scene;s.name='S04 D reference-angle still v023';before=geo(s);s.frame_set(355);bpy.context.view_layer.update()
cam=s.camera;cam.animation_data_clear();cam.data=cam.data.copy();cam.data.animation_data_clear();cam.rotation_mode='QUATERNION';cam.data.clip_start=.0005
sx=bpy.data.objects['WORLD_CONTROL']['travel_m']+.7300000190734863
ghost=bpy.data.materials['ECCO D explanatory transparent housing'];ghost.node_tree.animation_data_clear();ghost.node_tree.nodes['Housing opacity - sensor remains solid'].outputs[0].default_value=1
light=bpy.data.lights.new('Reference angle soft inspection key','SUN');light.energy=.65;light.angle=.4;light.use_shadow=False;lo=bpy.data.objects.new(light.name,light);s.collection.objects.link(lo);lo.rotation_euler=Vector((0,-1,.5)).to_track_quat('-Z','Y').to_euler()
# Keep engineering geometry and true gap. Only the camera and local preview lights change.
rows=[]
for i,(dx,y,z,lens) in enumerate([(.07,.15,-.03,14)]):
 cam.location=(sx+dx,y,z);target=Vector((sx,.146,0));cam.rotation_quaternion=pose(cam.location,target);cam.data.lens=lens;cam.data.shift_x=0;cam.data.shift_y=0;bpy.context.view_layer.update()
 s.render.filepath=str(B/'Previews'/f'S04_D_candidate_{i}_v023.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
 rows.append({'candidate':i,'seconds':dt,'eye_m':list(cam.location),'target_m':list(target),'lens_mm':lens,'sensor_projection':list(world_to_camera_view(s,cam,Vector((sx,.129,0)))),'contact_projection':list(world_to_camera_view(s,cam,Vector((sx,.1626,0))))})
 if dt>=5:raise RuntimeError('Frame time cap exceeded')
assert before==geo(s)
(B/'Records/candidates.json').write_text(json.dumps(rows,indent=2))
# Save a review scene with candidate zero. No movie-camera integration.
r=rows[0];cam.location=r['eye_m'];cam.rotation_quaternion=pose(cam.location,Vector(r['target_m']));cam.data.lens=r['lens_mm'];s['scope']='Still-only test of owner reference angle. Opaque ECCO; worn steel wall, no rock substitution. Full v022 path not integrated.'
out=B/'Scenes/S04_D_reference-angle_v023.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
(B/'Records/build.json').write_text(json.dumps({'source':str(SRC),'source_sha256':hashlib.sha256(SRC.read_bytes()).hexdigest(),'physical_meshes_unchanged':True,'housing_opaque':True,'source_frame':355,'no_animation_integration':True,'native':str(out)},indent=2))
