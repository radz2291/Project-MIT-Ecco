"""Focused source, geometry, controls and fresh-open checks for T44 revision."""
import bpy,json,hashlib,struct,sys,runpy,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[4];ASSET=ROOT/'04-Production/Shared/Assets';TASK=ROOT/'04-Production/Records/Tasks/T-044';REV=TASK/'Revision_v005';E=REV/'Evidence';SCENES=REV/'Scenes'
sys.path.insert(0,str(HERE));sys.argv=['script','--','noop'];B=runpy.run_path(str(HERE/'build_world_t44.py'))
R=runpy.run_path(str(HERE/'build_formation_revision_v005.py'))
checks=[]
def check(name,value,detail=None):checks.append(dict(name=name,passed=bool(value),detail=detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def signature(o):
 h=hashlib.sha256()
 for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
 for p in o.data.polygons:h.update(struct.pack('<I',len(p.vertices)));h.update(struct.pack('<%dI'%len(p.vertices),*p.vertices))
 return h.hexdigest()
old=json.loads((ASSET/'World/manifest_v004.json').read_text())
for item in old['sources']+old['artifacts']:check('preserved '+item['path'],sha(ROOT/item['path'])==item['sha256'])
names=[v+'_'+kind for v in ['NOMINAL','IRREGULAR','SPIRAL','CASING','CEMENT'] for kind in ['FULL','CUTAWAY']]
bpy.ops.wm.open_mainfile(filepath=str(ASSET/'WellAssembly/World_environment_v004.blend'),load_ui=False,use_scripts=False);oldmesh={n:signature(bpy.data.objects[n]) for n in names}
bpy.ops.wm.open_mainfile(filepath=str(ASSET/'WellAssembly/World_environment_v005.blend'),load_ui=False,use_scripts=False)
for n,h in oldmesh.items():check('unchanged registered wall/layer mesh '+n,signature(bpy.data.objects[n])==h)
for obj in [o for o in bpy.data.objects if o.name.startswith('FORMATION_') and o.type=='MESH']:
 v=0 if 'NOMINAL' in obj.name else 1 if 'IRREGULAR' in obj.name else 2
 margin=min(math.hypot(p.co.y,p.co.z)-R['radius'](p.co.x,math.atan2(p.co.z,p.co.y),v) for p in obj.data.vertices)
 check('surrounding mass stays outside source bore '+obj.name,margin>=.0006,dict(minimum_margin_m=margin))
check('formation has no product copy',not any('ECCO' in o.name for o in bpy.data.objects))
files=['downhole_A_v006.blend','downhole_B_v006.blend','layers_v010.blend','BHA_detail_v006.blend','wide_context_v007.blend','Reuse_A_formation_v005.blend','Reuse_B_formation_v005.blend']
native=[]
for filename in files:
 p=SCENES/filename;rec=R['inspect'](p);native.append(rec)
 check('fresh-open relative links '+filename,all(l['exists'] and l['path'].startswith('//') for l in rec['libraries']))
 check('metric source units '+filename,rec['units']==1)
 if filename.startswith(('downhole','BHA','Reuse')):check('one product '+filename,rec['mesh_instances']==1)
for k in ['A','B']:
 data=json.loads((E/f'migration_{k}_v005.json').read_text());check('camera/timing/local controls preserved '+k,data['preserved_camera_timing_controls'])
from formation_controls_v002 import create_world
B['clean']();root,ctrl,instances=create_world(ASSET)
for cut in [0,1]:
 for variant in [0,1,2]:
  ctrl['cutaway']=cut;ctrl['variant']=variant;ctrl['show_formation']=1;ctrl.update_tag();bpy.context.view_layer.update()
  visible=[n for n,o in instances.items() if n.startswith('WORLD_FORMATION_') and not o.hide_render]
  expect='WORLD_FORMATION_'+['NOMINAL','IRREGULAR','SPIRAL'][variant]+('_CUTAWAY' if cut else '_FULL')
  check('one matching formation variant '+str((cut,variant)),visible==[expect],visible)
ctrl['show_formation']=0;ctrl.update_tag();bpy.context.view_layer.update();check('formation visibility control',all(o.hide_render for n,o in instances.items() if n.startswith('WORLD_FORMATION_')))
p=ASSET/'Formation/Formation_cased-section_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
obj=bpy.data.objects['CASED_FORMATION_MASS'];check('upper-host section stays above boundary',max(v.co.x for v in obj.data.vertices)<0);check('upper-host section inner radius preserved',min(math.hypot(v.co.y,v.co.z) for v in obj.data.vertices)>=.2229)
data=dict(checks=checks,all_pass=all(c['passed'] for c in checks),native=native,verification='Executor self-checks. Rendered appearance acceptance belongs to Radzi; geometric/source checks do not certify engineering.')
(E/'native-verification_v005.json').write_text(json.dumps(data,indent=2),encoding='utf-8');print('FORMATION_VERIFY',len(checks),data['all_pass'],[c for c in checks if not c['passed']],flush=True)
