# ECCO-052 — Shared hardware and satin finish

Candidate implementation and builder checks are complete. Master verification and publication govern submission to Review; only Radzi accepts appearance.

Task UUID `84299107-cdb7-4248-8900-9467907ead6f`; delegated by ECCO-051 under Radzi's direct assignment. Base checkout `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`, main, preserving unrelated changes. Controlling decisions: ECCO-050 at `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. Source hashes were checked by the master before delegation.

## Result

The accepted ECCO/BHA geometry is preserved in versioned successors. A separate linked satin group uses the selected S07 steel and darker sensor-face colors, with restrained 0.018 roughness modulation. It controls appearance without replacing geometry, local lights, or alpha/transparency behavior. S05 keeps its fluid choreography and S02 keeps its simple descent string.

New native masters (relative to `04-Production/Shared/Assets`):

- `ECCO/Satin_finish_v001.blend`
- `ECCO/ECCO_film_v003.blend`
- `BHA/BHA_core_satin_v001.blend`
- `BHA/BHA_film_v008.blend`

Consumer copies are `Consumers/S07_shared-satin_v001.blend`, `Consumers/S05_shared-satin_v001.blend`, and `Consumers/S02_shared-satin_v001.blend`. See [controls and migration](README-controls.md). All media/native files are local, ignored, and not uploaded or newly backed up.

## Checks so far

- Official Blender MCP read-only query confirmed access; the dirty running BHA v007 session was left untouched. MCP background execution could not locate Blender. Isolated background jobs used installed Blender 5.2.2 at `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`.
- Seven new native files reopened. All library paths are relative and resolve. [Saved-file evidence](Evidence/package-verification.json).
- A bounded shared roughness-base edit from .291 to .321 was observed on reopen in both S07 and S05. The library was then restored byte-for-byte. No consumer camera/timing edits were made. [Baseline mapping and evaluated camera samples](Evidence/consumer-mappings.json).
- First representative full render-to-file benchmarks at 640×360, Eevee, 8 samples: S07 f90 **3.083s** including first shader startup, S07 f170 **0.411s**, S05 f240 **1.257s**. [Timings](Evidence/render-benchmarks.json). These are working-setting checks, not claims for original high-resolution settings.
- The first master review found the silhouette and studio/fluid context readable without visible introduced clipping, and requested the 32-sample refinement documented below to reduce grain.

## Completed refinement and hardware proofs

- Master rendered the 32-sample refinement and inspected S07/S05: **1.982, 0.533, 2.619s**, with reduced grain. Its independent reopened camera/lens/range/fps comparison passed. See T-051 `Evidence/052-independent-check.json` and `review-findings.md`.
- The forced-Eevee S02 frame was blank gray: retained as a **failed appearance proof**, despite fast timing. Original Workbench f360 was a valid but too-tight view. Final Workbench f528 shows the simple string in the retained hole/camera composition, **1.884s**. Workbench proves geometry/visibility; finish is assessed in S07/S05.
- Isolated BHA demo shows the entire connected assembly with continuation hidden (**1.753s**) and the same control enabled at 2m. Initial continuation view clipped its left endpoint; the wider corrected demonstration shows the full endpoint (**1.154s**). Only this isolated inspection camera widened. The default master remains 12m; no locked camera changed.
- `Previews/S07_shared-satin_motion_1s.mp4` contains **24 consecutive frames 72–95 at native 24fps**, exactly one second. Every frame passed; maximum **1.331s** at 640×360, Eevee32. It is actual existing camera motion, not a sampled montage. Encoded video was decoded successfully. [Per-frame timings](Evidence/hardware-motion.json).
- Fresh geometry checks compare mesh vertex/topology hashes, parents and local transforms: ECCO **18 objects**, BHA core **148**, BHA wrapper **156**, all identical to their selected predecessors. [Geometry evidence](Evidence/geometry-preservation.json).
- The isolated BHA proof initially stopped before rendering because its source had no World datablock. The proof creates a local inspection background; source masters remain untouched.

Native/media hashes are in [native manifest](Evidence/native-manifest.json); permitted tracked files in [publication list](publication-files.json). All binaries remain local. Master owns commit/push and remote verification; the containing commit is attached to Work after synchronization. Work run `5b0847ef-85a1-48c9-ad78-0d5dbe57224d`, worker `ECCO-052-builder-20261030`, awaits master's synchronized closure.

Commands use the installed Blender executable with `--factory-startup --disable-autoexec -b -t 4 --python <script>`. Build: `build_shared.py`; fresh file/propagation checks: `verify_package.py`; geometry checks: `verify_geometry.py`; serialized proofs: `proof_hardware.py -- bench` then `-- motion`. The latter stops immediately if any render-to-file reaches 5s. FFmpeg encodes frame072 onward with `-framerate 24 -frames:v 24 -c:v libx264 -crf 18 -pix_fmt yuv420p`.

No engineering certification, exact BHA interface fit, calibrated sensor-face claim, client acceptance, or full-film production is implied. Supplied temporary closures and source limitations remain.
