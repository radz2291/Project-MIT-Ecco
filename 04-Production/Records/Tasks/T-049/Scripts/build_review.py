"""Build an image-led review packet from inspected natives and decoded media."""
from pathlib import Path
import json, hashlib, html, os, sys
R=Path(__file__).resolve().parents[5]; T=R/'04-Production/Records/Tasks/T-049'
def read(p):return json.loads((T/p).read_text(encoding='utf-8'))
def write(p,s):(T/p).write_text(s,encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=read('sources.json'); audit=read('Evidence/source-audit.json'); images=read('Evidence/image-manifest.json'); media=read('Evidence/media-audit.json'); comps=read('components.json')
by_image={x['id']:x for x in images}
native={x['id']:x for x in audit}
decision=read('owner-decisions.json')[0]
if '--documents-only' in sys.argv:
    selections=read('Evidence/selection-evidence.json')
else:
    locks=[]; selections=[]; product=[]
    for s in sources:
        d=native[s['id']];p=R/s['native']; locks.append({'id':s['id'],'path':s['native'],'sha256':sha(p),'unchanged_since_inspection':sha(p)==d['sha256']})
        if s.get('acceptance'):
            p=(R/s['acceptance']).resolve();selections.append({'id':s['id'],'path':p.relative_to(R).as_posix(),'sha256':sha(p),'recorded_evidence':p.read_text(encoding='utf-8-sig')})
        raw=read(f"Evidence/{s['id']}_native.json")
        for o in raw['objects']:
            if o['type']=='MESH' and 'housing' in o['name'].lower():
                m=raw['meshes'].get(o['data'],{})
                product.append({'source':s['id'],'object':o['name'],'library':o['library'],'vertices':m.get('vertices'),'geometry_sha256':m.get('geometry_sha256'),'materials':o['materials'],'note':'Datablock inventory, not a count of simultaneously rendered instances. Source mm meshes and consumer metre-scale objects must be distinguished.'})
    write('Evidence/source-lock.json',json.dumps(locks,indent=2));write('Evidence/selection-evidence.json',json.dumps(selections,indent=2));write('Evidence/product-comparison.json',json.dumps(product,indent=2))

intro='''# ECCO-049 — Component selection review

27 October 2026 · **C03/C04 grouping and C07 source recorded; report only** · documentation only

Keep the completed seven-section previs as the visual baseline. The product shape is already consistent: the housing mesh matches the shared source across every section that contains it. The useful selection is mainly which finish, environment and behavior should become reusable later.

**Recommended starting choice:** retain film ECCO v002 and connected BHA v007 as geometry references; use S05 previs v020 as the owner-selected hydraulic source; retain S07's clean satin finish as a proposed appearance reference; keep camera-dependent cutaways, lighting, reveals and data cases local. **Radzi requested that the report propose: combine the well environment and formation into one modular shared environment.** No consolidation or scene migration has begun.

## C03 — owner-requested report proposal

Combine the existing well environment and surrounding formation into one reusable environment master. Give it separate controls for rock, borehole shape, casing, cement, mud and wider earth context, with optional surface context when needed. Casing, cement, channel and wear objects are physical subcomponents of this environment (C04 detail), not a separate peer environment asset. Pulse/response demonstration animation is documented separately from those objects. Scenes select the modules, extent, detail and visibility they need instead of carrying independent overlapping environment builds.

This replaces C03's earlier blanket **keep local** recommendation. Keep each approved scene's camera, lens, timing, motion, local lighting and viewing cutaways while adapting it to the future master. Existing sources remain preserved. The shared master is a later build deliverable; compatibility through each locked shot must be checked before adoption. S03/S06 illustrative data and reconstruction remain separate from the physical environment.

The owner explicitly instructed: report only; do not combine yet. No implementation is authorized. Recorded instruction: [owner-decisions.json](owner-decisions.json).

**C07 hydraulic source selected:** use the approved Section 5 previs v020 amber fluid, cuttings and flow motion. Earlier Hydraulics v003 remains historical comparison. This records the source choice only; no extraction or migration is authorized.

- [Hardware and world comparison](Images/02-hardware-and-world.jpg)
- [Sensing and casing comparison](Images/03-sensing-and-casing.jpg)
- [Flow and data comparison](Images/04-flow-and-data.jpg)
- [All seven sections](Images/01-seven-section-baseline.jpg)
- [Exact image/source index](image-index.md) · [Native sources and acceptance](source-index.md) · [Detailed inventory](inventory.md)

## Component choices and proposals

| Component | Proposed choice | Reason / effect |
|---|---|---|
'''
for c in comps:intro+=f"| {c['id']} — {c['component']} | **{c['choice']}** | {c['reason']} |\n"
intro+='''
## Choices left for joint review

1. Use S07 satin metal as the common appearance reference while keeping per-shot lighting and S04 transparency, or retain all finishes separately?
2. Keep S04's selected v033 look, or scope a later correction for its known dark-band/pit impression? Rejected v034 is not a replacement.

These are pending selections, not permission requests to continue this ticket. No polishing, relinking, rebuilding, retiming or downstream task creation has begun.

## Safe consolidation order — proposal only

1. Record Radzi's selected components and immutable source hashes. Preserve every approved scene/movie and the current camera, lens, motion and event score.
2. Register geometry identities first: ECCO/closures, then connected BHA/bit/joints. Keep local display wrappers distinct from source geometry; do not delete apparent duplicates based on datablock counts.
3. Plan the proposed C03 modular environment: reconcile overlapping rock/casing/cement sources, use one declared axis/unit convention, and provide selectable layers, borehole variants, near/wide extents and detail controls. Preserve existing source versions. Keep approved scene cameras, local lighting/cutaways and data cases intact; migrate only in a later released build after affected-shot checks. S05 v020 is selected as the hydraulic source; extraction or migration still requires a later scoped instruction. Material controls remain pending.
4. Reopen copies through every affected locked camera at entry, exit, reveal, close-up and heaviest frames. Check silhouette, cap origin, bit order, occlusion, finite flow/particle clearance, layer order, world-fixed history, geometry/amplitude separation, seam/colors and neighboring cuts. Compare camera/lens/animation hashes and timing before and after; benchmark complete writes strictly below 5 seconds/frame before a batch.
5. Return those later replacement versions to Radzi. He alone updates film assembly. Keep old consumers unmigrated until their checks pass.

Section allocations currently total **96 seconds** (10/12/18/18/18/12/8). S05's approved 18 seconds supersedes its old 12-second plan. The S02 review movie also contains three seconds reused from S01; do not add that overlap twice. No edit or retiming was performed.
'''
write('comparison.md',intro)

inv='''# ECCO-049 — Actual inventory and consumer ownership

This inventory describes the saved local candidates inspected on 27 October 2026. V3 A/B/C/D names below are editorial aliases for integrated section sequences, not newly segmented or retimed shots. Earlier T42/T45 consumer lists described future use; the following records actual saved libraries and local implementations.

`local` means a local Blender datablock. Blender does not preserve a reliable append history: provenance is recovered from reports and exact mesh matches, not inferred solely from its name. Listed datablocks may be prototypes, source copies or unused retained blocks; counts are not rendered-instance counts. Geometry fingerprints cover raw vertex coordinates and loop topology; they do not certify evaluated modifiers, world-space fit or physical equivalence.

'''
for c in comps:
    label='Owner-selected source; report only' if c['id']=='C07' else ('Report proposal only' if c['id'] in ('C03','C04') else 'Proposal')
    inv+=f"## {c['id']} — {c['component']}\n\n**{label}:** {c['choice']}. **Proposed master/reference:** {c['master']}\n\n**Consumers:** {c['consumers']}\n\n**Observed:** {c['actual']}\n\n**Why / visual impact:** {c['reason']} {c['impact']}\n\n**Limits:** {c['limits']}\n\n**Inspect:** "+' · '.join(f"[{by_image[id]['title']}]({by_image[id]['image']})" for id in c['images'])+'\n\n'
inv+='''## Evidence and interpretation limits

- [Object-level ownership, collections, instance targets, materials and mesh fingerprints](Evidence/component-members.json) is the detailed member map. Categories are keyword aids and may overlap; the human-readable component entries above resolve their meaning.
- [Cross-source geometry matches](Evidence/geometry-matches.json) identifies duplicates without assuming they should be merged. [Housing comparison](Evidence/product-comparison.json) shows the common 348876-vertex housing fingerprint `4d0a0e7868d305fe2d4079c27e6f4e36656e7c71f46842075674e1384257cda6`.
- S04 retains source and display collections with different unit transforms, edges, transparency and viewing windows. Do not mistake raw millimetre mesh extents for evaluated metre dimensions, or merge source/display blocks without checking scene instances and stage visibility.
- S05 retains an ECCO library entry but its object datablocks are local. A library name alone does not prove a live linked consumer. Its extra default Scene/Camera/Cube/Light are retained data, not evidence that the approved production camera changed.
- No unified Measurements/Graphics master was present in the inspected T44–T48 package. S02 acquisition, S03 geometry/amplitude and S06 report data have distinct local implementations and illustrative provenance. No claim that S03 and S06 use the same samples is supported.
- T44 is Done in live Work. T45–T48 remain Review. Their frozen packages are comparison sources; this task does not accept or reopen those tickets. Some old manifests/reports still say integration/acceptance pending; fresh Work controls current status.
- Surface v003, Formation v002, cased Formation v002, World v009, T6 variants v003 and T5 plugged v002 were opened as earlier comparison sources. None is automatically promoted over a completed section.
'''
write('inventory.md',inv)

si='''# ECCO-049 — Exact local sources

Machine root: `C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco`.

Paths below are relative to that root. Heavy native/movie files remain local; the GitHub review branch contains this packet and selected derived stills, not these media files. [Source audit](Evidence/source-audit.json) records exact native/library hashes, saved scene names, ranges, camera/lens fingerprints, images and fonts. [Selection evidence](Evidence/selection-evidence.json) preserves the read approval/closure text and its source hash.

| Section | Selected version | Saved range / delivered frames | Acceptance source |
|---|---|---|---|
'''
versions=['Gentle-10s-Finish','v011 continuation','v036','v033 (v034 rejected)','Camera-Proof v020','polished v004','Sequence v006']
for i,s in enumerate(sources[:7]):
    d=native[s['id']];scene=d['scenes'][0];m=next(x for x in media if x['id']==s['id']);e=next(x for x in selections if x['id']==s['id'])
    si+=f"| {s['id']} | {versions[i]} | {scene['frame_start']}–{scene['frame_end']}; video {m['decoded_frames']}f | `{e['path']}` |\n"
si+='\nS01–S02 use 960×540 Workbench; S03/S05 use 960×540 Eevee; S04/S06/S07 use 1280×720 Eevee, all at 24 fps. S02 native covers S01 and S02 (1–528); its 360-frame review excerpt starts at native 169. Its 97-frame wall-build detail starts at native 432. Current selected videos were decoded and their frames extracted, not regenerated.\n\n'
for s in sources:
    d=native[s['id']];si+=f"## {s['id']}\n\nNative: `{s['native']}`\n\nSHA256: `{d['sha256']}`\n\n"
    if s.get('video'):si+=f"Movie: `{s['video']}`\n\n"
    if s.get('detail_video'):si+=f"Detail movie: `{s['detail_video']}`\n\n"
    libs=[Path(l['resolved']).resolve().relative_to(R).as_posix() for l in d['libraries']]
    si+='Saved libraries: '+('; '.join(f'`{x}`' for x in libs) if libs else 'none')+'.\n\n'
si+='''## Recovery and access

S04 closure records C-native hash identity to the original delivery and a separately relinked D-native; only the movies are byte-identical. S05/S06/S07 closure records describe same-machine D recovery. S01/S02/S03 records do not establish off-machine media backup. Recovery copies were not re-audited in this task, and no new backup/upload is claimed. Exact selected C sources and dependencies were checked live.

The running Blender session contained unsaved changes in Acoustics_v003. Only read-only official MCP queries were used there. Inspection used separate Blender 5.2.2 background processes with auto-execution disabled, no save and no rendering. The unsaved live state is not the frozen shared master.
'''
write('source-index.md',si)

ix='''# ECCO-049 — Image index

All pictures are actual decoded selected movie frames or existing Blender review renders. No generated comparison art or diagnostic render was created. Images are reduced JPEG derivatives; source hashes and exact movie/native frame references are in [image-manifest.json](Evidence/image-manifest.json). Different cameras are deliberately labeled; these sheets are not same-scale engineering comparisons.

| Comparison sheet | Purpose |
|---|---|
| [Seven-section baseline](Images/01-seven-section-baseline.jpg) | Three frames from each selected section |
| [Hardware and world](Images/02-hardware-and-world.jpg) | Earlier connected assembly versus current product, environment and finish |
| [Sensing and casing](Images/03-sensing-and-casing.jpg) | Earlier packet/layer proofs versus current acquisition and S04 display |
| [Flow and data](Images/04-flow-and-data.jpg) | Sparse prior flow versus current amber; separate S03/S06 information cases |

## Individual images

'''
for x in images:ix+=f"- [{x['title']}]({x['image']}) — source `{x['source']}`; "+(f"movie frame {x['video_frame_1based']}, native frame {x['native_frame']}." if 'video_frame_1based' in x else 'existing selected still; exact saved view below.')+f" Native: `{x['native']}`.\n"
ix+='''
The three T46 phase stills are selected report aliases from Sensing_reuse_A_v009; their originating report/manifest provides send/contact/return correspondence rather than embedding frame numbers in the alias filenames. T47 layer/wear f1 stills correspond to the separate LayerSection/WearSection v011 inspection natives, not to the reusable layer master by itself. Every displayed image's source and native path exists locally; no fresh pixel-match render is claimed.
'''
write('image-index.md',ix)

E=html.escape
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ECCO-049 — Component review</title><style>
body{margin:0;background:#101820;color:#e4edf2;font:16px/1.5 system-ui,sans-serif}main{max-width:1280px;margin:auto;padding:28px}h1{font-size:32px;line-height:1.2}h2{margin-top:48px}p{max-width:920px}a{color:#8bdaea}nav{display:flex;gap:18px;flex-wrap:wrap;padding:14px 0}.tag{color:#f5cc80}section{border-top:1px solid #35414b;margin-top:28px;padding-top:10px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,360px),1fr));gap:16px}figure{margin:0;background:#19252f;border:1px solid #344652}img{width:100%;display:block}figcaption{padding:10px;font-size:14px}.note{color:#b4c8d3}summary{cursor:pointer;color:#a0ddec}code{overflow-wrap:anywhere}td,th{text-align:left;vertical-align:top;padding:9px;border-bottom:1px solid #35414b}table{width:100%;border-collapse:collapse}button{padding:8px} @media print{body{background:white;color:black}a{color:#075366}section{break-inside:avoid}}
</style><main><p class="tag">ECCO-049 · 27 October 2026 · C03/C04 grouping and C07 source recorded; report only</p><h1>Keep the shots. Choose what becomes shared.</h1><p>The completed previs is the baseline. The housing shape matches across the inspected sources. The useful differences are the finish, environment, explanatory views and behavior. No scenes have been edited.</p><nav><a href="comparison.md">Short proposal</a><a href="inventory.md">Inventory</a><a href="source-index.md">Exact sources</a><a href="image-index.md">Image index</a></nav><p class="tag"><b>C03 report proposal:</b> combine the well environment and formation into one modular shared environment, with controls for rock, borehole variants, casing, cement, mud and wider ground context. C04 casing/cement/channel/wear objects belong inside C03; animation demonstrations are separate from the physical asset. Each scene uses the parts it needs while preserving its approved camera, motion, lighting and cutaways.</p><p class="tag"><b>C07 hydraulic source selected:</b> Section 5 previs v020. Use its approved amber flow, cuttings and motion; the earlier Hydraulics v003 demo is historical comparison. Source selection only: no extraction or migration is authorized.</p><p class="note">C03 replaces the earlier keep-local recommendation. Other component choices remain proposals. No environment build or scene migration is authorized; original native scenes remain preserved.</p><h2>Component choices and proposals</h2><table><tr><th>Component</th><th>Choice</th></tr>'''
for c in comps:page+=f'<tr><td><a href="#{c["id"]}">{E(c["component"])}</a></td><td>{E(c["choice"])}</td></tr>'
page+='</table>'
for c in comps:
    label='Owner-selected source; report only' if c['id']=='C07' else ('Report proposal only' if c['id'] in ('C03','C04') else 'Proposal')
    page+=f'<section id="{c["id"]}"><h2>{c["id"]} · {E(c["component"])}</h2><p class="tag">{label}: {E(c["choice"])}</p><p>{E(c["reason"])}</p><div class="grid">'
    for id in c['images']:
        x=by_image[id];page+=f'<figure><a href="{x["image"]}"><img loading="lazy" src="{x["image"]}" alt="{E(x["title"])}"></a><figcaption>{E(x["title"])}<details><summary>Exact source</summary><p><code>{E(x["source"])}</code></p><p>Native: <code>{E(x["native"])}</code></p></details></figcaption></figure>'
    page+=f'</div><p><b>Observed:</b> {E(c["actual"])}</p><p><b>Reference:</b> {E(c["master"])}</p><p class="note">{E(c["limits"])}</p></section>'
page+='''<section><h2>Later consolidation</h2><p>Record selections → freeze geometry identities → extract only chosen material/effect controls → compare copies through locked cameras and motion → benchmark below 5 seconds/frame → return new versions for Radzi review.</p><p>Current section allocations total 96 seconds. Radzi owns timing, logo, audio and film assembly. Heavy native/video files remain local. This packet contains actual review imagery and inspected records.</p></section></main></html>'''
write('review.html',page)
print('Built review, comparison, inventory, source index, image index and evidence')
