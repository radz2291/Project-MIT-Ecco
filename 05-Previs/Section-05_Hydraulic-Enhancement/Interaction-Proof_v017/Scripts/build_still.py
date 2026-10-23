import bpy,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_rich-amber_v017.blend'
assert not OUT.exists() and Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v016'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_RichAmber_StillReview_v017'
domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];fog=domain.data.materials[0].copy();fog.name='S05_v017_BalancedAmberFluid';domain.data.materials[0]=fog
factor=fog.node_tree.nodes['v016_FogStrength_32percent'];factor.name='v017_FogStrength_44percent';factor.inputs[1].default_value=.44;next(n for n in fog.node_tree.nodes if n.type=='MIX_SHADER').inputs[0].default_value=.011
color=(1.0,.48,.035,1.0);trail=bpy.data.materials['S05_v008_SoftAmberWisp'].copy();trail.name='S05_v017_RichAmberWisp';next(n for n in trail.node_tree.nodes if n.type=='BSDF_DIFFUSE').inputs['Color'].default_value=color;trail.diffuse_color=color
for o in bpy.data.collections['S05_INTERNAL_WISPS_v012'].objects:o.data.materials[0]=trail
copies={}
for o in bpy.data.collections['S05_TRACKED_COHORT_v013'].objects:
 for slot in o.material_slots:
  old=slot.material
  if old.name not in copies:
   new=old.copy();new.name=old.name.replace('v014','v017');new.node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=color;new.diffuse_color=color;copies[old.name]=new
  slot.material=copies[old.name]
s.frame_set(48);s.render.filepath=str(B/'Previews/rich-amber_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
s['proof_scope']='v017 slightly restored fog and richer matching amber rocks/trails; still approval only.'
result={'prior_v016_sha256':prior_hash,'fog_strength_relative_v014':.44,'previous_fog_strength':.32,'surface_alpha':.011,'old_rock_trail_linear_RGBA':[.78,.55,.27,1],'new_rock_trail_linear_RGBA':list(color),'still_frame':48,'render_seconds':dt,'samples':s.eevee.taa_render_samples,'animation_rendered':False,'preserved':['all geometry and sizes','camera and lighting','rock and trail opacity/roughness','all motion','no added emission']}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/rich-amber_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
