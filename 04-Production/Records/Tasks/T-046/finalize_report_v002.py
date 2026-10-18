"""Finalize honest review handoff after actual queued media exists; no Git writes."""
import json,hashlib,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];T=ROOT/'04-Production/Records/Tasks/T-046';A=ROOT/'04-Production/Shared/Assets/Acoustics';E=T/'Evidence'
manifest=json.loads((A/'manifest_v002.json').read_text());native=json.loads((E/'native-verification_v010.json').read_text());media=json.loads((E/'media-verification_v002.json').read_text())
assert native['all_pass'] and media['decode_without_errors'] and media['all_frames_nonblank_size']
logs=[json.loads((E/n).read_text()) for n in ['sample_A_v009.json','benchmark_A_v009.json','benchmark_B_v010.json','batch_A_v009.json']];assert all(x['all_under_5'] for x in logs)
rows=[r for log in logs for r in log['frames']];times=[r['seconds'] for r in rows];bench=[r['seconds'] for log in logs[:3] for r in log['frames']]
held=T/'report_held_v001.md'
if not held.exists():shutil.copyfile(T/'report.md',held)
text=f'''# T46 — shared acoustic package for master integration

18 October 2026. Reusable cyan send/contact/emerald return package and two linked reuse consumers are saved and visually inspected. Current artifacts: Acoustics v003, consumer A v009 and B v010, event exports v003, interface v002, four-second behavior video v002. This is an asset-stage candidate for Radzi review; actual film shots, A-OUTPUT, reconstruction and film assembly remain outside scope.

Ticket `41cb52bd-780a-4fc2-9b2f-df2728b3aba4`, delegated by owner-authorized T45. Attempt 2 run `ddddac19-70e4-4844-beda-5ebfd24ce4c0`, worker `codex-t45-sensing-builder-v001`. The accepted upstream is T44 commit `a08d0ecfbd6f3241298f506b3ea42613388b3baf`; fresh Work confirmed T44 Done before reclaim. T45 alone integrates Git and final independent verification. Only Radzi accepts reviewed work.

## Candidate and review media

[Exact native/media/source hashes](../../../Shared/Assets/Acoustics/manifest_v002.json), [portable interface](../../../Shared/Assets/Acoustics/README_v001.md), [packet schema](../../../Shared/Assets/Acoustics/event-interface_v002.json). Native/video paths are local to `C:\\Users\\RZ1\\Desktop\\RZ\\261013-MIT-Ecco`; no media upload or off-machine backup is claimed.

| Inspect | Selected current still |
|---|---|
| Three cyan outgoing fronts and actual retained sensor cap | [Send](Previews/Review_send_v002.png) |
| True wall interaction, curved cup and fine patch | [Contact](Previews/Review_contact_v002.png) |
| Three emerald returns toward the same cap | [Return](Previews/Review_return_v002.png) |
| Minimal explicitly schematic arrival-time cue | [Arrival cue](Previews/Review_arrival_cue_v002.png) |
| Second linked consumer, distinct camera/timing | [Reuse B](Previews/Review_reuse_B_v002.png) |

Local playable demo: `Previews/Sensing_behavior_v002.mp4` — 96 frames, 24 fps, 1280×720, 4 seconds, silent H.264. It shows one held pulse/contact/return, assembly movement between events, then a second held event. Acquired points remain world-fixed. B retains its separate 108-frame/4.5-second score. No ten-second B201 score or V3 movie timing is copied.

## Sources, reuse and registration

Read fresh live handoff, current owner cycle, T45 ownership/common contract, T42 register, T43 controlling release and relevant S02/S04 contracts, Scene Director/Directorial Identity, Engineering Baseline and accepted T44 continuity interface/handoff. Actual T44 and B201 natives were inspected in isolated Blender 5.2.2; the user's live scene remains untouched.

The effect-only `ACOUSTICS_MASTER` contains nine shared prototypes and no hardware/world geometry. Both consumers relatively link the same master data and one actual T44 assembly. Direct BHA v006 migrated to accepted v007; nested v006/ECCO/environment remain unchanged. Canonical 12 m continuation and joint inherit existing hardware placement/travel/spin. Source 2.400 m +X geometry and three one-plane/120° sensor references remain unscaled.

Bounded acoustic revision propagation is recorded through v001→v002→v003. Camera/timing/local motion survive the shared relinks and T44 migration. Actual far-rim testing subsequently found the uphole-facing B view exposed the finite continuation endpoint; a separately documented B v010 camera-only reversal fixes this, preserving the predecessor and all other motion/timing. The two final views remain distinct.

The sampler derives the visible retained temporary-cap exit exactly 2 mm ahead of the inherited reference. It preserves reference identity/local coordinates and records reference/exit poses plus actual cap object/library/version/hash/offset. This is a provisional source-derived graphical exit convention, not a newly certified transducer datum. Missing/ambiguous caps raise; no implicit reference fallback remains.

## Packet and native checks

Common send/contact/receive times are explicitly the leading front. Three fronts lag 0, 0.07 and 0.14 s; per-front phases and packet intervals are exported. The actual cap stays fixed through the last return at receive_s + 0.14 s. Timing is illustrative, never calibrated acoustic speed or firing cadence. No mud-sensor coordinate is invented.

[Fresh-open verification](Evidence/native-verification_v010.json) passes {len(native['checks'])} scene/source checks plus {sum(len(p['checks']) for p in native['packets'])} per-event packet checks. It checks each of the three fronts in each direction separately: native source/contact/return positions and visibility, nondegenerate progression, finite curve envelopes within the first wall/outside the cap plane, and actual cap/reference hold through the trailing return. Actual cap/wall source hashes, face identity and native offset are re-sampled. Saved location channels cover hidden endpoints; evaluated world matrices cover visible fronts, avoiding Blender's stale hidden-matrix diagnostic.

Additional checks cover one ECCO/extension/joint, unchanged predecessor/source hashes, relative actual nested dependencies, linked shader surfaces, sensor geometry, world-fixed samples, actual sender/contact sightlines and finite acoustic clearance from the new continuation. [Finite-rim coverage](Evidence/extension-visibility_v010.json) checks rim vertices and end-face centres over all 96/108 frames; both final rims are behind/outside the camera, with zero projected samples. These are executor self-checks. The public `acoustic_verify_v002.verify_packet` also supports actual combined/cased consumers; final stage compatibility and an independent exact-candidate verdict remain T45 responsibilities.

## Render and media evidence

T45 serialized all render grants. Current three sample plus ten representative/peak benchmark calls passed {min(bench):.3f}–{max(bench):.3f} s. The 96-frame batch also passed; all {len(rows)} current measured calls were {min(times):.3f}–{max(times):.3f} s, each strictly below 5 s. Measurements wrap complete render-to-written-file calls, including initialization and output writing, without a hidden warmup render. Profile: 1280×720, 24 fps, EEVEE16, Vulkan, AgX Medium High Contrast, compositor disabled, normal existing GPU disk caches. T44's empty-cache initialization 12.55–25.13 s remains unresolved; no universal cold-machine compliance is claimed.

[Media verification](Evidence/media-verification_v002.json): full H.264 decode without errors, all {media['decoded_frames']} frames have correct size and nonblank content; {media['distinct_decoded_frame_hashes']} distinct decoded hashes. Executor inspected current source/send/contact/return/cue and 24 chronological decoded frames. T45 inspected the three full-size current arc samples. This does not establish narrated cold-viewer comprehension, engineering approval or client acceptance.

## Preserved diagnostics and limits

Earlier consumers/images remain local: shifted library paths in v002/v003, formation/source occlusion, edge-on thick-arc v006, B v009 finite-rim exposure, and the hidden-matrix verification diagnostic. Current successors resolve the affected claims; failure evidence is preserved and excluded from selected review stills. The previous hold handoff/report remains historical evidence of the upstream pause, now resolved by the accepted T44 release.

No calibrated acoustics, bond/thickness estimate, field output, physical simulation, engineering certification or final film acceptance is claimed. The minimal `Echo arrival` graphic says `Schematic timing`, uses no invented values, and retains editable installed Segoe UI without redistributing the font. Radzi owns narration/editing/client communication and assembly.

## Integration and next action

Builder edits are confined to `Shared/Assets/Acoustics/` and `Records/Tasks/T-046/`. No Git/global manifest/live Blender changes occurred. Native/video and new raw/decoded Frames media are ignored; selected Review PNGs plus exact text/scripts/JSON are listed in [allowed-tracked_v002.json](allowed-tracked_v002.json). Historical diagnostic PNGs remain local and excluded from that allow-list.

The run returns waiting for T45 to inspect the exact stills/playable demo, integrate only the allow-list, verify the pushed commit, and obtain fresh independent verification against that SHA and these native hashes. Only then submit T46 to Review with pinned links. No Review or human acceptance is asserted here.
'''
(T/'report.md').write_text(text,encoding='utf-8')
allowed=[]
for root in [A,T]:
 for p in root.rglob('*'):
  if p.is_file() and p.suffix.lower() in ['.md','.py','.json'] and 'Previews' not in p.parts:allowed.append(p.relative_to(ROOT).as_posix())
for p in (T/'Previews').glob('Review_*_v002.png'):allowed.append(p.relative_to(ROOT).as_posix())
allowed.append((T/'allowed-tracked_v002.json').relative_to(ROOT).as_posix())
(T/'allowed-tracked_v002.json').write_text(json.dumps(dict(task='T46',status='waiting_master_integration_and_independent_verdict',paths=sorted(set(allowed)),excluded='All native/video/cache/raw or decoded Frames and historical diagnostic PNGs; builder performed no Git mutation.'),indent=2),encoding='utf-8')
print(json.dumps(dict(report='report.md',allowed_count=len(set(allowed)),all_current_render_calls=len(rows),seconds=[min(times),max(times)]),indent=2))
