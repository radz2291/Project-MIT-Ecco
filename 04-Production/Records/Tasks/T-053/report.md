# ECCO-053 — Shared physical World v010

Candidate built and master checks completed. Publication and Radzi review remain; this is not owner acceptance.

The physical World now provides the exact S02 irregular wall as a reusable shape, preserves the earlier variants and extends surrounding soil without enlarging the borehole. Selected source natives are unchanged. The digital and descent builders received the saved/reopened interface.

Task UUID `1a107625-2539-4692-a13c-91509108f8c0`; authority: ECCO-051 delegated build stage and pinned ECCO-050 decisions at `58013a6f5a907bfdfe9a7c7d63405e3306c2c42c`. Local base `bb9a503c8d69ae0cf5ba20273a5280d130cc1949`, main; unrelated changes preserved. Master alone integrates Git.

## Outputs

- `04-Production/Shared/Assets/WellAssembly/World_environment_v010.blend`, SHA256 `9cb7d5c946e8573abc05af4ee3c12492610a982c1773a6437f90a762055fb540`.
- Adjacent `World_interface_v010.json`, `README_v010.md`, `Scripts/world_interface_v010.py` define named collection selection, placement, local visibility, source provenance and migration.
- `Scenes/S02_World_v010.blend` replaces only S02's physical retained shell and copies its local appearance action; camera/lens unchanged over all528 frames after save/reopen.
- `Scenes/T44_layers_World_v010.blend` preserves locked T44 layer view. This cased view uses the separate cased-formation module; it does not prove the changed open-hole outer extent.
- `Scenes/T44_open_World_v010.blend` is the open-hole Reuse_A consumer with the new library. Its representative render was completed and independently viewed by the master.
- `Scenes/World_extent_probe_v010.blend` and two `*_propagation_probe.blend` copies are isolated shared-edit tests, never production sources.

All paths above except shared paths are relative to this T-053 directory. Native media remain local; no new off-machine backup claimed.

## Checks and limits

`Evidence/geometry-verification.json`: all72,120 physical authority vertices match `(X,Y,Z)=(z+735,x,y)` exactly, with zero coordinate error. Source radius is0.155575–0.210530m. Selected WORLD, FORMATION, CASED-FORMATION, CASING and S02 hashes unchanged; no missing libraries. This is authored previs geometry, not certified clearance or field data.

`Evidence/consumers.json`: saved/reopened S02 and T44 cameras preserved; all source S02 frames checked. Master independently checked representative cameras and library resolution. S04 masks and timing, S02 samples/history, and all source cameras remain section-owned.

`Evidence/render-benchmarks.json`: full render-to-file Workbench960×540, AA8, S02 f528 **2.882s**, T44 layers f1 **0.523s**, both below5s. Images are geometry/coverage proofs, not Eevee material approval. S02 widened soil fills the final pullback frame. S01 surface/descent and S03 wide-view coverage must be checked by055/054 integration; no universal framing claim.

The S02 outer boundary is circular radius20m. Legacy formation outer cross-sections are square with20m transverse half-width (corners28.284m), not a20m-radius cylinder. Legacy `outer_radius_m` metadata denotes half-width for those square modules; use the documented geometry bounds. Existing axial lengths and cutaway angles are preserved. Formation_context_v002, Formation_cased-section_v002 and CasedHole_v002 remain separately selected modules, not stacked duplicate geometry.

`Scripts/verify_propagation.py` changes outer coverage20→21m in an isolated shared library and reloads two consumers while preserving their cameras. Earlier checker failures are retained: raw Blender `//` relative paths must resolve through `bpy.path.abspath` before Windows pathlib matching; square outer boundaries require half-width checks instead of radial checks. See final propagation evidence for actual result.

## Master closure checks

The master ran `Scripts/render_motion.py` in the single render queue: one T44 open-hole still and eight selected S02 frames, all strictly below five seconds. Per-frame measurements are in `Evidence/motion-benchmarks.json`. The master independently viewed the connected tool/open-hole composition and S02 contact, recording and pullback samples. `Previews/S02_sampled-coverage_v010.mp4` is an eight-frame coverage montage at 2fps, explicitly not a continuous native-speed motion proof. The S01–S02 continuous passage is tested by ECCO-055.

Independent master reopen evidence is in `../T-051/Evidence/053-independent-check.json`: sampled cameras, lenses, frame ranges and playback rates match baselines; external libraries resolve. The shared extent edit test passed in both saved/reopened probe consumers: S02 radius 21.000002m and T44 open-hole half-width 21m; production v010 was not modified by the probe.

The original worker lease expired while the package waited for aggregate integration. A fresh closure attempt was claimed after a live run check: `3c55b1b1-5d55-41eb-be46-8f1740e8c6b6`, worker `ECCO-053-world-20261030`. No other worker claim was present. The master owns scoped publication and will attach the verified remote SHA and pinned report to Work. No final film rendering or assembly is included.
