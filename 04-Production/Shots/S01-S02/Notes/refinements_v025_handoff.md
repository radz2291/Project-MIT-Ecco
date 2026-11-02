# ECCO-057 — fitted measurement and trailing contours v025

Owner authorized both refinements. Current editable scene: `Scenes/S01-S02_production_v025.blend` (local, SHA256 in refinements_v025.json). v024 remains preserved.

The measurement shell now follows the actual World bore interior rather than the legacy previs radius. Projection uses the physical retained wall and the two real unit05 front closure meshes to cover the open camera sector. A nominal4mm air-side normal clearance accommodates the2mm contour profile and1.5mm tile arrival offset. All73856 wall vertices retain their Z, azimuth, face IDs, reveal attributes and materials. This is an illustrative display fit, not engineering certification.

All six beam endpoints and breathing contact cues move onto the fitted tile surfaces (2.11–2.87mm endpoint correction). Beam source positions, pulse styling, exchange timing, camera, blue color, upward reveal onset around520 and beyond-crop continuation remain unchanged. No canonical shared master changed; this fit and timing binding belong to this shot.

Major contours now follow each revealed section with a2frame delay, then build thickness smoothly over4frames. Four opacity stages accompany the build; the settled original pale material remains afterward. They derive from the revealed wall and persist. Native Geometry Nodes and drivers provide playback; no Python playback handler is required.

On `Shared fine measurement display`, object custom properties control `Contour rings enabled`, `Contour delay frames`, and `Contour build frames`. These are wired to native node inputs and cold-tested. The local fine-style group’s `Curve Circle.001` controls the2mm peak radius. The fit clearance is an authoring parameter in `Scripts/conform_and_soften_v025.py`; rebuild a successor if the World shape or ring thickness materially changes.

## Review evidence

- `Previews/Fitted-contours-v025/fitted_contours_v025.mp4`:115frames,960×540,12FPS,9.583seconds; source frames508–736 sampled every2frames at original playback speed. This is the pullback refinement proof, not a full-shot rerender.
- All115 encoded frames inspected chronologically across five decoded contact sheets. Blue front crosses the picture during pullback; contour sections build behind it, persist and follow the fitted wall. No visible cut-through observed in this proof.
- `during_reveal.png`620, `wide.png`756 and `close.png`382:1920×1080 stills,0.629/0.490/0.479s respectively.
- Active render-to-file sum64.162s; average0.558s; maximum0.779s. Elapsed timer job110.456s, including idle/UI/evaluation overhead. All exported frames strictly below5s.
- Cold reopen:18 sampled camera transforms/lenses identical to v024; all reveal face attributes identical; no missing linked libraries. All six evaluated wall/overlay tests at520/550/600/650/700/756 show zero sampled radial penetrations over0.1mm. Minimum sampled overlay clearance1.982mm, including major-ring thickness. This is sampled geometric evidence, not exhaustive collision certification.
- Final saved native controls reopened and on/off, delay and duration drivers verified. The control wiring added after preview uses identical default values, preserving the rendered geometry.

See `refinements_v025_verification.json`, `refinements_v025_controls.json`, `refinements_v025_render_summary.json` and reproducible Scripts. Native scene and MP4 remain local; scripts, reports and selected stills are Git deliverables. No off-machine native/media backup claimed. Owner review remains open; ECCO-057 is not concluded.
