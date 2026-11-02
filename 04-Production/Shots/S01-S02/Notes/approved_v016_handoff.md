# Approved exchange integration — v016

Radzi approved quickv022 on 2 November. [Shared v021 preset and controls](../../../Shared/Assets/Effects/Waveform/README_v021.md) preserve that appearance without further creative changes.

Current native: `../Scenes/S01-S02_production_v016.blend`. Six exchanges start 300/360/420/480/540/600. Each holds tool/camera for 54 frames; six frames then turn to the next target. Final pullback follows. Frame range 1–756 at 24 FPS, 31.5 seconds. Pre-300 camera keys retained; long trial v015 preserved.

[Integration](approved_v016_integration.json) records source/target positions, center errors and landmarks. [Verification](approved_v016_verification.json) checks all six versions, centered hits, feedback before turns, patch hold/handover and demo relative links. First-event geometry equals approved quickv022 at nine samples.

[Proof timings](waveform_approved_v016_render.json): 57 exports at 640 by 360, max 0.605 seconds/frame, below the strict five-second cap. First exchange: `../Previews/Waveform-approved_v016/approved_exchange_v016.mp4`, 54 frames / 2.25 seconds, decoded successfully. Later-event frame 641 inspected. Full 31.5-second shot has not been rendered or accepted here.

Shared master contains waveform geometry/style; companion patch/reveal helpers author native actions. Target faces, actual hits, camera viewing wedge, camera and tool choreography remain shot-owned. Circular impact remains disabled.

Native scenes/demo/video remain local; no off-machine media backup claimed. Scripts/configuration/reports/selected stills synchronize separately. ECCO-057 remains open for whole-shot review.
