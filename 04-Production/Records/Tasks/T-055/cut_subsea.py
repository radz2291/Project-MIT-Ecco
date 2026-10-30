"""Illustrative axial viewing opening; preserves v004 and original sources."""
import bpy,json,math
from pathlib import Path
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets/Surface'
src=A/'Surface_descent_v004.blend';dest=A/'Surface_descent_v005.blend'
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
bpy.ops.mesh.primitive_cylinder_add(vertices=64,radius=.45,depth=140,location=(0,0,-55))
cutter=bpy.context.object;cutter.name='T055 temporary axial viewing cutter'
targets=[o for o in bpy.data.collections['SURFACE_SUBSEA_v004'].objects if o.name in ['RIG_MarineRiser','SUBSEA_Foundation'] or o.name.startswith(('SUBSEA_BOPStack','SUBSEA_RiserCoupling'))]
records=[]
for o in targets:
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('Illustrative axial viewing opening','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=cutter
 before=len(o.data.polygons);bpy.ops.object.modifier_apply(modifier=mod.name)
 records.append({'object':o.name,'before_faces':before,'after_faces':len(o.data.polygons)})
bpy.data.objects.remove(cutter,do_unlink=True)
# A bounded near-side wedge accommodates the locked impossible-camera approach.
# Keep upper water-column silhouette and the original full v004 package intact.
ring=[(0,0)]+[(2*math.cos(math.radians(a)),2*math.sin(math.radians(a))) for a in range(-85,-34,5)]
n=len(ring);verts=[(x,y,z) for z in [-121,-100] for x,y in ring]
faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
mesh=bpy.data.meshes.new('Temporary camera access wedge');mesh.from_pydata(verts,[],faces);mesh.update()
wedge=bpy.data.objects.new('Temporary camera access wedge',mesh);bpy.context.scene.collection.objects.link(wedge)
for o in targets:
 if o.name=='SUBSEA_Foundation':continue
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
 mod=o.modifiers.new('Local near-camera section','BOOLEAN');mod.operation='DIFFERENCE';mod.solver='EXACT';mod.object=wedge
 bpy.ops.object.modifier_apply(modifier=mod.name)
bpy.data.objects.remove(wedge,do_unlink=True)
bpy.context.scene['viewing_opening']='Illustrative0.45m axial opening through riser/BOP/base plus near-side50degree wedge only z-121..-100; original v004 and supplied sources preserved. Camera access, not certified internal hardware.'
bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
for sid in ['S01','S02']:
 p=T/'Consumers'/f'{sid}_shared-descent_v001.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
 for lib in bpy.data.libraries:
  if Path(bpy.path.abspath(lib.filepath)).name==src.name:lib.filepath=str(dest);lib.reload()
 out=T/'Consumers'/f'{sid}_shared-descent_v002.blend'
 for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
 bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(T/'Evidence/axial-opening.json').write_text(json.dumps({'radius_m':.45,'near_side_wedge':{'azimuth_degrees':[-85,-35],'z_m':[-121,-100],'radius_m':2,'foundation_excluded':True},'source':str(src.relative_to(R)),'candidate':str(dest.relative_to(R)),'objects':records},indent=2));print('AXIAL_OPENING_DONE')
