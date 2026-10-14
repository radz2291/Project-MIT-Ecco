# Information Beat — Source-to-Meaning Contract

Use this reference when the information story needs a reproducible record. This is an **agnostic outline**, not a duplicate of a client's approved storyboard, data model or scene specification. Map relevant fields into the project's existing contract.

An **information beat** is the smallest coherent change in what the audience understands. One beat may be a sentence, a mark, a sequence of frames, or one section of a visualization. It does not automatically equal one camera shot.

## Compact proposed record

```yaml
schema: information-beat/v0.1
status: conceptual_proposal # verified_values / source_reviewed / client_approved only with evidence
id: BEAT-01
viewer:
  audience: "who needs the explanation; may be unknown"
  before: "their starting assumption/question"
  after: "one specific understanding or supported inference"
  cognitive_task: "recognize | compare | infer | locate | trace | decide"
source_and_claim:
  claim: "statement to be explained, not embellished"
  source_kind: "observed | derived | simulation | state | comparison | illustrative | interpretation"
  source_ref: "file, document, dataset/version, expert statement, or NOT_YET_AVAILABLE"
  verification: "pending; specify responsible owner if known"
  quantitative_context:
    unit: "if applicable; else not_applicable"
    baseline: "if applicable"
    scale: "real | schematic | not_to_scale | to_verify"
    precision_or_uncertainty: "if relevant"
  assumptions_and_limits:
    - "what the source does not establish"
semantic_mapping:
  origin: "where information arises"
  visual_mark: "what should appear on screen"
  represents: "real-world meaning of the mark"
  correspondence: "how the viewer connects mark to its source"
  inference: "what the viewer is permitted to conclude"
  non_implications:
    - "what the visual must NOT suggest"
representation:
  candidate: "physical | editorial | diagram | plot | anchored | analogy | hybrid"
  rationale: "why this helps THIS cognitive task"
  anchoring: "world | screen | separate data stage | not_applicable"
  labels: ["literal approved text OR proposed placeholder"]
  reading_order: "what is revealed first / next / last"
temporal_lifecycle:
  motivation: "which question prompts this beat"
  reveal: "first appearance"
  connect: "mapping becomes legible"
  emphasis: "what matters"
  resolution: "persist | transform | clear | cut"
  readability_check: "qualitative question to test at target size/speed"
handoff:
  unresolved_source_questions: ["questions for authorized owner"]
  artifact: "sketch | SVG | animatic | actual data graphic | pending"
  review_status: "not_run"
  next_test: "one cheapest meaningful comprehension / factual check"
```

Delete irrelevant fields for short work. Do not fill unknowns with fabricated data. A `source_ref` need not be online: a named, versioned client file or expert review can be authoritative within its appropriate scope.

## Five critical integrity checks

1. **Identity:** Is the mark tied to the correct source kind? Measured, calculated, simulation, hypothetical, and interpretation are distinguishable.
2. **Mapping:** Does the visual change track the real variable/event, not decorative animation?
3. **Comparison:** Same baseline, units, category boundaries, time window and graphic scale where fairness depends on them.
4. **Inference:** Does the conclusion claim only what the source establishes? Correlation does not by itself establish causation.
5. **Presentation:** Can the viewer distinguish the principal message from support details at actual playback size and duration?

## Short handoff form

When a structured record would be excessive, deliver:

- **Audience takeaway:** one sentence.
- **Source/authority:** known facts, source identity, unverified placeholders.
- **Visual path:** three or fewer meaningful information steps, with a representation choice.
- **Integrity boundary:** one misleading implication to avoid.
- **Validation:** one concrete comprehension or domain review question.

## Story progression, not decorative animation

For an illustrative process, a sensible conceptual order may be:

1. Show the event or phenomenon.
2. Make the observation traceable to that event.
3. Reveal the relationship to the result.
4. Hold the resulting inference only as long as it is readable.

This is **one possible narrative**, not a universal four-step template; a comparison or a conclusion-led editorial may need a different order.

## Version and evidence handling

Store the **source truth** in its authoritative location; a visual beat can cite that source but cannot replace it. When review changes a claim, revisit dependent labels, encodings, imagery and motion. An aesthetic approval does not authorize the underlying science or data.

If the user has not requested document persistence, keep the beat in the answer. If persistence is requested, verify the destination and existing schema, then update only the relevant source of interpretation.
