"""Keep the advancing recorded-surface front visible during camera withdrawal."""
import bpy,json,math,bisect,datetime,hashlib
from pathlib import Path
from mathutils import Vector
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02')
assert bpy.data.filepath.endswith('S01-S02_production_v021.blend')
out=Q/'Scenes/S01-S02_production_v022.blend';assert not out.exists()
if bpy.data.is_dirty:bpy.ops.wm.save_as_mainfile(filepath=str(Q/'Scenes'/('Before_visible_front_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+'.blend')),copy=True,compress=True)
s=bpy.context.scene;w=bpy.data.objects['ONE WALL - old history and current cells share topology'];me=w.data
history=[p for p in me.polygons if me.materials[p.material_index].name=='Recorded shell — common settled blue'];base=min(p.center.z for p in history)-.0075
start,end=532,700;front=[];targets=[]
for f in range(474,721):
 s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();cam=s.camera.evaluated_get(dg);m=cam.calc_matrix_camera(dg,x=1920,y=1080)@cam.matrix_world.inverted()
 def screen(z):
  c=m@Vector((0,0,z,1));return Vector((.5+.5*c.x/c.w,.5+.5*c.y/c.w))
 b=screen(base);direction=screen(base+.1)-b
 # Intersection of the projected tube axis with the upper/right frame edge.
 distance=min((1-b[i])/direction[i] for i in range(2) if direction[i]>1e-8)
 edge=b+direction*distance;p=max(0.,min(1.,(f-start)/(end-start)));progress=1.12*p*p*(3-2*p);target=b+(edge-b)*progress
 k=0 if abs(direction.x)>abs(direction.y) else 1;u=2*target[k]-1
 z=(m[k][3]-u*m[3][3])/(u*m[3][2]-m[k][2]) if progress>0 else base
 z=max(base,z,front[-1] if front else base);front.append(z)
 targets.append({'frame':f,'progress':progress,'z':z,'screen_front':list(screen(z))})
assert front[-1]<max(v.co.z for v in me.vertices)-.15,(front[-1],max(v.co.z for v in me.vertices))
for face in history:
 z=face.center.z;i=bisect.bisect_left(front,z)
 if i>=len(front):birth=100000
 else:
  angle=math.atan2(face.center.y,face.center.x);col=round(angle/(math.tau/32));row=math.floor((z-base+.0001)/.06);jitter=(col*13+row*7)%3
  birth=max(start,474+i-1+jitter)
 me.attributes['ecco_receipt_frame'].data[face.index].value=-2000;me.attributes['ecco_reveal_order'].data[face.index].value=birth-1
w['Upward reveal']='Visible front from scan row after fourth exchange532, traverses picture, exits around700; continues beyond final crop720.'
s.frame_set(620);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
(Q/'Notes/visible_front_v022.json').write_text(json.dumps({'scene':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source':'S01-S02_production_v021.blend','visual_review_failure':'v021 reveal stayed mostly above the crop; camera uncovered already-blue geometry, not a visible advancing front.','reveal_start':start,'front_exit_target':end,'camera_pull':[474,720],'screen_front_samples':[t for t in targets if t['frame'] in [474,532,550,580,600,620,640,660,680,700,720]],'history_faces_retimed':len(history),'preserved':['camera','sixbeam/pulse/contact/localtileanimations','settledbluecolor','extendedclosedwideshell','finaldisplaycleanupandedgefix','sharedmasters'],'native_settle_frames':4,'cell_start_stagger_frames':[0,2],'review_required':'Entire decoded new motion sequence, not just endpoint coverage.'},indent=2))
result={'saved':str(out),'start':start,'exit':end,'samples':[t for t in targets if t['frame'] in [550,600,640,680,720]]}
