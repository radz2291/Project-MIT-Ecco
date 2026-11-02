# Restore widening during scans — v017

Owner requested restoring the previs camera sequence. Direct inspection of original S01-S02 continuous v011 shows scan2 return ends360, scan3 return ends402, and camera pulls back408–528 while scans4–6 continue. Productionv016 incorrectly postponed its pullback until after all six and ended short of the previs wide lens/position.

Current native: `../Scenes/S01-S02_production_v017.blend`. The actual original408–528 camera arc/lens is rigidly aligned to the production third-scan camera and retimed to474–720. First474frames retain the prior camera at sampled checkpoints; third return completes469, beam closes472, hold ends474, scan4 starts480. Scan5 starts540; scan6 starts600. Final wide55mm lens reached720, held through756. Scene length remains31.5seconds/24FPS. Hardware and approved beam/pulse/contact/reveal timings remain unchanged; shared masters unchanged.

A necessary companion correction protects current target cells from the camera-facing inspection wedge. Otherwise the restored view deleted four faces from scan4. The mask excludes receipt frames300–999 (the six current target patches) from deletion. Native source patches and material animation are unchanged.

[Restore record](camera_v017_restore.json) includes native SHA, camera samples and preserved first-section checks. [Verification](camera_v017_verification.json) checks all six return timings and all16target faces per event, plus continuous camera motion. Relative links resolve after reopen. Before-protection draft and old native versions are retained locally.

Blender crashed during the first preview attempt. Owner restarted; official bridge reconnected to clean savedv017 at600. Saved correction was intact. Background verification passed, then a separate fresh preview was generated without saving/reloading during active export. A second export crash occurred at source656 after103frames. Crash backtrace identifies EXCEPTION_ACCESS_VIOLATION in nvoglv64.dll at GPUOffScreen.draw_view3d, inside the preview exporter. This points to the NVIDIA OpenGL export path; it does not establish the driver defect cause. No animation recovery loss found. Owner reopened Blender again; official bridge resumed after read-only check, and frame656 exported individually in0.931seconds. Remaining51frames resumed from saved preview records.

Fast changed-section proof: `../Previews/Camera-v017-verified/camera_pullback_v017.mp4`, source450–756 sampled every2frames at12FPS. It preserves playback speed, but shows half the temporal samples of the24FPS scene. 154frames/12.833seconds/640x360. This is not a new full-shot render. Benchmarks/render/decode records sit beside this note. Owner review of the correction remains open.

Native/video local only, no off-machine backup claimed. Scripts/configuration/reports/selected proof stills synchronize separately. Original supplied previs and productionv016 preserved.

Retry completed:154frames decode12.833seconds, zero drops/duplicates. Active export120.002seconds, average0.779s/frame,max3.871s below5s cap. Combined measured render-attempt wall148.222seconds excludes restart/diagnostic waiting. [Timing summary](camera_v017_render_summary.json). Current correction remains awaiting owner visual review.

