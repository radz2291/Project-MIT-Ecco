"""Closed equipment-entry trial. No inherited side wedge; authored entry sleeve.
Run background with v007 loaded. v007/v004 remain byte-exact.
"""
import bpy,json,math,hashlib,bmesh,sys
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Surface';Q=R/'04-Production/Shots/S01-S02'
src=B/'Surface_descent_v007.blend';original=R/'04-Production/Shared/Archive/2026-10-31/Assets/Surface/Surface_descent_v004.blend';dst=B/'Surface_descent_v008.blend';assert not dst.exists() or '--replace-unpublished' in sys.argv
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [src,original]}
col=bpy.data.collections['SURFACE_SUBSEA_v004']
targets=[o for o in col.all_objects if o.type=='MESH' and (o.name in ['RIG_MarineRiser','SUBSEA_Foundation'] or o.name.startswith(('SUBSEA_BOPStack','SUBSEA_RiserCoupling')))]
names=[o.name for o in targets]
with bpy.data.libraries.load(str(original),link=False) as (a,b):b.objects=list(names)
for target,source in zip(targets,b.objects):
 assert source is not None
 target.data=source.data.copy()
 # Restore the original closed mesh and its original modifier stack.
 for m in list(target.modifiers):target.modifiers.remove(m)
 for m in source.modifiers:
  new=target.modifiers.new(m.name,m.type)
  for prop in m.bl_rna.properties:
   if prop.identifier in ['rna_type','name','type'] or prop.is_readonly:continue
   try:setattr(new,prop.identifier,getattr(m,prop.identifier))
   except (TypeError,AttributeError,ValueError):pass
 target['entry_trial']='Closed pre-wedge v004 mesh restored; continuous axial viewing passage, no side sector removal.'
 bpy.data.objects.remove(source,do_unlink=True)
# A round central passage is the only access cut in the restored equipment.
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=.66,depth=145,location=(0,0,-55));cutter=bpy.context.object
for ob in targets:
 if ob.name=='RIG_MarineRiser':continue
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob
 m=ob.modifiers.new('Round continuous viewing passage','BOOLEAN');m.operation='DIFFERENCE';m.solver='EXACT';m.object=cutter
 while ob.modifiers.find(m.name)>0:bpy.ops.object.modifier_move_up(modifier=m.name)
 bpy.ops.object.modifier_apply(modifier=m.name)
bpy.data.objects.remove(cutter,do_unlink=True)
# Replace the lower riser side-wall crossing with an actual open flared mouth.
# Top pipe ends at-100; open sleeve at that level accommodates off-axis approach.
def tube(ob,rings):
 n=96;vs=[];fs=[];inv=ob.matrix_world.inverted()
 for z,inner,outer in rings:
  for r in [inner,outer]:
   for j in range(n):
    a=math.tau*j/n;vs.append(tuple(inv@Vector((r*math.cos(a),r*math.sin(a),z))))
 def ix(k,b,j):return k*2*n+b*n+j%n
 for k in range(len(rings)-1):
  for j in range(n):
   fs.append((ix(k,0,j),ix(k+1,0,j),ix(k+1,0,j+1),ix(k,0,j+1)))
   fs.append((ix(k,1,j+1),ix(k+1,1,j+1),ix(k+1,1,j),ix(k,1,j)))
 for k in [0,len(rings)-1]:
  for j in range(n):fs.append((ix(k,0,j),ix(k,0,j+1),ix(k,1,j+1),ix(k,1,j)))
 me=bpy.data.meshes.new(ob.name+' closed entry mesh');me.from_pydata(vs,[],fs);me.update()
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();me.update()
 for mat in ob.data.materials:me.materials.append(mat)
 for p in me.polygons:p.use_smooth=True
 ob.data=me
riser=bpy.data.objects['RIG_MarineRiser'];tube(riser,[(10,.45,.55),(-100,.45,.55)])
sleeve=bpy.data.objects.new('SUBSEA_EntrySleeve_PRESENTATION',bpy.data.meshes.new('Entry sleeve carrier'));col.objects.link(sleeve)
for mat in riser.data.materials:sleeve.data.materials.append(mat)
# Smooth cubic blend in radius avoids a shoulder in the narrowing interior.
rings=[]
for j in range(25):
 t=j/24;u=t*t*(3-2*t);rings.append((-100-8*t,1.1*(1-u)+.63*u,1.2*(1-u)+.65*u))
# The liner fits inside the0.66m equipment passage; its inner skin must not
# coincide with the equipment Boolean wall, which otherwise causes depth fighting.
rings.extend([(-118,.63,.65),(-120,.63,.65)]);tube(sleeve,rings)
sleeve['meaning']='Authored flared viewing sleeve for continuous camera entry. Not sourced/certified physical equipment. No time-dependent visibility or side wedge.'
# Route the small exterior auxiliary lines around the authored sleeve, not through its interior.
rerouted=[]
def line_radius(z):
 if z>=-94:return .72
 if z>=-100:
  t=(-94-z)/6;u=t*t*(3-2*t);return .72*(1-u)+1.35*u
 t=min(1.,max(0.,(-100-z)/8));u=t*t*(3-2*t);return 1.2*(1-u)+.65*u+.15
for ob in list(col.all_objects):
 if not ob.name.startswith('SUBSEA_AuxiliaryLine') or ob.type!='MESH':continue
 points=[ob.matrix_world@v.co for v in ob.data.vertices];lo=min(v.z for v in points);hi=max(v.z for v in points)
 if lo>=-94:continue
 center=sum(points,Vector())/len(points);direction=Vector((center.x,center.y,0)).normalized();inv=ob.matrix_world.inverted();vs=[];fs=[];n=24;nz=max(2,math.ceil(hi-lo))
 for k in range(nz+1):
  z=lo+(hi-lo)*k/nz;c=direction*line_radius(z)
  for j in range(n):
   a=math.tau*j/n;vs.append(tuple(inv@Vector((c.x+.06*math.cos(a),c.y+.06*math.sin(a),z))))
 for k in range(nz):
  for j in range(n):fs.append((k*n+j,k*n+(j+1)%n,(k+1)*n+(j+1)%n,(k+1)*n+j))
 fs.extend([tuple(reversed(range(n))),tuple(nz*n+j for j in range(n))]);me=bpy.data.meshes.new(ob.name+' outside entry sleeve');me.from_pydata(vs,[],fs);me.update()
 for mat in ob.data.materials:me.materials.append(mat)
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 for p in me.polygons:p.use_smooth=True
 ob.data=me;rerouted.append(ob.name)
col['entry_revision']='v008 trial: closed restored equipment, round central passage, authored flared entry sleeve. Camera remains external then crosses an open mouth, not a pipe side wall.'
txt=bpy.data.texts.new('README Surface v008 entry trial');txt.write('Closed entry trial for ECCO057. Restores v004 pre-wedge equipment meshes; applies only circular0.66m passage in BOP/foundation/couplings. Upper riser hollow0.45/0.55m and ends at-100. Authored entry sleeve opens at-100, inner radius1.1 ->0.63m by-108, continuing to-120; outer terminal radius0.65 fits within equipment opening. Editorial viewing accommodation, not certified equipment design. No animated visibility or clipping. Source files unchanged; only S01-S02 v004 consumes this trial.\n')
bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(dst),compress=True)
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
d={'native':str(dst),'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'sources':hashes,'restored_objects':names,'rerouted_auxiliary_lines':rerouted,'passage_radius_m':.66,'upper_riser_bounds_z':[10,-100],'sleeve_z':[-100,-120],'sleeve_inner_radius_m':[1.1,.63],'sleeve_terminal_outer_radius_m':.65,'camera_actions':0,'side_wedge':False,'consumer':'S01-S02 production v004 only','status':'Illustrative camera-entry trial, owner visual review pending; no engineering approval.'}
(B/'Surface_interface_v008.json').write_text(json.dumps(d,indent=2));(Q/'Notes/surface_v008_build.json').write_text(json.dumps(d,indent=2));print('SURFACE_V008_READY')
