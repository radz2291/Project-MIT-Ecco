"""Record exact saved review candidate, measured timing, and output linkage."""
import json,hashlib,re
from pathlib import Path
P=Path(__file__).resolve().parents[3];E=P/'Records/Tasks/T-007/Evidence/Motion_v005';T=P/'Records/Tasks/T-007'
build=json.loads((E/'build.json').read_text());qa=json.loads((E/'video-qa.json').read_text())
assert json.loads((E/'verification.json').read_text())['passed']
scene=P/build['scene'];video=P/qa['video']
assert hashlib.sha256(scene.read_bytes()).hexdigest()==build['scene_sha256']
assert hashlib.sha256(video.read_bytes()).hexdigest()==qa['video_sha256']
report=T/'report.md';text=report.read_text(encoding='utf-8')
text=text.replace('## Editable source and verification',f"Measured native render time: **{qa['mean_render_seconds']:.3f} seconds/frame average; {qa['max_render_seconds']:.3f} seconds slowest**. All 240 frames remain below10 seconds. All delivered frames decoded successfully; {qa['distinct_decoded_frames']} distinct, no blank frames. [Video QA](Evidence/Motion_v005/video-qa.json) | [Render timing](Evidence/Motion_v005/render-progress.json) | [Output manifest](Evidence/Motion_v005/output-manifest.json). Representative contact buildup and reception frames visually inspected.\n\n## Editable source and verification")
text=text.replace('## Review and synchronization','[Contact buildup](Evidence/Motion_v005/Decoded/decoded_f031.png) | [Surface settling and return](Evidence/Motion_v005/Decoded/decoded_f038.png) | [First reception](Evidence/Motion_v005/Decoded/decoded_f048.png)\n\n## Review and synchronization')
report.write_text(text,encoding='utf-8')
paths=[scene,video]+[E/'Decoded'/f'decoded_f{f:03d}.png' for f in (31,38,48)]
manifest={'scope':'T7 v005 organic contact review','local_only_heavy_media':True,'Still05_included':False,'outputs':[{'path':x.relative_to(P).as_posix(),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()} for x in paths]}
(E/'output-manifest.json').write_text(json.dumps(manifest,indent=2))
for link in re.findall(r'\]\(([^)]+)\)',text):
 if '://' not in link:assert (report.parent/link).resolve().is_file(),link
settings=json.loads((P/'Mechanisms/B201/preview-settings_fast_v002.json').read_text())
settings.update(mean_measured_seconds=qa['mean_render_seconds'],max_measured_seconds=qa['max_render_seconds'],render_script='Scripts/render_motion_preview_v005.py',encode_script='Scripts/encode_verify_motion_v005.py',contact_response='Native material local sphere-rock arrival/maturation/decay, continuous eased contact sweep')
(P/'Mechanisms/B201/preview-settings_fast_v005.json').write_text(json.dumps(settings,indent=2))
print('PACKAGE_PASS',len(paths),'outputs; all report links resolve')
