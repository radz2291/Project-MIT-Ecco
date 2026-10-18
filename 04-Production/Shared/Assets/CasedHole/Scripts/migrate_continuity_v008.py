"""T47 scoped T44 accepted-continuity migration; no render or Git operations."""
import bpy,sys,json,hashlib,struct
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-047';S=T/'Scenes';E=T/'Evidence'
sys.path.insert(0,str(A/'World/Scripts'));sys.path.insert(0,str(A/'Acoustics/Scripts'))
from continuation_controls_v001 import attach_continuation
from acoustic_event_v001 import native_instance
INPUTS={'Reuse_A':'CasedReuse_A_v002','Reuse_B':'CasedReuse_B_v002','Hardware':'CasedHardware_v003','Channel':'CasedChannel_v005','WearGraze':'CasedWearGraze_v005','WearSection':'CasedWearSection_v005','Retrieval':'CasedRetrieval_v004','Support':'CasedSupport_v006'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(ROOT).as_posix()
def dump(p,d):p.write_text(json.dumps(d,indent=2),encoding='utf8')
def channels(block):
 if not block.animation_data or not block.animation_data.action:return []
 return [(fc.data_path,fc.array_index,[(list(k.co),k.interpolation) for k in fc.keyframe_points]) for l in block.animation_data.action.layers for s in l.strips for b in s.channelbags for fc in b.fcurves]
def scalar(v):return isinstance(v,(int,float,str))
def snapshot():
 s=bpy.context.scene;c=s.camera
 return dict(camera=dict(location=list(c.location),rotation=list(c.rotation_euler),lens=c.data.lens,type=c.data.type,ortho_scale=c.data.ortho_scale,clip=[c.data.clip_start,c.data.clip_end],object_keys=channels(c),data_keys=channels(c.data)),timing=[s.frame_start,s.frame_end,s.render.fps,s.render.fps_base],local={o.name:dict(props={k:v for k,v in o.items() if scalar(v)},keys=channels(o)) for o in bpy.data.objects if not o.library and (o.animation_data or 'CONTROL' in o.name)})
def sensor_snapshot():
 s=bpy.context.scene;w=bpy.data.objects['WORLD_CONTROL'];old=w['show_hardware'];w['show_hardware']=1;w.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update();rows=[]
 for f in sorted({s.frame_start,(s.frame_start+s.frame_end)//2,s.frame_end}):
  s.frame_set(f);bpy.context.view_layer.update();rows.append(dict(frame=f,sensors=[dict(name=n,matrix=[list(r) for r in native_instance(n)[1]]) for n in ['ECCO_SENSOR_REF_01','ECCO_SENSOR_REF_02','ECCO_SENSOR_REF_03']]))
 w['show_hardware']=old;w.update_tag();s.frame_set(1);bpy.context.view_layer.update();return rows
def save(p):
 assert not p.exists(),p
 for l in bpy.data.libraries:l.filepath=bpy.path.relpath(bpy.path.abspath(l.filepath),start=str(p.parent))
 bpy.ops.wm.save_as_mainfile(filepath=str(p),relative_remap=False)
rows=[]
assert sha(A/'BHA/BHA_film_v007.blend')=='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1'
for name,source_name in INPUTS.items():
 src=S/(source_name+'.blend');old_sha=sha(src);bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);before=snapshot();sensors_before=sensor_snapshot()
 for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
 direct=[l for l in bpy.data.libraries if not l.parent and Path(l.filepath).name=='BHA_film_v006.blend'];assert len(direct)==1
 direct[0].filepath=str(A/'BHA/BHA_film_v007.blend');direct[0].reload()
 h=[o for o in bpy.data.objects if not o.library and o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.name=='WORLD_HARDWARE'];assert len(h)==1
 attach_continuation(A,h[0]);after=snapshot();after['local']={k:after['local'][k] for k in before['local']};assert before==after,(name,'camera/timing/old control or keys changed')
 sensors_after=sensor_snapshot();assert sensors_before==sensors_after,(name,'sensor pose changed')
 p=S/('Cased'+name+'_v008.blend');save(p);assert sha(src)==old_sha
 rows.append(dict(name=name,source=rel(src),source_sha256=old_sha,candidate=rel(p),sha256=sha(p),camera_timing_keys_old_controls_preserved=True,sensors_preserved=True,before=before,after=after,sensors=sensors_after,direct_bha_version='v007',nested_bha_version='v006',base_commit='a08d0ecfbd6f3241298f506b3ea42613388b3baf'))
dump(E/'continuity-migration_v008.json',rows)
fresh=[]
for row in rows:
 p=ROOT/row['candidate'];bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False);s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update();libs=[dict(path=l.filepath,resolved=str(Path(bpy.path.abspath(l.filepath)).resolve()),parent=l.parent.filepath if l.parent else None,sha256=sha(Path(bpy.path.abspath(l.filepath)).resolve())) for l in bpy.data.libraries];assert all(l['path'].startswith('//') and Path(l['resolved']).exists() for l in libs)
 assert len([l for l in libs if not l['parent'] and Path(l['resolved']).name=='BHA_film_v007.blend'])==1
 assert any(l['parent'] and Path(l['resolved']).name=='BHA_film_v006.blend' for l in libs)
 w=bpy.data.objects['WORLD_CONTROL'];default=w['show_hardware'];w['show_hardware']=1;w.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update();names=[i.object.original.name for i in bpy.context.evaluated_depsgraph_get().object_instances];assert names.count('ECCO_HOUSING_SOURCE_MESH')==1 and names.count('UPHOLE_UNIT_COLLAR_EXTENSION')==1
 hw=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];ext=bpy.data.objects['WORLD_UPHOLE_EXTENSION_INSTANCE'];joint=bpy.data.objects['WORLD_UPHOLE_JOINT_INSTANCE'];ctrl=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL'];coverage=[]
 for f in range(s.frame_start,s.frame_end+1):
  s.frame_set(f);bpy.context.view_layer.update();d=bpy.context.evaluated_depsgraph_get();h=hw.evaluated_get(d).matrix_world;x=ext.evaluated_get(d).matrix_world;near=x@Vector((0,0,0));far=x@Vector((-1,0,0));err=(near-(h@Vector((-1.5,0,0)))).length;assert err<1e-5
  assert abs(ext.evaluated_get(d).scale.y-1)<1e-6 and abs(ext.evaluated_get(d).scale.z-1)<1e-6
  c=world_to_camera_view(s,s.camera,far);coverage.append(dict(frame=f,join_error_m=err,far_in_frame=bool(0<=c.x<=1 and 0<=c.y<=1 and c.z>s.camera.data.clip_start)))
 # Both explicit hero visibility and inherited hardware visibility hide the parts.
 ctrl['show']=0;ctrl.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update();assert ext.hide_render and joint.hide_render
 ctrl['show']=1;ctrl.update_tag();w['show_hardware']=0;w.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update();assert ext.hide_render and joint.hide_render
 w['show_hardware']=default;w.update_tag();s.frame_set(1);bpy.context.view_layer.update()
 fresh.append(dict(scene=row['candidate'],sha256=sha(p),libraries=libs,one_ecco_and_extension_when_enabled=True,default_hardware_visibility=default,visibility_propagates=True,coverage=coverage,unit_scale=s.unit_settings.scale_length))
dump(E/'continuity-fresh-native_v008.json',dict(passed=True,records=fresh,limits='Executor native checks; combined effect/finite geometry and render evidence follow separately.'))
print('T47_CONTINUITY_MIGRATION_PASS',len(rows),flush=True)
