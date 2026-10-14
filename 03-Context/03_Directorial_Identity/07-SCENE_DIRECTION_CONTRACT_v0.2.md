# Scene Direction Contract — v0.2

**Purpose:** A reproducible handoff from an AI/human director to Codex/Blender production.  
**State:** Candidate contract, not yet production-tested. Do not confuse a filled contract with technical approval.

## Source-of-truth hierarchy

Engineering/client technical authority → project/brand constraints → narrative purpose → documented Rolladice taste → shot-specific artistic decisions → execution convenience.

Before making a creative choice, check [Personality](01-ROLLADICE_CREATIVE_PERSONALITY_v0.1.md), [Evidence](02-TASTE_EVIDENCE_REGISTER.md), [Casebook](04-VISUAL_DECISION_CASEBOOK_v0.2.md), [Camera](05-CAMERA_AND_MOTION_LANGUAGE_v0.2.md) and [Look](06-LOOK_LIGHTING_AND_MATERIAL_DIRECTION_v0.2.md).

## Minimum deliverable for a proposed shot

1. **Shot purpose:** factual message, viewer's desired understanding/emotion, transition to next shot.
2. **Authority register:** which geometry, mechanism, dimensions and movement are verified; pending client questions, owner and blocking level.
3. **Core visual premise:** why this particular composition? What makes the subject present, distinctive and understandable?
4. **Camera score:** entry, all meaningful showcase arrivals, traversal purpose, gaze, lens/projection rationale, spatial continuity, timing/rhythm and exit.
5. **Objects and events:** authoritative animation mode, key interaction, occlusion, final state and asset provenance.
6. **Look plan:** motivated lighting, reflection hierarchy, silhouette, environmental depth, candidate material finish and whether artistic representations require technical disclaimer/approval.
7. **Diagrams:** lightweight, editable conceptual `camera-plan.svg` and `beat-frames.svg` when spatial planning benefits; these are not exact geometry.
8. **Implementation handoff:** scene file/link targets, units, FPS/aspect from project, concrete keyframe targets only once the relevant geometry is available, proposed render mode, pass/mask needs, QA conditions.
9. **Review:** initial assistant critique, director response, technical review state, shot version and accepted/rejected alternatives.
10. **Deferred domains:** typography and motion graphics remain **UNDECIDED** in Rolladice taste v0.2. Preserve known client requirements and placeholders; do not invent permanent graphical style.

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
  typography_taste: DEFERRED_DISCOVERY
  motion_graphics_taste: DEFERRED_DISCOVERY
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

- **D0 — Concept:** engineering purpose and source facts clearly separated from hypotheses; visual direction stated.
- **D1 — Art direction:** hero compositions and camera-score rationale accepted internally, or explicitly released as a test.
- **D2 — Execution-ready:** exact scene/asset versions, coordinate system, frame rate, path poses and lens have been derived from source/Blender, not invented; implementation unknowns recorded.
- **D3 — Animatic reviewed:** representative frames and continuous motion inspected for meaning, continuity and technical correctness; client engineering approval obtained where necessary.
- **D4 — Finishing:** only after scene-specific dependencies are resolved; use [production workflow](../01_Foundation/05-PRODUCTION_WORKFLOW.md) and [Blender animation reference skill](../00_Skill/blender-animation-reference/SKILL.md).

Do not block safe exploration because an unrelated technical question remains unresolved. Do not present a speculative scene as execution-ready.

## Agent handoff instruction

"Implement the attached director-approved or explicitly experimental scene contract. Verify source asset/coordinate system and engineering restrictions before assigning transforms. Treat conceptual SVG as spatial explanation, not exact camera path. Preserve product and effect identities, generate a low-cost Blender playblast first, inspect entry/arrivals/transitions/exit and report deviations. Do not generate expensive finishing, alter approved geometry, or decide unresolved graphics/typography taste without authorization."

## QA / critique

- Does every meaningful camera arrival communicate something new?
- Is the journey itself expressive, fluid and legible rather than empty travel?
- Would a major held frame still make a visual statement?
- Is subject presence achieved with coherent space and material, not added spectacle?
- Does darkness reveal deliberately rather than erase important engineering?
- Are all quantities, hardware changes and physics grounded or clearly pending?
- Can another agent reproduce the direction using registered assets and actual scene coordinates?
- What was actually previewed/inspected? Do not claim validation without evidence.
