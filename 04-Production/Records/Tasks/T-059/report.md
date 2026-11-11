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
