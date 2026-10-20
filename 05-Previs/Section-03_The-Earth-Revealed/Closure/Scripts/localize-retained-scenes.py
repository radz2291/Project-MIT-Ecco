import bpy,json,hashlib,time
from pathlib import Path
R=Path(__file__).resolve().parents[2]
report=[]
def mesh_hash():
 h=hashlib.sha256()
 for m in sorted(bpy.data.meshes,key=lambda m:m.name):
  import array
  a=array.array('f',[0])*(len(m.vertices)*3);m.vertices.foreach_get('co',a);h.update(m.name.encode());h.update(a.tobytes())
 return h.hexdigest()
for version in ['v009','v014','v023','v028','v033','v036']:
 for p in sorted((R/version).rglob('*.blend')):
  bpy.ops.wm.open_mainfile(filepath=str(p));before=mesh_hash();original_hash=hashlib.sha256(p.read_bytes()).hexdigest();images=[]
  data=R/version/'Data';data.mkdir(exist_ok=True)
  for i in bpy.data.images:
   if i.source!='FILE':continue
   if i.packed_file:payload=bytes(i.packed_file.data)
   else:payload=Path(bpy.path.abspath(i.filepath)).read_bytes()
   digest=hashlib.sha256(payload).hexdigest();suffix='.png' if payload.startswith(b'\x89PNG') else '.bin'
   dst=data/('packed-source_'+digest[:16]+suffix)
   if not dst.exists():dst.write_bytes(payload)
   assert dst.read_bytes()==payload
   i.filepath=bpy.path.relpath(str(dst),start=str(p.parent))
   if not i.packed_file:i.pack()
   images.append({'name':i.name,'path':i.filepath,'sha256':digest,'packed':True})
  bpy.context.preferences.filepaths.save_version=0
  bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
  bpy.ops.wm.open_mainfile(filepath=str(p))
  assert before==mesh_hash(),'Geometry changed'
  assert len(bpy.data.libraries)==0,'Unexpected external library'
  for i in bpy.data.images:
   if i.source=='FILE':assert i.packed_file and Path(bpy.path.abspath(i.filepath)).is_file()
  report.append({'version':version,'scene':str(p.relative_to(R)),'original_scene_sha256':original_hash,'localized_scene_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'geometry_unchanged':True,'reopened':True,'images':images})
  (R/'Closure/Localized-dependency-verification.json').write_text(json.dumps(report,indent=2))
  print('LOCALIZED',p.name,flush=True)
  if version=='v036':
   s=bpy.context.scene;s.frame_set(60);s.render.filepath=str(R/'Closure/Final-label-verification.png');t=time.perf_counter();bpy.ops.render.render(write_still=True)
   (R/'Closure/Final-proof-timing.json').write_text(json.dumps({'frame':60,'seconds':time.perf_counter()-t}))
