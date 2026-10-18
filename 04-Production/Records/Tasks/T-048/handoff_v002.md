# T48 frozen candidate handoff v002

18 October 2026. Build/native/media preparation is complete; the run waits for T45 integration, exact remote SHA and fresh-context verification. **Not Review.** No native renderer/build/encoder remains active. Only the two owned roots were modified; no Git or live Blender changes.

Current accepted T44 base: `a08d0ecfbd6f3241298f506b3ea42613388b3baf`. Current [manifest_v002.json](../../../Shared/Assets/Hydraulics/manifest_v002.json) hashes exact resolved direct v007/nested v006, ECCO/environment and Flow geometry dependencies, both current consumers, three selected stills and the local playable demo. The earlier hold is resolved; historical hold records and predecessors are retained.

| Candidate | SHA256 |
|---|---|
| `Shared/Assets/Hydraulics/Hydraulics_v003.blend` | `e4db1c08362b7bc9d6476382a4c98124fe1ed148045e98384c982e015f447a5c` |
| `Records/Tasks/T-048/Scenes/Flow_reuse_A_v006.blend` | `24813e95903c38ba6d7dd24badc4f1ae0f2f09b19cd76c3de6b699b90218a4ab` |
| `Records/Tasks/T-048/Scenes/Flow_reuse_B_v006.blend` | `463c7acc16eed27476eaa8de8d126e288c1fef2adfd494ae83d5e957807531aa` |
| `Records/Tasks/T-048/Previews/Revision_v007/Hydraulics_behavior_B_v007.mp4` | `1083449ff1ea54fb94b79ade3e1db149b6c7dd36082aaf5f1b69915ba6d565b8` |

Paths above are beneath `04-Production/`. The machine root is `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`. Heavy natives/video/raw frames stay local Git-ignored, with no off-machine backup claimed.

Preflight item 5 is repaired in `Scripts/verify_hydraulics_v002.py`: provenance-based hardware enumeration, whole finite support slab, every intersecting triangle clipped including outside-vertex crossing cases, actual rigid registration and complete finite meshes every frame. Conservative tested hardware/wall clearance is at least 0.897/0.852 mm with numerical guard. Continuity parents and camera/timing/animation/old-control invariance pass. No enlarged geometry or source rescale.

Master-granted six samples measured 0.722–1.914 s; every B demo frame passed 0.612–1.644 s. The MP4 fully decodes 96 frames/24 fps/4 s/720p/H.264/yuv420p/silent. All six stills plus full-size decoded frames and chronology were inspected. The master independently decoded all 96 distinct frames and inspected chronology. Geometry/camera/amber continuity is coherent; matte cuttings/sliding dashes remain subtle and are explicitly for Radzi's readability review. No comprehension/physical transport/CFD or engineering acceptance is claimed. Empty-cache startup remains unresolved.

Integration input: [allowed-tracked-files_v002.txt](allowed-tracked-files_v002.txt), an exact list containing owned scripts/text/JSON and only three current generated PNGs. Do not sweep native/video/raw/log files or unrelated changes. Current report is [report.md](report.md), interface `Hydraulics/README_v002.md`, finite checks `Evidence/native-verification-summary_v007.json`, timings `benchmark_v007.json`/`batch_B_v007.json`, media `encode-qa_v007.json`.

Run identity: `6866654a-0703-4f3f-9a63-2ee249cdca58`, attempt 2, worker `codex-t45-flow-builder`. T45 owns remote commit/pinned outputs, combined integration and independent verdict before Review. Only Radzi accepts; no later shot or film work authorized by this handoff.
