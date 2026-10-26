# ECCO-049 — Component selection review

27 October 2026 · **C03 proposal recorded for Radzi; report only** · documentation only

Keep the completed seven-section previs as the visual baseline. The product shape is already consistent: the housing mesh matches the shared source across every section that contains it. The useful selection is mainly which finish, environment and behavior should become reusable later.

**Recommended starting choice:** retain film ECCO v002 and connected BHA v007 as geometry references; retain S05's approved amber flow and S07's clean satin finish as appearance references; keep camera-dependent cutaways, lighting, reveals and data cases local. **Radzi requested that the report propose: combine the well environment and formation into one modular shared environment.** No consolidation or scene migration has begun.

## C03 — owner-requested report proposal

Combine the existing well environment and surrounding formation into one reusable environment master. Give it separate controls for rock, borehole shape, casing, cement, mud and wider earth context, with optional surface context when needed. Casing, cement, channel and wear objects are physical subcomponents of this environment (C04 detail), not a separate peer environment asset. Pulse/response demonstration animation is documented separately from those objects. Scenes select the modules, extent, detail and visibility they need instead of carrying independent overlapping environment builds.

This replaces C03's earlier blanket **keep local** recommendation. Keep each approved scene's camera, lens, timing, motion, local lighting and viewing cutaways while adapting it to the future master. Existing sources remain preserved. The shared master is a later build deliverable; compatibility through each locked shot must be checked before adoption. S03/S06 illustrative data and reconstruction remain separate from the physical environment.

The owner explicitly instructed: report only; do not combine yet. No implementation is authorized. Recorded instruction: [owner-decisions.json](owner-decisions.json).

- [Hardware and world comparison](Images/02-hardware-and-world.jpg)
- [Sensing and casing comparison](Images/03-sensing-and-casing.jpg)
- [Flow and data comparison](Images/04-flow-and-data.jpg)
- [All seven sections](Images/01-seven-section-baseline.jpg)
- [Exact image/source index](image-index.md) · [Native sources and acceptance](source-index.md) · [Detailed inventory](inventory.md)

## Component choices and proposals

| Component | Proposed choice | Reason / effect |
|---|---|---|
| C01 — ECCO body and closures | **Retain** | One product shape already underlies the film. Keep each approved material/camera treatment while selecting a reusable finish separately. |
| C02 — Connected BHA, bit and joints | **Retain / keep local** | Keep v007 as the reusable connected assembly; preserve current simple/local string and all existing cropping until a component is explicitly selected. |
| C03 — Well environment: formation, borehole and cased-hole parts | **Propose one modular shared environment — report only** | Group the physical environment objects together: surrounding rock, borehole, casing, cement, channel and wear geometry, mud and wider context. Scenes would select required modules from one shared environment. |
| C04 — Cased-hole parts — subcomponents of C03 | **Part of the well environment — report classification only** | Casing, cement, the exterior channel and inner wear are physical parts or conditions of the well environment, so classify them under C03 rather than as a separate peer environment asset. The support-response animation demonstrates these objects; it is not the physical asset itself. |
| C05 — Fluid, metal finish and lighting | **Polish proposal / keep local** | Select a common metal/amber direction through actual locked views before extracting shared materials. Keep lights, opacity and optical cutaways local. |
| C06 — Pulse, contact, echo and acquisition | **Retain shared semantics / keep scores local** | Retain shared packet/contact prototypes for future reuse; preserve S02's accepted event order and pixel-wall build instead of replacing its animation with a four-second asset demo. |
| C07 — Hydraulic flow and cuttings | **Retain S05 / combine interface later** | The current richer amber treatment was approved. Later extract S05 behavior behind stable visibility/speed controls, rather than reinstating the older sparse demo. |
| C08 — Reconstruction, amplitude, map and report | **Keep local / combine conventions later** | Share quantity/color/seam conventions only after selecting compatible data contracts; retain case identity and native transformation behavior. |
| C09 — Labels, studio hero and ending | **Keep local** | Retain each approved information beat; a global HUD/branding package would change the current direction. |

## Choices left for joint review

1. Use S07 satin metal as the common appearance reference while keeping per-shot lighting and S04 transparency, or retain all finishes separately?
2. Extract S05's approved rich amber behavior into a later shared package, or keep it local? The earlier T48 sparse flow remains a control/clearance reference, not an automatic replacement.
3. Keep S04's selected v033 look, or scope a later correction for its known dark-band/pit impression? Rejected v034 is not a replacement.

These are pending selections, not permission requests to continue this ticket. No polishing, relinking, rebuilding, retiming or downstream task creation has begun.

## Safe consolidation order — proposal only

1. Record Radzi's selected components and immutable source hashes. Preserve every approved scene/movie and the current camera, lens, motion and event score.
2. Register geometry identities first: ECCO/closures, then connected BHA/bit/joints. Keep local display wrappers distinct from source geometry; do not delete apparent duplicates based on datablock counts.
3. Plan the proposed C03 modular environment: reconcile overlapping rock/casing/cement sources, use one declared axis/unit convention, and provide selectable layers, borehole variants, near/wide extents and detail controls. Preserve existing source versions. Keep approved scene cameras, local lighting/cutaways and data cases intact; migrate only in a later released build after affected-shot checks. Material controls and S05 flow remain pending selections.
4. Reopen copies through every affected locked camera at entry, exit, reveal, close-up and heaviest frames. Check silhouette, cap origin, bit order, occlusion, finite flow/particle clearance, layer order, world-fixed history, geometry/amplitude separation, seam/colors and neighboring cuts. Compare camera/lens/animation hashes and timing before and after; benchmark complete writes strictly below 5 seconds/frame before a batch.
5. Return those later replacement versions to Radzi. He alone updates film assembly. Keep old consumers unmigrated until their checks pass.

Section allocations currently total **96 seconds** (10/12/18/18/18/12/8). S05's approved 18 seconds supersedes its old 12-second plan. The S02 review movie also contains three seconds reused from S01; do not add that overlap twice. No edit or retiming was performed.
