# T-031 / B1.5-A — cinematic shot architecture v001

17 October 2026 · **D0 proposal for Radzi review — no creative acceptance recorded**

## Identity and authority

- Stable task `d73a0020-fdf0-4036-a572-43e55eb309f0`, project MIT ECCO, reviewer Radzi.
- Run `8f6a420e-d1b7-4f5b-8dde-095c9704eb72`; stable worker `codex-t31-ai-director`. Fresh live task/handoff and owner override revision 1 checked. T3/T5/T6 are Done. No other ticket claimed.
- Authority: Radzi's direct T31 request to develop, save, synchronize and submit a proposal. This permits review records and D0 contracts despite the generic AI Director workflow's default to discuss before ticket/document changes. It does **not** approve the direction, start Blender work or release downstream production.
- Actual checkout `/workspace/scratch/a3bb82cc35c1/Project-MIT-Ecco`, branch `main`, remote `https://github.com/radz2291/Project-MIT-Ecco.git`; base `8d3ef594ac629c21adc255ebe8ad7a3cb1b10a99`. Fresh clone initially clean. Radzi's Windows native media was not available or inspected here.
- Owner override governs sequencing: B1.5 concept → editable 3D storyboards → T39 timed storyboard assembly → T40 exact-film human gate. B2 additionally requires explicit Radzi resume; B3 motion remains later. Earlier README sequencing is not used to bypass that override.

## Reviewable result

**Recommendation: “The hidden wall becomes readable.”** Follow sound from a real sensor to a discovered wall, then broaden the result into geometry, separate acoustic response, casing evaluation, hydraulic design and readable recorded output. Resolve on the actual tool. Camera arrivals change what the audience understands; mechanical board panels supply information rather than compositions.

- [Film direction map and review record v001](../../../Direction/B3/film-direction-map_v001.md): creative premise, differentiated framing/rhythm, 17-shot map, section takeaways/truth constraints, transitions, source limits and review decisions.
- **17 canonical D0 Scene Direction Contracts** under `04-Production/Shots/S01–S07/<shot-id>/direction.md`, linked individually from the film map. Each follows the 11 minimum contract fields; actual transforms/lens remain pending scene inspection. No parallel camera/handoff spec created.
- **S02 priority pilot plan:** six essential 16:9 camera-framed still states across three shots, native version/metadata/source requirements, controlled revision/rerender proof and audience/expert review tests. These are future pilot requirements, not delivered storyboard stills or B2 refinement instructions.
- [Shot index v001](Evidence/shot-index_v001.json): per-shot timing, contract and source paths. Totals remain 10/12/18/18/12/12/8 = 90 seconds. Provisional 24fps implies 2160 frames; final delivery settings are not locked.
- [Source manifest](Evidence/source-manifest_v001.json), [sanitized task/dependency snapshot](Evidence/task-authority_v001.json) and [self-check evidence](Evidence/verification_v001.json). This map/index is the new proposed cinematic register for this review; historical A03 registers/previews remain unchanged and do not depict the new shots.

## Inputs studied and limits

Read active AI Director and Scene Director, authority map, Engineering Baseline/decisions, MIT identity, narrative windows, production workflow/closure, directorial modules 01/02/04/05/06/07/08/09 and index, V2 section captions/narratives and C01–C09. Read T3 inventory closure, T5 plugged-v002 evidence, T6 v003 evidence/interfaces, B201 v006 report/consumer guide, B202 v009 synthetic mechanism/handover and T27 current v007b report; original client chat was consulted for source relationships. The revised S03 through-depth caption overrides literal rotating-ribbon readings. Also read preserved B203 v002/T9 and B204 v001/T10 candidate reports; these contain useful mechanism studies with open framing/stage-map limits, not accepted film layouts. No B205 implementation record was found at the expected production paths. Exact source hashes are recorded for 47 files.

Live Work distinguishes B201's historical accepted baseline from current Review; T27 v007b remains Review and is a 30s mechanism library, not a film shot. T8 synthetic acceptance does not establish ENP3 acquisition calibration. Native libraries/videos are ignored local media on the production machine; repository reports/selected images are not substitutes for reopening them. No full video replay or actual camera inspection is claimed by this direction task.

Source-attributed product facts, synthetic reconstruction and illustrative treatment stay distinct. No confidential ENP1 report pixels, invented field values, measured instrument accuracy, actual MIT FEA/CFD contours, hydraulic performance values or client approvals are included. C08 actual-analysis and C09 rights-cleared-report slots are reserved inside the existing durations with clearly marked internal placeholders. Final substitution/omission requires an explicit scope decision; placeholder presence does not close either source blocker.

## Checks

Run from repository root:

```bash
python 04-Production/Records/Tasks/T-031/verify_direction_v001.py
git diff --check
git status --short
```

Self-check verifies 17 unique contracts, contiguous 0–90s, section sums, provisional 2160 frames, 11 contract fields each, local Markdown link resolution, saved output hashes and unchanged input fingerprints. The assistant additionally read the film map and shot-contract content for source/camera/audience consistency, preserving existing mechanism/rights/approval limits. These are document self-checks; no independent review, human comprehension test, physics validation, rendered still, opened native scene or motion proof is claimed.

## Review questions / next action

Radzi reviews the central concept, 17-shot count/time map and S02 pilot premise. Focus questions: does the film's discovery progression feel compelling; is S02's 12-second teaching load right; does S04's response-to-map emphasis feel clear; retain or revise the reserved C08/C09 source slots? The map records assistant critique and risks. No general taste questionnaire or extra engineering confirmation is made a prerequisite to this proposal review.

Only after exact concept acceptance and separate authorized storyboard execution should the dependent ticket create/edit scenes. Storyboard approval does not certify mechanisms; B2 stays paused until explicit resume and required exact-film gate. Work remains Review until Radzi acts; do not self-mark Done or alter other tickets/dependencies/reviewers.

## Synchronization and preservation

The full live-input snapshot remains local/ignored under the repository rule; the synchronized authority snapshot excludes unrelated account/workspace details. Only this task's text/JSON records, verification script and new proposed-shot `direction.md` files are included. Existing shared masters, mechanism scenes/scripts/data, historical A03 previews/registers, task acceptance and client records are untouched. No new heavy media exists. This is repository-backed work, not a separate artifact-library copy.

The containing candidate commit SHA and commit-pinned report/map links are recorded in Rolladice **after** a normal scoped push and fresh remote reachability check. The report does not insert its own commit hash recursively. If synchronization fails, keep the task visibly incomplete and record the exact blocker; never infer a successful remote submission from a local save.
