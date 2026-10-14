# Contextual Creative Decision Record

Load this reference when a consequential creative choice needs a portable written record or handoff. For quick conversation, use a concise verbal recommendation; do not force a formal file.

**One decision record = one creative decision for one context.** This is not a storyboard, production timeline, taste-evidence register, engineering verification sheet, or client approval contract.

## Compact record template

```yaml
decision_id: D001
status: proposed              # proposed | preview_reviewed | direction_accepted | client_approved
decision_unit: "one explanatory moment"
primary_purpose: "help the viewer understand a single relationship"
audience: "specific audience or unknown"
medium: "medium / device / delivery conditions if known"
hard_boundaries:
  - "specific verified constraint or note unresolved"
taste_inputs:
  - reference_or_evidence_id: "Pxx/Eyy, when actually supplied"
    evidence_scope: "what was liked, where, and how directly"
    applicability: "direct | transfer_hypothesis | unknown"
candidates:
  - label: "A"
    treatment: "short distinct description"
    contribution: "what it improves"
    sacrifice: "what it weakens or risks"
    best_fit: "when this option becomes stronger"
  - label: "B"
    treatment: "short distinct description"
    contribution: "..."
    sacrifice: "..."
    best_fit: "..."
selected: "B"
reason: "why B fits the primary purpose here"
tradeoff: "the real cost of B"
mitigation: "how to reduce that cost"
alternative_when: "condition under which A wins"
unverified_assumptions:
  - "a claim requiring validation or real source inspection"
validation:
  cheapest_test: "one targeted mockup or task"
  qualitative_question: "what exactly should be legible/evocative after review?"
  result: not_run
change_relation: "new | qualifies Dxxx | supersedes Dxxx | scoped_split with Dxxx"
next_owner: "who reviews/executes this decision; not assumed"
```

Remove unsupported or irrelevant fields for a small decision. Use source paths/links only when verified. If using a plain-text note, preserve the same logic.

## Short conversational format

**Choice:** [recommended option for this precise moment].  
**Reason:** [primary communicative/narrative advantage] using [supported taste/constraint] where relevant.  
**Trade-off:** [specific weakness] and how to mitigate it.  
**Alternative wins when:** [one contextual exception].  
**Status / check:** [proposal or actually-reviewed choice; one necessary test or approval].

## Authority labels

- **Proposed:** a reasoned art-direction judgment; no claim of user/client approval.
- **Preview reviewed:** a real preview was inspected; say by whom when known, and exactly which version.
- **Direction accepted:** the director explicitly selected a treatment **for the given decision unit**.
- **Client approved:** an authorized reviewer accepted the actual deliverable/version. Never infer this from the director's taste or a polished mockup.

## Versioning changes

When the user changes their choice, preserve the original record and mark its **scope**. Newer feedback supersedes only the exact decision context it names. If two treatments are good for different circumstances, record a **scoped split** instead of treating one as globally rejected.

For discovering/storing a person's long-term preferences (rather than a decision), use the separate taste-discovery skill. For machine-level build plans or actual production authority, hand this decision to the relevant implementation workflow.

## Sample record (fictional)

A fictional exhibit needs a large 3D diagram to teach the relation of two objects. A minimal static annotation was previously preferred elsewhere. Choose a spatial diagram **for the exhibit** because the audience needs to understand proximity; preserve a clean on-screen caption for numeric facts. The prior preference for minimal annotations remains valid for a simple standalone measurement. **This is a constructed example**, not an endorsement or project specification.
