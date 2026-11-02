# World v014 — closed descent / front reveal candidate

New consumer: `04-Production/Shots/S01-S02/Scenes/S01-S02_production_v003.blend` only. v013 and all pinned consumers unchanged. Review candidate, no owner appearance acceptance claimed.

- `WORLD_DESCENT_CONNECTED`: exact retained v013 geometry, including original shape keys.
- `WORLD_DESCENT_FRONT_CLOSURE`: complementary130-degree sector, split in halves. Seam radii follow the original profiles; the missing sector is interpolated and illustrative. Axial sampling0.25m, matching regional continuation.
- `WORLD_DESCENT_CLOSED`: both collections for a complete circumference and seabed cap.
- `WORLD retained bore presentation v001` and `WORLD front closure presentation v001`: Geometry Nodes groups with **Bore scale** (nominal1) and **Front reveal** (closed0, absent1). No time dependency, shot actions, cameras or lights. Consumer creates local objects sharing linked meshes, with local modifier controls and original placement. Do not stack these objects with a second World instance.

Only vertices inside radius1m receive bore scaling. Outer earth extent stays fixed. Expanded interior receives smooth shading; nominal retained wall geometry stays exact. Source S02 outer-margin shape keys must be evaluated when comparing geometry; raw Basis is20m whereas its existing evaluated margin is25m.

S01–S02 owns the source-derived clearance/retraction curves. This is an editorial viewing device, not physical rock motion or measured geology. Source v013 preserved; exact hashes and build information in World_interface_v014.json and the sequence Notes/world_v014_build.json. Build script: Scripts/build_world_v014.py. Native remains local only; no off-machine backup claimed.
