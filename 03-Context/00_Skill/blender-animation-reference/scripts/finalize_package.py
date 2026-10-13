"""Gate ready status on completed prompts, unchanged assets and actual agent review."""
import argparse
import json
import re
from pathlib import Path
from reference_common import load_config, file_hash, write_json, segment_plan, digest


def completed_text(path):
    if not path.is_file():
        raise ValueError(f'Missing authored document: {path}')
    text = path.read_text(encoding='utf-8').strip()
    if not text or re.search(r'\{\{.*?\}\}', text):
        raise ValueError(f'Empty or unfilled document: {path}')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--config', required=True); p.add_argument('--review', required=True)
    args = p.parse_args(); cfg = load_config(args.config); root = Path(cfg['output_dir'])
    review = json.loads(Path(args.review).read_text(encoding='utf-8'))
    completed_text(root / 'scene-description.md')
    if len(cfg['segments']) > 1:
        completed_text(root / 'master-timeline.md')
    manifest_path = root / 'package_manifest.json'
    package = json.loads(manifest_path.read_text(encoding='utf-8'))
    if file_hash(cfg['source_blend']) != package['source_sha256']:
        raise ValueError('Source changed since export')
    results = []; pending = []
    for seg in cfg['segments']:
        folder = root / seg['id']; completed_text(folder / 'prompt.md')
        mpath = folder / 'delivery_manifest.json'; m = json.loads(mpath.read_text(encoding='utf-8'))
        plan = segment_plan(cfg, seg, m['source_fps'])
        if any(plan[k] != m[k] for k in ['source_start', 'source_end', 'fps_fraction', 'output_frames', 'source_samples']) or digest(cfg.get('render', {})) != m['render_config_sha256'] or (cfg['resolution'] is not None and tuple(cfg['resolution']) != tuple(m['resolution'])):
            raise ValueError('Configuration changed after export')
        item = review.get('segments', {}).get(seg['id'])
        if not item or item.get('approved_for_handoff') is not True or not item.get('findings', '').strip():
            raise ValueError(f'{seg["id"]}: explicit agent review and findings required')
        required = {'first_frame.png', 'last_frame.png', 'review_sheet.jpg'} | {v['file'] for v in m['event_images']}
        inspected = set(item.get('inspected_assets', []))
        if not required.issubset(inspected):
            raise ValueError(f'{seg["id"]}: review omitted required boundary/transition assets')
        for name in inspected:
            target = (folder / name).resolve()
            if not target.is_relative_to(folder.resolve()) or not target.is_file():
                raise ValueError('Review references a missing/out-of-package asset')
        if m['warnings'] and not item.get('warning_disposition', '').strip():
            raise ValueError('QA warnings require an explicit review disposition')
        if not m['decode_passed'] or not m['motion_preserved'] or file_hash(Path(m['video'])) != m['video_sha256']:
            raise ValueError('Encoded asset changed or failed technical QA')
        if [file_hash(folder / m['first_frame']), file_hash(folder / m['last_frame'])] != m['boundary_image_source_hashes']:
            raise ValueError('Boundary stills do not match exported samples')
        m['visual_review'] = item; m['prompt_status'] = 'authored and reviewed'
        m['ready_status'] = 'Reference assets and prompt ready; generated reproduction not tested'
        m['prompt_sha256'] = file_hash(folder / 'prompt.md')
        pending.append((mpath, m))
        results.append({'id': seg['id'], 'video': m['video'], 'prompt': str(folder / 'prompt.md'),
                        'visual_review': 'completed', 'warnings_reviewed': len(m['warnings'])})
    # Validate every segment before marking any of them ready.
    for mpath, m in pending:
        write_json(mpath, m)
    package['segments'] = results
    package['scene_description_sha256'] = file_hash(root / 'scene-description.md')
    if len(cfg['segments']) > 1:
        package['master_timeline_sha256'] = file_hash(root / 'master-timeline.md')
    package['ready_status'] = 'Ready for handoff; external generator input support/reproduction remains to verify'
    write_json(manifest_path, package)
    print(json.dumps({'ready': results}))


if __name__ == '__main__':
    main()
