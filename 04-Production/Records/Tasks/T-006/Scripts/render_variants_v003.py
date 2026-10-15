"""Save and render a preview consumer for each live-control configuration."""
import bpy,json,math,time,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];TASK=ROOT/'Records/Tasks/T-006'
master=ROOT/'Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend'
cases=[('nominal',0,.5,1.1,96),('irregular',1,.5,1.1,96),('spiral',2,.5,1.1,96),
       ('cased',0,-3.2,-2.6,96),('interval-transition',0,-3.2,.6,144)]
evidence=[]
for name,variant,start,end,count in cases:
    bpy.ops.wm.open_mainfile(filepath=str(master));s=bpy.context.scene;r=bpy.data.objects['ASSEMBLY_CONTROL']
    r['variant']=variant;r['cutaway']=1
    s.frame_end=count
    for frame,t,angle in [(1,start,0),(count,end,2*math.pi)]:
        r['travel_m']=t;r.keyframe_insert(data_path='["travel_m"]',frame=frame)
        r['rotation_rad']=angle;r.keyframe_insert(data_path='["rotation_rad"]',frame=frame)
    for fc in r.animation_data.action.layers[0].strips[0].channelbag(r.animation_data.action_slot).fcurves:
        for point in fc.keyframe_points:point.interpolation='LINEAR'
    r.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    frames=TASK/f'Previews/v003/{name}/Frames';frames.mkdir(parents=True,exist_ok=True)
    scene_path=TASK/f'Previews/v003/{name}/B102_{name}_preview_v003.blend'
    # Relativize again because the consumer lives in a different directory.
    for lib in bpy.data.libraries:lib.filepath=bpy.path.relpath(bpy.path.abspath(lib.filepath),start=str(scene_path.parent))
    s.render.filepath='//Frames/frame_';s['preview_case']=name
    s['preview_limit']='Provisional illustration. Orange BHA/adapters/bit placeholders; test speed is not drilling rate. O05 open.'
    bpy.ops.wm.save_as_mainfile(filepath=str(scene_path),relative_remap=False)
    # Prove the saved candidate resolves its source before rendering it.
    bpy.ops.wm.open_mainfile(filepath=str(scene_path));s=bpy.context.scene;r=bpy.data.objects['ASSEMBLY_CONTROL']
    r.update_tag();s.frame_set(1);bpy.context.view_layer.update()
    assert len(bpy.data.collections['ECCO_MASTER_v002'].all_objects)>10
    assert all(Path(bpy.path.abspath(lib.filepath)).is_file() for lib in bpy.data.libraries)
    visible=[name for name in ('NOMINAL_CUTAWAY','IRREGULAR_CUTAWAY','SPIRAL_CUTAWAY') if not bpy.data.objects[name].hide_render]
    assert visible==[('NOMINAL','IRREGULAR','SPIRAL')[variant]+'_CUTAWAY'],visible
    t=time.perf_counter();bpy.ops.render.render(animation=True)
    evidence.append({'name':name,'variant':variant,'travel_m':[start,end],'rotation_rad':[0,2*math.pi],
        'frames':count,'fps':24,'seconds':count/24,'resolution':[1280,720],
        'render_seconds':time.perf_counter()-t,'scene':str(scene_path.relative_to(ROOT.parent)).replace('\\','/'),
        'scene_sha256':hashlib.sha256(scene_path.read_bytes()).hexdigest()})
    (TASK/'Evidence/preview-renders_v003.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
print('RENDER_V003_PASS')
