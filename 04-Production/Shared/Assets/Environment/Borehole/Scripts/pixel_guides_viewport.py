"""Screen-pixel strokes from evaluated shared guide edges. Run install() after opening.

Native Viewport Render omits Python draw callbacks; export() explicitly draws the
same strokes over a GPUOffScreen scene with its original depth buffer.
"""
import bpy
import gpu
import numpy as np
from gpu_extras.batch import batch_for_shader

KEY = 'ecco_world_pixel_guides'
PREFIX = 'World pixel_'
_cache = {}

def batches():
    dg = bpy.context.evaluated_depsgraph_get()
    ctrl = bpy.data.objects.get('World pixel guide controls')
    entry = bpy.data.objects.get('ENTRY presentation controls')
    signature = (bpy.context.scene.frame_current, repr(dict(ctrl.items())) if ctrl else '',
                 repr(dict(entry.items())) if entry else '')
    if _cache.get('signature') == signature:
        return _cache['prepared']
    shader = gpu.shader.from_builtin('POLYLINE_UNIFORM_COLOR')
    out = []
    camera = bpy.context.scene.camera
    eye = camera.evaluated_get(dg).matrix_world.translation if camera else bpy.context.region_data.view_matrix.inverted().translation
    for ob in bpy.context.scene.objects:
        if not ob.name.startswith((PREFIX, 'WORLD_PIXEL_')):
            continue
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        if me.edges:
            out.append(batch_for_shader(shader, 'LINES',
                # Move only along the viewing ray: identical screen position,
                # small depth bias avoids distant surface z fighting.
                {'pos': [(ob.matrix_world @ v.co).lerp(eye, .0005) for v in me.vertices]},
                indices=[tuple(e.vertices) for e in me.edges]))
        ev.to_mesh_clear()
    _cache.update(signature=signature, prepared=(shader, out))
    return shader, out

def draw(size, prepared=None):
    ctrl = bpy.data.objects.get('World pixel guide controls')
    if not ctrl or not ctrl.get('Enabled', False):
        return
    shader, items = prepared or batches()
    gpu.state.depth_test_set('LESS_EQUAL')
    gpu.state.depth_mask_set(False)
    gpu.state.blend_set('ALPHA')
    try:
        shader.bind()
        shader.uniform_float('viewportSize', size)
        shader.uniform_float('lineWidth', float(ctrl.get('Line width px', 1.2)))
        shade = float(ctrl.get('Stroke shade', .08))
        shader.uniform_float('color', (shade, shade, shade, float(ctrl.get('Line opacity', .75))))
        for batch in items:
            batch.draw(shader)
    finally:
        gpu.state.blend_set('NONE')
        gpu.state.depth_mask_set(True)
        gpu.state.depth_test_set('NONE')

def live_draw():
    draw(gpu.state.viewport_get()[2:])

def remove_before_load(_):
    previous = bpy.app.driver_namespace.pop(KEY, None)
    if previous:
        bpy.types.SpaceView3D.draw_handler_remove(previous, 'WINDOW')
    _cache.clear()

class ECCO_PT_world_pixel_guides(bpy.types.Panel):
    bl_label = 'World motion grid'
    bl_idname = 'ECCO_PT_world_pixel_guides'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'World Grid'

    def draw(self, context):
        c = bpy.data.objects.get('World pixel guide controls')
        layout = self.layout
        if c is None:
            layout.label(text='No World grid controls in this scene')
            return
        layout.prop(c, '["Enabled"]', text='Grid enabled')
        body = layout.column()
        body.enabled = bool(c.get('Enabled', False))
        for title, toggle, fields in [
            ('Cave', 'Show bore', [('Bore ring spacing m','Ring spacing (m)'),('Bore lengthwise spacing deg','Lengthwise spacing (deg)')]),
            ('Cut earth', 'Show cut faces', [('Depth spacing m','Horizontal spacing (m)'),('Radial spacing m','Vertical spacing (m)')]),
            ('Seabed', 'Show seabed', [('Seabed spacing m','Spacing (m)')])]:
            box=body.box()
            box.prop(c, '["'+toggle+'"]', text=title)
            fields_ui=box.column();fields_ui.enabled=bool(c.get(toggle,False))
            for prop,label in fields:
                if prop in c: fields_ui.prop(c, '["'+prop+'"]', text=label)
        body.label(text='Larger spacing = fewer lines')
        for prop,label in [('Line width px','Stroke width (px)'),('Line opacity','Opacity'),('Stroke shade','Shade')]:
            body.prop(c, '["'+prop+'"]', text=label)

def install():
    previous = bpy.app.driver_namespace.pop(KEY, None)
    if previous:
        bpy.types.SpaceView3D.draw_handler_remove(previous, 'WINDOW')
    ctrl = bpy.data.objects['World pixel guide controls']
    for name, value in [('Line width px', 1.2), ('Line opacity', .75)]:
        if name not in ctrl: ctrl[name] = value
    ctrl.id_properties_ui('Line width px').update(min=.5, max=5.)
    ctrl.id_properties_ui('Line opacity').update(min=0., max=1.)
    for prop in ['Depth spacing m','Radial spacing m','Seabed spacing m','Bore ring spacing m']:
        if prop in ctrl: ctrl.id_properties_ui(prop).update(min=1., max=200., description='Larger spacing gives fewer lines; whole metre steps')
    if 'Bore lengthwise spacing deg' in ctrl:
        ctrl.id_properties_ui('Bore lengthwise spacing deg').update(min=30.,max=180.,description='Use30,60,90,120 or180 degrees; larger spacing gives fewer lengthwise lines')
    previous_panel = getattr(bpy.types, 'ECCO_PT_world_pixel_guides', None)
    if previous_panel: bpy.utils.unregister_class(previous_panel)
    bpy.utils.register_class(ECCO_PT_world_pixel_guides)
    ctrl['meaning'] = 'World-anchored edge guides drawn with a fixed screen-pixel GPU stroke. Run pixel_guides_viewport.py install() after reopening; use export() for playblast.'
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            area.spaces.active.overlay.show_overlays = False
            area.tag_redraw()
    bpy.app.driver_namespace[KEY] = bpy.types.SpaceView3D.draw_handler_add(live_draw, (), 'WINDOW', 'POST_VIEW')
    for handler in list(bpy.app.handlers.load_pre):
        if getattr(handler, '__name__', '') == 'remove_before_load':
            bpy.app.handlers.load_pre.remove(handler)
    bpy.app.handlers.load_pre.append(remove_before_load)

def export(path, width=480, height=270):
    s = bpy.context.scene
    bpy.context.view_layer.update()
    area = next(a for a in bpy.context.screen.areas if a.type == 'VIEW_3D')
    region = next(r for r in area.regions if r.type == 'WINDOW')
    space = area.spaces.active
    old_overlay = space.overlay.show_overlays
    space.overlay.show_overlays = False
    dg = bpy.context.evaluated_depsgraph_get()
    cam = s.camera.evaluated_get(dg)
    view = cam.matrix_world.inverted()
    projection = cam.calc_matrix_camera(dg, x=width, y=height)
    prepared = batches()
    off = gpu.types.GPUOffScreen(width, height)
    try:
        with bpy.context.temp_override(window=bpy.context.window, area=area, region=region):
            off.draw_view3d(s, bpy.context.view_layer, space, region, view, projection, do_color_management=False)
        with off.bind():
            gpu.matrix.push()
            gpu.matrix.push_projection()
            try:
                gpu.matrix.load_matrix(view)
                gpu.matrix.load_projection_matrix(projection)
                draw((width, height), prepared)
                pixels = np.asarray(gpu.state.active_framebuffer_get().read_color(0, 0, width, height, 4, 0, 'FLOAT')).copy().reshape(-1)
            finally:
                gpu.matrix.pop_projection()
                gpu.matrix.pop()
        im = bpy.data.images.new('World pixel guide export', width, height, alpha=True, float_buffer=True)
        try:
            im.pixels.foreach_set(pixels)
            im.save_render(str(path), scene=s)
        finally:
            bpy.data.images.remove(im)
    finally:
        off.free()
        space.overlay.show_overlays = old_overlay
