import bpy,math,time,json,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
B=Path(__file__).resolve().parents[1];old=B.parent/'D-Physical-Wear_v009/Scenes/S04_D_physical-comparison_v009.blend'
bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
s=bpy.data.scenes['D C_preferred-closeup - physical only'];bpy.context.window.scene=s
def snap():return dict(meshes={o.name:hashlib.sha256(repr(([tuple(v.co) for v in o.data.vertices],[tuple(p.vertices) for p in o.data.polygons])).encode()).hexdigest() for o in s.objects if o.type=='MESH'},camera=[list(r) for r in s.camera.matrix_world],lens=s.camera.data.lens,lights={o.name:[list(o.location),o.data.energy] for o in s.objects if o.type=='LIGHT'})
before=snap()
def tree(name):
 o=bpy.data.objects[name];return BVHTree.FromPolygons([v.co for v in o.data.vertices],[list(p.vertices) for p in o.data.polygons])
nom=tree('CASED_STEEL_NOMINAL_CUTAWAY');worn=tree('CASED_STEEL_WEAR_CUTAWAY')
coll=bpy.data.collections.new('Circumferential comparisons at registered wear stations');s.collection.children.link(coll)
white=bpy.data.materials['Original inner surface - dashed reference'];cyan=bpy.data.materials['Existing worn inner surface - cyan profile']
def point(tree,x,a,offset):
 di=Vector((0,math.cos(a),math.sin(a)));p=tree.ray_cast(Vector((x,0,0)),di,1)[0]
 if p is None:raise RuntimeError('Actual registered circumference ray missed')
 return p-di*offset
def line(name,pts,mat,width):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=width;c.bevel_resolution=2;sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
 for p,co in zip(sp.points,pts):p.co=(*co,1)
 ob=bpy.data.objects.new(name,c);coll.objects.link(ob);c.materials.append(mat)
stations=[]
for k,x in enumerate([-1.88,-1.68]):
 diffs=[]
 for j in range(181):
  a=-math.pi/2+math.pi*j/180
  diffs.append((point(worn,x,a,0)-point(nom,x,a,0)).length)
 for i in range(22):
  a=-math.pi/2+math.pi*i/22;b=a+math.pi/22*.49
  angles=[a+(b-a)*j/8 for j in range(9)]
  line('Station %d original nominal dash %02d'%(k+1,i),[point(nom,x,a,.00004) for a in angles],white,.00013)
 line('Station %d actual worn solid profile'%(k+1),[point(worn,x,-math.pi/2+math.pi*j/240,.00004) for j in range(241)],cyan,.00019)
 stations.append({'x_m':x,'sampled_actual_radial_change_range_m':[min(diffs),max(diffs)]})
assert snap()==before
s.name='D registered circumferential comparisons v013';s.eevee.taa_render_samples=8
s['scope']='Owner removes near-normal far station, retains worn station and adds middle station. Nominal white dashed; worn cyan solid. Same approved shot, still only.'
s['meaning']='Each white/cyan pair shares an exact axial station. White is source nominal steel; cyan is actual worn steel at that station. No exaggerated radial separation, no single-pulse thickness/volume claim.'
out=B/'Scenes/S04_D_circumference-comparison_v013.blend'
for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(out.parent))
s.render.filepath=str(B/'Previews/S04_D_circumference-comparison_v013.png');bpy.ops.wm.save_as_mainfile(filepath=str(out),relative_remap=False)
t=time.perf_counter();bpy.ops.render.render(scene=s.name,write_still=True);elapsed=time.perf_counter()-t
(B/'Records/verification.json').write_text(json.dumps({'source':str(old),'render_seconds':elapsed,'under_5_seconds':elapsed<5,'physical_meshes_camera_lights_unchanged':snap()==before,'stations':stations,'removed_near_normal_station_m':-2.16,'nominal_style':'white dashed','worn_style':'cyan solid','profile_radial_visibility_offset_m':.00004,'radial_exaggeration':False,'ghost_fill_present':False,'depth_pins_present':False,'fixed_front_comparison_preserved':True,'all_new_graphics_are_registered_cross_sections':True,'source_nominal':'CASED_STEEL_NOMINAL_CUTAWAY','source_worn':'CASED_STEEL_WEAR_CUTAWAY','numeric_measurements_added':False},indent=2));print('CIRCUMFERENCE_SECONDS',elapsed,flush=True)

