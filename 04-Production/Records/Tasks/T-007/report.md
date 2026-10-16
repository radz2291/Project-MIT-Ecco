# T7 — Still03 width-led patch coverage v016

Task fbe3e8c3-5ccf-4205-9aa4-48832b0d2cd3. v015 directionally approved; exact Still03 final visual acceptance remains pending. Full T7 incomplete; no Still04 or animation yet.

[Owner direction record](Evidence/Still_03/directional-approval_still03_v015.json) | [Direction contract](../../../Mechanisms/B201/direction.md) | [Prior report](report_still03_v015.md).

[Native 1920×1080 Still03 v016](../../../Mechanisms/B201/Previews/Still_03/B201_wall-interaction_still03_v016.png) | [Retained v015 comparison](../../../Mechanisms/B201/Previews/Still_03/B201_wall-interaction_still03_v015.png). Editable local scene: `04-Production/Mechanisms/B201/Scenes/B201_wall-interaction_still03_v016.blend`. [Builder](../../../Mechanisms/B201/Scripts/build_still03_v016.py).

Localized coverage change: patch width influence radius increases 35 percent from 15 to 20.25mm, while height remains 17mm. This targets the requested 30–40 percent larger visible area as a visual starting point; irregular cell visibility, perspective and rock geometry mean it is not a measured pixel-area claim. Existing rock texture, organic boundary variation, strongest activation at contact and edge dropout/fading are retained. Cell spacing unchanged, so expansion exposes additional cells rather than enlarging existing cells.

The acoustic membrane geometry/material and actual sphere-rock intersection remain exactly unchanged. The cinematic surface-registration field expands laterally from the same contact origin; this separate visual acquisition spread avoids enlarging the acoustic sphere or falsely claiming that its physical contact footprint grew. Existing local registration delays and completeness variation retained. Editable `acquisition_growth` (0 to 1) scales the localized surface mask from the contact origin to its maximum; rendered at 1, with no keyframes or animation. Patch remains a measurement-acquisition metaphor, not a literal rock-texture image from one ultrasonic ping.

Camera/composition, ECCO, borehole mesh, membrane shape/material, actual contact seam, lights and cyan language preserved. [Render record](Evidence/Still_03/build-render_still03_v016.json) | [Saved-scene verification](Evidence/Still_03/verification_still03_v016.json) | [Actual intersection correspondence](Evidence/Still_03/contact-correspondence_still03_v016.json). 37 saved-scene self-checks passed. Prior v015 hashes rechecked and unchanged; membrane vertices/material sockets compared directly with v015. Exact full-size image inspected.

Selected render/scripts/evidence synchronize to established main; exact SHA/pinned report recorded on Rolladice after fresh remote verification. Scene remains local ignored media without remote backup. O04 calibration remains unresolved. Await final approval of this Still03 image before Still04 — Returning Echo. No whole-ticket completion or self-acceptance.
