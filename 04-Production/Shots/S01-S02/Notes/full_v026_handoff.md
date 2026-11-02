# ECCO-057 — complete v026 scene review render

Owner requested the full scene after approving removal of the first bottom contour. Rendered every frame1–756 from the unchanged local `Scenes/S01-S02_production_v026.blend` at1920×1080,24FPS. Video is31.5seconds, H.264/yuv420p, with the established final visibility and pixel guides.

Local review video: `Previews/Full-v026/S01-S02_full_v026.mp4`. Full PNG sequence is in the same folder. This is the production playblast/reference look for collaborative review and subsequent AI finishing; no scene/camera/material/timing edits were made for this export. Source SHA256 remains2aa8d05af5b7eaa72d0610dfbb2cd22eba6e851c5d2d63deb944855cc3674f08.

Successful frame render-to-file sum467.019seconds (7m47s); average0.61775seconds; maximum1.39382seconds. Elapsed rendering job691.809seconds (11m32s), including interruption/recovery, excluding subsequent video encoding and visual review. All frames stay strictly below5seconds. Benchmark/settings in `full_v026_benchmark.json`; per-frame timings in `full_v026_render.json`.

Initial Blender process crashed after112 completed frames inside native `im.save_render` (access violation in VCRUNTIME memmove; exact underlying cause unconfirmed). Crash evidence is retained locally in `full_v026_initial_crash.txt`. Reopened the unchanged native through the official Blender bridge and resumed113 onward using reusable image/offscreen buffers. All remaining frames completed without another failure. `stable_full_export_v026.py` retains the canonical pixel-guide rendering algorithm and final object visibility; it avoids creating/deleting buffers for every frame.

FFmpeg decoded756frames,31.500seconds,1920×1080 at24FPS, with zero drops/duplicates. All756 encoded frames were inspected chronologically on16 decoded contact sheets; selected full-resolution encoded stills at536/620/756 also inspected. Reviewed the entry, descent, cyan/violet exchanges, tile reveals, persistent blue, upward front, retained later rings, omitted first ring and final wide hold. No source-animation edits were introduced to address broader creative choices. `full_v026_review.json` records scope; `full_v026_summary.json` records video hash and timing.

Scripts, compact records and selected decoded stills are Git deliverables. Native/MP4/complete PNG sequence remain local; no off-machine media backup claimed. Full-shot owner review is open and ECCO-057 remains in collaborative progress.
