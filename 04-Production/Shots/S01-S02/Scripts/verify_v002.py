import bpy,json,time,os
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
s=bpy.context.scene
records=json.loads((Q/'Notes/integration_v002.json').read_text())
checks={'missing_libraries':[l.filepath for l in bpy.data.libraries if not os.path.exists(bpy.path.abspath(l.filepath))], 'reveal_groups':[n.name for n in bpy.data.node_groups if n.library and 'Surface' in n.name], 'events':[]}
for e in records['events']:
 ob=bpy.data.objects[e['object']];counts=[]
 for f in [e['start']-1,e['start']+3,e['echo_start']+2,e['receipt']+2]:
  s.frame_set(f);ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();counts.append([f,len(me.vertices)]);ev.to_mesh_clear()
 checks['events'].append({'event':e['event'],'samples':counts,'pass':counts[0][1]==counts[-1][1]==0 and counts[1][1]>0 and counts[2][1]>0})
wall=bpy.data.objects['ONE WALL - old history and current cells share topology'];checks['reveal_samples']=[]
for f in [299,318,319,360,361,441,480,528]:
 s.frame_set(f);ev=wall.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();checks['reveal_samples'].append([f,len(me.polygons)]);ev.to_mesh_clear()
# Sample actual local physical bore for radial fit. Cutaway excludes some directions;
# report uncovered rays separately rather than claiming full circumferential certification.
physical=bpy.data.objects.get('S02 geological wall retained section')
if physical and physical.type=='MESH':
 tree=BVHTree.FromPolygons([physical.matrix_world@v.co for v in physical.data.vertices],[list(p.vertices) for p in physical.data.polygons],all_triangles=False)
 fit=[]
 for f in [240,300,432,528]:
  s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();tested=outside=uncovered=0;worst=-1;names=set()
  for ins in dg.object_instances:
   ob=ins.object
   if not ins.is_instance or not ins.parent or ins.parent.original.name!='BHA sequence assembly' or ob.type!='MESH' or ob.hide_render or 'CUTTER' in ob.name:continue
   me=ob.data
   for v in list(me.vertices)[::max(1,len(me.vertices)//60)]:
    p=ins.matrix_world@v.co;r=(p.x*p.x+p.y*p.y)**.5
    if r<.001:continue
    axis=Vector((0,0,p.z));direction=Vector((p.x,p.y,0)).normalized();hit,normal,index,distance=tree.ray_cast(axis,direction,2.)
    if hit is None:uncovered+=1;continue
    tested+=1;error=r-distance;worst=max(worst,error)
    if error>.0005:outside+=1;names.add(ob.name)
  fit.append({'frame':f,'tested':tested,'outside_samples':outside,'uncovered_cutaway':uncovered,'worst_radial_excess_m':worst,'objects_outside':sorted(names)})
 checks['fit']=fit
(Q/'Notes/verification_v002.json').write_text(json.dumps(checks,indent=2))
result=checks
