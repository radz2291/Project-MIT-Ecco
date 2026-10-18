# V3 shot instruction placeholders

**Owner: separate AI directing agent. Status: unfilled planning placeholders.** P01 identifies the required inputs and decisions; it does not choose camera choreography, lighting, visual treatment or event frames.

Use the [live-board source index](Evidence/source-index_v001.json) and each linked shot card below. The directing agent must use the repository Scene Director skill and relevant Directorial Identity modules. Resolve instructions in one canonical `04-Production/Shots/<section>/<V3-id>/direction.md` per shot when authorized. These planned paths are not created contracts. Earlier numeric shot folders and T31 proposals are historical sources and must not be overwritten or relabeled by title.

Every contract needs: approved component versions and technical limits; one viewer takeaway; actual scene axis/units; camera/lens and entry/reveal/payoff/exit states; event timing; lighting/material/visibility decisions; graphic wording/quantity/provenance; adjacency requirements; cheap-render settings and benchmark evidence; audience and engineering checks; Radzi's decision against an exact candidate. Leave unknowns explicit until the responsible role resolves them.

## Shared visual decisions

| Slot | Required decision | Owner | Status |
|---|---|---|---|
| VD01 | Surface setting, rig detail, geological context and surface-to-downhole continuity | AI director / Radzi | UNFILLED |
| VD02 | Common hardware finish, BHA/bit visibility and selective fluid/wall/casing visibility | AI director / Radzi, within sourced geometry | UNFILLED |
| VD03 | Pulse/contact/echo vocabulary, waveform arrival-time treatment and wall-data accumulation | AI director / Radzi, preserving C02 | UNFILLED |
| VD04 | Geometry and amplitude presentation; case transitions; fixed legends, seam and data-output continuity | AI director / Radzi, with data executor | UNFILLED |
| VD05 | Cased support/channel/wear treatment and operating-phase transitions | AI director / Radzi, preserving C04–C07 | UNFILLED |
| VD06 | Hydraulic mode and illustrative flow vocabulary distinct from acoustics; treatment of unresolved CAD stage mapping | AI director / Radzi, with source inspection | UNFILLED |
| VD07 | Typography, capability reminders, real/demo output framing and selected MIT lockup | AI director / Radzi | UNFILLED |
| VD08 | Working profile, shot handles and editor handoff conventions within the strict render budget | Radzi / director / executor | UNFILLED |

## Shot slots

Components refer to the [component register](component-register_v001.md). All camera, look, event-frame and approval fields are null in the [machine-readable shot map](shot-map_v001.json).

| Source shot | Seconds | Components | Required content from V3 | Instruction to resolve |
|---|---:|---|---|---|
| [S01-A](../../Storyboard-Board-V3/Shots/S01-A.md) | 0–3 | SURFACE, BHA, WELL | Rig, sea/seabed or selected setting, string and strata; establish route below surface. | **UNFILLED:** Surface setting and practical transition; no precise field-location claim. |
| [S01-B](../../Storyboard-Board-V3/Shots/S01-B.md) | 3–7 | BHA, WELL, MUD | Continuous string in fluid-filled geological context. | **UNFILLED:** Descent continuity and visibility; no dry cave or through-steel camera. |
| [S01-C](../../Storyboard-Board-V3/Shots/S01-C.md) | 7–10 | ECCO, BHA, WELL, MUD | Actual product and nearest wall, no acoustic event yet. | **UNFILLED:** Exact handoff to S02-A; verify sensor region. |
| [S02-A](../../Storyboard-Board-V3/Shots/S02-A.md) | 10–13 | ECCO, BHA, WELL, MUD, ACOUSTICS | Isolated transmit/contact/same-sensor return; transient local patch. | **UNFILLED:** Select/adapt B201 candidate appearance and event timing. |
| [S02-B](../../Storyboard-Board-V3/Shots/S02-B.md) | 13–17 | ECCO, BHA, WELL, MUD, ACOUSTICS, DATA, GRAPHICS | Arrival-time waveform tied to wall points; additional acquisitions. | **UNFILLED:** Conceptual signal treatment, arrival spacing and point persistence. |
| [S02-C](../../Storyboard-Board-V3/Shots/S02-C.md) | 17–22 | ECCO, BHA, WELL, MUD, ACOUSTICS, DATA | Whole assembly rotates; wall-fixed samples form one circumference. | **UNFILLED:** One-plane reveal and match to S03; no full-depth volume yet. |
| [S03-A](../../Storyboard-Board-V3/Shots/S03-A.md) | 22–28 | ECCO, WELL, DATA, GRAPHICS | White nominal reference, blue enlargement, red tight region. | **UNFILLED:** How separate existing cases satisfy V3 without inventing a combined measured hole. |
| [S03-B](../../Storyboard-Board-V3/Shots/S03-B.md) | 28–34 | ECCO, WELL, DATA | Successive measured sections and wall-bound spiral irregularity. | **UNFILLED:** Preserve geometry while selecting readable source contours/surface. |
| [S03-C](../../Storyboard-Board-V3/Shots/S03-C.md) | 34–40 | ECCO, WELL, DATA, GRAPHICS | Independent yellow/brown echo-strength channel on same coordinates. | **UNFILLED:** Fixed transfer and semantic bridge; no lithology certainty. |
| [S04-A](../../Storyboard-Board-V3/Shots/S04-A.md) | 40–44 | ECCO, BHA, WELL, MUD, CASING | Later upward retrieval into existing casing, product before lower bit. | **UNFILLED:** Deviated context, shoe boundary and visible hardware refinement. |
| [S04-B](../../Storyboard-Board-V3/Shots/S04-B.md) | 44–49 | ECCO, WELL, MUD, ACOUSTICS, CASING, GRAPHICS | Qualitative supported/poor-support response behind steel. | **UNFILLED:** Package schematic proof into same spatial scene; response provenance. |
| [S04-C](../../Storyboard-Board-V3/Shots/S04-C.md) | 49–54 | ECCO, WELL, MUD, CASING, GRAPHICS | Localized axial channel outside steel within cement. | **UNFILLED:** Anchored reveal, no river or full unwrap. |
| [S04-D](../../Storyboard-Board-V3/Shots/S04-D.md) | 54–58 | ECCO, WELL, MUD, ACOUSTICS, CASING, GRAPHICS | Inner groove increases local radius; exterior fixed. | **UNFILLED:** Source-scale groove and nominal comparison; avoid thickness claim. |
| [S05-A](../../Storyboard-Board-V3/Shots/S05-A.md) | 58–62 | ECCO, BHA, WELL, MUD, FLOW | Uphole return flow and cuttings near accelerator body region. | **UNFILLED:** Resolve stage map and mode before close feature attribution. |
| [S05-B](../../Storyboard-Board-V3/Shots/S05-B.md) | 62–66 | ECCO, BHA, WELL, MUD, FLOW | Twisted-pad flow illustration and transported cuttings. | **UNFILLED:** Resolve pad identity and affordable effect density. |
| [S05-C](../../Storyboard-Board-V3/Shots/S05-C.md) | 66–70 | ECCO, BHA, WELL, MUD, FLOW | Integrated downstream flow story. | **UNFILLED:** No invented pressure/efficiency evidence; transition out of hydraulics. |
| [S06-A](../../Storyboard-Board-V3/Shots/S06-A.md) | 70–74 | ECCO, WELL, DATA, GRAPHICS | Retrieved data becomes reconstructed surface. | **UNFILLED:** Flow-to-data editorial separation; same dataset for next shot. |
| [S06-B](../../Storyboard-Board-V3/Shots/S06-B.md) | 74–79 | DATA, GRAPHICS | Same depth/azimuth samples unwrap; separate geometry/amplitude maps. | **UNFILLED:** Seam, depth direction and coordinate mapping; no physical peeling. |
| [S06-C](../../Storyboard-Board-V3/Shots/S06-C.md) | 79–82 | OUTPUT, GRAPHICS | Authorized real/redacted report or labeled demonstrator. | **UNFILLED:** Choose permitted content and truthful identity; generated screen is composition only. |
| [S07-A](../../Storyboard-Board-V3/Shots/S07-A.md) | 82–84 | ECCO, OUTPUT, GRAPHICS | Output recedes into actual product. | **UNFILLED:** Carry S06 provenance; editorial association, no live stream. |
| [S07-B](../../Storyboard-Board-V3/Shots/S07-B.md) | 84–88 | ECCO, GRAPHICS | Actual hero with optional five capability reminders. | **UNFILLED:** Shared finish and restrained motifs; no simultaneous-mode claim. |
| [S07-C](../../Storyboard-Board-V3/Shots/S07-C.md) | 88–90 | ECCO, BRAND, GRAPHICS | Product and unaltered supplied MIT identity. | **UNFILLED:** Icon-only versus full logo, approved wording and end hold. |

## Historical source mapping

| Historical source | V3 reuse target | Limit |
|---|---|---|
| T5/T6 shared masters | Hardware/environment consumers in shot map | Assets only; acceptance does not cover new staging |
| T7 B201 v005/v006 | S02-A/B; event primitives potentially S04-B/D | v006 pending review; no direct timeline/camera carryover |
| T8 B202-S v009 | S02-B/C, S03-A/B/C, S06-A/B | Synthetic data and controls; unwrap not implemented |
| T27 B202-M v007b | S03-A/B/C; supporting S02 accumulation reference | 30-second mechanism library is not the V3 18-second S03 sequence |
| T9 B203 v002 | S04-A/B/C/D respectively retrieval/support/channel/wear | Adapt explanatory proofs; no new-cycle acceptance implied |
| T10 B204 v001 | S05-A/B/C | Circulation-only schematic; CAD stage-map limits persist |
| A03 numeric 22-shot inventory, T31 17-shot architecture and T41 S02 previs | Historical research only | Counts/titles do not establish one-to-one V3 identity; use exact V3 source card |

No agent should fill these slots by copying generated sensor anatomy, fictional logs or historical camera transforms. Resolve actual geometry and controls in the authorized execution environment.
