"""Temporary, removable visualization closures; v001 and supplied mesh preserved."""
import bpy,json,hashlib,time,array
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-005';ASSET=ROOT/'Shared/Assets/ECCO'
OLD=Path(r'C:\Users\RZ1\Desktop\RZ\261008-MIT-Ecco\04-Project\01-ECCO_First_Ping-Test\01-Blender\ECCO_First_Ping.blend')
v1=ASSET/'ECCO_master_v001.blend';before=hashlib.sha256(v1.read_bytes()).hexdigest()
def sig(o):
    a=array.array('f',[0.0])* (len(o.data.vertices)*3);o.data.vertices.foreach_get('co',a)
    b=array.array('i',[0])*len(o.data.loops);o.data.loops.foreach_get('vertex_index',b)
    return hashlib.sha256(a.tobytes()+b.tobytes()).hexdigest()
housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];original_sig=sig(housing);scene=bpy.context.scene;master=bpy.data.collections['ECCO_MASTER_v001'];master.name='ECCO_MASTER_v002'
collection=bpy.data.collections.new('ECCO_TEMPORARY_CLOSURES');master.children.link(collection)
with bpy.data.libraries.load(str(OLD),link=False) as (src,dst):
    dst.objects=[n for n in src.objects if n=='ENP3 | source geometry presentation copy' or n.startswith(('Imaging port ','Service port ','Service cover '))]
old_housing=next(o for o in dst.objects if o.name.startswith('ENP3 | source geometry'))
old_source_matches=sig(old_housing)==original_sig
assert old_source_matches,'Prior presentation housing differs from preserved source'
mapping=housing.matrix_world @ (old_housing.matrix_parent_inverse @ old_housing.matrix_basis).inverted()
closure_data=[]
mat=bpy.data.materials.new('TEMP_CLOSURES_neutral');mat.diffuse_color=(.45,.48,.52,1)
for old in dst.objects:
    if old==old_housing:continue
    local=old.matrix_parent_inverse @ old.matrix_basis
    placement=mapping @ local
    old.parent=None;old.animation_data_clear();old.constraints.clear()
    old.name='TEMP | '+old.name;collection.objects.link(old);old.parent=bpy.data.objects['ECCO_ROTATION_X'];old.matrix_world=placement
    if 'Service cover' in old.name:
        # Earlier plates were deep inside the pocket. Seat near the surrounding
        # pad rim using source-mesh ray samples; retain this as visual geometry.
        p=old.matrix_world.translation; n=Vector((0,p.y,p.z)).normalized(); tangent=Vector((0,-n.z,n.y)); inv=housing.matrix_world.inverted(); samples=[]
        for dx,dt in [(-.06,-.032),(.06,.032)]:
            start=Vector((p.x+dx,0,0))+n*.3+tangent*dt
            ok,hit,normal,idx=housing.ray_cast(inv@start,inv.to_3x3()@(-n))
            assert ok
            samples.append((housing.matrix_world@hit).dot(n))
        rim=sum(samples)/len(samples)
        new_matrix=old.matrix_world.copy();new_matrix.translation=Vector((p.x-.015,0,0))+n*(rim-.0012)
        old.matrix_world=new_matrix
        # Original local box X/Y axes are axial/tangential respectively.
        old.scale.x*=.145/.105;old.scale.y*=.080/.054
        old['temporary_fit']='145x80mm plate including pocket extension; top seated at surrounding rim ray samples, not manufacturing design'
        bpy.context.view_layer.update()
        placement=old.matrix_world.copy()
    old.data.materials.clear();old.data.materials.append(mat)
    old['status']='TEMPORARY VISUALIZATION CLOSURE; replace with client assembled STEP; not manufacturing geometry'
    old['provenance']='Earlier First Ping removable presentation component; source-mesh correspondence checked, transformed back to source X axis'
    closure_data.append({'name':old.name,'matrix_source_m':[list(row) for row in placement],'vertices':len(old.data.vertices),'fit':old.get('temporary_fit','Inherited presentation cap/plug mapped to matching source mesh')})
assert len(closure_data)==9
# Remove only unlinked append dependencies introduced by this build.
for o in list(bpy.data.objects):
    if not o.users_collection:bpy.data.objects.remove(o,do_unlink=True)
for library in list(bpy.data.libraries):
    if library.users==0:bpy.data.libraries.remove(library)
master['version']='v002';master['status']='PROVISIONAL TEMPORARILY PLUGGED VISUALIZATION; assembled STEP pending'
master['temporary_closures']='9 removable additions: 3 imaging-port caps, 3 service-port plugs, 3 service covers. Do not treat as official assembly.'
scene['B101']='v002 temporary closures per producer relayed client message, 15 October 2026. No manufacturing approval.'
scene.display.shading.color_type='MATERIAL'
housing.color=(.57,.60,.65,1)
if not housing.data.materials:
    hm=bpy.data.materials.new('Housing_neutral');hm.diffuse_color=(.57,.60,.65,1);housing.data.materials.append(hm)
scene.camera=bpy.data.objects['INSPECT_overview'];scene.render.filepath='//../../../Records/Tasks/T-005/Previews/'
bpy.ops.wm.save_as_mainfile(filepath=str(ASSET/'ECCO_master_temporary-plugs_v002.blend'))
renders=[]
for name in ['overview','opposite','sensor-closeup','end-X0']:
    scene.camera=bpy.data.objects['INSPECT_'+name];scene.render.filepath=str(TASK/'Previews'/('ECCO_temporary-plugs_'+name+'_v002.png'));start=time.perf_counter();bpy.ops.render.render(write_still=True)
    renders.append({'view':name,'seconds':time.perf_counter()-start,'frame':1,'resolution':[1280,720]})
e={'source_v001_unchanged':hashlib.sha256(v1.read_bytes()).hexdigest()==before,'source_v001_sha256':before,'housing_signature_unchanged':sig(housing)==original_sig,'old_presentation_source_mesh_matches':old_source_matches,'old_scene_sha256':hashlib.sha256(OLD.read_bytes()).hexdigest(),'closures':closure_data,'renders':renders,'limits':['Temporary interpretation only, pending official assembled plugged STEP','No end bore closures: functional axial passage retained','Smaller fastener details retained from supplied mesh; not all manufacturing holes certified closed','Sensor references stay at inherited rim centres; not moved to fabricated cap faces']}
(TASK/'Evidence/temporary-plugs-build_v002.json').write_text(json.dumps(e,indent=2),encoding='utf-8');print('TEMP_PLUG_BUILD_COMPLETE',len(closure_data))
