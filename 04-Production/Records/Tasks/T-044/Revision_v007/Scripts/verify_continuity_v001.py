"""Native checks only; no render, shared-master publication or Git mutation."""
import bpy,sys,runpy,json,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;sys.argv=['script','--','noop'];D=runpy.run_path(str(HERE/'build_continuity_v001.py'))
ROOT=D['ROOT'];ASSET=D['ASSET'];REV=D['REV'];E=D['E'];SCENES=D['SCENES'];checks=[]
def check(n,v,detail=None):checks.append(dict(name=n,passed=bool(v),detail=detail))
m=json.loads((ASSET/'World/manifest_v006.json').read_text())
for item in m['artifacts']:check('preserved accepted native '+item['path'],D['sha'](ROOT/item['path'])==item['sha256'])
records=[]
for name in ['Reuse_A_continuity','Reuse_B_continuity','connection_wide','furthest_uphole']:
 path=SCENES/(name+('_v003.blend' if name=='connection_wide' else '_v002.blend'));rec=D['inspect'](path);records.append(rec)
 check('fresh relative links and single product/extension '+name,rec['eccos']==1 and rec['extension_meshes']==1)
 s=bpy.context.scene;hw=D['hardware_instance']();ctrl=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL'];ext=bpy.data.objects['WORLD_UPHOLE_EXTENSION_INSTANCE'];joint=bpy.data.objects['WORLD_UPHOLE_JOINT_INSTANCE']
 check('source metre scale '+name,s.unit_settings.scale_length==1 and all(abs(x-1)<1e-6 for x in hw.scale))
 frames=list(range(s.frame_start,s.frame_end+1));poses=[]
 for f in frames:
  s.frame_set(f);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();h=hw.evaluated_get(deps).matrix_world;e=ext.evaluated_get(deps).matrix_world
  near=e@Vector((0,0,0));join_expected=h@Vector((-1.5,0,0));far=e@Vector((-1,0,0));edge=world_to_camera_view(s,s.camera,far)
  check('continuous join '+name+' f'+str(f),(near-join_expected).length<1e-5)
  check('far end outside camera '+name+' f'+str(f),not(0<=edge.x<=1 and 0<=edge.y<=1 and edge.z>s.camera.data.clip_start))
  poses.append(dict(frame=f,near=list(near),far=list(far),end_camera=list(edge)))
 check('transverse radius unchanged '+name,abs(ext.evaluated_get(deps).scale.y-1)<1e-6 and abs(ext.evaluated_get(deps).scale.z-1)<1e-6)
 # Length is a local instance parameter, never a duplicate or rescale of source ECCO.
 for length in [1.,12.,24.]:
  ctrl['length_m']=length;ctrl.update_tag();bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();e=ext.evaluated_get(deps).matrix_world
  measured=((e@Vector((-1,0,0)))-(e@Vector((0,0,0)))).length
  check('adjustable length '+name+' '+str(length),abs(measured-length)<1e-5,dict(measured_m=measured))
 ctrl['length_m']=12.;ctrl['show']=0;ctrl.update_tag();bpy.context.view_layer.update()
 check('hero hides continuation/joint '+name,ext.hide_render and joint.hide_render)
 ctrl['show']=1;ctrl.update_tag();bpy.context.view_layer.update();check('show restores continuation/joint '+name,not ext.hide_render and not joint.hide_render)
 if name=='connection_wide':
  s.frame_set(1);bpy.context.view_layer.update();p=world_to_camera_view(s,s.camera,hw.matrix_world@Vector((-1.5,0,0)))
  check('original source endpoint now connection visible in wider frame',0<p.x<1 and 0<p.y<1 and p.z>0,list(p))
 (E/(name+'_pose-coverage_v007.json')).write_text(json.dumps(poses,indent=2),encoding='utf-8')
for k in ['A','B']:
 data=json.loads((E/f'migration_{k}_v007.json').read_text());check('original camera/timing/controls preserved '+k,data['existing_camera_timing_controls_preserved'])
sys.path.insert(0,str(ASSET/'World/Scripts'))
from formation_controls_v004 import create_world
D['B']['clean']();root,ctrl,instances=create_world(ASSET);local=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL']
check('new canonical API defaults12m/show',local['length_m']==12 and local['show']==1)
ctrl['show_hardware']=0;ctrl.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update()
check('canonical API hardware visibility propagates',all(instances[n].hide_render for n in ['WORLD_HARDWARE','WORLD_UPHOLE_EXTENSION','WORLD_UPHOLE_JOINT']))
ctrl['show_hardware']=1;ctrl.update_tag();bpy.context.view_layer.update();bpy.context.view_layer.update()
check('canonical API restores hardware/continuation',all(not instances[n].hide_render for n in ['WORLD_HARDWARE','WORLD_UPHOLE_EXTENSION','WORLD_UPHOLE_JOINT']))
for k in ['A','B']:
 p=E/f'Reuse_{k}_continuity_canonical-migration_v007.json';data=json.loads(p.read_text());check('canonical save preserves camera/timing/all controls '+k,data['camera_timing_all_controls_preserved'])
out=dict(checks=checks,all_pass=all(c['passed'] for c in checks),native=records,status='Canonical native successor prepared; human appearance approval pending; synchronization handled by sole T45 integrator',limits='Interface is simplified/provisional; coverage is for these saved static views and original consumer camera/travel ranges at12m default only. Recheck other camera paths/shorter lengths.')
(E/'native-verification_canonical_v007.json').write_text(json.dumps(out,indent=2),encoding='utf-8');print('CONTINUITY_VERIFY',len(checks),out['all_pass'],[c for c in checks if not c['passed']],flush=True)
