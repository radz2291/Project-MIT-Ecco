import pathlib,json,hashlib
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';old=json.loads((T/'publication-manifest_ribbon_v010.json').read_text())['local_only'];out=[]
for x in old:
 p=R/x['path'];h=hashlib.sha256(p.read_bytes()).hexdigest();out.append({'path':x['path'],'sha256':h,'matches_preserved_manifest':h==x['sha256']})
for path,expected in [('04-Production/Shared/Assets/Acoustics/PressureField_v007/S02_pressure-field-proof_v007.blend','940efed0f0cb2254c8301a58141c40532e3fcf1528e7958638b6e8a40260e519'),('04-Production/Records/Tasks/T-056/Previews/pressure-field_v007_slow-review.mp4','79d072cac103e17fd6a8bcdd408db98c1ed93db3911cca99bbd6538a1a76b96c')]:
 h=hashlib.sha256((R/path).read_bytes()).hexdigest();out.append({'path':path,'sha256':h,'matches_preserved_manifest':h==expected})
(T/'formation-preservation_v011.json').write_text(json.dumps(out,indent=2));print('Preserved',all(x['matches_preserved_manifest'] for x in out),len(out))
