import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S04_continuous-camera_v019.blend'),use_scripts=False,load_ui=False);main=bpy.context.scene
physical=[o for o in main.objects if o.type=='MESH' and not o.hide_render and (o.name.startswith('Cement ') or 'organic fluid-filled' in o.name or 'capped true source' in o.name or 'closed source-guided' in o.name)]
def snap():return {o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],tuple(o.matrix_world))).encode()).hexdigest() for o in physical}
baseline=snap();cameras=[];camera_pos=[];states=[];clearances=[]
steel=bpy.data.objects['STEEL - capped true source section'];tree=BVHTree.FromPolygons([v.co.copy() for v in steel.data.vertices],[tuple(p.vertices) for p in steel.data.polygons])
for f in range(1,433):
 main.frame_set(f);bpy.context.view_layer.update();assert snap()==baseline
 cameras.append(main.camera.name);camera_pos.append(main.camera.matrix_world.translation.copy());states.append({o.name:not o.hide_render for o in physical})
 pos=camera_pos[-1];plane=pos.dot(Vector((0,-math.sin(math.radians(39)),math.cos(math.radians(39)))))-.00005
 # A nearest triangle's normal is not a reliable inside test at an annular end edge.
 # Use the known fixed half-plane and a conservative nominal steel annulus instead.
 if plane>0:signed=plane
 elif pos.x>0:signed=pos.x
 elif pos.x<-5.5:signed=-5.5-pos.x
 else:
  radius=math.hypot(pos.y,pos.z);signed=max(.1589405-radius,radius-.1698625)
 clearances.append(signed);assert signed>=-1e-5,('Camera enters conservative steel annulus',f,signed)
assert len(set(cameras))==1 and all(v==states[0] for v in states)
steps=[(b-a).length for a,b in zip(camera_pos,camera_pos[1:])]
libs=[{'path':bpy.path.abspath(l.filepath),'relative':l.filepath.startswith('//'),'exists':Path(bpy.path.abspath(l.filepath)).is_file()} for l in bpy.data.libraries];assert all(r['exists'] for r in libs)
loss=bpy.data.objects['STEEL - capped true source section'].data.attributes['ComputedWearDepth_m'];maxloss=max(x.value for x in loss.data);assert maxloss<.004001
review=bpy.data.scenes.new('S04 REVIEW - continuous main plus C window');review.frame_start=1;review.frame_end=432;review.render.fps=24;review.render.resolution_x=1280;review.render.resolution_y=720;review.render.resolution_percentage=100;review.view_settings.view_transform='Standard'
editor=review.sequence_editor_create();strip=editor.strips.new_image('Uninterrupted main view + entering/exiting comparison C',str(B/'Work/Assembly/S04_0001.png'),channel=1,frame_start=1)
for f in range(2,433):strip.elements.append(f'S04_{f:04d}.png')
strip.directory='//../Work/Assembly/'
review['edit_3D_scene']=main.name;review['C_source']='S04_C_comparison-window_v019.blend';main['review_scene']=review.name
for f,name in [(1,'Continuous entry - fixed half section'),(97,'B physical sensing composition'),(121,'C window enters'),(133,'Synchronized comparison'),(235,'C window exits'),(254,'Same camera continues to wear'),(318,'D inspection arrival'),(361,'Fixed wear values exposed'),(405,'Final hold')]:review.timeline_markers.new(name,frame=f);main.timeline_markers.new(name,frame=f)
review.frame_set(182)
for w in bpy.context.window_manager.windows:
 w.scene=review
 for area in w.screen.areas:
  if area.type=='VIEW_3D':area.type='SEQUENCE_EDITOR';area.spaces.active.view_type='SEQUENCER_PREVIEW'
main_name=main.name
out=B/'Scenes/S04_complete-continuous_v019.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False,load_ui=False);review=bpy.data.scenes['S04 REVIEW - continuous main plus C window'];assert all((Path(bpy.path.abspath(strip.directory))/e.filename).is_file() for strip in review.sequence_editor.strips for e in strip.elements)
master=B.parents[2]/'04-Production/Shared/Assets/CasedHole/CasedHole_v002.blend';master_sha=hashlib.sha256(master.read_bytes()).hexdigest();assert master_sha=='52c14a8f71d9d3c160acbdfaade240f7e699334c3a2ed4bd649cb220b59e49ba'
report={'saved_and_reopened':True,'complete_native':str(out),'physical_scene':main_name,'main_camera_count_over_timeline':len(set(cameras)),'physical_geometry_and_transforms_static':True,'physical_layer_visibility_static':True,'section_fixed_from_first_frame':True,'camera_outside_conservative_steel_annulus_all_frames':True,'clearance_check':'Fixed retained half-plane plus nominal RI/RO annulus; nominal RI is conservative because wear only increases inner radius. Nearest-face signed normal rejected as unreliable at end edges. This is not a complete tool/formation collision audit.','minimum_separating_plane_or_radial_margin_m':min(clearances),'canonical_master_sha256_unchanged':master_sha,'maximum_camera_step_m':max(steps),'camera_step_samples_m':steps,'max_authored_loss_mm':1000*maxloss,'all432_review_images_exist':True,'libraries':libs,'engineering_acceptance':False,'human_motion_review_pending':True}
(B/'Records/verification.json').write_text(json.dumps(report,indent=2));print('PACKAGE VERIFIED')
