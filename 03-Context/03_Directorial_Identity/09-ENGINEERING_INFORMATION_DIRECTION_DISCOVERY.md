# Engineering Information Direction — Discovery v0.1 (Module 09)

**Created:** 14 October 2026  
**Status:** Research/discovery discipline. **Information-representation decisions are not technically/client-approved.** Rolladice's existing typography and graphic-integration preferences are recorded separately in [module 08](08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md).  
**Responsibility:** Artistic and narrative presentation of supplemental technical information within a film.  
**Not the authority for:** physical truth, client engineering validation, data provenance, product calculations, the actual CFD/FEA model, official MIT charts or corporate style.

## 1. What this discipline is

An engineering film contains more than scenes of a product in operation. It can also communicate a **measurement, computed value, derived property, operational state, simulation output, comparison, spatial annotation, progressive accumulation, or engineering interpretation**. These are not necessarily simulations in themselves. Their on-screen form may be typography, plotting, vector illustration, highlighting, a diagram, a 2D/3D graphic, a cutaway or a transition.

**Directorial problem:** select **which information is worth showing, what it means, where it belongs in the cinematic composition, how it enters and exits, and how it connects to the physical scene**.

Do not treat information as generic decorative overlays. It may be the primary narrative subject of an entire sequence. The art of integrating it is **Engineering Information Direction**; typography and motion graphics are two possible means, **not the whole field**.

## 2. Important distinction — source truth vs presentation

Every information element requires a declared *epistemic kind*:

| Kind | Meaning | Safeguard |
|---|---|---|
| Observed/measured | Sensor, test, instrument or actual field reading | Identify source, device/data identity, time/conditions, units and precision where applicable |
| Calculated/derived | Arithmetic or analytic result based on other values | Source quantities, formula/model assumptions and uncertainty/limitations must be traceable |
| Simulation result | An output **extracted from a model run** (e.g., CFD velocity contour, pressure, FEA stress) | Record dataset/run, variable, units, range, conditions and display scale; never label it measured field data |
| Operational state | Actual or planned system status (recording, rotating, moving, completed) | State transitions must be sourced; mock/schematic states must be labeled |
| Conceptual/illustrative | Simplified or hypothetical explanation | Avoid unmarked numeric claims, calibrated-looking legends or 'actual data' implication |
| Interpretation/conclusion | Meaning inferred from a pattern or result | Show evidence and level of confidence; avoid claiming more than approved engineering supports |

**Measurement and calculation are often chained**: a measured echo time can contribute to a derived stand-off distance. A simulation result can become a summarized KPI, but the KPI retains its simulation provenance.

Scientific precedents:
- NASA SVS on art+science and data-backed visual truth: https://svs.gsfc.nasa.gov/gallery/visualization-principles/
- IBM Design Language on chart labels, motion and avoiding misleading transitions: https://www.ibm.com/design/language/data-visualization/design/basics/
- Ansys on CFD post-processing (vectors, scalars, calculations, animation and plots): https://ansyshelp.ansys.com/public/Views/Secured/corp/v252/en/cfx_intr/i1312123.html
- NIST on measurement results and uncertainty: https://www.nist.gov/pml/nist-technical-note-1297/nist-tn-1297-7-reporting-uncertainty

These resources inform *technical communication principles*, not confirmed Rolladice taste preferences.

## 3. Information families and visual questions

| Family | Information question | Candidate expression, not a mandated style |
|---|---|---|
| Measurement | What is the observed value and reference? | dimension, waveform marker, scale-aware readout, spatial point |
| Calculation | How does one quantity yield another? | relation, transformation, limited on-screen equation, derived result |
| State | What mode/condition has changed? | state marker, status transition, phase |
| Simulation result | What did the model produce? | validated contour/legend, vector field, clipped section or summary plot |
| Comparison | Against what baseline does this matter? | aligned geometry, reference outline, difference map, paired data |
| Annotation | Which component/location is relevant? | leader, anchored callout, geometric highlight |
| Accumulation/history | How do repeated measurements become structure? | incremental plotted marks, spatial map, sampled trajectory |
| Interpretation | What can legitimately be concluded? | evidence-oriented highlight, qualified statement, conclusion |

One semantic family may have multiple presentation methods. A motion-graphic flourish is **not** itself an information family.

## 4. Information choreography

An information beat should have a narrative **lifecycle**:

1. **Motivation:** what phenomenon/action creates the need for information?
2. **Origin:** which sensor, model, source or state produces the value?
3. **Introduction:** when does the audience first encounter the information?
4. **Relationship:** how is it spatially/causally tied to the subject or shot?
5. **Emphasis:** which variable, threshold, pattern or change matters and why?
6. **Recognition:** allow sufficient legibility for the intended audience and edit rhythm.
7. **Resolution:** does the information persist, transform into a result or hand off to the next scene?

The camera may navigate **information as a subject**, not only a physical object. Choose between (a) world-anchored information, (b) 2D editorial presentation, (c) a dedicated diagram/data-space, (d) a contextual cutaway or (e) a hybrid. Select for clarity and integrity; do not force holographic text and HUDs.

Tie this to [Rolladice Camera & Motion Language](05-CAMERA_AND_MOTION_LANGUAGE_v0.2.md) without duplicating camera-spline rules.

## 5. ECCO examples — conceptual, not approved production designs

### S02 — Pulse/echo → measured time → derived spatial distance

An ultrasonic return is recorded. A waveform can present transmission and echo arrival; their round-trip interval informs a **derived stand-off distance**, after mud sound-speed calibration and correct sensor offset/corrections. Consecutive readings produce a 360° outline. Do not invent a waveform, speed, measured interval, numeric radius or physically calibrated accuracy. See [S02 V2](../02_Storyboard/V2/ECCO_Section_02_Reveal_The_Principle_Padlet_v2/PADLET_SECTION_02_V2.md) and [Engineering Baseline](../01_Foundation/02-ENGINEERING_BASELINE.md).

### S03 — Geometry vs amplitude as *different* mapped quantities

White nominal bit-size reference, blues for enlargement and red for tight spots are client-proposed geometry conventions. A separate yellow/brown map indicates acoustic amplitude patterns. Neither colormap is a generic Rolladice preference. Do not visually imply one dataset morphs mathematically into the other.

### S05 — MIT simulation-derived information

MIT's actual FEA/flow analysis material was requested in client comment C08 and has **not** been verified/imported. A credible presentation would identify which simulation variable is shown, its spatial field, units/legend, scenario and whether an image is actual analysis or illustrative. Do not generate a simulation-looking contour and claim it is MIT's actual result.

### S06 — 3D sampled borehole → unwrapped information space

A conceptual longitudinal seam/unwrapping explains the same recorded measurements in a new 2D coordinate view. It is not physical cutting and not live downhole transmission. The ENP1 example log is rights-sensitive and cannot be republished without permission.

## 6. Proposed information-beat specification

```yaml
information_beat:
  id: TBD
  question_for_viewer: TBD
  source_kind: measured | derived | simulation_result | state | illustrative | interpretation
  exact_source_file_version: TBD
  quantity_or_claim: TBD
  units_and_scale: TBD_OR_NOT_APPLICABLE
  reference_and_assumptions: TBD
  uncertainty_or_limitations: TBD
  reviewer_and_approval: pending
  temporal_relation_to_scene: TBD
  visual_anchor: world | frame | data_stage | cutaway | hybrid | TBD
  candidate_representation: TBD_NOT_A_STYLE_PRESET
  emphasis_and_read_time: TBD_AFTER_PREVIS
  exit_or_persistence: TBD
  visual_qa: readability_source_integrity_and_correct_mapping
```

**The human director/agent must make the creative choices** and record their rationale. No fixed fonts, color palettes, plot aesthetic, animation recipe or numerical measurements are implied by this schema. A value displayed without a unit, reference, reasonable precision or appropriate uncertainty can mislead.

## 7. Taste discovery plan

Investigate separately:
- **Information hierarchy:** information as supporting annotation vs the hero of a scene.
- **Representation:** numeric readout, chart, geometry-anchored mapping, diagram, abstract but meaningful metaphor.
- **Spatial relationship:** anchored to physical geometry, in an editorial 2D plane, or a separate transformed data space.
- **Narrative rhythm:** reveal versus accumulate versus compare versus resolve; coexistence with camera choreography.
- **Legibility and restraint:** when selective emphasis beats a crowded screen.
- **Trust:** audience recognition of actual measurements, derived values, hypothetical examples, simulation outputs and engineering interpretation.

Potential studies: Territory Studio **Desktop Metal**, NASA **Scientific Visualization Studio**, Ansys results post-processing and IBM **Data Visualization Design**.

**Typography already has initial evidenced taste** in [module 08](08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md); this module does not redefine it. The presentation taste for specific engineering information families, visual quantities, scientific charts and data-heavy sequences remains under discovery. This document defines their semantic/directorial discipline and research questions, not a new art-style prescription.

## 8. Authority and production boundary

- Technical source and permissible claims: [Engineering Baseline](../01_Foundation/02-ENGINEERING_BASELINE.md), [Storyboard V2](../02_Storyboard/README.md) and [Decision Register](../01_Foundation/06-DECISIONS_AND_READINESS.md).
- Creative staging: [Rolladice Personality](01-ROLLADICE_CREATIVE_PERSONALITY_v0.1.md), [Typography & Graphic Integration Taste](08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md), and the single [Scene Direction Contract](07-SCENE_DIRECTION_CONTRACT_v0.2.md). An `information_beat` is a subsection of that contract's shot-specific content, not a competing handoff.
- Blender/AI execution and QA: [Production Workflow](../01_Foundation/05-PRODUCTION_WORKFLOW.md).
- This document is the **single home for the meaning and lifecycle of supplemental information**, not another second scene contract.
