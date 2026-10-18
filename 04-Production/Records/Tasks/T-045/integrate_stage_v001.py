"""Master-owned saved integration proof; no movie shot or source mutation.

Build/verify modes do not render. Render requires the master's single queue slot.
"""
import bpy
import hashlib
import json
import sys
import time
from pathlib import Path
from mathutils import Vector

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
ASSETS=ROOT/'04-Production/Shared/Assets'
E=HERE/'Evidence'
S=HERE/'Scenes'
P=HERE/'Previews'
for folder in [E,S,P]:
    folder.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ASSETS/'Acoustics/Scripts'))
from acoustic_event_v002 import sample_native_event,validate_event,validate_native_event,native_instance
from acoustic_binding_v001 import bind_event
from acoustic_verify_v002 import verify_packet
from bpy_extras.object_utils import world_to_camera_view
from mathutils.bvhtree import BVHTree

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rel(p):
    return p.relative_to(ROOT).as_posix()

def dump(name,data):
    (E/name).write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

def open_file(path):
    bpy.ops.wm.open_mainfile(filepath=str(path),load_ui=False,use_scripts=False)

def snapshot():
    s=bpy.context.scene
    return {'camera_matrix':[list(r) for r in s.camera.matrix_world],
            'lens':s.camera.data.lens,'frames':[s.frame_start,s.frame_end,s.render.fps]}

def resolved_library(lib):
    """Hash Blender's actual normalized exposed path, never basename lookup.

    5.2 inspection shows even nested Library.filepath is consumer-relative.
    Applying lib.parent again duplicates traversal; preserve parent as provenance.
    See T046/Evidence/nested-path-inspection_resume_v001.json.
    """
    path=Path(bpy.path.abspath(lib.filepath)).resolve(strict=True)
    assert path.is_file(),(lib.filepath,str(path))
    return path

def candidate_config():
    config=json.loads((HERE/'integration-candidates_v001.json').read_text(encoding='utf-8-sig'))
    assert config['upstream_commit']=='a08d0ecfbd6f3241298f506b3ea42613388b3baf'
    assert config['ready'],'Final successor paths are not released yet'
    for kind in ['flow','cased']:assert sha(ROOT/config[kind+'_consumer'])==config[kind+'_sha256'],kind
    return config

def extension_coverage():
    """All-frame finite native rim visibility, static registered hardware proof."""
    s=bpy.context.scene;s.frame_set(1);bpy.context.view_layer.update()
    ext,pose=native_instance('UPHOLE_UNIT_COLLAR_EXTENSION')
    points=[pose@v.co for v in ext.data.vertices if abs(v.co.x+1)<1e-6]
    points.extend(pose@p.center for p in ext.data.polygons if all(abs(ext.data.vertices[i].co.x+1)<1e-6 for i in p.vertices))
    trees=None;rows=[]
    for frame in range(s.frame_start,s.frame_end+1):
        s.frame_set(frame);bpy.context.view_layer.update();_,current=native_instance(ext.name)
        assert max(abs(current[r][c]-pose[r][c]) for r in range(4) for c in range(4))<1e-6,'Coverage helper requires static hardware'
        origin=s.camera.matrix_world.translation
        projected=[]
        for point in points:
            uv=world_to_camera_view(s,s.camera,point)
            if 0<=uv.x<=1 and 0<=uv.y<=1 and uv.z>s.camera.data.clip_start:projected.append(point)
        if projected and trees is None:
            trees=[]
            for inst in bpy.context.evaluated_depsgraph_get().object_instances:
                ob=inst.object.original;matrix=inst.matrix_world
                if ob.type!='MESH' or ob.hide_render or ob.name.startswith('MUD_') or ob.get('shared_package')=='Acoustics':continue
                trees.append(BVHTree.FromPolygons([matrix@v.co for v in ob.data.vertices],[list(p.vertices) for p in ob.data.polygons]))
        exposed=0
        for point in projected:
            delta=point-origin
            if not any(tree.ray_cast(origin,delta.normalized(),delta.length-.0001)[0] is not None for tree in trees):exposed+=1
        rows.append({'frame':frame,'projected_rim_samples':len(projected),'unoccluded_rim_samples':exposed})
    return {'rim_samples':len(points),'frames':rows,'all_pass':all(r['unoccluded_rim_samples']==0 for r in rows),'method':'Full native far-rim vertices and planar end face centres; actual opaque-mesh ray occlusion when projected'}

def native_record(path):
    open_file(path)
    s=bpy.context.scene
    rows=[]
    for lib in bpy.data.libraries:
        actual=resolved_library(lib)
        rows.append({'path':lib.filepath,'parent':lib.parent.filepath if lib.parent else None,'resolved':rel(actual),'sha256':sha(actual),
                     'relative':lib.filepath.startswith('//')})
    assert all(row['relative'] for row in rows)
    s.frame_set(1)
    deps=bpy.context.evaluated_depsgraph_get()
    count=sum(i.object.original.name=='ECCO_HOUSING_SOURCE_MESH' for i in deps.object_instances)
    assert count==1,count
    sensors={name:sum(i.object.original.name==name for i in deps.object_instances) for name in ['ECCO_SENSOR_REF_01','ECCO_SENSOR_REF_02','ECCO_SENSOR_REF_03']}
    assert all(n==1 for n in sensors.values()),sensors
    hardware=[o for o in s.objects if o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.name=='WORLD_HARDWARE']
    assert len(hardware)==1,len(hardware)
    continuation={}
    for name in ['WORLD_UPHOLE_EXTENSION','WORLD_UPHOLE_JOINT']:
        obs=[o for o in s.objects if o.instance_type=='COLLECTION' and o.instance_collection and o.instance_collection.name==name]
        assert len(obs)==1,(name,len(obs))
        assert obs[0].parent==hardware[0],name
        continuation[name]={'instance':obs[0].name,'parent':obs[0].parent.name}
    ctrl=bpy.data.objects.get('UPHOLE_CONTINUATION_CONTROL')
    assert ctrl and ctrl.parent==hardware[0]
    assert any(r['resolved'].endswith('BHA/BHA_film_v007.blend') and r['sha256']=='b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1' for r in rows)
    assert s.unit_settings.scale_length==1
    invalid=[]
    for frame in [1,18,36,s.frame_end]:
        s.frame_set(frame)
        for ob in s.objects:
            if ob.animation_data:
                invalid.extend((ob.name,fc.data_path) for fc in ob.animation_data.drivers if not fc.driver.is_valid)
    assert not invalid,invalid
    return {'scene':rel(path),'sha256':sha(path),'libraries':rows,'product_instances':count,
            'sensor_instances':sensors,'continuation':continuation,'continuation_control':{'length_m':ctrl['length_m'],'show':ctrl['show']},
            'unit_scale':s.unit_settings.scale_length,'snapshot':snapshot(),'invalid_drivers':invalid}

def build():
    config=candidate_config()
    source=ROOT/config['flow_consumer']
    open_file(source)
    s=bpy.context.scene
    s.frame_set(1)
    before=snapshot()
    event=sample_native_event('ECCO_SENSOR_REF_01','NOMINAL_CUTAWAY',
                             't45-open-flow-sensing-01',.25,.65,1.05)
    validate_event(event)
    validate_native_event(event)
    bind_event(event,frames=s.frame_end,fps=s.render.fps,library_version=config['acoustics_version'])
    s['purpose']='T45 compatibility/reuse proof only: linked sensing + flow + single accepted T44 world'
    s['limits']='Illustrative timing/circulation, no source rescale or calibrated physics. Not an actual V3 film shot.'
    s.frame_set(1)
    assert before==snapshot()
    path=S/'OpenFlowSensing_v001.blend'
    assert not path.exists(),path
    for lib in bpy.data.libraries:
        if lib.parent:
            continue
        actual=resolved_library(lib)
        lib.filepath=bpy.path.relpath(str(actual),start=str(path.parent))
    bpy.ops.wm.save_as_mainfile(filepath=str(path),relative_remap=False)
    dump('integration-open-event_v001.json',{'contract':'ecco-acoustic-event-v001','events':[event]})
    dump('integration-open-preservation_v001.json',{'source':rel(source),'source_sha256':sha(source),
         'before':before,'after':snapshot(),'camera_timing_preserved':before==snapshot()})
    verify()

def verify():
    config=candidate_config()
    paths=[S/'OpenFlowSensing_v001.blend',ROOT/config['cased_consumer']]
    rows=[native_record(p) for p in paths]
    open_file(paths[0])
    coverage=extension_coverage();dump('combined-extension-coverage_v001.json',coverage);assert coverage['all_pass']
    events=json.loads((E/'integration-open-event_v001.json').read_text(encoding='utf-8'))['events']
    packets=[verify_packet(event,frames=range(bpy.context.scene.frame_start,bpy.context.scene.frame_end+1),fps=bpy.context.scene.render.fps) for event in events]
    dump('combined-packets_v001.json',{'results':packets,'all_pass':all(p['all_pass'] for p in packets)})
    assert all(p['all_pass'] for p in packets)
    dump('combined-native_v001.json',{'results':rows,'all_pass':True,
         'scope':'Master fresh-open checks, source links, single product, scale and driver validity; separate fresh-context review follows'})

def render():
    path=S/'OpenFlowSensing_v001.blend'
    open_file(path)
    s=bpy.context.scene
    rows=[]
    for frame in [1,12,17,24,36,72]:
        s.frame_set(frame)
        s.render.filepath=str(P/('OpenFlowSensing_f%03d_v001.png'%frame))
        start=time.perf_counter()
        bpy.ops.render.render(write_still=True)
        dt=time.perf_counter()-start
        rows.append({'frame':frame,'seconds':dt,'under_5':dt<5,'path':rel(Path(s.render.filepath))})
        dump('combined-benchmark_v001.json',{'scene':rel(path),'native_sha256':sha(path),'samples':rows,
             'resolution':[s.render.resolution_x,s.render.resolution_y],'samples_eevee':s.eevee.taa_render_samples,
             'compositor':s.render.use_compositing,'color':[s.view_settings.view_transform,s.view_settings.look],
             'cache':'Normal existing driver cache; full first-process render included; empty-cache T44 limitation unresolved'})
        assert dt<5,dt

mode=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'verify'
if mode=='build':
    build()
elif mode=='verify':
    verify()
elif mode=='render':
    render()
else:
    raise ValueError(mode)
print('T45_INTEGRATION_'+mode.upper()+'_COMPLETE')
