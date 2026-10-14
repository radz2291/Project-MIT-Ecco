# Evidence and Profile Model

Use this when the user wants an enduring creative profile, an evidence register, or machine-readable transfer to another agent. This is an **output schema**, not an instruction to save automatically. Use only fields supported by the actual conversation or inspected references.

## 1. Evidence entry

| Field | Meaning |
|---|---|
| `id` | Stable, incrementing identifier local to this profile |
| `recorded_at` | Date/time known from conversation or `unknown` |
| `subject` | Person whose taste is being discovered |
| `domain` | Film, type, UX, music, etc. |
| `reference` | Exact work, artist, shot/timecode or controlled variant; link if verified |
| `input_type` | Initial impression, detailed reaction, selection, correction, project review |
| `verbatim_feedback` | The person's exact words when available; otherwise explicitly marked paraphrase |
| `polarity` | Positive / negative / mixed / tentative |
| `direct_observation` | What the person confirmed without interpretation |
| `inferred_traits` | Proposed aesthetic concepts, each labeled as a hypothesis |
| `context` | Personal attraction / project suitability / concrete deliverable |
| `scope` | This frame/work/test, this application, or broader pattern supported by multiple tests |
| `uncertainty` | Missing evidence, multiple variables, uninspected work, or untested execution |
| `relation` | New / qualifies E### / supersedes E### / conflicts E### / confirms E### |
| `status` | Reaction confirmed / inference pending / tested in production / client-approved (only if documented) |
| `next_probe` | One small comparison or observation that would most reduce uncertainty |

Use plain-language statuses rather than invented numerical scores. If a timestamp, image or source has not been inspected, write `not inspected`. **Approval** requires an actual approver and reviewed version.

## 2. Working preference card

```yaml
id: P01
title: "Meaningful spatial presence"
scope: "Product hero compositions; provisional"
preference: "Objects can feel monumental through composition and depth"
evidence: ["E001", "E004"]
why_it_may_work: "agent interpretation: changes scale perception without exaggerating geometry"
favorable_contexts:
  - "Emotive product introduction"
alternatives_or_exceptions:
  - "Use neutral orthographic views for dimensional comparison"
not_yet_supported:
  - "Preferred lens length"
  - "Specific lighting rig"
confidence_basis: "Direct detailed feedback for one work; no repeated project test"
lifecycle: "working hypothesis"
```

This is an **illustrative, invented card**, not a claimed real person's preference.

## 3. Profile summary

Keep this short and useful:
- **Purpose and scope:** Whose preferences, for which domain; personal versus project-suitable.
- **Strongest evidenced signals:** typically three to seven taste cards, linked to evidence IDs.
- **Conditional variants:** when apparent contradictions reflect context (e.g., spatial treatment for immersive sequence, flat treatment for quick facts).
- **Negative reactions:** exactly which work/feature was rejected; no universal prohibitions inferred.
- **Undiscovered traits:** untested type, sound, motion, layout, materials, etc.
- **Change history:** newest corrections and which earlier choices they supersede.
- **Next test:** one actionable comparison, not a large open-ended questionnaire.

## 4. Persistence safety

1. Locate the project's existing evidence and profile sources, if any.
2. Preserve the original raw statement and older evidence; append a revision rather than falsifying earlier history.
3. Update the *interpretation* separately from *evidence*; refer by evidence IDs.
4. Keep the agnostic skill source free of a particular person's brand, style, or technical facts.
5. Confirm successful tool writes before reporting a persisted update.
