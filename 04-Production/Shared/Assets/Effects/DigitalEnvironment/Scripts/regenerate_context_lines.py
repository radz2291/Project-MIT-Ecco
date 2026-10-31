# ECCO_RUNTIME_PATH_MIGRATION_20261031
"""Derive contextual lines from actual World cap; preserve all data surfaces.

Separate v004 consumer. Regenerate after changing pinned World shape. This is
an explicit derived representation, not a claim of live baked-curve updates.
"""


def _ecco_repo_root():
    from pathlib import Path
    for candidate in Path(__file__).resolve().parents:
        if (candidate / '04-Production').is_dir():
            return candidate
    raise RuntimeError('ECCO repository root not found')

import bpy,json,math,bisect,hashlib
from pathlib import Path
from collections import defaultdict
from mathutils import Vector
R=_ecco_repo_root();T=R/'04-Production/Records/Tasks/T-054';src=T/'Consumers/S03_shared-digital_v003.blend';dst=T/'Consumers/S03_shared-digital_v004.blend';W=R/'04-Production/Shared/Assets/Environment/Borehole/World_environment_v010.blend'
import argparse
p=argparse.ArgumentParser();p.add_argument('--consumer-source',required=True);p.add_argument('--consumer-output',required=True);p.add_argument('--shared-output',required=True);p.add_argument('--evidence-output',required=True)
import sys
opts=p.parse_args(sys.argv[sys.argv.index('--')+1:]);src=Path(opts.consumer_source).resolve();dst=Path(opts.consumer_output).resolve();assert not dst.exists() and not Path(opts.shared_output).exists(),'Choose new successor outputs; never overwrite verified files'
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);s=bpy.context.scene;s.frame_set(1)
assert not bpy.data.collections.get('ECCO World-derived contextual cap lines v004'), 'Use retained v003 generation template, not already-linked v004 successor'
from mathutils import Matrix, Euler
ob=bpy.data.objects['S03 | physical World live context']
transform=next(n for n in ob.modifiers[0].node_group.nodes if n.bl_idname=='GeometryNodeTransform')
M=Euler(tuple(transform.inputs['Rotation'].default_value)).to_matrix().to_4x4()
world_object=next(o for o in bpy.data.objects if o.name=='FORMATION_IRREGULAR_CUTAWAY' and o.library and Path(bpy.path.abspath(o.library.filepath)).resolve()==W.resolve())
mesh=world_object.data;angles=97;radial=41;rows=len(mesh.vertices)//(2*(angles+radial))
assert not world_object.modifiers, 'Unregistered source modifiers require topology adapter update'
assert len(mesh.vertices)==2*rows*angles+2*rows*radial, 'Source cap topology changed; fail closed'
cap_first_polygon=2*(rows-1)*(angles-1);cap_first_vertex=2*rows*angles
assert len(mesh.polygons)==cap_first_polygon+2*(rows-1)*(radial-1), 'Source polygon layout changed'
assert all(all(v>=cap_first_vertex for v in p.vertices) for p in list(mesh.polygons)[cap_first_polygon:])
mesh.calc_loop_triangles();triangles=[]
for t in mesh.loop_triangles:
 if t.polygon_index<cap_first_polygon:continue
 points=[M@world_object.matrix_world@mesh.vertices[i].co for i in t.vertices]
 normal=(points[1]-points[0]).cross(points[2]-points[0]).normalized()
 if normal.y>0:normal=-normal
 triangles.append((points,normal))
source_topology={'grid_rows':rows,'grid_angles':angles,'radial_cap_vertices':radial,'cap_first_polygon':cap_first_polygon,'cap_first_vertex':cap_first_vertex,'vertices':len(mesh.vertices),'polygons':len(mesh.polygons),'rule':'Explicit cap grids from build_formation_revision_v005.mass; asserted layout. Extent-coordinate edits allowed; topology changes fail closed.'}
def source_planes(name,axis):
 values=[]
 for spline in bpy.data.objects[name].data.splines:
  pts=[bpy.data.objects[name].matrix_world@Vector(p.co[:3]) for p in spline.points]
  if pts:values.append(round(sum(p[axis] for p in pts)/len(pts),4))
 return sorted(set((0.0001 if axis==2 and abs(v)<1e-8 else v) for v in values if (-8<v<10 if axis==2 else -6.001<v<6.001)))

def key(v):return tuple(round(x,5) for x in v)

def line_chains(segments):
 positions={};normals=defaultdict(lambda:Vector());adj=defaultdict(set);edge_set=set()
 for a,b,n in segments:
  ka,kb=key(a),key(b)
  if ka==kb:continue
  edge=tuple(sorted((ka,kb)))
  if edge in edge_set:continue
  edge_set.add(edge);positions[ka]=a;positions[kb]=b;normals[ka]+=n;normals[kb]+=n;adj[ka].add(kb);adj[kb].add(ka)
 remaining=set(edge_set);chains=[]
 for start in sorted(adj,key=lambda k:(len(adj[k])==2,k)):
  for nxt in list(adj[start]):
   edge=tuple(sorted((start,nxt)))
   if edge not in remaining:continue
   path=[start];prev=start;current=nxt;remaining.remove(edge)
   while True:
    path.append(current);choices=[q for q in adj[current] if tuple(sorted((current,q))) in remaining]
    if not choices:break
    following=choices[0];remaining.remove(tuple(sorted((current,following))));prev,current=current,following
    if current==start:path.append(start);break
   if len(path)>1:chains.append([positions[k]+normals[k].normalized()*.003 for k in path])
 return chains,{'segments':len(edge_set),'branch_vertices':sum(len(a)>2 for a in adj.values()),'endpoints':sum(len(a)==1 for a in adj.values())}

records=[]; created=[]
for name,axis in [('Luminous geological strata',2),('Subordinate formation survey grid',0)]:
 old=bpy.data.objects[name];planes=source_planes(name,axis)
 if not planes:raise RuntimeError('No source planes '+name)
 byplane=defaultdict(list)
 for points,normal in triangles:
  mn=min(p[axis] for p in points);mx=max(p[axis] for p in points)
  for value in planes[bisect.bisect_left(planes,mn):bisect.bisect_right(planes,mx)]:
   hits=[]
   for a,b in zip(points,points[1:]+points[:1]):
    da=a[axis]-value;db=b[axis]-value
    if abs(da)<1e-8:hits.append(a)
    if da*db<0:hits.append(a.lerp(b,da/(da-db)))
   unique={key(p):p for p in hits}
   if len(unique)<2:continue
   pair=max(((a,b) for a in unique.values() for b in unique.values()),key=lambda pair:(pair[0]-pair[1]).length)
   byplane[value].append((*pair,normal))
 curve=bpy.data.curves.new(name+' | cap intersection v004','CURVE');curve.dimensions='3D';curve.resolution_u=1;curve.bevel_depth=old.data.bevel_depth;curve.bevel_resolution=0;curve.materials.append(old.data.materials[0]);new=bpy.data.objects.new(name+' | World intersection v004',curve);s.collection.objects.link(new);created.append(new);stats=[]
 for value in planes:
  chains,stat=line_chains(byplane[value]);lengths=[]
  for chain in chains:
   length=sum((b-a).length for a,b in zip(chain,chain[1:]))
   if length<.02:continue
   spline=curve.splines.new('POLY');spline.points.add(len(chain)-1)
   for q,p in zip(spline.points,chain):q.co=(*p,1)
   lengths.append(length)
   assert not (min(p.x for p in chain)<-.01 and max(p.x for p in chain)>.01), 'Context chain crosses hole'
  stats.append({'plane':value,'chains':len(lengths),'length_m':sum(lengths),**stat})
 old.hide_render=True
 for other in bpy.data.objects:
  if other.name.startswith(name+' |') and other!=new:other.hide_render=True
 new['provenance']='Intersection of evaluated shared World cap with source contextual mean-depth/X planes; 3mm averaged cap-normal offset; local data surfaces untouched.'
 new['regenerate_on_world_change']=True;records.append({'source_context':name,'axis':axis,'planes':planes,'curve':new.name,'stats':stats})
shared_path=Path(opts.shared_output).resolve()
collection=bpy.data.collections.new('ECCO World-derived contextual cap lines v004')
for obj in created:collection.objects.link(obj)
collection['world_sha256']=hashlib.file_digest(open(W,'rb'),'sha256').hexdigest()
collection['representation']='Derived S03-context planes; regenerate after World edit. Not measured data.'
collection['coordinate_mapping']='World X->local Z,Y->Y,Z->-X. No scale.'
collection['normal_offset_m']=.003
collection['junction_tiebreak_m']=.0001
bpy.data.libraries.write(str(shared_path),{collection},path_remap='RELATIVE_ALL',fake_user=True)
for obj in created:bpy.data.objects.remove(obj,do_unlink=True)
bpy.data.collections.remove(collection)
with bpy.data.libraries.load(str(shared_path),link=True) as (available,target):target.collections=['ECCO World-derived contextual cap lines v004']
s.collection.children.link(target.collections[0])
bpy.ops.wm.save_as_mainfile(filepath=str(dst));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dst))
report={'candidate':str(dst.relative_to(R)),'source':str(src.relative_to(R)),'world_sha256':hashlib.file_digest(open(W,'rb'),'sha256').hexdigest(),'selected_cap_triangles':len(triangles),'source_topology':source_topology,'selection':'Exact two cap face grids; no heuristic normal or coordinate rejection','offset_m':.003,'junction_tiebreak_m':.0001,'shared_asset':str(shared_path.relative_to(R)),'hole_crossing_chains':0,'representation':'Regenerated derived lines, not live automatic curve geometry','records':records}
Path(opts.evidence_output).write_text(json.dumps(report,indent=2));print('INTERSECTIONS_DONE',len(triangles),[(r['source_context'],len(r['planes']),sum(s['chains'] for s in r['stats'])) for r in records])
