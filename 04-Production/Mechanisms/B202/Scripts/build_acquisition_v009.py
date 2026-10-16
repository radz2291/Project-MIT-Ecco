"""Deterministic synthetic acquisition from actual evaluated Blender walls.
Standalone background process only. Generates data, never cinematic motion.
"""
import bpy,math,json,sys,hashlib,numpy as np
from pathlib import Path
from mathutils import Vector,Matrix
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';DATA=BASE/'Data/v009';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence/v009'
sys.path.insert(0,str(BASE/'Scripts'))
from acquisition_core_v009 import *
C=read_json(BASE/'acquisition_config_v009.json')
T5=ROOT/'04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend';T6=ROOT/'04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
def filehash(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def source_matrix(o):
    q=o.rotation_quaternion if o.rotation_mode=='QUATERNION' else o.rotation_euler.to_quaternion();m=Matrix.LocRotScale(o.location,q,o.scale)
    return source_matrix(o.parent)@o.matrix_parent_inverse@m if o.parent else m
def load_sources():
    bpy.ops.wm.open_mainfile(filepath=str(T6));rig=bpy.data.objects['ASSEMBLY_CONTROL'];rig['cutaway']=0
    walls={}
    for mode,name in [(0,'nominal'),(1,'irregular'),(2,'spiral')]:
        rig['variant']=mode;rig.update_tag();bpy.context.view_layer.update();o=bpy.data.objects[name.upper()+'_FULL'];ev=o.evaluated_get(bpy.context.evaluated_depsgraph_get());me=ev.to_mesh();me.calc_loop_triangles()
        walls[name]=([tuple(ev.matrix_world@v.co) for v in me.vertices],[tuple(t.vertices) for t in me.loop_triangles]);ev.to_mesh_clear()
    sensors=[]
    for i in range(1,4):
        o=bpy.data.objects[f'ECCO_SENSOR_REF_{i:02d}'];m=source_matrix(o);p=m.translation;n=(m.to_3x3()@Vector((0,0,1))).normalized()
        sensors.append({'sensor_id':i-1,'reference_name':o.name,'local_origin_m':list(p),'local_outward_direction':list(n),'proxy_acoustic_face':True})
    return walls,sensors
class RayWall:
    """Blender BVH fast path, float64 triangle fallback at numerical seams.
    A miss stays a miss if the independent triangle intersection finds none.
    No wall radius shortcut or manufactured return is used.
    """
    def __init__(self,vertices,triangles):
        self.bvh=BVHTree.FromPolygons([Vector(v) for v in vertices],triangles,all_triangles=True,epsilon=0.)
        tri=np.asarray(vertices,dtype=np.float64)[np.asarray(triangles)];self.a=tri[:,0];self.e1=tri[:,1]-tri[:,0];self.e2=tri[:,2]-tri[:,0];self.xmin=tri[:,:,0].min(axis=1);self.xmax=tri[:,:,0].max(axis=1)
    def ray_cast(self,origin,direction,maximum):
        result=self.bvh.ray_cast(origin,direction,maximum)
        if result[0] is not None:return (*result,'blender_bvh')
        o=np.asarray(origin,dtype=np.float64);d=np.asarray(direction,dtype=np.float64);xend=o[0]+maximum*d[0]
        ids=np.flatnonzero((self.xmin<=max(o[0],xend)+1e-8)&(self.xmax>=min(o[0],xend)-1e-8))
        if not len(ids):return None,None,None,None,'no_triangle_hit'
        a=self.a[ids];e1=self.e1[ids];e2=self.e2[ids];p=np.cross(d,e2);det=np.einsum('ij,ij->i',e1,p);inv=np.zeros_like(det);nz=np.abs(det)>1e-14;inv[nz]=1/det[nz];tv=o-a;u=np.einsum('ij,ij->i',tv,p)*inv;q=np.cross(tv,e1);v=np.einsum('ij,j->i',q,d)*inv;t=np.einsum('ij,ij->i',e2,q)*inv
        good=np.flatnonzero(nz&(u>=-1e-9)&(v>=-1e-9)&(u+v<=1+1e-9)&(t>0)&(t<=maximum))
        if not len(good):return None,None,None,None,'no_triangle_hit'
        k=good[np.argmin(t[good])];normal=np.cross(e1[k],e2[k]);normal/=np.linalg.norm(normal)
        return Vector(o+d*t[k]),Vector(normal),int(ids[k]),float(t[k]),'float64_triangle_fallback'
def bvh_wall(vertices,triangles):return RayWall(vertices,triangles)
def changed_wall(vs):
    out=[]
    for x,y,z in vs:
        a=math.atan2(z,y);angle=math.atan2(math.sin(a-2.5),math.cos(a-2.5));dr=.008*math.exp(-((x-3.0)/.35)**2-(angle/.5)**2);r=math.hypot(y,z)+dr;out.append((x,r*math.cos(a),r*math.sin(a)))
    return out
def tight_wall(vs):
    out=[]
    for x,y,z in vs:
        a=math.atan2(z,y);angle=math.atan2(math.sin(a-2.5),math.cos(a-2.5));r=C['nominal_radius_m']-.0012*math.exp(-((x-2.73)/.4)**2-(angle/.65)**2);out.append((x,r*math.cos(a),r*math.sin(a)))
    return out
def acquire(case,bvh,sensors,c,material='constant',eccentric=(0.,0.),orientations=None,max_distance=None):
    events=[];truth={};phase0=math.atan2(sensors[0]['local_origin_m'][2],sensors[0]['local_origin_m'][1]);start=math.tau/(2*c['azimuth_bins'])-phase0
    count=c['tool_orientations_per_depth'] if orientations is None else orientations;seq=0
    for di,depth in enumerate(c['depths_m']):
        for ri in range(count):
            angle=start+ri*math.tau/c['tool_orientations_per_depth'];R=Matrix.Rotation(angle,3,'X')
            # Quasi-static fixture poses, not physical drilling speed/cadence.
            translation=Vector((depth-sensors[0]['local_origin_m'][0],*eccentric))
            for ref in sensors:
                sid=ref['sensor_id'];n=(R@Vector(ref['local_outward_direction'])).normalized();origin=translation+R@Vector(ref['local_origin_m'])+n*c['sensor_radial_offset_m'];eid=f'{case}:d{di:02d}:r{ri:03d}:s{sid}'
                e={'id':eid,'source_kind':'synthetic_illustrative','timestamp_s':seq*c['synthetic_event_spacing_s'],'sensor_id':sid,'receiver_sensor_id':sid,'tool_pose':{'translation_m':list(translation),'rotation_xyz_rad':[angle,0.,0.]},'sensor_origin_m':list(origin),'outward_direction':list(n),'mud_sound_speed_m_s':c['mud_sound_speed_m_s'],'tof_2way_s':None,'echo_strength':None,'valid_tof':False,'valid_amplitude':False,'quality_flag':'no_wall_hit_within_demo_range'};seq+=1
                hit,normal,face,distance,method=bvh.ray_cast(origin,n,max_distance or c['max_ray_distance_m']);e['raycast_method']=method
                if hit is not None:
                    distance=(hit-origin).length;inc=abs((-n).dot(normal.normalized()));echo,factors=forward_echo(tuple(hit),distance,inc,material,c)
                    valid=distance>=c['blind_zone_demo_m'] and echo>=c['minimum_echo_strength'];e.update(tof_2way_s=2*distance/c['mud_sound_speed_m_s'],echo_strength=echo,valid_tof=valid,valid_amplitude=valid,quality_flag=('weak_patch_valid' if factors['coherent_patch_factor']<1 else 'valid') if valid else 'synthetic_echo_rejected',incidence_cos=inc,response_factors=factors)
                    truth[eid]={'hit_position_m':list(hit),'wall_normal':list(normal),'triangle_index':face,'stand_off_m':distance}
                events.append(e)
    return events,truth
def produce():
    DATA.mkdir(parents=True,exist_ok=True);E.mkdir(parents=True,exist_ok=True)
    assert not (DATA/'index_v009.json').exists(),'Refuse overwrite of existing v009 data; version any correction'
    preserve=[p for p in BASE.rglob('*v008*') if p.is_file() and p.suffix not in ['.log','.pyc']]+[T5,T6,ROOT/'04-Production/Mechanisms/B201/Scenes/B201_pulse-echo_fast-preview_v005.blend',ROOT/'04-Production/Mechanisms/B201/Previews/Motion_v005/B201_pulse-echo_fast-preview_v005.mp4']
    preservation={p.relative_to(ROOT).as_posix():filehash(p) for p in sorted(set(preserve))};write_json(E/'preservation_before_v009.json',preservation)
    walls,sensors=load_sources();walls['tight']=(tight_wall(walls['irregular'][0]),walls['irregular'][1]);walls['irregular_changed']=(changed_wall(walls['irregular'][0]),walls['irregular'][1])
    cases={
      'nominal_constant':dict(wall='nominal',material='constant'),
      'irregular_constant':dict(wall='irregular',material='constant'),
      'irregular_changed_constant':dict(wall='irregular_changed',material='constant'),
      'irregular_material_changed':dict(wall='irregular',material='changed_constant'),
      'irregular_layers':dict(wall='irregular',material='layers'),
      'spiral_layers':dict(wall='spiral',material='layers'),
      'tight_layers':dict(wall='tight',material='layers'),
      'eccentric_nominal':dict(wall='nominal',material='constant',eccentric=(.0007,-.0006)),
      'sparse_irregular':dict(wall='irregular',material='layers',orientations=10),
      'missed_nominal':dict(wall='nominal',material='constant',max_distance=.001),
      'weak_nominal':dict(wall='nominal',material='constant',threshold=.9)}
    index={'version':'v009','config_sha256':filehash(BASE/'acquisition_config_v009.json'),'source_hashes':{p.relative_to(ROOT).as_posix():filehash(p) for p in (T5,T6)},'sensors':sensors,'cases':{}}
    for case,opts in cases.items():
        opts=dict(opts);name=opts.pop('wall');threshold=opts.pop('threshold',C['minimum_echo_strength']);config={**C,'minimum_echo_strength':threshold};vs,ts=walls[name];bvh=bvh_wall(vs,ts)
        events,truth=acquire(case,bvh,sensors,config,**opts);processed=reconstruct(events,config);grid=grid_samples(processed,config,case)
        paths={key:f'{case}_{key}_v009.json.gz' for key in ['events','truth','grid']}
        for key,value in [('events',events),('truth',truth),('grid',grid)]:write_json(DATA/paths[key],value)
        params={'minimum_echo_strength':threshold,'orientations_per_depth':opts.get('orientations',C['tool_orientations_per_depth']),'max_ray_distance_m':opts.get('max_distance',C['max_ray_distance_m']),'known_eccentric_yz_m':list(opts.get('eccentric',(0.,0.)))}
        index['cases'][case]={'wall':name,'material':opts['material'],'case_parameters':params,'wall_sha256':digest({'vertices':vs,'triangles':ts}),'events':len(events),'valid_events':len(processed),'measured_bins':sum(p['measured'] for p in grid['cells']),'files':paths,'content_sha256':{key:digest(value) for key,value in [('events',events),('truth',truth),('grid',grid)]}}
        print(case,len(events),len(processed),index['cases'][case]['measured_bins'],flush=True)
    write_json(DATA/'index_v009.json',index)
    # Inspectable small trace; full records above retain every event/factor.
    base=read_json(DATA/index['cases']['irregular_layers']['files']['events']);grid=read_json(DATA/index['cases']['irregular_layers']['files']['grid']);cell=next(p for p in grid['cells'] if p['measured']);lookup={e['id']:e for e in base}
    write_json(E/'example_bin_trace_v009.json',{'case':'irregular_layers','cell':cell,'source_events':[lookup[i] for i in cell['event_ids']]})
    write_json(E/'build_acquisition_v009.json',{'index_sha256':filehash(DATA/'index_v009.json'),'event_count':sum(x['events'] for x in index['cases'].values()),'cases':index['cases'],'preservation_count':len(preservation)})
    print('B202_V009_ACQUISITION_PASS')
if __name__=='__main__':produce()
