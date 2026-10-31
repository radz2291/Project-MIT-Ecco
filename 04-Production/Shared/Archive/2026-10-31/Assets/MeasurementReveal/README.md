# Measurement surface reveal v001

Shared display behavior from ECCO-050: S02 v011 staggered arrival and ten-frame settle, with S06 v004 fine points, lines and a translucent fill. It is a stored-data display, not a fresh acoustic acquisition or calibrated physical simulation.

`Measurement_reveal_v001.blend` contains two independently linkable geometry-node groups:

- `ECCO Stored Surface Reveal v001`: local mesh in/out; Start frame, Stagger frames, Settle frames, Arrival offset. Local FACE float attributes `ecco_receipt_frame` and `ecco_reveal_order` supply each cell's history. Arrival = max(Start frame, receipt + 1) + order × stagger. Geometry remains hidden if either attribute is missing. Settle displaces the newly arriving surface slightly along its own normals and settles to its unchanged sample coordinates.
- `ECCO Fine Surface Style v001`: fine point radius, line radius, translucent fill. Exact S06 guide color (.2,.46,.72) and strength1.4 inform the fine treatment; S03 environmental contours remain a separate darker style. No measurements, dimensions or data colors are inferred from this presentation.

Use a local node-group wrapper to set inputs while retaining the linked shared group. This also avoids depending on version-specific modifier socket APIs. Keep section sample values, transforms and unfold/office motion local.

T-054 includes two authored shape cases plus an actual S02 integration copy. The S02 adapter derives reveal order from the existing `PIXEL history … start…` material names, preserves original materials and active acquisition row, and begins stored reveal only after recorded acquisition. Its fine overlay reads the evaluated local wall; it does not copy a replacement dataset.

Native files are local and Git-ignored. Refer to T-054 report for verification, performance limits and review status. No locked previs is replaced.
