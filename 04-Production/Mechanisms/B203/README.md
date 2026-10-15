# B203 — Cased-hole inspection proofs

T9 / `38a96b60-83c6-4f68-a56b-c5fd9f16e161`. Candidate v002; standalone B2 mechanism tests, not S04 film shots or final finishing.

Open the [combined 24-second review cut](Previews/v002/B203_all-proofs_v002.mp4) or [review sheet](Previews/v002/B203_review-sheet_v002.jpg). See [task report](../../Records/Tasks/T-009/report.md) and [B206 questions](../../Records/Tasks/T-009/review-questions_v002.md).

| Proof | Editable source | Meaning |
|---|---|---|
| Retrieval | `Scenes/B203_retrieval_v002.blend` | Accepted T6 assembly, linked T5 product; authored motion into pre-existing casing. No active drilling. |
| Support | `Scenes/B203_support_v002.blend` | Two straight local longitudinal casing segments; schematic pulse paths and illustrative ringdown comparison. Outside layers are offset for visibility. |
| Channel | `Scenes/B203_channel_v002.blend` | One authored axial channel; same local axial/azimuth mask creates the exploded cutaway and conceptual processed map. |
| Wear | `Scenes/B203_wear_v002.blend` | Authored inner groove with fixed outer radius; nominal inner reference and magnified local wall-section graphic. |

Each proof is 144 frames at 24 fps. Workbench renders 1280×400; scripted composition yields 1280×720 H.264, silent. Text, waveforms and maps are editable in `Scripts/package_proofs_v002.py`; the Blender scenes retain geometry and animation. Composited information is part of the preview and is not embedded in the `.blend` alone.

Inputs: accepted `Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend` and `Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend`; [S04 V2](../../../03-Context/02_Storyboard/V2/ECCO_Section_04_Cased_Hole_Padlet_v2/PADLET_SECTION_04_V2.md), canonical engineering baseline, Decision Register and module 09. Source dimensions follow the T6 authorized configuration. New axial extents, animation time, channel width/extent, waveforms and 4 mm wear depth are authored illustrations, not measurements.

Geometry coordinates: longitudinal X, positive Y is retained rear half, angle is `atan2(Z,Y)`. The blue channel uses axial X in [-1.2,1.2] m and azimuth [.25,.85] rad. Its display translation +0.35 m in Z is an exploded-view offset only. Map has 0°–360° horizontally and axial position vertically; finite cell/mesh resolution causes boundary rounding. Sequential map reveal explains processing/accumulation, not real-time surface transmission. Gold/blue are the client-scenario cement/water interpretation and have no relation to open-hole geometry colors.

Waveforms use arbitrary time/amplitude with no calibrated axes; damping rates are authored for qualitative comparison. A single response does not prove water, cement bond quality or material identity. No acoustic propagation, resonance simulation, physical vibration or thickness inversion is implemented. Schematic pulse origins are not verified CAD acoustic faces. Straight local segments are appropriate for this bounded mechanism test; full deviated-well context and camera choreography belong to the later S04 blocking task.

Reproduction: run installed Blender 5.2 in background with `Scripts/build_proofs_v002.py`, then bundled Python with `Scripts/package_proofs_v002.py`, then background Blender with `Scripts/verify_proofs_v002.py`. Builder refuses existing candidates; version or archive explicitly before rebuilding. The support framing correction is reproduced by `Scripts/refine_support_v002.py` on the original v002 candidate. Originals and initial v001 attempt remain locally for evidence. Never run the builder in the user's active scene.

Relative product links resolve after fresh-open. Keep this folder in the project tree, or relink intentionally and reverify. Replacement product geometry requires new envelope/clearance, control, occlusion and scene checks. This proof does not modify either shared master.

Binaries, rendered frame sequences and videos are organized locally and Git-ignored; Git review contains scripts, reports, JSON checks and selected stills only. No remote backup of `.blend`/MP4 media is implied.
