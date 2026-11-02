# ECCO-057 — closure handoff, 3 November2026

Radzi requested ticket wrap, then authorized cleanup of unused Blender assets. The completed collaborative execution is submitted for human Review. Final editable handoff: `Scenes/S01-S02_production_v027_clean.blend`. The reviewed full clip remains `Previews/Full-v026/S01-S02_full_v026.mp4` (756frames,24FPS,31.5seconds,1920×1080). v026 and earlier useful versions remain preserved locally. Review submission does not imply client/engineering certification or completed AI finishing.

## Implemented scene direction contract

| Aspect | Retained implementation |
|---|---|
| Intent | One continuous journey from offshore surface into a tight borehole, arriving at BHA/transmitter measurement and pulling back to the recorded blue bore surface. |
| Camera and environment | Previs-derived path, pipe-to-rock transition around95, later cutaway reveal and source-driven bore presentation. Pullback474–720 with wide hold720–756; later exchanges continue during pullback. No added slowdown at180. |
| Hardware and shared inputs | BHA_film_v008, Surface_descent_v008, World_environment_v014, World_motion_grid_v003, Waveform_shared_v021 and Measurement_reveal_v001. ECCO hardware is retained within BHA dependency hierarchy, not as the replaced standalone shot assembly. Current native contains nine resolving library links including nested dependencies. |
| Signal choreography | Six shot-owned exchanges begin300/360/420/480/540/600. Shared connected beam opens over5frames; cyan send and violet feedback, bipolar pulse variation/amplitude, held breathing contact patch and center-out tile glitch. No circular impact. Real source/contact placement retained; feedback completes before tool changes target. |
| Measurement look | Uniform settled blue persists, fitted to actual bore interior with nominal4mm clearance, upper extent beyond frame. Upward motion starts gently around520. Rings trail the tile front2frames, build over4frames, persist; first bottom ring omitted. Width, delay/build and enable controls retained. |
| Final visibility | Superseded tan proxy plates, point markers, premature legacy borders and replaced source presentations excluded; retained native measured lines/fill and approved fixed-pixel world guides. |
| Optional DOF | Investigation only. Layered camera-depth blur is feasible in one960×540 still; it is not integrated into the production native or full video. Focus remains disabled in production. |
| Truth limits | Camera accommodation, waves and measurement display are illustrative visual explanations, not engineering measurements or physical simulation. Radzi owns film assembly, narration/sound and client acceptance. |

## Cleanup and verification

`Scripts/cleanup_scene_v027.py` checks ID dependencies before deleting disabled/replaced local objects and obsolete waveform control links. It retains the actual linked v021 controller and all required asset dependencies, then removes orphaned data and unused local fake-user data. No shared source file is edited. Saved/reopened cleaned native is3,315,355bytes versus19,112,763bytes (82.65%smaller). Scene objects616→58;558unused objects removed. Total loaded objects1348→770 because linked BHA/environment source objects are still required. Library links16→9. Exact inventory and hashes are in `cleanup_v027.json` and `closure_manifest_v027.json`.

Thirty sampled frames verify identical camera/BHA transforms, lens, evaluated wall coordinates/topology counts and all six waveform coordinate hashes before/after cleanup. Five960×540 still comparisons at1/95/386/620/756 were inspected:95and386 pixel-identical; others have sparse edge-level differences, maximum mean absolute channel difference0.0000156. No visible appearance change found. This is proportionate sampled equivalence, not an exhaustive new v027 motion render. The v026 full render remains the current full-shot visual reference.

Full-video evidence:756decodedframes,31.500seconds, zero drops/duplicates; all756 encoded frames inspected chronologically across16contact sheets and selectedHDdetails. Successful render-to-file sum467.019s, average0.61775s/frame, max1.39382s/frame. Elapsed691.809s includes recovery after an initial Blender crash at112 completed frames; no further failure after reusable export buffers. [Full-render record](full_v026_handoff.md).

## Controls and reuse

- `World pixel guide controls`: N→World Grid, master and cave/cut-earth/seabed switches, independent densities, fixed-pixel stroke width/opacity. After reopening run embedded `START HERE — pixel guides`; native F12 alone does not include the Python guide overlay. Use the provided final-visibility/pixel export scripts for this established reference look.
- `Shared fine measurement display`: Contour rings enabled, Contour delay frames, Contour build frames. Local profile radius defines2mm ring weight. The bore-fit clearance is an authoring parameter, not a live arbitrary-shape solver.
- `WF_MASTER_CONTROLS` / sharedv021: reusable pulse/style/color/variation/beam and timing controls. All six live fields link the v021 system. Contact/glitch companion timings must be reauthored if the exchange landmarks change. [Shared interface](../../../Shared/Assets/Effects/Waveform/README_v021.md).

## Deferred work and storage

DOF investigation found correct physical focus placement and a working separate-layer still; animation, near/far overlap, scene-linear premultiplied compositing, pixel-guide participation and total1080p cost need a focused future test. [Research and method](dof_investigation_v002.md). No deferred feature is silently presented as delivered production behavior; no new follow-up ticket has been created.

Native masters, full MP4/PNG sequence and predecessor/research scenes remain local under this sequence root or `04-Production/Shared/Assets`. No off-machine native/video backup or media upload is claimed. Scripts, reports, interface consumer metadata, compact verification and selected stills are synchronized on the existing task branch. Unrelated staged/unstaged workspace reorganization is preserved. Work records carry the exact closure commit and pinned report link.

Next action: Radzi's final ticket review; any later creative change or DOF integration starts from this cleaned handoff. No more rendering or scene changes are running.
