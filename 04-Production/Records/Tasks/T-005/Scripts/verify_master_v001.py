"""Fresh-process self-checks of saved master. Does not save the .blend."""
import bpy,json,math,hashlib,array
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';ASSET=ROOT/'Shared/Assets/ECCO'
def sig(o):
    a=array.array('f',[0.0])*(len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a)
    b=array.array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',b)
    return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];root=bpy.data.objects['ECCO_ROOT'];rot=bpy.data.objects['ECCO_ROTATION_X'];refs=[bpy.data.objects['ECCO_SENSOR_REF_%02d'%i] for i in range(1,4)]
saved_library_count=len(bpy.data.libraries)
with bpy.data.libraries.load(str(ASSET/'Originals/Source_Imported_ecco.blend'),link=False) as (src,dst):dst.objects=src.objects
source=next(o for o in dst.objects if o and o.type=='MESH')
bpy.context.scene.collection.objects.link(source)
bpy.context.view_layer.update()
radius=max(math.hypot(v.co.y,v.co.z)*.001 for v in housing.data.vertices)
angles=sorted(math.degrees(math.atan2(o.location.z,o.location.y))%360 for o in refs)
spacing=[(angles[(i+1)%3]-angles[i])%360 for i in range(3)]
initial=[o.matrix_world.translation.copy() for o in refs]
rot.rotation_euler.x=math.pi/2;root.location.x=.1;bpy.context.view_layer.update()
errors=[]
for start,o in zip(initial,refs):
    expected=Vector((start.x+.1,-start.z,start.y));errors.append((o.matrix_world.translation-expected).length)
checks={'fresh_open':True,'source_vertex_and_loop_signature_equal':sig(source)==sig(housing),'source_object_matrix_equal':False, 'three_refs_120deg':max(abs(v-120) for v in spacing)<1e-5,'common_source_X_730mm':all(abs(o.location.x-.730)<1e-7 for o in refs),'rotation_and_axial_travel':max(errors)<1e-6,'non_destructive_cutaway_disabled':all(not m.show_viewport and not m.show_render for m in housing.modifiers),'no_external_libraries':saved_library_count==0,'no_external_images':all(i.source!='FILE' or i.packed_file for i in bpy.data.images),'source_step_reference_resolves':Path(bpy.path.abspath(housing['source_step'])).exists(),'no_added_product_faces_or_plugs':len(bpy.data.collections['ECCO_GEOMETRY_REPLACEABLE'].objects)==1}
# Return to saved default before checking matrices.
rot.rotation_euler.x=0;root.location.x=0;bpy.context.view_layer.update()
checks['source_object_matrix_equal']=all(abs(source.matrix_world[r][c]-housing.matrix_world[r][c])<1e-7 for r in range(4) for c in range(4))
result={'checks':checks,'all_pass':all(checks.values()),'maximum_source_axis_radius_m':radius,'maximum_source_axis_diameter_m':2*radius,'sensor_angles_deg':angles,'sensor_spacing_deg':spacing,'motion_error_m':errors,'units':{'system':bpy.context.scene.unit_settings.system,'scale_length':bpy.context.scene.unit_settings.scale_length},'note':'Self-checks, not independent engineering approval. No replacement received. Thread fit/internal mud sensor/shoulder datum unverified.'}
(TASK/'master-verification_v001.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
assert result['all_pass'],result
print('B101_VERIFY_COMPLETE',json.dumps(result))
