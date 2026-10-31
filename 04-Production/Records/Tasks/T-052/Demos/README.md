# Hardware — SHARED + DEMO

Open **Hardware_demo_v001.blend**. The upper exhibit is the standalone ECCO; the lower exhibit is its connected BHA assembly. They link the existing shared masters rather than copying a section scene. There are no measurement datasets, film cameras, fluid animation or section timelines here.

The file opens in its review camera with quick solid/Workbench shading. The existing continuation control is selected: open Object Properties → Custom Properties. Set **show** to `1` to reveal the uphole continuation, or `0` for the connected core only. **length_m** defaults to `2` in this demo. The shared master still defaults to `12`; these are local library overrides. Longer lengths may extend beyond the review camera; zoom out for inspection. Geometry and satin remain live linked.

The existing shared masters are unchanged:

- `04-Production/Shared/Assets/ECCO/ECCO_film_v003.blend`
- `04-Production/Shared/Assets/ECCO/Satin_finish_v001.blend`
- `04-Production/Shared/Assets/BHA/BHA_film_v008.blend`
- `04-Production/Shared/Assets/BHA/BHA_core_satin_v001.blend`

The linked **ECCO | Satin finish v001** node group remains revision1, base roughness .291 with its original .018 machining modulation. Review lighting is stored locally. Workbench shows form/organization, not the node-based satin shader; the earlier S07/S05 material proofs remain the finish evidence.

Reopen checks confirm relative links resolve and the actual linked control changes extension visibility and evaluated length. The four master hashes match the previous delivered manifest. See `verification.json` and `master-audit.json`.

The first Eevee still took **32.895s**, failed the render budget and stopped the run. It is retained in `Hardware_demo_show0.png` / `render-evidence.json`. The quick Workbench organization still took **1.652s**. Default native settings now use Workbench. No animation batch or consumer-copy delivery was created in this cleanup.

All native Blender files remain local with no new backup/upload claim. This package is for owner review, not engineering certification. Temporary closure and BHA interface limits remain unchanged.
