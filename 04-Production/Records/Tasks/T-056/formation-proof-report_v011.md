# ECCO-056 — Waveform formation proof v011

Status: focused animated proof awaiting Radzi's review. The owner asked to see the waveform actually form, rather than a light moving along a finished shape. V011 provides both an isolated example and a device-context example. V007 and v010 remain preserved, not overwritten.

## What moves

The ribbon begins flat and faint. Local height grows progressively from the sensor end while the far end stays flat; the broad peak and trough then develop fully. The ribbon settles, a weaker response develops from the wall end, and the shape returns to the same flat starting geometry. The object does not translate. Route coordinates, endpoints and transverse width stay anchored.

Seventeen local shape keys drive the 32 filaments. At frame 25, the near region (route coordinate 0.25) has height factor 0.926 while the far region (0.85) remains zero. Frame 50 reaches full height. Intermediate evaluated geometry hashes differ; frames 1 and 120 have exactly the same geometry hash. All sampled object matrices and endpoint positions remain unchanged. Full centerline height is 40.039 mm; filament thickness adds 0.064 mm. This is within the inspected provisional sensor-face display size.

## Meaning and limits

The starting profile uses the unchanged assumed 400 kHz model's 2.5–5.0 microsecond sample window, with the artistic taper/fan already documented in v010. The new delayed height envelope is an artistic animation model, not measured ECCO data, physical fluid displacement or a wave-equation simulation. The weaker response coefficient is 0.52. The five-second cinematic timeline is separate from the source sample's microsecond time axis.

The device-context clip uses a fixed review camera and a tableau frozen at source native frame 305. The original CAM_S01_Continuous datablock and action are retained in the context file; this is not a claim that the review clip uses the original shot camera or timing. The isolated file excludes source collections. Both native files use relative ECCO library references and stored shape-key animation; no auto-execution handler is needed for playback.

## Review files

- `Previews/ribbon_formation-isolated_v011.mp4`: 120 frames, 24 fps, five seconds, 960×540, Eevee 32 samples.
- `Previews/ribbon_formation-context_v011.mp4`: matching five-second device-context review, 640×360, Eevee 16 samples.
- Native files: `Shared/Assets/Acoustics/RibbonWaveform_v011/Ribbon_formation-dark_v011.blend` and `S02_ribbon-formation-review_v011.blend` (relative to `04-Production`).
- Geometry evidence: `ribbon-geometry_v011.json`; render evidence: `ribbon-benchmarks_v011.json` and `formation-batch-*_v011.json`.
- Preservation evidence: `formation-preservation_v011.json`, all six v007/v010 native/video hashes match their retained manifests.

Native files, videos and raw frames remain local. Only permitted scripts, reports and selected stills are included in the publication manifest. Master alone integrates Git. No completed shared library, variants, consumer migration or owner acceptance is claimed.

Completed render evidence: isolated 120 frames, maximum 1.48 s and mean 0.32 s; context 120 frames, maximum 2.38 s and mean 0.88 s. Both clips are exactly five seconds at 24 fps. Context local-growth frame 25, weaker-response frame 90 and flat-end frame 120 were inspected.
