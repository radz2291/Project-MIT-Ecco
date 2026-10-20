import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2]
rows=[]
for version in ['v009','v014','v023','v028','v033','v036']:
 for path in sorted((R/version/'Scenes').glob('*.blend')):
  bpy.ops.wm.open_mainfile(filepath=str(path))
  row={'version':version,'scene':str(path.relative_to(R)),'libraries':[],'images':[],'fonts':[]}
  for x in bpy.data.libraries:row['libraries'].append({'path':x.filepath,'resolved':bpy.path.abspath(x.filepath),'exists':Path(bpy.path.abspath(x.filepath)).is_file()})
  for x in bpy.data.images:
   if x.source!='FILE':continue
   row['images'].append({'name':x.name,'path':x.filepath,'packed':bool(x.packed_file),'packed_sha256':hashlib.sha256(bytes(x.packed_file.data)).hexdigest() if x.packed_file else None,'resolved':bpy.path.abspath(x.filepath),'exists':Path(bpy.path.abspath(x.filepath)).is_file()})
  for x in bpy.data.fonts:
   if x.filepath!='<builtin>':row['fonts'].append({'path':x.filepath,'packed':bool(x.packed_file),'exists':Path(bpy.path.abspath(x.filepath)).is_file()})
  rows.append(row)
  (R/'Closure/Retained-scene-dependencies.json').write_text(json.dumps(rows,indent=2))
print('AUDITED',len(rows),flush=True)
