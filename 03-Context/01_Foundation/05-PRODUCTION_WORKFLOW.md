> **HISTORICAL WORKFLOW — superseded 18 October 2026.** Do not execute the old phases, gates or ticket assignments below. Read [current production cycle](../../04-Production/README.md) and the active MIT ECCO Work project (`a0b9b971-e282-42f0-a25f-0c78729eff87`). The V3 cinematic board guides separate AI-director instructions, shared assets and actual fast-render shots (<5 seconds/frame). Radzi alone assembles the film. Prior work/evidence is retained as history.

# MIT / ECCO — Production Workflow

**Version:** 0.3 mechanical-first execution update · 15 October 2026  
**Sole owner:** Blender asset structure, reference-generation/AI finishing process, QC and actual output records. For design decisions, read [MIT identity](03-MIT_PRODUCTION_IDENTITY.md), [Engineering Baseline](02-ENGINEERING_BASELINE.md) and [Rolladice Scene Contract](../03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md). For content use [Storyboard V2](../02_Storyboard/README.md).

## Development order

Operating integration and local output organization were authorized by Radzi on 15 October 2026. The detailed task roadmap remains provisional except where a specific execution instruction authorizes a bounded ticket; no engineering, schedule or film acceptance is inferred.

| Stage | Required result |
|---|---|
| A — Production readiness | Source/scope reconciliation, actual asset inspection, shot/blocker inventory and confirmed preview conventions |
| B1 — Mechanical foundation | Reusable validated product and compatible well/assembly assets |
| B2 — Mechanism development | Standalone moving demonstrations of sensing, scanning/reconstruction, casing, hydraulics and unwrapping |
| B3 — Shot blocking and animatic | S01–S07 shots using those mechanisms, actual cameras/timing/transitions and a complete moving preview cut |
| B4 — Mechanical and technical lock | Recorded MIT feedback and Radzi acceptance of the exact corrected mechanical film; retained critical mechanical/technical/source blockers closed or explicitly removed from scope |
| C — Visual finishing | Materials, lighting, controlled render/AI finishing and precise finished graphics derived from the accepted film |
| D — Final review and delivery | Editorial/sound polish, client review, verified exports and agreed editable-source handover |

B2 tests whether the mechanism works; B3 tests whether a shot communicates it. Build non-blocked work progressively and seek early targeted feedback on high-risk interpretations. B2/B3 may overlap when their dependencies are satisfied. No repeat AI-finishing pilot is required now. Workbench/grayscale with semantic colors is appropriate; show real motion rather than static storyboard placeholders. Final finishing follows B4.

Rolladice Work owns current assignments, dependencies and execution records. Follow the [production workspace](../../04-Production/README.md) for folders, run lifecycle, agent/human responsibilities and mandatory cleanup/evidence at closure. Agents prepare and correct; Radzi directs, communicates with MIT and accepts. Rework must update affected source assets, shots, previews and review evidence.

## Division of control

| Layer | Responsibility |
|---|---|
| Approved technical references | Mechanism, claims, physical constraints and data identity |
| Blender | Product geometry, spatial layout, camera, motion, effect causality and timing |
| AI-finished boundary stills | Intended material, lighting, environment and opening/ending appearance |
| AI video | Proposed finished motion between the supplied states; subject to fidelity review |
| Compositing / editing | Exact graphics, recoverable hardware details, sound, narrative and final assembly |

Build the minimum editable 3D structure that makes the visual event unambiguous. Add rendering complexity when it solves an observed problem. The reference animation should communicate without requiring a long prompt to explain unclear geometry.

## Current asset map

The [A02 asset manifest](../../04-Production/Records/asset-manifest_v001.md) owns the inspected asset inventory as of 15 October 2026. The actual local checkout contains the client chat, ENP3 PDF, photos/videos, original ENP1 log, prior motion-reference MP4s and a Git-ignored STEP in Shared/Assets. Earlier saved Blender candidates were located and inspected in the previous local projects; no approved production master or selected final AI video is declared. Governing commercial PDFs are registered in T-001. V1/V2 storyboard presence still does not establish a synchronized live Padlet or technical approval.

| Asset group | Present record | Needed before use |
|---|---|---|
| ECCO ENP3 | STEP and earlier imported mesh registered by A02; photos/PDF in `01-Brief` | B101 technical reconciliation: 2.400 m mesh vs nominal 2.25 m, datum, latest revision, mud sensor and presentation additions |
| Rig, earth and drill assembly | Narrative planned | Local file paths, scale and deployment scenario |
| Open-hole / casing / cement | Technical concepts sourced | Compatible dimensions, approved scenario and reusable variants |
| Sensing / reveal / background | Earlier 7 s First Ping and 4 s transformation scenes/media registered by A02 | Approved reuse and technical/creative reconciliation; selected final AI outputs not established |
| Hydraulic flow / cuttings | Datasheet describes stages | Faithful pads and selected operating mode; editable illustrative controls |
| Output graphics / Mi-VU | Original local ENP1 report identified and inspected by A02 | MIT/operator permission and exact approved/redacted version/caption; no ENP3 relabeling |
| MIT branding | Brochure contains a visible logo | Official artwork, type/color constraints and approved end-card text |
| Generated references | `02-Reference` | Label by intended use; do not treat generated design as CAD authority |

A02 inspected the working checkout `C:\Users\RZ1\Desktop\RZ\261013-MIT-Ecco`; Shared/Assets contains the registered STEP and README. Preserve existing supplied sources at registered locations until deliberately imported into validated masters. Save new production outputs under `04-Production/` using the workspace conventions. Record relative paths and versions/hashes. Respect exclusions for videos, heavy reports, CAD and local Blender/media files; local saving does not authorize GitHub publication or imply backup.

## Modular Blender architecture

This is the planned architecture, not a list of files already created:

| Library asset | Owns |
|---|---|
| ECCO product | Geometry, stable materials, rig and documented sensor/connection interfaces |
| Earth / well | Geological context, borehole variants, casing and cement |
| Rig / drill string / BHA | Surface context and compatible drilling assembly |
| Effects | Sensing, reveal, illustrative mud flow and cuttings controls |
| Background | Separate distant parallax geometry |
| MIT identity | Approved logo/end-card graphics where needed |
| Individual shot file | Linked assets, shot animation/overrides, camera, lighting and reference render settings |
| Final edit | Shot assembly, exact typography/diagrams, voice/music/SFX and delivery versions |

Use linked library assets and suitable overrides so a product correction can propagate across shots. Keep shared geometry changes in the source asset; shot-specific animation in the shot. Validate units, linked paths and interface names before reuse. Do not collapse all product, well, effects and cameras into one unmaintainable file.

## Per-shot execution

Steps 1–3 are the mechanical/blocking work. Assemble and inspect all retained sections as a full mechanical animatic and obtain B4 acceptance before applying steps 4–7 as finishing. The detailed shot checks still apply; assembly at preview quality is part of B3, not deferred until finishing.


1. **Receive directed shot.** Use the [Scene Direction Contract](../03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md) for one technical point, source, initial/final state, camera/lighting and unresolved questions. Do not independently redefine the creative brief.
2. **Build the motion reference.** Correct hardware, camera, parallax, occlusion and essential effect timing. Distinguish the tool, travelling effect, local borehole and distant background.
3. **Review the technical preview.** Check geometry and meaning internally, then obtain MIT's answer on any mechanism or claim needing acceptance. Record the version.
4. **Choose boundary controls.** For a continuous shot, select first, last or both according to the opening identity and intended final reveal. Generate finishing stills from those exact Blender frames; match their finish.
5. **Generate and review.** Use the full motion reference and selected appearance anchors wherever supported. The prompt describes the finish calmly and identifies the reference's authority. A mid-frame beauty still can aid look development without becoming a generation anchor.
6. **Correct observed failures.** Fix ambiguous reference geometry in Blender; adjust finish/conditioning for a clear reference that drifts. Composite exact hardware/graphics where needed, or use a controlled render for shots that fail fidelity requirements.
7. **Assemble and verify.** Check the shot in the full edit for narrative, product continuity, technical meaning, branding and sound.

**Boundary-frame finding:** Radzi's experiments favored first/last appearance anchors over isolated middle anchors for continuous single-camera animation. Independent middle images were hard to keep consistent and made the beginning/ending less controlled. Add middle anchors when reliable continuous appearance consistency makes them useful. For multi-camera edits, apply the rule separately to each shot; a middle timeline frame may be another shot's boundary.

## Prototype findings and provenance

The [Visual Decision Casebook, V03](../03_Directorial_Identity/04-VISUAL_DECISION_CASEBOOK_v0.2.md) owns artistic comparison of meaningful sensing versus decorative rings, cage-like clutter and nonpersistent reveals. **Do not duplicate those aesthetic decisions here.**

Production observations retained here: curved distant geometry can help parallax when distinguished from the local borehole; concise and calm finishing prompts worked better than verbose constraint-heavy ones in the ECCO experiment. These are empirical heuristics, not universal AI guarantees. Attractive renders are workflow outputs, not independent proof of acoustic physics or cost/temporal fidelity.

## Minimum review record

For each shot, retain the Blender version, reference video, chosen anchor frames, generation platform/model/settings and prompt, attempt count, selected output and corrective work. Record elapsed time and credit cost when available. Compare source and result at the boundaries and at the event's important moments; track camera, silhouette, sensor origin, effect contact, reveal timing and ending state.

Export product/effect masks, depth or useful passes when practical. Use them to preserve exact features instead of accepting an AI redesign. Add precise labels and logo artwork in the edit. Final delivery settings and source-file handover follow the accepted quote once verified.
