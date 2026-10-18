# T44 — surrounding formation revision for review

18 October 2026 · revision v005 · **revised image approval pending Radzi**. Prior T44 work was marked Done by the owner; this covers the additional visual revision in the discussion. [Previous report](report_v004.md) and every previous master/consumer remain preserved.

**Result:** reusable surrounding rock now fills the foreground, sides and background. Five full-size saved-candidate images are the primary deliverable: [wide rig/earth context](Previews/Revision_v005/wide_context_working_v007.png), [downhole A](Previews/Revision_v005/downhole_A_working_v006.png), [nearby downhole B](Previews/Revision_v005/downhole_B_working_v006.png), [steel/cement/formation](Previews/Revision_v005/layers_working_v010.png), and [BHA/bit/adapter detail](Previews/Revision_v005/BHA_detail_working_v006.png).

[Overview](Previews/Revision_v005/approval-overview_v005.jpg) · [image notes](Revision_v005/review-guide.md) · [shared usage/controls](../../../Shared/Assets/World/README_v002.md) · [native versions/hashes](../../../Shared/Assets/World/manifest_v005.json).

## Review decision

Judge surrounding-ground depth/coverage, tactile rock/fluid treatment, metal detail, layer distinction and simplified bit/adapter appearance. Both nearby downhole images have255 alpha throughout: no studio pixels. This supports coverage, not automatic appearance approval. Source bore/hardware were not enlarged. No new concept, movie animation, sensing/flow effects or film assembly was produced. Radzi alone approves these images.

## Shared implementation and verification

- Environment v005:18 m axial /4.8 m transverse coverage; six nominal/irregular/spiral × full/cutaway masses, relief outside the bore, wet mineral shading and a static optical fluid section. Exact registered T6 inner wall/casing/cement meshes remain unchanged.
- Context v002 and surface v003: shared earth/strata/seafloor section and unchanged owner-designated rig geometry, with a deliberate near water cutaway. Depths/strata/riser arrangement are illustrative.
- Cased section v002: shared upper-host-only end reveal. Tool, mud and foreground lower rock are hidden to inspect steel/cement/formation/shoe; dimensions/layer spacing remain fixed. BHA/ECCO film v002 and sensor references are unchanged.
- Two old consumers migrate v004→v005 through the same library reload procedure with cameras, timing and local controls identical. [Rendered proof](Previews/Revision_v005/propagation_v005.jpg), [migration A](Revision_v005/Evidence/migration_A_v005.json), [B](Revision_v005/Evidence/migration_B_v005.json).
- **62 native/source/geometry/control/fresh-open checks pass**: prior hashes preserved, ten source layer/wall meshes exact, added mass outside the bore, controls select one matching mass, relative libraries resolve and one product remains where shown. [Native checks](Revision_v005/Evidence/native-verification_v005.json) · [package/image checks and timings](Revision_v005/Evidence/package-verification_v005.json).

## Render evidence

Blender5.2.2, EEVEE/Vulkan,1280×720 /24fps /16 samples, ray tracing/compositor off, AgX Medium High Contrast. Lighting/exposure are saved. Every image is rendered individually from a freshly reopened candidate; timers include the complete first render through PNG writing, excluding process/file loading and no warmup render.

Final approval images take approximately1.23–2.32 s/frame. Initial new-shader test4.04 s also passed; all revision samples are below5 s. **Normal existing GPU caches are required for this measured result.** The original empty-cache startup12.55–25.13 s remains disclosed in prior evidence. Cache/backend/driver/machine/material or heavier-shot changes require a new benchmark before batches; any sample≥5 s stops the batch. No cap waiver or universal cold-machine guarantee.

## Authority and scope

T44 ID `b77297cc-0600-4a17-8fb9-ba95cc3d6220`, active MIT ECCO `a0b9b971-e282-42f0-a25f-0c78729eff87`. User instructed this chat to read the discussion and work autonomously. Controlling comments `19ea2372-2aa4-4b78-8ba6-ac46272b843f` and `69a691b5-d597-415c-9b59-7e8f0a2696f3` require surrounding coverage, neighboring views and approval images. They describe two reference images; new reference pixels were not returned as Work attachments. T43/V3, actual native sources and the explicit spatial requirements governed this revision, not generated tool anatomy or clearance.

Fresh handoff: T42/T43 Done, current production standard revision1. Reopened only this requested revision; run `60e85272-1228-42ad-8ebd-340346c58fae`, worker `codex-a-world-t44-formation-20261018`. Git base `86bbab19ed1cdc10a3961a97f795ffbdecaf0c09`, main, authorized origin `radz2291/Project-MIT-Ecco`.

The live v004 scene was inspected clean and preserved during background work. Exact native paths/hashes/camera versions are in the manifest under local root `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco/04-Production/`. Native media stay ignored/local; no off-machine backup/upload is claimed. Source sensor-face/interface, actual BHA/thread/shoe and O04/O05/O14 limits remain; executor checks do not certify engineering.

Visual QA corrected framing/exposure, macro seafloor closure, foreground layer masking and section-cap indexing. Initial iterations remain local and superseded; only manifest-listed candidates are submitted. Individual images, not the checklist or tiny overview, are the primary acceptance deliverable.

## Closure and next action

Permitted scripts/records/JSON and five individual stills plus overview/proof JPGs synchronize for review. Exact remote commit/parity and commit-pinned report attach to T44 after push. Native files/raw iterations/logs remain organized locally; unrelated imagery is preserved. [Consumer map](Revision_v005/component-consumers_v005.json) identifies actual tests and affected future V3 IDs; no movie shot is falsely reported migrated. No downstream ticket was started.

Radzi reviews these five images and exact candidates. Later authorized builders link the approved environment, use the extent/cutaway/axis controls and benchmark their actual shot states.
