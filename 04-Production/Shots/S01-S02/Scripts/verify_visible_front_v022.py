import bpy,json,math
from pathlib import Path
from mathutils import Vector
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');Q=R/'04-Production/Shots/S01-S02'
bpy.ops.wm.open_mainfile(filepath=str(Q/'Scenes/S01-S02_production_v022.blend'),use_scripts=False)
s=bpy.context.scene;w=bpy.data.objects['ONE WALL - old history and current cells share topology'];blue=bpy.data.materials['Recorded shell — common settled blue'];events=json.loads((Q/'Notes/approved_v016_integration.json').read_text())['events'];matches=[]
for e in events:
 s.frame_set(e['start']+53)
 for idx in {w.data.polygons[i].material_index for i in e['faces']}:
  mat=w.data.materials[idx];assert max(abs(a-b) for a,b in zip(mat.diffuse_color,blue.diffuse_color))<1e-6
 matches.append(e['event'])
samples=[]
for f in [474,528,600,660,720,756]:
 s.frame_set(f);eo=w.evaluated_get(bpy.context.evaluated_depsgraph_get());me=eo.to_mesh();zs=[v.co.z for v in me.vertices];samples.append({'frame':f,'revealed_faces':len(me.polygons),'front_z':max(zs)});eo.to_mesh_clear()
assert all(a['front_z']<=b['front_z']+.001 for a,b in zip(samples,samples[1:])),samples
cam=s.camera;dg=bpy.context.evaluated_depsgraph_get();proj=cam.calc_matrix_camera(dg,x=1920,y=1080)@cam.matrix_world.inverted();front=samples[-1]['front_z'];ring=[]
for a in range(32):
 v=proj@Vector((.18*math.cos(a*math.tau/32),.18*math.sin(a*math.tau/32),front,1));x=.5+.5*v.x/v.w;y=.5+.5*v.y/v.w;ring.append((x,y))
assert all(not(0<=x<=1 and 0<=y<=1) for x,y in ring),ring
assert all(Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries)
(Q/'Notes/visible_front_v022_verification.json').write_text(json.dumps({'saved_native_reopens':True,'settled_color_match_events':matches,'common_rgba':list(blue.diffuse_color),'upward_front_progress':samples,'revealed_front_outside_final_crop':True,'revealed_front_projected_bounds':{'x':[min(x for x,y in ring),max(x for x,y in ring)],'y':[min(y for x,y in ring),max(y for x,y in ring)]},'relative_links_resolve':True,'current_patch_faces':sum(len(e['faces']) for e in events),'scene_seconds':s.frame_end/24},indent=2));print('VISIBLE_FRONT_V022_VERIFIED')

