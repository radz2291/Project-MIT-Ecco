"""Read-only scene/key/evaluated-motion extraction. Run with Blender --python."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bpy
from reference_common import arguments, load_config, write_json, file_hash, segment_plan
from blender_common import select_scene, animation_record, animation_binding, sample, geometry_hash, rna_settings


def main():
    cfg = load_config(arguments(True).config)
    s = select_scene(cfg)
    initial = (s.frame_current, s.frame_subframe, s.camera)
    out = Path(cfg['output_dir']) / 'inspection'
    settings = cfg.get('inspect', {})
    names = settings.get('objects') or [o.name for o in s.objects]
    if any(n not in s.objects for n in names):
        raise ValueError('Unknown inspected object')
    objects = [s.objects[n] for n in names]
    source_hash = file_hash(cfg['source_blend'])
    warnings = []
    scene_objects = []
    for o in s.objects:
        mods = [rna_settings(m) for m in o.modifiers]
        if o.rigid_body or any(m.type in ['CLOTH', 'FLUID', 'SOFT_BODY', 'PARTICLE_SYSTEM', 'NODES'] for m in o.modifiers):
            warnings.append(f'{o.name}: simulation/procedural system; verify caches and evaluated geometry')
        scene_objects.append({'name': o.name, 'type': o.type, 'parent': o.parent.name if o.parent else None,
            'parent_type': o.parent_type, 'parent_bone': o.parent_bone,
            'collections': [c.name for c in o.users_collection], 'dimensions': list(o.dimensions),
            'materials': [m.name if m else None for m in getattr(o.data, 'materials', [])] if o.data else [],
            'modifiers': mods, 'constraints': [rna_settings(c) for c in o.constraints],
            'animation': animation_binding(o), 'data_animation': animation_binding(o.data) if o.data else None,
            'shape_key_animation': animation_binding(o.data.shape_keys) if o.type == 'MESH' and o.data.shape_keys else None})
    fps = s.render.fps / s.render.fps_base
    bindings = []
    for collection_name in ['objects', 'meshes', 'curves', 'cameras', 'lights', 'armatures', 'shape_keys', 'materials', 'worlds', 'scenes', 'node_groups', 'collections']:
        for owner in getattr(bpy.data, collection_name, []):
            binding = animation_binding(owner)
            if binding:
                bindings.append({'collection': collection_name, 'name': owner.name, 'animation': binding})
            tree = getattr(owner, 'node_tree', None)
            binding = animation_binding(tree) if tree else None
            if binding:
                bindings.append({'collection': collection_name, 'name': owner.name, 'node_tree': tree.name, 'animation': binding})
    plans = [segment_plan(cfg, seg, fps) for seg in cfg['segments']]
    step = float(settings.get('sample_step', 1))
    if step <= 0:
        raise ValueError('sample_step must be positive')
    times = set(float(v) for v in settings.get('extra_frames', []))
    for plan in plans:
        lo, hi = sorted([plan['source_start'], plan['source_end']])
        f = lo
        while f <= hi + 1e-8:
            times.add(round(f, 8)); f += step
        times.add(hi)
    try:
        samples = [sample(s, f, cfg, objects, settings.get('pose_bones', False), settings.get('evaluated_geometry', False)) for f in sorted(times)]
        write_json(out / 'scene.json', {'source': cfg['source_blend'], 'sha256': source_hash,
            'scene': s.name, 'fps': fps, 'range': [s.frame_start, s.frame_end],
            'render_format': {'resolution': [s.render.resolution_x, s.render.resolution_y], 'percentage': s.render.resolution_percentage,
                'pixel_aspect': [s.render.pixel_aspect_x, s.render.pixel_aspect_y], 'border': s.render.use_border, 'crop_to_border': s.render.use_crop_to_border},
            'unit_system': s.unit_settings.system, 'unit_scale': s.unit_settings.scale_length,
            'markers': [{'name': m.name, 'frame': m.frame, 'camera': m.camera.name if m.camera else None} for m in s.timeline_markers],
            'objects': scene_objects, 'geometry_sha256': geometry_hash(list(s.objects)),
            'animation_bindings': bindings,
            'plans': plans, 'warnings': warnings,
            'visibility_note': 'Object render flags are not an occlusion or collection-visibility test'})
        write_json(out / 'animation_keys.json', {'actions': animation_record(),
            'note': 'All Actions included. Inspect binding/users; NLA remaps action times. Evaluated samples determine scene motion.'})
        write_json(out / 'motion_samples.json', {'tracked_objects': names, 'samples': samples})
        assert file_hash(cfg['source_blend']) == source_hash
    finally:
        s.frame_set(initial[0], subframe=initial[1]); s.camera = initial[2]
    print({'inspection': str(out), 'samples': len(times), 'objects': len(objects), 'warnings': len(warnings)})


if __name__ == '__main__':
    main()
