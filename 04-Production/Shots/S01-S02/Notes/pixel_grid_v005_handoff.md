# Fixed-pixel motion guides — v005 trial

ECCO-057, 2 November 2026. Optional world-anchored grid on cut earth faces, seabed and bore interior. The bore has circumferential rings and lengthwise guides following World v014's existing expansion/retraction controls. Geometry and camera/event animation are unchanged from v004. Cave entry remains around95; the cutaway reveal stays on the outward move.

Current native: `../Scenes/S01-S02_production_v005.blend`, saved at106. Review video: `../Previews/Pixel-grid-v005/S01-S02_pixel_grid_v005.mp4`, frames80–169, 90 frames /3.75 seconds/24fps,480x270; decoded successfully. Representative stills80/95/106/138/157 and per-frame logs are in that preview folder and Notes. All90 frame exports passed <5s; maximum2.236s. Working viewport SOLID/material colors, shadows/cavity off. Full linked environment retained.

## Drawing and controls

The rejected v001 surface-strip attempt is retained locally, hidden, in `S01-S02_grid_strip_attempt_v005.blend`; it is superseded. The new shared `World_motion_grid_v002.blend` contains edge positions and spacing attributes, zero faces and no tube/strip thickness. `pixel_guides_viewport.py` draws them with GPU polylines at **1.2 output pixels**, independent of zoom or world scale. Strokes use scene depth, plus a small viewing-ray bias to avoid surface depth fighting. No camera-facing floating grid.

`World pixel guide controls`: Enabled; independent cut-face/seabed/bore visibility; depth25m, radial10m, seabed10m and bore-ring1m spacing; Line width px1.2, Line opacity0.8, Stroke shade0.008. Units describe illustrative reference spacing, not measurement data. Sparse/irregular rock topology can make lengthwise guides jagged; this is a review trial.

After reopening, run the Blender text **START HERE — pixel guides** once to install the live viewport overlay. This is explicit setup, without trusted-file auto-execution. The saved scene preserves all guide data and controls, but Python draw callbacks do not persist in a fresh Blender process. Normal F12 and native Viewport Render do not include this custom overlay. Use `Scripts/render_pixel_grid_v005.py`, which renders the same viewport into an offscreen buffer and draws pixel strokes against its scene depth before PNG export. The shared drawing implementation is linked by relative script path in the Blender text.

## Scope and evidence

Only consumer: S01–S02 v005. Other shared consumers remain pinned. World v014 hash is unchanged; Surface v008 was not edited. BHA v008, waveform v015 and measurement reveal remain as before. v004 and the pre-v005 session snapshot are preserved. Toggle verification produces zero evaluated guide edges when disabled; every guide mesh has zero faces. Library paths resolve. Native reopen and explicit overlay restoration are checked in verification JSON.

Native scenes/shared modules and video/raw frames are local only, with no off-machine backup claimed. Scripts, interface and selected proof stills are Git evidence. AI rerender/removal of the reference grid has not been tested. This is a collaborative checkpoint, not owner acceptance or task closure.
