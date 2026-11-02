"""Dependency-audited cleanup successor; original v026 preserved."""
import bpy,collections,json,hashlib,sys,time,array,os
from pathlib import Path
Q=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/Shots/S01-S02');source=Q/'Scenes/S01-S02_production_v026.blend';out=Q/'Scenes/S01-S02_production_v027_clean.blend'
assert Path(bpy.data.filepath)==source and not out.exists()
source_hash=hashlib.sha256(source.read_bytes()).hexdigest();original_frame=bpy.context.scene.frame_current
P=Q/'Previews/Cleanup-v027';P.mkdir(exist_ok=True);sys.path.insert(0,str(Q/'Scripts'));import final_render_visibility as display
frames=sorted(set([1,94,95,120,474,520,620,756]+[s+d for s in [300,360,420,480,540,600] for d in [0,22,40,54]]))
def mesh_hash(o,dg):
 ev=o.evaluated_get(dg);m=ev.to_mesh()
 if m is None:return None
 a=array.array('f',[0.])* (3*len(m.vertices));m.vertices.foreach_get('co',a)
 r={'vertices':len(m.vertices),'faces':len(m.polygons),'coordinates':hashlib.sha256(a.tobytes()).hexdigest()};ev.to_mesh_clear();return r
def snapshot():
 rows=[];s=bpy.context.scene
 for f in frames:
  s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();c=s.camera;b=bpy.data.objects['BHA sequence assembly']
  rows.append({'frame':f,'camera':[round(x,7) for row in c.matrix_world for x in row],'lens':round(c.data.lens,7),'bha':[round(x,7) for row in b.matrix_world for x in row],'wall':mesh_hash(bpy.data.objects['ONE WALL - old history and current cells share topology'],dg),'signals':[mesh_hash(bpy.data.objects[f'WF sequence event {i}'],dg) for i in range(1,7)]})
 return rows
before=snapshot();counts_before={k:len(getattr(bpy.data,k)) for k in ['objects','collections','meshes','curves','materials','node_groups','actions','libraries']};scene_before=len(bpy.context.scene.objects)
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
 for f in [1,95,386,620,756]:bpy.context.scene.frame_set(f);display.export(P/f'before_{f:04}.png',960,540)
arch={c for c in bpy.data.collections if not c.library and c.hide_render and c.hide_viewport};candidate={o for c in arch for o in c.all_objects}
names={'World pixel guide controls','ENTRY presentation controls','BHA sequence assembly','Shared fine measurement display','ONE WALL - old history and current cells share topology'}
for o in bpy.context.scene.objects:
 if (not o.library and o.hide_get() and o.name not in names and not o.name.startswith(('WF sequence event','Contact patch event','World pixel_','WORLD_PIXEL_'))) or o.name=='WF_MASTER_CONTROLS':candidate.add(o)
roots=set(bpy.context.scene.objects)-candidate;roots|={bpy.context.scene.camera,bpy.context.scene.world};roots.discard(None)
for name in names:
 if name in bpy.data.objects:roots.add(bpy.data.objects[name])
children=collections.defaultdict(set)
for dependency,users in bpy.data.user_map().items():
 for user in users:children[user].add(dependency)
seen=set();todo=list(roots)
while todo:
 x=todo.pop()
 if x in seen:continue
 seen.add(x)
 # Do not treat a referenced Scene as a request to retain every archive collection.
 if not isinstance(x,bpy.types.Scene):todo.extend(children.get(x,()))
keep=candidate&seen;remove=candidate-seen
deleted=[{'name':o.name,'library':o.library.filepath if o.library else None} for o in remove]
protected=[{'name':o.name,'library':o.library.filepath if o.library else None} for o in keep]
for o in remove:bpy.data.objects.remove(o,do_unlink=True)
empty=[]
for col in list(bpy.data.collections):
 if not col.library and not col.all_objects:empty.append(col.name);bpy.data.collections.remove(col)
cleared=[]
for kind in ['actions','node_groups','meshes','curves','materials','cameras','lights','images']:
 for item in getattr(bpy.data,kind):
  if not item.library and item not in seen and item.use_fake_user:item.use_fake_user=False;cleared.append({'kind':kind,'name':item.name})
purged=bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
bpy.context.scene.frame_set(original_frame);bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
bpy.ops.wm.open_mainfile(filepath=str(out),use_scripts=False)
after=snapshot();assert before==after,'Cleanup changed a sampled camera/BHA/wall/signal result'
images=[]
with bpy.context.temp_override(window=bpy.context.window_manager.windows[0]):
 for f in [1,95,386,620,756]:
  bpy.context.scene.frame_set(f);t=time.perf_counter();display.export(P/f'after_{f:04}.png',960,540);dt=time.perf_counter()-t;assert dt<5
  a=bpy.data.images.load(str(P/f'before_{f:04}.png'),check_existing=False);b=bpy.data.images.load(str(P/f'after_{f:04}.png'),check_existing=False)
  import numpy as np
  x=np.array(a.pixels[:],dtype=np.float32);y=np.array(b.pixels[:],dtype=np.float32);diff=np.abs(x-y);images.append({'frame':f,'seconds':dt,'identical_pixels':bool(np.array_equal(x,y)),'mean_abs_linear_error':float(diff.mean()),'max_abs_linear_error':float(diff.max())});bpy.data.images.remove(a);bpy.data.images.remove(b)
assert all(r['mean_abs_linear_error']<.0001 for r in images),images
missing=[l.filepath for l in bpy.data.libraries if not os.path.isfile(bpy.path.abspath(l.filepath))];assert not missing
bpy.context.scene.frame_set(original_frame)
assert source_hash==hashlib.sha256(source.read_bytes()).hexdigest()
r={'source':str(source),'source_sha256':source_hash,'clean_scene':str(out),'clean_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'source_bytes':source.stat().st_size,'clean_bytes':out.stat().st_size,'scene_objects_before':scene_before,'scene_objects_after':len(bpy.context.scene.objects),'counts_before':counts_before,'counts_after':{k:len(getattr(bpy.data,k)) for k in counts_before},'removed_objects':deleted,'protected_dependencies':protected,'removed_empty_collections':empty,'unused_local_fake_users_cleared':cleared,'orphan_datablocks_purged':purged,'verified_sample_frames':frames,'camera_bha_wall_six_signals_identical':before==after,'matched_visual_checks':images,'saved_reopen':True,'missing_libraries':missing,'dof_enabled':bpy.context.scene.camera.data.dof.use_dof,'source_full_video':'Previews/Full-v026/S01-S02_full_v026.mp4','render_policy':'Existing v026 full render retained; visual equivalence checked at five frames, not newly full-rendered.'}
(Q/'Notes/cleanup_v027.json').write_text(json.dumps(r,indent=2));result={k:r[k] for k in ['clean_scene','source_bytes','clean_bytes','scene_objects_before','scene_objects_after','counts_before','counts_after','protected_dependencies','matched_visual_checks']}
