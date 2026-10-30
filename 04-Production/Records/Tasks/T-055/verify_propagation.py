"""Bounded successor-only edit with byte-exact restoration, two saved consumer reopens."""
import bpy,json,hashlib
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets';src=A/'Surface/Surface_descent_v005.blend'
original=src.read_bytes();before=hashlib.sha256(original).hexdigest();name='T055 earth | Cutaway earth 00 side -1'
def read():
 out=[]
 for sid in ['S01','S02']:
  p=T/'Consumers'/f'{sid}_shared-descent_v002.blend';bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False)
  mesh=next(m for m in bpy.data.meshes if m.name==name and m.library)
  out.append({'consumer':sid,'x':mesh.vertices[0].co.x,'library':mesh.library.filepath})
 return out
baseline=read()
try:
 bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False);bpy.data.meshes[name].vertices[0].co.x+=.001
 bpy.context.preferences.filepaths.save_version=0;bpy.ops.wm.save_as_mainfile(filepath=str(src),compress=True)
 changed=read()
 assert all(abs(b['x']+.001-c['x'])<1e-6 for b,c in zip(baseline,changed))
finally:src.write_bytes(original)
restored=read();assert baseline==restored;assert hashlib.sha256(src.read_bytes()).hexdigest()==before
bpy.ops.wm.open_mainfile(filepath=str(src),load_ui=False)
col=bpy.data.collections['SURFACE_SUBSEA_v004'];bounds={}
for o in col.objects:
 if o.type=='MESH' and o.name in ['SUBSEA_Foundation','RIG_MarineRiser','SUBSEA_BOPStack','SUBSEA_GuidePost']:
  pts=[o.matrix_world@Vector(v) for v in o.bound_box];bounds[o.name]=[[min(p[i] for p in pts),max(p[i] for p in pts)] for i in range(3)]
(T/'Evidence/propagation-and-joins-v005.json').write_text(json.dumps({'baseline':baseline,'changed':changed,'restored':restored,'byte_exact_restore':True,'source_sha256':before,'subsea_bounds':bounds,'seabed_z':-120,'riser_top_z':10,'limits':'Illustrative adaptation; not certified engineering fit'},indent=2))
print('PROPAGATION_RESTORED',before)
