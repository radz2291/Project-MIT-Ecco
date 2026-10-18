# Build order for the V3 film

P01 proposes the following work after Radzi reviews the component register. These are proposal labels, not live tickets. No downstream work has been created or started.

## Next ticket

**D-FILM — Resolve shared visual decisions and write V3 shot instructions**, assigned to a separate AI directing agent. It consumes this inventory, the live V3 board, Scene Director skill and Directorial Identity. First resolve the shared decisions below, then complete one instruction contract per shot. It should preserve the source direction while supplying executable choices within the render budget. Radzi reviews treatments; the Blender executor implements the released instructions.

D-FILM is first because rig setting, hardware visibility, pulse/flow distinction, data display and branding affect more than one build. Release instructions by component/shot as they become ready rather than waiting for all 22 contracts. This is not a reinstated editable 3D storyboard gate.

## Proposed build tickets

| Proposal | Bounded output | Dependencies for execution | Completion evidence |
|---|---|---|---|
| A-WORLD | Refine BHA/bit and environment wrappers; register existing ECCO; surface context and well-fluid treatment; shared source axes and interval boundary | P01 review; relevant D-FILM choices; current T5/T6 sources | Fresh-open links, one product instance, source hashes, whole-assembly motion, visible clearance/order, surface/downhole continuity and representative render timings |
| A-SENSING | Extract B201 acoustic event controls; wrap B202 data/replay and nominal/independent strength channels; supply timing-graphic hooks | P01 review; D-FILM sensing treatment; A-WORLD interface for integrated verification | Same-emitter return, constant propagation to contact, wall-fixed samples, independent channels, validity/cutoff, one-plane ring and benchmark; preserve existing data |
| A-CASED | Integrate B203 support/channel/wear with real product and shared casing; refine shoe/interval context | A-WORLD released interface; D-FILM cased instructions; A-SENSING event interface where used | Upward order, supported/poor-support interpretation, outside axial channel, fixed exterior wear check, qualitative signal labels, benchmark |
| A-FLOW | Film-ready illustrative annular flow/cuttings around source-supported stages; shared mode and flow direction | A-WORLD; D-FILM hydraulic choices; resolve material stage-map uncertainty or approve a bounded explanation without unsupported face claims | Mode/direction checks, geometry/path clearance, stage attribution, graphic distinction from sound, no invented CFD legend, benchmark |
| A-OUTPUT | Build deterministic 3D-to-2D data mapping, shared graphics/capability package, register permitted evidence and supplied brand assets | A-SENSING data interface for unwrap; D-FILM graphics/brand choices; permitted content decision for S06-C | Sample ID/seam/depth/color correspondence, separate amplitude, truthful demo/real identity, text/brand checks, benchmark |

Do not create a separate asset ticket for each minor object. Split these proposed packages only if actual ownership or scope requires it. A-WORLD can release the existing product interface before completing surface scenery. A-OUTPUT can develop the demonstrator/mapping while real-output permission is pending, but must not claim an authentic field-evidence result.

## Actual shot work

Create **one shot execution ticket per V3 shot** when its required components and director contract are released. The [shot map](shot-map_v001.json) supplies exact component dependencies and source seconds. Each ticket delivers its own editable scene, render, boundary stills, verification, component/version manifest and transition notes for Radzi. No film-assembly ticket belongs to an agent.

Suggested release order:

1. S02-A/B/C first to settle the common sensor/wall/event/data interfaces; follow with S01-C and S03-A/B/C so adjoining cuts can be checked.
2. S01-A/B after surface context is selected. S04-A/B/C/D after cased assets and instructions are ready.
3. S05-A/B/C after stage/direction/mode questions are bounded.
4. S06-A/B after data mapping, then S06-C and S07-A after output identity is settled.
5. S07-B/C after shared hero/graphics/brand decisions. Product-only setup can proceed sooner if released.

This order is a proposal, not authorization to start. Shot dependencies should reference released shared assets and necessary adjacent boundary states, without chaining every unrelated shot. Stage-shared checks protect continuity; Radzi remains the sole film assembler/editor and owns narration, sound integration, final timeline and client feedback.

## Decisions that change the next work

| Decision | Owner and scope | Affected work |
|---|---|---|
| Offshore or other surface setting; visible rig/BHA/bit/shoe detail | AI director proposes; Radzi chooses. Existing simplified production baseline remains usable. | A-WORLD; S01-A/B and S04-A |
| Pulse/contact/arrival-time language, fluid appearance and common graphic system | AI director with Radzi; preserve client C02 and quantity semantics | A-SENSING, A-OUTPUT and associated shots |
| Exact CAD hydraulic stage/end mapping and selected operating mode | Asset executor inspects sources; Radzi obtains only material MIT clarification; director bounds the depicted treatment | A-FLOW, S05-A/B/C. C08 analysis request stays explicit; no fabricated FEA substitute |
| Permitted real/redacted output versus explicitly labeled demonstration | Radzi obtains permission/content and approves truthful alternative | S06-C/S07-A; no ENP1 relabeling or confidential screenshot reuse |
| Icon-only or full original MIT mark; end wording/hold | AI director proposes; Radzi/client resolves brand choice | S07-C |
| Working output profile and frame rate for Radzi's edit | Radzi with director/executor; initial benchmark proposal below | All shots; final delivery settings remain O02 |

Existing sensor-face/datum uncertainty matters for close sensing/claims. Incoming plugged hardware does not block all production: retain accepted v002, inspect any replacement and reverify affected consumers. No new request for a complete client BHA is needed.

## Render benchmark and batch gate

Current authority requires **every sampled frame strictly below 5.000 seconds** on the executing machine at the chosen shot settings. No average can hide a failure. P01 performs no rendering and makes no speed claim.

Proposed first working test: Blender 5.2.2, EEVEE (`BLENDER_EEVEE`), 1280×720 at 100%, 24 fps, square pixels, low initial sample count (16), with the actual proposed compositing and effect stack. This is a test starting point, not an accepted film profile. The older 1080p/24fps profile was a proposal; Radzi's edit needs one agreed output profile. Record GPU/CPU, driver, engine, samples, shadows, transparency/volume settings, color management, resolution, fps, machine load, native SHA and full dependency manifest.

For each saved shot candidate, choose entry, reveal/contact, peak visible geometry/effects, maximum transparency/overdraw/particles, and exit. Add any frame identified as heavier by the executor. In particular test:

| Shot family | Representative and likely expensive state |
|---|---|
| S01 | Rig/water/strata overview; longest visible geology and fluid depth |
| S02 | Pulse-wall contact plus return and timing overlay; fullest circumferential points |
| S03 | Longest reconstructed wall/spiral; geometry/reference overlap; full amplitude surface |
| S04 | Tool at shoe with all layers; overlapping steel/cement/channel reveals; wear comparison |
| S05 | Highest flow/cuttings density at twisted pads; widest integrated body view |
| S06 | Complete reconstructed surface; halfway unwrap with two maps/graphics; final output screen |
| S07 | Largest metal close-up with specular/lighting effects; maximum capability graphics; final logo |

Measure a cold first render and at least two repeat renders per selected frame. Time each full render-to-written-frame operation, including compositor; report process start/load separately. Count cold render shader work rather than silently dropping it. Save per-frame timings, native/settings hashes and the exact resulting frames. Inspect images for readability and defects before release.

If **any** sampled render is 5 seconds or slower, reduce cost and repeat the failing and affected representative samples. Candidate reductions: invisible geometry, distant detail, texture cost, effect density, transparency overlap, volumes, shadows/samples; resolution changes need a recorded working-profile decision. Preserve engineering meaning and director intent. A different machine, material/effect/compositor change or meaningful asset revision invalidates affected timings. Log per-frame batch timing too; stop and revise if the cap fails during the batch.

## Handoff and client revision loop

Each shot supplies local frame range, seconds, nominal master in/out, color profile, exact component versions, entry/exit state and agreed handles. At proposed 24 fps, local frame 1 starts the shot and duration × 24 is the inclusive end; handles stay outside the 90-second content budget. Seconds in V3 remain authoritative until frame rate is agreed.

Radzi assembles the 22 shots, adds narration/sound and owns the final timeline. Feedback identifies shot/version/time and whether it changes direction, a local implementation, or a shared asset. Shared changes follow the consumer propagation procedure; local fixes remain shot-local. Agents return revised individual shots and evidence for review. No automated client contact, final acceptance or delivery is implied.
