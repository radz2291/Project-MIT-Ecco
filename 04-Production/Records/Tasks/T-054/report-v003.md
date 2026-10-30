# ECCO-054 — Bounded v003 geometry diagnostic

**Still partial. Stop geometry iteration.** Master independently reviewed both v003 images and confirmed incomplete contextual line coverage. This diagnostic does not supersede the verified v002 mapping or close the task. S02 reveal and S06 context findings in the main report remain unchanged.

On 30 October 2026, master authorized one different method: derive contextual strata/grid curves by intersecting the actual evaluated World cap triangles with regular planes, instead of projecting old incompatible curves. `Scripts/cap_intersections_v003.py` writes the separate local `Consumers/S03_shared-digital_v003.blend`. The original v002 remains unchanged.

The helper recovers mean-Z strata planes and X grid planes from the existing contextual curves. It selects cap-like transverse triangles, orients double-sided normals toward the frame1 camera, intersects triangles, connects matching segment endpoints, and offsets chains3mm along averaged cap normals. Local measured/reconstructed geometry, data contours, cameras and timing are not changed. It never bridges missing geometry to invent continuity.

Final diagnostic:40920 selected triangles,70 strata planes producing217 chains,8 grid planes producing478 chains. Some outer lines are more coherent, but the selected context surface still yields incomplete source-like coverage. No complete shared visual quality or owner acceptance is claimed.

- `Previews/S03_cap-intersections-v003_f001.png`:2.873s.
- `Previews/S03_cap-intersections-v003_f120.png`:1.229s.

Both are full render-to-file640×360 Eevee8 proofs with compositor/raytracing disabled. No batch was run. Root inspected the rendered results and retained **partial** status.

The curves are a **derived representation, not live geometry updates**. `Evidence/cap-intersections-v003.json` pins the exact World SHA256. Run `Shared/Assets/DigitalEnvironment/check_context_derivation.py` before reuse: it exits nonzero on a changed World file. Regenerate through `Scripts/cap_intersections_v003.py` in background Blender after any World shape change, then review again. The guard prevents silent stale use; it does not turn this incomplete diagnostic into an accepted presentation.

`Evidence/native-manifest-v003.json` records the diagnostic hash and v002 preservation check. `publication-files-v003.json` names only this incremental evidence for the master integrator. No Git operation, native-source overwrite or final Work completion was performed. The remaining styling choice is deferred to the master/owner; no further geometry attempts are authorized in this handoff.
