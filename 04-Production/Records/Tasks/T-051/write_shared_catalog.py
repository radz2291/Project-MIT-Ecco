from pathlib import Path
import json,os,hashlib,re
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');S=R/'04-Production/Shared';A=S/'Assets';T=R/'04-Production/Records/Tasks/T-051/Reorganization'
items=[
 ('ECCO','Hardware/ECCO/ECCO_film_v003.blend','Hardware_demo_v001.blend','Current ECCO geometry and linked satin finish. Temporary closures and source geometry limits remain as documented.'),
 ('BHA','Hardware/BHA/BHA_film_v008.blend','Hardware_demo_v001.blend','Connected assembly. UPHOLE_CONTINUATION_CONTROL exposes length_m and show; the required satin core is in Dependencies.'),
 ('Borehole','Environment/Borehole/World_environment_v010.blend','World_demo_v001.blend','Physical World variants and cutaways. World_interface_v010.json describes coordinates/selection. Dependencies contains casing, formation and provisional assembly modules. Scripts provides the current physical selection, compatibility and casing interfaces. Old World assembly APIs are archived without further link maintenance.'),
 ('Surface','Environment/Surface/Surface_descent_v005.blend','Surface_demo_v001.blend','Surface/subsea assembly and earth source. The illustrative axial viewing opening is preserved. Demo scene selector provides assembly overview and subsea detail.'),
 ('Waveform','Effects/Waveform/Waveform_shared_v015.blend','Waveform_demo_v015.blend','Clean two-object native Geometry Nodes master. Select WF_MASTER_CONTROLS for shared settings and WF_LIVE_FIELD for local overrides/preset. Defaults retain provisionally approved V013 motion. Presets are illustrative, not measured signals.'),
 ('Digital environment','Effects/DigitalEnvironment/Digital_context_lines_v004.blend','Digital_environment_demo_v005.blend','Contextual lines plus supporting style/physical wrapper in Dependencies. Run Scripts/check_context_derivation_v004.py before reuse; regenerate with Scripts/regenerate_context_lines.py after World shape changes. The preserved T054 v003 template is still the documented regeneration input.'),
 ('Measurement reveal','Effects/MeasurementReveal/Measurement_reveal_v001.blend','Measurement_reveal_demo_v002.blend','Link ECCO Stored Surface Reveal v001 and ECCO Fine Surface Style v001. Local receipt/history attributes remain owned by the shot. Demo uses two authored proxy shapes.'),
 ('Hydraulics','Effects/Hydraulics/Hydraulics_v003.blend',None,'Current retained hydraulic library. Scripts/hydraulics_controls_v001.py accepts an explicit library path. Existing Section5 evidence remains the hydraulic demonstration; no new unrelated demo scene was built.')]
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8')
def apply():
 # Update active JSON/MD metadata path references only, with exact pre-edit backups.
 plan=json.loads((T/'move-plan.json').read_text());changes=[]
 for x in plan:
  if (T/'catalog-update.json').exists():continue
  if x['kind']!='active' or Path(x['new']).suffix not in ['.json','.md']:continue
  p=R/x['new'];raw=p.read_bytes();text=raw.decode('utf-8-sig');updated=text
  replacements={}
  for y in sorted(plan,key=lambda y:len(y['old']),reverse=True):
   # Long absolute/repository-relative paths first. Historical records elsewhere stay unchanged.
   replacements[str(R/y['old']).replace('\\','/')]=str(R/y['new']).replace('\\','/')
   replacements[y['old']]=y['new']
   replacements[y['old'].replace('/','\\\\')]=y['new'].replace('/','\\\\')
   old='04-Production/Shared/Assets/'
   if y['old'].startswith(old):replacements[y['old'][len(old):]]=os.path.relpath(R/y['new'],A).replace('\\','/')
  updated=re.sub('|'.join(re.escape(k) for k in sorted(replacements,key=len,reverse=True)),lambda m:replacements[m.group()],text)
  if updated!=text:
   backup=T/'Backup/Metadata'/x['new'];backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(raw);p.write_text(updated.replace('\r\n','\n'),encoding='utf-8',newline='\n');changes.append(x['new'])
 lines=['# Shared production assets — current catalog','','Reorganized31October2026. Open the versioned master for editing; use its separate demo for inspection. Supporting files remain beside the asset in Dependencies or Scripts. Earlier releases and experimental work are preserved outside Assets.','','| Asset | Shared master | Demo |','|---|---|---|']
 for label,master,demo,desc in items:
  link=f'[{Path(master).name}]({master})';dlink=f'[{demo}](../Demos/{demo})' if demo else 'Retained Section5 evidence'
  lines.append(f'| {label} | {link} | {dlink} |')
  folder=(A/master).parent;extra='\n\nSee the embedded Blender README and the demo README for operation. Preserve relative library paths. Final native acceptance remains with Radzi.'
  write(folder/'README.md',f'# {label}\n\nShared master: `{Path(master).name}`.\n\n{desc}\n\n'+(f'Demo: `04-Production/Shared/Demos/{demo}`.' if demo else 'No separate new demo is supplied; retain the existing hydraulic shot evidence.')+extra)
 lines+=['','Archive: `../Archive/2026-10-31/Assets/`. Supplied originals: `../Sources/`. Per owner direction, archived files and historical scene links were not repaired or validated. This delivery maintains active assets and demos only.','','The migration map and verification are in `Records/Tasks/T-051/Reorganization/`. Blender/video files remain local; no new off-machine backup is claimed.']
 write(A/'README.md','\n'.join(lines))
 write(S/'README.md','# Shared production library\n\n- Assets: active reusable components under Hardware, Environment and Effects.\n- Demos: six linked inspection scenes, with no full section timelines.\n- Sources: supplied original files and provenance.\n- Archive/2026-10-31: previous releases, experiments, legacy scripts and backups; still referenced where needed.\n\nStart with Assets/README.md. No historical shot was upgraded to a different geometry version during this cleanup.')
 write(S/'Demos/README.md','# Shared asset demos\n\nThese six scenes link the active shared masters. Editing a master and reopening a demo reloads it. Each demo has an embedded README. World/Surface use the scene dropdown for detail and overview. Hardware Workbench is for fast geometry inspection; satin materials remain linked.\n\n'+'\n'.join(f'- {p.name}' for p in sorted((S/'Demos').glob('*.blend'))))
 write(S/'Sources/README.md','# Supplied originals\n\nECCO contains the supplied CAD/imported model, sensor reference and implementation provenance. Surface contains the supplied surface-scene original. Names and source contents are preserved. The duplicate root housing STP is retained in the dated archive; it hashes identically to the canonical ECCO original.')
 write(S/'Archive/2026-10-31/README.md','# Preserved shared-asset history\n\nThe previous Assets tree is retained here except files promoted to active Assets or Sources. This includes prior releases, experiments, generated caches and editor backups. Per owner instruction, archive contents and their links were left untouched; reopening historical scenes may require manual relinking through the migration map.\n\nExact original/new locations and hashes are recorded in T051/Reorganization/move-plan.json. Only active asset/demo references were repaired without resaving scene content. Local rollback data is retained with the task; it is not an off-machine backup.')
 (T/'catalog-update.json').write_text(json.dumps({'metadata_paths_updated':changes,'asset_entries':len(items),'demo_files':6},indent=2))
if __name__=='__main__':apply()
