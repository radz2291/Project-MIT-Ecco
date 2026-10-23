# S05 v012 — Longer trails, still review

Owner requests a little more length after v011. All 18 amber trails are another 25% longer than v011 (1.875 times v010 length). Width remains at v011 scale: 1.35 times v010. Leading ends and geometry-aware paths are unchanged; tails extend backward along those paths. Camera, fluid, rock tracking, hardware and borehole are preserved.

Review `Previews/trail-scale_still.png`, matching frame 48. Native: `Scenes/S05_trail-scale_v012.blend`. The still rendered in 1.662 seconds at 1280 x 720, EEVEE 8 samples. No animation frames were rendered. Hold for owner approval before animation.

Enlarged geometry passes complete triangle/containment checks at 96 frame positions plus 95 halfway positions. No sampled steel/fluid-boundary intersections; minimum checked steel distance 10.925 mm and wall margin 1.680 mm. These are geometry checks, not CFD. The native reopens with a valid relative shared-source link. v011 remains unchanged. A hash-verified local D recovery copy includes native, still and relative source dependency. Scripts, records and selected still are published; heavy native stays local. Exact remote proof is in local `Records/sync-verification.json` after push.
