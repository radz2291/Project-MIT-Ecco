# S05 v017 — Approved amber treatment, four-second render

Owner approved the v017 still and requested rendering on 23 October 2026. The approved slightly lifted fog and richer matching amber rocks/trails are retained exactly. Fluid strength is 0.44 of v014, surface alpha 0.011; rock/trail linear RGBA (1.0, 0.48, 0.035, 1). Longer trails and 50% larger fragments retain their checked motion and geometry.

## Delivery

- Video: `Previews/S05_rich-amber_v017.mp4` — 4 seconds, 96 frames, 24 fps, 1280 x 720, H.264.
- Editable native: `Scenes/S05_rich-amber_v017.blend`.
- Review page: `Previews/review.html`; chronological contact sheet: `Previews/motion-review.jpg`.
- Entry, interaction and exit stills are beside the video. The original approved still remains `Previews/rich-amber_still.png`.

## Verification

EEVEE, 6 samples. Representative preflight frames 1/48/96 rendered in 1.87/1.14/1.12 seconds. All 96 batch frames stayed below five seconds; maximum 1.662 seconds, mean 1.079 seconds. The MP4 decoded completely to 96 frames. Batch frame 48 is pixel-identical to the approved still. Native hash is unchanged; reopened in live Blender at frame 48 with a valid relative ECCO source link.

Twelve chronological decoded frames were inspected. The same three fragments travel through the passage. This is illustrative motion; existing v012/v013 geometry checks are inherited, not CFD validation. Owner normal-speed review of this rendered proof remains pending. Full 18-second integration is not released.

## Storage and recovery

Previous proofs and shared masters are preserved. Native, video and shared dependency have matching same-machine recovery copies under `D:/MIT-ECCO-Render-Recovery/S05-v017-Still-Review/`, preserving relative paths. Frame cache: `D:/MIT-ECCO-Render-Recovery/S05-v017-RenderCache/Frames` (kept on D because C has limited space). Heavy media remains local, not offsite. See `Records/animation-verification.json` and `Records/media-verification.json`; exact source-control publication evidence is saved locally in `Records/animation-sync-verification.json` after push.
