import bpy,numpy as np,json,hashlib,math
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2];OLD=B.with_name('S06_Sculpted-Information_v001')
bpy.ops.wm.open_mainfile(filepath=str(OLD/'Scenes/S06_journey_v001.blend'))
oldob=bpy.context.scene.objects['Recorded geometry | illustrative S03 source']
oldkeys=[np.array([p.co[:] for p in key.data],dtype='f') for key in oldob.data.shape_keys.key_blocks]
bpy.ops.wm.open_mainfile(filepath=str(B/'Scenes/S06_cinematic-study_v002.blend'))
s=bpy.context.scene;ob=s.objects['Recorded geometry | illustrative S03 source']
for src,key in zip(oldkeys,ob.data.shape_keys.key_blocks):assert np.array_equal(src,np.array([p.co[:] for p in key.data],dtype='f'))
d=np.load(B/'Data/surface_samples.npz');meta=json.loads((B/'Records/source.json').read_text(encoding='utf-8'));source=ROOT/meta['source'];original=np.load(source)
assert np.array_equal(d['radius_m'],original['actual_radius_m'][np.ix_(d['source_row'],d['source_col'])])
assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['source_sha256']
raw=d['radius_m'];nz,na=raw.shape;rad=np.c_[raw,raw[:,0]];n=rad.size;depth=d['depth_from_interval_top_m'];H=float(depth[-1])
stored=np.empty(n,dtype='f');ob.data.attributes['source_radius_m'].data.foreach_get('value',stored);assert np.array_equal(stored,rad.ravel())
def evaluated(f):
    s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();eo=ob.evaluated_get(dg);me=eo.to_mesh();co=np.array([v.co[:] for v in me.vertices]);eo.to_mesh_clear();return co.reshape(nz,na+1,3)
closed=evaluated(1);flat=evaluated(288);ang=np.linspace(0,math.tau,na+1);TH,DP=np.meshgrid(ang,depth)
errors={'closed_radius_m':float(abs(np.sqrt(closed[:,:,0]**2+(closed[:,:,1]-.156)**2)-rad).max()),'flat_x_m':float(abs(flat[:,:,0]-.156*(TH-math.pi)).max()),'flat_y_m':float(abs(flat[:,:,1]).max()),'depth_m':float(abs(flat[:,:,2]-(H/2-DP)).max())}
assert max(errors.values())<1e-6
assert np.array_equal(rad[:,0],rad[:,-1]);assert np.all(np.diff(flat[:,0,2])<0)
features=[]
for label,func in [('enlargement',np.argmax),('tight',np.argmin)]:
    j,k=np.unravel_index(func(raw),raw.shape);features.append({'label':label,'id':int(j*(na+1)+k),'source_row':int(d['source_row'][j]),'source_col':int(d['source_col'][k]),'radius_m':float(raw[j,k]),'trajectory':[],'occluded_frames':[]})
bounds=[]
for f in range(1,289):
    co=evaluated(f).reshape(-1,3);dg=bpy.context.evaluated_depsgraph_get()
    for item in features:
        p=Vector(co[item['id']]);screen=world_to_camera_view(s,s.camera,p)
        assert 0<screen.x<1 and 0<screen.y<1
        item['trajectory'].append([f,float(screen.x),float(screen.y)])
        direction=(p-s.camera.location).normalized();hit,location,normal,face,hitob,matrix=s.ray_cast(dg,s.camera.location,direction,distance=(p-s.camera.location).length+.001)
        if hit and (location-p).length>.004:item['occluded_frames'].append(f)
    if f%12==1:
        pts=[world_to_camera_view(s,s.camera,Vector(v)) for v in co[::24]]
        bounds.append({'frame':f,'xmin':min(v.x for v in pts),'xmax':max(v.x for v in pts),'ymin':min(v.y for v in pts),'ymax':max(v.y for v in pts)})
amp=np.load(B/'Data/independent_amplitude.npz');AA,DD=np.meshgrid(ang[:-1],depth/H)
expected=np.clip(.48+.20*np.sin(2*math.pi*(9*DD+.21*np.sin(AA+.4)))+.13*np.sin(2*math.pi*(28*DD+.07*np.cos(2*AA)))+.10*np.cos(3*AA-9*DD)+.05*np.sin(7*AA+60*DD),0,1).astype('f')
assert np.array_equal(expected,amp['amplitude_normalized'])
derived=np.load(B/'Data/derived_report_arrays.npz');diam=raw+np.roll(raw,na//2,axis=1)
for key,vals in [('diameter_min_m',diam.min(1)),('diameter_mean_m',diam.mean(1)),('diameter_max_m',diam.max(1)),('radial_std_m',raw.std(1))]:assert np.array_equal(derived[key],vals)
out={'native_reopened':True,'all_33_shape_keys_bitwise_equal_to_v001':True,'source_values_exact':True,'geometry_samples':raw.size,'errors':errors,'depth_down':True,'seam_duplicates_equal':True,'independent_amplitude_formula_verified':True,'report_geometry_arrays_verified':True,'missing_libraries':[lib.filepath for lib in bpy.data.libraries if not Path(bpy.path.abspath(lib.filepath)).exists()],'fonts_packed':all(f.packed_file is not None for f in bpy.data.fonts if f.filepath and not f.filepath.startswith('<')),'feature_tracking':features,'sampled_screen_bounds':bounds,'claim_limit':'Implementation correspondence; illustrative data, not engineering or instrument accuracy certification'}
assert not out['missing_libraries']
(B/'Records/verification.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print('VERIFIED',errors,'occlusion frames',[len(x['occluded_frames']) for x in features])
