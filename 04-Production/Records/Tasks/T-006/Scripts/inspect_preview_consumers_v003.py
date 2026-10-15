"""Fresh-open every delivered moving-preview source; inspect actual instances."""
import bpy,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
rows=json.loads((TASK/'Evidence/preview-renders_v003.json').read_text());result=[]
for row in rows:
    path=ROOT.parent/row['scene'];bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
    rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    libraries=[{'stored':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).is_file(),
                'sha256':hashlib.sha256(Path(bpy.path.abspath(l.filepath)).read_bytes()).hexdigest()} for l in bpy.data.libraries]
    instances=[i.object.name for i in bpy.context.evaluated_depsgraph_get().object_instances
               if i.is_instance and (i.object.name=='ECCO_HOUSING_SOURCE_MESH' or 'TEMP | ' in i.object.name)]
    visible=[n for n in ('NOMINAL_CUTAWAY','IRREGULAR_CUTAWAY','SPIRAL_CUTAWAY') if not bpy.data.objects[n].hide_render]
    checks={'saved_source_matches_render':hashlib.sha256(path.read_bytes()).hexdigest()==row['scene_sha256'],
            'relative_libraries_resolve':all(l['stored'].startswith('//') and l['exists'] for l in libraries),
            'linked_product_and_nine_closures':len(instances)==10,
            'correct_visible_variant':visible==[('NOMINAL','IRREGULAR','SPIRAL')[row['variant']]+'_CUTAWAY'],
            'initial_travel':abs(rig['travel_m']-row['travel_m'][0])<1e-6}
    s.frame_set(row['frames']);bpy.context.view_layer.update()
    checks['end_travel']=abs(rig['travel_m']-row['travel_m'][1])<1e-6
    checks['end_full_rotation']=abs(rig['rotation_rad']-row['rotation_rad'][1])<1e-6
    result.append({'name':row['name'],'checks':checks,'libraries':libraries,'all_pass':all(checks.values())})
assert all(r['all_pass'] for r in result),result
(TASK/'Evidence/preview-consumer-checks_v003.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('CONSUMERS_PASS',[r['name'] for r in result])
