# Render feasibility — v005

ECCO-057, owner-requested render test,2 November2026. Live full linked scene; no asset, camera or saved scene changes. Restored user's current frame117. Same GPU viewport-depth/pixel-guide exporter as v005, SOLID/material colors, existing light/shadow settings,1.2px guides. This tests the playblast-to-AI input workflow, not a lit Cycles/Eevee render or AI generation.

720p1280x720: nine sampled frames1/80/95/106/123/157/318/432/528 passed0.877–1.655s each, including full environment and late measurement effects.1080p1920x1080: four samples80/106/432/528 passed1.160–1.693s. Timing includes frame evaluation through PNG saved, with guide geometry and pixel transfer/export. Raw timing records accompany this note.

Actual1080p motion: frames95–122,28frames at24fps (1.167s). Every frame passed; range1.64–2.46s, average1.82s, below strict5s cap. Exported `../Previews/Render-feasibility-v005/S01-S02_entry_1080_v005.mp4`; encode and full decode succeeded. Stills and raw PNGs in that folder are local only. No expensive render or full528-frame batch ran.

Conclusion:1080p viewport-style output with the screen-pixel grid is manageable on this machine. A full528-frame pass would be roughly16minutes at the measured motion average, an estimate rather than verified whole-sequence timing. Rebenchmark materially different settings. The grid is fine at1080p; irregular longitudinal lines remain an appearance review point. AI interpretation/removal remains untested.

Reproduce using Scripts/benchmark_pixel_render_v005.py in the connected Blender UI (set __file__ when executing its source). Override test_frames/test_size/test_prefix for short clips. Native F12 does not draw the custom Python overlay; use the supplied GPU exporter. Native/media stay local; scripts and measurements are synced evidence. Task remains collaborative/in progress.
