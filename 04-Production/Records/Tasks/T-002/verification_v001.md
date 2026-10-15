# A02 verification — v001

15 October 2026 · Agent self-checks, not independent engineering validation.

- Live task/handoff and latest pinned standard v2 read; no dependencies; run claimed with stable worker and periodically updated.
- Native STEP header inspected: AP214 / NX2506.1700 / export 9 October / mm / BREP declaration; matching current and older source hashes. No fresh STEP solid-validation or conversion claim.
- Four saved `.blend` files open using Blender 5.2.2 LTS in separate background processes; dimensions/units/objects/resources recorded. No missing external images or linked libraries detected in those candidates.
- Source mesh inspection image rendered and viewed. Sensor annotation, inherited motion contact sheet and 26-image reference contact sheet viewed. Three scene markers measured at 120° spacing on one plane. Shoulder/mud-sensor validation remains open.
- Official live MCP connection succeeded after Radzi enabled Blender: clean unsaved default scene, no ECCO loaded. Read-only queries; no source saves or live changes.
- 3-page brochure text and all page renders inspected. 21-page original ENP1 report text extracted privately, first-page render inspected. Permission not assumed; private evidence ignored.
- 18 video headers inspected; 15 samples decoded across five selected videos, contact sheet viewed. No claim of full frame-by-frame video QA.
- 53 current local input records and 13 selected external records hashed. Closure helper rechecks all 66 hashes and relative links; results saved in `Evidence/closure-check_v001.json`.
- Git whitespace/status/ignore checks at closure. Existing A01 edits preserved. No commit/push/client contact, source movement or backup claim.
- Closure passed: 7 Markdown files, 51 relative links, 66 matching source hashes, all retained files nonempty; Git whitespace check passed. STEP and Private field-log preview confirmed ignored. Rolladice revision 100 confirms T-2 Review and run finished, reviewer Radzi retained.

## Reproduction

Runtime: `C:\Users\RZ1\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. Blender: `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.

Run the saved inspection helpers from the repository root. For each registered scene, use:

```powershell
& 'C:\Program Files\Blender Foundation\Blender 5.2\blender.exe' --background '<registered-source.blend>' --python '04-Production\Records\Tasks\T-002\inspect_blend_v001.py' -- '<task-evidence.json>'
```

`render_inspection_v001.py` uses the same command shape and a PNG destination; it makes a temporary camera only in the disposable background process and never saves the scene. `inventory_v001.py`, `register_external_v001.py`, `inspect_media_v001.py` and `verify_v001.py` run with the listed Python runtime. Historical source scripts were not blindly rerun.

Brochure rendered with `pdftoppm -f 1 -l 3 -scale-to 1100 -png`; field-log first page with `-f 1 -l 1 -scale-to 1000 -png`. Destinations are the registered task Evidence/Private directories.

Useful failure evidence: live MCP initially unreachable; official CLI tool lacked executable configuration; first inspection render found no World datablock. Direct installed background Blender and corrected viewport background completed the saved-file inspection without configuration/source changes.
