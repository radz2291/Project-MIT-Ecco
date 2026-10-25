import bpy,json,math,hashlib
from pathlib import Path
B=Path(__file__).resolve().parents[1]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_report-recreation_v004.blend'))
s=bpy.context.scene
nodes=[n for m in bpy.data.materials if m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE']
assert not nodes and not list(bpy.data.images),'Source imagery found'
assert not list(bpy.data.actions),'Still unexpectedly has animation'
assert all(math.isfinite(v) for o in s.objects if o.type=='MESH' for p in o.data.vertices for v in p.co)
used_fonts={o.data.font for o in s.objects if o.type=='FONT'}
print('FONT CHECK',[(f.name,f.filepath,bool(f.packed_file)) for f in used_fonts])
assert all(f.packed_file or f.filepath=='<builtin>' for f in used_fonts)
assert not list(bpy.data.libraries)
texts=[o.data.body for o in s.objects if o.type=='FONT']
assert not any(any(c.isdigit() for c in t) for t in texts if t not in ('360° geometry','REPORT SHAPE  /  RECREATED IN 3D'))
out={'saved_native_reopened':True,'source_image_nodes':len(nodes),'images':len(bpy.data.images),'animation_actions':len(bpy.data.actions),'external_libraries':0,'fonts_packed':True,'mesh_coordinates_finite':True,'text':texts,'scope':'One still. No integration. No recovered measurement claim.'}
(B/'Records/saved-verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('SAVED NATIVE VERIFIED')
