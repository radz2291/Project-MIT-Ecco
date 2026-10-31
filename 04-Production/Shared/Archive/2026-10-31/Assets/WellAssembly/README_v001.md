# B102 well/assembly preparation v001

T-006, 15 October 2026. **Incomplete: O05 / BL02 blocks dependent assembly construction.** No production well, BHA, bit, casing/cement master or validated variant scene is claimed.

## Saved preparation

- [Editable clearance fixture](B102_clearance-fixture_v001.blend), [four-second MP4](../../../Records/Tasks/T-006/Previews/B102_clearance-fixture_v001.mp4), [fresh-open checks](../../../Records/Tasks/T-006/Evidence/clearance-fixture-verification_v001.json): uses accepted linked T5 v002 against the published 12.3in minimum-ID boundary, with 360-degree rotation / 100mm test travel. Fixture checks pass; no casing thickness or selected deployment asserted. 96 frames, 24fps, 1280x720; Workbench render 23.596 seconds; silent H.264. This is an inspection fixture, not the complete variants requested by T6.

- [Dimensional gate and source-based fit calculations](Scripts/compatibility_v001.py).
- [Pending configuration](config_pending_v001.json): unknown dimensions remain null. The published minimum casing ID is deliberately not assigned as the actual well configuration.
- [Draft Blender builder](Scripts/build_variants_v001.py): prepares nominal, irregular and spiral wall surfaces, casing/cement cutaways, shared axial/rotation controls and variant visibility, once supported inputs are supplied. Syntax and refusal of pending inputs checked; geometry, controls, cutaway topology, saved links and moving-preview behavior **not validated**. This is source preparation, not a deliverable scene ready for downstream use.
- [Task report](../../../Records/Tasks/T-006/report.md), [fit study](../../../Records/Tasks/T-006/Previews/compatibility-study_v001.png), [checks](../../../Records/Tasks/T-006/Evidence/compatibility-checks_v001.json).

## Sources inspected

Original `01-Brief/ECCO_ENP3_Datasheet-1.pdf` pp1-3: 12in max OD, 12.3in minimum casing ID; 2.25m nominal length (actual may differ); 6-5/8 F.H. Box/Pin, optional crossover. Diagram explicitly not to scale. No complete BHA, bit, casing OD/wall, cement thickness or actual deployment drawing provided there.

`01-Brief/Chat/chat.md`, 7 October 9:07/9:42 PM: 12.25in and 8.5in bit/hole examples; 9-5/8in and 7in casing **OD** examples. Smaller examples do not accommodate this inspected ENP3. Positive ideal gap for the 12.25in open hole does not approve that scenario. All 23 brief photos plus `images.jpg` inspected as a local contact sheet; they show product/workshop context and imaging reference, not a dimensioned complete deployment. No client media republished.

## Product version handling

Frozen v001 housing measured afresh in background Blender 5.2.2: 2.400000095m long, 0.304800154m maximum diameter about source X. Its SHA-256 matches T5 build evidence. T6 then inspected `ECCO_master_temporary-plugs_v002.blend` / `ECCO_MASTER_v002` including nine temporary closures; maximum diameter remains 0.304800154m. During inspection T5's evidence initially referred to an older failing snapshot. A fresh verification subsequently arrived and matches the inspected v002 hash `704a91cb478a1a38304835786fa62d549df5bf5833e457cbc4da094fd6557fd7`: all T5 executor checks pass, including closure placement and movement. This is source/control self-verification, not independent engineering acceptance.

Pending config now pins the temporary plugged **v002** and its matching hash as T6's provisional reference, preserving v001. Re-read T5 and remeasure all visible geometry if that hash changes. Preserve T5 outputs; no master was changed here.

## Resume after O05

Record actual deployment/source and inspect supplied BHA/bit, datum mapping, thread compatibility, casing ID/OD and cement/well bounds. Enter configuration plus field-level provenance. Shape amplitudes/pitch and cutaway extent may be approved illustrative values; identify them as such. Confirm no clash across rotation, travel, shoe and deviated intervals. Straight centered calculations are insufficient for those checks.

In an isolated background process run `blender.exe --background --factory-startup --python Scripts/build_variants_v001.py -- <confirmed-config.json>`. Do not execute in the user's live scene. Builder refuses missing configuration, changed product hash and conservative envelope clashes; it never fabricates BHA/bit geometry. It writes a new local candidate only after gates pass. Then inspect/rework the draft builder, reopen the saved candidate, verify relative libraries, geometry/control/visibility behavior, and export/inspect moving variants. Update the manifest and submit exact candidate/evidence for Radzi review. No approval is inferred from a successful gate.

Incoming assembled/plugged hardware O14 requires new measurements, interface/sensor checks and affected mechanism/shot reverification. No automatic dimension or datum correspondence is assumed.
