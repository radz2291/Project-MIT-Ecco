# Match blue, extend shell and synchronize the upward reveal — v021

Owner identified three issues in v020: scanned strip color differed from the historical shell; upper shell ended inside the frame; upward reveal retained timing that no longer matched the restored camera pullback.

Native: `../Scenes/S01-S02_production_v021.blend`. Sourcev020anddirtyreviewcopy retained. Shared masters unchanged.

Color: the old historical face colors were sampled at the settled end state and averaged by face count. That referenceRGBA(0.033471,0.428582,0.922452,0.201033) now supplies a single settled historical material and the end state of all24scanpatchmaterials. Initial scan glitch/color keys through relative31frames remain; patches settle to the common blue at+39and hold. This replaces the unmatched0.4opacityband while preserving a visible persistent record. Sixpostbeamcolor matches verified.

Extent: continuation uses the existing128vertextopring and15mmrow spacing. Shell top extends fromZ-724.700to-720.919; savedmesh73728faces. Original96scanfacepositions preserved. At the end, the revealed front projects outside the image at normalizedX1.106–1.149/Y1.103–1.181, so its upper termination is beyond the crop. Extra continuation is illustrative display geometry; no BHA dimensions or engineering approval changed.

Timing: old historical447–518starts were replaced with a monotonic upward height front derived from the actual camera474–720. The front initially grows from the scan row, follows the upper/right picture region, then passes beyond the crop as the pullback finishes. The existing native4framesettle supplies cell motion. Current six panel receipts, beam/pulse/contact timing, BHA motion and camera path remain unchanged.

Old independent historical grid/contour objects are retained disabled; their old reveal clock cannot run ahead of the surface. The local display builds coarse history lines and fourth-row contours from the actual revealed wall, while preserving all fine tile edges on the six scan patches. Point markers and previs target plates remain excluded. Closed wide cutaway retained.

[Change/native hash](shell_sync_v021.json). [Cold reopen checks](shell_sync_v021_verification.json): all six common settled colors, monotonic upward front across474/528/600/660/720/756, revealed front beyond finalcrop and resolving relative links. Savedscene756frames/24FPS/31.5seconds.

Quick final proof: `../Previews/Shell-sync-v021-final/camera_reveal_v021.mp4`, source474–756every3frames at8FPS,95frames/11.875seconds/960x540. Playback speed preserved; temporal sampling is lower than native24FPS. Decoded95frames, zero drops/duplicates. [Timings](shell_sync_v021_motion_summary.json):61.131swall,36.042sactive,avg0.379s/frame,max0.669s. No crash. [Two1080pstills](shell_sync_v021_final_stills.json):matched_blue_close414andextended_wide756, each0.59s. Sixinitialstaticviewpoints also inspected. The first diagnostic/coarse-grid preview remains separate from the final preview; final adds preserved scan-tile edges.

No new full-shot render or final AI stylization. Native/videos local only, no off-machine backup claimed. Reports/scripts/selected stills synchronize separately. Owner visual review remains open.
