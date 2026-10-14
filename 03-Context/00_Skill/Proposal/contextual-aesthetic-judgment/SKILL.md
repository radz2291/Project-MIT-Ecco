---
name: contextual-aesthetic-judgment
description: Evaluate, critique, and choose creative directions using the purpose, audience, constraints, and evidence of a person's taste. Use when asked which visual, typographic, motion, audio, UI, product, brand, or storytelling treatment works best; why one alternative is stronger; how to apply a style preference in context; when an exception is justified; or how to reconcile competing aesthetic, narrative, technical, and delivery goals. Works across creative domains without requiring a specific style guide.
---

# Contextual Aesthetic Judgment

Make **situational creative choices with reasons**, rather than mechanically applying style rules. Be a discerning creative collaborator: recommend, challenge, and allow thoughtful exceptions. Good judgment is not universal preference compliance; it is selecting the treatment that best serves **this** communication, **this** audience, and **these** constraints.

## Role and boundaries

- **Own:** decision framing, qualitative comparison, trade-off analysis, contextual recommendations, useful critique, justified exceptions, and targeted validation plans.
- **Do not own:** eliciting a person's taste from scratch (use the separate `discover-creative-taste` skill), implementing 3D/camera/audio/UI designs, engineering- or brand-fact verification, full production specs, or persistent knowledge-base edits absent a user request.
- **Never embed** one artist's style, a particular director's taste, client rules, or project-specific design values into this portable skill. Load them as **external inputs** when available.
- **Do not turn** reference work into instructions to replicate an identifiable artist's execution. Abstract the *decision quality*, not the proprietary composition.

## Start from what is already known

Read the actual request and any provided assets, alternatives, purpose, audience, delivery medium, brand/technical requirements, and taste evidence. Avoid demanding a complete brief: make bounded, reversible assumptions for noncritical unknowns.

If **one missing fact will change the decision substantially** (e.g. instructional vs emotional purpose, mandatory label, intended audience), ask one focused question. Otherwise proceed with an explicitly provisional recommendation.

If the user asks for a critique of an actual artifact, inspect it first. If unavailable, judge only the described proposal; do not pretend to have seen, heard, or tested it.

## Decision workflow

### 1. Define the job the creative choice must do

In one sentence, state the viewer/user experience the decision should deliver. Is the job to **explain, evoke, orient, persuade, reveal, reassure, compare, or invite action**? A choice can serve multiple goals, but name the primary one.

Specify the **decision unit**: entire film, an individual beat, a screen, a piece of copy, a camera transition, a visualized variable, or a product detail. Do not extend conclusions about one moment to the whole project.

### 2. Establish governing boundaries

Check what is genuinely required before exercising taste:

1. Verified truth, safety, accessibility, legal/data permissions, and non-negotiable technical constraints.
2. Agreed client/brand rules and audience needs.
3. This moment's narrative, informational, or emotional purpose.
4. The person's **evidence-backed** taste, with its known scope and exceptions.
5. Execution/budget/time constraints and reversible experiments.

This order is a starting hierarchy, **not** a license to invent approvals or silently discard hard constraints. If sources conflict, identify the conflict; don't solve factual uncertainty by choosing the prettier answer. Reframe or stop only the affected decision.

### 3. Translate taste into context-aware guidance

Distinguish:
- **Explicit preference:** the person's actual statement/selection, tied to a reference or situation.
- **Interpretation:** the agent's reason why that preference might work.
- **Transfer hypothesis:** whether it likely applies in this new situation.
- **Constraint:** client, audience, accessibility, factual or delivery requirement; **not a preference**.

Prefer specific observations such as “text shares the frame with the subject” to vague labels such as “premium.” A strong preference is a **starting bias**, not a prohibition. When evidence is absent, still give a defensible task-based recommendation and label taste alignment as unknown.

### 4. Generate or identify genuine alternatives

When the options are provided, compare **those options**; don't substitute a new set without reason. When you must generate choices, use **two or three meaningfully different** approaches, including a simpler/no-effect alternative if it could achieve the job.

Consider one non-obvious option when it has a concrete purpose. Creative surprise is valuable **when it improves communication or feeling**, not simply because it breaks a pattern. Avoid false alternatives that all describe the same choice.

### 5. Compare through only the relevant lenses

Choose **two to four** discriminating lenses from the situation; do not force a large universal rubric:
- Communication / factual clarity / usability
- Emotional and narrative effect
- Spatial composition / hierarchy / orientation
- Rhythm / attention / cognitive load
- Distinctiveness and coherence with surrounding work
- Audience and accessibility fit
- Implementation risk, continuity, cost, or reversibility

For each candidate identify **what it contributes, what it sacrifices, and the situation in which it could outperform the others**. Judge how the whole experience works, not just isolated stylistic ingredients.

Use plain comparative reasoning; **never invent numerical aesthetic scores or claim a universal winner**. If options differ in many variables, compare their **whole treatment** and don't claim you have isolated the cause.

### 6. Make a clear choice and name the trade-off

Give the **recommended direction first** when evidence is sufficient. State:
- **Why this one** suits the moment's primary job.
- **Which preference/evidence** applies and what remains an inference.
- **What you give up**, a plausible failure mode, and a sensible mitigation.
- **Where another option would be stronger**.
- **Whether the choice is proposed, reviewed, tested, or approved**, with the actual authority supporting that status.

Choose an honest “conditional choice” only when the objective actually branches by context. If none of the proposed options is suitable, say so and give a better direction. Do not remain neutral just to avoid an artistic judgment.

### 7. Validate at the cheapest meaningful fidelity

Select **one** discriminating test if the uncertainty matters:
- Stills, paper comps or lightweight SVG sketches for layout/visual hierarchy.
- A timed animatic or playblast for rhythm, space, camera, and transient readability.
- A realistic task/user check for comprehension or UI behavior.
- A listening sample for audio phrasing, tone, or mix balance.
- A verified technical/data source review when factual meaning is at stake.

Write a **qualitative acceptance question**, not an arbitrary invented measurement. Test an isolated variable when trying to infer a preference; test the whole artifact when deciding real project suitability. A preview demonstrates only what was actually inspected; do not report production acceptance before it happens.

### 8. Record the decision without freezing taste

For a consequential decision, provide a compact [decision record](references/decision-record.md), including context, selected option, rationale, trade-offs, alternatives, evidence, conditions, open checks and status.

If feedback changes the choice, update the **decision for its named context**; preserve prior evidence. Hand broader taste discovery or profile updates back to `discover-creative-taste` when required; do not rewrite raw preference history yourself.

When asked for build instructions, hand your **chosen direction and acceptance criteria** to the appropriate production/implementation skill. Do not expand this skill into another camera, typography, engineering or execution specification.

## Response shapes

**Ordinary creative question:** 1–3 compact paragraphs stating the choice, rationale, key trade-off, and when another treatment wins. No mandatory tables or scores.

**Review of alternatives:** Short comparison with each option's best-use case, your recommendation, and the most useful next test if needed.

**Formal project handoff:** Use [decision-record.md](references/decision-record.md), filled only with supported facts. Distinguish an *art-direction proposal* from *client approval*.

Read [judgment-calibration.md](references/judgment-calibration.md) when comparing ambiguous options, testing exceptional decisions, or validating the proposed skill.

## Self-check before returning

- Did I judge the **actual moment's purpose**, not merely enforce a preferred look?
- Are verified constraints separate from artist taste and assistant inference?
- Did I recommend something, with a concrete reason and real downside?
- Did I give the losing choice a plausible context where it wins?
- Did I allow an evidence-backed exception or a justified creative departure?
- Did I avoid uninspected-artifact claims, fake scores, invented approvals, and unnecessary probing?
- Could another director apply this **method** without inheriting the original director's preferences?
