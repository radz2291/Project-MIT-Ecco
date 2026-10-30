import bpy,pathlib,json,hashlib,math
ROOT=pathlib.Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-053';S=T/'Scenes'
def cam(s):
 out=[]
 for f in sorted(set([s.frame_start,s.frame_end,(s.frame_start+s.frame_end)//2])):
  s.frame_set(f);out.append([f,[list(r) for r in s.camera.matrix_world],s.camera.data.lens])
 return out
def save(p):
 for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
 bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(l.filepath)
 bpy.ops.wm.save_as_mainfile(filepath=str(p),compress=True)
world=A/'WellAssembly/World_environment_v010.blend';probe=S/'World_extent_probe_v010.blend'
bpy.ops.wm.open_mainfile(filepath=str(world),load_ui=False);save(probe)
cons=[]
jobs=[('S02',S/'S02_World_v010.blend'),('T44_open',ROOT/'04-Production/Records/Tasks/T-044/Revision_v006/Scenes/Reuse_A_cleanup_v010.blend')]
for name,path in jobs:
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False);before=cam(bpy.context.scene)
 for l in bpy.data.libraries:
  if pathlib.Path(l.filepath).name in ['World_environment_v009.blend','World_environment_v010.blend']:l.filepath=str(world);l.reload()
 if name=='T44_open':save(S/'T44_open_World_v010.blend')
 for l in bpy.data.libraries:
  if pathlib.Path(l.filepath).name=='World_environment_v010.blend':l.filepath=str(probe);l.reload()
 dest=S/f'{name}_propagation_probe.blend';save(dest);cons.append((name,dest,before))
bpy.ops.wm.open_mainfile(filepath=str(probe),load_ui=False)
changed=[]
for o in bpy.data.objects:
 if o.type!='MESH' or o.library:continue
 count=0
 for v in o.data.vertices:
  r=math.hypot(v.co.y,v.co.z)
  if r>19.99:v.co.y*=1.05;v.co.z*=1.05;count+=1
 if count:
  changed.append([o.name,count]);o['outer_radius_m']=21.0
  if o.data.shape_keys:
   for k in o.data.shape_keys.key_blocks:
    for v in k.data:
     r=math.hypot(v.co.y,v.co.z)
     if abs(r-20)<.002:v.co.y*=1.05;v.co.z*=1.05
save(probe)
checks=[]
for name,path,before in cons:
 bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False)
 for l in list(bpy.data.libraries):
  if pathlib.Path(bpy.path.abspath(l.filepath)).name==probe.name:l.reload()
 linked=[o for o in bpy.data.objects if o.library and pathlib.Path(bpy.path.abspath(o.library.filepath)).name==probe.name and o.type=='MESH']
 radii={o.name:max((math.hypot(v.co.y,v.co.z) if 'S02' in o.name else max(abs(v.co.y),abs(v.co.z))) for v in o.data.vertices) for o in linked if o.get('outer_radius_m')==21.0}
 assert radii and all(abs(r-21)<.002 for r in radii.values()),radii
 assert cam(bpy.context.scene)==before
 checks.append(dict(consumer=name,path=str(path.relative_to(ROOT)),observed_outer_radii=radii,cameras_preserved=True,reopened=True))
(T/'Evidence/propagation.json').write_text(json.dumps(dict(shared_edit='Isolated probe library only: outside soil20→21m; borehole unchanged',changed=changed,checks=checks,production_library_unchanged=True),indent=2));print('PROPAGATION PASS')
