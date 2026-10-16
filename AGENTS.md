# Agent Entry Point — MIT / ECCO

**First read:** [03-Context/README.md](03-Context/README.md). It owns the canonical source map, precedence and task-specific reading routes. Do not load the entire repository context indiscriminately.

## Execute through Rolladice Work

Rolladice Work / **MIT ECCO** is the core task, dependency, execution and review system. Repository sources remain authoritative for engineering, creative direction and implementation. Read the live ticket and fresh handoff before execution; obey dependency and pinned-standard checks. A direct instruction from Radzi to execute a ticket authorizes that bounded work while the wider roadmap may remain provisional.

Follow [04-Production/README.md](04-Production/README.md) for the run lifecycle (`run_start`, stable worker, periodic `run_update`, evidence, Review), outage recovery and human/agent responsibilities. Do not self-accept reviewed work or bypass prerequisites. Preparing a handoff does not launch Codex.

**Work and save under `04-Production/`.** Reusable assets belong in `Shared/Assets/`; mechanism proofs, shot scenes, scripts, previews and records each have defined destinations. Before ending a run, organize all retained task outputs, verify links and saved files, update records and attach exact output references to Rolladice. No task is complete with deliverables left only in scratch/temp/chat or scattered outside the project. Heavy/ignored files stay organized locally; local saving does not imply Git publication or backup.

**Commit and push before Review (owner-authorized, 16 October 2026).** Synchronize the task's reviewable reports, scripts, configuration, evidence and selected permitted review images to this repository's authorized branch. Inspect and stage only intended task files, preserve unrelated work, make a scoped commit and push normally. Verify the candidate commit is present on the remote; attach its SHA/commit link and report link to Rolladice. A local commit alone is not synchronized. In parallel work, one designated integrator performs Git mutations and pushes the agreed task commits; workers provide exact file lists and wait for confirmed synchronization. Never force-push, stage others' changes blindly, bypass branch protection or force-add excluded/private media. If no destination is established or sync fails, record the exact blocker and preserve local work; do not claim ready for Review. See the production closure rules for details.

Mechanical correctness and a complete moving animatic precede final finishing; use the mechanical-first sequence in the workflow. Inspect the actual checkout and preserve unrelated user changes. Do not assume this cloud session can access Radzi's Windows production files.

## Choose the task

- **Fact, technical claim or open approval:** [Engineering Baseline](03-Context/01_Foundation/02-ENGINEERING_BASELINE.md) → [Decision Register](03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md) → original source.
- **New camera/scene/lighting design:** relevant [V2 storyboard](03-Context/02_Storyboard/README.md) → [MIT identity](03-Context/01_Foundation/03-MIT_PRODUCTION_IDENTITY.md) → [scene-director skill](03-Context/00_Skill/rolladice-scene-director/SKILL.md).
- **Construct, finish or QC:** [Production Workflow](03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md), with the actual shot's [Scene Direction Contract](03-Context/03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md).
- **Existing Blender animation → generative reference:** [blender-animation-reference skill](03-Context/00_Skill/blender-animation-reference/SKILL.md).

**Mechanical storyboard use:** extract mechanisms, required information beats and client corrections; do not reproduce its schematic panels as the film design. Translate the content through Directorial Identity into on-model cinematic scenes. Storyboard graphics are neither engineering proof nor a locked composition/camera plan.

**B2 paired workflow (16 October 2026):** Blender mechanism tickets provide grounded baseline stills, scene constraints, implementation and verification. T26 is the ongoing visual-direction partner working with Radzi on those actual frames; generated references are optional. Use current frame → concrete question → Radzi decision → bounded Blender change. T26 completion is not an execution prerequisite. Gate specific treatments/motion scope, not all B2. Preserve T7's completed still work and authorized progress; do not restart it. See [B2 paired workflow](04-Production/B2-VISUAL_APPROVAL.md).

## Directorial context and replaceable hardware

For every S01–S07 blocking task, explicitly apply the [rolladice-scene-director skill](03-Context/00_Skill/rolladice-scene-director/SKILL.md) with the relevant [Directorial Identity](03-Context/03_Directorial_Identity/README.md) modules **before scene construction**. Save one Scene Direction Contract per actual shot in its shot folder; inspect the moving preview against that contract. Camera, composition, pacing and information choreography belong in blocking, not only finishing. The legacy AI Director Interpretation Guide is superseded; read the active index. B1 foundation work does not need cinematic shot design. **B2 pairs grounded Blender work in T7–T11 with T26 visual direction**, using the Scene Director skill and relevant Directorial Identity modules as decisions arise. Follow [B2 visual approval expectations](04-Production/B2-VISUAL_APPROVAL.md); detached schematic proofs alone are insufficient. B3 develops camera choreography and shot transitions from those reusable scenes.

**Production baseline, owner decision 16 October 2026:** use accepted T5 plugged ECCO v002 and T6 well/assembly v003 for continued production; the current plugged product may appear in final delivery. Do not wait for the incoming plugged model or a complete client BHA package. If a replacement arrives, inspect actual differences and reverify affected outputs. Keep shared geometry replaceable. Surrounding BHA/bit/adapters use sourced, simplified references; refine visible details during B3 to the shot's needs. O05/O14 are not blanket development holds; raise only unresolved facts material to the explanation or visible hardware claims. Producer acceptance is not MIT engineering certification. See the decision register and production workspace for scope.

## Non-negotiable boundaries

Do not confuse storyboard drafts, artistic hypotheses or local examples with client approvals or engineering truth. Do not invent product geometry, physical simulation, actual camera transforms or evidence of a successful render. **Typography has an initial evidenced preference profile** ([module 08](03-Context/03_Directorial_Identity/08-TYPOGRAPHY_AND_GRAPHIC_INTEGRATION_v0.3.md)): quiet elegant sans-serif editorial; meaningful wording/composition; gentle fades or motion; screen-space or spatial as appropriate. Technical motion-graphics details remain largely untested. Retain client-required information without inventing a finished design system.

**Publication caution:** The public repository contains a sample ENP1 field-log illustration with rights/permissions unresolved; do not republish or export it until the producer confirms permission in the decision register.
