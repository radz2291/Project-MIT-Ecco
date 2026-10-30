import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets'
files=[A/'ECCO/Satin_finish_v001.blend',A/'ECCO/ECCO_film_v003.blend',A/'BHA/BHA_core_satin_v001.blend',A/'BHA/BHA_film_v008.blend']+list((T/'Consumers').glob('*.blend'))
result=[]
for p in files:
    bpy.ops.wm.open_mainfile(filepath=str(p)); s=bpy.context.scene
    libs=[{'path':l.filepath,'absolute':bpy.path.abspath(l.filepath),'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
    result.append({'file':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'libraries':libs,'objects':len(bpy.data.objects),'groups':[{'name':g.name,'linked':bool(g.library),'revision':g.get('revision')} for g in bpy.data.node_groups if 'Satin finish' in g.name]})
lib=A/'ECCO/Satin_finish_v001.blend';original=lib.read_bytes();prop=[]
try:
    bpy.ops.wm.open_mainfile(filepath=str(lib));g=bpy.data.node_groups['ECCO | Satin finish v001'];g['revision']=2
    g.nodes['Math.001'].inputs[1].default_value=.321
    bpy.ops.wm.save_as_mainfile(filepath=str(lib))
    for p in [T/'Consumers/S07_shared-satin_v001.blend',T/'Consumers/S05_shared-satin_v001.blend']:
        bpy.ops.wm.open_mainfile(filepath=str(p));g=bpy.data.node_groups['ECCO | Satin finish v001'];prop.append({'consumer':p.name,'revision':g['revision'],'roughness_base':g.nodes['Math.001'].inputs[1].default_value,'observed_edit':g['revision']==2})
finally:lib.write_bytes(original)
(T/'Evidence/package-verification.json').write_text(json.dumps({'files':result,'propagation':prop,'restored_library_sha256':hashlib.sha256(lib.read_bytes()).hexdigest()},indent=2))
print('VERIFY',len(files),prop)
