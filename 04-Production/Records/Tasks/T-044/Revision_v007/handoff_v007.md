# T44 continuity release / T45 integration handoff

Canonical geometry/control successor prepared for scoped integration; human appearance approval pending. T45 is the sole Git integrator. It confirmed no earlier extension work was begun and independently inspected the primary actual PNGs. T44's five-still serialized slot is released; no further rendering planned. Live user Blender has unsaved changes and remains untouched.

## Exact inputs

- `04-Production/Shared/Assets/BHA/BHA_film_v007.blend` — SHA256 `b6b98f870064f5b9e07640bec9dadaeb457c7e45ebdb5d33d2ac18b6210acdd1`.
- [Native/consumer manifest](../../../../Shared/Assets/World/manifest_v007.json) supplies all final scene hashes and exact local root. Heavy natives stay local/Git-ignored; no off-machine backup/upload claimed.
- [Interface v004](../../../../Shared/Assets/World/README_v004.md), `World/Scripts/formation_controls_v004.py`, `World/Scripts/continuation_controls_v001.py`.
- [Wider product/connection](../Previews/Revision_v007/connection_wide_v003.png), [furthest uphole](../Previews/Revision_v007/furthest_uphole_v002.png), [unchanged camera A](../Previews/Revision_v007/Reuse_A_v002.png), [unchanged camera B](../Previews/Revision_v007/Reuse_B_v002.png), [propagation comparison](../Previews/Revision_v007/propagation_v007.jpg).
- [389 canonical native checks](Evidence/native-verification_canonical_v007.json), [package/timing/source checks](Evidence/package-verification_v007.json), [exact permitted tracked allow-list](allowed-tracked_v007.json), [current report](../report.md).

## Migration and dependent checks

Preserve existing T46/T47/T48 scenes. Snapshot original cameras, time ranges/fps, keyframes, independently owned controls and local source/event registration. Resolve current library paths before Save As. Reload only the direct `BHA_film_v006.blend` library to v007; leave nested source v006 intact. Then call:

```python
from continuation_controls_v001 import attach_continuation
local_control, parts, far_endpoint = attach_continuation(asset_dir, existing_hardware_instance)
```

`existing_hardware_instance` is the existing local collection-instance whose collection is `WORLD_HARDWARE`. New linked extension/joint children inherit its full placement/travel/spin. Local `UPHOLE_CONTINUATION_CONTROL.length_m` defaults12; `show` hides both for isolated heroes. Existing hardware visibility also hides them. No geometry copy, sensor/property reassignment or new motion tracks. New consumers can use `formation_controls_v004.create_world` directly. Save to new filenames with relative libraries and `relative_remap=False`.

Fresh-open: one ECCO, one extension, all relative links exist, unchanged predecessor hashes/camera/timing/keys/old-control values, same source geometry/metre scale and sensor/cap registration. Recheck actual combined contact/sightlines, hydraulic finite clearances/occlusion and performance because added geometry occupies upholeX<=-1.44m. T44 tests do not release combined effect behavior or approve an actual film shot. Existing T44 source consumers keep72/96frame timings. Shorter length/new camera paths require coverage checks.

## Performance and gate

All five full first render-to-file samples pass: final wide2.5567s, furthest1.6986s, reuseA1.5501s, reuseB2.0451s, retained first wide1.9690s.720p/EEVEE16/Vulkan, normal existing disk GPU caches, no warmup render excluded. Prior empty-cache startup12.55–25.13s remains unresolved; strict5s cap remains. Source geometry and exact client/thread interfaces remain separately qualified/provisional.

T45 should inspect the allow-list/staged diff, commit only listed task-owned records/scripts/selected stills, push normally to authorized main and verify exact remote SHA/parity. Return that SHA to T44 for pinned outputs and a finished run/Review update. T44 performs no Git mutation. Do not stage native files/logs/intermediate raw samples or unrelated generated image. All T45–T48 roots/global asset register remain T45-owned.

Progressive technical release enables integration planning/checks, not human acceptance. New T44 visual approval is pending; do not mark Done, remove dependencies or bypass the actual Work gate. Report any T45 reclaim barrier truthfully to Radzi. Only Radzi accepts reviewed work and assembles the film.
