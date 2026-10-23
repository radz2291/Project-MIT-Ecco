import bpy,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_softer-fog_v016.blend'
assert not OUT.exists() and Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v015'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_SofterFog_StillReview_v016'
domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];m=domain.data.materials[0].copy();m.name='S05_v016_SoftAmberFluid';domain.data.materials[0]=m
factor=m.node_tree.nodes['v015_FogStrength_80percent'];factor.name='v016_FogStrength_32percent';factor.inputs[1].default_value=.32
mix=next(n for n in m.node_tree.nodes if n.type=='MIX_SHADER');mix.inputs[0].default_value=.008
s.frame_set(48);s.render.filepath=str(B/'Previews/softer-fog_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t;assert dt<5
s['proof_scope']='v016 fog 60 percent weaker than v015, 32 percent of v014 density and interface tint; rocks and trails unchanged; still approval only.'
result={'prior_v015_sha256':prior_hash,'fog_density_relative_v014':.32,'fog_density_relative_v015':.4,'surface_alpha':.008,'still_frame':48,'render_seconds':dt,'samples':s.eevee.taa_render_samples,'animation_rendered':False,'preserved':['rock and trail materials and geometry','amber hue','fluid movement pattern','all geometry','camera and lighting']}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/softer-fog_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
