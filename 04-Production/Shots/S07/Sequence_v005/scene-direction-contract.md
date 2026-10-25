# S07 v005 — v002-based three-shot edit

Direct owner instruction: return to the preferred v002, break it into three shots, begin each shot with linear camera movement already underway, keep shot 2's end composition different from shot 3's start, and retain removal of the logo. This supersedes the continuous-take requirement. Final centered product and fade to black remain in scope.

AI Director application: use the two established detail arrivals and a clear scale change into the full-product view. A continuous visual story is achieved through framing, consistent lighting, subject and editorial rhythm; this version deliberately contains two cuts. Actual hardware remains stationary. No new operation, dimensions or product features are introduced.

| Shot | Frames / local time | Image and movement |
|---|---|---|
| A | 1–60 / 0–2.5 s | Open directly on the product, using the v002 initial angle. Straight, constant-speed camera translation through the shoulder/pad detail. No opening fade or ease-in. |
| B | 61–120 / 2.5–5 s | Cut to the v002 reverse three-quarter beauty. Constant-speed close glide; remain close through frame 120. No retreat into the next shot's composition. |
| C | 121–192 / 5–8 s | Cut to the whole centered instrument. The camera is already translating backward at constant speed. Continue moving through the final fade rather than stopping at a static pose. |

Frames 164–190 fade the whole image to black; 190–192 finish black. All closing text is removed. The owner adds the logo afterward as a separate frame. S07 no longer includes the S06 laptop dissolve: the boundary preview demonstrates a direct edit from approved S06 into moving product imagery. S06 itself is untouched.

Implementation: one native camera, frame-baked look target and orientation, linear camera translation within each range, constant interpolation on frames 60 and 120 to make hard cuts at 61 and 121. Three independent MP4 exports accompany the complete edit. Lens 55 mm and original source dimensions/materials/light rig retained. Camera transforms and exact beat endpoints are in Records/shot-definitions.json and camera-score.json. All previous source/engineering limitations from v001 carry forward.

Verification: benchmark first; every complete frame under five seconds. Check exact source geometry and stationary matrices, native dependencies, nonzero and constant per-frame camera displacement within each shot, hard-cut interpolation, no opening fade, distinct projected scale between frames 120 and 121, centered full-product bounds throughout sampled wide frames, final black and all video decodes. Inspect cut-adjacent frames and timed previews. Owner review pending; no client or engineering acceptance implied.
