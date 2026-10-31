"""Fresh native self-checks for the bounded T44 cleanup, not human acceptance."""
import bpy,sys,runpy,json,math,struct,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];ASSET=ROOT/'04-Production/Shared/Assets';TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v006';E=REV/'Evidence';SCENES=REV/'Scenes'
sys.path.insert(0,str(HERE));sys.argv=['script','--','noop'];B=runpy.run_path(str(HERE/'build_world_t44.py'));C=runpy.run_path(str(HERE/'build_cleanup_v006.py'))
checks=[]
def check(n,p,d=None):checks.append(dict(name=n,passed=bool(p),detail=d))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(o):
 h=hashlib.sha256()
 for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
 for p in o.data.polygons:h.update(struct.pack('<I',len(p.vertices)));h.update(struct.pack('<%dI'%len(p.vertices),*p.vertices))
 return h.hexdigest()
for filename in ['manifest_v004.json','manifest_v005.json']:
 m=json.loads((ASSET/'World'/filename).read_text())
 for i in m.get('sources',[])+m['artifacts']:check('preserved '+i['path'],sha(ROOT/i['path'])==i['sha256'])
old=ASSET/'WellAssembly/World_environment_v005.blend';C['openfile'](old)
names=[o.name for o in bpy.data.objects if o.type=='MESH' and o.name!='MUD_CINEMATIC_SECTION']
before={n:signature(bpy.data.objects[n]) for n in names}
C['openfile'](ASSET/'WellAssembly/World_environment_v009.blend')
for n,h in before.items():check('unchanged environment geometry '+n,signature(bpy.data.objects[n])==h)
for n in ['CASING_FULL','CASING_CUTAWAY']:
 m=bpy.data.objects[n].data;check('analytic cylindrical corner normals '+n,m.has_custom_normals and sum(p.use_smooth for p in m.polygons)==18432)
check('no render-overlapping illustrative shoe surfaces',bpy.data.objects['ILLUSTRATIVE_SHOE_RIM'].hide_render)
for n in ['MUD_CURVED_REAR_OPTICAL_SKIN','MUD_CURVED_OPTICAL_CUT']:
 o=bpy.data.objects[n];margin=min((.1589405 if v.co.x<0 else .155575)-math.hypot(v.co.y,v.co.z) for v in o.data.vertices)
 check('fluid inside every registered bore '+n,margin>=.0004,dict(minimum_margin_m=margin))
check('fluid uses continuous alpha blending',bpy.data.materials['WORLD_StaticFluid_v009'].surface_render_method=='BLENDED')
C['openfile'](ASSET/'BHA/BHA_film_v006.blend');deps=bpy.context.evaluated_depsgraph_get();pts=[]
for o in bpy.data.objects:
 if o.name.startswith('PDC_') and o.type=='MESH':
  ev=o.evaluated_get(deps);me=ev.to_mesh();pts.extend(o.matrix_world@v.co for v in me.vertices);ev.to_mesh_clear()
rmax=max(math.hypot(p.y,p.z) for p in pts);xmin=min(p.x for p in pts);xmax=max(p.x for p in pts)
check('evaluated bit within registered diameter and axial envelope',rmax<=.155575+.000002 and xmin>=2.9-.000002 and xmax<=3.24+.000002,dict(radius_max_m=rmax,diameter_max_m=2*rmax,x_min_m=xmin,x_max_m=xmax))
check('evaluated gauge reaches registered12.25in diameter',abs(rmax-.155575)<.000002,dict(radius_max_m=rmax))
check('six integral blades',sum(o.name.startswith('PDC_INTEGRAL_BLADE') for o in bpy.data.objects)==6)
check('48 cutter substrates and tables',sum(o.name.startswith('PDC_COMPACT') for o in bpy.data.objects)==48 and sum(o.name.startswith('PDC_TABLE') for o in bpy.data.objects)==48)
check('six recessed nozzle mouths',sum(o.name.startswith('PDC_NOZZLE_') and not o.name.startswith('PDC_NOZZLE_BORE') for o in bpy.data.objects)==6)
native=[]
for name in ['downhole_A','downhole_B','layers','BHA_detail','BHA_face','Reuse_A','Reuse_B']:
 C['inspect'](name,'v010');native.append(json.loads((E/(name+'_fresh-open_v010.json')).read_text()))
 for v in ['v006','v007','v008','v009','v010']:
  p=E/(name+'_migration_'+v+'.json')
  if p.exists():
   m=json.loads(p.read_text());check('camera/timing/local controls retained '+name+' '+v,m['preserved_camera_timing_controls'])
for k in ['A','B']:
 a=json.loads((TASK/'Revision_v005/Evidence'/f'migration_{k}_v005.json').read_text())['after']
 C['openfile'](SCENES/f'Reuse_{k}_cleanup_v010.blend');z=B['snapshot']()
 check('end-to-end prior reuse camera/timing '+k,a['camera']==z['camera'] and a['timing']==z['timing'] and a['local_controls']==z['local_controls'])
from formation_controls_v003 import create_world
B['clean']();root,ctrl,instances=create_world(ASSET)
for cut in [0,1]:
 for variant in [0,1,2]:
  ctrl['cutaway']=cut;ctrl['variant']=variant;ctrl.update_tag();bpy.context.view_layer.update()
  visible=[n for n,o in instances.items() if n.startswith('WORLD_FORMATION_') and not o.hide_render]
  expect='WORLD_FORMATION_'+['NOMINAL','IRREGULAR','SPIRAL'][variant]+('_CUTAWAY' if cut else '_FULL')
  check('one correct formation control '+str((cut,variant)),visible==[expect])
ctrl['show_mud']=0;ctrl.update_tag();bpy.context.view_layer.update();check('fluid visibility control',instances['WORLD_MUD'].hide_render)
data=dict(checks=checks,all_pass=all(c['passed'] for c in checks),native=native,verification='Executor native self-checks; visual and technical acceptance remain human-owned.')
(E/'native-verification_v006.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print('CLEANUP_VERIFY',len(checks),data['all_pass'],[c for c in checks if not c['passed']],flush=True)
