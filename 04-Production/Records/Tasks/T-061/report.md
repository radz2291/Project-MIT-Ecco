# ECCO-061 · Section 6 opening preview

12 November 2026

The source is the owner-approved `04-Production/Studies/S06_Report-Recreation_v004/Scenes/S06_cinematic-study_v004_polished.blend`. Its native SHA-256 `7f2a0086992be7c12c0896505d6fafbc42d82c7967a89ef9686f885bb06374a3` and movie SHA-256 `b1af840ef30a7862b31801b1b12c360487412bd60b20b6e5ab449dd5a3de13fe` match the recorded approval.

## Shared production copy

The local native is `04-Production/Shots/S06/Scenes/S06_shared-reconstruction_v005.blend`, SHA-256 `7eb6f378a54048affd2cc0d86f3d767317108d8f22aad1dd8869555cb9a75ba0`.

- The T-054 S06 integration was recovered against the exact polished v004 baseline. Three relocated library references were repaired in the new copy. The shared context uses the pinned World v010 cutaway, Digital style v001 and the local stage fade. The display is visible in the opening and hidden for the report. The pinned World preserves the approved framing and the geometry used in the prior integration.
- Shared ECCO v003 supplies the housing and nine closures with identical source geometry. The linked satin finish uses the existing S06 shader visibility controls.
- The linked fine-contour group in Measurement reveal v001 is used on 33 animated opening guide paths. Local guide width, color and fade are retained. The local indexed dots, authored reveal timing, stored illustrative geometry, independent amplitude data and report imagery remain section-owned.
- All 288 camera and sampled shape-key states matched the approved previs. The five checked reconstruction and sample meshes matched in coordinates, topology and selected data attributes. All nine text bodies matched. The local dataset pointer resolves to the approved study. [Integration evidence](../../../Shots/S06/Notes/v005-integration.json)

## Opening motion proof

The local MP4 is `04-Production/Shots/S06/Previews/S06_shared-reconstruction_v005_opening.mp4`, SHA-256 `a877e43d9934b0505909d412c673a81f2281a28cfa7fb15e321210ad9340ced2`. Frames 1–96 are the first four seconds of the 12-second section, with the establishing view, depthwise sample build and the beginning of the surface opening. All 96 frames decoded at 960 × 540 and 24 fps. Encoded frames 1, 24, 52, 72, 88 and 96 were visually inspected. The local sheet is `04-Production/Shots/S06/Previews/S06_shared-reconstruction_v005_decoded-check.png`.

The opening preview used Vulkan EEVEE, eight samples and the existing compositor. An initial benchmark at frame 96 took 7.606 seconds. The batch waited for warmup at the opening, reveal and transition. The nine repeated benchmark frames peaked at 3.554 seconds. The 96 preview frames averaged 1.414 seconds and peaked at 3.766 seconds with no retries. All six relative libraries resolve on reopen. Shared context opacity matches the original rock at eleven sampled frames, and the caps follow the original steel fade at those same frames. [Preview timings and decode](../../../Shots/S06/Notes/v005-preview-delivery.json)

The complete production timeline is in the native. The short motion proof is ready for owner feedback before the full render. Native and video remain local, with off-machine backup unverified.

## Opening camera revision v007

Radzi requested cleaner composition and smoother movement after reviewing the v005 opening. The first review showed the reconstructed tube crossing the top of frame and a rapid acceleration into the opening surface. v007 shows the complete tube in the wider opening, then pulls back and turns gradually toward the unfolding. The first framing trial, v006, still cropped the mid-reveal and was stopped. v007 gives that beat additional distance and keeps the projected tube in frame at all nine review samples through frame 132.

Only camera position and rotation on frames 1–124 were edited. The original camera matches exactly from frame 125 through 288, and the lens matches throughout. The maximum frame-to-frame travel fell from 0.1454 m to 0.1010 m. The maximum frame-to-frame turn fell from 1.817° to 0.960°. The local editable scene is `04-Production/Shots/S06/Scenes/S06_camera-polish_v007.blend`, SHA-256 `380ab8db417a9831a0b828830bef5d687dbced0dbd0acb79a48920cb4aa40469`. The reconstruction, its shared links and the laptop sequence carry forward. [Camera comparison](../../../Shots/S06/Notes/v007-camera.json)

The local motion proof is `04-Production/Shots/S06/Previews/S06_camera-polish_v007_opening.mp4`, SHA-256 `ec79950f20c34df0e3bef95995680032cabad93ccb82f5c104a22d9715801cbf`. All 132 frames decoded at 960 × 540 and 24 fps, for 5.5 seconds. Encoded frames 1, 52, 76, 96, 112 and 132 were inspected, covering the wider establishing composition, the scan build and the early unfolding. The nine warmed benchmarks peaked at 3.632 seconds. All 132 production frames rendered below five seconds, with a 4.007-second peak and zero retries. [Preview verification](../../../Shots/S06/Notes/v007-preview-delivery.json)

## Close opening with light camera polish v008

Radzi preferred the original close product composition with a gentle swipe and ongoing movement. v008 starts from v005. A small offset of 0.133 m at frame 1 creates a tracking move along the product and settles into the original path. A restrained smoothing pass eases the pullback into the unfolding. The peak frame-to-frame travel falls from 0.1454 m to 0.1232 m and the peak turn falls from 1.817° to 1.636°. The lens and timing match v005, and the camera matches exactly from frame 125 onward.

The local native is `04-Production/Shots/S06/Scenes/S06_close-swipe_v008.blend`, SHA-256 `a496390e3ab559222492fe479b842c078180bbb8bed3d4a10adf6a5b8ebd8934`. Only the opening camera's position and rotation were edited. The saved scene reopened with six relative libraries resolved and the 12-second timeline intact. [Camera checks](../../../Shots/S06/Notes/v008-camera.json)

The 5.5-second proof is `04-Production/Shots/S06/Previews/S06_close-swipe_v008_opening.mp4`, SHA-256 `951c3ecfcb5bbd60b1c6a4f0751f3a5c44724746fce08a560fd98e32094f71e0`. All 132 frames decoded at 960 × 540 and 24 fps. Encoded frames 1, 25, 52, 76, 96 and 132 were visually inspected. The nine accepted benchmark frames peaked at 4.849 seconds, and the accepted production frames peaked at 4.384 seconds. Two attempts above the cap were discarded and rerendered, one during benchmarking and one during production. [Preview verification](../../../Shots/S06/Notes/v008-preview-delivery.json)

## Overlap the pullback and grid reveal v009

Radzi asked for the grid to build as the camera pulls back from the close view. v009 preserves the v008 first frame and advances the pullback on the existing path. The guide fade runs from frames 10–70. At frame 42, the camera has moved 0.542 m from the opening pose and the guide fade is at 56%. By frame 64 the camera has moved 2.038 m and the grid is almost fully visible. The indexed dots, shape-key timing and laptop handoff remain on their original frames.

The local editable scene is `04-Production/Shots/S06/Scenes/S06_overlapped-reveal_v009.blend`, SHA-256 `58e00061dcc51c68bde2a9adde0563f43069ad9ecc3d7d2dc63966b1c266edac`. Lens and shifts match v008 across all 288 frames. The camera matches v008 from frame 125, and the later grid fade matches from frame 81. All six libraries resolve in the reopened native. [Timing and join checks](../../../Shots/S06/Notes/v009-overlap.json)

The 5.5-second local MP4 is `04-Production/Shots/S06/Previews/S06_overlapped-reveal_v009_opening.mp4`, SHA-256 `a7cf6a3628bf961b2a77be22cb115ec70e5ed5e539dc935a7d5f53a6588ce221`. All 132 frames decoded at 960 × 540 and 24 fps. Encoded samples at frames 1, 21, 42, 52, 70 and 132 cover the close opening, overlap and unfold. The nine accepted benchmark frames peaked at 4.422 seconds after two over-cap benchmark attempts were discarded. All 132 production frames rendered below the cap, with a 4.656-second maximum. [Preview verification](../../../Shots/S06/Notes/v009-preview-delivery.json)

## Direct opening camera sweep v010

Radzi's sketch specifies one continuous sweep from the close view into the unfolding view. v010 uses one cubic path for position and a continuous rotation curve across frames 1–144. Frame 1 matches the v009 close view exactly. The move progresses toward its destination on every frame and joins the existing camera at frame 145 with matching travel and turn. The grid still appears during frames 10–70. The lens, shared assets and data timing carry forward.

The local scene is `04-Production/Shots/S06/Scenes/S06_direct-sweep_v010.blend`, SHA-256 `d1efd95312c343fbbc3aaa1d94c09051d7f1816302fc19b7fb45a4157f35599b`. The reopened native retains the 12-second timeline and resolves six relative libraries. The camera matches v009 at frames 145–288. Travel across the join is 34.88 mm into frame 145 and 34.78 mm out of it. [Path and join verification](../../../Shots/S06/Notes/v010-direct-sweep.json)

The local 6.25-second MP4 is `04-Production/Shots/S06/Previews/S06_direct-sweep_v010_opening.mp4`, SHA-256 `fd162d3259bdbc212189c7e27fa6ec1df1a595b71ae1e82bdd3b9e47f21f70d1`. All 150 frames decoded at 960 × 540 and 24 fps. Encoded frames 1, 25, 48, 70, 90, 110, 132, 145 and 150 were visually inspected. The eleven warmed benchmark frames peaked at 3.463 seconds, and all 150 production frames passed with a 3.840-second maximum. [Preview verification](../../../Shots/S06/Notes/v010-preview-delivery.json)
