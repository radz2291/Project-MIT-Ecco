# Sparse cave / denser cut earth — v006

ECCO-057, owner-requested refinement,2 November2026. Current scene `../Scenes/S01-S02_production_v006.blend`, saved/open at the user's frame220. Dirtyv005 preserved as `../Scenes/S01-S02_session_before_v006.blend`; priorv005 remains. Only consumer upgraded to additive shared `World_motion_grid_v003.blend`. Existing camera, physical World v014, Surface v008, BHA, waveform and reveal timing unchanged.

## Easy controls

In Blender's3D viewport press **N**, then select **World Grid**. The panel supplies a master Grid enabled switch, independent Cave / Cut earth / Seabed switches, spacing for each area, and stroke width/opacity/shade. Larger spacing means fewer lines. Controls live on `World pixel guide controls`; modifier drivers read those saved properties, so each shot can choose its own preset. Source master defaults disabled; v006 enables the trial.

After reopening, run embedded **START HERE — pixel guides** once to restore the panel and live overlay. The shared master has the same setup text. No trusted-file auto-execution required. Existing GPU export helper includes the overlay in saved PNGs; native F12/Viewport Render omits Python overlays.

| Control | Previous shotv005 | Current shotv006 |
|---|---:|---:|
| Cave ring spacing |1m|4m|
| Cave lengthwise spacing |30deg, baked selection|90deg, adjustable|
| Cut-face depth spacing |25m|20m|
| Cut-face across-face spacing |10m|5m|
| Seabed spacing |10m|10m|
| Stroke width |1.2px|1.2px|

Cave rings are four times farther apart and lengthwise guides about three times farther apart. Lengthwise spacing supports30/60/90/120/180degrees; metre controls use whole-metre intervals. This avoids changing wall geometry to adjust density. Sparse source seams can still make individual guides irregular.

## Proof

720p1280x720 stills at80/106/157/220 passed0.53–0.88s each. Short cave proof95–122:28frames at24fps, maximum1.014s/frame; encoded and fully decoded. Local clip: `../Previews/Grid-v006/S01-S02_sparse_cave_v006.mp4`. Representative cave and cut-face stills are in that folder. Timing measures frame evaluation through PNG saved.

Verified: master off produces zero evaluated edges; Cave off leaves cut faces active; cut-face/seabed switches each remove their own guides. Four spacing inputs change evaluated counts and restore correctly. Scene reopened; panel/helper restored; relative library paths resolve. Shared master and shot native hashes are recorded in interface/verificationJSON. Native/video/raw frames local only; no new backup claim. AI finishing untested. This is a collaborative checkpoint, not acceptance or task closure.
