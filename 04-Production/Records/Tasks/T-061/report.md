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
