"""Independent T45 Flow verification; isolated Blender, no render or native save."""
import bpy, math, hashlib, struct, json, traceback
from pathlib import Path
from mathutils import Vector

ROOT=Path(__file__).resolve().parents[6]
OUT=Path(__file__).resolve().parent
SCENES=ROOT/'04-Production/Records/Tasks/T-048/Scenes'
SHA='974f138a9634965254dd58ca8a6cb30fb623bfde'
EPS=1e-6

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def mat(m): return [float(x) for row in m for x in row]
def equal(a,b): return max(abs(x-y) for x,y in zip(mat(a),mat(b)))<2e-6

def snapshot():
    s=bpy.context.scene
    return dict(camera=dict(name=s.camera.name,lens=s.camera.data.lens,matrix=mat(s.camera.matrix_world)),
        timing=[s.frame_start,s.frame_end,s.render.fps],
        controls={o.name:dict(o.items()) for o in bpy.data.objects if not o.library and o.name.endswith('_CONTROL') and o.name!='UPHOLE_CONTINUATION_CONTROL'},
        animation={o.name:[(f.data_path,f.array_index,[[float(p.co.x),float(p.co.y)] for p in f.keyframe_points]) for f in o.animation_data.action.layers[0].strips[0].channelbag(o.animation_data.action_slot).fcurves] for o in bpy.data.objects if not o.library and o.animation_data and o.animation_data.action})

def clip(poly,axis_bound,sign):
    ans=[]
    for k,p in enumerate(poly):
        q=poly[(k+1)%len(poly)]
        dp=sign*(p.x-axis_bound);dq=sign*(q.x-axis_bound)
        if dp>=0: ans.append(p)
        if (dp<0)!=(dq<0): ans.append(p+(q-p)*(dp/(dp-dq)))
    return ans

def slab(poly,lo,hi): return clip(clip(poly,lo,1),hi,-1) if poly else []
def minimum_radius(poly):
    yz=[Vector((p.y,p.z)) for p in poly]
    if not yz: return float('inf')
    # If the projected polygon encloses the axis, radial lower bound is zero.
    area=sum(a.x*b.y-a.y*b.x for a,b in zip(yz,yz[1:]+yz[:1]))
    cross=[a.x*b.y-a.y*b.x for a,b in zip(yz,yz[1:]+yz[:1])]
    if abs(area)>1e-12 and (all(c>=-1e-12 for c in cross) or all(c<=1e-12 for c in cross)): return 0.0
    result=min(p.length for p in yz)
    for a,b in zip(yz,yz[1:]+yz[:1]):
        d=b-a;t=max(0,min(1,-a.dot(d)/d.length_squared)) if d.length_squared else 0
        result=min(result,(a+t*d).length)
    return result

def collect(c,seen=None):
    seen=set() if seen is None else seen
    if c.as_pointer() in seen: return set()
    seen.add(c.as_pointer());out=set()
    for o in c.objects:
        if o.type=='MESH': out.add(o.as_pointer())
        if o.instance_collection: out|=collect(o.instance_collection,seen)
    for ch in c.children: out|=collect(ch,seen)
    return out

def check(kind):
    old=SCENES/f'Flow_reuse_{kind}_v005.blend'
    bpy.ops.wm.open_mainfile(filepath=str(old),load_ui=False,use_scripts=False)
    bpy.context.scene.frame_set(1);before=snapshot()
    p=SCENES/f'Flow_reuse_{kind}_v006.blend'
    bpy.ops.wm.open_mainfile(filepath=str(p),load_ui=False,use_scripts=False)
    s=bpy.context.scene;s.frame_set(1);assert snapshot()==before
    dep=bpy.context.evaluated_depsgraph_get()
    hardware=bpy.data.objects['WORLD_HARDWARE_INSTANCE'];flow=bpy.data.objects['FLOW_PLACEMENT'];ctrl=bpy.data.objects['FLOW_CONTROL']
    H=hardware.evaluated_get(dep).matrix_world.copy();Hi=H.inverted()
    assert equal(H,flow.evaluated_get(dep).matrix_world)
    assert all(abs(v-1)<1e-6 for v in H.to_scale()) and abs(H.determinant()-1)<1e-6
    housing=bpy.data.objects['ECCO_HOUSING_SOURCE_MESH'];basis=housing.matrix_world.copy()
    source_scales=list(basis.to_scale());assert all(abs(v-.001)<1e-9 for v in source_scales)
    source_hash=hashlib.sha256(b''.join(struct.pack('3f',*v.co) for v in housing.data.vertices)).hexdigest()
    assert source_hash=='8fdbba227e8c46a9520e1cc8fb4cd270d6486ed0a58781efea5f7ee2116ebc9b'
    imported=[basis@v.co for v in housing.data.vertices]
    length=max(v.x for v in imported)-min(v.x for v in imported);assert abs(length-2.4)<1e-6
    libs=[dict(path=l.filepath,resolved=str(Path(bpy.path.abspath(l.filepath)).resolve()),parent=l.parent.name if l.parent else None,sha256=digest(Path(bpy.path.abspath(l.filepath)))) for l in bpy.data.libraries]
    assert all(l['path'].startswith('//') for l in libs)
    assert len([l for l in libs if Path(l['resolved']).name=='BHA_film_v007.blend' and l['parent'] is None])==1
    assert len([l for l in libs if Path(l['resolved']).name=='BHA_film_v006.blend' and l['parent'] is not None])==1
    roots={r:bpy.data.objects[n] for r,n in [('base','WORLD_HARDWARE_INSTANCE'),('extension','WORLD_UPHOLE_EXTENSION_INSTANCE'),('joint','WORLD_UPHOLE_JOINT_INSTANCE')]}
    assert roots['extension'].parent==roots['joint'].parent==hardware
    ids={r:collect(o.instance_collection) for r,o in roots.items()}
    paths=[o for o in s.objects if o.name.startswith('FLOW_FLOW_PATH_')]
    cuts=[o for o in s.objects if o.name.startswith('FLOW_CUTTING_')]
    tracers=[o for o in s.objects if o.name.startswith('FLOW_TRACER_') and o.type=='MESH'];moving=cuts+tracers
    assert (len(paths),len(cuts),len(tracers))==(10,30,20)
    assert all(o.data.library and Path(bpy.path.abspath(o.data.library.filepath)).name=='Hydraulics_v003.blend' for o in paths+moving)
    nodes=[];chord_rmin=float('inf')
    for o in paths:
        pts=[Hi@o.matrix_world@Vector(p.co[:3]) for spl in o.data.splines for p in spl.points];nodes+=pts
        for a,b in zip(pts,pts[1:]): chord_rmin=min(chord_rmin,minimum_radius([a,b]))
        assert min(v.x for v in pts)<.5 and max(v.x for v in pts)>1.56
    bevel=max(o.data.bevel_depth for o in paths)
    shape_r=max([bevel]+[math.hypot(v.co.y,v.co.z) for o in moving for v in o.data.vertices])
    axial=max([bevel]+[abs(v.co.x) for o in moving for v in o.data.vertices])
    lo=min(v.x for v in nodes)-axial-EPS;hi=max(v.x for v in nodes)+axial+EPS
    rlo=chord_rmin-shape_r-EPS;rhi=max(math.hypot(v.y,v.z) for v in nodes)+shape_r+EPS
    witness=[Vector((lo-1,.12,0)),Vector((hi+1,.12,0)),Vector((hi+1,.12,.01))]
    assert len(slab(witness,lo,hi))>=3
    hwmax=0;wallmin=float('inf');records=[];counts={r:0 for r in roots};n_housing=0;crossing=0
    for inst in dep.object_instances:
        o=inst.object;orig=o.original
        if orig==housing: n_housing+=1;assert equal(inst.matrix_world,H@basis)
        roles=[r for r,vals in ids.items() if orig.as_pointer() in vals]
        wall=orig.name in ('NOMINAL_CUTAWAY','FORMATION_NOMINAL_CUTAWAY')
        if o.type!='MESH' or not (roles or wall):continue
        if o.hide_render and roles:continue
        m=o.to_mesh();m.calc_loop_triangles();T=Hi@inst.matrix_world;vs=[T@v.co for v in m.vertices];tris=[list(t.vertices) for t in m.loop_triangles];o.to_mesh_clear()
        for role in roles:counts[role]+=1
        selected=0;bound=0;wbound=float('inf');n_cross=0
        for tri in tris:
            pts=[vs[i] for i in tri]
            if max(v.x for v in pts)<lo or min(v.x for v in pts)>hi:continue
            poly=slab(pts,lo,hi)
            if not poly:continue
            selected+=1
            if all(v.x<lo or v.x>hi for v in pts):n_cross+=1
            if roles:bound=max(bound,max(math.hypot(v.y,v.z) for v in poly))
            if wall:wbound=min(wbound,minimum_radius(poly))
        if roles:hwmax=max(hwmax,bound);crossing+=n_cross
        if wall:wallmin=min(wallmin,wbound)
        records.append(dict(name=orig.name,roles=roles,wall=wall,triangles=len(tris),selected=selected,crossing_faces=n_cross,radial_max=bound,radial_min=wbound if math.isfinite(wbound) else None))
    assert n_housing==1 and counts=={'base':135,'extension':1,'joint':1},(n_housing,counts)
    clearance_hw=rlo-hwmax-EPS;clearance_wall=wallmin-EPS-rhi
    assert clearance_hw>0 and clearance_wall>0,(clearance_hw,clearance_wall)
    initial=dict(ctrl.items());ctrl['density']=10;ctrl['stage_emphasis']=0;ctrl.update_tag()
    vertices=0;positions=[]
    for f in range(1,s.frame_end+1):
        s.frame_set(f);dep=bpy.context.evaluated_depsgraph_get();assert equal(hardware.evaluated_get(dep).matrix_world,H) and equal(flow.evaluated_get(dep).matrix_world,H)
        housings=[i.matrix_world.copy() for i in dep.object_instances if i.object.original==housing];assert len(housings)==1 and equal(housings[0],H@basis)
        for o in moving:
            q=o.evaluated_get(dep);T=Hi@q.matrix_world;R=T.to_3x3()
            assert all(abs(R[i][j])<1e-6 for i in range(3) for j in range(3) if i!=j)
            assert all(.8499<=R[i][i]<=1.0001 for i in range(3))
            m=q.to_mesh()
            for v in m.vertices:
                w=T@v.co;rr=math.hypot(w.y,w.z);vertices+=1
                assert lo<=w.x<=hi and rlo<=rr<=rhi,(f,o.name,list(w),lo,hi,rlo,rhi)
            q.to_mesh_clear()
        positions.append(list(Hi@cuts[0].evaluated_get(dep).matrix_world.translation))
    # Each continuous path remains visible across the three neutral windows during emphasis.
    for emphasis in [0,1,2,3]:
        ctrl['stage_emphasis']=emphasis;ctrl.update_tag();s.frame_set(21+emphasis);dep=bpy.context.evaluated_depsgraph_get()
        assert all(not o.evaluated_get(dep).hide_render for o in paths+moving)
    ctrl['density']=0;ctrl.update_tag();s.frame_set(29);dep=bpy.context.evaluated_depsgraph_get();assert all(o.evaluated_get(dep).hide_render for o in cuts) and all(not o.evaluated_get(dep).hide_render for o in paths+tracers)
    ctrl['density']=10;ctrl['cuttings_visible']=0;ctrl.update_tag();s.frame_set(30);dep=bpy.context.evaluated_depsgraph_get();assert all(o.evaluated_get(dep).hide_render for o in cuts) and all(not o.evaluated_get(dep).hide_render for o in paths+tracers)
    ctrl['cuttings_visible']=1;ctrl['flow_visible']=0;ctrl.update_tag();s.frame_set(31);dep=bpy.context.evaluated_depsgraph_get();assert all(o.evaluated_get(dep).hide_render for o in paths+tracers) and all(not o.evaluated_get(dep).hide_render for o in cuts)
    ctrl['flow_visible']=1;ctrl['speed']=0;ctrl.update_tag();s.frame_set(32);a=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();s.frame_set(39);b=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();assert (a-b).length<1e-6
    ctrl['phase']+=.13;ctrl.update_tag();s.frame_set(40);c=cuts[0].evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world.translation.copy();assert (b-c).length>.05
    ctrl['operating_mode']=1;ctrl.update_tag();s.frame_set(41);dep=bpy.context.evaluated_depsgraph_get();assert all(o.evaluated_get(dep).hide_render for o in paths+moving)
    assert all(m.node_tree and len(m.node_tree.nodes)>0 for m in bpy.data.materials if m.library)
    return dict(kind=kind,path=p.relative_to(ROOT).as_posix(),sha256=digest(p),predecessor_sha256=digest(old),unchanged_camera_timing_keys_old_controls=True,initial_controls=initial,source_scales=source_scales,source_mesh_hash=source_hash,source_length_m=length,libraries=libs,hardware_counts=counts,one_housing=n_housing,slab=[lo,hi],finite_radial_interval=[rlo,rhi],hardware_max=hwmax,wall_minimum_all_clipped_triangles=wallmin,hardware_clearance_m=clearance_hw,wall_clearance_m=clearance_wall,crossing_face_regression_pass=True,actual_crossing_faces=crossing,all_frame_count=s.frame_end,all_frame_finite_vertices=vertices,control_probes='density/independent_visibility/speed_zero/phase/mode_off/emphasis_all_regions_pass',first_particle_positions=positions[::12],hardware_wall_records=records)

try:
    rows=[check(k) for k in ['A','B']]
    report=dict(candidate_commit=SHA,pass_checks=True,method='Independent triangle clipping and exact 2D segment/polygon radial extrema; no builder verification function imported; no renders or native writes',consumers=rows)
    (OUT/'native-check_v001.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print('INDEPENDENT_FLOW_NATIVE_PASS')
except Exception:
    (OUT/'native-failure_v001.txt').write_text(traceback.format_exc(),encoding='utf-8')
    raise
