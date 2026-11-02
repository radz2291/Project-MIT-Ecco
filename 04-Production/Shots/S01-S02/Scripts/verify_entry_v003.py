import bpy,math,json,os,hashlib
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02';s=bpy.context.scene
d={'missing_libraries':[l.filepath for l in bpy.data.libraries if not os.path.exists(bpy.path.abspath(l.filepath))]}
native=json.loads((Q/'Notes/entry_previs_native.json').read_text());errors=[]
for row in native['samples']:
 s.frame_set(row['frame']);errors.append(max(abs(s.camera.matrix_world[i][j]-row['camera_matrix'][i][j]) for i in range(4) for j in range(4)))
d['source_camera_sample_max_error']=max(errors)
def tree(objects):
 vs=[];fs=[];dg=bpy.context.evaluated_depsgraph_get()
 for ob in objects:
  ev=ob.evaluated_get(dg);me=ev.to_mesh();base=len(vs);vs.extend(ob.matrix_world@v.co for v in me.vertices);fs.extend(tuple(base+i for i in p.vertices) for p in me.polygons);ev.to_mesh_clear()
 return BVHTree.FromPolygons(vs,fs,all_triangles=False)
world=[o for o in s.objects if o.name.startswith('SHOT WORLD |')]
band=[o for o in world if ('REGIONAL_UNIT_01' in o.name or 'FRONT_UNIT_01' in o.name)]
s.frame_set(106);t=tree(band);origin=s.camera.matrix_world.translation.copy();hits=[]
for a in range(0,360,5):
 p,n,index,dist=t.ray_cast(origin,Vector((math.cos(math.radians(a)),math.sin(math.radians(a)),0)),3)
 hits.append(dist if p is not None else None)
d['enclosed106']={'rays':len(hits),'missing':sum(x is None for x in hits),'min_camera_to_wall_m':min(x for x in hits if x is not None),'camera_clip_start_m':s.camera.data.clip_start}
s.frame_set(80);t=tree(band);hits=[]
for radius in [2,10,50,100]:
 for a in range(0,360,10):
  origin=Vector((radius*math.cos(math.radians(a)),radius*math.sin(math.radians(a)),-119.5));p,n,index,dist=t.ray_cast(origin,Vector((0,0,-1)),2);hits.append(dist if p is not None else None)
d['intact_seabed80']={'rays':len(hits),'missing':sum(x is None for x in hits),'expected_hit_distance_m':.5,'max_distance_error_m':max(abs(v-.5) for v in hits if v is not None)}
ctrl=bpy.data.objects['ENTRY presentation controls'];d['control_samples']=[]
for f in [94,106,114,115,120,123,132,141,169,300,528]:
 s.frame_set(f);frontfaces=0
 for ob in world:
  if 'FRONT_UNIT_01' in ob.name:
   ev=ob.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();frontfaces+=len(me.polygons);ev.to_mesh_clear()
 d['control_samples'].append({'frame':f,'bore_scale':ctrl['Bore scale'],'front_reveal':ctrl['Front reveal'],'unit01_front_faces':frontfaces})
s.frame_set(169);ob=next(o for o in world if 'WORLD_S02_PHYSICAL_CUTAWAY_MESH' in o.name)
# The source already has Outer_soil_margin_25m at1. Compare evaluated source,
# not raw Basis coordinates (20m), to avoid a false5m outer-margin failure.
ref=bpy.data.objects.new('TEMP verify nominal source',ob.data);s.collection.objects.link(ref);ref.hide_render=True;bpy.context.view_layer.update();dg=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(dg);me=ev.to_mesh();rev=ref.evaluated_get(dg);rme=rev.to_mesh()
d['nominal_measurement_wall169']={'same_vertices':len(me.vertices)==len(rme.vertices),'max_local_position_error_m':max((a.co-b.co).length for a,b in zip(me.vertices,rme.vertices)),'reference':'Evaluated original linked source mesh with its existing Outer_soil_margin_25m shape key; no presentation modifier.'};ev.to_mesh_clear();rev.to_mesh_clear();bpy.data.objects.remove(ref,do_unlink=True)
d['source_files_unchanged']={}
for label,record,path,key in [('World v013','world_v014_build.json',R/'04-Production/Shared/Assets/Environment/Borehole/World_environment_v013.blend','source_sha256'),('Surface v006','surface_v007_build.json',R/'04-Production/Shared/Assets/Environment/Surface/Surface_descent_v006.blend','predecessor_sha256')]:
 expected=json.loads((Q/'Notes'/record).read_text())[key];d['source_files_unchanged'][label]=hashlib.sha256(path.read_bytes()).hexdigest()==expected
d['pass']=not d['missing_libraries'] and d['source_camera_sample_max_error']<1e-6 and not d['enclosed106']['missing'] and not d['intact_seabed80']['missing'] and d['nominal_measurement_wall169']['max_local_position_error_m']<1e-7 and all(d['source_files_unchanged'].values())
(Q/'Notes/entry_v003_verification.json').write_text(json.dumps(d,indent=2));result=d
