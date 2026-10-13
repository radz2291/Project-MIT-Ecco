"""Texture-free exports with measured retiming and preservation checks."""
import fnmatch
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
from reference_common import arguments, load_config, segment_plan, file_hash, write_json, digest
from blender_common import select_scene, sample, animation_record, geometry_hash, pure_volume, set_time, camera_at


def grouped(name, groups, initial):
    result = initial
    for group in groups:
        if any(fnmatch.fnmatchcase(name, pattern) for pattern in group['patterns']):
            result = float(group['value'])
    if not 0 <= result <= 1:
        raise ValueError('Grey/alpha values must be between zero and one')
    return result


def main():
    cfg = load_config(arguments(True).config)
    s = select_scene(cfg)
    out = Path(cfg['output_dir']); out.mkdir(parents=True, exist_ok=True)
    settings = cfg.get('render', {})
    objects = list(s.objects)
    source_hash = file_hash(cfg['source_blend'])
    source_fps = s.render.fps / s.render.fps_base
    source_aspect = s.render.resolution_x * s.render.pixel_aspect_x / (s.render.resolution_y * s.render.pixel_aspect_y)
    resolution = cfg['resolution'] or [max(2, round(source_aspect * 720 / 2) * 2), 720]
    if s.render.use_border and s.render.use_crop_to_border:
        raise ValueError('Source uses cropped render border; preserve its framing with a custom export or authorized adaptation')
    plans = [(seg, segment_plan(cfg, seg, source_fps)) for seg in cfg['segments']]
    static_before = geometry_hash(objects)
    keys_before = digest(animation_record())
    suppressed = set()
    changes = list(cfg.get('adaptations', []))
    particles = []
    for o in objects:
        if any(fnmatch.fnmatchcase(o.name, p) for p in settings.get('hide_objects', [])):
            suppressed.add(o.name); changes.append({'kind': 'hide_object', 'object': o.name, 'reason': 'configured reference omission'})
        elif settings.get('suppress_volume_only', True) and pure_volume(o):
            suppressed.add(o.name); changes.append({'kind': 'suppress_volume_only', 'object': o.name})
        if settings.get('suppress_particle_systems', True):
            for m in o.modifiers:
                if m.type == 'PARTICLE_SYSTEM' and m.show_render:
                    particles.append((o, m)); changes.append({'kind': 'suppress_particle_modifier', 'object': o.name, 'modifier': m.name})
    baseline = {}; baseline_records = {}
    evaluated = settings.get('verify_evaluated_geometry', False)
    for _, plan in plans:
        path = out / plan['id'] / 'frames'
        if (path.exists() and any(path.glob('frame_*.png'))) or (path.parent / 'render_manifest.json').exists():
            if not cfg.get('overwrite', False):
                raise FileExistsError(f'{path.parent}: existing output; explicitly choose overwrite or a new directory')
        # Hash all source objects, including bones if present. Hide flags for explicitly suppressed effects are excluded.
        records = [sample(s, f, cfg, objects, True, evaluated, suppressed) for f in plan['source_samples']]
        if any(v['camera']['type'] not in ['PERSP', 'ORTHO'] for v in records):
            raise ValueError('Workbench helper supports perspective/orthographic cameras; use a faithful alternative for panoramic cameras')
        baseline_records[plan['id']] = records
        baseline[plan['id']] = digest(records)

    s.render.engine = 'BLENDER_WORKBENCH'
    sh = s.display.shading
    sh.light = 'STUDIO'; sh.studio_light = settings.get('studio_light', 'paint.sl')
    sh.color_type = 'OBJECT'; sh.background_type = 'VIEWPORT'
    bg = float(settings.get('background_grey', .15)); sh.background_color = (bg, bg, bg)
    sh.show_shadows = bool(settings.get('shadows', False)); sh.show_cavity = bool(settings.get('cavity', False))
    if sh.show_cavity:
        sh.cavity_type = 'WORLD'; sh.cavity_ridge_factor = .5; sh.cavity_valley_factor = .5
    sh.show_specular_highlight = False; sh.show_object_outline = False; sh.show_xray = False; sh.use_dof = False
    s.display.render_aa = str(settings.get('anti_aliasing', '32'))
    s.render.use_compositing = False; s.render.use_sequencer = False; s.render.film_transparent = False
    s.render.resolution_x, s.render.resolution_y = resolution; s.render.resolution_percentage = 100
    s.render.pixel_aspect_x = 1; s.render.pixel_aspect_y = 1
    if abs(resolution[0] / resolution[1] - source_aspect) > .002:
        changes.append({'kind': 'output_aspect_change', 'source_aspect': source_aspect, 'output_aspect': resolution[0] / resolution[1]})
    s.render.image_settings.file_format = 'PNG'; s.render.image_settings.color_mode = 'RGB'
    s.view_settings.view_transform = 'Standard'; s.view_settings.look = 'None'; s.view_settings.exposure = 0; s.view_settings.gamma = 1
    changes.append({'kind': 'reference_shading', 'engine': 'BLENDER_WORKBENCH', 'textures': False,
                    'grey_groups': settings.get('grey_groups', []), 'shadows': sh.show_shadows, 'cavity': sh.show_cavity})
    for o in objects:
        g = grouped(o.name, settings.get('grey_groups', []), float(settings.get('base_grey', .62)))
        alpha = grouped(o.name, settings.get('alpha_groups', []), 1.)
        o.color = (g, g, g, alpha)
        if alpha != 1:
            changes.append({'kind': 'reference_alpha', 'object': o.name, 'alpha': alpha})
    for _, m in particles:
        m.show_render = False

    for seg, plan in plans:
        records_after = [sample(s, f, cfg, objects, True, evaluated, suppressed) for f in plan['source_samples']]
        after = digest(records_after)
        geometry_after = geometry_hash(objects); keys_after = digest(animation_record())
        if after != baseline[plan['id']] or geometry_after != static_before or keys_after != keys_before:
            differences = []
            for a, b in zip(baseline_records[plan['id']], records_after):
                if a == b:
                    continue
                entry = {'source_frame': a['source_frame']}
                if a['camera'] != b['camera']:
                    entry['camera_before'] = a['camera']; entry['camera_after'] = b['camera']
                entry['objects'] = [{'before': x, 'after': y} for x, y in zip(a['objects'], b['objects']) if x != y][:5]
                differences.append(entry)
                if len(differences) >= 5: break
            write_json(out / 'preservation_failure.json', {'geometry_before': static_before, 'geometry_after': geometry_after,
                       'keys_before': keys_before, 'keys_after': keys_after, 'sample_differences': differences})
            raise RuntimeError('Preservation check failed: shading changes affected measured motion/geometry/keys')
        folder = out / plan['id']; frames = folder / 'frames'; frames.mkdir(parents=True, exist_ok=True)
        manifest_file = folder / 'render_manifest.json'
        if cfg.get('overwrite'):
            manifest_file.unlink(missing_ok=True)
            for p in frames.glob('frame_*.png'):
                if p.stem.removeprefix('frame_').isdigit():
                    p.unlink()
        # These are source-time stills. Changing scene FPS can change drivers and
        # simulations; output FPS belongs only to the encoding manifest.
        landmarks = []
        for i, f in enumerate(plan['source_samples']):
            set_time(s, f); s.camera = camera_at(s, f, cfg)
            for name in suppressed:
                s.objects[name].hide_render = True
            bpy.context.view_layer.update()
            for lm in seg.get('landmarks', []):
                obj = s.objects.get(lm['object'])
                if obj is None:
                    raise ValueError(f'Unknown landmark object: {lm["object"]}')
                p = obj.evaluated_get(bpy.context.evaluated_depsgraph_get()).matrix_world @ Vector(lm.get('local_point', [0, 0, 0]))
                q = world_to_camera_view(s, s.camera, p)
                landmarks.append({'name': lm.get('name', obj.name), 'output_index': i + 1, 'source_frame': f,
                    'screen': [q.x, q.y, q.z], 'inside_frustum': bool(0 <= q.x <= 1 and 0 <= q.y <= 1 and q.z > 0),
                    'required_at': lm.get('required_at', []), 'note': 'Projection only; actual occlusion requires visual review'})
            s.render.filepath = str(frames / f'frame_{i + 1:06d}.png')
            bpy.ops.render.render(write_still=True)
        if file_hash(cfg['source_blend']) != source_hash:
            raise RuntimeError('Original source file changed during export')
        write_json(manifest_file, {**plan, 'source_blend': cfg['source_blend'], 'source_sha256': source_hash,
            'scene': s.name, 'camera_override': cfg.get('camera'), 'resolution': resolution,
            'motion_before': baseline[plan['id']], 'motion_after': after, 'motion_preserved': True,
            'source_geometry_sha256': static_before, 'source_animation_sha256': keys_before,
            'evaluated_geometry_checked': evaluated, 'reference_changes': changes, 'landmarks': landmarks,
            'render_config_sha256': digest(settings),
            'generator': cfg.get('generator', {}), 'visual_review': 'pending', 'event_frames': seg.get('event_frames', [])})
        print({'rendered_segment': plan['id'], 'frames': plan['output_frames'], 'duration': plan['duration_seconds']})
    if settings.get('save_reference_blend', False):
        bpy.ops.wm.save_as_mainfile(filepath=str(out / 'viewport_shaded_source.blend'), copy=True)
    assert file_hash(cfg['source_blend']) == source_hash


if __name__ == '__main__':
    main()
