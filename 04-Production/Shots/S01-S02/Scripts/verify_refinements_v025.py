"""Cold-reopen preservation and radial solid-boundary checks."""
import bpy,json,math,os
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
def camera_samples():
 s=bpy.context.scene;rows=[]
 for f in [1,94,95,120,240,300,360,420,474,480,520,550,600,620,650,700,720,756]:
  s.frame_set(f);rows.append(([float(x) for row in s.camera.matrix_world for x in row],s.camera.data.lens))
 return rows
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v024.blend'),use_scripts=False)
baseline=camera_samples();w=bpy.data.objects['ONE WALL - old history and current cells share topology']
attrs={name:[x.value for x in w.data.attributes[name].data] for name in ['ecco_receipt_frame','ecco_reveal_order']}
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v025.blend'),use_scripts=False)
current=camera_samples();assert baseline==current
w=bpy.data.objects['ONE WALL - old history and current cells share topology']
assert all(attrs[name]==[x.value for x in w.data.attributes[name].data] for name in attrs)
missing=[bpy.path.abspath(lib.filepath) for lib in bpy.data.libraries if not os.path.isfile(bpy.path.abspath(lib.filepath))];assert not missing
anchor=Vector((0,0,-729.5));vertices=[];polygons=[]
for name in ['SHOT WORLD | WORLD_S02_PHYSICAL_CUTAWAY_MESH']+[f'SHOT WORLD | WORLD_FRONT_UNIT_05_HALF_{i}' for i in range(2)]:
 ob=bpy.data.objects[name];off=len(vertices);vertices.extend(ob.matrix_world@v.co-anchor for v in ob.data.vertices);polygons.extend(tuple(off+i for i in p.vertices) for p in ob.data.polygons)
bvh=BVHTree.FromPolygons(vertices,polygons)
def clearance(points):
 values=[];uncovered=0
 for p in points:
  r=math.hypot(p.x,p.y)
  if r<.001:continue
  d=Vector((p.x/r,p.y/r,0));hit=bvh.ray_cast(Vector((0,0,p.z))-anchor,d,.6)
  if hit[0] is None:uncovered+=1
  else:values.append(hit[3]-r)
 return {'samples':len(values),'uncovered':uncovered,'minimum_radial_clearance_mm':min(values)*1000,'penetrations_over_0_1mm':sum(x<-.0001 for x in values)}
rows=[]
for f in [520,550,600,650,700,756]:
 bpy.context.scene.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();row={'frame':f}
 for name,label in [(w.name,'wall'),('Shared fine measurement display','overlay')]:
  ob=bpy.data.objects[name];ev=ob.evaluated_get(dg);m=ev.to_mesh();step=max(1,len(m.vertices)//24000)
  row[label]=clearance([ev.matrix_world@m.vertices[i].co for i in range(0,len(m.vertices),step)])
  if label=='overlay':
   a=m.attributes.get('ecco_contour_birth');row['contour_birth_attribute']=bool(a)
   row['soft_materials']=[x.name for x in m.materials if x and 'soft build' in x.name]
  ev.to_mesh_clear()
 rows.append(row)
assert all(r[k]['penetrations_over_0_1mm']==0 for r in rows for k in ['wall','overlay']),rows
record={'cold_reopen':True,'camera_samples_unchanged':len(current),'reveal_face_attributes_unchanged':True,'missing_libraries':missing,'clearance_samples':rows,'scope':'Radial rays against retained physical wall plus actual closed-front source geometry; evaluated wall and overlay include reveal offsets and major-ring thickness. Not engineering certification.'}
(Q/'Notes/refinements_v025_verification.json').write_text(json.dumps(record,indent=2));print(json.dumps(record))
