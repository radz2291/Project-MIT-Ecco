# S04 v019 — continuous physical scene with temporary C comparison

## Released change

Owner rejected the v018 cut-based assembly and required one continuous main camera. C may enter as a temporary comparison during B, then exit before the camera continues to D. Owner also requires the borehole already cut at 50% from the start, with no animated cutaway. B must be recomposed for that fixed section. The current instruction explicitly releases execution of this revision.

AI Director camera guidance was applied by composing the sensing and wear arrivals before connecting them. The camera retains a stable radial frame of reference, settles for the response comparison, then approaches the worn inner wall through the existing open half. Position, gaze, lens and horizontal framing changes use sampled smooth transitions. There is one main camera and one physical well scene for all 432 frames. No editorial cut or specimen substitution connects B to D.

## What appears

|Time|Action|
|---|---|
|0–4 s|Follow upward entry into the already sectioned casing; approach the side sensor.|
|4–5 s|Read the physical B arrangement: formation, cement, steel, internal fluid gap and ECCO.|
|5–5.5 s|C comparison window slides into the right half. B stays in the continuing main view.|
|5.5–9.75 s|Synchronized approved send/contact/reaction/return, with different illustrative decay.|
|9.75–10.5 s|C window slides out; the underlying main image remains continuous.|
|10.5–13.25 s|Same camera moves along the fixed section and enters the inspection gap beside the tool.|
|13.25–18 s|Reference/current contours appear, followed by the fixed computed wear-depth display and final hold.|

## Preserved source meaning

The main scene starts from the approved v009 B native scene. The approved canonical full worn steel is clipped once, before animation, by the fixed section plane. This restores the full retained 180-degree half rather than using a second crop of an already sectioned steel mesh. No radial dimensions or wear depth are enlarged. Existing capped cement and localized stationary exterior fluid channel remain fixed. The surrounding formation is extended as illustrative context to fill the opening view; it is not field-data geometry.

The approved B response animation is shifted uniformly by five seconds. C retains its native timing and is displayed against that same clock. C is a separate fixed location and explanatory camera view. It is not an ultrasonic picture of fluid, a flowing stream or cement changing in front of the viewer. Source layer colors are translated from the earlier Workbench display to inexpensive EEVEE shading for a consistent continuous physical scene.

D uses this same whole-length steel, not the cropped inspection specimen from v017. The cool palette and reference/current profiles come from v017. Curves are statically clipped to the permanent viewing section. The loss field is recomputed on the continuous source steel using registered nominal radial intersections: max(0, actual inner radius minus nominal inner radius), in metres, with roundoff below 0.1 micrometre set to zero. Outer vertices stay zero. Maximum remains approximately 3.998 mm. Revealing its colors does not change the mesh. Fine dashed nominal sectors, solid cyan actual worn sectors and grey normal context remain distinct. No toothpick or new measurement numbers are added.

This is authored illustrative geometry and response, not field measurement, calibrated defect identification, physical wear simulation or a direct one-pulse wall-thickness/volume measurement. No new engineering claim is introduced by the camera revision.

## Verification and cost

Representative entry, sensing, transition and wear frames are benchmarked before batch rendering. Each render-to-file is logged and must remain strictly under five seconds; the owner target remains roughly one second per rendered frame, with playback at 24 fps. Exact final count/mean/maximum timings are in delivery.json and timings-render.json / timings-C-render.json. Startup, framing tests and movie assembly are separate overhead.

The package verification checks the same main camera across all 432 frames, unchanged physical mesh coordinates and transforms, fixed physical-layer visibility, accessible relative libraries, maximum authored wear and all review image dependencies. The native package is saved/reopened and the complete movie is decoded through 432 frames. There are no camera-bound timeline markers that switch cameras. The C window score records its source frame and screen position explicitly.

Visual self-review uses the main arrival/transition stills and chronological assembled frames. It checks the layer separation at B, paired contact and response, C entrance/exit, the absence of physical opening animation, and the view of the worn wall around the tool. The move has deliberately readable arrivals rather than constant travel. Normal-speed audience comprehension and acceptance of this new composition remain for owner review. No cold-viewer test or client acceptance is claimed.

## Files and preservation

The complete native contains both the editable main physical scene and a review scene referencing composed image frames. C has its own native source. Scripts and exact camera/window scores make the render reproducible. Original v006, v009, v017, v018 and canonical assets remain unchanged. Heavy media remain local; only task-owned records, scripts and selected stills are synchronized. opened-in-Blender.json records the actual live handoff.
