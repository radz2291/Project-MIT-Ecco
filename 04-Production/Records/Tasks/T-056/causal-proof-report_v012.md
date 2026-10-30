# ECCO-056 — Causal device-context waveform v012

Focused seven-second review proof, awaiting owner acceptance. The narrative is now visible in the actual device/wall context: the oval on the right emits a finite pulse toward the wall on the left; that exact wall location reacts; a smaller changed echo returns and enters the same oval; only after receipt does a wall measurement mark appear. Inactive gap regions are invisible.

## Timing

| Event | Review frames at 24 fps |
|---|---|
| Quiet start | 1–17 |
| Outgoing pulse enters the gap | after 18 |
| Leading wall contact / localized response | 48 / visible from 49 |
| Outgoing tail finishes at wall | about 61.2 |
| Echo begins at wall | after 66 |
| Leading sensor receipt | 102 |
| Echo tail finishes entering sensor | about 117.84 |
| Sensor receipt cue finishes | 122 |
| Measurement mark appears at sampled wall location | 124–168 |

The green mark is one illustrative cue, not a replacement for or edit to the existing measurement dataset. Both wall reaction and mark share the original wall-contact anchor. Emission/reception rings share the actual oval's inspected front plane, offset outward by 0.12 mm for visibility.

## Implementation and limits

`OUTGOING_FINITE_PACKET` and `RETURN_FINITE_PACKET` use fixed object transforms and route-coordinate sample sites. Actual local height and transverse geometry change as a finite sampled envelope passes; this is not a translated wiggling object or whole-bridge inflation. Absolute shape keys store every rendered frame; `route_u`, `strand_v` and the material node `Causal_front_route_coordinate` control finite support. No runtime handlers are required. Every-frame storage corrected the preliminary three-frame interpolation amplitude loss.

Full outgoing height and width are about 40 mm, matching the provisional visible face; the return is about 20 mm, with a violet shift. The unchanged source profile is an artistic window of an assumed 400 kHz pulse. Shape dimensions and seven-second playback are separate from physical sample time. This is not measured ECCO RF data, calibrated fluid displacement or a full acoustic simulation. Original 24.576 mm gap and anchors remain unchanged.

The fixed wider review camera and source-frame-305 tableau remain. Original CAM_S01_Continuous exists as a retained datablock/action, not as the active camera/timing of this proof. Existing source data remains preserved.

## Evidence and delivery

Final native: `04-Production/Shared/Assets/Acoustics/RibbonWaveform_v012/S02_causal-waveform-review_v012.blend` with relative ECCO library reference. Main video: `Previews/causal-waveform-context_v012.mp4`, 168 frames at 24 fps, seven seconds. Heavy native/video/raw frames remain local.

`causal-verification_v012.json` records active route bounds, projected positions, geometry hashes, object matrices and cue visibility across 19 frames. `causal-preservation_v012.json` confirms all ten retained v007/v010/v011 native/video hashes match previous manifests. Final selected stills and render timings are included in the publication manifest.

An initial cold shader benchmark exceeded the five-second cap and stopped before batch. The corrected candidate passed all representative checks; final every-frame outbound benchmark was 2.593 seconds and receipt 2.485 seconds at 640×360 Eevee16. No cap exception was taken. Master independently reviews and integrates; full shared controls, variants and consumer migration remain incomplete until representation is chosen.

Final completed batch: 168 frames, exactly seven seconds at 24 fps; maximum full render-to-file 2.86 seconds, mean 0.96 seconds. All frames stayed below five seconds. Final quiet, outgoing, contact, return, receipt and post-receipt measurement stills were inspected.
