# MIT / ECCO — Production Workflow

**Version:** 0.2 routing update · 14 October 2026  
**Sole owner:** Blender asset structure, reference-generation/AI finishing process, QC and actual output records. For design decisions, read [MIT identity](03-MIT_PRODUCTION_IDENTITY.md), [Engineering Baseline](02-ENGINEERING_BASELINE.md) and [Rolladice Scene Contract](../03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md). For content use [Storyboard V2](../02_Storyboard/README.md).

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

The repository presently contains the client chat, ENP3 PDF and still images. It does not contain the registered production CAD, Blender shot files, motion references, selected generated videos or accepted quote export. The repository **does contain V1/V2 storyboard panel assets and V2 notes**; no synchronized live Padlet snapshot or approvals have been verified. The producer reports that a product model and sample animation exist locally; their locations and versions remain to be registered.

| Asset group | Present record | Needed before use |
|---|---|---|
| ECCO ENP3 | Photos/PDF in `01-Brief`; local model reported | Actual CAD source/version, units, imported geometry, approved modifications and sensor plane |
| Rig, earth and drill assembly | Narrative planned | Local file paths, scale and deployment scenario |
| Open-hole / casing / cement | Technical concepts sourced | Compatible dimensions, approved scenario and reusable variants |
| Sensing / reveal / background | Four-second test reported | Exact `.blend`, playblast and selected final-anchor/video versions |
| Hydraulic flow / cuttings | Datasheet describes stages | Faithful pads and selected operating mode; editable illustrative controls |
| Output graphics / Mi-VU | ENP1 report previously discussed | Verified source, permission, labeling and location |
| MIT branding | Brochure contains a visible logo | Official artwork, type/color constraints and approved end-card text |
| Generated references | `02-Reference` | Label by intended use; do not treat generated design as CAD authority |

Keep media at their actual local or controlled external locations. Record portable relative project paths where available and the relevant version/hash; do not invent paths. Respect the repository's existing exclusions for videos, heavy borehole reports and STEP/IGES assets.

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
