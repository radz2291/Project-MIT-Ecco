"""Fresh-open verification of removable temporary closures; no saved edits."""
import bpy,json,hashlib,array,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';ASSET=ROOT/'Shared/Assets/ECCO'
e=json.loads((TASK/'Evidence/temporary-plugs-build_v002.json').read_text());v1=json.loads((TASK/'Evidence/build-evidence_v001.json').read_text())
housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];closures=list(bpy.data.collections['ECCO_TEMPORARY_CLOSURES'].objects);rot=bpy.data.objects['ECCO_ROTATION_X'];root=bpy.data.objects['ECCO_ROOT']
a=array.array('f',[0.0])*(len(housing.data.vertices)*3);housing.data.vertices.foreach_get('co',a)
b=array.array('i',[0])*len(housing.data.loops);housing.data.loops.foreach_get('vertex_index',b)
signature=hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
bpy.context.view_layer.update();initial=[o.matrix_world.copy() for o in closures];placement_errors=[]
for row in e['closures']:
    obj=bpy.data.objects[row['name']];placement_errors.append(max(abs(obj.matrix_world[r][c]-row['matrix_source_m'][r][c]) for r in range(4) for c in range(4)))
rot.rotation_euler.x=math.pi/2;root.location.x=.1;bpy.context.view_layer.update()
motion_errors=[]
for o,m in zip(closures,initial):
    p=m.translation;expected=Vector((p.x+.1,-p.z,p.y));motion_errors.append((o.matrix_world.translation-expected).length)
checks={'fresh_open':True,'v001_file_unchanged':hashlib.sha256((ASSET/'ECCO_master_v001.blend').read_bytes()).hexdigest()==e['source_v001_sha256'],'source_mesh_unchanged':signature==v1['measured']['mesh_signature'],'nine_removable_closures':len(closures)==9,'closures_follow_rotation_control':all(o.parent==rot for o in closures),'source_axis_mapping_correct':max(placement_errors)<1e-6,'rotation_and_axial_motion':max(motion_errors)<1e-6,'closures_explicitly_temporary':all('TEMPORARY' in o['status'] for o in closures),'source_step_resolves':Path(bpy.path.abspath(housing['source_step'])).exists(),'no_external_libraries':len(bpy.data.libraries)==0,'no_external_images':all(i.source!='FILE' or i.packed_file for i in bpy.data.images)}
result={'all_pass':all(checks.values()),'checks':checks,'placement_max_error':max(placement_errors),'motion_max_error_m':max(motion_errors),'master_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'note':'Executor self-checks only. Temporary caps/plates are visual interpretations; assembled STEP still pending. Sensor refs not engineering-approved.'}
(TASK/'Evidence/temporary-plugs-verification_v002.json').write_text(json.dumps(result,indent=2),encoding='utf-8');assert result['all_pass'],result;print('V002_VERIFY_PASS',result)
