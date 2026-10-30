# Surface and descent controls — v005

Current native master: `04-Production/Shared/Assets/Surface/Surface_descent_v005.blend`. v004 retains the full pre-cutaway exterior. Collection names retain v004 for stable references.

- Link collection `SURFACE_RIG_SUBSEA_v004` at identity for the selected S01/S02 world coordinates (metres, vertical Z). It contains the detailed Surface v003 rig and adapted original `03_SUBSEA` only. No historical camera/tool/mechanism imported.
- The seabed remains at Z=-120m. Original subsea lower parts were at -160m, so the new version raises the lower assembly by 40 m and shortens the long riser/guide spans, keeping their top at 10 m. These are illustrative scene dimensions, not verified equipment dimensions.
- Local collection-instance transform provides placement. Individual meshes remain editable in the master. Do not scale the full descent scene or camera to move an asset.
- `SURFACE_DESCENT_EARTH_SOURCE` stores named earth mesh data, hidden as a library source. Consumer earth objects link those meshes while retaining their original transforms and actions. Widening changes far outer faces, leaving the local animated opening untouched.
- The deep destination is linked separately from `WellAssembly/World_environment_v010.blend`, collection `WORLD_S02_PHYSICAL_CUTAWAY`, using `World_interface_v010.json`'s `canonical_to_s02` matrix. It replaces only `S02 geological wall retained section`; its local action and action slot remain intact.
- The standalone S01 copy ends at frame 240 and keeps the World destination hidden. The continuous S02 copy retains the original appearance transition at 240→241; it is the continuity verification scene. This avoids showing two competing walls.

Consumer copies are `Consumers/S01_shared-descent_v002.blend` and `Consumers/S02_shared-descent_v002.blend`. Their cameras, lenses, frame ranges and timing remain local. No source previs scene was overwritten. Relative links resolve from this repository layout.

v005 contains an illustrative 0.45 m axial opening and a near-side 50-degree camera-access cut from Z=-121 to-100. It clears the locked camera's path through the subsea assembly. This is a viewing section, not actual internal hardware; use v004 if a full exterior is needed. The foundation has only the axial opening and remains seated at Z=-120.

Do not migrate locked production automatically. Adopt the collection and mesh references into a new section version, compare the full local camera path, and preserve local data/reveal behavior. Surface detail remains source-derived illustrative geometry, without new engineering certification.
