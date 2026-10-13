# Worked example: subsea descent

This example demonstrates how to translate measured motion and inspected images into instructions. Replace it with the current job's evidence; it is not a default offshore animation or a universal four-second limit.

## Source and assets

The approved saved source spans frames 55-86 at 24 fps. A requested four-second export uses 96 evaluated samples with inclusive source endpoints. Source frame 70 is represented by output sample 47, source 70.0105, at 1.9167 s. Frame 82 is represented by sample 84, source 82.0842, at 3.4583 s. The last source endpoint appears at 3.9583 s and remains displayed through 4.0000 s.

Export a texture-free Workbench video, exact first/last stills and two event stills. Retain the labeled contact sheet for QA only. The saved source already includes the previously approved endpoint camera revision; record that lineage instead of describing this export as an unmodified copy of the earlier original scene.

The inspected camera descends alongside a fixed riser. It moves closer horizontally early and outward later, with changing viewing angle and slight lens changes. It is not a straight vertical translation. The first image looks down the shaft; intermediate images reveal the lower assembly; the final image puts the rectangular base across the upper image with nearby ground in the foreground. Collars and rails travel upward in the picture because the camera descends.

## Example motion instructions

> 0.00-1.28 s: start already looking down beside the stationary riser. Descend and move horizontally closer along the supplied path. Keep the continuous shaft beyond the top of frame; collars pass upward through the image.
>
> 1.28-2.55 s: continue descending without a pause. The lower equipment becomes clearly visible and grows through physical approach. Around 1.92 s, match the transition still showing the tall riser leading to the still-small rectangular base below.
>
> 2.55-3.46 s: follow the authored slight outward movement and changing angle toward the lower equipment. Stacked housings, side blocks and protective posts grow into the foreground. Around 3.46 s, match the close assembly view.
>
> 3.46-4.00 s: continue down past the lowest housings and rails until the camera reaches the base/ground boundary. The base travels upward through the image. End with the base across the upper image and ground in the foreground, matching the exact final still. Do not finish on a distant view of the entire assembly or add a hover above the seabed.

Add the explicit scene description and separate finishing appropriate to the request. Do not invent an appearance image that was not supplied. Describe realistic steel/seabed if the user requests realism, while preserving the visible shapes and relationships. Avoid adding atmospheric effects that conceal the endpoint. Reference greys and suppressed volume effects are visibility controls, not instructions to make real steel transparent.

This package was tested for reference extraction, rendering, decoding, timing, preservation and visual readability. A generated-video reproduction was not tested by the skill build. The user's earlier reported success applies to the earlier segment experiment, not a universal generator guarantee.
