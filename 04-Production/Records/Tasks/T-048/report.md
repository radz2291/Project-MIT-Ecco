# T48 — Shared circulation and cuttings candidate

18 October 2026 · ticket `adfe3c82-31e2-4c1e-a725-94a29c1ef573` · T45 builder · reviewer Radzi. Current run `6866654a-0703-4f3f-9a63-2ee249cdca58`, attempt 2, worker `codex-t45-flow-builder`.

Reusable continuous amber circulation, authored sparse matte cuttings and restrained sliding dashes are saved with two independent linked consumers and a playable four-second demo. The current candidate adopts accepted T44 continuity commit `a08d0ecfbd6f3241298f506b3ea42613388b3baf`. Execution is complete for master integration and fresh-context verification; this is not a Review submission or human/engineering acceptance.

## Exact current outputs

| Native candidate | SHA256 |
|---|---|
| `Shared/Assets/Hydraulics/Hydraulics_v003.blend` | `e4db1c08362b7bc9d6476382a4c98124fe1ed148045e98384c982e015f447a5c` |
| `Records/Tasks/T-048/Scenes/Flow_reuse_A_v006.blend` | `24813e95903c38ba6d7dd24badc4f1ae0f2f09b19cd76c3de6b699b90218a4ab` |
| `Records/Tasks/T-048/Scenes/Flow_reuse_B_v006.blend` | `463c7acc16eed27476eaa8de8d126e288c1fef2adfd494ae83d5e957807531aa` |

Paths in this table are beneath `04-Production/`. [Manifest v002](../../../Shared/Assets/Hydraulics/manifest_v002.json) records exact dependency/image/video hashes. [Interface v002](../../../Shared/Assets/Hydraulics/README_v002.md) documents linked geometry and stable phase/speed/density/visibility/emphasis/mode controls. Planned V3 consumers are S05-A/B/C; no actual movie shot or film assembly was produced.

Current selected stills are `Previews/Revision_v007/Flow_A_f0036.png`, `Flow_B_f0048.png`, `Flow_B_f0096.png`. Local playable demo: `Previews/Revision_v007/Hydraulics_behavior_B_v007.mp4`, SHA256 `1083449ff1ea54fb94b79ade3e1db149b6c7dd36082aaf5f1b69915ba6d565b8`, 878311 bytes. All 96 frames fully decode: 1280×720, 24 fps, 4.000 s, H.264/yuv420p, silent. No temporal synthesis.

## Source and revision checks

Fresh Work/handoff and the master authorized resumption after T44 became Done. Direct BHAv006 alone was reloaded to v007; frozen nested v006 was retained. One extension and joint attach to the existing hardware instance. Original camera/lens, 72/96-frame timing, camera keyframes, old controls, source geometry/metre scale and actual hardware/flow placement are preserved. Earlier material/cutting-geometry shared revisions still reach both linked consumers. Predecessor natives, initial readability samples, old failed registration and upstream-hold records remain unchanged; see [repair history](repair-history_v001.md) and [historical hold report](report_hold_v001.md).

[Source map v002](source-map_v002.md) retains the inspected brochure/chat/CAD/B204/T43 provenance. Source length remains 2.400 m, with the original CAD unit conversion retained. Return follows selected T44 −X uphole. Physical source end identity and certified hydraulic stage-face assignment remain unresolved; neutral region windows are morphological anchors. All three regions operate simultaneously, with no acoustic arcs or performance labels. Paths, cuttings and timing are illustrative, not CFD, calibrated velocity/pressure, wake/efficiency evidence or verified particle transport.

Preflight item 5 is repaired in `verify_hydraulics_v002.py`. It derives the complete finite axial envelope from actual guide nodes and shape support, enumerates hardware recursively by collection provenance, and clips every intersecting triangle. Faces crossing the slab are covered even if their vertices lie outside it. All 135 visible base-hardware meshes plus the extension/joint are considered, including recorded disjoint geometry. The crossing-face regression witness passes. Every frame checks actual rigid assembly registration and finite particle/tracer meshes at peak density. Source unit conversion, relative/nested links, materials and one ECCO/extension/joint pass fresh-open checks.

For the declared centred nominal pose, conservative full-shape clearance is at least 0.897 mm to hardware and 0.852 mm to the evaluated faceted wall, including a 1 micrometre numerical guard. No hardware or wall enlargement occurred. New bores, eccentricity, scaling, hardware or motion require affected rechecks. Evidence: `native-verification-summary_v007.json`, both `Flow_reuse_*_v006_fresh-open_v002.json` and `continuity_*_migration_v007.json`.

## Performance and actual preview inspection

Master slot T48-FINAL-01 serialized six samples, master image inspection, then the B96-frame demo. Six complete write calls measured 0.722–1.914 s. Every demo frame passed: 0.612–1.644 s, 68.655 s summed write time. Logs stop at any frame reaching 5 s. Settings: 1280×720/24 fps/EEVEE16/Vulkan, AgX Medium High Contrast, no compositor; GTX 1060 3GB, NVIDIA 560.94, DESKTOP-46SO266. Normal existing driver caches were retained. Prior empty-cache startup of 12.55–25.13 s remains unresolved; no universal cold-machine claim.

All six stills, full-size decoded B48/B96 and the ordered nine-frame chronology were inspected. Camera/geometry/amber continuity remain coherent. Fine matte cuttings and directional dashes are deliberately subtle at actual clearance; moving readability requires Radzi review and is not claimed as a comprehension pass. Master independently fully decoded all 96 distinct video frames and inspected the chronology. `encode-qa_v007.json`, `benchmark_v007.json` and `batch_B_v007.json` record the checks. These executor/master inspections do not replace fresh-context verification or human appearance/technical acceptance.

## Ownership, storage and remaining handoff

Only Hydraulics/ and T-048/ were modified. No live Blender edits, Git writes, shared-global edits, client contact, A-OUTPUT, movie shots or film assembly. Machine root is `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Blender/video/raw frames and logs remain local; no native upload or off-machine backup is claimed.

[allowed-tracked-files_v002.txt](allowed-tracked-files_v002.txt) is the explicit task-owned integration list: scripts, records/JSON and three selected current generated stills. The master alone stages/commits/pushes and verifies the exact remote SHA, runs cross-package integration and fresh-context verification, then attaches pinned evidence before Review. The child run waits for that integration. Only Radzi accepts.