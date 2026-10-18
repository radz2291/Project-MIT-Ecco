# Agent Entry Point — MIT / ECCO

## Current owner-authorized cycle — 18 October 2026

Read [Production workspace](04-Production/README.md) for the current cycle, lifecycle and closure rules. This cycle supersedes older mechanical-first, B2 pairing, separate still/animation and editable 3D storyboard gates.

- Active Rolladice Work project: **MIT ECCO**, ID `a0b9b971-e282-42f0-a25f-0c78729eff87`. Previous-cycle and PREVIS projects are archived history; do not execute their unfinished tickets.
- T31 is complete. Visual source: **ECCO - Cinematic Film Storyboard**, board ID `8466dd02-7299-4e68-85fc-f95d0d61931e`, V3 / 22 shots / seven sequences / 90 seconds. Read its start guide and relevant shot cards. [Board/source handoff](04-Production/Records/Storyboard-Board-V3/README.md); [V3 sources](03-Context/02_Storyboard/V3/).
- Cycle: shared-component plan → shared asset builds and separate AI-director instructions → actual movie shots with fast renders → **Radzi alone assembles the film** and obtains client feedback → scoped corrections → delivery.
- The orchestrator/planning agent supplies visual-instruction placeholders. A separate AI directing agent owns treatments and execution briefs using the [Scene Director skill](03-Context/00_Skill/rolladice-scene-director/SKILL.md) and [Directorial Identity](03-Context/03_Directorial_Identity/README.md). Blender executes the approved briefs; consequential visual ambiguities return to the director.
- Shot renders must be **strictly less than 5 seconds per frame** on the executing machine. Benchmark representative/heaviest frames at working settings before batch rendering, record timings/settings, and reduce cost if needed. Do not silently raise this cap. No expensive rendering now.
- Shots reference canonical shared masters with stable controls and documented versions. Record consumers; shared revisions require affected-shot checks/rerenders. Preserve supplied originals and useful completed work.
- Read live Work for current tickets and releases. Planning proposes downstream work; only owner-authorized tickets are created or executed. A directing ticket may release approved components/shot briefs progressively without finishing every brief first.

## Execution and source authority

Read the live ticket and fresh handoff before execution; verify dependencies and current pinned standards. Radzi's instruction to execute a specific ticket authorizes that bounded work. Follow the production run lifecycle; only Radzi accepts reviewed results.

[03-Context/README.md](03-Context/README.md) maps subject sources. Engineering/client constraints remain authoritative; old workflow paragraphs do not override the current owner cycle. Mechanical boards provide engineering information and client corrections, never the film camera plan. Generated concepts guide appearance, not dimensions or evidence of physical simulation.

Use [Engineering Baseline](03-Context/01_Foundation/02-ENGINEERING_BASELINE.md) and [Decision Register](03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md) for facts and consequential open questions. Current T5 plugged ECCO v002 and T6 well/assembly v003 are reuse candidates; inspect actual assets and preserve their stated limits. Incoming plugged geometry is not a blanket blocker. Do not invent exact BHA interfaces or technical approval.

## Save, verify and synchronize

Work under `04-Production/`; reusable masters belong in `Shared/Assets/`, actual shots use V3 IDs under `Shots/<section>/<shot-id>/`. Keep one [Scene Direction Contract](03-Context/03_Directorial_Identity/07-SCENE_DIRECTION_CONTRACT_v0.2.md) per shot, supplied by the directing agent and completed with actual implementation facts by the executor.

Organize retained files, verify saved candidates and relative links, and save a concise task report under `Records/Tasks/T-<number>/`. Commit/push permitted task-owned reports, scripts, configuration, evidence and selected stills; verify remote commit and attach pinned links before Review. Preserve unrelated Git changes; no force-push or force-adding excluded media. Shared checkouts use one Git integrator. Record sync failures truthfully.

Heavy Blender/video/cache files remain organized locally with exact paths and backup status. No claim of remote media access, engineering certification, client acceptance or successful render without evidence. Restricted field-log imagery requires recorded permission before reuse/publication. Radzi owns client communication and film assembly.
