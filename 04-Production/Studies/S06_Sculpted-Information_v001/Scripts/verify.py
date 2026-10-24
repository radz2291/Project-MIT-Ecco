"""Source comparison independent of shader appearance; inspect the saved, evaluated mesh."""
import bpy,sys,json,math,hashlib
import numpy as np
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
B=Path(__file__).resolve().parents[1];ROOT=B.parents[2]
mode=sys.argv[-1] if sys.argv[-1] in ('proof','journey') else 'proof'
bpy.ops.wm.open_mainfile(filepath=str(B/f'Scenes/S06_{mode}_v001.blend'))
s=bpy.context.scene;ob=s.objects['Recorded geometry | illustrative S03 source']
d=np.load(B/'Data/surface_samples.npz');meta=json.loads((B/'Records/source.json').read_text())
source=ROOT/meta['source'];a=np.load(source)
same=np.array_equal(d['radius_m'],a['actual_radius_m'][np.ix_(d['source_row'],d['source_col'])]);assert same
assert hashlib.sha256(source.read_bytes()).hexdigest()==meta['source_sha256']
raw=d['radius_m'];nz,na=raw.shape;rad=np.c_[raw,raw[:,0]];n=rad.size
stored=np.empty(n,dtype='f');ob.data.attributes['source_radius_m'].data.foreach_get('value',stored)
assert np.array_equal(stored,rad.ravel())
dep=d['depth_from_interval_top_m'];angles=np.linspace(0,math.tau,na+1)
az,dp=np.meshgrid(angles,dep);height=dep[-1]
def evaluated(f):
    s.frame_set(f);dg=bpy.context.evaluated_depsgraph_get();ev=ob.evaluated_get(dg);me=ev.to_mesh()
    co=np.empty(n*3,dtype='f');me.vertices.foreach_get('co',co);ev.to_mesh_clear();return co.reshape(nz,na+1,3)
closed=evaluated(1);flat=evaluated(s.frame_end)
closed_r=np.sqrt(closed[:,:,0]**2+(closed[:,:,1]-.156)**2)
radius_error=float(abs(closed_r-rad).max());xerror=float(abs(flat[:,:,0]-.156*(az-math.pi)).max());yerror=float(abs(flat[:,:,1]).max());zerror=float(abs(flat[:,:,2]-(height/2-dp)).max())
assert max(radius_error,xerror,yerror,zerror)<1e-6
assert np.all(np.diff(flat[:,0,2])<0)
assert np.array_equal(rad[:,0],rad[:,-1]);assert np.max(abs(closed[:,0,:]-closed[:,-1,:]))<1e-6
features=[]
for label,find in [('enlargement',np.argmax),('tight_region',np.argmin)]:
    j,k=np.unravel_index(find(raw),raw.shape);idx=j*(na+1)+k
    frames=[]
    for f in range(1,s.frame_end+1):
        co=evaluated(f).reshape(-1,3)[idx]
        from mathutils import Vector
        p=world_to_camera_view(s,s.camera,Vector(co));assert 0<p.x<1 and 0<p.y<1
        frames.append([f,float(p.x),float(p.y)])
    features.append({'feature':label,'source_row':int(d['source_row'][j]),'source_col':int(d['source_col'][k]),'source_radius_m':float(raw[j,k]),'map_azimuth_deg':float(angles[k]*180/math.pi),'relative_depth_m':float(dep[j]),'same_id_each_frame':int(idx),'all_frames_inside_image':True,'screen_trajectory':frames})
missing=[lib.filepath for lib in bpy.data.libraries if not Path(bpy.path.abspath(lib.filepath)).exists()]
assert not missing
out={'mode':mode,'actual_saved_native_reopened':True,'source_values_exact':same,'source_sha256_unchanged':True,'geometry_samples':int(raw.size),'duplicated_seam_samples':nz,'max_closed_radius_error_m':radius_error,'max_map_x_error_m':xerror,'max_map_plane_error_m':yerror,'max_depth_error_m':zerror,'depth_increases_down':True,'seam_source_values_identical':True,'missing_dependencies':missing,'font_packed':all(f.packed_file is not None for f in bpy.data.fonts if f.filepath and not f.filepath.startswith('<')),'data_class':'synthetic illustrative surface samples; no field measurement or calibration claim','render_interpolation':'Source values at vertices retained; faces interpolate for display. Not new measured samples.','features':features}
(B/f'Records/{mode}-verification.json').write_text(json.dumps(out,indent=2));print('DATA AND MAPPING VERIFIED',mode)
