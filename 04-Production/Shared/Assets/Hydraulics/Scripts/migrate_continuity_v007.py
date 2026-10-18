"""T48 resume: direct T44v006 -> v007, with nested immutable base preserved."""
import bpy,sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];ASSET=ROOT/'04-Production/Shared/Assets';TASK=ROOT/'04-Production/Records/Tasks/T-048';S=TASK/'Scenes';E=TASK/'Evidence'
sys.path.insert(0,str(HERE));from build_hydraulics_v001 import snapshot
sys.path.insert(0,str(ASSET/'World/Scripts'));from continuation_controls_v001 import attach_continuation
EXPECTED='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf-8')
def resolve_library(lib):
 # Blender exposes loaded Library.filepath normalized relative to the main file,
 # including nested libraries. parent records lineage, not a new path base.
 return Path(bpy.path.abspath(lib.filepath)).resolve()
def libraries():
 return [dict(path=l.filepath,resolved=str(resolve_library(l)),sha256=sha(resolve_library(l)),parent=str(resolve_library(l.parent)) if l.parent else None) for l in bpy.data.libraries]
def rigid_poses():
 dep=bpy.context.evaluated_depsgraph_get();hs=[i.matrix_world.copy() for i in dep.object_instances if i.object.original.name=='ECCO_HOUSING_SOURCE_MESH'];assert len(hs)==1,len(hs)
 return dict(housing=[list(r) for r in hs[0]],flow=[list(r) for r in bpy.data.objects['FLOW_PLACEMENT'].evaluated_get(dep).matrix_world])
def save_relative(p):
 direct=[(l,resolve_library(l)) for l in bpy.data.libraries if l.parent is None]
 for lib,absolute in direct:lib.filepath=bpy.path.relpath(str(absolute),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
if __name__=='__main__':
 master=ASSET/'BHA/BHA_film_v007.blend';assert sha(master)==EXPECTED
 for kind in ['A','B']:
  src=S/('Flow_reuse_'+kind+'_v005.blend');out=S/('Flow_reuse_'+kind+'_v006.blend');assert not out.exists(),'Preserve existing candidate; choose successor version'
  initial=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);before=snapshot();oldpose=rigid_poses();oldlibs=libraries()
  direct=[l for l in bpy.data.libraries if l.parent is None and resolve_library(l).name=='BHA_film_v006.blend'];assert len(direct)==1
  direct[0].filepath=str(master);direct[0].reload()
  hardware=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];assert hardware.instance_collection.name=='WORLD_HARDWARE'
  ctrl,parts,endpoint=attach_continuation(ASSET,hardware)
  s.frame_set(1);bpy.context.view_layer.update();after=snapshot();old_compatible=dict(after);old_compatible['controls']=dict(after['controls']);del old_compatible['controls']['UPHOLE_CONTINUATION_CONTROL']
  assert before==old_compatible
  newpose=rigid_poses();assert oldpose==newpose,(oldpose,newpose)
  deps=libraries();assert any(Path(x['resolved']).name=='BHA_film_v006.blend' and x['parent'] and Path(x['parent']).name=='BHA_film_v007.blend' for x in deps)
  assert not any(Path(x['resolved']).name=='BHA_film_v006.blend' and x['parent'] is None for x in deps)
  assert all(p.parent==hardware for p in parts.values())
  save_relative(out);assert sha(src)==initial and sha(master)==EXPECTED
  dump(E/('continuity_'+kind+'_migration_v007.json'),dict(accepted_base_commit='a08d0ecfbd6f3241298f506b3ea42613388b3baf',source=rel(src),source_sha256=initial,output=rel(out),output_sha256=sha(out),before=before,after=after,preserved_old_controls_camera_timing_animation=before==old_compatible,old_pose=oldpose,new_pose=newpose,rigid_registration_preserved=oldpose==newpose,libraries_before=oldlibs,libraries_after=deps,continuation_parent=hardware.name,continuation_parts=list(parts),default_length_m=ctrl['length_m'],notes='Only direct BHAv006 relinked; new BHAv007 nests original frozen006. Existing hardware instance unchanged; continuation children attach to it.'))
 print('T48_CONTINUITY_MIGRATION_PASS')
