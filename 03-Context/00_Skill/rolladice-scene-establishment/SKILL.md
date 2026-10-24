---
name: rolladice-scene-establishment
description: Establish or revise a film, 3D, VFX, motion-graphics, product, or engineering scene before full production. Use for AI Director collaboration, scene meaning, technical truth, representation, styling, camera planning, targeted proofs, or scattered feedback that needs a clear next step. Coordinate existing directing skills through six stages and three approval gates; explain decisions in language an interested 12-year-old can follow. Not a renderer, engineering certifier, fixed visual style, or automatic permission to build.
---

# Rolladice Scene Establishment

**Version 1.1.0 — 25 October 2026.** A risk-triggered visual-communication refinement informed by the ECCO Section 5 retrospective. It retains six stages, three existing approval gates and one scene contract. Reduced iteration is a goal to test, not a proven performance claim.

**Understand the story. Check what is true. Choose what to show. Design the look and movement. Test the uncertain part. Then build.**

Own the order of decisions, not every specialist's job. Use AI Director judgment and the project's existing Scene Direction Contract. Do not create another ticket system, approval register, compulsory storyboard package, or agent hierarchy. One agent may wear several roles; do not spawn agents just because the stages have names.

## 1. Clarity is a prerequisite

Read [Clarity-First Communication](references/clarity-first-communication.md) when loading this skill. Every human-facing proposal, explanation, review, question, progress report and handoff opening must be understandable to an interested 12-year-old. Use mature, ordinary language; never talk down to the user or assume their age.

Lead with **what is happening, why it matters, and the recommendation**. Explain a needed technical word immediately. Put exact quantities, formulas, paths and implementation details after the simple explanation. Do not weaken those details or hide uncertainty. Clear writing is not a reason to make a false claim.

## 2. Recover context before proposing or changing anything

Read applicable `AGENTS.md`, the project context/skill index, the current task and the relevant source/approval records. Locate the actual latest working file and approved baseline; they may differ. Direct updates made with another agent can supersede earlier chat directions. Read live connected records for live status, and the actual local files for local scene state.

Choose one mode:

| Mode | Do now | Do not assume |
|---|---|---|
| Establish | Develop the unresolved scene decisions | A vague idea authorizes a build |
| Continue | Resume from the first unresolved decision | Every stage needs repeating |
| Review | Inspect the supplied artifact against its agreed purpose | Reviewing permits edits or cinematic criticism outside the requested scope |
| Revise | Change the named decision and affected outputs | One rejection cancels all prior approvals |

A user request to execute an already released task goes to the production workflow, not back through discovery by habit. A review-only request stays read-only. A skill never grants permissions beyond the current request and project policy.

Recover: audience, scene role, timing, accepted narrative, technical sources, approved visual choices, rejected directions and reasons, exact asset versions, next/previous scene links, production budget, and unresolved questions. Ask only for a missing decision that changes the next safe action. Do not ask the user to repeat information already available.

Use [Skill Routing](references/skill-routing.md) to load only the specialists needed for the current decision. Missing optional companions do not prevent use of the core workflow; missing critical evidence blocks only the claim or action that depends on it.

## 3. Six stages, not six documents

Record results inside **one existing scene contract**. A sequence may have one shared direction with linked per-shot records if that is already the project's convention.

| Stage | Plain question | Minimum result | Main owner |
|---|---|---|---|
| 01 — Narrative Intent | What should the viewer understand or feel? | Audience, before/after understanding, ordered discoveries, meaning carried by voice/image/sound | AI Director + information storytelling |
| 02 — Truth & Mechanism | What actually happens, and what can we honestly show? | Sources, cause/result chain, movement owners and reference frames where relevant, limits, evidence type and unresolved risks | Domain sources + technical investigator |
| 03 — Visual Representation | What form will make this idea visible? | Chosen visual form, an observable cause/response/change, and a risk-based visual mechanism test when needed | Information direction + representation framework |
| 04 — Art Direction | What should the image look and feel like? | Active project taste, focused references, an inspectable target at intended viewing size and clear exclusions | AI Director + contextual aesthetic judgment |
| 05 — Camera & Motion Architecture | How do the discoveries unfold in time? | Meaningful arrival compositions before paths, active travel, effect states, voice/sound timing and exit | Scene Director + spatial choreography |
| 06 — Targeted Proof & Scene Lock | What is still risky, and has the smallest useful test answered it? | Playback-scale perceptual proof when relevant, reviewed evidence, remaining limits, exact released scope and execution contract | Mechanism review + execution handoff |

Read [Stages and Gates](references/stages-and-gates.md) for stage questions, outputs and pass conditions. Read [Representation and Direction](references/representation-and-direction.md) for translating technical meaning into visible events.

Order the thinking sensibly, not mechanically. A camera-feasibility test can happen early for an impossible-camera idea. Inspect existing CAD before committing to an impossible close-up. But do not start a full build while its meaning, truth, look or main motion remains undecided.

### Visual Communication Check — only when meaning could fail on screen

For an invisible phenomenon, causal interaction, difficult comparison, data transformation or other **material representation risk**, answer these five questions briefly **inside the existing scene contract**. This is not a seventh stage, another approval gate or a mandatory deliverable for ordinary scenes.

1. **Recognize:** What should the viewer recognize without having to guess the physical objects or information?
2. **Locate:** Which subject, surrounding space, reference and relevant boundary must be visible?
3. **See change:** What observable before → interaction → after event proves the intended relationship?
4. **Avoid misreading:** What tempting but wrong interpretation could the image create?
5. **Test cheaply:** Which minimum still, matched comparison or short motion test exposes that risk at actual viewing size and speed?

Keep the narration/image responsibility split: test physical relationships silently where useful, then test the intended full meaning with narration when this is a narration-led film. **Do not require a silent image to explain every technical term.** Check source/engineering truth separately. See [Stages and Gates](references/stages-and-gates.md) and [Proof and Review](references/proof-and-review.md).

When moving subjects interact, identify their independent motion and reference frames **before choosing effects**: e.g. rotating hardware, world-space fluid, carried particles, and independently moving camera. A newly approved operating-mode change reopens only affected mechanism, representation and motion decisions, not every stage.

A risky visual representation may justify an early two-treatment proof (for example surface tracers versus tracers within a volume) before an elaborate animation. For distinctive camera work, inspect a few meaningful **arrival frames before interpolating paths**, then check travel and timing in a cheap preview. Do not add these proofs when the answer is already evident from accepted, inspectable work.

## 4. Three human decisions

- **Gate A — Meaning & Truth:** agree on the scene's purpose, its factual limits and safe illustrative assumptions.
- **Gate B — Creative Direction:** agree on representation, visual language, meaningful compositions and motion plan.
- **Gate C — Production Release:** required proofs pass; the owner authorizes a named build or integration scope.

These are decision summaries, not three extra approval systems. Map them into the project's existing gates. A simple scene may resolve all three in one exchange; an existing approval counts when its scope and version still match. Do not interrupt for every checkbox.

**Approval to test is not approval to integrate. A passed technical check is not human approval.** If the owner has explicitly authorized integration after named checks pass, continue within that permission without another redundant request. Otherwise return the proof and request the one remaining release.

## 5. Small tests before full Blender production

Distinguish three activities:

**Inspection:** read existing files and measure or inspect the current scene without changing it.

**Disposable proof:** an authorized proxy, still or short isolated effect/camera test in a separate version. State its question and budget first. This may use Blender before Gate C; it is not the full production build.

**Production:** assemble the released scene, integrate accepted effects, render and prepare delivery under project rules.

Select the cheapest test that can answer the question. A drawing can explain a mechanism but cannot prove timing. A still can approve a look but cannot approve camera motion. A pretty render cannot prove correct data. **For a risky visual mechanism, test whether the intended viewer can perceive cause and effect before paying to polish its appearance.** Use the reference image, mechanism sketch, cross-section, proxy playblast, matched shader test or short edit that actually tests the risk. Read [Proof and Review](references/proof-and-review.md).

Before release, the scene contract must contain enough truth, intent, assets, target images, motion and acceptance criteria for production to proceed without inventing major creative decisions. Exact transforms and implementation values must come from inspected scene geometry, not invented precision in a concept document.

## 6. Bounded reviews and revisions

Start every review with the named artifact and what was actually inspected. Respect a request to review only engineering, only style or only motion.

State **intended meaning** versus **observed result**. Separate observation, suspected cause and verified cause. Choose the failed decision before prescribing a fix: narrative, truth, representation, art direction, camera/motion, implementation, continuity or rights.

Issue one bounded next step:

**PRESERVE → CHANGE → FREE TO CHOOSE → DO NOT IMPLY → NEXT PROOF.**

Do not keep saying "more cinematic" or "more scientific" without showing what that means. **After two non-improving attempts at the same symptom, stop that adjustment family and diagnose the failed assumption** (mechanism, representation, camera, styling or implementation) with a controlled comparison. This is a reset trigger, not an automatic remake or compulsory new gate. Distinguish a newly requested aesthetic preference from an implementation defect. If the current result meets the agreed test, accept that scope and move forward.

Read [Authority and Decisions](references/authority-and-decisions.md) for conflicts, scoped approvals and change impact. The [Casebook](references/scene-casebook.md) explains the failure patterns this skill is designed to prevent.

## 7. Keep a compact working record

Reuse the existing Scene Direction Contract. The [contract section template](assets/scene-contract-section.template.md) is an optional subsection, not a second source of truth.

Record accepted decisions, exact evidence, owner/scope, experiments, unresolved risks, superseded choices and the next action. Keep source facts, verification results, rights and creative approval as separate fields. Preserve originals and accepted derivatives. Use actual local/project paths and relative asset links; do not assume a chat attachment path exists on another machine.

On continuation, show the current state briefly: **what is settled, what remains, and what will be tested or built next**. Do not replay the entire project history.

## 8. Completion and transfer

Release only the agreed scope; do not equate "scene lock" with permanent perfection or engineering certification. Production may choose rigs, nodes, scripts and efficient implementations within the accepted boundaries. A major change in story, geometry, data meaning, representation, edit or cost returns to its responsible decision.

Examples: [continuous camera](examples/continuous-camera-discovery.md), [cause and response](examples/cause-response-measurement.md), [engineering data](examples/engineering-data-visualization.md). They teach methods, not universal colors, dimensions or shot recipes.

Use [Calibration Scenarios](references/calibration-scenarios.md) to test adoption. Structural validation alone does not prove good directing, reading-level comprehension, engineering correctness or reliable behavior in Codex. Report such limits honestly.
