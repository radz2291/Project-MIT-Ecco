import bpy,math,time,json,hashlib,csv
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];old=B.parent/'D-Physical-Wear_v015/Scenes/S04_D_selective-wear-rings_v015.blend'
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D normal rings with local worn arcs v015'];bpy.context.window.scene=s
def snap():
 return {'geometry':{o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},'camera':[list(r) for r in s.camera.matrix_world],'lens':s.camera.data.lens,'lights':{o.name:[list(o.location),o.data.energy] for o in s.objects if o.type=='LIGHT'},'curves':{o.name:hashlib.sha256(repr([[tuple(p.co) for p in sp.points] for sp in o.data.splines]).encode()).hexdigest() for o in s.objects if o.type=='CURVE' and not o.hide_render}}
before=snap();steel=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'))
nom=bpy.data.objects['CASED_STEEL_NOMINAL_CUTAWAY'];tree=BVHTree.FromPolygons([v.co for v in nom.data.vertices],[list(p.vertices) for p in nom.data.polygons])
nominal_vertices=[v.co.copy() for v in nom.data.vertices if math.hypot(v.co.y,v.co.z)<.164]
steel.data=steel.data.copy();attr=steel.data.attributes.new('ComputedWearDepth_m','FLOAT','POINT');rows=[];edge_fallback=0
for v,d in zip(steel.data.vertices,attr.data):
 x,y,z=v.co;rw=math.hypot(y,z);angle=math.atan2(z,y);inner=rw<.164
 if inner:
  ray=Vector((0,math.cos(angle),math.sin(angle)));p=tree.ray_cast(Vector((x,0,0)),ray,1)[0]
  if p is None:
   # Exact section edge: recover the corresponding original angular source sample.
   p=min(nominal_vertices,key=lambda q:abs(math.atan2(q.z,q.y)-angle));edge_fallback+=1
  rn=math.hypot(p.y,p.z);depth=max(0,rw-rn)
  if depth<1e-7:depth=0
 else:rn=None;depth=0
 d.value=depth;rows.append([v.index,x,angle,rw,rn,depth,int(inner)])
with (B/'Records/computed-wear-samples.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['vertex','x_m','azimuth_rad','actual_radius_m','nominal_source_radius_m','computed_loss_depth_m','inner_surface']);w.writerows(rows)
# Change material only: blend a data-color contribution into the existing satin shader.
m=steel.data.materials[0].copy();m.name='Satin steel plus geometry-computed loss-depth heatmap';steel.data.materials[0]=m
nt=m.node_tree;ns=nt.nodes;li=nt.links;output=next(n for n in ns if n.type=='OUTPUT_MATERIAL');old_surface=output.inputs['Surface'].links[0].from_socket
data=ns.new('ShaderNodeAttribute');data.attribute_name='ComputedWearDepth_m';data.label='Computed radial steel loss in metres'
norm=ns.new('ShaderNodeMapRange');norm.clamp=True;norm.inputs['From Min'].default_value=0;norm.inputs['From Max'].default_value=.004;li.new(data.outputs['Fac'],norm.inputs['Value'])
ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='EASE';cr=ramp.color_ramp
cr.elements[0].position=0;cr.elements[0].color=(.025,.16,.40,1)
cr.elements[1].position=1;cr.elements[1].color=(.96,.11,.025,1)
for pos,col in [(.25,(.015,.55,.72,1)),(.60,(.95,.65,.045,1))]:cr.elements.new(pos).color=col
li.new(norm.outputs['Result'],ramp.inputs['Fac'])
fade=ns.new('ShaderNodeMapRange');fade.interpolation_type='SMOOTHSTEP';fade.clamp=True;fade.inputs['From Min'].default_value=.000025;fade.inputs['From Max'].default_value=.004;fade.inputs['To Min'].default_value=0;fade.inputs['To Max'].default_value=.68;li.new(data.outputs['Fac'],fade.inputs['Value'])
em=ns.new('ShaderNodeEmission');em.inputs['Strength'].default_value=.95;li.new(ramp.outputs['Color'],em.inputs['Color'])
mix=ns.new('ShaderNodeMixShader');li.new(fade.outputs['Result'],mix.inputs[0]);li.new(old_surface,mix.inputs[1]);li.new(em.outputs[0],mix.inputs[2]);li.new(mix.outputs[0],output.inputs['Surface'])
assert before==snap()
inner_rows=[r for r in rows if r[-1]];unworn=[r for r in inner_rows if r[1]<-2.31];assert unworn and all(r[5]==0 for r in unworn)
assert max(r[5] for r in rows)<.004001 and all(r[5]==0 for r in rows if not r[-1])
s.name='D geometry-computed wear heatmap v016';s['scope']='One geometry-driven loss-depth heatmap still. Same steel/camera/approved rings. No animation/full integration or measured field result.'
s['heatmap_meaning']='Color and fade are driven by actual-minus-nominal radial source geometry in metres. Not a temperature map, acoustic amplitude map, physical wear simulation or calibrated field measurement. No painted texture/noise mask/displacement.'
out=B/'Scenes/S04_D_computed-wear-heatmap_v016.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_computed-wear-heatmap_v016.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
result={'source':str(old),'render_seconds':elapsed,'under_5_seconds':elapsed<5,'physical_geometry_camera_lights_visible_curves_unchanged':before==snap(),'calculation':'d=max(0,r_actual_inner_mesh-r_nominal_source_intersection), registered axial/azimuth coordinates; values below 0.1 micrometre removed as roundoff','max_computed_loss_m':max(r[5] for r in rows),'unchanged_area_samples':len(unworn),'unchanged_area_depth_exactly_zero':all(r[5]==0 for r in unworn),'outer_surface_depth_exactly_zero':all(r[5]==0 for r in rows if not r[-1]),'section_edge_reference_vertex_fallbacks':edge_fallback,'scalar_attribute':'ComputedWearDepth_m','heat_material_slots':[0],'static_inspection_section_material_unchanged':True,'field_calibration_claim':False,'new_image_textures':False,'new_noise_driven_mask':False,'displacement_or_bump_added':False,'shader_color_scale_m':[0,.004],'shader_fade_range_m':[.000025,.004],'heat_max_mix':.68,'sample_csv':'Records/computed-wear-samples.csv'}
(B/'Records/verification.json').write_text(json.dumps(result,indent=2));print('HEATMAP_SECONDS',elapsed,flush=True)
