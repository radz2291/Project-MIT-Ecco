# Progressive product-arrival trial — v008 (not selected)

Owner decision2 November2026: keep original v007 motion. v008 is retained as an unused comparison trial; v007 is restored as current.

ECCO-057,2 November2026. Owner requests a clear fade in travel speed before the product close-up so the viewer feels the approach is nearly complete. Owner clarified the slowdown should be around180. This matches the first product arrival: the trial is clearly braking around180 and settles into the close-up at240. The affected camera span is141–240.

Current trial: `../Scenes/S01-S02_production_v008.blend`, saved/reopened at216. Dirtyv007 preserved in `S01-S02_session_before_v008.blend`. Full-film baseline and its22s render remain v007. This proof changes camera pose only142–239; all rendered integer camera samples outside that range match their source exactly. Lens action, first-ping handoff240, waveform/measurement events, grids and shared geometry are unchanged. Total scene remains528frames/24fps.

## Motion

Previously most travel stopped around180, while the lens continued zooming through240. The trial spreads braking over the last part of the descent, following the existing route and orientation samples. Travel slows steadily as the grid passes the camera, then settles into the same product framing at240. The lens keeps its existing zoom timing. No added cut, title or lighting change.

Implementation: camera action copied and original retained. Route sampled at1/8frame for cumulative distance over141–240 (227.168m). Distance easing1-(1-t)^4.76966 matches incoming travel speed and tends to zero at arrival. Camera location and quaternion read from the corresponding source path time. Observed travel per frame at141/156/180/204/228:10.738/5.761/1.606/0.229/0.003m, progressively decreasing. Saved speed samples pass monotonicity within1mm/frame numerical tolerance. Endpoints and camera curves outside the affected integer frames have zero error. Pose-only retiming means the scene's optical zoom continues independently; this is an artistic trial to review in motion.

## Proof

`../Previews/Arrival-v008/S01-S02_product_arrival_v008.mp4`: frames128–264,137frames,1920x1080/24fps,5.708s. Original and trial comparison: `compare_v007_left_v008_right.mp4` (original left, trial right; synchronized source frames). Both videos decoded137frames successfully. All newly rendered frames passed strict5s cap:0.469–0.712s, mean0.525s. Separate720p still benchmarks and one1080p benchmark passed before the batch. Comparison sheet samples source frames152/180/204/228.

Native reopened; original action retained, live overlay restored and relative libraries resolve. Source-action mapping, travel speeds, render timings, decode progress and native/video hashes are in accompanyingJSON/txt. Native/video/raw frames remain local only; no new backup claim. This is a focused trial for owner visual feedback, not acceptance or a new full-film render. AI rerender untested.
