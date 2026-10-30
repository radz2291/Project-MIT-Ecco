# ECCO-054 — Digital environment and stored-surface reveal

30 October 2026. **Partial candidate: S03 contextual line continuity remains unresolved. Not a completed visual delivery.** Master ECCO-051 integrates and independently reviews this package. Task `832f05b9-228a-4d65-8430-f2fd56178d85`; worker `ECCO-054-digital-20261030`; run `4c187a7c-5fca-4d03-90af-5e0ca0c47867`. Base `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`. Controlling T-050 decisions are pinned at `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`.

## Implemented scope

- Shared S03 dark soil/cyan contour/strata/grid material library and shared palette, preserving S06's local opacity and brightness controls.
- Live World physical geometry with separate digital look; canonical X→local Z transform and local display windows. Local reconstructed samples remain separate.
- Parameterized stored-surface arrival/settle and a separate fine-point/line/translucent style. S02 local cell start times remain authoritative; S06 fine guide colors inform presentation.
- Actual S02, S03 and S06 integration copies plus two deliberately illustrative shape cases. No locked source scene is overwritten.

## Outputs

Native masters are under `04-Production/Shared/Assets/DigitalEnvironment/` and `MeasurementReveal/`. Their README files document inputs and usage. Native consumer copies, evidence, scripts and previews are under this task folder. `.blend`, videos and raw frame sequences remain local/ignored, without a new backup claim.

`Digital_style_v001.blend`: selected exact S03 materials and common cyan palette. `Digital_world_v001.blend`: live World geometry wrapper plus width-only dependent adapter. `Measurement_reveal_v001.blend`: linked reusable reveal and fine style groups.

The earlier S03/S06 `shared-digital_v001` copies are **width-only comparisons**, not a claim of full physical-shape synchronization. Final `shared-digital_v002` copies use actual linked `WORLD_FORMATION_IRREGULAR_CUTAWAY`, with exact mapping X→local Z, Y→local Y, Z→negative local X (determinant+1), no scaling, and local axial windows. Its existing soil caps remain intact. Data is not silently reshaped to fit the physical context.

## Verification so far

Official Blender read-only connection was checked. The UI was never mutated; all native work used installed Blender5.2 background with factory startup and auto-execution disabled. The running MCP scene changed independently from the inherited earlier BHA state; no restore/save operation was attempted.

Saved S02 reveal evaluation: frames317/441 retain512 original acquisition-row faces and no stored history;447 has640 faces,480 has8292,528 has41472. Missing receipt attribute hides all test geometry. Original mesh coordinates/topology, material values/keyframes and local datasets are retained; the shared overlay reads the evaluated local stored wall and excludes the acquisition row.

Initial S06 f52 benchmark failed at13.741s, retained in `Evidence/render-benchmarks-initial.json`. The first isolated proof was too faint/cropped and was revised. Current six-frame preview benchmark passed0.187–1.494s at640×360: Eevee8 for S03/S06 and isolated proof, original Workbench for S02; compositor/raytracing disabled at runtime. These settings do not certify original full-resolution render cost. No full movie batch was rendered.

Master identified the width-only synchronization limitation; v002 uses real linked geometry. Executor then identified S06 animated physical visibility could resurrect the old context and interfere with later stages. A bounded correction preserves the local stage-opacity chain while replacing only physical geometry; old physical objects evaluate to zero faces and the new source hides at250/288, leaving the laptop clean. The initial full-shell face deletion also removed planar soil caps: evaluated geometry existed but little ground was visible. Diagnostic opacity was1, not transparent; the selected correction uses the actual capped shared cutaway and its inspected orientation.

Raw sample coordinates, topology and object transforms match original S02/S03/S06 exactly (`Evidence/data-preservation.json`). Shared reveal motion covers source440–528, sampled every4frames and encoded6fps to preserve source timing:23frames, maximum full render-to-file2.185s after final528 benchmark. No baseline files were saved by this task.

## Remaining closure

The shared reveal and S06 context have concrete native/visual evidence ready for master review. S03 soil now comes from the actual shared World, but its old contextual grid/strata were drawn on a flat viewing surface. Projection onto the uneven shared cap did not recover their full former line hierarchy. Sparse legacy curve modifiers failed; the bounded final method uses sampled local mesh-edge carriers, live World ray projection, captured original hit mask, cap-facing selection and a 0.25m local display-clearance window. It removes the false cross-hole fan/loop, but some contextual lines remain fragmented or occluded. **Do not present this as resolved or visually accepted.** Preserve this evidence for a scoped choice about adapting the contextual lines to the shared physical cap.

Latest S03 proof is `Previews/S03_final-projected-ground_f001.png` and `_f120.png`, full render-to-file2.609/1.209s. Capped S06 proof is `Previews/S06_final-capped-ground_f052.png` (1.223s). Earlier `S06_final-context_f250.png` verifies clean laptop stage; the later cap-source substitution retains the same local stage-hide/opacity controller. S02 native motion is `Previews/S02_shared-reveal_motion_v001.mp4` (23frames, source timing preserved, maximum2.185s).

`Evidence/final-consumer-mappings.json` names the final native candidates for master camera/library checks. `Evidence/native-manifest.json` records exact current versions/hashes; `publication-files.json` identifies permitted task files for the sole integrator. Synchronization and commit-pinned links are supplied by master; this worker makes no Git mutation. Do not mark this task Done or complete while the S03 visual defect remains. Only Radzi accepts appearance.

No engineering certification, real-sample calibration, final movie assembly, client contact or delivery is implied. All native/video artifacts remain local with no new backup claim.
