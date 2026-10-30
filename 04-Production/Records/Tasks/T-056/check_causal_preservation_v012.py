import pathlib,json,hashlib
R=pathlib.Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');T=R/'04-Production/Records/Tasks/T-056';out=[]
for manifest in ['publication-manifest_ribbon_v010.json','publication-manifest_formation_v011.json']:
 for x in json.loads((T/manifest).read_text())['local_only']:
  h=hashlib.sha256((R/x['path']).read_bytes()).hexdigest();out.append({'path':x['path'],'sha256':h,'matches_previous':h==x['sha256']})
for path,expect in [('04-Production/Shared/Assets/Acoustics/PressureField_v007/S02_pressure-field-proof_v007.blend','940efed0f0cb2254c8301a58141c40532e3fcf1528e7958638b6e8a40260e519'),('04-Production/Records/Tasks/T-056/Previews/pressure-field_v007_slow-review.mp4','79d072cac103e17fd6a8bcdd408db98c1ed93db3911cca99bbd6538a1a76b96c')]:
 h=hashlib.sha256((R/path).read_bytes()).hexdigest();out.append({'path':path,'sha256':h,'matches_previous':h==expect})
(T/'causal-preservation_v012.json').write_text(json.dumps(out,indent=2));print('Preservation',len(out),'files',all(x['matches_previous'] for x in out))
