# T-006 / B102 — preparation and unresolved fit inputs v001

15 October 2026. Task `0d01c109-a994-461b-b4c1-2fd3661f6fac`; run `37bc8f7e-d319-4e81-b0cb-f0faf3c3a2bd`; worker `codex-t006-01a13f79`; reviewer Radzi.

## Result

**Moving clearance fixture and independent preparation saved; T6 remains incomplete.** O05 / BL02 prevents constructing a supported complete well/BHA/bit assembly. The fixture checks the accepted product's linked interface against a published diameter boundary; it is not a selected casing/cement or well variant. Complete-assembly/variant criteria remain unsatisfied. The instruction to continue T6 authorizes this work; it does not supply missing deployment dimensions.

Live T2, T3 and T4 were Done; pinned roadmap revision 2 current; fresh handoff read before claiming. T5 initially was revising v002, then Radzi reported acceptance and live Work confirmed T5 Done. Continued fixture construction uses that accepted temporary plugged v002; v001 remains unchanged. Official MCP queried the live default Cube/Camera/Light scene and left it unchanged. Isolated background Blender 5.2.2 handled the saved assets/fixture.

## Inspectable outputs

- [Moving fixture MP4](Previews/B102_clearance-fixture_v001.mp4), [editable linked fixture](../../../Shared/Assets/WellAssembly/B102_clearance-fixture_v001.blend), [motion sheet](Previews/B102_clearance-motion-sheet_v001.jpg), [fresh-open checks](Evidence/clearance-fixture-verification_v001.json), [render evidence](Evidence/clearance-fixture-build_v001.json), [video QA](Evidence/video-qa_v001.json). Reproducible scripts: `Scripts/build_clearance_fixture_v001.py`, `Scripts/verify_clearance_fixture_v001.py`, `Scripts/package_clearance_preview_v001.py`.

- [Compatibility preview](Previews/compatibility-study_v001.png): sourced diameter comparisons; visually inspected, text and boundaries legible. Not a Blender render or complete assembly.
- [Shared preparation/interface](../../../Shared/Assets/WellAssembly/README_v001.md), [pending config](../../../Shared/Assets/WellAssembly/config_pending_v001.json), [dimensional gate](../../../Shared/Assets/WellAssembly/Scripts/compatibility_v001.py), [draft variant builder](../../../Shared/Assets/WellAssembly/Scripts/build_variants_v001.py).
- [Fit/gate checks](Evidence/compatibility-checks_v001.json), [v001 inspection](Evidence/product-inspection_v001.json), [v002 snapshot including closures](Evidence/product-inspection_v002.json), [output hashes](Evidence/output-manifest_v001.json).
- [Brief image index](Evidence/brief-image-index_v001.jpg) and [mapping](Evidence/brief-image-index_v001.txt), [datasheet text](Evidence/datasheet-text_v001.txt). Internal local inspection evidence, not public/client distribution.
- [Read-only inspection script](Scripts/inspect_product_v001.py), [preparation checks](Scripts/verify_preparation_v001.py).

## Findings from original brief

Radzi directed checking `01-Brief` and specifically the ENP3 datasheet. Its three pages were text-extracted completely. Published 12in maximum OD and 12.3in minimum casing ID agree with the inspected 304.800154mm envelope. At that minimum ID, ideal centered radial gap is approximately 3.809923mm. This is not a drift, thread or full BHA fit certification.

The 12.25in chat open-hole example has approximately 3.174923mm ideal radial gap; that alone does not confirm its deployment or bit/BHA. The 8.5in hole and 9-5/8in / 7in casing OD examples are smaller than this tool. Casing OD comparisons are upper bounds on the actual ID clearance, not misidentified casing IDs. The brief's workshop/product images do not provide complete dimensioned assembly inputs. Datasheet illustration is explicitly not to scale. No scale was recovered from photographs.

## T5 consumption / checks

v001 read-only measurement matches its T5 SHA-256 `c37547042cd56780bbeb3577377df8933b794371e60b0a853305f1e2a436a057`; 348,876 housing vertices. T6 also inspected v002 including nine closures, hash `704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7`; its envelope is unchanged. T5's placement record initially referred to a different earlier failing hash. A fresh verification subsequently arrived matching this inspected v002 hash: all executor checks pass, including closure placement and movement. T6 now pins temporary plugged v002 as its provisional reference; it does not accept that geometry on MIT's behalf. No T5 output or ticket was edited. Re-read its report/hash before later construction.

Pure checks passed for inch conversion, measured OD correspondence, incompatible smaller examples, eccentric contact and invalid numbers. Missing configuration is rejected; prepared scripts compile. Pending-config invocation exits before assembly construction as intended. Complete variant-builder geometry/control/cutaway checks remain unperformed; syntax/refusal testing does not validate those future assets.

## Source-sized moving clearance fixture

After T5 acceptance, built the linked-source fixture with a published 12.3in minimum-ID wire boundary, no wall thickness, and axial extent derived from measured 2.4m product plus 100mm functional test travel. The 360-degree rotation is a control exercise, not an asserted drilling direction/RPM. No BHA, bit, casing OD, cement or selected trajectory was invented.

Fresh-open self-checks pass: rendered source matches fixture hash; relative v002 library resolves and source hash matches; nine closures remain present; evaluated collection instances match controls exactly; full turn / 100mm test travel preserves positive radial clearance approximately 3.81mm and swept axial bounds. Frames 1/25/49/73/96 were measured; pure X rotation/translation preserves radius throughout. This does not certify eccentric/deviated operation. Initial harness retained transient dependency-graph iterator records; failure log retained, harness corrected to copy matrices and retain original datablocks. Fixture/source were unchanged by that correction.

Rendered 96 PNGs, Workbench 1280x720 / 24fps, elapsed **23.596 seconds**. Silent H.264/yuv420p MP4 decodes exactly 96 frames / 4.0 seconds / 24fps / 1280x720 without errors. Visually inspected all 96 frames through four chronological sheets, labeled encoded-video motion sheet and full-size raw frames 1/49. Motion is continuous; product remains framed; closures follow it; stationary boundary remains separate. This is frame-by-frame inspection, not a claim of real-time playback review or human acceptance. Boundary denotes only the inner limit; the separate fit diagram shows readable gap values. Actual deployment and complete mechanical-shot QA remain pending.

## Required inputs / next action

Resolve O05 through Radzi/MIT: actual BHA/bit geometry and connection/datum mapping, selected open-hole and casing ID/OD, cement extent and shoe/deviation constraints. Do not use the minimum casing ID as proof of an actual scenario. Confirm permitted illustrative wall-shape parameters separately. Once these are supplied, select the settled T5 version, remeasure the full envelope, complete/rework and validate the prepared builder, export moving variant previews, and return exact candidates for Review. O04 and O14 remain open and affect acceptance/replacement checks.

## Closure / repository state

Base main / `ffa19e6b4792ddc859e8f93da10f8c7e073f2f95`. Candidate explicitly uncommitted. Starting tree contained T5 changes to the Decision Register, asset/blocker registers, T5 task folder and ECCO asset folder; preserved. T6 retained outputs are entirely under `04-Production/Shared/Assets/WellAssembly` and `04-Production/Records/Tasks/T-006`; registers receive a bounded evidence addendum only. No commit, push, backup, client contact, public publication, engineering approval or self-acceptance. Local paths are not remote downloads.

Reproduction: run installed `C:/Program Files/Blender Foundation/Blender 5.2/blender.exe --background <ECCO master> --python <T-006/Scripts/inspect_product_v001.py>` read-only; run bundled `C:/Users/RZ1/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe -X utf8 <T-006/Scripts/verify_preparation_v001.py>`. Pending builder refusal: `blender.exe --background --factory-startup --python <WellAssembly/Scripts/build_variants_v001.py> -- <WellAssembly/config_pending_v001.json>`. No production construction bypass is authorized.

## Rolladice synchronization

Partial evidence attached as five exact machine-local absolute output references on T6 and its run. Task is Blocked on O05/BL02, not Review/Done. The connector requires ending an active run before marking its task Blocked: waiting did not release ownership, so the execution was ended with failed status explicitly due to missing inputs, then T6 was marked Blocked. Fixture checks passed; this run disposition does not mean the fixture failed. No work was accepted on Radzi's behalf.

## Follow-up: researched standard scenario v002

Radzi asked for research into normal/expected configurations and MIT website sources. [Research note](research-standard-scenario_v002.md), [sourced proposal configuration](../../../Shared/Assets/WellAssembly/config_researched-proposal_v002.json), [comparison diagram](Previews/researched-scenario_v002.png) and [arithmetic checks](Evidence/researched-scenario-checks_v002.json) provide a credible provisional 17.5in host / 13.375in casing / 12.25in lower open-hole scenario. 61lb/ft casing reference: 12.515in nominal ID, 12.359in drift. Actual MIT deployment/placement and adapter interfaces remain unconfirmed; no production scene or existing configuration overwritten. Earlier closure above describes the initial run, not this research follow-up.
