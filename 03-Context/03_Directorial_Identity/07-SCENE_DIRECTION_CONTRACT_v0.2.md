# Scene Direction Contract — v0.2

**Purpose:** A reproducible handoff from an AI/human director to Codex/Blender production.  
**State:** Candidate contract, not yet production-tested. Do not confuse a filled contract with technical approval.
**Amendment (17 October 2026):** Adds mixed-audience comprehension and discovery/payoff review; preserves the v0.2 schema and existing stage gates.

## Source-of-truth hierarchy

Engineering/client technical authority → project/brand constraints → narrative purpose → documented Rolladice taste → shot-specific artistic decisions → execution convenience.

Before making a creative choice, check [Personality](01-ROLLADICE_CREATIVE_PERSONALITY_v0.1.md), [Evidence](02-TASTE_EVIDENCE_REGISTER.md), [Casebook](04-VISUAL_DECISION_CASEBOOK_v0.2.md), [Camera](05-CAMERA_AND_MOTION_LANGUAGE_v0.2.md) and [Look](06-LOOK_LIGHTING_AND_MATERIAL_DIRECTION_v0.2.md). **When text or motion graphics matter**, also consult [Typography & Graphic Integration v0.3](08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md). For measured, derived, simulated or interpreted on-screen information, use [Engineering Information Direction](09-ENGINEERING_INFORMATION_DIRECTION_DISCOVERY.md) to document provenance and on-screen lifecycle **within this same scene contract** (not another handoff).

## Minimum deliverable for a proposed shot

1. **Shot purpose and audience:** factual message, target audiences and prior knowledge, one-sentence *non-technical audience takeaway*, expert-verifiable technical meaning, why the result matters, and transition to next shot.
2. **Authority register:** which geometry, mechanism, dimensions and movement are verified; pending client questions, owner and blocking level.
3. **Core visual premise:** why this particular composition? What makes the subject present, distinctive and understandable?
4. **Camera score:** entry, all meaningful showcase arrivals, traversal purpose, gaze, lens/projection rationale, spatial continuity, timing/rhythm and exit.
5. **Objects and events:** authoritative animation mode, key interaction, occlusion, final state and asset provenance.
6. **Look plan:** motivated lighting, reflection hierarchy, silhouette, environmental depth, candidate material finish and whether artistic representations require technical disclaimer/approval.
7. **Diagrams:** lightweight, editable conceptual `camera-plan.svg` and `beat-frames.svg` when spatial planning benefits; these are not exact geometry.
8. **Implementation handoff:** scene file/link targets, units, FPS/aspect from project, concrete keyframe targets only once the relevant geometry is available, proposed render mode, pass/mask needs, QA conditions.
9. **Review:** initial assistant critique, director response, technical review state, shot version and accepted/rejected alternatives.
10. **Typography/graphics:** apply the evidence-backed typography preferences and *optional* 3D/on-screen graphic integration in [module 08](08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md) only when scene-appropriate. Record exact copy and whether it is approved. Font specifics, annotation systems, data-graphics language and motion-design parameters remain **UNDISCOVERED**.
11. **Audience proof:** define a minimal *cold-viewer* comprehension question (what was discovered/changed; why it matters), the key visual comparison or consequence if relevant, and a separate expert truth/provenance check. Test the actual moving preview, not just the scene's technical implementation or attractive stills. If the sequence relies on voiceover or a label, specify that dependency rather than claiming silent clarity.

## Machine-readable draft — `scene-directive.yaml`

```yaml
schema: rolladice-scene-directive/v0.2
shot_id: S07-01
status: proposal_not_approved
source:
  client: MIT
  technical_reference: "03-Context/01_Foundation/02-ENGINEERING_BASELINE.md"
  visual_identity: "03-Context/01_Foundation/03-MIT_PRODUCTION_IDENTITY.md"
  creative_personality: "03-Context/03_Directorial_Identity/01-ROLLADICE_CREATIVE_PERSONALITY_v0.1.md"
  taste_evidence: [E002, E003, E004]
timing:
  duration_seconds: 8 # provisional existing storyboard
  fps: TBD_FROM_PROJECT
  aspect: TBD_FROM_PROJECT
subject:
  product_asset: TBD_REGISTER_AND_VALIDATE
  verified_geometry: false
  product_motion: proposed_stationary_for_hero
narrative:
  engineering_message: "Present genuine ECCO engineering"
  emotional_goal: "Confident technological presence"
  core_image_idea: "Fluid discovery through purposeful detail arrivals"
audience:
  groups: [engineers, non_technical_stakeholders] # illustrative MIT audience example; confirm for each project
  prior_knowledge: mixed
  nontechnical_takeaway: TBD_ONE_PLAIN_LANGUAGE_SENTENCE
  expert_truth_check: TBD_SOURCE_GROUNDED_RELATIONSHIP
  why_it_matters: TBD_GROUNDED_CONSEQUENCE_NO_UNSUPPORTED_VALUE_CLAIM
  discovery_or_comparison: TBD_IF_RELEVANT
  comprehension_check: "Can a new viewer explain the discovery and significance after the preview?"
camera:
  pose_units: scene_units
  lens_mm: TBD_AFTER_BLOCKING
  rig: separate_camera_path_and_gaze_candidate
  beats:
    - id: ENTRY
      purpose: establish_recognizable_silhouette
      time_seconds: TBD_AFTER_PREVIS
      pose: TBD_AFTER_SCENE_INSPECTION
    - id: ARRIVAL_A
      purpose: reveal_verified_product_detail
      time_seconds: TBD_AFTER_PREVIS
      pose: TBD_AFTER_SCENE_INSPECTION
    - id: ARRIVAL_B
      purpose: resolve_on_product_presence
      time_seconds: TBD_AFTER_PREVIS
      pose: TBD_AFTER_SCENE_INSPECTION
  motion_phrasing: "travel reveals; slow into meaningful arrivals"
look:
  lighting_intent: "sculpt readable verified surfaces; candidate"
  material_authority: "actual material/finish requires MIT confirmation"
  atmosphere: restrained_if_spatially_useful
graphics:
  direction_reference: "03-Context/03_Directorial_Identity/08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md"
  exact_copy: TBD_IF_TEXT_REQUIRED
  text_treatment: choose_none_screen_overlay_or_spatial_by_story
  typography_starting_point: quiet_elegant_sans_serif_editorial_if_context_suits
  text_animation: quiet_appearance_or_graceful_movement_if_needed
  technical_graphics_style: UNDISCOVERED_VALIDATE_PER_SHOT
  technical_labels: only_if_approved_and_needed
hybrid:
  motion_authority: blender
  appearance_anchors: choose_first_last_or_both_after_previs
checks:
  - first_and_arrival_frames_composed
  - no_false_product_geometry
  - continuous_camera_travel_or_documented_cut
  - no_unapproved_material_claims
  - final_view_readable
  - cold_viewer_understands_essential_discovery_and_why_it_matters
  - expert_checks_technical_meaning_and_provenance_separately
  - typography_and_graphics_legible_if_present
  - exact_required_text_is_approved_or_placeholder
  - technical_review_recorded
files:
  camera_plan_svg: conceptual_only
  beat_frames_svg: conceptual_only
  blender_playblast: NOT_YET_CREATED
approvals:
  director: pending
  client_technical: pending
```

**Important:** YAML values above are candidates or placeholders. Never present the sample as executed, technically validated or an approved ECCO direction.

## Release gates

- **D0 — Concept:** engineering purpose and source facts clearly separated from hypotheses; visual direction stated; target audience and non-technical takeaway identified.
- **D1 — Art direction:** hero compositions and camera-score rationale accepted internally, or explicitly released as a test; director can identify the intended discovery/consequence a non-specialist should recognize.
- **D2 — Execution-ready:** exact scene/asset versions, coordinate system, frame rate, path poses and lens have been derived from source/Blender, not invented; implementation unknowns recorded.
- **D3 — Animatic reviewed:** representative frames and continuous motion inspected for meaning, continuity, intended audience comprehension and technical correctness; client engineering approval obtained where necessary. A procedural/scene-check pass alone never proves comprehension.
- **D4 — Finishing:** only after scene-specific dependencies are resolved; use [production workflow](../01_Foundation/05-PRODUCTION_WORKFLOW.md) and [Blender animation reference skill](../00_Skill/blender-animation-reference/SKILL.md).

Do not block safe exploration because an unrelated technical question remains unresolved. Do not present a speculative scene as execution-ready.

## Agent handoff instruction

"Implement the attached director-approved or explicitly experimental scene contract. Verify source asset/coordinate system and engineering restrictions before assigning transforms. Treat conceptual SVG as spatial explanation, not exact camera path. Preserve product and effect identities, generate a low-cost Blender playblast first, inspect entry/arrivals/transitions/exit **and the non-specialist discovery/meaning payoff**, and report deviations. Do not generate expensive finishing, alter approved geometry, or invent precise fonts/data-graphics styling/animation parameters as confirmed Rolladice taste. Use the typography evidence module when relevant, while deferring unresolved specifics to director review."

## QA / critique

- Can a viewer without prior domain knowledge say what changed or was discovered and why it matters, using the proposed preview and any explicitly planned minimal wording?
- Can a technical reviewer recognize the correct mechanism and source-versus-synthetic data distinction without an invented effect, exaggerated geometry, or unsourced business benefit?
- Does the camera/graphic emphasis show the result and its meaningful difference rather than spending the entire sequence on acquisition detail?
- Does every meaningful camera arrival communicate something new?
- Is the journey itself expressive, fluid and legible rather than empty travel?
- Would a major held frame still make a visual statement?
- Is subject presence achieved with coherent space and material, not added spectacle?
- Does darkness reveal deliberately rather than erase important engineering?
- Are all quantities, hardware changes and physics grounded or clearly pending?
- Can another agent reproduce the direction using registered assets and actual scene coordinates?
- What was actually previewed/inspected? Do not claim validation without evidence.
