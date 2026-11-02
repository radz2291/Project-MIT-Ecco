# Full sequence render — v007

ECCO-057,2 November2026. Owner requested more horizontal cut-earth grid lines and a render of the whole continuous scene.

Current native: `../Scenes/S01-S02_production_v007.blend`, saved/open at the user's frame155. Pre-change dirtyv006 preserved as `S01-S02_session_before_v007.blend`. Horizontal cut-face spacing20→5m; vertical spacing remains5m. Cave remains sparse: rings4m/lengthwise90degrees. Seabed10m unchanged. All areas enabled for this proof; master and independent switches remain available in **N → World Grid**, with clearly labelled Horizontal/Vertical spacing. Stroke stays fixed1.2pixels. This is a shot preset using shared guidev003; master defaults and other shot consumers remain pinned. Physical World v014, Surface v008, BHA, waveform, camera and event timing unchanged.

## Completed output

`../Previews/Full-v007/S01-S02_full_1080_v007.mp4`:1920x1080,24fps,528frames,22seconds. All frames1–528 exported with the full linked environment and pixel guides. PNG sequence retained in the same folder. Encode succeeded; complete video decode verified528frames. Review sheet samples1/80/106/155/240/318/432/528 from the encoded video.

Strict render-to-file cap passed on **every frame**: minimum0.462s, maximum1.452s, mean0.630s. Frame timing includes scene evaluation through PNG saved. Full timer-driven export wall time440.1s (~7min20s), including UI/timer overhead; video encoding/verification followed. Seven representative1080p benchmarks passed0.644–1.009s before starting. Actual first1/80/106/155 PNG hashes match benchmark images exactly. No skipped frames, resolution reduction or environment culling.

This is the established GPU viewport/playblast-style output for AI input, not a new lighting treatment or AI-generated final. All source callbacks and fixed-pixel guide exports use the shared helper. After reopening, run **START HERE — pixel guides** once to restore overlay/panel; F12/native Viewport Render does not draw that custom Python overlay.

## Recovery and evidence

Render script `../Scripts/render_full_v007.py` renders one frame per timer tick, records each timing and stops on a5s cap failure. `verify_full_v007.ps1` checks all528 nonempty PNGs, encodes the movie and verifies decoded frame count. Timings, decode progress, native/link record and video SHA256 are in full_v007_*.json/txt. The user's frame155 and live controls were restored after rendering; all relative libraries resolve.

Native scenes, raw frames and video remain local under this checkout; no off-machine backup claimed. Scripts/reports/selected stills are synced evidence. AI interpretation/removal of guides remains untested. Collaborative visual review remains open; this is not owner acceptance or ECCO-057 closure.
