"""Shared config/timing utilities; safe to import outside Blender."""
import argparse
import hashlib
import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path


def arguments(in_blender=False):
    argv = sys.argv[sys.argv.index('--') + 1:] if in_blender and '--' in sys.argv else (sys.argv[1:] if not in_blender else [])
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True)
    return p.parse_args(argv)


def load_config(path):
    path = Path(path).resolve()
    cfg = json.loads(path.read_text(encoding='utf-8-sig'))
    for key in ['source_blend', 'output_dir']:
        value = Path(cfg[key]).expanduser()
        cfg[key] = str((path.parent / value).resolve() if not value.is_absolute() else value.resolve())
    cfg['_config_file'] = str(path)
    if not Path(cfg['source_blend']).is_file():
        raise ValueError('source_blend must identify an existing saved Blender file')
    if Path(cfg['output_dir']) == Path(cfg['source_blend']):
        raise ValueError('Output cannot replace the source file')
    size = cfg.get('resolution')
    if size is not None and (len(size) != 2 or any(not isinstance(v, int) or v < 2 or v % 2 for v in size)):
        raise ValueError('H.264 reference resolution must contain two positive even integers')
    cfg['resolution'] = size
    if not cfg.get('segments'):
        raise ValueError('At least one explicit source segment is required')
    names = set()
    for seg in cfg['segments']:
        name = seg['id']
        if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,63}', name) or name in names:
            raise ValueError('Segment ids must be unique safe directory names, maximum 64 characters')
        names.add(name)
        for key in ['source_start', 'source_end']:
            if not math.isfinite(float(seg[key])):
                raise ValueError('Source frame endpoints must be finite')
    return cfg


def segment_plan(cfg, seg, source_fps):
    fps = Fraction(str(cfg.get('fps') or source_fps)).limit_denominator(100000)
    if fps <= 0:
        raise ValueError('FPS must be positive')
    start, end = float(seg['source_start']), float(seg['source_end'])
    duration = Fraction(str(seg['duration'])) if seg.get('duration') is not None else Fraction(str(abs(end - start) + 1)) / Fraction(str(source_fps)).limit_denominator(100000)
    n = duration * fps
    if n.denominator != 1 or n < 2:
        raise ValueError(f'{seg["id"]}: duration × FPS must be an integer of at least two frames; got {n}')
    n = int(n)
    samples = [start + (end - start) * i / (n - 1) for i in range(n)]
    return {'id': seg['id'], 'source_start': start, 'source_end': end,
            'source_fps': float(source_fps), 'fps': float(fps), 'fps_fraction': str(fps),
            'duration_seconds': float(duration), 'output_frames': n, 'source_samples': samples,
            'last_sample_time': (n - 1) / float(fps), 'sampling': 'Inclusive endpoints; last image displayed through clip duration'}


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()
