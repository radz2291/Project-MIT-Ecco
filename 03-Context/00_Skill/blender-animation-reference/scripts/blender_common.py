"""Blender-specific read/evaluation helpers; no scene edits on import."""
import array
import hashlib
import math
import struct
from pathlib import Path
import bpy
from reference_common import digest


def select_scene(cfg):
    expected = Path(cfg['source_blend']).resolve()
    if not bpy.data.filepath or Path(bpy.data.filepath).resolve() != expected:
        raise ValueError('Loaded Blender file does not match configured source_blend')
    s = bpy.data.scenes.get(cfg.get('scene')) if cfg.get('scene') else bpy.context.scene
    if s is None:
        raise ValueError('Configured scene is missing')
    if bpy.context.window:
        bpy.context.window.scene = s
    return s


def set_time(s, f):
    integer = math.floor(f)
    s.frame_set(integer, subframe=f - integer)


def camera_at(s, f, cfg):
    if cfg.get('camera'):
        camera = s.objects.get(cfg['camera'])
    else:
        markers = sorted((m for m in s.timeline_markers if m.camera and m.frame <= f), key=lambda m: m.frame)
        camera = markers[-1].camera if markers else s.camera
    if camera is None or camera.type != 'CAMERA':
        raise ValueError(f'No valid camera at source frame {f}')
    return camera


def matrix(m):
    return [round(float(v), 8) for row in m for v in row]


def curves(action):
    if hasattr(action, 'layers') and len(action.layers):
        for layer in action.layers:
            for strip in layer.strips:
                for bag in getattr(strip, 'channelbags', []):
                    for fc in bag.fcurves:
                        yield fc, {'layer': layer.name, 'slot_handle': bag.slot_handle}
    else:
        for fc in getattr(action, 'fcurves', []):
            yield fc, {}


def rna_settings(owner):
    """Capture scalar/array settings without traversing arbitrary object graphs."""
    values = {}
    for prop in owner.bl_rna.properties:
        if prop.identifier == 'rna_type':
            continue
        try:
            value = getattr(owner, prop.identifier)
            if prop.type in ['BOOLEAN', 'INT', 'FLOAT', 'STRING', 'ENUM']:
                values[prop.identifier] = list(value) if prop.is_array else value
            elif prop.type == 'POINTER' and isinstance(value, bpy.types.ID):
                values[prop.identifier] = {'id': value.name}
        except (AttributeError, TypeError, ValueError, RuntimeError):
            pass
    return values


def animation_record():
    records = []
    for a in bpy.data.actions:
        data = {'name': a.name, 'users': a.users, 'fake_user': a.use_fake_user, 'curves': []}
        for fc, context in curves(a):
            data['curves'].append({'path': fc.data_path, 'index': fc.array_index, 'mute': fc.mute, 'extrapolation': fc.extrapolation, **context,
                'keys': [{'time': float(k.co.x), 'value': float(k.co.y), 'interpolation': k.interpolation,
                          'easing': k.easing, 'left_handle': list(k.handle_left), 'right_handle': list(k.handle_right),
                          'left_handle_type': k.handle_left_type, 'right_handle_type': k.handle_right_type}
                         for k in fc.keyframe_points],
                'modifiers': [rna_settings(m) for m in fc.modifiers]})
        records.append(data)
    return records


def id_name(value):
    return value.name if value is not None else None


def animation_binding(owner):
    ad = getattr(owner, 'animation_data', None)
    if ad is None:
        return None
    nla = []
    for track in ad.nla_tracks:
        nla.append({'name': track.name, 'mute': track.mute, 'solo': track.is_solo,
            'strips': [{'name': st.name, 'type': st.type, 'action': id_name(st.action),
                        'start': st.frame_start, 'end': st.frame_end, 'action_start': st.action_frame_start,
                        'action_end': st.action_frame_end, 'scale': st.scale, 'repeat': st.repeat,
                        'blend_type': st.blend_type, 'influence': st.influence,
                        'animated_time': st.use_animated_time, 'animated_influence': st.use_animated_influence}
                       for st in track.strips]})
    drivers = []
    for fc in ad.drivers:
        drivers.append({'path': fc.data_path, 'index': fc.array_index, 'expression': fc.driver.expression,
            'type': fc.driver.type, 'variables': [{'name': v.name, 'type': v.type,
                'targets': [{'id': id_name(t.id), 'path': t.data_path, 'bone': t.bone_target,
                             'transform_type': t.transform_type, 'transform_space': t.transform_space}
                            for t in v.targets]} for v in fc.driver.variables]})
    return {'action': id_name(ad.action), 'nla_enabled': ad.use_nla, 'nla_tracks': nla, 'drivers': drivers}


def geometry_hash(objects, evaluated=False, depsgraph=None):
    h = hashlib.sha256()
    def feed_mesh(mesh):
        coords = array.array('f', [0.0]) * (len(mesh.vertices) * 3)
        mesh.vertices.foreach_get('co', coords)
        h.update(coords.tobytes())
        h.update(struct.pack('<III', len(mesh.vertices), len(mesh.edges), len(mesh.polygons)))
        for p in mesh.polygons:
            h.update(struct.pack('<I', len(p.vertices)))
            h.update(array.array('I', p.vertices).tobytes())
    for o in sorted(objects, key=lambda x: x.name):
        if o.type not in ['MESH', 'CURVE', 'SURFACE', 'FONT']:
            continue
        h.update(o.name.encode())
        if evaluated:
            ev = o.evaluated_get(depsgraph)
            mesh = ev.to_mesh()
            try:
                if mesh is not None:
                    feed_mesh(mesh)
            finally:
                ev.to_mesh_clear()
        elif o.type == 'MESH':
            feed_mesh(o.data)
            if o.data.shape_keys:
                for key in o.data.shape_keys.key_blocks:
                    h.update(key.name.encode())
                    coords = array.array('f', [0.0]) * (len(key.data) * 3)
                    key.data.foreach_get('co', coords)
                    h.update(coords.tobytes())
        else:
            details = []
            for sp in o.data.splines:
                details.append([sp.type, [(list(p.co), p.radius, p.tilt) for p in sp.points],
                    [(list(p.co), list(p.handle_left), list(p.handle_right), p.radius, p.tilt) for p in sp.bezier_points]])
            h.update(digest([details, getattr(o.data, 'body', None), o.data.bevel_depth,
                             o.data.extrude, o.data.resolution_u]).encode())
    return h.hexdigest()


def sample(s, f, cfg, objects, pose=False, geometry=False, visibility_exclusions=()):
    set_time(s, f)
    c = camera_at(s, f, cfg)
    s.camera = c
    dg = bpy.context.evaluated_depsgraph_get()
    evc = c.evaluated_get(dg)
    data = evc.data
    camera = {'name': c.name, 'matrix_world': matrix(evc.matrix_world), 'type': data.type,
              'lens': data.lens, 'ortho_scale': data.ortho_scale, 'shift': [data.shift_x, data.shift_y],
              'sensor': [data.sensor_width, data.sensor_height, data.sensor_fit],
              'clip': [data.clip_start, data.clip_end], 'focus_distance': data.dof.focus_distance}
    items = []
    for o in objects:
        ev = o.evaluated_get(dg)
        # Curve bounds can be lazy/sentinel-sized until the draw engine evaluates
        # them. Transform fidelity must not compare that cache as geometry truth.
        item = {'name': o.name, 'matrix_world': matrix(ev.matrix_world)}
        if o.name not in visibility_exclusions:
            item['hide_render'] = bool(o.hide_render)
        if pose and o.type == 'ARMATURE':
            item['pose_bones'] = {b.name: matrix(b.matrix) for b in ev.pose.bones}
        items.append(item)
    result = {'source_frame': float(f), 'camera': camera, 'objects': items}
    if geometry:
        result['evaluated_geometry_sha256'] = geometry_hash(objects, True, dg)
    return result


def pure_volume(o):
    if o.type == 'VOLUME':
        return True
    materials = list(getattr(o.data, 'materials', [])) if o.data else []
    if not materials or any(m is None or not m.use_nodes for m in materials):
        return False
    for m in materials:
        outputs = [n for n in m.node_tree.nodes if n.type == 'OUTPUT_MATERIAL' and n.is_active_output]
        if not outputs or any(n.inputs['Surface'].is_linked or not n.inputs['Volume'].is_linked for n in outputs):
            return False
    return True
