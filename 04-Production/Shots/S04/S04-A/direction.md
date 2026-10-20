# S04-A — Entering the Cased World

> Current continuation: scene establishment, 20 October 2026. Stages 1–5 are owner-agreed, including the director-reviewed camera intention. Stage 6 conceptual reveal is owner-approved; full 18-second cinematic previs v005 is now owner-released and being prepared for review. Final finishing remains unreleased. Earlier T43 direction remains historical input. The sequence-wide stage record is maintained in this existing contract; S04-B/C/D link here.

Scene Direction Contract v0.2 · shot version v001 · T43 · 18 October 2026

## State and authority

D0 complete. Approved shared concept and narration-led responsibility split apply. This detailed brief is released as a **D1 implementation test**, submitted for Radzi's review; it is not D2 execution-ready, D3 motion-approved or D4 final-approved. No production is launched by T43.

Authority: engineering/client facts → project/brand constraints → narrative → documented taste → this composition → execution convenience. Sources: [S04-A.md](/04-Production/Records/Storyboard-Board-V3/Shots/S04-A.md), [shared-direction_v001.md](/04-Production/Records/Tasks/T-043/shared-direction_v001.md), [release-index_v001.md](/04-Production/Records/Tasks/T-043/release-index_v001.md), [component-register_v001.md](/04-Production/Records/Tasks/T-042/component-register_v001.md), [07-SCENE_DIRECTION_CONTRACT_v0.2.md](/03-Context/03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md). T42 inspection is inherited evidence, not a fresh Blender inspection by this director.

## Purpose, audience and premise

**Nontechnical takeaway:** A later upward pass enters steel already installed higher in the well.

Audience: engineers and nontechnical stakeholders with mixed prior knowledge. Intended feeling: A deliberate change of environment. The value of this moment is making the stated relationship understandable without an unsupported performance claim. The central image and expert-verifiable meaning are the physical/data relationship below, not decorative activity.

**Narration cue:** Higher in the well, steel casing protects an earlier section. This cue is thematic, not a replacement script or timed recording. Narration carries meaning and significance; imagery carries the discovery. Review comprehension with the intended narration (temporary read is sufficient). Voice-recording synchronization is outside T43 and does not block this brief.

## Camera score and objects/events

Film window: **40–44 s**; content duration **4 s**. Local seconds below are editorial targets, not measured mechanism cadence or fixed recording timing.

Wider longitudinal three-quarter view of inclined well; existing casing shoe and deeper open hole in one frame. Track upward with modest retreat; preserve uphole direction.

| Local seconds | Visual event / gaze / arrival |
|---|---|
| 0–0.8 | Establish later phase, existing shoe and upper steel interval. |
| 0.8–2.8 | Upper BHA and ECCO move upward across shoe while bit remains lower. |
| 2.8–4 | Sensing region is inside casing; settle before closer response view. |

**Entry:** Editorial cut from S03-C, no claim of continuous drilling descent.

**Exit:** S04-B uses same inclination, inner steel side, dimensions and sensor region.

Maintain occlusion and object identity through travel; use the stated cut/reveal rather than penetrating opaque hardware. Product/effect motion is authored in Blender; source measurements govern spatial registration. Separate camera path and gaze where useful; slow into meaningful arrivals. Exact poses, focal length, clipping and keyframes are derived from the inspected scene. This beat table is the canonical conceptual spatial score; no precision camera diagram or extra 3D storyboard is required.

## Look, lighting and atmosphere

Rock gives way to controlled steel reflections; casing boundary remains clear, no materializing tube.

Shared tactile rock/fluid and satin metal apply where present. A broad motivated grazing key reveals shape, restrained rim separates silhouettes, and dark negative space protects the discovery. Metallic reflections describe real geometry. Downhole illumination is an explanatory lighting convention, not literal sunlight. Use depth/parallax before fog; keep fluid present without expensive volume scattering. Candidate finishes are art direction, not MIT material certification.

## Engineering information and graphics

**Fixed technical boundary / expert truth check:** ECCO is above bit and crosses before bit on upward motion. Validate clearance in provisional T6 scenario; no claim of loaded passage/safety certification. Do not assemble casing around instrument.

**Exact copy / information treatment:** None unless phase is unclear, then small 'Cased-hole evaluation' cue. Copy specified here is proposed for this implementation test unless already mandated by provenance; omission of optional copy is permitted when narration and imagery suffice. Required synthetic-data identification cannot be omitted. Use calm editable sans serif, stable reading positions, quiet entrances and limited simultaneous information. Font/license, scale and moving legibility must be verified at preview resolution.

Information lifecycle: introduce only at its corresponding beat; anchor measurement to its source location; retain the stated comparison through its reading hold; remove or explicitly switch channel at the exit. Physical lighting is not data. Illustrative acoustic/flow graphics do not assert visible emission, calibrated velocity or simulation results. Never invent values to improve contrast. Preserve missing/invalid samples and label interpolation; real/synthetic provenance must survive into maps and reports.

## Asset register and implementation handoff

- **ECCO:** `04-Production/Shared/Assets/ECCO/ECCO_master_temporary-plugs_v002.blend` (registered native source; absent from Git tree, resolve in production workspace) ECCO_MASTER_v002; source longitudinal X in metres. Inspect actual sensor face/datum. Do not rescale 2.4 m to 2.25 m. Controls ECCO_ROOT, ECCO_ROTATION_X and ECCO_SENSOR_REF_01–03.
- **BHA:** `04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend` (registered native source; absent from Git tree, resolve in production workspace) WELL_ASSEMBLY_v003 / ASSEMBLY_CONTROL. Bit/adapters simplified; refine visible silhouettes only after source inspection. Avoid duplicated linked ECCO.
- **WELL:** `04-Production/Shared/Assets/WellAssembly/WellAssembly_variants_v003.blend` (registered native source; absent from Git tree, resolve in production workspace) Reuse registered spatial variants; inspect scale, layer ordering and boundaries.
- **MUD:** New implementation required; no existing asset claimed. New shared fluid visibility wrapper; bounded optical simplification, never a dry void.
- **CASING:** `04-Production/Mechanisms/B203/Scenes/B203_retrieval_v002.blend` (registered native source; absent from Git tree, resolve in production workspace) Also B203_support_v002.blend, B203_channel_v002.blend, B203_wear_v002.blend in same folder. Standalone mechanism proofs require spatial integration; no default exploded offsets.

**Shot-specific work:** T6 v003 and B203 retrieval v002 are references; integrate one linked ECCO, refine shoe only enough to communicate existing boundary.

Before D2, the Blender executor verifies accessible native files, collection names, metre scale/axes, actual sensor surfaces and any visible stage/layer geometry; records exact versions and selected data case; derives lens/poses from blocking. Three sensors at 120° in one plane and the sourced shoulder reference do not substitute for coordinate inspection. Whole-tool rotation, where shown, follows the sourced clockwise view from surface looking downhole. Preserve source files and completed mechanism proofs; create versioned adapters/shot scenes.

Working profile for testing: 1280×720, 24 fps, EEVEE, 16 samples, 16:9. This is a proposed test profile, not final delivery approval. Seconds remain authoritative. Use 0.5 s handles where action permits, outside content duration; final assembly and audio belong to Radzi. Record color management, compositor and profile. Separate geometry, amplitude, signal, labels and reveal masks where used; avoid compulsory multilayer passes if they add no review value.

Targets relative to this shot folder: `Scenes/S04-A_v001.blend`, `Previews/v001/` (entry, major arrivals, peak-cost and exit stills plus continuous playblast), `Evidence/v001/` (asset/component manifest, scene-derived camera/frame score, provenance, benchmark log and review record). These are future deliverable paths, not created outputs. Update this same contract with D2 facts rather than creating competing direction specifications.

## Cost and review gates

**Likely heavy state and bounded alternative:** Shoe plus most visible layers; opaque sectional window rather than full transparent well.

Every sampled full render-to-written-frame must be **strictly under 5 seconds**, including compositor and cold render. Benchmark entry, arrivals, peak effect, exit and any heavier state; log hardware/settings and cold plus repeat timings. No average-only pass. No render was run for T43. Simplify invisible geometry, transparent layers and particles first; never silently reduce resolution, change source scale or falsify meaning. Benchmark before batch rendering.

**Initial director critique:** the shot succeeds only if its arrival communicates the takeaway; decoration, hidden relationships and hurried reading are failure modes. Preserve successful blocking; make bounded corrections before adding effects. The specific unresolved risk is whether the proposed composition, timing and source assets support the expert check above; the executor tests this rather than assuming approval.

**Cold-viewer question:** Can the viewer see which part is already cased and that ECCO moves upward into it? After the narrated moving preview, also ask why the discovery matters. Do not claim silent comprehension or infer motion approval from a still.

## Scene establishment continuation — 20 October 2026

### Stage 1 — Narrative Intent: owner-agreed

Radzi approved the Stage 1 proposal in this conversation: "Good, I agree. Let's move to stage 2."

Audience: engineers and nontechnical stakeholders. Takeaway: **ECCO helps engineers assess the support outside the casing and changes to its inner wall.** Preserve the ordered discoveries: upward return into pre-existing casing; acoustic response and backing support; a possible channel continuing along one side outside steel; separate inner-wall wear detection. Narration explains significance while images establish locations and differences. This approval does not accept a new camera, representation or full build.

### Stage 2 — Truth & Mechanism: qualitative illustrative boundaries owner-agreed

Radzi accepted the plain-language Stage 2 explanation with "Okay, correct." The accepted explanation distinguishes backing-support clues from inner-wall distance measurement, keeps casing pre-existing, places the channel outside steel and treats wear as pre-existing. The cases and visible effects remain illustrative. This is Gate A acceptance of meaning and safe interpretation, not domain certification or approval of unseen numerical claims. The detailed source and asset notes below remain supporting evidence with their stated limits.

**Physical chain:** this is a later upward BHA pass after deeper drilling, not continued downward drilling with casing appearing around the tool. ECCO stays above the bit and crosses the shoe before the lower bit. The layers are tool/well fluid, steel, cement or a localized exterior channel, then formation. These relationships follow client corrections C04–C07 and the existing S04 contracts.

**Information chain:** an outward-facing sensor sends an ultrasonic pulse through well fluid to steel and receives its return. The received waveform contains a response whose decay can inform interpretation of backing support. The illustrative supported case decays faster than the reduced-support/fluid-backed comparison; this is not a universal material classifier. Separately, echo arrival time with mud acoustic-velocity correction supports sensor-to-inner-wall distance. Reconstructing casing radius requires tool-position/eccentricity treatment. A local inner-wall recess increases local internal radius; it does not establish direct wall-thickness measurement by itself.

**Display chain:** any visible fronts, response traces, retained marks, backing reveal or colors are explanatory representations of synthetic examples. They are not emitted light, an optical photograph through steel, acquired field logs or a calibrated acoustic simulation. Do not present a backing change at one location as cement physically changing during measurement. Do not imply measured full-log telemetry to the surface.

**Fixed boundaries:** use three sensor references in one plane, 120 degrees apart; outward send and same-sensor receive. Channel geometry is outside steel and localized along one circumferential side. It is static and does not establish fluid chemistry or active flow. Wear predates sensing, recedes into steel from the inside and retains the fixed exterior; no material removal by a pulse. Do not portray an irregular open-hole wall inside the installed steel interval.

**Source and asset evidence:** [Engineering Baseline](../../../../03-Context/01_Foundation/02-ENGINEERING_BASELINE.md), including its limits; [Decision Register](../../../../03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md), especially O04/O05/O06 and the 16 October illustrative-scenario amendment; Ahmed's explanation in `01-Brief/Chat/chat.md`, lines 236–254; [client corrections C04–C07](../../../../03-Context/02_Storyboard/V2/ECCO_Section_04_Cased_Hole_Padlet_v2/MASTER_CLIENT_FEEDBACK_REGISTER.md); [CasedHole interface](../../../Shared/Assets/CasedHole/README_v002.md) and [manifest](../../../Shared/Assets/CasedHole/manifest_v002.json).

The prior read-only Blender inspection opened CasedHole v002 and Retrieval v008 with metre units and resolved libraries. During Stage 2, all 20 native/input file hashes in the CasedHole manifest matched the current local files. Retain BHA_film_v007 and its v006 dependency, ECCO_film_v002, World_environment_v009, Acoustics_v003 and CasedHole_v002. This confirms package identity, not MIT engineering approval. Live Work revision 701 still places T47/T46/T45 in Review; T43/T44 are Done. No ticket was claimed, changed or self-accepted.

**Existing illustrative example:** casing ID 317.881 mm, OD 339.725 mm; cement exterior diameter 444.5 mm. The channel is 2.1 m long at source X[-2.5,-0.4] m and azimuth [0.30,0.80] radians. Wear is authored at up to 4 mm; actual cross-section sampling can be slightly smaller. These are source-owned demonstration parameters, not field measurements or a verified ENP3 deployment specification. Preserve the 2.400 m mesh; do not silently resize it to the brochure's nominal 2.25 m.

**Unresolved and scoped limits:** exact deployment fit/loaded passage, sensor acoustic-face certification and product-specific calibration remain unverified. These block associated engineering, quantitative and operational-safety claims, not the already permitted illustrative explanation. No calibrated waveform, bond-strength number, guaranteed identification of water, proven zonal isolation or measured thickness claim is released. No acoustic acquisition during upward rotation is assumed solely from the drilling narrative; any shown motion must be compatible with the selected event binding and operating illustration.

**Independent principle check:** [SLB USI](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-construction/well-cementing/cement-evaluation/usi-ultrasonic-imager) supports the generic decay/backing relationship; [SLB Isolation Scanner](https://www.slb.com/products-and-services/innovating-in-oil-and-gas/well-construction/well-cementing/cement-evaluation/isolation-scanner) documents ambiguity where cement/fluid acoustic contrast is insufficient. These references check the principle only. Do not transfer another tool's thickness capability, resolution, transducer arrangement or real-time output to ECCO.

**Gate A outcome:** the meaning and qualitative illustrative boundaries are accepted through the Stage 1 and plain-language Stage 2 exchanges. Stage 3 representation was subsequently accepted as recorded below. Stage 4 look, Stage 5 motion and Stage 6 production release remain subsequent decisions. No new Blender scene, proof, render or integration was made during Stage 2.

### Stage 3 — Visual Representation: limited viewing window owner-agreed

Radzi accepted the plain-language Stage 3 proposal with "Yes, I agree that." Approval covers a recognizable well, a temporary viewing window for outside support/channel, and return to inner wear with a registered original-surface outline. It does not release a camera path, final look, proof or full production.

**Recommendation and reason:** keep ECCO in the recognizable physical well and use a limited illustrative viewing window to explain the layers. Primary representation is a controlled cutaway (R4), with the surrounding well retained as context. The window is a visibility operation for the audience, not a physical opening or a capability of the sensor. This lets the same steel boundary explain both outside support and inside wear.

**Visible and hidden:** first identify the existing casing boundary, the tool inside and surrounding formation. For the backing-support/channel discussion, selectively hide only the facing portions needed to see the steel, cement and localized gap together. Retain enough of the casing's curved wall and cut edges to establish a pipe enclosing the tool. Keep all layers at their actual registered positions and scales. Full geometry remains available outside the temporary viewing operation.

**Information and reference:** show a short, clearly illustrative response cue beside its actual sensing location to explain faster versus longer ringing; its exact design belongs to Stage 4. The revealed exterior gap is an authored scenario, not a measured field map. Keep its location fixed in the well as more of its length is exposed. When attention returns to inner wear, withdraw the outside reveal and compare the existing recessed inner wall with a thin registered outline of the original inner surface. Preserve the real outside casing boundary; do not deepen the groove for readability.

**Continuity:** Section 4 is a later upward pass into an existing upper cased interval, not the identical Section 3 recorded interval changing from rock into steel. Reuse product identity and the established formation context without claiming dataset identity. A phase change must remain understandable; the exact edit and camera path are later Stage 5 decisions. Section 3 remains untouched. Section 5 is a separate hydraulic demonstration.

**Alternative not recommended:** removing the whole environment or spreading the layers apart would weaken the inside/outside relationship and the established physical context. A controlled local cutaway is the proposed simplification; no actual geometry or well clearance changes are proposed.

**Decision for this stage:** the limited viewing-window representation is accepted, keeping the tool, pipe and ground connected. Palette, shading, typography, signal styling, camera poses and timing were not selected by this approval. No proof or full production is released here.

### Stage 4 — Art Direction: realistic environment owner-agreed

**Owner decision:** after questioning the digital-environment proposal, Radzi accepted the revised recommendation with "Okay then, I agree." Use realistic rock, drilling fluid, steel and cement, continuing the physical-world appearance of Sections 1 and 2 and reusing existing assets. Keep digital graphics for sound, signal traces and reference outlines. Preserve the approved viewing window. The earlier proposal to carry Section 3's digital ground into Section 4 was not selected. This approval covers look direction, not an unseen finished frame, camera animation or production release.

**Appearance references and limits:** the owner's selected physical-world reference is Sections 1 and 2. Reuse the current canonical formation/fluid/product packages rather than copying Section 3's reconstructed geometry or amplitude map. The inspected `03-Context/02_Storyboard/V3/ECCO_Section_04_Cinematic_Rich_Direction_Separated/S04_C_The_Hidden_Channel/S04_C_The_Hidden_Channel.png` supplies distinguishable steel, warm cement and a one-sided blue channel. Exclude its generated ECCO anatomy, apparent clearances, river-like channel detail, excessive translucency and baked annotations. The inspected S03 `v036/Previews/Final-video-check.png` documents the digital-ground alternative that was not selected; it is not the S04 environmental target. A new combined S04 target still has not been created.

**Physical surfaces:** ECCO and steel use readable satin silver-grey highlights. Broad controlled grazing light describes pipe curvature and the shallow existing inner groove, preserving detail without white hotspots. Cement is matte warm sand/ochre with restrained grain. The static illustrative gap has subdued blue identification, not an animated liquid stream. Realistic rock and drilling fluid provide physical enclosure and depth. The inspection window preserves visible casing curvature and edges. Do not add an environmental HUD/grid or luminous soil as the default world treatment.

**Information appearance:** reuse thin cyan outgoing fronts and lighter emerald returns, tied to the same sensor. A compact signal cue explains the short/long response; its trace is illustrative, without invented numbers. Wear uses a fine original-surface reference alongside the registered actual profile. Data graphics remain a separate display layer and do not alter steel, cement or formation geometry. Do not reuse the S03 yellow/brown amplitude image as a cement material or diagnostic cement map.

**Text and hierarchy:** keep explanatory text sparse, quiet and readable near the relevant feature. Optional plain-language candidates are 'Cement', 'Possible gap' and 'Inner wear', used only when needed; these words, font choice and placement are still proposed. Retain the illustrative-example identification. The actual tool and the active finding take priority over background linework and response graphics.

**Key target state:** a recognizable ECCO inside a curved steel boundary; the limited window exposes matte warm cement with a narrow blue interruption on one side; realistic ground surrounds the well and continues beyond the view. Steel, cement, gap and explanatory graphics must be separately identifiable. No neon flood, spark cloud, exaggerated groove, invented calibrated field display or new geometric deformation is selected.

**Stage boundary:** the revised realistic look direction is accepted. A combined target still has not been created or approved. Any later proof must use the selected representation and actual assets, in a separate version and within its named release. Stage 5 motion and Stage 6 proof/production release remain separate.

### Stage 5 — Camera & Motion Architecture: refined continuous journey owner-agreed

**Owner decision and director review:** Radzi accepted the reviewed Stage 5 refinement with "OK agree" after the comparison against the AI Director workflow, Camera & Motion Language and live S04 storyboard revision 14. Preserve the discovery order and 18-second target, reduce repeated close/back/close travel, give the response comparison a nearly still recognition moment and connect exterior channel to inner wear through the established viewing window with a stable pipe edge. This accepts creative motion intention (Gate B), not a tested camera, exact transforms or production release.

**Accepted intention:** one continuous camera move within Section 4, mainly along the same side and axial direction of the well. Follow ECCO upward, settle beside the sensor, glide along the revealed channel, settle on the inner wear and finish gently toward the product. Prefer the window's progressive exposure over a large camera excursion. Keep part of ECCO and a recognizable steel boundary available through transitions. Source geometry and well clearances remain unchanged; camera smoothness, feature readability and timing are untested.

| Local time / ID | Main view and new discovery | Movement and recognition intent |
|---|---|---|
| 0–4 s / S04-A | Medium side-oblique view includes the existing casing entrance, ECCO and the lower bit where needed to establish order. Tool travels uphole toward the same screen direction, provisionally upper right. | Follow the upward crossing gently; keep the casing entrance readable while ECCO enters ahead of the bit. End with the sensing region inside steel. |
| 4–9 s / S04-B | Settle beside the side-facing sensor and inner steel. Keep part of ECCO on one side and the contact/steel boundary on the other. Two existing backing locations provide the qualitative response comparison. | Become nearly still for response recognition. Separate send, contact, return and response reading. Retain context behind the same pipe without crossing intact steel. |
| 9–14 s / S04-C | Glide along the same side while the limited window exposes the outside cement and narrow channel. ECCO remains an anchor as axial extent becomes readable. | Use the reveal to expose more length, with only a small framing adjustment if necessary. Avoid a compulsory pullback followed by another push-in. The gap and steel stay fixed. |
| 14–18 s / S04-D | Through the established viewing access, shift attention to the inner wear and registered original-surface outline near a side third. | Keep a recognizable pipe edge through the transition, settle gently for reading, then release attention toward the product body. No fast loop, full orbit or sudden wide exit. |

**Separate motion tracks:** camera navigation, upward assembly movement, sampling/rotation, signal animation and the viewing-window mask are separate controls. The casing, cement, gap, wear and registered reference remain fixed in well coordinates. The existing acoustic binding samples a fixed emitter pose; keep that pose valid through the complete return packet or use an explicitly verified moving-emitter solution. Do not assume camera travel makes emitter travel valid. Present qualitative response comparison at distinct fixed backing locations rather than switching the actual cement beneath one contact. Exact operating emphasis and phase durations require the actual blocking/event proof; no calibrated acquisition cadence is asserted.

**Entry/exit:** the join from S03 identifies a later upward pass, preserving the meaningful well-axis orientation and product identity without claiming the same physical event or dataset. A deliberate phase-change edit is permitted there; the proposed single camera is internal to S04. The final product emphasis hands off editorially to S05's separate hydraulic demonstration. Exact matching, lens, positions, clip planes and keyframes remain TBD from actual scene blocking; no precision transforms are invented here.

**Voice and proof limits:** retain the working 4/5/5/4-second allocation, with the cement-support thought aligned to B/C and the inner-wear question aligned to D. These are editorial planning targets, not verified narration synchronization. The key risk is whether outside-channel context can connect legibly to an intimate inner-wear arrival within the available time and actual geometry. Stage 6 proposes the bounded proof below. No new Blender proof or full sequence has been built.

### Stage 6 — Targeted Proof & Scene Lock: limited test authorized, review pending

**Question:** can the camera guide attention from the channel outside steel to wear inside it smoothly, while ECCO and the pipe remain recognizable and the shallow groove is readable?

**Hypothesis and variable:** the existing local viewing window can expose the relationships without a large outward/inward camera excursion. Test camera path/gaze, the window's visibility mask and only the lighting needed for readable physical layers. Preserve the accepted assets, realistic look direction, dimensions, fixed outer casing, channel position, wear depth and registered reference. Do not deepen the groove or move the channel to solve composition.

**One bounded artifact:** a six-second normal-speed transition excerpt covering proposed S04 local seconds 11–17, preserving that interval's timing rather than compressing the full 18 seconds. Use actual linked hardware/casing/formation, practical existing materials and simple lighting. Deliver one MP4 plus the channel and inner-wear representative stills extracted from that same test. These are one proof, not separate creative gates or a full production scene.

**Proposed settings and budget:** 1280×720, 24 fps, EEVEE, initially 16 samples, 144 frames. Benchmark representative channel, transition and wear frames before the batch; every complete sampled render-to-file must remain strictly under 5 seconds. Record actual setup/render/encoding cost, settings and cold-cache limits. If the cap fails, simplify cost without changing geometry or silently reducing inspection resolution. The six seconds is clip duration, not a wall-time promise.

**Success:** identifiable steel/cement/gap; a stable steel boundary through the transition; part of ECCO stays available for orientation; the reveal does not look like a new physical hole; shallow inner wear and its reference are readable at normal playback; no jump, arbitrary loop, unannounced steel penetration or abrupt scale change. A viewer should be able to point to the outside gap and inside wear. Executor self-review does not substitute for Radzi's review or an independent audience/engineering test.

**Planned paths, not created deliverables:** `../S04-C/Scenes/Proofs/v001/S04-C-D_transition-proof_v001.blend` and `../S04-C/Previews/proof-v001/S04-C-D_transition-proof_v001.mp4`, with two stills and verification alongside the preview. Preserve relative asset links and fresh-open the saved proof. Do not replace the live Blender scene or modify shared masters.

**Stop point and remaining limits:** stop after this proof and return it for review. It does not verify entry, the complete support-response timing, narration synchronization, the S03/S04 edit or the whole 18-second rhythm. Those checks remain in the consuming build/review if production is later released. No full sequence, finishing, film assembly, new ticket or external publication is authorized by Stage 5 acceptance. Await an explicit release of this named test; full production remains separately unreleased.

**Acceptance:** inspect entry, arrivals, transition and exit stills, then continuous motion with intended narration; verify source relationship separately with an expert. Record still, motion, engineering and final acceptance separately. Source uncertainty blocks only the affected claim/feature, not unrelated shot exploration. Radzi reviews the exact brief and previews; client technical review is required for unsupported engineering interpretations. Current status: no native scene, render benchmark, moving preview or client technical acceptance inspected in this task.

### Stage 6 bounded correction — exterior gap readability, 20 October 2026
Owner rejected blue channel placeholder because it reads as a solid ribbon. Realistic finish remains the direction; low-cost playblast must still communicate missing cement. v002 removes the local solid channel placeholder entirely. Existing canonical cement pieces already form the open channel. Local exterior casing shading is darkened to distinguish the recessed floor from cement side edges; inner inspection shading and all linked geometry/camera keys remain unchanged. No canonical assets edited. Proof: 05-Previs/Section-04_Cement-Casing-Integrity/v002/Previews/S04_open-gap_0013.png. Saved scene: v002/Scenes/S04_transition-test_v002.blend. One fresh-open still inspected, not a new full animation. Measured single-frame render-to-save 1.79 seconds (including 0.38 seconds saving); startup additional. Owner review pending; full Section 4 production remains unreleased.

Owner steering: gap appearance remains unresolved; defer that choice and continue the already authorized six-second transition proof. v002 is a review candidate, not accepted gap styling. Playback remains 24 fps; target approximately one second render time per frame. Actual proof lives under 05-Previs/Section-04_Cement-Casing-Integrity as explicitly requested, superseding earlier proposed 04-Production proof destinations. Stage 6 test authorized; full production remains unreleased.

### Owner-authorized channel-volume proof v003
Owner rejected both ribbon and black-slot representations and requested a separate 3–5 second simple-proxy meaning test. Four-second, 96-frame, 24fps proof created under 05-Previs/Section-04_Cement-Casing-Integrity/Channel-Volume-Proof_v003. Steel, cement and rock are distinct closed annular cutaway sectors. A capped 50-degree fluid sector occupies radial interval .6801–.9999 inside the cement annulus .68–1.0, between axial positions -1.65 and1.65; these are proxy units, not claimed engineering dimensions. Cement is absent from exactly this sector while retained above/below/beside it. Fluid geometry and position are fixed; transparency reveals cyan explanatory fluid, with no stream or displaced cement animation. Broad realistic layer colors, no scientific-stage redesign of production. Existing native scenes and masters untouched; current Blender UI not replaced. Delivered establishing frame, reveal frame, four-second MP4 and editable standalone native scene. All96 MP4 frames decoded; inspected opening and final stills. Average render .335s/frame, max1.171s, total32.162s; process startup excluded. Four-sample grain retained for speed. Viewer comprehension remains for owner review; no direct photographed-fluid claim or full-production release.

### Channel discovery proof v004 — bounded revision, owner review pending
Preserve v003 proxy meshes/proportions/channel; owner requests readable normal-support → fluid-gap discovery → length continuity. New standalone five-second/120-frame proof under 05-Previs/Section-04_Cement-Casing-Integrity/Channel-Volume-Proof_v004. Opening shows intact supported top cross-section from opposite side, with channel physically occluded. Camera moves around cutaway to upper channel boundary, tracks downward beside fixed channel, then pulls back to full length. No geometry movement, cement dissolution, fluid flow or animated fluid opacity. Native v003/v004 vertex/face hashes match for every mesh. Channel closed manifold; radial bounds .6801–.9999 lie outside steel .68 and inside cement .68–1.0. Opening occlusion checked and sampled opening/reveal/track/end frames visually inspected. All120 video frames decode. Render mean .285s/frame, max1.040s, total34.242s; startup excluded. Existing production/live Blender scene unchanged. Illustrative MIT channel interpretation, not direct fluid imagery. Independent comprehension and owner acceptance remain pending; full production not released.

### Stage 6 release — complete Section 4 cinematic previs v005
Owner approves v004 conceptual progressive reveal and explicitly authorizes inexpensive full Section4 previs, reaffirmed with 'continue, follow stage6 manual'. Eighteen-second integration released: upward entry, two qualitative native ultrasonic casing-response events at distinct backing positions, organic localized fluid-filled annular channel reveal, then existing inner wear/reference. Materials and organic channel derivative are illustrative previs candidates, not final geometry/finish approval. Preserve canonical steel and shared masters, previous versions and current unsaved Blender state. Actual source/camera checks, representative benchmarks and review evidence precede completion; stop at owner review, no final finishing or whole-film assembly released.

### Stage 6 v005 implementation and pre-render review
Actual integration: 432 frames/18s/24fps/1280x720, EEVEE Vulkan4 samples. Saved scene and pending playblast: 05-Previs/Section-04_Cement-Casing-Integrity/Cinematic-Previs_v005/Scenes/S04_cinematic-previs_v005.blend and Previews/S04_cinematic-previs_v005.mp4. One camera follows upward entry, pauses for two side-sensor packets at distinct backing locations, opens outward to the channel extent, and returns to unchanged inner wear/reference. Selected supported sensor X=-0.32m; channel sensor X=-1.50m. Whole hardware is held through each final trailing return. Shared A-SENSING sample/bind/verify API and existing cased qualitative response graphic generator are reused. Local exposure compensation affects explanatory graphics only. A temporary viewer window opens around the sensor and later returns to its narrow steel edge; it is not physical material removal. The static fluid volume's audience visibility begins at8.9s as the camera leaves the response close-up; camera travel reveals its length. Organic annular side boundaries vary within0.30–0.80rad envelope, between unchanged steel exterior R0.1698625m and cement exterior R0.22225m; cement uses complementary local derivative meshes. This is explicitly illustrative, not a new engineering master or final geometry approval.

Fresh-open verification passed: all libraries relative/resolved, exactly one ECCO, linked steel unchanged without modifiers/displacement, closed fluid mesh wholly in annulus, unchanged source hashes and both strict native pulse/cap/wall/hold/return checks. Nine benchmark frames1/104/116/166/180/260/325/400/432 took0.454–1.326s, median approximately0.49s. Earlier blocked macro compositions were corrected before batch. Sampled entry, both sensor arrivals, channel extent and ending inspected; four-sample mask grain and bright metal remain preview limitations. Small signal/response legibility and the outside-to-inside journey require moving owner review, not automatic scene lock. No independent audience test or narration sync claimed. The live unsaved Blender v002 scene is preserved. Existing S01/S02/S03 and shared masters untouched. Review report and exact render timings live beside this candidate; final finishing remains unreleased.

### Stage 6 v005 review submission
Complete final18-second MP4 encoded and all432 frames decoded. Final delivered batch mean0.4904s/frame, max1.3297s, total211.864s; encode8.542s. The earlier full batch cost208.975s, preserved separately because the chronological entry review exposed a blocked approach. The corrected audience window extends through the casing entrance and opens earlier; entry frames48/72/96 were rechecked, then the complete batch was rerendered. Geometry, camera and event timing stayed fixed during this correction. Final source/native/MP4 hashes and measured costs: Cinematic-Previs_v005/Records/delivery.json. Saved native fresh-open verification passes. Final report: Cinematic-Previs_v005/Records/Review-report.txt. Stage6 status is owner review, not self-accepted scene lock; full cinematic finishing remains unreleased. Media remain local; permitted scripts/reports/metadata may synchronize, with no claim of remote native/video backup.
