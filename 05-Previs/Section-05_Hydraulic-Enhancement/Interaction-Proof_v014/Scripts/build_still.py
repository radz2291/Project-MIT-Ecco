import bpy,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_amber-cuttings_v014.blend'
assert not OUT.exists() and Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v013'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_AmberCuttings_StillReview_v014'
trail=bpy.data.materials['S05_v008_SoftAmberWisp'];color=list(next(n for n in trail.node_tree.nodes if n.type=='BSDF_DIFFUSE').inputs['Color'].default_value);copies={}
for o in bpy.data.collections['S05_TRACKED_COHORT_v013'].objects:
 for slot in o.material_slots:
  old=slot.material
  if old.name not in copies:
   new=old.copy();new.name=old.name.replace('v008','v014');p=new.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=color;new.diffuse_color=color;copies[old.name]=new
  slot.material=copies[old.name]
s.frame_set(48);s.render.filepath=str(B/'Previews/amber-cuttings_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
s['proof_scope']='v014 matte rock fragments match the trail amber color; inherited 50 percent larger rocks and longer v012 trails; still approval only.'
result={'prior_v013_sha256':prior_hash,'matched_linear_RGBA':color,'rocks_linear_size_multiplier':1.5,'trail_width_relative_v010':1.35,'trail_length_relative_v010':1.875,'still_frame':48,'render_seconds':dt,'geometry_camera_and_motion_unchanged_from_v013':True,'animation_rendered':False,'treatment':'Same base amber for all rock material slots and trail diffuse shader; rocks retain matte roughness and geometry shading, no emission added.'}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/amber-cuttings_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
