import bpy,json,pathlib,math,hashlib
from mathutils import Matrix
ROOT=pathlib.Path(__file__).resolve().parents[5];A=ROOT/'04-Production/Shared/Assets';T=ROOT/'04-Production/Records/Tasks/T-053'
sources={x['id']:ROOT/x['native'] for x in json.loads((ROOT/'04-Production/Records/Tasks/T-050/sources.json').read_text())}
M=Matrix(((0,0,1,735),(1,0,0,0),(0,1,0,0),(0,0,0,1)))
bpy.ops.wm.open_mainfile(filepath=str(sources['WORLD']),load_ui=False)
changes=[]
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith('FORMATION_'):
  count=0
  for v in o.data.vertices:
   r=math.hypot(v.co.y,v.co.z)
   if r>2.39:
    v.co.y*=20/2.4;v.co.z*=20/2.4;count+=1
  changes.append(dict(object=o.name,outer_vertices=count,inner_unchanged=True))
  o['outer_radius_m']=20.0;o['scope']='Outer soil extension only; inner wall and axial profile preserved'
with bpy.data.libraries.load(str(sources['S02']),link=False) as (a,b):
 b.objects=['S02 WALL AUTHORITY full irregular inner surface','S02 geological wall retained section']
for o in b.objects:
 authority='AUTHORITY' in o.name
 name='WORLD_S02_IRREGULAR_AUTHORITY' if authority else 'WORLD_S02_PHYSICAL_CUTAWAY'
 c=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(c);c.objects.link(o)
 o.animation_data_clear();o.parent=None;o.matrix_world=Matrix.Identity(4);o.hide_render=authority;o.hide_viewport=authority
 o.name=name+'_MESH';o.data=o.data.copy()
 count=0
 for v in o.data.vertices:
  if not authority and math.hypot(v.co.x,v.co.y)>.3199:
   v.co.x*=20/.32;v.co.y*=20/.32;count+=1
  v.co=M@v.co
 o['source_object']='S02 WALL AUTHORITY full irregular inner surface' if authority else 'S02 geological wall retained section'
 o['source_file']=str(sources['S02'].relative_to(ROOT));o['canonical_axis']='X; X=z+735, Y=x, Z=y'
 o['outer_radius_m']=20.0
 if not authority:
  o.shape_key_add(name='Basis');k=o.shape_key_add(name='Outer_soil_margin_25m')
  for p in k.data:
   if math.hypot(p.co.y,p.co.z)>19.99:p.co.y*=1.25;p.co.z*=1.25
  changes.append(dict(object=o.name,outer_vertices=count,inner_unchanged=True))
 # Whole collection is selected through a local collection instance, never combine alternate walls.
 bpy.context.scene.collection.children.unlink(c);c.use_fake_user=True
 c.hide_render=False;c.hide_viewport=False
for sid in ['FORMATION','CASED-FORMATION','CASING']:
 with bpy.data.libraries.load(str(sources[sid]),link=True) as (a,b):b.collections=list(a.collections)
 # Library collections are available for selective linking, not automatically stacked into the scene.
 for c in b.collections:c.use_fake_user=True
ctrl=bpy.data.objects.new('WORLD_INTERFACE_v010',None);bpy.context.scene.collection.objects.link(ctrl)
ctrl['outer_radius_m']=20.;ctrl['axis']='X';ctrl['s02_origin_depth_m']=-735.;ctrl['shape_policy']='Select one wall/formation variant; do not stack nominal and irregular collections'
ctrl['physical_layers']='Bore fluid -> steel casing (when present) -> cement -> formation; channel/wear source variants remain in CasedHole_v002'
out=A/'WellAssembly/World_environment_v010.blend'
for l in bpy.data.libraries:l.filepath=bpy.path.abspath(l.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
for l in bpy.data.libraries:l.filepath=bpy.path.relpath(l.filepath)
bpy.ops.wm.save_as_mainfile(filepath=str(out),compress=True)
interface=dict(version='v010',native=str(out.relative_to(ROOT)),units='metres',axis='X',source_to_canonical=[list(r) for r in M],canonical_to_s02=[list(r) for r in M.inverted()],s02_axial_bounds=[-15,15],outer_radius_m=20,wall_collections=['WORLD_S02_IRREGULAR_AUTHORITY','WORLD_S02_PHYSICAL_CUTAWAY'],legacy_collections=[c.name for c in bpy.data.collections if c.name.startswith('WORLD_') and not c.library],source_modules={k:str(sources[k].relative_to(ROOT)) for k in ['FORMATION','CASED-FORMATION','CASING']},policy='Exactly one selected wall and outer formation per placement. S02 authority is physical shape only; no measurement samples or display animation included. S02 cutaway retains source angular opening. Legacy cutaways retain their original half-space. Layer visibility is controlled on local collection instances; no global changes to shared collection hide flags.',changes=changes)
(A/'WellAssembly/World_interface_v010.json').write_text(json.dumps(interface,indent=2))
(T/'Evidence/build-v010.json').write_text(json.dumps(interface,indent=2))
print('BUILT',out)
