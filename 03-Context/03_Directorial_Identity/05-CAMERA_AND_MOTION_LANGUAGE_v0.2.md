# Camera & Motion Language — v0.2

**Date:** 14 October 2026  
**Role:** Translate **P03 / E004** (Tendril camera preference) into intentional, reproducible shot direction.  
**Status:** Practical method proposed for testing, not an endorsed list of camera presets.

## 1. Camera principle: guided discovery

The director values a fluid camera navigating a subject, where **every meaningful stop is a showcase**, and the travel between those stops feels like its own sub-narrative shaped by timing, acceleration and rhythm.

**Do not reduce this to** 'smooth orbit' or 'ease in/out.' A path can be perfectly smooth and still be uninteresting. Plan the *image at arrivals*, then ask what the travel adds.

## 2. Design the composition before the spline

For a continuous shot, build a small **camera score**:

| Element | Required question |
|---|---|
| Entry frame | What is the first visual premise? What is deliberately still concealed? |
| Arrival A | Why should the viewer pause here? Is it a strong frozen composition? |
| Travel A→B | Which spatial relation changes? Does parallax or occlusion communicate something? |
| Arrival B | What new information/emotion does this frame contain that A did not? |
| Exit | How does framing, target direction and velocity hand off to the edit? |

Do not force two arrivals if one is stronger; cut the shot when a continuous move weakens the story. A static shot can also be the right artistic decision.

## 3. Camera pose and travel contract

At **each** principal beat, record:
- **Time or normalized progress:** seconds or fraction of shot (clearly labeled; not fabricated measured velocity).
- **Camera world transform:** loc/rot or a rig target/path reference once a real scene exists; otherwise qualitative path and `TBD_AFTER_SCENE_INSPECTION`.
- **Lens and framing intent:** focal length/projection, subject crop, screen-space target, foreground/mid/background relationship.
- **Subject target:** what the camera is looking at; the target may be animated separately.
- **Visibility change:** which edge, surface, joint or relationship newly enters the picture.
- **Velocity condition:** arriving, settling, continuing, or leaving; no accidental hard stop.
- **Hold purpose:** recognition, understanding, suspense or transition, not a generic number.

At **each transition**, document:
- Curve/path topology and intended orbital/linear components.
- What stays in frame for orientation and what is allowed to leave.
- Approximate screen-space travel of the hero and target.
- Whether speed changes because of geometry, emotion or information density.
- Intentional roll vs unintentional horizon drift; occlusion and collision risks.

## 4. Motion phrasing vocabulary (non-prescriptive)

| Phrase | Directional intention | Use when | Avoid when |
|---|---|---|---|
| **Approach** | Increase proximity and reveal detail | Entry curiosity becomes tactile understanding | Causes clipping or distorts engineering relationships |
| **Arc** | Change silhouette/parallax around a volume | Spatial discovery reveals another face | Implies impossible access or creates aimless circling |
| **Glide** | Maintain continuity across regions | Need graceful visual linkage | Transit adds no new view |
| **Pivot** | Shift point of attention | Comparing related features | Sudden target snap confuses continuity |
| **Rise/descend** | Change scale relationship | Journey through structure or depth | Vertical movement becomes ornament |
| **Settle** | Decelerate into a meaningful arrival | Viewer needs time to read a hero/detail | Every arrival becomes sluggish |
| **Release** | Hand momentum into cut or next shot | An edit continues directional energy | End pose is lost or final meaning unreadable |
| **Hold** | Let a deliberately composed view speak | Comprehension or emotional weight | Static dead time without reason |

Names are shorthand, not keyframe presets. Specify actual resulting screen imagery.

## 5. Timing, acceleration and continuity

**Plan by visual events, not evenly divided clip length.** A proposed eight-second motion can be scored as: entry, approach, first arrival, reframing travel, final arrival, resolution. Exact times require preview and editorial context.

A credible continuous move may need:
1. A gentle initial departure whose subject silhouette is readable.
2. Acceleration while the viewer has a stable spatial landmark.
3. Braking as a new surface becomes legible.
4. A brief natural recognition interval at a showcase composition.
5. Renewed momentum as the next idea becomes visible.
6. Settling or purposeful directional release at the ending.

**Do not force all six phases.** Sometimes a hard cut, static observation or straight constant-rate move is superior.

### Rigging and Blender implementation

- Prefer a separate **camera rig, path, and look target** so translation and gaze can be tuned independently where appropriate.
- For a curved move, a Bezier/NURBS path or parent rig may be useful; for hand-shaped movement, keyed transforms and custom animation curves may be better.
- In Graph Editor inspect actual location/rotation and derived screen-space motion, not merely keyframe curve smoothness.
- Maintain at least C0 positional continuity at joins; for a perceptually seamless glide, evaluate **velocity and acceleration** around arrival/restart rather than accidentally forcing a stop. Intentional holds are legitimate and should be separately marked.
- Avoid unmotivated banking/roll, subject drift off-frame, autofocus/target snaps, clipping and scale jumps.
- Check animated targets, constraints and parenting at intermediate frames; control interpolation and handles intentionally.
- A camera in Blender is a controllable reference. Do not expect generated video to reproduce its trajectory until motion fidelity is tested.

### Camera movement and object movement are different authorities

Mark whether the tool is moving, the camera is moving, or both. An isolated product hero can use a stationary model and a moving camera; drilling/scanning explanations must retain correct operating motion. Use [Engineering Baseline](../01_Foundation/02-ENGINEERING_BASELINE.md).

## 6. Camera plan assets (cheap first)

Create editable source/diagram assets where useful:

1. `camera-plan.svg`: top/side view of approximate object bounds, paths, target changes, occlusion and important views. Label it conceptual until linked to actual CAD coordinates.
2. `beat-frames.svg` or quick Blender screen grabs: entry/major arrival/exit framing and safe margins.
3. `camera-score.md`: timed or normalized beats and what each communicates.
4. **Blender playblast**: final arbiter of real timing and perceptual smoothness, with source revision/path and exact frame range.

The SVG is not a measurement tool unless exported from actual scene coordinates and verified.

## 7. Critique against the director's taste

- **Arrival:** Is every showcased frame worth landing on? Does the subject feel significant and specifically observed?
- **Journey:** Does transit reveal changing relations or anticipation, rather than dead movement?
- **Flow:** Is camera velocity continuous where intended? Does deceleration feel like a deliberate sentence ending?
- **Orientation:** Can viewers follow what part of the object is being observed?
- **Breath:** Does the camera give the viewer sufficient time for the image to speak?
- **Truth:** Has the desired movement incorrectly suggested that the product rotates or operates differently?
- **Difference:** Would a simpler cut or static view communicate more? If yes, prefer it.

## 8. Applied case

See [ECCO S07-01 Directing Study](examples/ECCO_S07-01_direction_study.md) and its SVG path sketch. It is a proposed direction to validate with actual product geometry, not a final approved motion.
