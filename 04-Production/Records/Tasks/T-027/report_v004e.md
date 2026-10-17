# T27 / B202-M — bounded v004 revision for D2/D3 re-review

**17 October 2026 · Candidate v004e · T27 remains IN PROGRESS.** Revised cheap proof requested in discussion `b94637dc-0785-4585-92f4-967b433bdda2`; full sequence and visual/engineering acceptance remain pending. [Previous v003 report](report_v003.md) and all prior assets are preserved.

Task `486a2a68-c921-4f2d-9323-5115a6f9340a`; worker `codex-b202m-20261016`; new run `762b45f1-4edd-485f-acce-74db90020f20`. Current discussion and fresh handoff read before restart. Prior waiting run expired and the connector marked it failed; fresh claim succeeded. T8 remains Done, standard v2 current. Base `f474e46b19360aab2e5c35da2072bb800d3d7c12`.

## Exact review outputs

- [Playable revised proof v004e](../../../Mechanisms/B202/Previews/MotionProof_v004e/B202-M_motion-proof_v004e.mp4): 14 seconds / 336 frames / 24 fps / 960×540.
- [Entry/contact/ring/release/payoff sheet](../../../Mechanisms/B202/Previews/MotionProof_v004e/B202-M_review-sheet_v004e.jpg).
- [Local review player](../../../Mechanisms/B202/Previews/MotionProof_v004e/review_v004e.html).
- [Editable Blender v004e](../../../Mechanisms/B202/Scenes/B202-M_motion-proof_v004e.blend).
- [Single direction contract §9: revised camera/event score](../../../Mechanisms/B202/B202-M_scene-direction_v001.md).
- [Replay manifest/all event receipt IDs](Evidence/replay_manifest_v004e.json), [saved-scene checks](Evidence/verification_motion-proof_v004e.json), [encoded playback/output hashes](Evidence/playback_qa_v004e.json).

Root `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. All outputs organized under `04-Production`. Blender/video/raw frames are local ignored media, not uploaded or backed up by Git. Reports/scripts/evidence and selected permitted images are synchronized; exact commit and pinned report links are attached to Rolladice after remote verification. No restricted ENP1 imagery.

## Response to the critique

| v003 problem | Bounded revision | Remaining visual judgment |
|---|---|---|
| Floating flat patch; enclosure unclear | Continuous solid-rock cutaway with unchanged T6 inner wall, authored exterior and sealed cut faces. Actual annulus macro pulls out to enclosing context. | Does the true-scale interaction and transition read in playback? |
| Outline looks attached/decorative | World-fixed event points and coverage-limited contour persist as tool transfers; camera initially follows then anchors to the well. | Is acquisition causality immediately understood? |
| Two stations form only a short sleeve | All 13 source stations reconstruct three metres; camera holds while ECCO moves onward. Source white nominal references clarify subtle deviation. | Does the unexaggerated irregular volume communicate a measured borehole? |

**All 4,212 v009 events are merely retimed; none regenerated.** Original values/IDs/poses and masks remain. Three sensor events per orientation are grouped for display. Four-frame transfers pause acquisition; eleven-frame station rotations are explicitly compressed replay, not ENP3 cadence. Fourteen seconds gives opening, ring, depth accumulation and final release room to read. Tight/spiral and separate amplitude stay outside this bounded proof.

Geometry uses v009 measurement-only inverse, conservative completed-bin readiness and fixed scales. Physical rock is context only; its coordinates never feed reconstruction. Authored .68 m outer mass/cut faces are presentation dimensions; actual inner borehole/tool are unchanged. Rock fading is a data-presentation cutaway transition, not physical disappearance. White is nominal size, not acquired samples or a gauge bit. Point glyphs shrink near payoff without changing positions. Ten-microsecond cutoff bias handles float32 over the full 42-second source timeline, far below source 10 ms spacing.

## Validation and preservation

**1,744 fresh-open checks pass**, including original indexed raw-event content hash, 4,212 source IDs, three sensors/same-sensor reception, native hashes, unchanged T6 inner vertices, sealed/manifold cutaway, fixed inverse points, exact per-frame receipt membership, coverage-limited contours, no future averages, independent channels, no acquisition during transfers, three-metre final span and camera release. These are agent synthetic checks, not acoustic certification or visual acceptance. **All 336 encoded frames decode**, at 24 fps / 14.0 seconds / 960×540. Entry, contact, ring, depth and payoff frames and the sequential sheet were visually inspected; D2/D3 viewer comprehension remains pending.

T5 v002, T6 v003, v009 master and v003 candidate hashes match. T7 untouched. Official Blender was initially off; after Radzi enabled it, MCP connected to a clean unsaved scene and opened the saved revision for local viewing. Separate background processes rendered/verified it; no unrelated live scene was replaced.

Local v004/a–d composition/debug candidates and useful logs remain. Testing caught float32 rounding above source time 32 seconds; v004e corrects cutoff and reruns checks. Source irregularity stays subtle rather than stretched. Actual acoustic-face/datum, calibration, processing and sampling remain MIT questions. No telemetry/field-data claims.

## Re-review and next action

Judge the moving revision: **does the enclosing borehole read, do readings visibly remain behind as ECCO advances, and does the release reveal meaningful shape through depth?** These remain D2/D3 judgments. Discussion requests this bounded proof before full expansion. No approval is inferred from checks. T27 stays in progress, run waiting for targeted feedback after synchronization.

Implementation: [build](../../../Mechanisms/B202/Scripts/build_motion_proof_v004e.py), [verify](../../../Mechanisms/B202/Scripts/verify_motion_proof_v004e.py), [encode/decode/package](../../../Mechanisms/B202/Scripts/package_motion_proof_v004e.py). Build refuses native overwrite; use a fresh version/path for rebuilding. Blender 5.2.2 and bundled Python/Pillow/numpy were used. Updated runtime lacked imageio_ffmpeg, so version 0.6.0 was restored from a cached wheel into the task-specific user cache `.cache/codex-b202m-deps`; bundled/shared Python was not changed. Package script contains the fallback import. Continue from exact v004e after feedback. Full B202-M still needs accepted explanation, independent amplitude/cases and complete moving validation; only Radzi accepts Done.
