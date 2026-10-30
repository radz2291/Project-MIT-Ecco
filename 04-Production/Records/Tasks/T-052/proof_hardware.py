"""Queue-only hardware geometry checks and native-speed S07 short motion."""
import bpy,json,time,sys
from pathlib import Path
from mathutils import Vector
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent
mode=sys.argv[-1] if '--' in sys.argv else 'bench'
records=json.loads((T/'Evidence/hardware-bench.json').read_text()) if mode=='bench' and (T/'Evidence/hardware-bench.json').exists() else []
def render(label,frame,engine):
    s=bpy.context.scene;s.frame_set(frame);s.render.engine=engine
    s.render.resolution_x=640;s.render.resolution_y=360;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG'
    if engine=='BLENDER_EEVEE':s.eevee.taa_render_samples=32
    out=T/('Frames' if mode=='motion' and label.startswith('S07_motion_') else 'Previews')/(label+'.png');out.parent.mkdir(exist_ok=True)
    s.render.filepath=str(out);start=time.perf_counter();bpy.ops.render.render(write_still=True);dt=time.perf_counter()-start
    records.append({'label':label,'frame':frame,'engine':engine,'seconds':dt,'passes':dt<5,'output':str(out),'resolution':[640,360]})
    (T/'Evidence'/('hardware-'+mode+'.json')).write_text(json.dumps(records,indent=2));print('BENCH',records[-1],flush=True)
    if dt>=5:raise RuntimeError('Budget failed; stop further rendering')
def bha_scene():
    bpy.ops.wm.open_mainfile(filepath=str(R/'04-Production/Shared/Assets/BHA/BHA_film_v008.blend'))
    s=bpy.context.scene;c=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL'];c['show']=0;c.update_tag();s.frame_set(1)
    # Frame connected core from evaluated instance geometry, excluding hidden continuation.
    pts=[]
    for inst in bpy.context.evaluated_depsgraph_get().object_instances:
        o=inst.object
        if o.type!='MESH' or o.hide_render or any(x in o.name for x in ['CUTTER','UPHOLE_UNIT','UPHOLE_SIMPLIFIED']):continue
        pts.extend(inst.matrix_world@Vector(v) for v in o.bound_box)
    lo=Vector(tuple(min(v[k] for v in pts) for k in range(3)));hi=Vector(tuple(max(v[k] for v in pts) for k in range(3)));center=(lo+hi)*.5
    cd=bpy.data.cameras.new('T052 inspection camera');cam=bpy.data.objects.new('T052 inspection camera',cd);s.collection.objects.link(cam);s.camera=cam
    cam.location=center+Vector((9,-14,5));cam.rotation_euler=(center-cam.location).to_track_quat('-Z','Y').to_euler();cd.type='ORTHO';cd.ortho_scale=max(hi-lo)*1.15;cd.clip_end=200
    if not s.world:s.world=bpy.data.worlds.new('T052 inspection background')
    s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_shadows=True;s.display.shading.show_cavity=True;s.display.shading.background_type='WORLD';s.world.color=(.035,.035,.035)
    bpy.ops.wm.save_as_mainfile(filepath=str(T/'Consumers/BHA_connected-controls_v001.blend'));bpy.ops.file.make_paths_relative();bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    return c
if mode=='bench':
    if not records:
        bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S02_shared-satin_v001.blend'));render('S02_simple-string_f360_workbench',360,'BLENDER_WORKBENCH')
    c=bha_scene();render('BHA_connected_core_show0',1,'BLENDER_WORKBENCH');c['show']=1;c['length_m']=2;c.update_tag();bpy.context.scene.frame_set(2);render('BHA_connected_extension_2m',2,'BLENDER_WORKBENCH')
    bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S07_shared-satin_v001.blend'));render('S07_motion_benchmark_f072',72,'BLENDER_EEVEE');render('S07_motion_benchmark_f095',95,'BLENDER_EEVEE')
elif mode=='motion':
    bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S02_shared-satin_v001.blend'));render('S02_simple-string_f528_workbench',528,'BLENDER_WORKBENCH')
    bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/BHA_connected-controls_v001.blend'));s=bpy.context.scene;c=bpy.data.objects['UPHOLE_CONTINUATION_CONTROL'];c['show']=1;c['length_m']=2;c.update_tag();s.camera.data.ortho_scale*=1.65;s.frame_set(2)
    render('BHA_connected_extension_2m_wide',2,'BLENDER_WORKBENCH')
    bpy.ops.wm.open_mainfile(filepath=str(T/'Consumers/S07_shared-satin_v001.blend'))
    for f in range(72,96):render(f'S07_motion_{f:03d}',f,'BLENDER_EEVEE')
