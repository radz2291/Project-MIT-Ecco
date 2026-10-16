import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
tables=json.loads((BASE/'sampling_tables_v008.json').read_text());checks=[]
bpy.ops.wm.open_mainfile(filepath=str(ROOT/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'));c=bpy.data.objects['ASSEMBLY_CONTROL'];c['cutaway']=0
for mode,name in [(1,'irregular'),(2,'spiral')]:
    c['variant']=mode;c.update_tag();bpy.context.view_layer.update();ev=bpy.data.objects[name.upper()+'_FULL'].evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh()
    vs=[tuple(v.co) for v in me.vertices];fs=[tuple(p.vertices) for p in me.polygons];ids={i for i,v in enumerate(vs) if 1.5<=v[0]<=4.8};used={i for f in fs if all(i in ids for i in f) for i in f}
    actual={tuple(round(x,7) for x in vs[i]) for i in used};saved={tuple(round(x,7) for x in v) for v in tables[name]['vertices']};checks.append({'check':'independent fresh T6 evaluated '+name,'pass':actual==saved,'source_vertices':len(actual),'derived_vertices':len(saved)});ev.to_mesh_clear()
manifest=json.loads((ROOT/'04-Production/Records/Tasks/T-007/Evidence/Motion_v005/output-manifest.json').read_text())
for entry in manifest['outputs'][:2]:
    p=ROOT/'04-Production'/entry['path'];checks.append({'check':'accepted T7 byte preservation '+entry['path'],'pass':hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']})
out={'passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks};(E/'source-correspondence_v008.json').write_text(json.dumps(out,indent=2));print(json.dumps(out));assert all(x['pass'] for x in checks)
