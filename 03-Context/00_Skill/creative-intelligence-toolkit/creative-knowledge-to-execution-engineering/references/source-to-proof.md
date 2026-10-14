# Source-to-Proof Traceability

Read this for a complex execution handoff, cross-agent continuation, revision audit, or review. It is a **method**, not a required new database/schema. Use existing project records wherever possible.

## Purpose of the trace

Make each required property traceable:

**source → claim/decision → instruction/invariant → artifact → inspected evidence → approval scope**

A broken link in that chain should be visible, not silently filled by the agent.

## Minimal trace row

| Field | Reason |
|---|---|
| Claim / decision ID | Stable referent; avoid duplicating the source |
| Source / owner | Which record or authorized person establishes it |
| Exact version | Relevant file/hash/date/revision, if actually known |
| Kind | Verified fact, binding requirement, accepted direction, hypothesis, or discretionary preference |
| Scope | Which specific scene/screen/release/variable it applies to |
| Dependent output | Which file, implementation or visual element realizes it |
| Check | An observable review, runtime trace, unit test, frame inspection or factual comparison |
| Evidence | Real result, screenshot, tool log or reviewer statement |
| Status | NOT_RUN, BLOCKED, FAIL, PASS_WITH_NONBLOCKING_ISSUES, PASS |
| Open issue | What is unresolved and who owns the decision |

**Important:** Do not mistake an artistic preference for a factual validation source. A gorgeous final image is not a geometry audit. Do not use `client_approved` without a recorded authorized reviewer and artifact revision.

## Dependency classification

Classify unknowns relative to **this slice**, not the whole project:

- **Blocking:** cannot responsibly execute the proposed step without resolution (e.g. source measurements required to publish a measured chart).
- **Non-blocking but disclosed:** does not prevent a bounded conceptual proof; must not escape as a final fact.
- **Assumption for testing:** provisional, reversible, explicitly framed, and never upgraded to approval through repetition.
- **Out of scope:** no dependency on this task; don't bring it into the agent's context unnecessarily.

When a blocked branch does not impede a smaller illustrative slice, propose that slice with its separate proof standard.

## Quality gates: a lightweight pattern

A high-value proof typically moves through:
- **G0 — Intake:** relevant source/decision authority and unknowns identified.
- **G1 — Small proof:** minimal editable or functional output produced; primary idea visible/testable.
- **G2 — Inspection:** real output inspected for creative meaning and technical/source constraints; deviations recorded.
- **G3 — Production/release:** only if scope, actual artifact version, needed reviewer approval and finishing/delivery checks exist.

These are **illustrative labels**; do not overwrite a project's existing named gates. An artifact can pass the concept proof while failing production readiness. Don't proclaim a global pass because an isolated unit test passed.

## Verification matrix by output type

| Output type | Actually useful proof | Insufficient proof by itself |
|---|---|---|
| SVG plan | SVG parses/renders, labels/path relationships inspectable, review of concept | Exact physical dimensions or animation timing |
| Image | Image inspected at delivery size, subject/claim compared to verified source | Camera continuity, functional interaction, verified data |
| Timed animatic or playblast | Continuous playback/frame checks for arrival, timing, orientation | Final-material acceptance, independently verified science |
| Generated video | Entire video viewed for subject/motion consistency and artifact changes | First and last keyframe similarity only |
| UI prototype | User action/test performed and state effects observed | Attractive screenshots or passing build only |
| Code/package | Relevant tests/build executed against stated revision, behavior observed | Commit existing or dependency compile only |
| Chart / infographic | Data/source, scale, labels and intended inference validated | A clean design or scientific-looking color palette |
| Documentation/spec | Links resolve, ownership and status consistent, instructions dry-run | Existence of Markdown file or claimed review |

## Status and closure example (fictional)

An agent receives a proposal for an interactive diagram. It creates an SVG source, validates that it parses, and shows a preview to a reviewer. The **SVG file** and **syntax** can be marked PASS for a named version, but the **user interaction** remains NOT_RUN because a static SVG cannot prove working controls. If source data is hypothetical, publishability remains BLOCKED until validated.

A downstream implementer should understand those distinctions without reading the original chat history.

## Change impact

For a new or revised creative decision, enumerate **only affected** downstream dependencies: script/text, source mappings, frames, composition, graphic annotations, code, tests, documentation and approvals. Preserve unrelated validated components and prior evidence. Re-run checks that could have been invalidated. Report the updated revision and still-unaffected evidence separately.

## Independent review

An agent may self-check its own output, but must call that **self-verification**, not independent audit. If an external review is requested, obtain a distinct reviewer/agent or flag that independence is pending. A synthetic scenario and a written test plan are not proof of executed verification.
