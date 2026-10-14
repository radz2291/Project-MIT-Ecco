# Camera Score, View Beats and Review Criteria

Use this reference when a request needs a reproducible scene-direction handoff or full-sequence critique. Keep the core SKILL.md workflow short; this file owns the extended recording format.

## Three representations of one shot

**1. Beat images / frame cards** define *what is visible* at key perceptual moments. They are stills, sketches, or scene snapshots—not proof of motion.

**2. Camera path diagram** defines *how spatial relationships may change*. It can show intended camera route, viewing direction, blocking objects, reveal boundaries and target changes. The supplied SVG template is conceptual and never a validated CAD plan.

**3. Camera score** defines *what happens in time*. It captures beats and the reasons for traversals, pauses, gaze changes and edits. A real animatic/playblast is needed to judge perceptual timing.

Keep all three representations mutually consistent. If a new view is added, adjust the score and path; if the scene orientation changes, update the frame sketches.

## Compact camera score

```yaml
schema: spatial-camera-score/v0.1
status: conceptual_direction   # not executed or approved
scene_purpose: "What the viewer should learn or feel"
subject_source: "verified asset | supplied sketch | hypothetical"
viewer_state:
  before: "what is initially known"
  after: "what new relationship becomes clear"
spatial_anchors:
  - "distinct feature or fixed landmark"
motion_authority:
  camera: moving_or_static
  subject: source_verified_or_illustrative
beats:
  - id: ENTRY
    progress: "opening portion (no numeric time asserted)"
    viewer_sees: "dominant subject with identifiable silhouette"
    screen_composition: "relative position / scale / depth / clear space"
    camera_mode: "static | travel | cut | TBD"
    look_target: "feature or relation, if known"
    purpose: "orient"
  - id: DISCOVERY
    progress: "middle"
    viewer_sees: "a new relation enabled by parallax/occlusion"
    screen_composition: "foreground feature remains recognizable"
    camera_mode: "curved track candidate"
    look_target: "specific feature as it becomes visible"
    purpose: "reveal"
  - id: RESOLUTION
    progress: "closing"
    viewer_sees: "clear spatial arrangement"
    screen_composition: "readable endpoint"
    camera_mode: "settle / cut / continue"
    look_target: "primary relationship"
    purpose: "resolve"
transitions:
  - from: ENTRY
    to: DISCOVERY
    change_during_travel: "which new fact/feeling emerges"
    orientation_anchor: "persistent landmark"
    velocity_phrase: "qualitative change, not arbitrary numeric curve"
    screen_space_risk: "subject drift / bad silhouette / occlusion"
editorial_handoff:
  screen_direction: "maintain/change intentionally"
  subject_state: "state carried to next shot"
unknowns:
  - "scene dimensions / exact camera positions / delivery timing"
next_check: "view full timed previs for transit readability"
```

**This example is hypothetical.** Remove irrelevant fields for an actual brief. If an existing project's shot contract owns structured handoff, map these conceptual fields into that contract—**do not create a competing schema**.

## View-beat annotation

For each essential view, specify: intended viewer reaction; subject crop; approximate on-screen center; foreground / middle / background; occlusion; screen-space scale; visual hierarchy; gaze/attention target; and what should be learned by the cut or arrival. Mark if the held image itself is valuable.

Before picking a lens or camera location, test whether the *screen image* carries the idea. If scene measurements and desired projection are available, the implementation artist determines camera parameters from the actual environment. A numeric focal length must not be invented as a universal cinematic preference.

## Movement review pass

During preview, watch at **normal playback speed**, not only individual frames:

| Review question | Signs of weakness | Possible remediation |
|---|---|---|
| Is the discovery legible? | Information appears and disappears before recognition | Reduce simultaneous motion, extend a moment or use a cut |
| Is travel meaningful? | Long movement showing unchanged information | Shorten path, recompose or replace with edit |
| Are arrivals worth reaching? | Endpoint has poor silhouette or no new meaning | Re-author the arrival frame |
| Is orientation preserved? | Unmotivated screen-direction reversal or gaze snap | Keep a landmark or insert an orienting view |
| Is rhythm intentional? | Unexplained braking, stalling or whiplash | Change beat timing and camera/target coordination |
| Is motion truthful? | Moving camera makes a fixed object appear operationally animated | Clarify camera vs object motion or re-stage |
| Is form readable? | Object merges with background/occluders | Adjust framing, staging, visible edges or light |
| Is the edit coherent? | Subject state, axis or direction changes without purpose | Amend shot bridge and continuity notes |

Don't claim preview problems have been solved until the actual updated preview has been inspected.

## Output expectations by fidelity

- **Concept only:** one-sentence premise and 2–4 beat descriptions; proposed movement alternatives.
- **Storyboard-ready:** framing sketches and a camera score with orientation and temporal intentions.
- **Previs-ready:** agreed scene/asset references, beat images, approximate path/target and explicit unverified coordinates.
- **Execution-ready:** project's actual scene units/geometry, camera transforms, lens and FPS, approved blocking, and reviewed animatic. Those values are **supplied/verified**, never fabricated by this skill.

Use the appropriate level for the task, not the most elaborate one by default.
