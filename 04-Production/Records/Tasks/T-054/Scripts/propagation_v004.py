import bpy,json,hashlib,shutil
from pathlib import Path
R=Path(__file__).resolve().parents[5];T=R/'04-Production/Records/Tasks/T-054';C=T/'Cache/propagation-v004';C.mkdir(parents=True,exist_ok=True);out=[]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for kind,rel,consumers in [('digital','DigitalEnvironment/Digital_style_v001.blend',[('S03_shared-digital_v004',1),('S06_shared-digital_v002',52)]),('reveal','MeasurementReveal/Measurement_reveal_v001.blend',[('S02_shared-reveal_v001',480),('Reveal_two-shapes_v001',60)])]:
 source=R/'04-Production/Shared/Assets'/rel;original=digest(source);copy=C/source.name;shutil.copy2(source,copy)
 # Remap libraries on saved disposable consumers, never production consumers.
 files=[]
 for name,frame in consumers:
  bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers'/f'{name}.blend'),load_ui=False)
  lib=next(l for l in bpy.data.libraries if Path(bpy.path.abspath(l.filepath)).resolve()==source.resolve());lib.filepath=str(copy);lib.reload()
  dst=C/f'{name}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(dst));files.append((dst,frame))
 def inspect():
  results=[]
  for dst,frame in files:
   bpy.ops.wm.open_mainfile(filepath=str(dst),load_ui=False);bpy.context.scene.frame_set(frame);dg=bpy.context.evaluated_depsgraph_get()
   if kind=='digital':
    values={g.name:list(g.nodes.get('Group Output').inputs['Color'].default_value) for g in bpy.data.node_groups if g.name.startswith('ECCO shared cyan palette') and g.library and Path(bpy.path.abspath(g.library.filepath)).resolve()==copy.resolve()};assert values
    results.append(values)
   else:
    names=['ONE WALL - old history and current cells share topology'] if dst.stem.startswith('S02') else [o.name for o in bpy.context.scene.objects if o.type=='MESH']
    results.append({n:len(bpy.data.objects[n].evaluated_get(dg).data.polygons) for n in names})
  return results
 before=inspect();bpy.ops.wm.open_mainfile(filepath=str(copy),load_ui=False)
 if kind=='digital':
  for g in bpy.data.node_groups:
   if g.name.startswith('ECCO shared cyan palette'):g.nodes['Group Output'].inputs['Color'].default_value=(.31,.07,.17,1)
 else:
  g=bpy.data.node_groups['ECCO Stored Surface Reveal v001'];output=next(n for n in g.nodes if n.bl_idname=='NodeGroupOutput')
  for link in list(g.links):
   if link.to_node==output:g.links.remove(link)
 bpy.ops.wm.save_as_mainfile(filepath=str(copy));after=inspect();assert all(a!=b for a,b in zip(before,after)),(kind,before,after)
 shutil.copy2(source,copy);restored=inspect();assert restored==before;assert digest(source)==original
 out.append({'kind':kind,'method':'Saved disposable exact shared master copy; saved consumers relinked; edited master saved; fresh reopened consumers evaluated; byte-exact copied master restoration and reopened verification. Production masters/consumers never saved.','before':before,'after':after,'restored':restored,'source_unchanged':True,'two_consumers_changed':True,'test_master_restored_sha256':digest(copy)})
(T/'Evidence/propagation-v004.json').write_text(json.dumps(out,indent=2));print('PROPAGATION_PASS',[(x['kind'],x['two_consumers_changed']) for x in out])
