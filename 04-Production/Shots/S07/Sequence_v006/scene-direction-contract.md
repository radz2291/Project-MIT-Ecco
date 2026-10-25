# S07 v006 — stronger third-shot pullback

Owner feedback: v005 is very good; add the emotional near-to-far pullback immediately before the final establishment. Preserve shots 1 and 2, three-shot structure, moving starts, logo removal and final fade. This scoped amendment changes only frames 121–192.

| Frames | Direction |
|---|---|
| 1–60 | v005 shot 1, unchanged native camera and rendered images. |
| 61–120 | v005 shot 2, unchanged native camera and rendered images. |
| 121–128 | Third shot cuts to a larger, diagonally framed partial product. Camera already retreats with constant velocity; no ease-in. |
| 129–156 | Continue the strong retreat, progressively braking into the full-product composition. |
| 156–192 | Subtle continuing drift keeps the established view alive. Final fade remains 164–190, then black. |

Meaning: give the instrument visual weight in the foreground, then reveal its complete form with a decisive change of scale. AI Director guidance is applied through active retreat and controlled settling. Camera motion only; actual product remains stationary. Third-shot entry remains a different viewpoint and scale from shot 2's endpoint.

Implementation: same v005 source scene. Straight camera retreat along the final hero sightline. First eight frames linear; a Hermite segment smoothly reduces speed into a gentle linear drift. The camera begins at 0.34 of the reference viewing distance, reaches 1.03 by f156 and 1.07 at f192. These are framing controls, not engineering measurements. Roll progresses from -42 to -48 degrees. Retain source geometry, scale, materials, lighting, lens and black ending. No branding.

Verify first 120 camera records, evaluated poses and rendered images against v005; source geometry and all hardware transforms unchanged; positive camera clearance; moving linear third-shot entry; monotonic retreat; final slow drift; centered whole-product bounds; clean cuts, media decode and saved native dependencies. Benchmark revised frames below five seconds each before rendering. Return for owner review; no new whole-sequence or client approval inferred.
