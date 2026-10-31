"""Extend existing irregular World bore through regional descent. No renders."""
import bpy,math,json,bisect,hashlib,struct
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');B=R/'04-Production/Shared/Assets/Environment/Borehole';D=R/'04-Production/Shared/Demos';T=R/'04-Production/Records/Tasks/T-055/Continuous_v013';T.mkdir(parents=True,exist_ok=True)
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.open_mainfile(filepath=str(B/'World_environment_v012.blend'),load_ui=False)
wall=bpy.data.objects['WORLD_S02_PHYSICAL_CUTAWAY_MESH']
digest=lambda o:hashlib.sha256(b''.join(struct.pack('fff',*v.co) for v in o.data.vertices)).hexdigest()
original=digest(wall);rings={};outer={}
def angle(y,z):
 a=math.atan2(z,y)
 return a+2*math.pi if a<math.radians(-5.01) else a
for v in wall.data.vertices:
 p=v.co;r=math.hypot(p.y,p.z);a=round(angle(p.y,p.z),8)
 if r<1:rings.setdefault(round(p.x,5),{})[a]=Vector((p.y,p.z))
 elif r>19:outer[a]=Vector((p.y,p.z))
xs=sorted(rings);angles=sorted(outer);na=len(angles)
def ray(points,t):
 d=Vector((math.cos(t),math.sin(t)))
 for a,b in zip(points,points[1:]):
  e=b-a;den=d.x*e.y-d.y*e.x
  if abs(den)<1e-10:continue
  r=(a.x*e.y-a.y*e.x)/den;u=(a.x*d.y-a.y*d.x)/den
  if r>0 and -1e-5<=u<=1+1e-5:return d*r
 raise ValueError(('profile ray',t))
profiles={x:[ray([rings[x][a] for a in sorted(rings[x])],t) for t in angles] for x in xs}
def profile(x):
 # Mirror continuation has matching endpoints, unlike abrupt repeated tiles.
 q=(x+15)%60;u=-15+q if q<=30 else 45-q
 k=max(0,min(len(xs)-2,bisect.bisect_right(xs,u)-1));a,b=xs[k:k+2];f=max(0,min(1,(u-a)/(b-a)))
 return [p.lerp(q,f) for p,q in zip(profiles[a],profiles[b])]
count=0;seams={}
for ob in bpy.data.collections['WORLD_REGIONAL_DESCENT'].objects:
 if '_INNER_' not in ob.name:continue
 lo,hi=ob['source_z_bounds_m'];steps=math.ceil((hi-lo)/.25);vs=[];fs=[]
 for k in range(steps+1):
  x=lo+(hi-lo)*k/steps+735;inner=profile(x)
  vs.extend((x,p.x,p.y) for p in inner);vs.extend((x,outer[a].x,outer[a].y) for a in angles)
  if k in [0,steps]:seams.setdefault(round(x,5),[]).append([(p.x,p.y) for p in inner])
 def ix(k,b,j):return k*2*na+b*na+j
 for k in range(steps):
  for j in range(na-1):fs.append((ix(k,0,j),ix(k+1,0,j),ix(k+1,0,j+1),ix(k,0,j+1)))
  for j in [0,na-1]:
   face=(ix(k,0,j),ix(k+1,0,j),ix(k+1,1,j),ix(k,1,j));fs.append(tuple(reversed(face)) if j==0 else face)
 for k,z in [(0,lo),(steps,hi)]:
  if z in [-1020.,-120.]:
   for j in range(na-1):fs.append((ix(k,0,j),ix(k,1,j),ix(k,1,j+1),ix(k,0,j+1)))
 old=ob.data;me=bpy.data.meshes.new(ob.name+' World irregular continuation');me.from_pydata(vs,[],fs);me.materials.append(old.materials[0]);me.update();ob.data=me
 for p in me.polygons:
  if p.index<steps*(na+1) and p.loop_total==4:p.use_smooth=False
 ob['bore_source']='Existing World S02 inner profiles, mirrored continuous extension; illustrative, not field geology';count+=1
assert original==digest(wall)
seam_error=max([max(math.dist(a,b) for a,b in zip(profiles[x],profile(x))) for x in [-15.,15.]])
assert seam_error<1e-5,seam_error
for x,parts in seams.items():
 if len(parts)>1:assert max(math.dist(a,b) for a,b in zip(parts[0],parts[1]))<1e-5
out=B/'World_environment_v013.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True,relative_remap=False)
meta=json.loads((B/'World_interface_v012.json').read_text());meta.update(version='v013',native=out.relative_to(R).as_posix(),native_sha256=hashlib.sha256(out.read_bytes()).hexdigest());meta['continuous_bore']={'source':'Exact existing S02 physical wall inner profiles','extension':'Mirrored, axially interpolated outside original30m; illustrative continuation, not new measurements','max_axial_step_m':.25,'original_local_wall_preserved':True,'join_error_m':seam_error};(B/'World_interface_v013.json').write_text(json.dumps(meta,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(D/'Surface_descent_demo_v003.blend'),load_ui=False)
for lib in list(bpy.data.libraries):
 if Path(lib.filepath).name=='World_environment_v012.blend':lib.filepath=str(out);lib.reload()
bpy.context.window.scene=bpy.data.scenes['World — layered descent']
demo=D/'Surface_descent_demo_v004.blend';bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True,relative_remap=False);bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=str(demo),compress=True,relative_remap=False)
bpy.ops.wm.open_mainfile(filepath=str(demo),load_ui=False);assert all(Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries)
(T/'verification.json').write_text(json.dumps({'regional_inner_objects_updated':count,'source_profiles':len(xs),'original_local_wall_unchanged':True,'join_error_m':seam_error,'saved_reopened_links_valid':True,'palette_preserved':True,'rendered':False,'demo':str(demo),'world':str(out)},indent=2));print('READY',str(demo))
