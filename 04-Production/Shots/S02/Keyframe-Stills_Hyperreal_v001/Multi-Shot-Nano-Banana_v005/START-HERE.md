# Section 2 — six-shot Nano Banana package

Prepared on 31 October 2026 from the six frames already selected in this chat. This package carries the current single-shot direction into the full sequence: pristine commercial steel, continuous machined housing and dense solid brown rock. It contains prompts and reference inputs; no new AI generation or Blender render has been run for this package.

## Main test: six shots in one image

Use the Nano Banana node you preferred in Weavy. Connect these files in this exact order:

| Node input | Packaged file | Purpose |
| --- | --- | --- |
| Image 1 | `inputs/01-blender-six-shot-grid.png` | Six approved views, layout, geometry and event states |
| Image 2 | `inputs/02-tool-reflective-metal.png` | Reusable four-view reflective steel reference |
| Image 3 | `inputs/03-rock-solid-structure.png` | User-supplied rock photograph: connected stone forms and surface character |

Paste the entire contents of `prompts/01-six-shot-final.txt` into the final generation node, replacing the old pilot prompt. Do not append the earlier granular-rock or single-shot instructions.

Keep the other settings that worked in your Nano Banana pilot. Match Image 1's 8:3 overall aspect if the node exposes that option or custom dimensions. The reference is 2880x1080: six 960x540 shots. This is the reference size, not a claim that this model/node supports an exact output size. A 16:9 overall canvas would change the individual shots' proportions. Do not add black padding or crop the approved views to force it.

The tool input is the verified Blender reflective-metal sheet v005, supplied as a self-contained clean appearance reference. It is not an unseen Weavy-generated tool sheet. The rock input is the third photograph you supplied, not the earlier generated granular-rock plate. The prompt borrows that photograph's structure but specifies dark earthy brown/umber instead of orange.

## Shot order

| Position | Native frame | Frozen moment |
| --- | --- | --- |
| Top-left | 241 | Opening wide |
| Top-centre | 278 | Camera approaches sensor |
| Top-right | 348 | Cyan outgoing pulse |
| Bottom-left | 358 | Green returning echo |
| Bottom-centre | 480 | Recorded history partially revealed |
| Bottom-right | 528 | Final wide history reveal |

The recorded six-frame selection is copied unchanged in `selection.json`. Existing complete stills and decoded review frames are reused; source mapping and hashes are retained. The package does not change the approved cameras or source Blender files. `style-brief.md` records the current appearance direction separately from the older selection record's proposed finish.

## Backup: individual shots, then assemble

If the node cannot preserve the 8:3 canvas or mixes the six event states, use the six complete prompts in `prompts/individual/`. Each one requests a single 16:9 image. For each run connect:

1. That prompt's matching `stills/` image as Image 1; its filename is in `shot-map.json`.
2. The same `inputs/02-tool-reflective-metal.png` as Image 2.
3. The same `inputs/03-rock-solid-structure.png` as Image 3.

Save the six selected generated results at identical dimensions and assemble them in shot order with `scripts/compose_grid.ps1`. This preserves the 3x2 layout without generative rearrangement. It requires six separate runs; it is a fallback, not an additional required test. The script takes `-ImagePaths` as an ordered array, `-Columns 3` and a new `.png` `-OutputPath`. It does not crop or resize mismatched images.

## Review the result

- Six distinct views, correct order, no clipped content, borders, captions or blank tiles.
- Same instrument across every shot; pristine steel, subtle orderly machining texture and no added handling wear.
- Solid connected brown rock, with believable texture scale in wide and close views.
- No invented seams at the continuous housing transition; genuine sensors, cover boundaries and the source's visible openings remain.
- Cyan outgoing pulse only in shot 3; green echo and the reference's faint traces in shot 4; partial versus full history in shots 5 and 6. First two shots remain clear of graphics.
- Measurement graphics remain restrained overlays; the instrument stays opaque.

`manifest.json` records exact input provenance and hashes. `verification.json` records packaging checks, not successful AI generation. This package and its media are local deliverables; local ZIP creation does not establish an off-machine backup.
