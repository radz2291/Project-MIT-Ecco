# ECCO-059 · S04 first playback

Ticket `de1854fe-e7b0-4d53-9b45-bb1f0bb0e124`. Radzi assigned ECCO-059 on 12 November 2026. ECCO-058 was Done at claim. Sync branch starts from `c8bf91a6a0c3c7c83c13a4ed446ec19a09f128f0`.

## Working files

Paths are relative to `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. The native and videos are local. Off-machine backup is unverified.

| File | Path | SHA-256 |
| --- | --- | --- |
| Selected v033 native | `04-Production/Shots/Archieve/S04/S04-A/Previs_v033/Scenes/S04_continuous_ABCD_v033.blend` | `018f65027ab9f190709085bcaf103edf10dc565bc49ab2c76d0dad79675ec77f` |
| Selected v033 movie | `04-Production/Shots/Archieve/S04/S04-A/Previs_v033/Previews/S04_continuous_ABCD_v033.mp4` | `2587e99921f59dec9b6e4fb637a7f1021665623e9614ecc98a11ba62a152dfa2` |
| Open production copy | `04-Production/Shots/S04/Scenes/S04_continuous_relinked_v035.blend` | `934f41bd817e86a38744222a607f6774f142243c6fd95c3775b6d35699084918` |
| First playback | `04-Production/Shots/S04/Previews/S04_response-comparison_v035.mp4` | `46de127d94dc52a340d05398758f266a66a2dd66a59df32422b7dae5c137fb33` |

## Source and recovery

The archived native and MP4 match the v033 delivery hashes. The owner selected v033 over v034 and left the dark band in the wear shot open. The S04-A through D contracts and V3 board cards supply the story and interpretation. Later owner direction gives priority to the continuous camera version. Shared waveform v021 is a reference for a future test.

Blender 5.2.3 opened a staging copy with the seven original-version libraries placed at the original relative locations using local hardlinks. [The recovery script](../../../Shots/S04/Scripts/recover_v035.py) saved v035 with relative library paths, render output at `//../Cache/v035/S04_`, and the opening playhead at frame 85. The script reopened v035 and confirmed seven links, zero missing datablocks, one camera, frames 1–432 at 24 fps, 465 scene objects and identical steel mesh and computed wear depth. At 15 frames, camera and sensor transforms, lens, acquisition front and sampled effect states matched the staged v033. The verified copy then opened in desktop Blender. The configured official MCP executable is absent after the restore, so the checks used Blender directly.

The old D: recovery cache was unavailable on this machine. The new cache resolved on C: with approximately 282 GB free. This checkpoint used the original rendered frames. The current renderer has yet to be timed at the export profile. Benchmark representative and heavy frames below 5 seconds per frame before a new full batch.

## First playback and owner decision

The comparison uses source frames 69–116 and 182–229 at full 1280 × 720. [The encoding script](../../../Shots/S04/Scripts/compare_responses_v035.ps1) concatenates them at 24 fps. All 96 frames decoded. Sampled frames show the labels, matched close framing, outgoing fronts and returning fronts in both cases. The blue backing region is easier to see than the short returning pulse. The graphic and geometry are illustrative.

The evaluated `ECCO_SENSOR_REF_01` local +Z ray hits the actual inner steel mesh in both cases, 29.859 mm from the recess-centre marker. The hit is approximately (-0.320, 0.12346, 0.09997) m in the supported case and (-1.500, 0.12346, 0.09997) m in the reduced-support case. The marker is an authored reference and the acoustic face remains unconfirmed. The send graphics are visible at frames 78 and 191, and echo graphics at 85 and 198. Exact graphic endpoint coincidence and return completion need a focused check in the next motion test.

Radzi confirmed on 12 November that the original previs animation is fine for the whole section. Preserve v033 response timing, camera crossing, and wear-reveal animation. Waveform v021 was consulted as a reference. The initial comparison and v035 use the v033 effects. The previously noted dark band remains a look question if Radzi asks to revisit it. The ticket remains open for directed production work or wrap. Radzi owns film assembly and client delivery.

## Intro-only proof v036 · 12 November 2026

Radzi authorized the v005 tool entry, shared ECCO and the approved S02 signal at the first sensor view. The output is a 6.375-second proof from a separate native. The v035 full-sequence hash still matches the baseline in the table above.

- Local native: `04-Production/Shots/S04/Scenes/S04_entry-first-sensor_v036.blend`, SHA-256 `7c67540ce6851683b11f2fb0c1b89e359e982d42a19bce0e7de9a367e16b7e89`.
- Local preview: `04-Production/Shots/S04/Previews/S04_entry-first-sensor_v036.mp4`, SHA-256 `2e2d1deeac912f01d9b5ef12d8c762a61ff17ad5cf1627651abd5e1e6fb7d596`.
- The v005 travel and the shared BHA v008 / ECCO v003 sensor pose match at frames 1, 49, 73 and 97. The first view eases to an oblique angle and uses an adjusted viewing mask so the sensor and impact area can be read together. The BHA is held at the v005 first response position through frame 153.
- The waveform links v021. The ray runs 27.859 mm from the shared cap to the inner steel. Approved timing, send and echo colors and contact patch are retained. The shot fits the response tiles to the curved casing and uses a 1.35 radius multiplier for screen readability. Echo completes at frame 146. [Placement evidence](../../../Shots/S04/Notes/v036-intro-placement.json).
- The saved v036 reopened with all ten relative library links resolving. The first cold EEVEE render with an empty shader cache took 37.527 seconds. With shaders initialized, ten benchmark frames peaked at 2.003 seconds. The 153-frame render at 960 × 540, 24 fps, EEVEE eight samples averaged 1.015 seconds and peaked at 2.259 seconds per frame. All 153 encoded frames decoded. Samples verified entry, sensor arrival, casing response and violet echo. The render cache is under `04-Production/Shots/S04/Cache/v036`.
- No new edit into the full sequence was made. The intro preview is ready for Radzi's feedback. Native, cache and video are local. Off-machine backup is unverified.

## Camera-only v037 · 12 November 2026

Radzi directed a return to the selected S04 previs and limited the revision to the opening camera move. v037 supersedes the v036 proof for review. It starts from v035 and changes only camera location and quaternion keys in frames 1–62. v005 camera score frames 1–92 supply the opening approach, fitted to the existing cutaway and timing. The 18-second scene retains the original tool travel, lens animation, signals, materials, lighting, crossing and wear.

- Full editable candidate: `04-Production/Shots/S04/Scenes/S04_continuous-opening-camera_v037.blend`, SHA-256 `1a74e9804305513213591ed674843a03cb599e4a90ad65931698ba5590fd442b`.
- Local 4.833-second preview: `04-Production/Shots/S04/Previews/S04_opening-camera_v037.mp4`, SHA-256 `00422768feb4cb723d153aed084b6ae8d8d7fc79219e09672771859750b81da1`.
- All seven relative libraries resolve. The saved camera matches v035 exactly at 739 whole- and half-frame samples from frame 63 through frame 432. The camera moves 0.262 mm across the frame 62–63 join. The v035 native still matches its original SHA-256. [Native check](../../../Shots/S04/Notes/v037-opening-camera.json).
- The 960 × 540 preview joins 62 new opening frames to selected v033 frames 63–116. Seven timed benchmark frames peaked at 3.559 seconds. The actual 62-frame render averaged 2.511 seconds and peaked at 3.412 seconds after renderer setup. All 116 encoded frames decoded at 24 fps. Entry, frame 62–63 continuity and the first response were checked in the encode. Cache is local at `04-Production/Shots/S04/Cache/v037`.
- v037 awaits Radzi's feedback. Native and media are local. Off-machine backup is unverified.

## Shared ECCO v038 and prepared cement/ground · 12 November 2026

Radzi directed the ECCO v003 product upgrade and asked to check the prepared cement and ground. v038 starts from the v037 camera-only candidate. The product display uses the linked v003 housing, nine temporary closures, cutter, controls and sensor references. The active materials use the v003 satin shader with the existing S04 surface fade.

- Full native is `04-Production/Shots/S04/Scenes/S04_continuous-shared-ecco_v038.blend`, SHA-256 `7a04c4d541b91f2cb0dc9ac11d3f69a0121181f0b59e6e212566d4ec7322ebc1`.
- All eleven mesh comparisons matched vertex coordinates and polygon loop indices. Camera, cap, sensor pose, acquisition front and housing fade were checked at eleven frames covering the opening, both responses, crossing and D. Maximum hardware matrix-component difference was 1.94e-7. The D edge geometry stays registered to the matching mesh. All eight relative libraries resolve. [Native evidence](../../../Shots/S04/Notes/v038-shared-ecco.json).
- Prepared cement is in `04-Production/Shared/Assets/Environment/Borehole/Dependencies/CasedHole_v002.blend`. Prepared surrounding ground is in `04-Production/Shared/Assets/Environment/Borehole/Dependencies/Formation_cased-section_v002.blend`. Both files are available and linked. The visible v033-derived cutaway uses the existing shot-local cement around the casing, its outside channel, and its source-guided formation shell. v038 retains that presentation.
- Saved native was sampled in EEVEE at 960 × 540, eight samples. Casing entry, first response and wear stage stills are in `04-Production/Shots/S04/Previews`, with render-to-file times of 3.289, 1.868 and 1.165 seconds after setup. Native and previews are local. Off-machine backup is unverified.

## Shared BHA and cement/ground trial v039 · 12 November 2026

Radzi asked to use shared BHA v008 and try the prepared cement and ground. v039 carries the v008 linked satin-core meshes and both continuation components in the existing S04 animation. It retains the v003 ECCO product, the v037 camera, the established signals and the wear presentation.

- Full native is `04-Production/Shots/S04/Scenes/S04_continuous-shared-bha-environment_v039.blend`, SHA-256 `4f505012040683d5b6fde9f88377e04a014c63d0efdd906884aa4685466bbfc3`.
- All 126 core and both continuation meshes matched coordinates, polygon loop indices and material assignments. Sampled hardware world matrices, camera and acquisition front match v038 at ten frames. Ten relative libraries resolved after reopening. [Native evidence](../../../Shots/S04/Notes/v039-shared-bha-environment.json).
- The prepared `CASED_CEMENT` finish from CasedHole v002 and `FORMATION_CasedSection_v005` finish from Formation cased-section v002 are applied to the existing S04 cutaway meshes. The stock source meshes have different bounds. Keeping the S04 meshes preserves the window, channel, casing and coverage. Existing environment opacity was matched at seven frames, including the D transition.
- Rendered the casing entry, reduced-support response and wear stage at 960 × 540, EEVEE eight samples. Render-to-file times after setup were 3.403, 2.304 and 1.196 seconds. Stills are in `04-Production/Shots/S04/Previews`. This is the look trial for Radzi's feedback. Native and media are local. Off-machine backup is unverified.

## Shared waveform and complete render v040 · 12 November 2026

Radzi directed the shared S01–S02 waveform and a full S04 render. The existing glitch and impact remain part of the selected S04 presentation. v040 starts from v039 and changes the outgoing/returning signal only. The shared v021 field and controller drive both exchanges. The twelve superseded local send/echo curves are hidden. The existing 293 casing response objects retain their visibility, motion and material samples at 22 frames. Camera and sensor pose match v039 at the same frames.

- Full native is `04-Production/Shots/S04/Scenes/S04_continuous-shared-waveform_v040.blend`, SHA-256 `ae3e1df36ed1e0c74301d2f41b918c2c9937bb3d5802a8a0f12fc47eec894853`.
- Full playback is `04-Production/Shots/S04/Previews/S04_continuous-shared-waveform_v040_full.mp4`, SHA-256 `c9ba6f29dfa6230b2947ae1811b3575182a41b3281b6bd305d888c9a1b42ef34`.
- Both signals run 27.859 mm from the shared ECCO cap surface to the actual inner steel. The v021 style and launch frames 73 and 185 were retained. The shot-local speed is 4/3 to match leading arrival to the existing glitch at frames 82 and 194. The return tail arrives at 105.25 and 217.25, while each sensor holds position. Eleven relative links resolve. [Waveform checks](../../../Shots/S04/Notes/v040-shared-waveform.json).
- A 1280 × 720 trial exceeded the strict cap at the crossing. The 960 × 540 Vulkan EEVEE profile at eight samples passed 19 timed frames with 2.897 s maximum. All 432 production frames rendered under the cap, with 1.148 s mean, 4.713 s maximum and 495.968 s total render-to-file time after setup. Cache is local at `04-Production/Shots/S04/Cache/v040/full-vulkan-75`. [Delivery evidence](../../../Shots/S04/Notes/v040-full-delivery.json).
- All 432 encoded frames decoded at 24 fps across 18 seconds. Decoded samples covered entry, both cyan arrivals and violet returns, existing response graphics and labels, crossing and wear through frame 432. The native and video are local. Off-machine backup is unverified.

## Waveform readability proof v041 · 12 November 2026

Both shared v021 waveforms face the camera and use 2.1× amplitude and 1.45× line radius. The source and steel contact are fixed. Both original glitch impacts still begin at frames 82 and 194. The direction contract describes the reduced-support case as a longer illustrative ring-down. v041 expresses that with a 1.65× return train length in the reduced-support case. The return starts and its leading edge arrives at the same frames as v040. Its trailing edge now reaches the sensor at 221.64. The five overlapping legacy response-tail curves are hidden.

- Native is `04-Production/Shots/S04/Scenes/S04_waveform-readability_v041.blend`, SHA-256 `abdc5ea17f64ff37266ea4af2ade76a4149ce163d3ca948ca64cbba8e873fb23`.
- Review clip is `04-Production/Shots/S04/Previews/S04_waveform-readability_v041.mp4`, SHA-256 `953effb132ababf8f046bc5b99595729780b5066fa9d092cd17afc25ae314d61`. All 89 frames decoded at 960 × 540 and 24 fps. Contact and return samples were visually checked. The full rendered reference is v040.
- [Waveform verification](../../../Shots/S04/Notes/v041-waveform-readability.json). Native and media are local. Off-machine backup is unverified.

## Visible crest sync v042 · 12 November 2026

v042 advances both shared sends by 2.75 frames so the visible crest is 98.8% across the gap when the original glitch starts at frames 82 and 194. The v041 crest was only 69.3% across. The return delay compensates for the advance, preserving the v041 violet return timing. Glitch keys and the larger camera-facing style are retained. The saved native is `Scenes/S04_waveform-crest-sync_v042.blend` and the 69-frame, 24 fps proof is `Previews/S04_waveform-crest-sync_v042.mp4`, both under `04-Production/Shots/S04`. All proof frames decoded. Contact frames and their neighbors were visually sampled. [Measured timing](../../../Shots/S04/Notes/v042-crest-sync.json).
