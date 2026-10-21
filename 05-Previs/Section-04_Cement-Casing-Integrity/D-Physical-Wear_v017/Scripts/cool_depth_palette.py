import bpy,json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1];old=B.parent/'D-Physical-Wear_v016/Scenes/S04_D_computed-wear-heatmap_v016.blend'
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D geometry-computed wear heatmap v016'];bpy.context.window.scene=s
steel=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'))
def snapshot():
 return {'meshes':{o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'lights':{o.name:[list(o.location),o.data.energy] for o in s.objects if o.type=='LIGHT'},'curves':{o.name:hashlib.sha256(repr([[tuple(p.co) for p in sp.points] for sp in o.data.splines]).encode()).hexdigest() for o in s.objects if o.type=='CURVE' and not o.hide_render},'depth_values':[d.value for d in steel.data.attributes['ComputedWearDepth_m'].data]}
before=snapshot()
m=steel.data.materials[0].copy();m.name='Satin steel plus computed wear depth - cool blue cyan';steel.data.materials[0]=m
ramp=next(n for n in m.node_tree.nodes if n.type=='VALTORGB')
palette=[(0,(.025,.10,.17,1)),(.25,(.025,.24,.35,1)),(.60,(.035,.46,.62,1)),(1,(.16,.68,.83,1))]
assert len(ramp.color_ramp.elements)==len(palette)
for e,(position,color) in zip(ramp.color_ramp.elements,palette):
 assert abs(e.position-position)<1e-6
 e.color=color
after=snapshot();assert before==after
s.name='D computed wear depth - cool palette v017';s['scope']='Owner applies agreed single cool-family depth palette. Color-only revision; calculation/lines/geometry/camera unchanged. One still, no animation/full integration.'
s['palette_meaning']='Shallow slate blue to deeper cyan-blue and strongest icy cyan. Same computed geometric steel-loss depth, not temperature or field data. Existing geometry-derived fade and satin shading retained.'
out=B/'Scenes/S04_D_cool-wear-depth_v017.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_cool-wear-depth_v017.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps({'source':str(old),'render_seconds':elapsed,'under_5_seconds':elapsed<5,'mesh_camera_lights_lines_depth_attribute_exactly_unchanged':before==after,'palette_only_revision':True,'palette':palette,'depth_range_m':[min(before['depth_values']),max(before['depth_values'])],'data_attribute':'ComputedWearDepth_m','line_graphic_cutoff_m':.00010,'line_cutoff_not_instrument_threshold':True,'same_color_ramp_positions':True,'same_shader_fade_and_intensity':True,'no_extra_glow_or_displacement':True},indent=2));print('COOL_DEPTH_SECONDS',elapsed,flush=True)
