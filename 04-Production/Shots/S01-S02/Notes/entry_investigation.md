# Enclosed entry and cutaway reveal — investigation

2 November 2026, ECCO-057. Radzi requested recovery of the tight enclosed-bore experience near94 and reveal only during the later pullout. Investigation only: no production geometry, shared masters, camera or event animation changed in this pass. Pre-inspection dirty session preserved in Scenes/S01-S02_session_before_entry_investigation.blend. Working base ab2ba32194c54d925a062355d14a45b36bb1a0a7.

## Finding

Camera preservation alone did not preserve the previs experience. Production v002 uses a permanently open World v013 cutaway with a smaller static bore. The previs environment independently animates its front closure and bore width. Current frame106 shows the open background, whereas previs frame106 surrounds the viewer with a complete wall. The entry at94 also intersects new subsea equipment visually; its access/occlusion needs a separate focused check before the bore interior.

## Actual source

Fresh background inspection of `05-Previs/Section-02_Measurement-History/v011/Continuation/Scenes/S01-S02_continuous_v011.blend`, never saved. Source has the known missing old ECCO link; this does not affect early camera/environment animation. Exact native samples: entry_previs_native.json; reproducible script: ../Scripts/inspect_entry_previs.py. Existing source frames visually inspected at94/106/120/132/141 in `05-Previs/Section-01_Continuous-Descent/v001/Gentle-10s-Finish/Work/Frames/frame_####.png`.

- At94 camera Z=-106.963m, approaching the opening. At97 Z=-121.401m, below the -120m seabed.
- Camera XY stays(.22,-.35)m through122, radial offset about.4134m, inside the early .65m bore; this exceeds the smaller static shared-bore radius.
- Bore radius .65m initially. First measurable radial decrease113; settles to .155575m by141. Source proxy mesh is .65m radius, XY scale1 -> .239346.
- Front closure: `Opening front ## ±1`, shape keys Enclosed/Retracted. First nonzero retraction115, first full retraction123 (integer samples). At120 retraction .74074. Rear and side geometry also adjust. Closure changes begin before the camera's noticeable outward travel.
- Camera starts departing its steady inner XY position after122. At126 camera(.2755,-.5773,-335.501)m; at132(.6984,-2.3076,-402.009)m; at141(2.2235,-8.5475,-502.853)m. Thus the owner's approximate120 reveal is supported; existing marker141 describes the later transition stage, not its onset.

## Restoration decision

Preserve the established camera and source timing. Provide a closed360-degree bore for entry/interior travel, with shot-controlled camera clearance matching the original wider passage. Retract the front sector only on the recovered reveal schedule, tighten the passage smoothly through141, and preserve the exact existing World/S02 wall and event binding at the destination. Reuse the shared irregular profile/materials rather than re-enable the old faceted slabs as the final environment. The widening/retraction is an illustrative camera device, not a physical bore expansion or simulation.

Keep animation and clearance controls local to this sequence. If the World needs a reusable full-shell/front-sector variant, add a versioned shared successor without changing pinned consumers. Do not globally scale the entire geology or alter BHA dimensions to force the view. Check the approach against current subsea/riser geometry at90–100 so a camera-access treatment does not introduce a visible hole or jump. No technical certification implied.

Next proof: one focused90–152 moving comparison, same camera and source timing, demonstrating enclosed passage first and cutaway only on reveal. Benchmark representative frames before rendering under5s/frame. Existing source and all v002 hardware/effects stay recoverable. This investigation has not yet built that restoration.

Current matched Workbench480×270 frames94/106/120/132 are in Previews/Entry-investigation;1.04–1.22s render-to-file. See entry_current_benchmarks.json. Native/media local only, no new backup claim.
