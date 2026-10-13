"""Encode and technically verify reference assets. Does not author semantic prompts."""
import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from PIL import Image, ImageDraw, ImageStat
import imageio_ffmpeg
from reference_common import arguments, load_config, file_hash, write_json, segment_plan, digest


def run(command):
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main():
    cfg = load_config(arguments().config)
    out = Path(cfg['output_dir']); source_hash = file_hash(cfg['source_blend'])
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    deliveries = []
    for seg in cfg['segments']:
        folder = out / seg['id']; frames = folder / 'frames'
        manifest = json.loads((folder / 'render_manifest.json').read_text(encoding='utf-8'))
        plan = segment_plan(cfg, seg, manifest['source_fps'])
        if any(plan[k] != manifest[k] for k in ['source_start', 'source_end', 'fps_fraction', 'output_frames', 'source_samples']) or (cfg['resolution'] is not None and tuple(cfg['resolution']) != tuple(manifest['resolution'])) or digest(cfg.get('render', {})) != manifest['render_config_sha256']:
            raise RuntimeError('Configuration changed after rendering; rerender rather than package stale assets')
        if source_hash != manifest['source_sha256'] or not manifest['motion_preserved']:
            raise RuntimeError('Source hash or reference preservation check failed')
        n = manifest['output_frames']; fps = manifest['fps']; size = tuple(manifest['resolution'])
        expected = [frames / f'frame_{i:06d}.png' for i in range(1, n + 1)]
        if any(not p.exists() for p in expected) or len(list(frames.glob('frame_*.png'))) != n:
            raise RuntimeError('Missing or stale frame files; render exact configured range')
        brightness, contrast, differences = [], [], []
        previous = None
        for p in expected:
            with Image.open(p) as im:
                if im.size != size:
                    raise RuntimeError(f'Unexpected resolution: {p}')
                grey = im.convert('L')
                stat = ImageStat.Stat(grey); brightness.append(stat.mean[0]); contrast.append(stat.stddev[0])
                thumbnail = grey.resize((64, 36))
                values = list(thumbnail.tobytes())
                if previous is not None:
                    differences.append(sum(abs(a - b) for a, b in zip(values, previous)) / len(values))
                previous = values
                neutral = grey.convert('RGB')
            neutral.save(p)
        video = folder / 'motion_reference.mp4'
        try:
            run([ff, '-y', '-v', 'error', '-framerate', manifest['fps_fraction'], '-i', str(frames / 'frame_%06d.png'),
                 '-frames:v', str(n), '-c:v', 'libx264', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', str(video)])
            run([ff, '-v', 'error', '-i', str(video), '-f', 'null', '-'])
        except subprocess.CalledProcessError as e:
            raise RuntimeError(e.stderr.decode(errors='replace')) from e
        reader = imageio_ffmpeg.read_frames(str(video)); metadata = next(reader); decoded = sum(1 for _ in reader)
        # ffmpeg prints a rounded fps in its probe text for fractional rates.
        if decoded != n or abs(metadata['fps'] - fps) > .02 or tuple(metadata['size']) != size:
            raise RuntimeError('Decoded frame count, FPS or resolution mismatch')
        first = folder / 'first_frame.png'; last = folder / 'last_frame.png'
        shutil.copyfile(expected[0], first); shutil.copyfile(expected[-1], last)
        events = []
        for event in seg.get('event_frames', []):
            index = min(range(n), key=lambda i: abs(manifest['source_samples'][i] - float(event)))
            dest = folder / f'event_{index + 1:06d}.png'; shutil.copyfile(expected[index], dest)
            events.append({'file': dest.name, 'requested_source_frame': event,
                           'actual_source_frame': manifest['source_samples'][index], 'output_seconds': index / fps})
        indices = sorted(set(round(i * (n - 1) / min(11, n - 1)) for i in range(min(12, n))))
        cols = min(4, len(indices)); cellw = 320; cellh = round(cellw * size[1] / size[0])
        sheet = Image.new('RGB', (cols * cellw, math.ceil(len(indices) / cols) * (cellh + 25)), (24, 24, 24))
        draw = ImageDraw.Draw(sheet)
        for k, index in enumerate(indices):
            x = k % cols * cellw; y = k // cols * (cellh + 25)
            with Image.open(expected[index]) as im:
                sheet.paste(im.resize((cellw, cellh)), (x, y))
            draw.text((x + 6, y + cellh + 5), f'{index / fps:.3f}s | source {manifest["source_samples"][index]:.3f}', fill='white')
        sheet.save(folder / 'review_sheet.jpg', quality=94)
        warnings = []
        low = [i + 1 for i, b in enumerate(brightness) if b < 12]
        flat = [i + 1 for i, v in enumerate(contrast) if v < 3]
        still = [i + 2 for i, v in enumerate(differences) if v < .02]
        if low: warnings.append({'kind': 'very_dark_frames', 'indices': low})
        if flat: warnings.append({'kind': 'low_detail_frames', 'indices': flat})
        if still: warnings.append({'kind': 'nearly_identical_adjacent_frames', 'indices': still, 'note': 'May be authored holds; inspect before changing'})
        if any(c.get('kind') == 'output_aspect_change' for c in manifest['reference_changes'] if isinstance(c, dict)):
            warnings.append({'kind': 'output_aspect_change', 'note': 'Verify this reframing is requested/authorized'})
        for lm in manifest.get('landmarks', []):
            point = 'first' if lm['output_index'] == 1 else ('last' if lm['output_index'] == n else None)
            if point and point in lm['required_at'] and not lm['inside_frustum']:
                warnings.append({'kind': 'landmark_outside_frustum', 'landmark': lm['name'], 'at': point})
        result = {**manifest, 'video': str(video), 'video_sha256': file_hash(video), 'first_frame': first.name, 'last_frame': last.name,
                  'boundary_image_source_hashes': [file_hash(expected[0]), file_hash(expected[-1])],
                  'event_images': events, 'decoded_frames': decoded, 'decoded_fps': metadata['fps'],
                  'verified_duration_seconds': n / fps, 'decode_passed': True,
                  'original_unchanged': file_hash(cfg['source_blend']) == source_hash,
                  'greyscale_packaging': True, 'warnings': warnings,
                  'visual_review': 'pending: agent must inspect the actual images/video',
                  'prompt_status': 'agent must author prompt.md from measured evidence'}
        write_json(folder / 'delivery_manifest.json', result)
        deliveries.append({'id': seg['id'], 'video': str(video), 'warnings': len(warnings), 'visual_review': 'pending'})
    write_json(out / 'package_manifest.json', {'source': cfg['source_blend'], 'source_sha256': source_hash,
               'segments': deliveries, 'ready_status': 'Technical export complete; semantic prompts and visual review required'})
    print(json.dumps({'packaged': deliveries}))


if __name__ == '__main__':
    main()
