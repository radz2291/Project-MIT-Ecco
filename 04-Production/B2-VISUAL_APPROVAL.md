# B2 — Visual direction before Blender execution

Updated 16 October 2026. Owner-authorized workflow: **one bundled visual-direction ticket, T26 / B200**, covers T7–T11. This supersedes earlier instructions asking individual Blender executors to discover their own visual treatment or limiting the still-first trial to T7.

## Sequence and ownership

1. **T26 — discuss, interpret and direct.** A separate visual-direction agent works with Radzi on engineering meaning, cinematic treatment and near-final AI-generated reference images. Iterate here while changes are cheap.
2. **Radzi approves the reference package.** Save exact approved frames, brief beat annotations and the existing Scene Direction Contract for each mechanism. Complete the bundled T26 package for human acceptance.
3. **T7–T11 — implement the approved package in Blender.** These execution tickets depend on T26, retaining their original technical dependencies. Preserve prior work and implement the selected visual language, not a fresh artistic exploration.
4. **Check implementation stills, then animate.** Verify actual geometry, occlusion and visual correspondence in representative stills; obtain Radzi's implementation approval before motion. This is a fidelity/feasibility check, not another visual-discovery phase.
5. **B3 — develop shot choreography and edit.** Reuse the approved direction and constructed scenes for camera movement, timing and transitions. Final rendering/AI finish remains later.

No Blender build or heavy render is required to develop the reference package. Read existing scenes/reports if useful for feasibility; do not mutate execution assets inside the direction ticket. Do not start B2 execution simply because generated images look attractive: Radzi must approve the exact package and the recorded dependencies must be satisfied. For now T26 is one bundled dependency; partial image approvals are preserved but do not silently bypass that task dependency.

## Immediate T7 starting point

Owner confirms **Still 1 and Still 2 approved**. Reuse, do not redesign:

- Sensor-origin: [Still01 v004](https://github.com/radz2291/Project-MIT-Ecco/blob/7dce0b86ec31267c9731667f912342cf028ff0cb/04-Production/Mechanisms/B201/Previews/Still_01/B201_sensor-origin_still01_v004.png), with [proposal](https://github.com/radz2291/Project-MIT-Ecco/blob/7dce0b86ec31267c9731667f912342cf028ff0cb/04-Production/Records/Tasks/T-007/still-proposal_01_v004.md).
- Outgoing/spreading pulse: [Still02c v001, approved translucent 3D wavefronts](https://github.com/radz2291/Project-MIT-Ecco/blob/079ed4b274a26eff70f6a4e5338a7f781f9dbca3/04-Production/Mechanisms/B201/Previews/Still_02c/B201_spreading-pulse_still02c_v001.png), with [approval record](https://github.com/radz2291/Project-MIT-Ecco/blob/079ed4b274a26eff70f6a4e5338a7f781f9dbca3/04-Production/Records/Tasks/T-007/Evidence/Still_02c/approval_still02c_v001.json).

Begin T26 with the three remaining visual beats, discussing one concrete proposal at a time:
1. Wall interaction — the pulse reaches the borehole wall.
2. Returning echo — sound returns to the same sensor.
3. Waveform connection — link that return to the displayed signal and distance measurement.

Their visual treatment is unapproved. Do not ask the T7 Blender agent to experiment on these while direction is being developed. Preserve its existing assets/technical work; T7 remains incomplete, not cancelled or accepted.

## Reference-package expectations

Read [Directorial Identity](../03-Context/03_Directorial_Identity/README.md), [Scene Director skill](../03-Context/00_Skill/rolladice-scene-director/SKILL.md), relevant modules and engineering sources. The mechanical storyboard supplies mechanisms, beats and client corrections; it is not the final layout, visual metaphor, camera plan or engineering proof.

Use AI-generated reference images close enough to the intended final appearance to resolve visual choices, especially VFX. Existing approved images may establish the language; generate only what resolves the next real choice. Work with Radzi before multiplying proposals. These images are appearance/direction references, not automatically first/last video-generation anchors.

For each mechanism, keep one concise package using the existing Scene Direction Contract:
- Objective, required information beats and engineering sources.
- Exact approved image versions and approval evidence. Preserve full-size reference files where available, provenance and any source-only access limits; a chat thumbnail alone is not a portable handoff.
- Annotations explaining what is approved: VFX form, thickness, spatial scale, transparency, falloff, origin, contact/return response, framing, depth and information placement as relevant.
- Which aspects must match, which are implementation choices, and known generated-image errors or unsupported features to correct in actual geometry.
- Explicitly sourced, inferred or illustrative physical/data elements and consequential unresolved questions.
- A short visual/technical checklist, executor inputs and intended mechanism output.

Store under `04-Production/Direction/B2/B201/` through `B205/` with a compact index/coverage matrix at `Direction/B2/README.md`. Update the existing direction contract instead of creating competing shot specifications; link prior mechanism contracts and preserve their history. T26 evidence/report belongs under `Records/Tasks/T-026/`. Follow permitted-file commit/push and Rolladice closure rules.

## Coverage across B2

| Executor | Direction to resolve before implementation |
|---|---|
| T7 / B201 | Sensor origin, outgoing wave, wall interaction, same-sensor echo and waveform/distance connection; preserve the first two approved stills |
| T8 / B202 | On-model scanning, accumulated samples and reconstruction through depth; geometry versus amplitude, nominal/enlarged/tight/spiral meanings |
| T9 / B203 | ECCO within casing; cement/channel/wear examples and readable cutaway-to-map correspondence, with inference limits |
| T10 / B204 | Fluid/cuttings appearance and behaviour around real pad/annular geometry; supported accelerator/twisted-pad/diffuser mapping |
| T11 / B205 | Spatial measurements becoming an unwrapped map while depth, azimuth, seam and color meaning stay coherent |

Source understanding constrains visual choices. A generated image cannot validate acoustic physics, exact sensor faces, hydraulic stage-to-CAD mapping, signal/material inference or calibrated field results. Investigate critical correspondence first; mark an inference or propose a supported simpler explanation instead of inventing engineering to match attractive imagery.

## Execution boundaries

Blender agents choose rigging, geometry implementation, controls and procedural methods after inspecting actual assets. They reproduce the approved explanation and preserve its defining visual features. If it cannot work spatially, return a concrete feasibility issue and the smallest corrective still proposal to T26/Radzi before redesigning. No broad creative exploration or expensive repeated construction to discover taste.

Use actual ECCO/environment geometry, spatially integrated effects and representative static framing for implementation stills. Diagnostic sticks/locators are not approved visible effects. Detached schematics are supporting evidence unless explicitly selected as film graphics. Simple readable shading is acceptable for implementation checks; compare it beside the approved appearance reference rather than silently substituting a different look.

After implementation still approval, animate the selected treatment and verify cause/effect, readability and technical meaning. Material changes to approved visual language return to direction review. Human visual approval is distinct from engineering confirmation and full task acceptance.

## Current release boundary

T26 is created but not executed by this documentation change. T7's first two still approvals remain valid; three remaining beats and other B2 direction packages await discussion. Existing B2 work/evidence is retained. T9/T10's prior workflow holds are now addressed by the concrete T26 dependency, not by requiring T7 itself to finish as a workflow experiment. This change does not claim those tickets' previous work meets the new package.
