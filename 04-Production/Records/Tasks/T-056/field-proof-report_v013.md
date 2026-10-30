# ECCO-056 — Fast rolling-wave field v013

Current focused proof: `Previews/rolling-wave-field-context_v013.mp4`, four seconds at native 24 fps. The owner requested faster, more organic internal motion. V013 replaces v012's largely fixed packet silhouette with continuously evolving, overlapping crests. The full rendered sequence was inspected through sequential frames and the every-six-frame contact sheet, `Previews/field_sequence_v013.png`.

## What changed

One sampled field combines an outgoing wave train and a delayed, weaker wall reflection. Two frequencies and coordinated phase variation across 32 strands make crests form, roll, interfere and decay. A smooth sine-squared envelope controls both geometry extent and opacity, removing the hard rectangular cut edges. No random wobble or object translation is used. An outgoing-only onset and a return-dominant tail remain visible.

Height uses one constant normalization for the entire clip, capped at approximately 40 mm peak-to-trough, plus tiny filament thickness. Width is capped at 40 mm. There is no per-frame normalization and no global pumping correction. The actual sensor-wall anchors, 24.576 mm gap and fixed wider review camera remain unchanged.

## Cause and timing

At 24 fps: source emission spans frames 8–38; wall arrivals span 20–50; the reflected field reaches the same sensor during 32–62. The sensor response cue ends at 64. A single wall measurement mark appears at 68 and remains through frame 96. The wall-born return overlaps outgoing waves after contact; the mark still waits until the return is over. This is fast cinematic timing, not physical acoustic time.

## Provenance and controls

This new multi-component field is explicitly authored, not raw RF samples or measured ECCO data. It is not a full acoustic solver or a calibrated depiction of fluid particle displacement. Controls are documented in the C dictionary of `build_field_v013.py` and in `field-model_v013.json`: source duration, travel delay, carrier period, frequency mixture, reflected strength, strand count and size limits. Changing them requires rebuilding the baked proof; this does not claim a finished shared-asset API.

The native stores 96 absolute shape samples and material-envelope animation. It replays without handlers or auto-execution scripts. The original CAM_S01_Continuous remains a retained datablock/action; this review uses a fixed source-frame-305 tableau. The existing measurement dataset is unchanged. Only the scoped illustrative wall mark is timed here.

## Verification and delivery

All 96 full render-to-file calls passed the five-second cap: maximum 2.26 seconds, mean 0.87 seconds at 640×360, Eevee16. Representative benchmarks topped out at 3.009 seconds. The sequence contact sheet includes every sixth frame from 6 through 96. Twelve prior v007/v010/v011/v012 native/video hashes match their retained manifests.

Final native: `04-Production/Shared/Assets/Acoustics/RibbonWaveform_v013/S02_rolling-wave-field_v013.blend`, with a relative ECCO library reference. Exact native/video hashes and permitted publication paths are in `publication-manifest_field_v013.json`. Heavy native/video/raw frames remain local. Master alone integrates Git. Owner acceptance and final reusable controls, variants and migration remain pending.
