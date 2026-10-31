import bpy,time,json
from pathlib import Path
D=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(D/'Hardware_demo_v001.blend'));s=bpy.context.scene
s.render.engine='BLENDER_WORKBENCH';s.render.resolution_x=640;s.render.resolution_y=360
s.display.shading.light='STUDIO';s.display.shading.color_type='MATERIAL';s.display.shading.show_cavity=True;s.display.shading.show_shadows=True;s.display.shading.background_type='WORLD'
s.world.color=(.025,.035,.045)
c=next(o for o in bpy.data.objects if o.name=='UPHOLE_CONTINUATION_CONTROL' and o.override_library)
if c.name not in s.collection.objects:s.collection.objects.link(c)
bpy.ops.object.select_all(action='DESELECT');c.select_set(True);bpy.context.view_layer.objects.active=c
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':area.spaces.active.shading.type='SOLID';area.spaces.active.shading.light='STUDIO';area.spaces.active.shading.color_type='MATERIAL'
        elif area.type=='PROPERTIES':area.spaces.active.context='OBJECT'
s.render.filepath=str(D/'Hardware_demo_workbench.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/'Hardware_demo_v001.blend'))
if not (D/'working-render-evidence.json').exists():
    t=time.perf_counter();bpy.ops.render.render(write_still=True);seconds=time.perf_counter()-t
    (D/'working-render-evidence.json').write_text(json.dumps({'seconds':seconds,'under_five':seconds<5,'engine':'BLENDER_WORKBENCH','resolution':[640,360],'scope':'Geometry/organization preview only; satin material remains linked but Workbench does not evaluate nodes.'},indent=2));print('SECONDS',seconds)
