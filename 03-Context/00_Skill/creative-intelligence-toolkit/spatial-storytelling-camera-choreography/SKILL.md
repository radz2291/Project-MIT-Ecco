---
name: spatial-storytelling-camera-choreography
description: Plan and critique spatial storytelling through framing, subject staging, depth, camera viewpoints, meaningful visual arrivals, movement paths, timing, acceleration, holds, and edit continuity. Use when directing a cinematic shot, product or architectural reveal, 3D scene, animated camera, virtual tour, documentary sequence, or storyboard; when a camera move feels generic or purposeless; or when converting a scene idea into a medium-agnostic camera score, beat frames, and lightweight SVG plans. Applies without prescribing a director's taste, software, lens preset, or physical geometry.
---

# Spatial Storytelling & Camera Choreography

Direct **what the viewer experiences in space and time**, not just where a camera travels. Design images with intention, then choreograph how the viewer discovers, compares, anticipates, or resolves them.

## Responsibility

- **Own:** frame composition, spatial relationships, viewpoint, depth hierarchy, subject-camera coordination, meaningful visual arrivals, camera movement intent, rhythm, transitions, shot continuity, and conceptual previs.
- **Do not own:** discovering a person's aesthetic preferences, choosing among unrelated brand styles, technical product truth, measurement semantics, arbitrary equipment presets, physically implementing a camera rig, final rendering, or client approval.
- **Use external inputs:** project narrative, verified scene geometry, delivery constraints, reference frames, taste profile, established editing context. Do **not** copy any named studio's signature style or embed one person's preferences here.
- **Adjacent skills:** `discover-creative-taste` supplies evidenced preferences; `contextual-aesthetic-judgment` helps decide among competing high-level approaches; information-visualization and implementation skills handle their distinct downstream work.

## Inputs and minimal clarification

Start with the intended viewer takeaway, subject/setting, known action, approximate duration/format, and relevant preceding/following shot if available. Also identify what is **observed**, **verified**, and **only proposed**.

Do not demand exact lens, coordinates, storyboard panels, or an asset file before producing a conceptual direction. Ask **one** clarifying question only when missing information genuinely changes the shot's purpose or physical truth; otherwise state assumptions and plan at conceptual fidelity.

For a supplied frame, animation, or scene file, inspect it where tools allow; never invent details of material that has not been viewed.

## Workflow

### 1. Express the visual story as a change

Complete this sentence in plain language:

> "The viewer begins by perceiving **X**, then discovers **Y**, and leaves understanding/feeling **Z**."

Specify which relationships must stay accurate: actor/object location, size, orientation, causality, scale, or direction. Separate the **story event** from the **cinematic depiction** of that event.

Identify whether the job is to **reveal**, **orient**, **inspect**, **compare**, **follow**, **build anticipation**, **demonstrate a mechanism**, or **linger**. This determines what camera and staging need to accomplish.

### 2. Stage the space before designing a path

Make a simple spatial model with **subject**, **secondary objects**, **background**, and **occluders** as relevant. Establish near/middle/far relationships, viewer orientation, foreground parallax, and what can legitimately be seen from each viewpoint.

Mark physical/technical restrictions (e.g., a moving mechanism, the location of a wall, a fixed prop, accessible camera clearance). If geometry is not yet available, label positions as **conceptual/not to scale**, not measured coordinates.

Distinguish movement authority explicitly: **camera**, **subject**, **environment**, **graphics**, or a combination. Do not animate the subject merely to make the camera shot dramatic if that changes the story's real mechanism.

### 3. Author the images worth seeing

Choose a few meaningful **view beats**, not an arbitrary number of keyframes:
- **Entry image:** orient attention; establish what is seen and what's withheld.
- **Discovery image(s):** introduce a new feature, relation, scale shift, or emotional state.
- **Resolution image:** make the central idea readable and establish the handoff.

For each view, describe the **screen image**: crop, subject position, scale, visual hierarchy, angle, depth and negative space, information now visible, and what viewer attention should do.

**Arrival test:** Would this frame communicate its assigned idea if the movement paused here? If not, improve the image or eliminate the arrival. Not every beat needs a stopped camera; a glancing pass may be intentional.

### 4. Choose move, hold, cut, or subject motion

For each transition ask: **What changes for the viewer during travel?**

| Treatment | Useful when | Failure mode |
|---|---|---|
| Static composed view | Observation, precision, weight, comprehension | Dead time or unresolved visual hierarchy |
| Cut / match cut | New information is clearer without travel | Lost orientation, mismatched scale/direction |
| Push / retreat | Shifts perceived proximity and detail/scale | Generic zoom with no payoff |
| Arc / orbit fragment | Reveals changing silhouette, occlusion or depth | Aimless circling, false object behavior |
| Track / glide | Preserves continuity across related features | Transit communicates nothing |
| Pivot / gaze shift | Reassigns attention across an existing space | Sudden target snap or unclear anchor |
| Rise / descent | Reveals vertical relationships or layered scale | Decorative camera excursion |
| Follow | Conveys action or shares a subject's movement | False motion causality or distracting reframing |

These are **options, not signature moves**. Sometimes the best choreography is no camera movement.

### 5. Give travel its own sentence

When moving, plan the *between*, not just start and end:
- **New perception:** which alignment, silhouette, reflection, occlusion, or parallax relationship changes during the path?
- **Attention continuity:** which recognizable landmark remains long enough to keep orientation?
- **Gaze choreography:** what does the camera attend to as attention transfers, separate from camera position?
- **Rhythm:** where does movement accelerate, maintain flow, brake, settle, or release into the cut?
- **Purposeful pauses:** hold only as long as needed for perception, feeling, or information to register.

Do **not** mechanically impose easing or smoothness. A calibrated linear scan, sudden reveal, handheld observation, direct cut, or deliberate hard stop may be the better choice. Specify a reason for unusual velocity or acceleration.

Check both **world-space camera behavior** and **what the subject appears to do on screen**. A physically smooth path can feel jerky when projected; a technically correct camera trajectory can still produce weak framing.

### 6. Choreograph across shots

When planning more than one shot, document handoffs:
- **Screen direction and orientation:** avoid accidental reversal of established movement or left/right relationships. A deliberate reversal is valid when made legible.
- **Scale and viewpoint change:** bridge wide-to-detail or front-to-back transitions without disorienting the viewer.
- **Velocity and editorial rhythm:** decide whether a cut stops motion, sustains it, or purposefully contradicts it.
- **State continuity:** track object configuration, actor/action state, lighting/graphics if relevant, and what has been revealed already.
- **Information continuity:** avoid revisiting the same explanation without new meaning.

Use familiar film grammar (including axis/eyeline checks) as a diagnostic, not an automatic ban on expressive crossings.

### 7. Previsualize cheaply and inspect the sequence

Choose the lowest-fidelity artifacts that can test the uncertainty:
1. **Beat frames:** two or more small framing sketches, storyboard crops, or sourced stills for major perceptual changes.
2. **Camera plan:** conceptual overhead/side SVG or sketches marking subject, path, gaze targets, occlusion and allowed movement. Use the optional [generic SVG camera-plan template](assets/camera-plan-template.svg); it is **not metric**.
3. **Camera score:** ordered beats and transitions with purpose and qualitative timing; see [camera score and QA reference](references/camera-score-and-review.md).
4. **Timed animatic/playblast:** necessary to evaluate rhythm, intermediate compositions, abrupt target shifts, comprehension intervals and continuity.

Avoid fabricating focal lengths, camera transforms, duration, FPS, acceleration values or subject dimensions. If the user supplies validated scene coordinates and requests execution, hand that to the actual implementation workflow rather than treating a conceptual SVG as a rig specification.

### 8. Critique, refine, and hand off

Review the whole sequence (not only hero stills): **meaning, orientation, visual arrival quality, active travel, temporal readability, emotional rhythm, truthful spatial relationships, and edit continuity**.

If weak, diagnose **what failed on screen** before prescribing a technical fix. Consider changing the framing, removing a beat, using a cut, shortening travel, or adjusting subject blocking before adding complexity.

Deliver a concise direction: **visual premise + beat frames + camera score + conceptual path/targets if helpful + unknowns + one cheapest meaningful next test**. Report exactly what was **proposed**, **illustrated**, **previewed**, or **approved**.

When implementation is requested, hand off to the project's scene/build system. This skill does not become a substitute for an application's scene contract, mechanical validation, or animation toolchain.

## Interaction and scope discipline

- When the user wants one shot direction, give **one strong design plus a credible simpler alternative** where useful; don't turn every request into a storyboard package.
- Preserve the artistic director's available freedom; the movement vocabulary is **not a recipe**.
- Prefer diagramming with simple SVG or storyboard sketches before expensive CG when it reduces uncertainty.
- Don't insist on motion to create sophistication. A still image can be the highest-quality arrival.
- Do not equate 'cinematic' with slow gliding, shallow depth of field, dark grades, orbiting, or spectacle.
- If visuals explain a real mechanism, prefer reviewed references and flag conceptual effects as illustrative.
- Do not assume a generative video model follows an intended camera path precisely; inspect the resulting video.

## Completion checklist

- Is each view beat assigned a distinct meaning?
- Does each movement or cut alter what the viewer perceives?
- Can the viewer stay oriented through space, gaze shifts, and scene changes?
- Are timing and acceleration narrative decisions, not default curves?
- Are camera and subject motion clearly distinguished?
- Are all factual/geometry claims grounded or labeled unverified?
- Could another artist stage a coherent preview from the handoff **without copying a reference studio**?

For non-obvious choices, compare behavior against the synthetic [calibration scenarios](references/scene-calibration.md) before adopting this draft as a mature skill.
