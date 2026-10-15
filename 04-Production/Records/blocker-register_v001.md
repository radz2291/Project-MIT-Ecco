# A03 — Production blocker register v001

15 October 2026 · T-003 · Open construction/lock/use dispositions, for Radzi review. **No engineering or rights approval is created here.** Global decisions remain in the [central Decision Register](../../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md). All O references below point there; C references point to the [master feedback register](../../03-Context/02_Storyboard/V2/ECCO_Section_04_Cased_Hole_Padlet_v2/MASTER_CLIENT_FEEDBACK_REGISTER.md).

Categories from roadmap revision 2: **critical mechanical** blocks dependent construction; **technical interpretation** permits provisional tests but blocks lock; **source/approval** blocks affected use/final content; **finishing** does not block mechanics. A technical question may coexist with a critical asset-fit blocker. Unknowns must be supported, corrected, or explicitly removed from agreed scope by the human.

BL01–BL02 are critical; BL03–BL08 and BL10 are interpretation; BL09, BL11–BL15 are source/approval; BL16 is finishing. These records carry exact next actions and exit evidence. They do not duplicate live task acceptance. See [shot inventory](shot-register_v001.md) for moving coverage and affected transitions.

## BL01 — critical mechanical

- **Affected system/shot:** All visible product; S01-02, S02, S04, S05, S06-01, S07
- **Central decision / feedback reference:** O04 / O12
- **Unresolved question:** Which source/model, units, sensor plane, closures and pad geometry are valid?
- **Source/evidence:** Engineering Baseline; A02 v001 A02-01–05/15 arrived in Review before A03 closure: registered STEP/imported mesh; 2.400 m mesh versus nominal 2.25 m; sensor shoulder datum, mud sensor and presentation additions unvalidated.
- **Provisional assumption:** Use no storyboard silhouette as construction geometry; registration is not technical acceptance; do not automatically rescale the candidate.
- **Owner:** B101 executor; Radzi and MIT review
- **Next action:** Consume versioned A02 manifest/evidence, reconcile length datum/revision, validate reusable master/sensors and documented modifications.
- **Exit evidence:** Registered file/hash, units/dimensions, sensor count/plane inspection and MIT-reviewed disputed features.
- **Status:** Open; blocks geometry-dependent construction

**B101 evidence, 15 October 2026:** [T-005 report](Tasks/T-005/report.md) and [provisional v001 interface](../Shared/Assets/ECCO/README_v001.md) now provide a preserved-mesh reusable wrapper, measured 2.400 m length / 0.304800 m maximum axis diameter, separate controls and inherited imaging recess references. Fresh-open geometry and control self-checks pass; this is not MIT acceptance. Length reconciliation, pin-shoulder datum/600 mm offset, acoustic face/mud-sensor identification and current revision remain open. O14 replacement inspection/swap checks are documented, not performed without the file. Independent preparation can use this explicitly provisional reference; unsupported geometry-dependent construction/claims and final hardware lock remain blocked. Do not treat this evidence note as closing BL01 or BL02.

**Temporary closure rework:** Radzi's relayed client request authorizes the [v002 removable visual plugs/covers](../Shared/Assets/ECCO/README_v002.md) pending the assembled STEP. This resolves the temporary presentation omission only; no new engineering decision closes O04/O14. Source housing/v001 preserved; actual closure/face compatibility must be checked when the supplied assembly arrives.

## BL02 — critical mechanical

**T-006 source inspection/preparation, 15 October 2026:** [Report](Tasks/T-006/report.md) and [fit study](Tasks/T-006/Previews/compatibility-study_v001.png) inspect the original three-page ENP3 datasheet, complete brief photo index and relevant chat. Published 12.3in minimum casing ID yields approximately 3.81mm ideal centered radial clearance around the inspected 12in envelope; it is not a selected deployment. Smaller chat examples remain incompatible. Full BHA/bit, casing wall/cement and deployment datums remain absent. [Adjustable builder/configuration preparation](../Shared/Assets/WellAssembly/README_v001.md) is saved, with scene construction gated and unvalidated. BL02/O05 remains open; no dependency or approval bypass.

- **Affected system/shot:** S01-02, S02–S05 assemblies
- **Central decision / feedback reference:** O05
- **Unresolved question:** Which BHA/bit/hole/casing sizes and clearances actually accommodate this tool?
- **Source/evidence:** Baseline conflict: 12-inch max tool OD / 12.3-inch min casing ID versus smaller generic chat examples.
- **Provisional assumption:** Do not build ENP3 in the smaller generic casing examples or invent substitute dimensions.
- **Owner:** MIT via Radzi; B102 executor
- **Next action:** Obtain actual deployment sketch/dimensions, then verify full assembly clearance.
- **Exit evidence:** Approved scenario/dimensions plus versioned fit/clearance checks including bit, shoe and deviated interval.
- **Status:** Open; blocks dependent assembly construction

## BL03 — technical interpretation

- **Affected system/shot:** S02-01/02, S03-03; inherited acoustic graphics
- **Central decision / feedback reference:** O03 / O06
- **Unresolved question:** What exactly is disputed in ping/light, and how should slowed pulse/echo and waveform timing read?
- **Source/evidence:** S02 V2 C02; unresolved sample comment; directorial E016 is taste, not technical approval.
- **Provisional assumption:** Illustrative pulse/contact/same-sensor return only; no visible-speed physics or numeric waveform claims.
- **Owner:** Radzi identifies frames; MIT reviews via B201/B206
- **Next action:** Prepare versioned short test after geometry prerequisites; ask on exact timestamped sample and two-way timing.
- **Exit evidence:** Recorded answer tied to preview/version; same-sensor round trip and interval meaning accepted.
- **Status:** Open; provisional test allowed, blocks lock

## BL04 — technical interpretation

- **Affected system/shot:** S02–S03; S06-01
- **Central decision / feedback reference:** O06
- **Unresolved question:** How do rotating/sliding operation, axial motion, mud correction and samples map to geometry?
- **Source/evidence:** S02/S03 V2; Engineering Baseline and client chat.
- **Provisional assumption:** Whole string rotation clockwise from surface-looking-down viewpoint; rotating drilling includes downward progression; sliding remains separate mode.
- **Owner:** MIT via Radzi; B201/B202 executors
- **Next action:** Review emission-to-wall correspondence, offset/eccentricity and sampling with operating mode explicit.
- **Exit evidence:** Versioned B201/B202 proof and MIT feedback; no radius/amplitude confusion; stationary wall samples.
- **Status:** Open; provisional tests allowed, blocks lock

## BL05 — technical interpretation

- **Affected system/shot:** S03-01–04, S06-01/02
- **Central decision / feedback reference:** O06
- **Unresolved question:** Which color thresholds, spiral meaning and amplitude interpretation are supportable?
- **Source/evidence:** S03 C01/C03; revised P3 caption; module 09.
- **Provisional assumption:** White nominal / blue enlargement / red tight; warm amplitude separate; hypothetical spiral wall shape only.
- **Owner:** MIT via Radzi; B202 executor
- **Next action:** Confirm sample geometry vs spiral, quantity labels and separate mappings.
- **Exit evidence:** Reviewed maps/legend/claims, source identity and explicit numeric thresholds if any; no definitive lithology/oil claim.
- **Status:** Open; qualitative tests allowed, blocks lock

## BL06 — technical interpretation

- **Affected system/shot:** S04-01–04
- **Central decision / feedback reference:** O05 / O06
- **Unresolved question:** Is upward retrieval/inspection and the deviated-well configuration correct for the chosen assembly?
- **Source/evidence:** S04 V2 C04/C05; dimensions remain BL02.
- **Provisional assumption:** Existing upper casing/shoe; upward retrieval after deeper drilling; no casing-installation morph.
- **Owner:** MIT via Radzi; B203 executor
- **Next action:** Confirm operating scenario separately from physical fit; prepare reviewed transition once BL02 closes.
- **Exit evidence:** MIT-approved retrieval/inspection explanation with versioned assembly preview.
- **Status:** Open; scenario interpretation blocks lock; BL02 still blocks fit construction

## BL07 — technical interpretation

- **Affected system/shot:** S04-02–04
- **Central decision / feedback reference:** O06
- **Unresolved question:** What does ringdown support, which channel is shown, and what internal-wear conclusion is permitted?
- **Source/evidence:** S04 C05–C07; baseline cautions.
- **Provisional assumption:** Qualitative supported/free response; axial one-sided water scenario; internal groove with fixed reference OD, not exterior measurement.
- **Owner:** MIT via Radzi; B203 executor
- **Next action:** Review physical cutaway-to-map relation, colors, fluid attribution and measurable wear observable.
- **Exit evidence:** Exact reviewed B203 playblasts and qualified claims; no single-waveform cement/fluid proof or unsupported thickness claim.
- **Status:** Open; provisional tests allowed, blocks lock

## BL08 — technical interpretation

- **Affected system/shot:** S05-01–03
- **Central decision / feedback reference:** O07
- **Unresolved question:** Which hydraulic mode, stage geometry/order and flow behavior should be shown?
- **Source/evidence:** Baseline datasheet-attributed stages; S05 caption warns placement is diagrammatic.
- **Provisional assumption:** Illustrative flow only; rotation, tripping or circulation can act independently; no invented pressure/performance.
- **Owner:** MIT via Radzi; B204/B101 executors
- **Next action:** Confirm pad identities against registered model and select mode/stage explanation.
- **Exit evidence:** Reviewed stage/mode diagram and moving proof, approved claims, no CFD implication.
- **Status:** Open; illustration test after geometry/fit prerequisites, blocks lock

## BL09 — source/approval

- **Affected system/shot:** S05-03 and inherited S05 analysis claims
- **Central decision / feedback reference:** O07 / O12; C08
- **Unresolved question:** Where is MIT analysis and which variable/run/conditions may be shown?
- **Source/evidence:** Master feedback C08 holds hydraulic P5; A02 v001 A02-12 reports no analysis source found in its bounded search.
- **Provisional assumption:** Hold analysis use; do not recreate simulation-looking results as MIT FEA.
- **Owner:** Radzi obtains MIT media; MIT confirms variable/rights; B204 integrates
- **Next action:** Obtain original video/frames/data and metadata, or human decision on explicit illustrative alternative.
- **Exit evidence:** Versioned permitted media, variable/units/range/conditions and approved integration; or dated agreed replacement/removal of analysis portion.
- **Status:** Open; blocks affected analysis use/final content

## BL10 — technical interpretation

- **Affected system/shot:** S06-01/02
- **Central decision / feedback reference:** O06 / O08; C09
- **Unresolved question:** How should recorded measurements, reconstructed surface, seam and axes correspond?
- **Source/evidence:** S06 V2; module 09; B205 pending.
- **Provisional assumption:** Later memory retrieval/processing; axial seam in representation only; azimuth horizontal/depth vertical; geometry and amplitude independent.
- **Owner:** MIT via Radzi; B205 executor
- **Next action:** Test landmark-preserving unwrap and explicit chronology; confirm clocking if calibrated output shown.
- **Exit evidence:** Reviewed B205 continuous preview with seam/axis correspondence and approved output labeling.
- **Status:** Open; synthetic topology test allowed, blocks lock

## BL11 — source/approval

- **Affected system/shot:** S06-03; S07-01 entry; existing public repository exposure
- **Central decision / feedback reference:** O08 / O13
- **Unresolved question:** May actual ENP1 operator log be displayed and what remediation is required for prior public exposure?
- **Source/evidence:** S06 V2 rights warning; storyboard index/O13; A02 v001 A02-10 identifies original local 21-page ENP1 report with confidentiality footer. Availability is established by A02, permission is not.
- **Provisional assumption:** Do not copy/export/redistribute log; never relabel ENP1 as ENP3. Stylized alternative is a human decision.
- **Owner:** Radzi with MIT/operator; repository owner for exposure decision
- **Next action:** Resolve use permission, redaction, caption and existing public-history handling; prepare conditional edit route only.
- **Exit evidence:** Explicit permission/approved redaction and ENP1 labeling, or agreed omission/replacement; separate recorded repository-exposure decision.
- **Status:** Open; blocks actual-log use/publication; synthetic maps independent

## BL12 — source/approval

- **Affected system/shot:** All 22 proposed shots and full edit
- **Central decision / feedback reference:** O10 / O11; O02 for schedule/specs
- **Unresolved question:** Does live Padlet match V2, who reviews, and do boundaries/read times fit the confirmed 90 seconds?
- **Source/evidence:** Repository V2 plus T-001 v002: total 90 seconds confirmed; section allocation provisional.
- **Provisional assumption:** Retain seven sections/five applications; proposed 22-shot split is inventory only, not approved camera/edit plan.
- **Owner:** Radzi; MIT technical/final approver
- **Next action:** Reconcile live section versions; accept/revise inventory then review actual moving edit; agree review route/settings in assigned tasks.
- **Exit evidence:** Recorded Padlet reconciliation and exact inventory/animatic version, named reviewers and agreed settings; B401 human acceptance before finishing.
- **Status:** Open; planning/tests allowed; blocks timing/story lock and final content

## BL13 — source/approval

- **Affected system/shot:** S07-02/03; final branding and finish across film
- **Central decision / feedback reference:** O09
- **Unresolved question:** Which official logo/tagline/product name/finish and capability wording are approved?
- **Source/evidence:** S07 carried-forward caption includes supplied logo; no final artwork approval inferred.
- **Provisional assumption:** Do not alter brand proportions or select exact product finish/font as confirmed; neutral mechanical previews remain possible.
- **Owner:** Radzi with MIT; finishing executor later
- **Next action:** Register official assets and approve exact end-card/capability copy and hardware finish.
- **Exit evidence:** Versioned official files/rights and recorded approved copy/finish/end-card constraints.
- **Status:** Open; blocks affected final brand/content use, not neutral mechanics

## BL14 — source/approval

- **Affected system/shot:** S03-02; related spiral use in S06-01
- **Central decision / feedback reference:** O10 / O06
- **Unresolved question:** Which revised geometry panel and reference video meaning should supersede stale helix wording?
- **Source/evidence:** Narrative names absent 03_Spiral_Geometry_Through_Depth.svg; actual revised SVG/caption says wall deformation, not internal ribbon.
- **Provisional assumption:** Inventory uses actual revised P3 SVG and companion caption; no claim of live-board update or verified field spiral.
- **Owner:** Radzi with MIT; source maintainer
- **Next action:** Reconcile panel note/feedback register and live version; confirm video interpretation.
- **Exit evidence:** Dated source reconciliation and reviewed wall-geometry example, propagated to B202/S03/S06.
- **Status:** Open; local filename mapped, content/live-source reconciliation pending

## BL15 — source/approval

- **Affected system/shot:** S01-01/02
- **Central decision / feedback reference:** O10
- **Unresolved question:** Is offshore rig/water/seabed context retained for this film?
- **Source/evidence:** S01 caption explicitly calls offshore a proposed cinematic choice.
- **Provisional assumption:** Keep contextual option; do not make offshore-only product capability claim.
- **Owner:** Radzi with MIT as needed
- **Next action:** Confirm setting with current storyboard reconciliation before specific environment build.
- **Exit evidence:** Recorded retained setting and source/asset plan, or revised context preserving descent purpose.
- **Status:** Open; blocks specific setting lock; generic layout study allowed

## BL16 — finishing

- **Affected system/shot:** Camera/graphics polish throughout; S02-02, S06-02, S07
- **Central decision / feedback reference:** O09; directorial modules 05/08
- **Unresolved question:** Which final typography, annotation density, camera phrasing and finish survive moving QA?
- **Source/evidence:** Camera module; typography module; E016 preference is conceptual and untested in motion.
- **Provisional assumption:** Quiet sans-serif editorial starting point, C for fuller S02/A1 for simple moments; no fixed font/curves or universal 3D overlay rule.
- **Owner:** Radzi/director; shot executor; MIT for required labels
- **Next action:** Later single Scene Direction Contract per shot; validate arrivals/transitions/readability in cheap previews before B4 finishing.
- **Exit evidence:** Director feedback on versioned moving preview, legible exact required copy and source-consistent graphics; B4 acceptance before final materials/AI/expensive renders.
- **Status:** Open; does not block mechanical studies

## BL02 research addendum — provisional scenario available

T6 follow-up research found a [source-backed nominal scenario](Tasks/T-006/research-standard-scenario_v002.md) and [dimensional proposal](../Shared/Assets/WellAssembly/config_researched-proposal_v002.json). 13.375in casing in a 17.5in host with a subsequent 12.25in open-hole section is documented by SLB; selected 61lb/ft manufacturer reference yields nominal centered fit. This improves preparation beyond asking for every standard size. It does not establish actual MIT BHA placement, adapter design or deployment approval. O05/BL02 remains open for those claims; producer selection of the researched provisional illustration is separate from final engineering acceptance.
