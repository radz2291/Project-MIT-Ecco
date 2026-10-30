"""Versioned shared surface/descent package; preserve local cameras and animation."""
import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets'
S={s['id']:R/s['native'] for s in json.loads((R/'04-Production/Records/Tasks/T-050/sources.json').read_text())}
sys.path.insert(0,str(A/'WellAssembly/Scripts'))
from world_interface_v010 import link_variant,s02_placement
DEST=A/'Surface/Surface_descent_v004.blend'
def save(path):
 for lib in bpy.data.libraries:lib.filepath=bpy.path.abspath(lib.filepath)
 bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
 bpy.ops.file.make_paths_relative()
 bpy.ops.wm.save_as_mainfile(filepath=str(path),compress=True)
def append_collection(path,name):
 with bpy.data.libraries.load(str(path),link=False) as (a,b):b.collections=[name]
 return b.collections[0]
def camera():
 s=bpy.context.scene;res=[]
 for f in [1,60,120,180,220,240,min(241,s.frame_end),min(264,s.frame_end),s.frame_end]:
  s.frame_set(f);c=s.camera;res.append([f,[list(r) for r in c.matrix_world],c.data.lens])
 return res
# Capture selected earth meshes, keeping motion and local object bindings out of the library.
bpy.ops.wm.read_factory_settings(use_empty=True)
with bpy.data.libraries.load(str(S['S01']),link=False) as (a,b):
 b.objects=[n for n in a.objects if n.startswith(('Cutaway earth','Formation rear','Earth seam','Opening front'))]
earth=list(b.objects)
ec=bpy.data.collections.new('SURFACE_DESCENT_EARTH_SOURCE');bpy.context.scene.collection.children.link(ec)
mapping={}
for o in earth:
 for c in list(o.users_collection):c.objects.unlink(o)
 ec.objects.link(o);o.animation_data_clear();o.data=o.data.copy();o.data.name='T055 earth | '+o.name
 # Widen only far boundary; local animated opening remains exactly where authored.
 if o.name.startswith('Cutaway earth'):
  sign=1 if o.name.endswith(' 1') else -1
  for v in o.data.vertices:
   if v.co.x*sign>0:v.co.x=sign*3.5
   if v.co.y>0:v.co.y=5.5
 mapping[o.name]=o.data.name
 o.hide_render=True
ec.hide_render=True
rig=append_collection(S['SURFACE'],'SURFACE_REUSED_RIG');rig.name='SURFACE_RIG_v004'
print('RIG_LOADED',flush=True)
sub=append_collection(S['SURFACE-ORIGINAL'],'03_SUBSEA');sub.name='SURFACE_SUBSEA_v004'
print('SUB_LOADED',flush=True)
root=bpy.data.collections.new('SURFACE_RIG_SUBSEA_v004');bpy.context.scene.collection.children.link(root);root.children.link(rig);root.children.link(sub)
bpy.context.view_layer.update()
print('LINKED',flush=True)
for col in [rig,sub]:
 col.hide_render=False;col.hide_viewport=False
 for o in list(col.objects):
  if o is None:continue
  o.animation_data_clear();o.hide_render=False
  if o.type not in ['MESH','CURVE']:continue
  if col==sub and o.type=='MESH':
   o.data=o.data.copy();world=o.matrix_world.copy();inv=world.inverted()
   for v in o.data.vertices:
    p=world@v.co
    if p.z<=-145:p.z+=40
    elif p.z<10:p.z+=40*(10-p.z)/155
    if o.name=='SUBSEA_Foundation' and p.z < -119:p.z=-120
    v.co=inv@p
meta=bpy.data.objects.new('SURFACE_DEScent_INFO',None);root.objects.link(meta)
meta['source']='Surface v003 rig + original03_SUBSEA; illustrative resized water-column span'
meta['seabed_z_m']=-120.0;meta['riser_top_z_m']=10.0
meta['world_destination']='World_environment_v010 / WORLD_S02_PHYSICAL_CUTAWAY / canonical_to_s02'
save(DEST)
(T/'Evidence/earth-mapping.json').write_text(json.dumps(mapping,indent=2))
records=[]
proxy_prefix=('Deck side','Deck end','Platform leg','Rig machinery','Roof trim','Service building','Upper building')
for sid in ['S01','S02']:
 bpy.ops.wm.open_mainfile(filepath=str(S[sid]),load_ui=False);before=camera();s=bpy.context.scene
 removed=[]
 for o in list(s.objects):
  if not o.library and o.name.startswith(proxy_prefix):removed.append(o.name);bpy.data.objects.remove(o,do_unlink=True)
 with bpy.data.libraries.load(str(DEST),link=True) as (a,b):b.collections=['SURFACE_RIG_SUBSEA_v004'];b.meshes=list(mapping.values())
 inst=bpy.data.objects.new('Shared surface rig and subsea v004',None);s.collection.objects.link(inst);inst.instance_type='COLLECTION';inst.instance_collection=b.collections[0]
 loaded={m.name:m for m in b.meshes};replaced=[]
 for name,mname in mapping.items():
  o=bpy.data.objects.get(name)
  if o and not o.library:o.data=loaded[mname];replaced.append(name)
 if sid=='S02':
  original=bpy.data.objects['S02 geological wall retained section'];ad=original.animation_data
  world=link_variant(A,'WORLD_S02_PHYSICAL_CUTAWAY',s02_placement(A),'Shared descent World destination')
  if ad and ad.action:
   world.animation_data_create();world.animation_data.action=ad.action
   try:world.animation_data.action_slot=ad.action_slot
   except:pass
  bpy.data.objects.remove(original,do_unlink=True)
 else:
  world=link_variant(A,'WORLD_S02_PHYSICAL_CUTAWAY',s02_placement(A),'Shared descent World destination')
  world.hide_render=True;world.hide_viewport=True
  world['visibility_note']='S01-only copy ends240; canonical destination replaces old retained section from241 in continuous S02 copy.'
 assert before==camera(),'camera changed'
 s.frame_set(1);out=T/'Consumers'/f'{sid}_shared-descent_v001.blend';save(out)
 records.append({'baseline':str(S[sid].relative_to(R)),'candidate':str(out.relative_to(R)),'frames':[1,60,120,180,220,240,s.frame_end],'removed_proxy_objects':removed,'shared_earth_meshes':len(replaced),'camera_preserved':True})
(T/'Evidence/consumer-mappings.json').write_text(json.dumps(records,indent=2))
print('BUILT',str(DEST),len(records))
