# ECCO-052 — Candidate controls and migration

New versioned files preserve the selected sources. Do not relink locked production scenes automatically.

- `Shared/Assets/ECCO/Satin_finish_v001.blend`: link node group **ECCO | Satin finish v001** into a section-local material. Its `Sensor face`, `Roughness offset`, and `Machining strength` inputs are local controls. The default machining strength is 0.018 roughness modulation; it adds no geometry or displacement. Existing alpha/transparency controls remain on the local Principled shader. Lights and exposure remain section-owned.
- `Shared/Assets/ECCO/ECCO_film_v003.blend`: unchanged v002 geometry, parents, sensor references, temporary closures and source scale. Material slots use the linked finish. Existing collection visibility controls remain available; source geometry and provisional acoustic/engineering limits are unchanged.
- `Shared/Assets/BHA/BHA_core_satin_v001.blend`: successor of accepted v006 core, linked to ECCO v003. Same connected bit/collar arrangement; steel finish linked separately, carbide/diamond materials preserved.
- `Shared/Assets/BHA/BHA_film_v008.blend`: successor of v007, linked to the new core. Existing `UPHOLE_CONTINUATION_CONTROL` properties `length_m` and `show` remain; default length is 12m. The `show` control supports a shorter hero view without deleting the continuation.

Use a consumer copy and relink the chosen successor, then reload/reopen. New filenames never update accepted consumers automatically. All saved libraries use relative paths. S02 retains its simple string and camera; no detailed BHA substitution was made. S07/S05 retain their original geometry and material alpha behavior, with the shared finish plugged into section-local material copies. S05's pre-existing ECCO v002 dependency is intentionally retained: only its appearance is shared here.

The native consumer copies retain original resolution/sample settings. Review render scripts explicitly apply 640×360 working settings without saving those changes to the consumer scenes. These benchmark results do not certify the untouched original full-resolution settings.

Consumer/baseline mapping and camera samples are in `Evidence/consumer-mappings.json`. `Evidence/package-verification.json` records reopened libraries and a bounded shared roughness edit observed in both S07 and S05, followed by byte-exact restoration of the finish source.
