# T7 — B201 pulse, echo and waveform proof v005

16 October 2026 · MIT ECCO · Task `fbe3e8c3-5ccf-4205-9aa4-48832b0d2cd3` · Run `afb55145-4014-4506-a084-a2192c1989bf` · Worker `codex-t007-20261016` · Reviewer Radzi.

Radzi authorized “Pls work on T7.” Fresh live ticket/handoff and roadmap standard revision 2 were checked; T5/T6 were Done. Initial checkout `main`, upstream `origin/main`, base `86437b95433bb1e9feb7edd084d2fa86e0e8532f`, remote `https://github.com/radz2291/Project-MIT-Ecco.git`; tracked and staged work initially clean. Parallel T9/T10 outputs were preserved. Radzi explicitly authorized Git coordination with those chats; T7 became the agreed sole integrator and synchronized task-owned sets in separate commits. This report's containing SHA is attached in Rolladice after a fresh remote verification.

## Result and exact review candidate

An 18-second moving mechanism proof shows three early isolated pings, then three additional pulse/echo events revealing waveform arrival intervals. Each outgoing signal reaches a fixed wall point, flashes briefly and returns to its own transmitting sensor. The whole product changes station between held acquisitions. Shorter/longer authored stand-offs produce shorter/longer diagram intervals on a common time scale; equal peak heights do not encode radius.

| Output | Storage / exact version |
|---|---|
| [Editable scene](../../../Mechanisms/B201/Scenes/B201_pulse-echo_v005.blend) | v005; local Git-ignored, exact SHA in build/manifest evidence |
| [Moving preview](../../../Mechanisms/B201/Previews/B201_pulse-echo_v005.mp4) | v005; 18.000s, 432 frames, 24fps, 1280×720, silent H.264/yuv420p; local Git-ignored |
| [Early ping still](../../../Mechanisms/B201/Previews/B201_review_f0021_v005.png) | Selected generated review image |
| [Completed comparison still](../../../Mechanisms/B201/Previews/B201_review_f0432_v005.png) | Selected generated review image |
| [Use and replacement guide](../../../Mechanisms/B201/README_v005.md) | Links, controls, interpretation and rebuild limits |
| [B206 question packet](review-questions_v005.md) | Origin, corrected stand-off explanation, pacing and waveform picking; feedback pending |
| [Scoped register](proof-register_v005.md) | Sources, information lifecycle, affected S02/B202 and unresolved interpretation |
| [Fresh-open verification](Evidence/verification_v005.json) | 86 checks pass; implementation self-check, not independent engineering validation |
| [Output manifest](Evidence/output-manifest_v005.json) | Exact sizes/hashes and local versus synchronized distinction |

All retained files are beneath `04-Production`. Machine-local root `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Local scene/video links are not remote downloads; Git synchronization of reports/scripts/evidence/selected stills does not back up Blender binaries, MP4 or bulk frames. No client communication, B202 execution, final finishing or human acceptance is implied.

## Inputs, construction and meaning

- Accepted T5 plugged v002, collection `ECCO_MASTER_v002`, SHA-256 `704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7`. External relative library; geometry, controls, closures and original files unchanged. Three inherited sensor references remain at 120° in source X=.73m plane. Only sensor 01 fires in this bounded proof.
- Accepted T6 well/assembly v003, SHA-256 `6bdacfefa6b999d941d0e2a93a75b26563be8e46141ee761114fdb81dae754c4`. Appended local consumer; irregular wall evaluated at illustrative world X2.8m and product translated +2.07m. Actual sampled intersections determine the wall contour and path lengths. No measured borehole geometry, depth or exact operating clearance claim.
- [Engineering Baseline](../../../../03-Context/01_Foundation/02-ENGINEERING_BASELINE.md), [S02 V2](../../../../03-Context/02_Storyboard/V2/ECCO_Section_02_Reveal_The_Principle_Padlet_v2/PADLET_SECTION_02_V2.md), [Decision Register](../../../../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md), [workflow](../../../../03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md), [information-provenance module 09](../../../../03-Context/03_Directorial_Identity/09-ENGINEERING_INFORMATION_DIRECTION_DISCOVERY.md) and production conventions were read. This B2 mechanism proof does not construct an actual S01–S07 shot.
- Source mesh is intersected with the sensor plane to make consumer-only 2D section contours. No internal components are invented. Direct planar contours replaced an invalid Boolean solid-cut attempt, identified by an OD-boundary check. The imported source has 13 nonmanifold/boundary edges; no source repair was performed.
- Origin is ray-inspected on the temporary cap, offset outward by an authored 0.4mm for visibility. It is explicitly provisional, not a calibrated transducer face. Rounded per-leg diagram duration is proportional to scene stand-off at a common authored speed (3mm/frame, never shown as physical sound speed); equal legs preserve round-trip meaning. Quantization error is at most half a diagram frame.
- The waveform is an illustrative transmit/echo glyph. A–C use the same time scale and same arbitrary heights; their echo marks arrive with their corresponding return event. The formula is symbolic `stand-off = c_mud × Δt / 2`; mud-speed correction and physical sensor offset/eccentricity caveats are visible. No numeric TOF/speed/frequency, calibrated amplitude, radius, lithology or field-log claim.

## Verification and preview QA

Official Blender MCP read-only access passed: Blender 5.2.2 LTS, clean default scene (3 objects). All execution used isolated background Blender to preserve the running user scene. Saved candidate fresh-opened successfully with relative T5 library resolution and matching accepted source hashes.

86 implementation checks pass: exact candidate hash; unchanged source hashes; library resolution; sensor spacing; section inside source OD; outgoing contact and same-emitter return endpoints on all six pings; positive stand-off; equal outbound/return diagram duration; common schematic speed within rounding; whole-tool rotation controls; inactive emitters absent; differing A–C arrivals; timeline/settings.

Final scene render: **47.483 seconds**, Workbench, 700×700 hardware layer, frames 1–432 at 24fps. Editable Python graphics compose to 1280×720 and encode H.264 CRF20/yuv420p. [Video QA](Evidence/video-qa_v005.json) records encode/graphics time and hash; [closure checks](Evidence/closure_v005.json) record the independently decoded frame count/rate/size/duration, hashes and local links. “Independently decoded” is a media integrity check, not independent scientific review.

All 432 motion states were visually inspected in eight ordered contact sheets; full-size key frames checked pulse/contact/return, boundaries and final comparative labels. Final graphics moved the first bracket to clear the sensor-offset caveat. No real-time playback inspection is claimed. Early pings precede traces; wall stays fixed; step rotations move the whole tool; signals stay outside hardware; labels preserve illustrative provenance. Technical review and taste acceptance remain Radzi/MIT's responsibility.

## Retained diagnostics and limitations

v001–v004 source scenes/scripts/logs remain local diagnostic history; they are not alternate deliverables. Initial camera clipping gave uncapped edges. Boolean trials produced a source complement outside tool OD and were rejected by verification; v005's exact plane-contour representation passes. Bulk trial frames and contact sheets remain locally organized; no restricted ENP1 field-log image or client commercial material was used or published.

O04 acoustic-face/time-zero/processing conventions remain material review questions. O05/O14 are not blanket holds under the 16 October production amendment. Step-and-hold stations and a dim reference wall prioritize B2 mechanism legibility, not final S02 cinematic pacing. Continuous scan/circumference/depth reconstruction and production camera direction are downstream work. Geometry or sensor edits require a new version/rebuilt paths and reverification; no automatic recalibration or zero-rework replacement is promised.

## Review and next action

Submit this exact candidate and [four targeted questions](review-questions_v005.md) for Radzi review/B206 communication. No feedback for v005 has yet been supplied; do not mark the human feedback loop accepted. Record returned feedback by source/date/version, implement authorized corrections, preserve evidence and reverify affected S02/B202 consumers. Only Radzi accepts reviewed work as Done.
