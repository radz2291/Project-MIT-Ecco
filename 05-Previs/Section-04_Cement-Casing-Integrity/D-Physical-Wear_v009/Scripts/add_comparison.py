import bpy, math, json, time, hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];OLD=B.parent/'D-Physical-Wear_v008'
srcfile=OLD/'Scenes/S04_D_C_preferred-closeup_v008.blend'
bpy.ops.wm.open_mainfile(filepath=str(srcfile),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only'];bpy.context.window.scene=s
steel=next(o for o in s.objects if o.name.startswith('Actual registered worn steel'))
def snapshot():
 return dict(meshes={o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},camera=[list(r) for r in s.camera.matrix_world],lens=s.camera.data.lens,lights={o.name:dict(matrix=[list(r) for r in o.matrix_world],power=o.data.energy) for o in s.objects if o.type=='LIGHT'})
before=snapshot();source=bpy.data.objects['CASED_STEEL_WEAR_CUTAWAY'];bv=BVHTree.FromPolygons([v.co for v in source.data.vertices],[list(p.vertices) for p in source.data.polygons])
RI=.1589405;plane=-1.5125;front=plane+.00035
def mat(name,rgb):
 m=bpy.data.materials.new(name);m.diffuse_color=(*rgb,1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs['Color'].default_value=(*rgb,1);e.inputs['Strength'].default_value=1.25;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs['Surface']);return m
white=mat('Original inner surface - dashed reference',(.72,.79,.83));cyan=mat('Existing worn inner surface - cyan profile',(.025,.65,.82));amber=mat('Original-to-current geometric difference',(.72,.51,.20))
coll=bpy.data.collections.new('Registered physical comparison - no numeric depth claim');s.collection.children.link(coll)
def line(name,pts,m,width):
 d=bpy.data.curves.new(name,'CURVE');d.dimensions='3D';d.bevel_depth=width;d.bevel_resolution=2;sp=d.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,v in zip(sp.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,d);coll.objects.link(o);d.materials.append(m);return o
def nominal(a):return Vector((front,RI*math.cos(a),RI*math.sin(a)))
def measured(a):
 d=Vector((0,math.cos(a),math.sin(a)));hit=bv.ray_cast(Vector((plane,0,0)),d,1)[0]
 if hit is None:raise RuntimeError('Registered source wall ray missed')
 return Vector((front,hit.y,hit.z))
angles=[-.9+1.8*i/180 for i in range(181)]
line('Actual current inner profile - source registered',[measured(a) for a in angles],cyan,.00020)
for i in range(24):
 a=-.9+1.8*i/24;b=a+1.8/24*.51
 line('Original reference dash %02d'%i,[nominal(a+(b-a)*j/5) for j in range(6)],white,.00014)
n=nominal(0);p=measured(0)
line('Original-current comparison bracket',[n,p],amber,.00014)
for label,pt in [('Original',n),('Current',p)]:line(label+' bracket tick',[pt+Vector((0,0,-.0014)),pt+Vector((0,0,.0014))],amber,.00014)
s['scope']='Owner selected v008 close-up and released matching prior reference/current graphic. One still only. No full D animation or section integration.'
s['meaning']='White dashed original nominal inner surface; cyan source-registered worn inner surface. Amber gap is illustrative geometry difference, not calibrated field wear or wall thickness measured by one echo.'
assert snapshot()==before
out=B/'Scenes/S04_D_physical-comparison_v009.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_physical-comparison_v009.png')
bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps(dict(source=str(srcfile),before_after_physical_scene_identical=snapshot()==before,render_seconds=elapsed,under_5_seconds=elapsed<5,plane_m=plane,graphic_front_offset_m=front-plane,geometric_difference_m=(p-n).length,reference_radius_m=RI,actual_profile_method='Ray hits on original registered source mesh at existing section plane',no_numeric_labels=True,no_sensor_ray_without_sensor=True,snapshot=before),indent=2))
print('COMPARISON_SECONDS',elapsed,flush=True)
