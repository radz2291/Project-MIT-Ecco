# Optional World pixel guides v003

Owner-requested ECCO-057 sparse-cave/denser-cut-earth successor. Native `World_motion_grid_v003.blend`; [interface](World_motion_grid_interface_v003.json). Consumers: S01-S02 productionv006 and v007. v007 uses the same master with horizontal cut-face spacing5m; other preset values remain as v006. Prior consumers remain pinned.

Four edge-only meshes, zero faces, no surface strips. Existing visibility/spacing node group now also filters lengthwise bore guides by angular spacing. Defaults: rings4m, lengthwise90deg, cut-earth20m depth/5m radial, seabed10m; master disabled. Shared control empty supplies master and independent region switches. Shot controls remain local and adjustable.

Run embedded **START HERE — pixel guides**, then viewport **N → World Grid** for the panel. The shared [drawing/export module](Scripts/pixel_guides_viewport.py) supplies fixed-pixel1.2px strokes, scene-depth testing and sidebar controls. Run setup after reopening; no auto-execution. Native F12/Viewport Render does not include the custom overlay. [Consumer controls, proof and limits](../../../../Shots/S01-S02/Notes/grid_v006_handoff.md).

No physical environment or camera changes; illustrative motion guides, not measurements. Native asset remains local only. Predecessor guidev002 is preserved. AI rerender remains untested.
