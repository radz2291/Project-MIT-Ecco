---
name: creative-knowledge-to-execution-engineering
description: Turn creative research, taste evidence, approved direction, storyboards, information beats, and project constraints into actionable, traceable, testable instructions for AI or human production agents. Use when preparing a Codex/agent task, production handoff, reproducible design/build specification, smallest executable proof, source-of-truth map, acceptance criteria, verification plan, or change-impact review; or when an agent must execute without confusing proposals, facts, and approvals. Works across design, film, UI, content, software, and production tools.
---

# Creative Knowledge-to-Execution Engineering

Bridge **intent → evidence → bounded execution → inspected proof**. Protect the intelligence behind creative decisions while making instructions specific enough to act on and outcomes possible to verify.

A handoff is not good because it is long or machine-readable. It is good when a new agent can **find authoritative inputs, understand the intended experience, decide within known boundaries, produce a reviewable result, and report exactly what happened**.

## Role and limits

- **Own:** source routing, contract reconciliation, scope slicing, task packaging, controlled agent discretion, dependency/blocker classification, acceptance criteria, verification evidence, change impact, and closure status.
- **Do not own:** discovering artistic taste (`discover-creative-taste`), choosing among creative directions (`contextual-aesthetic-judgment`), inventing camera movement (`spatial-storytelling-camera-choreography`), explaining factual/data meaning (`information-to-visual-storytelling`), or implementing a toolchain merely to demonstrate this skill. Delegate or link to the appropriate owners.
- **Not an orchestrator by default.** A single agent and a single task may be enough. Do not impose multi-agent roles, elaborate approvals, YAML, or additional infrastructure unless the work requires them.
- **Not a new authority layer.** If a project already has a scene contract, design specification, source registry, task template, or verification gates, **map into those** rather than inventing parallel records.
- **No embedded taste or client rules.** Read project-specific sources at use time; never copy them into this reusable skill.

## Inputs and prerequisites

Use the context already given. Identify, as available: desired outcome, intended audience/user experience, project/repository, source assets, accepted decisions, currently unresolved facts, execution environment, deliverable, and review owner.

**Choose mode before work:**
- **Investigate:** read sources, reconcile readiness, and recommend the next safe slice; do not modify files or implement.
- **Prepare:** produce a traceable task/handoff; do not claim it has been run.
- **Execute:** modify/create only what is authorized, inspect results, and report artifacts and checks.
- **Review:** independently compare an existing artifact against its claim, contract, and evidence; do not conflate a documented test with a passing test.

If the mode is unclear, take the least destructive useful step. Don't require a full planning questionnaire. Ask **one** focused clarification only if the missing fact changes scope, safety, authority, or the user's requested action.

## Eight-stage workflow

### 1. Identify the delivery boundary

Define one **reviewable outcome** and the smallest useful execution slice. State what is **in scope** and **out of scope**. Distinguish a conceptual proof, functional mockup, prototype, production artifact, and final approved deliverable.

Choose a slice that exercises the **hardest important uncertainty** early, not merely the easiest cosmetic element. Prefer lightweight source-editable evidence (notes, SVG plans, quick renders, tests, small functional demos) over expensive finishing before the principle is verified.

A safe exploration slice may continue with explicitly illustrative placeholders; do not let an unrelated unresolved detail block all progress. A blocking factual/approval dependency must prevent **only the operation that needs it**.

### 2. Route sources by authority and freshness

Build a short **source map** from actual files/URLs/records. Read the smallest relevant set, preferably via an existing repository/context index.

| Authority kind | Governs | Never silently replaced by |
|---|---|---|
| Verified facts / data / constraints | What may truthfully be claimed, displayed, or built | Beautiful references, agent guesses, a storyboard |
| Contractual / client / accessibility rules | Binding scope, copy, legal or delivery constraints | Personal taste or execution convenience |
| Accepted purpose / narrative | What audience/user must experience | Generic visual polish |
| Taste evidence + contextual judgment | How the experience should feel, and situational exceptions | Rigid style presets or fabricated preferences |
| Shot / design / information decisions | Approved or explicitly experimental creative intent | Implementation tools choosing design by accident |
| Production environment / implementation records | Actual assets, paths, versions, transforms and tool behavior | Conceptual diagrams or invented coordinates |

For every reference state its **path or identifier, version/hash if available, authority scope, approval status, and unresolved conflict**. Do not invent links or imply all documents are current because they are committed. When two sources disagree, record the conflict and identify the actual decision owner; do not average them.

### 3. Extract the non-negotiable invariants

Identify properties that must remain true after implementation: factual assertions, subject identity, key geometry, source data and units, causal mechanisms, accessibility, essential wording, story outcome, asset integrity, or compatibility constraints.

Distinguish:
- **Hard constraint:** verified and binding; deviation requires authorization.
- **Accepted direction:** a scoped, human-approved choice; change requires an explicit revision.
- **Working hypothesis:** reasonable for testing, not yet endorsed.
- **Execution discretion:** implementation details the agent may choose within boundaries.
- **Unknown:** unresolved input or source requiring verification.

When conveying an aesthetic intention, specify **what should be perceived** and an inspectable example or reference. Avoid inventing numerical lens choices, font specifications, color values, simulation outputs or other false precision.

### 4. Allocate artistic and technical discretion

Give agents room to solve problems intelligently:
- **Fixed:** accepted wording, verified geometry/data, actual product behaviors, explicit design decisions, output/compatibility requirements.
- **Agent-directed:** alternative implementation, blocking arrangement, composition refinements, temporary scaffolds, test method, or code structure **where not fixed**.
- **Must escalate:** contradictory authorities, changing an accepted aesthetic decision, adding unverified physical/quantitative claims, sensitive asset release, irreversible/destructive operations, or costly scope expansion.

The agent may challenge a weak direction by offering a **reasoned alternative**, but may not secretly replace the accepted one. Record alternative options separately from the currently authorized task.

### 5. Compile one self-contained execution slice

Write a concise instruction using the [execution-slice template](assets/execution-slice.template.md). Include only the sections necessary for this task:
1. **Outcome / purpose:** what the result should communicate or accomplish.
2. **Input links and authority:** verified source paths, revisions and relevant evidence; clearly label missing/uninspected sources.
3. **Preserve:** invariants and explicit prohibitions tied to a reason.
4. **Do:** ordered minimal actions, implementation latitude and any tools that are truly available.
5. **Deliver:** inspectable artifact(s), expected location/format and ownership.
6. **Prove:** observable acceptance conditions, cheap test method, evidence to return.
7. **Stop / ask:** blockers, unsafe operations and escalation owner.

Use **an existing task/scene schema first**. For a cross-project example of source traceability and proof, read [source-to-proof reference](references/source-to-proof.md). Do not create redundant status registries.

An instruction is executable only if the assigned agent actually has the required files/tools/permissions. Never presume that a chat agent can access a local disk, connected GitHub, video renderer, browser, or credentials without checking.

### 6. Execute through inspectable milestones

When execution is authorized, make the smallest reversible change that yields learning:
- Read/inspect the actual baseline and environment before editing.
- Produce source-editable previews and a minimal working proof where appropriate.
- Verify at the resolution that matters: a static image cannot prove timing; a generated first/last frame cannot prove intermediate motion; a passing build cannot prove UX; a visually convincing chart cannot prove source data.
- Compare actual output to **both creative intent and binding constraints**. Flag where one passed but the other did not.

A tool response proves only the operation it reports. Creating a file is **not** validating its contents; committing to GitHub is **not** client approval; generating an image is **not** product-fidelity verification.

### 7. Return a falsifiable evidence report

Report:
- **Produced:** exact artifact/path/version/commit and what it contains.
- **Inspected:** precisely which files, frames, screens, logs, or data source were actually reviewed.
- **Passed:** specific acceptance conditions with observed evidence.
- **Failed / unknown:** deviations, missing inputs, untested conditions, approval gaps.
- **Next action:** a single high-value step or decision owner, with handoff for continuing work.

Choose honest statuses: `NOT_RUN`, `BLOCKED`, `FAIL`, `PASS_WITH_NONBLOCKING_ISSUES`, or `PASS`. A status applies to **the named test and artifact revision only**, not the entire project. Do not claim an independent audit if the same agent authored and evaluated the work.

If reviewer approval is required, record **who**, **what version**, and **what exact scope** was approved. Silence is not acceptance.

### 8. Carry forward changes without losing provenance

When instructions, preferences, client feedback or source assets change:
1. Capture the new input **without deleting previous evidence**.
2. Identify affected deliverables, contracts, diagrams, labels, tests and downstream dependencies.
3. Mark the prior choice as `superseded`, `qualified`, `conflicted`, or `still valid for another context` as appropriate.
4. Change only impacted work; preserve unrelated valid decisions.
5. Revalidate the affected acceptance conditions and actual artifact versions.
6. Update the existing canonical documents and index paths **only if authorized**.

Do not silently convert a draft to an accepted design, a preview to finished production, or an agent's interpretation to the user's own words.

## Output modes and evidence discipline

- **Quick handoff:** one short task paragraph with sources, invariants, deliverable and test.
- **Focused implementation slice:** use the [execution-slice template](assets/execution-slice.template.md); keep it as small as the real work permits.
- **Complex multi-step job:** use [source-to-proof](references/source-to-proof.md) for dependency and artifact traceability, and [calibration scenarios](references/calibration-scenarios.md) to check tricky handoffs.
- **Review-only request:** provide a findings/evidence report without modifying sources.
- **No external tools available:** provide an executable instruction *for the operator* or explain what cannot be verified. Never assert a file or commit was created when it was not.

**Minimum closure test:** Can another agent continue from the records without reconstructing the whole conversation? Can a reviewer tell what was proven versus merely proposed? Could a correct result still emerge if the next agent has different artistic taste or works in a different tool?

The answer should be **yes** before calling an execution slice ready.
