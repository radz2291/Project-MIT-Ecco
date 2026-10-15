# Preview settings — proposal v001

15 October 2026 · T-004 · Pending Radzi confirmation. No existing Blender scene was changed.

| Setting | Proposed convention | Status / reason |
|---|---|---|
| Working canvas | 1920 × 1080, 16:9, square pixels | Proposal for readable technical graphics; final delivery resolution remains O02. |
| Review playblast | 1280 × 720, 100% output scale | Proposal for light review files. Inspect small labels at 1080p if needed. |
| Frame rate | 24 fps, fps_base 1.0, constant frame rate | Proposal consistent with A02's inspected first-ping and source-imported records; not a delivery agreement. |
| Master timeline | 90 seconds; frames 1–2160 inclusive | Commercial duration confirmed by final QTE-MIT-003 via T-001. Frame count depends on proposed 24 fps. |
| Shot timeline | Local frame 1; inclusive end = duration × 24 | Record master in/out separately; handles excluded from the assembled duration. |
| Review video | MP4, H.264, yuv420p, constant 24 fps, CRF 20 target | Proposed encoder convention, no size promise. Silent until sound is intentionally included; record audio explicitly. |
| Inspection frames | PNG at first, key event and last frames | Same saved scene/version as video. Record exact frame indices. |
| Mechanical shading | Workbench/grayscale, with meaningful semantic colors | Pinned roadmap v2; preserve data distinctions and legibility. |
| Review identification | Task/shot, version, frame/time and “technical preview” | Use restrained review metadata outside critical content; illustrative signals/flows labeled. |
| Final finishing/delivery | Separate confirmed profile after technical lock | No final codec, color, audio or compressed-file size agreed here. |

## Proposed assembly frame allocation

From the [canonical narrative allocation](../../03-Context/01_Foundation/04-STORYBOARD_AND_SHOT_PLAN.md). These are section budgets, not camera shots or approved event timing. At 24 fps, time zero is the start of frame 1; frame 2160 ends at 90 seconds. Adjacent sections have no overlap or gaps. Transitions consume the existing budget; do not add duration by appending handles.

| Section | Seconds [start, end) | Master frames inclusive | Count |
|---|---|---|---:|
| S01 | 0–10 | 1–240 | 240 |
| S02 | 10–22 | 241–528 | 288 |
| S03 | 22–40 | 529–960 | 432 |
| S04 | 40–58 | 961–1392 | 432 |
| S05 | 58–70 | 1393–1680 | 288 |
| S06 | 70–82 | 1681–1968 | 288 |
| S07 | 82–90 | 1969–2160 | 192 |

## Repeatable export and review

Save the versioned source before export. Record Blender version, engine, actual resolution, fps/fps_base, inclusive range, output path, elapsed render/export time and source/script hashes. Check the encoded stream's dimensions, rate, frame count and duration; view boundaries and each causal event, then watch the complete preview. Record checks actually performed, failed attempts and limitations. Compare the saved candidate to its preview after any move or link change. A metadata pass alone is not visual QA.

Keep exact graphics editable; preserve masters and relative library links. [Conventions audit](Tasks/T-004/conventions-audit_v001.md) owns proposed naming/path examples; [first handoff](Tasks/T-004/first-execution-handoff_v001.md) owns the bounded next step. No preview, render duration or export success is claimed by this records-only task.

## Human confirmation

Radzi: confirm or revise the 1080p working canvas, 720p review profile and 24 fps convention. The 90-second total is already commercially established; section allocation remains provisional. Acceptance of this internal profile does not resolve final delivery O02, technical interpretation or rights.
