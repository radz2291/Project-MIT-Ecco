import bpy,pathlib,sys,json,hashlib,math
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-053';(T/'Scenes').mkdir(exist_ok=True)
sys.path.insert(0,str(A/'WellAssembly/Scripts'))
from world_interface_v010 import link_variant,s02_placement
sources={x['id']:ROOT/x['native'] for x in json.loads((ROOT/'04-Production/Records/Tasks/T-050/sources.json').read_text())}
def invariant(s):
 data=[]
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);data.append([f,[list(r) for r in s.camera.matrix_world],s.camera.data.lens])
 return hashlib.sha256(json.dumps(data).encode()).hexdigest()
reports=[]
for name,src in [('S02',sources['S02']),('T44_layers',ROOT/'04-Production/Records/Tasks/T-044/Revision_v006/Scenes/layers_cleanup_v010.blend')]:
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);s=bpy.context.scene;before=invariant(s)
 if name=='S02':
  original=bpy.data.objects['S02 geological wall retained section'];ad=original.animation_data
  o=link_variant(A,'WORLD_S02_PHYSICAL_CUTAWAY',s02_placement(A),'T53 shared S02 physical cutaway')
  # Only source shell appearance is replaced; timing copied to local instance.
  if ad and ad.action:
   o.animation_data_create();o.animation_data.action=ad.action
   try:o.animation_data.action_slot=ad.action_slot
   except:pass
  bpy.data.objects.remove(original,do_unlink=True)
 else:
  found=False
  for l in bpy.data.libraries:
   if pathlib.Path(l.filepath).name=='World_environment_v009.blend':l.filepath=str(A/'WellAssembly/World_environment_v010.blend');l.reload();found=True
  assert found,'Expected World library absent'
 after=invariant(s);assert before==after
 s.frame_set(528 if name=='S02' else s.frame_current)
 for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
 dest=T/'Scenes'/f'{name}_World_v010.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(l.filepath)
 bpy.ops.wm.save_as_mainfile(filepath=str(dest),compress=True)
 bpy.ops.wm.open_mainfile(filepath=str(dest),load_ui=False);s=bpy.context.scene
 assert invariant(bpy.context.scene)==before
 reports.append(dict(consumer=str(dest.relative_to(ROOT)),baseline=str(src.relative_to(ROOT)),camera_all_frames_sha256=before,reopened=True,frame_range=[s.frame_start,s.frame_end],missing_libraries=[l.filepath for l in bpy.data.libraries if not pathlib.Path(bpy.path.abspath(l.filepath)).exists()]))
(T/'Evidence/consumers.json').write_text(json.dumps(reports,indent=2));print('CONSUMERS VERIFIED')
