# Optional World pixel guides v002

Additive ECCO-057 shared module. Native: `World_motion_grid_v002.blend`; [interface](World_motion_grid_interface_v002.json). Consumed only by `Shots/S01-S02/Scenes/S01-S02_production_v005.blend`. Earlier consumers unchanged.

Four edge-only meshes cover cut faces, seabed, retained bore and retracting bore front. Geometry Nodes filter spacing/visibility; the bore consumer applies World v014's existing presentation groups. Source Enabled defaults off. The consumer uses1m bore rings; the module socket default15m is adjustable. No physical wall changes, camera or timeline in this module.

Use [pixel_guides_viewport.py](Scripts/pixel_guides_viewport.py) to draw fixed-pixel strokes and export playblasts; native loose-edge display is only a fallback and may show occluded wires. Call `install()` for the live overlay and `export(path,width,height)` for scene-depth-tested PNGs. Run setup after opening a new Blender process. The consumer contains a relative-path setup text. F12/native Viewport Render do not run the custom Python overlay.

[Consumer controls, proof and limitations](../../../../Shots/S01-S02/Notes/pixel_grid_v005_handoff.md). Optional illustrative motion reference, not geology measurements; AI finishing not tested. Native asset local only; see interface hash. Earlier strip module v001 is superseded, retained locally for recovery.
