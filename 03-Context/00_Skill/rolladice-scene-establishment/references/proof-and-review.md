# Small Proofs, Clear Reviews and Fewer Repeated Revisions

## The purpose of a proof

A proof answers one question that could change the next decision. It is not a smaller decorative render or a reason to delay production indefinitely.

Before testing, state: **question, suspected cause, variable to change, things to preserve, artifact to inspect, success condition, budget and stop point**. Use the existing contract or task, not another permanent report for every experiment.

| Question | Useful proof | What it does not prove |
|---|---|---|
| Does a required geometric condition exist? | Values, matched-axis cross-sections, neutral silhouette | Actual field occurrence or operational safety |
| Is the event sequence understandable? | One short cause/response loop | Full-scene rhythm |
| Is the image design suitable? | Source reference next to candidate at comparable scale | Correct 3D mapping |
| Is the texture placed correctly? | Flat image, ideal surface, actual surface with shared landmarks | Scientific validity of the source image |
| Does the camera reveal the feature? | Simple proxy path with real relevant bounds | Final materials or audio |
| Is the edit continuous? | Outgoing/incoming clips joined at the planned cut | Shared scene/data identity |
| Does the final reveal work? | Critical few seconds plus settled result | Whole-film acceptance |

## A disciplined diagnosis

Start from the artifact, not the agent's report alone. Record file/version and timestamps or visible states. Describe what the viewer sees before guessing causes.

Example:

**Observed:** the pattern appears folded when viewed along the tube.

**Hypotheses:** relief-like image content, mapping error, actual surface irregularity, shader response or perspective.

**Test:** same source image and display settings on a flat plane, ideal cylinder and actual wall; then matched camera controls.

**Conclusion:** accept only what the comparisons support. If an ideal cylinder also looks folded, actual wall irregularity is not the sole explanation. If the material is verified unlit, stop asking for removal of specular highlights already absent.

Do not state "the node graph is wrong" from one screenshot. Do not claim to have watched a video when only sampled stills were inspected. If evidence is unavailable, state the narrower review that is possible.

## Find the failed decision

| Failure | First place to investigate |
|---|---|
| Viewer cannot tell what discovery matters | Stage 01: story order and significance |
| Claimed geometry, motion or value is unsupported | Stage 02: truth and mechanism |
| Correct process looks like something else | Stage 03: representation |
| Chosen representation has the wrong visual character | Stage 04: look and reference |
| Important relation never becomes visible | Stage 05: composition and motion |
| Approved image/motion fails in software | Stage 06: implementation proof |
| Earlier accepted work changes unexpectedly | Dependency, version and continuity checks |
| Correct result cannot be shared | Rights and release scope |

Failures can have more than one cause. Fix the most informative one first; change multiple factors together only when their interaction is the hypothesis. State that reason and keep a control.

## Targeted correction format

**Verdict and scope:** working / partly working / not yet, naming what was reviewed.

**Intended versus observed:** one plain-language sentence for each.

**Preserve:** exact accepted artifacts and behavior.

**Change:** one highest-value correction with a visible target.

**Executor freedom:** safe implementation options, not invented source parameters.

**Do not imply:** the main false interpretation to avoid.

**Next proof:** exact still, event or short clip and its pass question.

Default to a concise message. Put long calculations and source records in the existing linked contract. A user asking for a brief agent comment should not receive another whole production brief.

## Separate quality decisions

Review **technical meaning**, **implementation**, **human comprehension**, **appearance**, **motion/edit continuity** and **delivery** independently. A component can pass one and fail another. Do not call a texture scientifically invalid because it feels material-like, or approve a signal's physics because its glow looks convincing.

Owner taste is legitimate but must be named as taste. A new preference should reopen the relevant direction, not retroactively label a faithful implementation a bug. A changed acceptance criterion needs an explicit reason and affected scope.

After an actual non-specialist watches the intended preview, record what they understood without coaching. Agent self-critique is useful but is not an independent comprehension test. Domain approval must come from the designated authority, not a scene script or a reviewer role label.

## Stop rules

After two attempts aimed at the same symptom with no useful improvement, pause that approach and reconsider the hypothesis, source reference or representation. This is a trigger for diagnosis, not an automatic requirement to rebuild.

When a focused test passes the agreed requirement, stop polishing that component and advance within permission. Nonblocking grain, placeholder text or mild preview shading should not restart scene design. Name limitations rather than silently declaring final quality.

Do not promise a fixed number of iterations. Aim to reduce avoidable rework by testing uncertainty early. If the user changes the intent, treat the resulting iteration as a new decision, not process failure.

## Integration checks

A passed isolated test must still be checked inside its consuming shot. Verify entry, main reveal, settled outcome and exit, plus adjoining cuts. Check actual playback at intended speed and final screen size. Preserve proof references so regression is identifiable.

For data layers, verify fixed geometry, correct spatial mapping, source identity, declared display scale, legend semantics and seam behavior where applicable. For a seam repair of synthetic art, preserve the original, identify the derivative and disclose that pixels changed. Never silently seam-paint genuine field data.

Keep verification proportional. A claim about exact unchanged geometry can justify hashes or vertex checks. A style-only comparison needs controlled stills. Do not require exhaustive technical evidence unrelated to the decision.

## Performance and application safety

Read the actual project's render/frame, time, cost and hardware constraints. A five-second render cap in one project is not a global rule. Benchmark representative and heaviest states before a long batch. Distinguish setup, rendering, encoding and verification time.

A preview must use features capable of answering its question. A fast mode that quantizes a reveal or omits transparency may be unsuitable for an appearance test, even if useful for camera blocking. Report that limit and use the cheapest adequate alternative.

Use separate versions and reversible tests. Protect unsaved application state and shared assets. Reopen saved candidates and verify local asset paths. Don't upload large media or restricted references by default.

## Final review record

Use these terms precisely: **proposed, created, inspected, self-checked, source-supported, owner-approved, domain-approved, not checked**. "PASS" always names its test and artifact. "Ready to build" is not "finished film." Carry unresolved issues only to the operations they affect.
