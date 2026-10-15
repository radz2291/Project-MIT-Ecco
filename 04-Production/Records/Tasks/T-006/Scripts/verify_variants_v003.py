"""Fresh-open source/interface/topology/clearance self-checks; no saved edits."""
import bpy,json,math,hashlib,bmesh
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006';ASSET=ROOT/'Shared/Assets/WellAssembly'
s=bpy.context.scene;rig=bpy.data.objects['ASSEMBLY_CONTROL']
c=json.loads((ASSET/'config_authorized_v003.json').read_text());source=(ASSET/c['product_library']).resolve()
build=json.loads((TASK/'Evidence/variants-build_v003.json').read_text())
checks={'fresh_open_candidate_hash':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==build['sha256'],
        'source_unchanged':hashlib.sha256(source.read_bytes()).hexdigest()==c['product_sha256'],
        'relative_library_resolves':all(l.filepath.startswith('//') and Path(bpy.path.abspath(l.filepath)).is_file() for l in bpy.data.libraries),
        'O05_explicitly_open':'Open' in bpy.data.collections['WELL_ASSEMBLY_v003']['O05']}
def update():rig.update_tag();s.frame_set(s.frame_current+1);bpy.context.view_layer.update()
def visible(names):return {n:not bpy.data.objects[n].hide_render for n in names}
names=[v+suffix for v in ('NOMINAL','IRREGULAR','SPIRAL') for suffix in ('_CUTAWAY','_FULL')]
vis=[]
for v in range(3):
    for cut in (0,1):
        rig['variant']=v;rig['cutaway']=cut;update();state=visible(names)
        expected=('NOMINAL','IRREGULAR','SPIRAL')[v]+('_CUTAWAY' if cut else '_FULL')
        vis.append({'variant':v,'cutaway':cut,'visible':[n for n,x in state.items() if x]})
        assert state[expected] and sum(state.values())==1,state
checks['variant_cutaway_selection']=True
for prop,targets in [('show_open',names),('show_casing',['CASING_CUTAWAY','CASING_FULL']),
                     ('show_cement',['CEMENT_CUTAWAY','CEMENT_FULL']),('show_hardware',['ECCO_LINK_v002']),
                     ('show_proxies',[o.name for o in bpy.data.collections['PROVISIONAL_BHA_PROXIES'].objects])]:
    rig[prop]=0;update();assert not any(visible(targets).values()),prop
    rig[prop]=1;update()
checks['visibility_toggles']=True
profile=[];slices={}
for variant,prop in [(1,'irregular_strength'),(2,'spiral_strength')]:
    rig['variant']=variant;rig['cutaway']=0;update()
    o=bpy.data.objects[('IRREGULAR','SPIRAL')[variant-1]+'_FULL']
    for strength in (0.,1.):
        rig[prop]=strength;update()
        evaluated=o.evaluated_get(bpy.context.evaluated_depsgraph_get());mesh=evaluated.to_mesh()
        radii=[math.hypot(v.co.y,v.co.z) for v in mesh.vertices]
        if strength==1:
            plane=min((v.co.x for v in mesh.vertices),key=lambda x:abs(x-2.8))
            points=[list(v.co) for v in mesh.vertices if abs(v.co.x-plane)<1e-6]
            slices[str(variant)]={'plane_x_m':plane,'points_m':points}
        evaluated.to_mesh_clear()
        profile.append({'variant':variant,'strength':strength,'min_radius_m':min(radii),'max_radius_m':max(radii)})
        assert min(radii)>=.31115/2-1e-6
        if strength==0:assert max(radii)-min(radii)<1e-6
    rig[prop]=1.
checks['profile_controls_outward_only']=True
topology={}
for o in list(bpy.data.collections['UPPER_CASED_INTERVAL'].objects)+list(bpy.data.collections['PROVISIONAL_BHA_PROXIES'].objects):
    bm=bmesh.new();bm.from_mesh(o.data);bad=sum(not e.is_manifold for e in bm.edges);bm.free()
    topology[o.name]={'nonmanifold_edges':bad};assert bad==0,o.name
checks['casing_cement_proxy_shells_manifold']=True
rig['show_proxies']=0;rig['variant']=0;rig['cutaway']=1
motion=[]
for travel,angle in [(-3.2,0),(-.8,math.pi/2),(.6,math.pi),(1.1,2*math.pi)]:
    rig['travel_m']=travel;rig['rotation_rad']=angle;update()
    inst=[{'name':i.object.original.name,'object':i.object.original,'matrix':i.matrix_world.copy()}
          for i in bpy.context.evaluated_depsgraph_get().object_instances
          if i.is_instance and i.object.type=='MESH' and
          (i.object.name=='ECCO_HOUSING_SOURCE_MESH' or any(col.name=='ECCO_TEMPORARY_CLOSURES' for col in i.object.original.users_collection))]
    assert len(inst)==10,len(inst)
    radius=0;min_gap=10;bounds=[100,-100];error=0
    for item in inst:
        expected=bpy.data.objects['ASSEMBLY_ROTATION_X'].matrix_world@item['object'].matrix_world
        error=max(error,max(abs(item['matrix'][r][k]-expected[r][k]) for r in range(4) for k in range(4)))
        for v in item['object'].data.vertices:
            q=item['matrix']@v.co;r=math.hypot(q.y,q.z);radius=max(radius,r)
            bounds[0]=min(bounds[0],q.x);bounds[1]=max(bounds[1],q.x)
            # Conservative minimum across both interval wall bounds; drift is a
            # separate reference only, not modeled as an actual casing bore.
            wall=(.317881/2 if q.x<0 else .31115/2);min_gap=min(min_gap,wall-r)
    assert error<1e-6 and min_gap>0
    motion.append({'travel_m':travel,'angle_rad':angle,'housing_and_closure_instances':len(inst),
                   'max_radius_m':radius,'bounds_x_m':bounds,'min_wall_gap_m':min_gap,'matrix_error':error})
checks['linked_product_motion_clearance']=True
# Generic bit gauge is nominal hole gauge (intentional wall contact, not clearance).
checks['proxy_gauge_not_larger_than_nominal_hole']=max(math.hypot(v.co.y,v.co.z) for v in bpy.data.objects['BIT_GAUGE_PROXY_NOT_CUTTERS'].data.vertices)<=.31115/2+1e-6
checks['proxies_labeled_provisional']=all('PROVISIONAL' in o['status'] for o in bpy.data.collections['PROVISIONAL_BHA_PROXIES'].objects)
driver_errors=[{'object':o.name,'path':f.data_path} for o in s.objects if o.animation_data for f in o.animation_data.drivers if not f.driver.is_valid]
checks['object_drivers_valid']=not driver_errors
result={'all_pass':all(checks.values()),'checks':checks,'visibility_cases':vis,'profile_cases':profile,
        'topology':topology,'motion_cases':motion,'invalid_drivers':driver_errors,
        'limits':'Provisional straight concentric illustration. No actual MIT deployment, thread/load/shoe/dogleg/bit cutting validation; O05 remains open.'}
(TASK/'Evidence/variants-verification_v003.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
(TASK/'Evidence/profile-slices_v003.json').write_text(json.dumps(slices,indent=2),encoding='utf-8')
assert result['all_pass'],result
print('VERIFY_V003_PASS',json.dumps(checks))
