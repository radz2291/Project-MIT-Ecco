# ECCO-056 current focused proof — ribbon v010

Awaiting Radzi's representation choice. This is a visual proof, not a finished shared library. V007 remains byte-exact as the alternative the owner liked. V008/v009 diagnostic ribbons are retained locally; v009's crowded full-pulse shape read as a fence, so v010 selects one broader cycle.

The fixed32filament ribbon selects2.5–5.0us of the unchanged assumed400kHz source pulse, tapers display endpoints with sin(pi*u)^0.3, adds modest static strand offsets±0.025 and amplitude fan0.65–1, then separately scales positive/negative height to±20.0195mm. This is an artistic sample-window/height mapping, not full-trace fidelity, measured ECCO data, pressure displacement or multichannel acquisition. Full transverse width40.000mm and vertical span40.039mm derive from the visible provisional acoustic cap; not certified hardware dimensions. Original24.576mm sensor-wall endpoints remain.

Only light travels along this static ribbon: native300–309 outgoing,309 contact,309–318 weakerreturn (half highlight gain). Seven saved-frame geometry/matrix hashes are identical and shader values differ. Source pulse time and cinematic playback time are separate. The79-frame clip samples native298–324 in1/3-frame increments at24fps:3.292seconds,3x slow review. Colors are artistic cyan/violet layers.

Review outputs: Previews/ribbon_v010_slow-review.mp4; Previews/ribbon_isolated_v010.png; Previews/ribbon_context-review_v010.png. The latter uses an explicitly separate20%wider review camera to contain full envelope and oval. Original context camera CAM_S01_Continuous remains in S02_ribbon-context_v010.blend; its diagnostic still is ribbon_context_v010.png and crops part of the upperfan. Review framing is not a locked shot-camera change.

Rendering960x540/Eevee32.79frames max1.41s/average0.35s full render-to-file; originalcontext2.671s, widerreview2.650s. Isolated source collections excluded, only ribbon/reviewcamera visible, late324 inspected clean. Dark-stage, originalcontext and widerreview native files remain locally organized under Shared/Assets/Acoustics/RibbonWaveform_v010. No remote heavy-media backup claimed.

Preserved v007 native SHA256940efed0f0cb2254c8301a58141c40532e3fcf1528e7958638b6e8a40260e519; video79d072cac103e17fd6a8bcdd408db98c1ed93db3911cca99bbd6538a1a76b96c. Original sourceCSV unchanged and already published in prior model package. Independent master verification and owner feedback govern next step; full controls/variants/consumer migration remain incomplete.

All three final v010 natives resaved with relative ECCO library references //../../ECCO/ECCO_film_v002.blend; path-only repair, no geometry/camera edits. Exact final native/media hashes are in publication-manifest_ribbon_v010.json.
