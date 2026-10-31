# Surface descent — connected World revision

31 October 2026. ECCO-051 owner-authorized revision of ECCO-055 / shared World. **Review candidate; Radzi retains native/appearance acceptance.** Base publication `9a818de2e587d1aecade8587825ed2c3b35e23b0`.

## Result

The offshore setup now has a sea surface at mean Z=0, with its pontoons submerged and its deck above water. Surface v006 contains equipment and two alternative ocean views, with no geology or complete section scene. World v011 owns seven broad, contiguous geological units and the exact existing S02 destination wall. A separate linked demo places both together and keeps World present from frame 1 through the S01–S02 handoff.

The narrative remains: leave the familiar surface, travel through rock and lose ordinary visibility, arrive beside ECCO and the same physical wall that Section 2 measures. Layer count and scene depths are illustrative, not a measured stratigraphic log or a confirmed ECCO deployment. Offshore remains the film's proposed setting.

## Current native files

Local root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/`.

| Purpose | Path below local root |
|---|---|
| Equipment and sea master | `04-Production/Shared/Assets/Environment/Surface/Surface_descent_v006.blend` |
| Physical World master | `04-Production/Shared/Assets/Environment/Borehole/World_environment_v011.blend` |
| World selection/placement | `04-Production/Shared/Assets/Environment/Borehole/World_interface_v011.json` and `Scripts/world_interface_v011.py` |
| Connected inspection demo | `04-Production/Shared/Demos/Surface_descent_demo_v002.blend` |
| Focused borehole inspection demo | `04-Production/Shared/Demos/World_demo_v002.blend` |
| Native-speed moving proof | `04-Production/Records/Tasks/T-055/Revision_v006/Previews/Surface-to-wall_v006.mp4` |

Use the connected demo's scene dropdown: **Descent — connected S01-S02**, **Surface — waterline**, **Surface — water column**, **World — layered descent**. Its 528-frame source reference is local to the demo. Shared masters contain no shot cameras, lights or local acquisition/history animation. No additional consumer-copy deliverables were created.

## Implementation and continuity

- Surface equipment uses the preserved v005 geometry, including its previously documented illustrative camera-access opening. Mean waterline Z=0m; pontoon bounds -20..-14m; deck wings 10.5..13.5m; seabed -120m. The half-ocean is an editorial viewing cut, selected instead of the full ocean for static inspection.
- Regional geology covers source Z=-120..-1020m with 180m outer extent. Unequal broad units are contiguous; finer bedding is a material treatment. The local interval -750..-720m reserves the exact S02 wall, avoiding stacked competing bores. Regional radial/profile boundaries and cutaway angle match the existing wall.
- The first static review exposed a rectangular destination patch. The regional opening was corrected to match the exact -5..225-degree S02 profile, and its host geological unit now shares the existing wall material. The original wall geometry/material remains unchanged.
- `WORLD_DESCENT_CONNECTED` combines regional geology with exactly one S02 physical cutaway. Its transform/scale is constant and has no appearance action at frames 240/241. The source physical authority remains available for existing local measurement/history bindings.
- The World master itself opens with only the connected collection in its scene, avoiding duplicate regional/legacy walls. Other physical variants are retained as selectable library collections; their geometry and visibility flags are unchanged.
- The original moving camera matrices/lenses match at all 528 evaluated frames. Local measurement/history animation remains local. Only the new demo repairs the old missing hardware link to the current ECCO v003. The source native is not repaired or saved.
- Removed old demo-only earth slabs, old sea/seabed proxies and the remaining `Main solid building` proxy that masked the detailed accommodation. Static overview framing is new demo composition; original moving camera/timing is unchanged.
- World v010 stays active and byte-exact for the visually approved Digital v004 and other pinned consumers. Its derivation guard still reports `valid: true`. No Digital styling, waveform, production shot or film assembly was changed.

## Verification and review evidence

See `world-evidence.json`, `demo-build.json`, `independent-verification-final.json`, `benchmark.json`, `motion.json`, `artifact-manifest.json`, `media-verification.json` and `archive-moves.json` beside this report. The independent verifier is separate from the Surface/demo author and World builder. It checks saved/reopened natives, links, all source cameras, exact predecessor geometry/shape keys/transforms, constant World state, object ownership and unchanged source hashes.

Export preview settings are Workbench 640x360, AA5, shadows/cavity off, 24fps; the regional static overview is portrait 360x640. The editable demo's inspection defaults remain 800x450 AA8 (portrait450x800). Representative cold/heavy frames are benchmarked before the moving proof; rendering stops on any full render-to-file frame of 5 seconds or more. The initial 960x540 AA16 motion render stopped at frame112 (5.069s); a second800x450AA8 attempt stopped at frame147 (5.068s). Both failed attempts and their frames/timing records are preserved. The export-only profile was simplified, both failed frames were added to its benchmark, and the complete proof was rerendered. Earlier benchmarks before the join correction are also retained. The preview covers native frames 1–288 at 24fps, without slowing or omitting source frames.

Master visually inspected the revised waterline, water column, regional geology, subsea travel and destination/handoff frames, then inspected the encoded proof's sequence-wide review sheet and decoded every frame. The proof establishes geometry and continuity. Final cinematic lighting, underwater optics, surface sea shading and motion finishing are not established by Workbench. The near-axial descent camera remains inherited from the selected source; this revision does not claim a new camera treatment.

Original/native sources and accepted variants are preserved. Previous Surface v005 and the two prior focused demos are moved byte-exact into the dated archive after verification; archived links are not maintained, per Radzi's instruction. `archive-moves.json` records exact paths/hashes. New Blender/video media remain local only, with no new off-machine backup claim. Only permitted reports, scripts, interfaces and a small still selection are published; no excluded media are force-added.

## Research supporting the agreed direction

- [SLB: semisubmersible](https://glossary.slb.com/en/terms/s/semisubmersible): buoyant submerged pontoons support the elevated deck through columns.
- [SLB: drilling riser](https://glossary.slb.com/en/terms/d/drilling_riser): connects the floating rig to the subsea BOP and returns mud to the surface.
- [Kansas Geological Survey: geologic maps and cross-sections](https://kgs.ku.edu/kansas-geologic-maps): sectional views reveal otherwise hidden subsurface relationships.

Review the ocean/equipment relationship, geological readability and continuous arrival beside the same sensor/wall. Technical checks are separate from owner appearance acceptance, engineering verification, client acceptance and final film assembly.
