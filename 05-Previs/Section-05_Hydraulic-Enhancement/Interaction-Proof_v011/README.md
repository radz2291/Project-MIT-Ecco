# S05 v011 — Trail scale still review

Owner requests slightly larger and longer trails, with a still before animation rendering. v010 is positively reviewed; this is a bounded size amendment.

Review `Previews/trail-scale_still.png`, frame 48, matched to v010's representative still. Amber trail cross-sections are 35% wider and tails extend 50% farther backward along the existing geometry-aware routes. Leading positions, opacity, color, camera, fluid shading and motion, rock tracking, source hardware, rotation and borehole remain unchanged. All 18 trail objects are rebuilt in this separate successor; v010 is preserved.

Editable source: `Scenes/S05_trail-scale_v011.blend`, reopened in Blender at frame 48 with valid relative shared-library link. Still rendered in 1.24 seconds at 1280 x 720, EEVEE 8 samples. No animation was rendered. Stop for owner still approval before any movie render.

The enlarged animated trail geometry was checked at 96 frame positions and 95 halfway positions without rendering those frames. No intersections with steel or fluid boundaries; minimum checked steel distance 10.925 mm, wall margin 1.680 mm. This is illustrative geometry, not CFD. See `Records/geometry-verification.json`. A same-machine D recovery copy contains the native, still and relative source dependency. Shared masters and v010 native are unchanged.

Scripts, reports and selected still are published through the dedicated D checkout. Heavy native stays local. Exact remote commit is recorded locally in `Records/sync-verification.json` after push.
