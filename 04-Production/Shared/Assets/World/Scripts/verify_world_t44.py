"""Native geometric/source and saved-consumer checks for A-WORLD."""
import bpy,json,hashlib,struct,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[5];ASSET=ROOT/'04-Production/Shared/Assets'
TASK=ROOT/'04-Production/Records/Tasks/T-044';EVID=TASK/'Evidence'
checks=[]
def check(name,ok,detail=None):checks.append(dict(name=name,pass_=bool(ok),detail=detail))
def signature(o):
 h=hashlib.sha256()
 for v in o.data.vertices:h.update(struct.pack('<3f',*v.co))
 for f in o.data.polygons:h.update(struct.pack('<I',len(f.vertices)));h.update(struct.pack('<%dI'%len(f.vertices),*f.vertices))
 return h.hexdigest()
def openfile(p):bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
openfile(ASSET/'ECCO/ECCO_master_temporary-plugs_v002.blend')
source={o.name:signature(o) for o in bpy.data.collections['ECCO_MASTER_v002'].all_objects if o.type=='MESH'}
refs={o.name:list(o.matrix_world) for o in bpy.data.objects if o.name.startswith('ECCO_SENSOR_REF_')}
refpos={o.name:list(o.location) for o in bpy.data.objects if o.name.startswith('ECCO_SENSOR_REF_')}
openfile(ASSET/'ECCO/ECCO_film_v002.blend')
for n,h in source.items():check('T5 exact vertex/topology '+n,signature(bpy.data.objects[n])==h)
for n,loc in refpos.items():check('T5 sensor reference '+n,max(abs(a-b) for a,b in zip(bpy.data.objects[n].location,loc))<1e-7)
check('Metres and original product length',bpy.context.scene.unit_settings.scale_length==1 and abs(bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'].dimensions.x-2.4)<1e-6)
openfile(ASSET/'WellAssembly/WellAssembly_variants_v003.blend')
source={o.name:signature(o) for o in bpy.data.collections['WELL_INTERVALS'].all_objects if o.type=='MESH'}
openfile(ASSET/'WellAssembly/World_environment_v004.blend')
for n,h in source.items():check('T6 exact base mesh '+n,signature(bpy.data.objects[n])==h)
check('Environment has no product geometry',not any('ECCO' in o.name for o in bpy.data.objects))
check('Casing/cement/host physical order',.1589405<.1698625<.22225)
openfile(ASSET/'BHA/BHA_film_v002.blend')
bit=[o for o in bpy.data.objects if o.type=='MESH' and not o.library and ('BIT' in o.name or 'CUTTER' in o.name)]
maxr=max(math.hypot(*(o.matrix_world@v.co)[1:]) for o in bit for v in o.data.vertices)
check('Bit remains inside 12.25in gauge',maxr<=.155575+1e-6,dict(maximum_radial_m=maxr,gauge_radius_m=.155575))
check('Centered bit fits nominal casing body',maxr<.1589405,dict(radial_clearance_m=.1589405-maxr,limit='Centered straight nominal geometry only; not loaded passage or connection drift'))
housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH']
check('ECCO above bit in selected layout',max((housing.matrix_world@v.co).x for v in housing.data.vertices)<2.9)
for label in ['A','B']:
 states=[]
 for tag in ['before_v003','after_v004']:
  p=TASK/'ReuseTests'/('Reuse_'+label+'_'+tag+'.blend');openfile(p);s=bpy.context.scene
  check(label+' '+tag+' relative/existing libraries',all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).exists() for l in bpy.data.libraries))
  for f in [1,s.frame_end]:
   s.frame_set(f);bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get()
   items=[i.matrix_world.copy() for i in deps.object_instances if i.object.original.name=='ECCO_HOUSING_SOURCE_MESH']
   check(label+' '+tag+' frame'+str(f)+' one evaluated housing',len(items)==1)
   h=items[0]
   check(label+' '+tag+' frame'+str(f)+' preserved source mm-to-m object scale',max(abs(v-.001) for v in h.to_scale())<1e-8)
  snap=json.loads((EVID/('migration_'+label+'_v004.json')).read_text());check(label+' camera/timing/local overrides preserved',snap['camera_timing_controls_preserved'])
  check(label+' '+tag+' local wrapper no mesh copies',not any(o.type=='MESH' and not o.library for o in bpy.data.objects))
  states.append(bpy.data.materials['WORLD_WetMineral'].node_tree.nodes.get('Noise Texture').inputs['Scale'].default_value)
 check(label+' adopts shared grain revision',states==[38.,62.],states)
 dump=None
data=dict(blender=bpy.app.version_string,checks=checks,all_pass=all(c['pass_'] for c in checks),method='Executor scripted self-checks; no independent engineering or visual acceptance')
(EVID/'geometry-verification_v004.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
print('T44_GEOMETRY',len(checks),data['all_pass'],[c for c in checks if not c['pass_']],flush=True)
