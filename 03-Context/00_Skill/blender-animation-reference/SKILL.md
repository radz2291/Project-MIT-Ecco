---
name: blender-animation-reference
description: Turn existing Blender animation into texture-free motion-reference videos, matching boundary stills, explicit scene descriptions, and timed prompts ready for a generative video model. Use for Blender-to-video motion transfer, segmented generation references, or revising unclear movement and endpoints. Does not submit to a video generator or guarantee exact generated reproduction.
---

# Blender Animation Reference

Produce a generator-ready package grounded in evaluated Blender animation. The reference supplies visible evidence; the scene explanation supplies spatial meaning; timed blocks specify progression; a separate appearance instruction supplies finishing. Preserve the user's animation and configurable output style.

## Read relevant guidance

- Connection, extraction, timing, rendering: [Blender workflow](references/blender-workflow.md).
- Before writing prompts: [Scene and motion translation](references/prompt-writing.md).
- Before delivery or generated-result diagnosis: [Quality and revisions](references/quality-and-revisions.md).
- For observed successes and limitations: [Session evidence](references/session-evidence.md). Observations are not universal model rules.
- For a concrete measured-to-prompt translation: [Worked subsea example](references/worked-example.md).
- Start configurations from [the export example](assets/export-config.example.json). Replace sample paths, ranges, roles and generator settings with the actual job. It is not an instruction to render its example range.

## Defaults and boundaries

Infer the source scene/camera, range, duration/FPS/aspect, style and supported generator inputs from the request and scene. Ask only when missing information materially affects the result. Otherwise retain source timing/aspect; use a practical 720p reference and source FPS. Finishing is configurable, not necessarily hyper-realism.

Reference default: texture-free Workbench studio shading, restrained neutral greys, stable depth shading, no decorative particles/atmosphere/reflections or overlays. Preserve meaningful simulated/deformed action; do not erase an essential animated subject because it resembles an effect.

Default to a **faithful reference**: preserve camera translation, rotation, roll, projection/lens, object transforms, deformation, event/reveal timing, and authored holds. A requested different duration retimes the source; explicitly record the mapping. Never claim unchanged absolute speed and changed duration together.

Use **clarity adaptation** only when requested or already authorized. A changed viewpoint, earlier cutaway, transparent surface, moved asset or extended endpoint is an adaptation. Document the exact change and reason; keep it separate from a faithful export. Never silently substitute an easier animation. Record shading/grey replacements and suppressed effects too.

## Execute the workflow

1. **Verify access and protect the source.** Query the running Blender scene read-only through available MCP tools before changes. Follow applicable AGENTS.md connection instructions. Compare the active file to the requested source; never change another open project. Prefer background export from the explicitly chosen saved source. Preserve source hashes and use a separate output directory. Do not replace MCP implementations or modify connection settings.
2. **Extract measured evidence.** Run `scripts/inspect_blender.py` inside Blender with the job config. Read `scene.json`, `animation_keys.json`, and `motion_samples.json`. Preserve every relevant F-curve key and its interpolation/handles, drivers, NLA and constraints. Evaluate movement between keys, including parents, camera changes, deformations, visibility and caches. Raw action time may differ from scene time under NLA.
3. **Inspect actual views.** Review previews, start/end views, occlusion, foreground/background, relative scale, subject screen motion and difficult transitions. Coordinates, object names and frustum projection do not replace visual inspection. Explain attachments and purpose only where supported by evidence; label uncertain interpretation.
4. **Plan motion blocks and segments.** Divide by meaningful actions, environment/scale transitions or changes in governing motion, not arbitrary equal lengths. Respect explicit whole-shot requests; otherwise use focused segments when a complex journey is difficult to convey. Keep a master timeline for segmented work. Define boundary pose, velocity, lens, object state and framing. Do not add pauses or crossfades at joins.
5. **Export texture-free references.** Check that Workbench represents the scene's meaningful silhouettes, effects and edits; use an appropriate alternative for unsupported representations as described in the workflow reference. Customize config roles/greys/landmarks. Run `scripts/render_reference.py` for compatible scene-camera geometry. The helper compares motion, animation and geometry fingerprints before/after shading changes. It does not invent camera fixes, bake caches, or retime source keyframes. Use Blender tools on an authorized separate copy for those changes, recording lineage and adaptations.
6. **Package and verify.** Run `scripts/package_reference.py` using the same config. Read all warnings and inspect first/last, transitions and consecutive frames around ambiguous movement. Verify decoded count/FPS/duration, no unexplained blank/occluded interval, and no textures/UI/artifacts that obscure the task. Fix justified issues and rerun affected outputs.
7. **Write evidence-grounded prompts.** Use `assets/generation-prompt.template.md` and the writing reference. Supply explicit scene relationships, output-local timed blocks, fixed/moving parts, visible motion cues, exact start/end requirements, continuity and separate finishing. Cover each relevant key/event through a meaningful interval; do not write hundreds of redundant sentences for densely sampled camera keys.
8. **Deliver ready-to-use assets.** Author the scene/prompt documents and record actual visual inspection using `assets/review.example.json`. Run `scripts/finalize_package.py --config <job.json> --review <review.json>` to gate ready status on documents, unchanged assets and review. Provide clean motion videos, exact boundary images, necessary transition stills, scene description, prompts and handoff instructions. Explain which inputs control motion, appearance and endpoints. Use known generator capabilities; otherwise deliver portable assets and disclose unverified input support. Supply the finished prompt in chat as well as a file when requested. Do not upload assets, spend credits or submit to external generation without authorization.

## Package contract and completion

Each segment requires `motion_reference.mp4`, `first_frame.png`, `last_frame.png`, `prompt.md`, and a manifest with source range/samples, output FPS/duration, camera, source hash, adaptations/omissions, preservation checks and QA. Event PNGs are optional when they resolve real ambiguity. Labeled contact sheets are review aids, not clean generator inputs. Appearance references retain their actual provenance.

Also write `scene-description.md`; multi-segment work needs `master-timeline.md` describing joins. Scripts cannot reliably author these semantic documents alone: the agent must inspect evidence and write them. Mark inspection-only/prompt-only output as partial if rendered assets were requested.

Complete only after assets exist, checks pass, visual review is performed, and prompt timing matches the files. Describe what was checked: decoded export, inspected stills/sequences, or played video. Never claim a successful generator test without its actual result. Exactness is enforced for measurements and exported reference within recorded retiming/adaptations; generated reproduction is an outcome to verify. If output is supplied, find its first divergence and revise the relevant segment using the QA guidance.
