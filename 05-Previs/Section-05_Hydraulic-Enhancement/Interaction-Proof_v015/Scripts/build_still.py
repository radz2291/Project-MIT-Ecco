import bpy,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];s=bpy.context.scene;OUT=B/'Scenes/S05_restrained-fog_v015.blend'
assert not OUT.exists() and Path(bpy.data.filepath).parent.parent.name=='Interaction-Proof_v014'
prior=Path(bpy.data.filepath);prior_hash=hashlib.sha256(prior.read_bytes()).hexdigest();bpy.ops.wm.save_as_mainfile(filepath=str(OUT));s.name='S05_RestrainedFog_StillReview_v015'
domain=bpy.data.objects['S05_v007_AnnularFluidDomain'];old=domain.data.materials[0];m=old.copy();m.name='S05_v015_RestrainedAmberFluid';domain.data.materials[0]=m
n=m.node_tree.nodes;l=m.node_tree.links;vol=next(n for n in n if n.type=='PRINCIPLED_VOLUME');link=vol.inputs['Density'].links[0];source=link.from_socket;l.remove(link);factor=n.new('ShaderNodeMath');factor.name='v015_FogStrength_80percent';factor.operation='MULTIPLY';factor.inputs[1].default_value=.8;l.new(source,factor.inputs[0]);l.new(factor.outputs[0],vol.inputs['Density'])
mix=next(n for n in n if n.type=='MIX_SHADER');old_alpha=mix.inputs[0].default_value;mix.inputs[0].default_value=old_alpha*.8
s.frame_set(48);s.render.filepath=str(B/'Previews/restrained-fog_still.png');t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
if dt>=5:
 s.eevee.taa_render_samples=6;t=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-t
assert dt<5
s['proof_scope']='v015 reduce amber fog density and interface tint strength by 20 percent; rocks and trails unchanged; still approval only.'
result={'prior_v014_sha256':prior_hash,'fog_density_multiplier':.8,'old_surface_alpha':old_alpha,'new_surface_alpha':mix.inputs[0].default_value,'preserved':['amber hue','animated density pattern and movement','rock and trail materials and geometry','hardware and borehole','camera and lighting'],'still_frame':48,'render_seconds':dt,'animation_rendered':False}
(B/'Records/still-build.json').write_text(json.dumps(result,indent=2));s.render.filepath='//../Previews/restrained-fog_still.png';bpy.ops.wm.save_as_mainfile(filepath=str(OUT))
