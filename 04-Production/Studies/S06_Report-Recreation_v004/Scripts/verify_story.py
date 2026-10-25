import bpy,json,hashlib,math
import numpy as np
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_ABC_study_v004.blend'))
D=np.load(B/'Data/story_field.npz');R=float(D['R']);H=float(D['H']);raw=D['radius'];nz,na=raw.shape;rr=np.c_[raw,raw[:,0]];TH,ZZ=np.meshgrid(np.linspace(0,math.tau,na+1),D['z'])
def coords(p):
    dist=R*TH;curl=math.tau*R*(1-p);t=(dist-curl)/R;dev=(rr-R)*(1-p)
    return np.stack([np.where(dist<curl,(R+dev)*np.sin(t),dist-curl),np.where(dist<curl,-(R+dev)*np.cos(t),-R-dev),ZZ],-1).reshape(-1,3)
def arr(o):return np.array([v.co[:] for v in o.data.vertices])
def colors(o):return np.array([v.color[:] for v in o.data.color_attributes['Illustrative sample colors'].data])
A=bpy.data.objects['A | reconstructed wall beginning to open'];BB=bpy.data.objects['B | same reconstructed samples'];C=bpy.data.objects['C | same geometry map'];mini=bpy.data.objects['C | same geometry reconstruction']
errors={}
for o in (A,BB):
    assert all(k.value==0 for k in list(o.data.shape_keys.key_blocks)[1:]),'Inactive stored poses must remain zero'
    errors[o.name]=float(abs(arr(o)-coords(o['p'])).max());assert errors[o.name]<1e-6
    radii=np.array([v.value for v in o.data.attributes['illustrative_radius_m'].data]);assert np.allclose(radii,rr.ravel(),atol=1e-8)
    assert np.array_equal(colors(o),colors(C))
assert np.array_equal(colors(mini),colors(C))
mini_expected=coords(0);mini_expected[:,0]=-.165+mini_expected[:,0]*.72;mini_expected[:,1]=-.11+mini_expected[:,1]*.72;mini_expected[:,2]=.70+mini_expected[:,2]*(1.06/H)
assert np.allclose(arr(mini),mini_expected,atol=1e-6)
ampB=bpy.data.objects['B | independent amplitude'];ampC=bpy.data.objects['C | independent amplitude'];assert np.array_equal(colors(ampB),colors(ampC));assert not np.array_equal(colors(C),colors(ampC))
housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];meshhash=hashlib.sha256(arr(housing).astype('f').tobytes()).hexdigest();build=json.loads((B/'Records/ABC-build.json').read_text())
assert meshhash==build['source_mesh_local_coordinates_sha256'];assert all(abs(v-1)<1e-8 for v in bpy.data.objects['ECCO_ROOT'].scale)
bpy.context.window.scene=bpy.data.scenes['A | Borehole to reconstruction'];bpy.context.view_layer.update()
world=np.array([housing.matrix_world@v.co for v in housing.data.vertices]);maxrad=float(np.hypot(world[:,0],world[:,1]).max());axial=float(np.ptp(world[:,2]));assert abs(axial-2.4)<1e-5
clearance=float(np.hypot(arr(A)[:,0],arr(A)[:,1]).min()-maxrad);assert clearance>.02
assert not list(bpy.data.images);assert not list(bpy.data.libraries)
assert all(o.data.font.packed_file for ss in bpy.data.scenes for o in ss.objects if o.type=='FONT')
assert all(t['under_five_seconds'] for t in build['scenes'].values())
bs=bpy.data.scenes['B | Same surface unfolds'];bpy.context.window.scene=bs;bpy.context.view_layer.update()
uv=np.array([world_to_camera_view(bs,bs.camera,v.co)[:2] for o in (BB,ampB) for v in o.data.vertices]);bounds=[uv.min(0).tolist(),uv.max(0).tolist()];assert uv.min()>.035 and uv.max()<.965
result={'saved_native_reopened':True,'shared_geometry_colors_A_B_C_exact':True,'C_miniature_same_radius_grid':True,'amplitude_independent_and_identical_B_C':True,'review_pose_max_error_m':errors,'source_mesh_unchanged':True,'hardware_axial_extent_m':axial,'hardware_max_radius_m':maxrad,'minimum_conservative_graphic_to_tool_radial_clearance_m':clearance,'B_complete_pair_in_frame':bounds,'source_images_packed':0,'external_libraries':0,'fonts_packed':True,'all_stills_under_five_seconds':True,'animation_verified':False,'audience_acceptance':'Pending owner still review'}
(B/'Records/ABC-verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print('ABC VERIFIED',json.dumps(result))
