"""Preserve tested v004; publish linked axial slivers/dashes for moving readability."""
import bpy,sys,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
from build_hydraulics_v001 import OWN,S,E,save,snapshot,dump,material
from hydraulics_controls_v001 import add_tracers
assert not (OWN/'Hydraulics_v003.blend').exists(),'Candidate exists; preserve it and choose new versions before rebuilding'
assert all(not (S/('Flow_reuse_'+k+'_v005.blend')).exists() for k in ['A','B'])
bpy.ops.wm.open_mainfile(filepath=str(OWN/'Hydraulics_v002.blend'),load_ui=False,use_scripts=False)
col=bpy.data.collections['HYDRAULICS_GEOMETRY'];col['version']='v003';col['revision']='Matte cuttings length6mm, radial extent unchanged0.7mm; sliding amber dashes length12mm/radial0.45mm. No source-hardware or path geometry change.'
me=col.objects['CUTTING_GEOMETRY'].data
for v in me.vertices:
 if abs(v.co.x)>.0001:v.co.x=.003 if v.co.x>0 else -.003
mat=me.materials[0];mat.diffuse_color=(.07,.045,.025,1);bs=mat.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.07,.045,.025,1);bs.inputs['Roughness'].default_value=.90
amber=material('FLOW_SlidingAmber',(.95,.42,.06),.65)
vs=[(.006,0,0),(-.006,0,0),(0,.00045,0),(0,-.00045,0),(0,0,.00045),(0,0,-.00045)];fs=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(2,0,5),(1,2,5),(3,1,5),(0,3,5)]
me=bpy.data.meshes.new('FLOW_TRACER_GEOMETRY');me.from_pydata(vs,[],fs);me.materials.append(amber);o=bpy.data.objects.new('FLOW_TRACER_GEOMETRY',me);col.objects.link(o);o.hide_render=True;o.hide_viewport=True
save(OWN/'Hydraulics_v003.blend')
for kind in ['A','B']:
 bpy.ops.wm.open_mainfile(filepath=str(S/('Flow_reuse_'+kind+'_v004.blend')),load_ui=False,use_scripts=False);bpy.context.scene.frame_set(1);before=snapshot()
 for lib in list(bpy.data.libraries):
  if Path(lib.filepath.replace('\\','/')).name=='Hydraulics_v002.blend':lib.filepath=bpy.path.relpath(str(OWN/'Hydraulics_v003.blend'),start=str(S));lib.reload()
 with bpy.data.libraries.load(str(OWN/'Hydraulics_v003.blend'),link=True) as (a,b):b.collections=['HYDRAULICS_GEOMETRY']
 source=b.collections[0];root=bpy.data.objects['FLOW_PLACEMENT'];ctrl=bpy.data.objects['FLOW_CONTROL'];col=bpy.data.collections['FLOW_LOCAL_WRAPPERS'];paths=sorted([o for o in col.objects if o.name.startswith('FLOW_FLOW_PATH_')],key=lambda o:o.name)
 add_tracers(source,root,ctrl,paths,col);ctrl.update_tag();bpy.context.scene.frame_set(1);bpy.context.view_layer.update();after=snapshot();assert before==after
 save(S/('Flow_reuse_'+kind+'_v005.blend'));dump(E/('reuse_'+kind+'_migration_v005.json'),dict(before=before,after=after,preserved_camera_timing_animation_controls=True,revision='One shared cutting-mesh axial-length/material revision via library reload + reusable linked sliding-dash wrapper migration. Source paths/hardware unchanged.',source='Hydraulics_v002.blend',successor='Hydraulics_v003.blend'))
print('T48_READABILITY_SUCCESSOR_SAVED')
