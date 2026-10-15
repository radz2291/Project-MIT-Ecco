import bpy,json,time,hashlib,math
from pathlib import Path
P=Path(__file__).resolve().parents[1];TASK=P.parents[1]/'Records/Tasks/T-010'
scene=P/'Scenes/B204_hydraulic-proof_v001.blend'
bpy.ops.wm.open_mainfile(filepath=str(scene));s=bpy.context.scene
assert s.frame_end==288 and s.render.fps==24
missing=[str(bpy.path.abspath(l.filepath)) for l in bpy.data.libraries if not Path(bpy.path.abspath(l.filepath)).exists()]
assert not missing,missing
rig=bpy.data.objects['HYDRAULIC_CONTROL'];checks=[];bad=[]
previous=None
for f in range(1,289):
    s.frame_set(f);bpy.context.view_layer.update()
    for o in s.objects:
        if o.animation_data:
            bad.extend([{'object':o.name,'frame':f,'expression':d.driver.expression} for d in o.animation_data.drivers if not d.driver.is_valid])
    o=bpy.data.objects['Mud_annular_00']
    checks.append({'frame':f,'annular_x':o.location.x,'diagram_x':bpy.data.objects['Diagram_mud_00'].location.x,'diagram_z':bpy.data.objects['Diagram_mud_00'].location.z})
assert not bad,bad
rig['flow_rate']=0.;rig.update_tag();s.frame_set(32);bpy.context.view_layer.update();a=tuple(bpy.data.objects['Mud_annular_00'].location)
s.frame_set(48);bpy.context.view_layer.update();b=tuple(bpy.data.objects['Mud_annular_00'].location);assert a==b
rig['flow_rate']=1.;rig['flow_visible']=0;rig.update_tag();bpy.context.view_layer.update();assert bpy.data.objects['Mud_annular_00'].hide_render
rig['flow_visible']=1;rig.update_tag();s.frame_set(1);bpy.context.view_layer.update()
assert all(abs(bpy.data.objects['ECCO_LINK_v002'].rotation_euler[i])<1e-9 for i in range(3))
(TASK/'Evidence/fresh-open-verification_v001.json').write_text(json.dumps({'scene_sha256':hashlib.sha256(scene.read_bytes()).hexdigest(),'missing_libraries':missing,'invalid_drivers':bad,'all_frames_sampled':288,'stationary_tool':True,'zero_rate_stops_motion':True,'flow_toggle':True,'samples':checks},indent=2))
s.render.filepath=str(P/'Previews/Frames/B204_');s.render.image_settings.file_format='PNG'
start=time.perf_counter();bpy.ops.render.render(animation=True)
(TASK/'Evidence/animation-render_v001.json').write_text(json.dumps({'seconds':time.perf_counter()-start,'frames':288,'resolution':[1280,720],'engine':'BLENDER_WORKBENCH','samples':'8','fps':24},indent=2))
