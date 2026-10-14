# Worked Handoff — Fictional Interactive Exhibit

This is a **synthetic end-to-end example** of integrating outputs from the first four skills into one execution slice. No actual files, client sign-off, physical dimensions, renders, or code tests are claimed to exist.

## Situation

A small science-museum kiosk is supposed to show **which connection holds a removable panel in place**. Its actual connector geometry is not yet delivered. A hypothetical director prefers purposeful spatial reveals over constant motion, and an earlier design discussion selected a quiet on-screen label for a straightforward component name.

Four upstream contributions are already available **within this fictional scenario**:

| Input discipline | Fictional finding | Authority boundary |
|---|---|---|
| 01 — Taste discovery | Director appreciates discovering hidden relationships through changes of view; dislikes aimless camera circling | Preference, not a physical requirement |
| 02 — Contextual judgment | Use a spatial reveal of the connection, with a simple fixed label rather than a dense HUD | Proposed art direction, not museum/client approval |
| 03 — Spatial storytelling | Entry: assembled panel; discovery: connection location becomes visible; resolution: connection and panel relationship legible | Conceptual visual beats, no validated camera path |
| 04 — Information-to-visual | Source-to-meaning: panel → connector location → why the connection matters; mechanism claim remains unresolved | Illustrative explanation only until engineering reference is supplied |

**Current execution mode: PREPARE.** The agent may write a ready-to-run task, not create a validated 3D model or claim the museum's physical system is accurately shown.

## Reconciled authority map

- **Technical geometry and mechanism:** `NOT_PROVIDED`; the approved drawing and an authorized reviewer are required for an accurate mechanical animation.
- **Visual intent:** the fictional spatial-reveal choice above is a **proposal**, not a universal camera preset.
- **Presentation taste:** keep one short label legible; no fixed typeface, palette, lens, or easing values are known.
- **Tool environment:** no scene file or renderer has been verified accessible.
- **Public distribution approval:** `NOT_RUN`.

## The task an execution agent would receive

> **Goal:** Build the smallest editable *concept-only* storyboard that lets reviewers judge whether a spatial reveal clarifies the panel-to-connection relationship.
>
> **Before work:** Inspect any supplied brief, existing storyboard and registered assets. If no verified connector geometry exists, do not invent a detailed mechanism or functional demonstration.
>
> **In scope:** Prepare two or three labeled concept frames; a simple SVG plan linking entry, discovery and resolution; one quiet label; a note distinguishing camera movement from object movement.
>
> **Out of scope:** Final CAD, measured values, physical operational animation, finished video, client endorsement and destructive source edits.
>
> **Invariants:** Never imply a specific connector type, dimensions, force or safety guarantee without a source. All temporary symbols are labeled "illustrative / not to scale."
>
> **Agent discretion:** Choose the clearest composition, crop, rough timing relationship and 2D label positioning. The agent may propose a cut if a continuous camera journey adds no useful reveal.
>
> **Deliverable:** An editable concept board and a review note at paths actually established by the execution environment. Do not invent a repository path.
>
> **Proof requested:** Inspect the resulting SVG, verify its text and links/paths are intact, and ask whether the reviewer can tell (a) where the connection is and (b) how the viewpoint change contributes to understanding. Record visible deficiencies.
>
> **Stop/escalate:** If the user requests a physically accurate mechanism animation, require the approved geometry and its owner before claiming fidelity.

## Traceability mini-matrix

| Requirement | Supplied by | Artifact element | Review proof |
|---|---|---|---|
| Relationship becomes clear | Narration/creative purpose | Entry → discovery → resolution | Viewer understands the relation after looking at the board |
| Spatial reveal has a purpose | Skills 02/03 fictional decision | Changing view and visual anchor | Movement reveals something previously occluded |
| Label stays readable | Skills 01/02 fictional preference | Simple screen-space label | Reviewer reads label at target size |
| Mechanism claims are not fabricated | Missing technical authority | Generic illustrative connector mark | No factual dimensions/type asserted; disclaimer present |
| Final geometry not yet approved | Technical owner TBD | Explicit blocker in handoff | Production mechanism remains BLOCKED |

## What the agent can truthfully return immediately

**Prepared:** a bounded, coherent task specification (this example).  
**Produced execution artifacts:** `NOT_RUN`.  
**Inspected actual SVG or video:** `NOT_RUN`.  
**Physical source verified:** `BLOCKED` until geometry arrives.  
**Client approval:** `NOT_RUN`.  
**Next move:** run the concept-only SVG slice in a tool-enabled environment, inspect it, then obtain targeted feedback before engineering animation.

## What this tests

The fifth skill succeeds if another agent can start work **without rediscovering the artistic reasoning** and without accidentally upgrading taste into physical truth. The next agent remains free to make implementation and composition choices, but must identify the source and proof for every claimed result.

This example is an **illustration of expected skill behavior**, not a live execution or independent audit.
