---
name: information-to-visual-storytelling
description: Translate factual explanations, abstract ideas, physical mechanisms, measurements, calculations, states, comparisons, and data into accurate, comprehensible, compelling visual narratives. Use when creating an explainer, technical animation, scientific visualization, infographic, data-driven video, educational graphic, diagram, product demonstration, or information overlay; when deciding what information to show, in what order, and whether to use annotation, charts, metaphor, typography, spatial graphics, or a hybrid. Keep source truth, provenance, uncertainty, and audience comprehension explicit without assuming a particular design style or software.
---

# Information-to-Visual Storytelling

Direct **how meaning becomes visible**. Start with what the audience must understand, trace the claim to its source, choose a truthful visual representation, and choreograph when information appears, connects, transforms, and resolves. Elegance comes from deliberate explanation—not from adding decorative data or motion.

## Responsibility and boundaries

- **Own:** conceptual decomposition, claim/source classification, information hierarchy, visual representation, explanation sequence, labeling/annotation purpose, meaningful graphic motion, quantitative integrity, illustrative storyboards, and comprehension checks.
- **Do not own:** discovering taste (`discover-creative-taste`), choosing a project's creative identity (`contextual-aesthetic-judgment`), detailed camera/lens/path direction (`spatial-storytelling-camera-choreography`), calculating or verifying source measurements, generating actual scientific results, or production pipeline contracts (future execution skill).
- **Never inherit** a specific brand's look, a named studio's motion language, domain-specific measurement assumptions, or the author's artistic preferences. Consume project/subject truth and taste as external inputs.
- **Preserve source ownership:** client/scientist/data authority determines whether a technical claim is correct and approved. This skill determines how to **explain the claim without changing it**.

## Start with what is available

Use the actual source text, data, drawings, images, concept, target audience, story purpose, context, and requested medium. If an essential variable, mechanism, source, or interpretation is missing, ask **one targeted question** or proceed with clearly labeled **concept-only** content. Do not fabricate a log, formula, simulation, scale, quantity, data trend, or client finding to fill a visual gap.

Clarify only details that change the meaning or feasibility. Otherwise choose a reversible presentation assumption and note it briefly.

## Procedure

### 1. Define the understanding change

Complete: **"The viewer begins knowing X and leaves understanding Y because they see Z."**

Make the **central claim or relationship** explicit. Identify who needs the explanation, its level of prior knowledge, and the viewer action or inference it should support. Distinguish **what happened**, **how it works**, **what was observed**, and **what can be concluded**; these are not interchangeable.

Split large concepts into the smallest meaningful **information beats**, each with one principal question, not necessarily one scene/shot. Ask whether each beat contributes something new or merely repeats a prior fact.

### 2. Create an evidence and meaning ledger

For every significant graphic, know **what it represents**:

| Information kind | Core question | Do not misrepresent as |
|---|---|---|
| Measured or observed | What was actually recorded, by whom, under what conditions? | A universal value or a simulated result |
| Derived or calculated | Which measured/assumed inputs and rule lead to this value? | Directly observed fact |
| Simulation/model output | Which model/run, assumptions, variable, scale and conditions produced this image? | Field measurement or verified physical result |
| State/event | What changed and what caused the change? | Operational reality when merely hypothetical |
| Comparison | What is the baseline, unit and like-for-like denominator? | A fair comparison when scales or populations differ |
| Hypothetical/illustrative | What simplified example demonstrates the principle? | Actual client data or calibrated geometry |
| Interpretation/conclusion | What can responsibly be inferred from the evidence? | A stronger claim than the source supports |

For quantities, retain units, coordinate reference, timeframe, baseline, precision, relevant uncertainty, legends and direction conventions **where meaningful**. Do not invent numeric values or color ranges. If the artifact is schematic, mark it **illustrative / not to scale** wherever confusion is plausible. Record sources and approval state explicitly.

### 3. Find the explanatory mechanism

Identify the smallest understandable causal or logical chain:

**origin → observed action/change → relation/operation → consequence → interpretation**.

Use only stages actually relevant to the subject. Decide which parts are **physical**, **temporal**, **spatial**, **comparative**, **statistical**, or **conceptual**. Surface the principle early when a viewer needs it to decode everything that follows; delay a reveal only when anticipation advances understanding.

Prefer an image or relationship that *demonstrates* the proposition over a label that merely repeats narration. Ask: **What becomes knowable at this exact visual change?**

### 4. Choose the representation for meaning, not decoration

Pick one or a minimal hybrid:

- **Physical/spatial depiction:** object, mechanism, cutaway, geometry or labeled location—useful when spatial cause and relations matter.
- **2D editorial presentation:** short text, callout, icon, timeline or value—useful for a simple statement and fast reading.
- **Diagram:** controlled simplification of a process, network, transformation or abstract relationship.
- **Plot/table/data space:** grounded values, distribution, trend or comparison—useful when quantities and structure matter.
- **World-anchored annotation:** highlight, marker or label attached to a verified surface or event—useful to connect data to source.
- **Metaphor:** clearly signaled analogy when literal representation is unavailable or burdensome; mark exactly where the analogy stops being physically true.
- **Hybrid:** e.g., physical event plus readable 2D graph; assign each layer a **different** information job.

**Do not force all information into a 3D HUD, an equation, or a cinematic spatial treatment.** Choose the simplest structure that preserves meaning and interest; richer dimensional treatment must contribute understanding, orientation or emotional consequence.

### 5. Choreograph information through time

An information beat may follow this lifecycle, not a mandatory seven-part animation:

1. **Motivate:** establish the question or phenomenon.
2. **Locate origin:** show who/what produces the data or idea.
3. **Introduce:** bring in one readable relationship at a time.
4. **Connect:** make the source-to-result mapping explicit.
5. **Emphasize:** isolate the consequential value, difference or event.
6. **Recognize:** allow the audience enough visual time to parse the message.
7. **Resolve:** persist, transform, compare or remove the graphic without breaking logic.

Avoid animating chart shapes merely for spectacle. Any morph, interpolation, accumulating sample, unwrapping, or 2D↔3D transition must preserve **which quantity, object or reference frame it represents**. If correspondence is unknown, use a cut/side-by-side rather than implying a false transformation.

Plan the **entrance, coexistence, movement and exit** of information relative to the underlying action. Decide what may be omitted so attention stays on the explanation.

### 6. Protect quantitative and semantic integrity

Before producing a candidate graphic, check:
- Do dimensions, axes, origins, baselines, legends, unit symbols and ranges mean what the source says?
- Are categorical, sequential and diverging colors used as distinguishable **encodings**, not misleading decoration? Don't invent a color convention or imply a severity ranking without evidence.
- Are relative size, area, angle and duration truthful? Do not scale a difference for drama without labeling the exaggeration.
- Does an annotation point to the correct location, event, state or data series?
- Does an animated transition imply a physical process or mathematical equivalence that the source **does not** establish?
- Can the primary inference be read without relying on color alone? Consider contrast, captions, reading order and delivery size.
- Are uncertainty and limitations shown at a level appropriate to the audience and stakes?

For regulated, safety-related, engineering, clinical or consequential decisions, require relevant domain review before presenting the graphic as a verified result. A visually polished chart can still be false.

### 7. Produce a cheap, truthful visual study

Make the **lowest-cost artifact that tests the explanation**:
- **Sentence + mapping sketch:** clarify the claim and its visual counterpart.
- **SVG-first information board:** draw source, relationship and conclusion in editable, labeled frames; use the neutral [concept storyboard SVG](assets/information-beat-template.svg) as *scaffolding*, not a fixed layout.
- **Two treatments:** compare minimal editorial versus physically/spatially integrated or data-stage options **with the same factual message** when the form is uncertain.
- **Timed animatic:** test temporal readability, accumulation, chart transformations and information handoffs.
- **Actual data visualization:** only after receiving valid source data, units, mapping rules and any necessary approval.

Label unknowns and hypotheses. **Never depict illustrative values or synthetic waveforms as source measurements**. State the test type (conceptual, controlled comparison, data-verified, or production-reviewed).

### 8. Evaluate comprehension and hand off

Review with the question: **Can the intended viewer now infer the right thing, for the right reason?**

Look for mistaken causality, missing references, overloaded frames, decorative annotation, unreadable intervals, distorted comparison and unmarked conceptual imagery. Prefer pruning or re-sequencing to adding explanation layers.

When a persistent brief is needed, use the [information-beat contract](references/information-beat-contract.md). For worked failure modes and scenario tests, read [calibration cases](references/meaning-preservation-tests.md).

Pass chosen information beats, source dependencies, labels and validation questions to the camera/directing and implementation workflows. **Do not invent a competing project scene contract**: map these fields into the existing handoff when one exists. Request authorized review where claims need it.

## Interaction and handoff

- A focused concept request should yield **one strong explanation with its visual beat sequence**, not a sprawling storyboard unless requested.
- Always distinguish **source fact**, **proposed depiction**, **viewer inference**, and **unverified detail**.
- Treat an aesthetically strong graphic as an explanation hypothesis until comprehension and factual checks occur.
- Respect an existing narrative, client corrections and data provenance. A reference frame is not automatically verified technical truth.
- Preserve accessibility and readability in the final medium. A graphic should work at the intended playback size and speed.
- If a simple static label is sufficient, use it. Graphic motion is meaningful only when it reveals a relationship or improves understanding.

## Completion check

1. Is the audience takeaway a **specific correct inference**, rather than "looks advanced"?
2. Can every consequential visual mark trace back to a fact, model, example, or declared abstraction?
3. Is measured vs derived vs simulated vs illustrative identity never blurred?
4. Does visual change correspond to a genuine logical or causal step?
5. Are units, references, baselines and uncertainty respected when applicable?
6. Is the information readable, appropriately sequenced and not overloaded?
7. Could another creative team apply the **method** without importing a particular client’s data or style?
8. Is the next approval/test clear without implying it already happened?
