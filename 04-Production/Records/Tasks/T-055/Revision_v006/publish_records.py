"""Current catalog and version-history housekeeping for the approved revision scope."""
from pathlib import Path
import json,hashlib,shutil
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');S=R/'04-Production/Shared';A=S/'Assets';T=R/'04-Production/Records/Tasks/T-055/Revision_v006'
def write(p,text):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text.rstrip()+'\n',encoding='utf-8',newline='\n')
def replace(p,pairs):
    text=p.read_text(encoding='utf-8')
    for old,new in pairs:text=text.replace(old,new)
    write(p,text)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (T/'archive-moves.json').exists(),'One-time release already applied; inspect saved records instead of repeating.'
assert json.loads((T/'independent-verification-final.json').read_text())['pass']
assert json.loads((T/'benchmark.json').read_text())['pass']
assert json.loads((T/'motion.json').read_text())['pass']
moves=[]
for old,new in [
    (A/'Environment/Surface/Surface_descent_v005.blend',S/'Archive/2026-10-31/Assets/Surface/Surface_descent_v005.blend'),
    (S/'Demos/Surface_demo_v001.blend',S/'Archive/2026-10-31/Demos/Surface_demo_v001.blend'),
    (S/'Demos/World_demo_v001.blend',S/'Archive/2026-10-31/Demos/World_demo_v001.blend')]:
    if not old.exists():continue
    assert old.resolve().is_relative_to(S.resolve()) and new.resolve().is_relative_to(S.resolve())
    assert not new.exists(),str(new);before=sha(old);new.parent.mkdir(parents=True,exist_ok=True);shutil.move(str(old),str(new));assert sha(new)==before
    moves.append({'old':old.relative_to(R).as_posix(),'new':new.relative_to(R).as_posix(),'sha256':before})
for folder,stem in [(A/'Environment/Surface','Surface_descent_v006'),(A/'Environment/Borehole','World_environment_v011')]:
    p=folder/(stem+'.blend1')
    if p.exists():
        q=T/'Build-backups'/p.name;q.parent.mkdir(exist_ok=True);shutil.move(str(p),str(q))
write(T/'archive-moves.json',json.dumps(moves,indent=2))
replace(A/'README.md',[
    ('Reorganized31October2026.','Updated 31 October 2026.'),
    ('World_environment_v010.blend','World_environment_v011.blend'),
    ('World_demo_v001.blend','World_demo_v002.blend'),
    ('Surface_descent_v005.blend','Surface_descent_v006.blend'),
    ('Surface_demo_v001.blend','Surface_descent_demo_v002.blend')])
with (A/'README.md').open('a',encoding='utf-8') as f:
    f.write('\nSurface v006 owns equipment and ocean. World v011 owns regional geology and the existing S02 wall. The connected Surface demo shows both. World v010 remains active for explicitly pinned existing Digital and other consumers; they were not upgraded.\n')
write(A/'Environment/Surface/README.md','''# Surface — v006

Shared master: `Surface_descent_v006.blend`. Equipment and ocean only; all geology belongs to World v011.

- `SURFACE_RIG_SUBSEA_v004`: retained rig, riser and subsea equipment.
- `SURFACE_OCEAN_FULL`: complete sea surface for the moving descent.
- `SURFACE_OCEAN_CUTAWAY`: alternative half-sea for explanatory inspection; select one ocean only.
- Mean sea Z=0m, pontoons Z=-20..-14m, deck Z=10.5..13.5m, seabed Z=-120m. Illustrative scene dimensions.

Connected demo: `04-Production/Shared/Demos/Surface_descent_demo_v002.blend`. Scene dropdown provides the continuous S01-S02 reference, waterline, water column and regional geology views. Cameras, data and animation belong to the demo, never this master. The inherited subsea viewing opening is illustrative, not certified internal equipment.

Previous v005 and its old demo are preserved in Shared/Archive/2026-10-31, with historical links untouched. New native acceptance remains with Radzi.
''')
write(A/'Environment/Borehole/README.md','''# World — v011 with pinned v010 retained

`World_environment_v011.blend` adds seven illustrative regional geological units to the exact existing v010 physical variants. No measured stratigraphic log is claimed.

- `WORLD_DESCENT_CONNECTED`: regional geology plus exactly one existing S02 destination wall. Use alone for the connected descent.
- `WORLD_REGIONAL_DESCENT`: regional mass only, reserving the S02 local interval. Do not add a second destination wall when using the connected collection.
- All v010 physical collection names, mesh geometry, shape keys and transforms are retained. Cameras, lights and section measurement/history animation are excluded.
- `World_interface_v011.json` and `Scripts/world_interface_v011.py` provide selection and placement. Canonical axis X remains; `canonical_to_s02` maps to the descent's vertical Z.
- Illustrative sea/seabed at source Z=0/-120m; regional formation extends to -1020m with180m outer radius. The existing local S02 bore shape is unchanged.

Focused borehole demo: `04-Production/Shared/Demos/World_demo_v002.blend`. Connected surface-to-wall demo: `04-Production/Shared/Demos/Surface_descent_demo_v002.blend`.

World v010 and its interface/helper remain active and byte-exact for the accepted Digital v004 derivation and other pinned consumers. This revision does not automatically upgrade those assets or historical shot files. Final appearance/native acceptance remains with Radzi.
''')
write(S/'Demos/README.md','''# Shared asset demos

Six current demos link their shared masters. Use the scene dropdown for alternate inspection views. The connected Surface demo owns its camera/timeline and existing local measurement/history; reusable masters contain no complete section scenes.

- Hardware_demo_v001.blend
- World_demo_v002.blend
- Surface_descent_demo_v002.blend — connected S01-S02, waterline, water column and regional geology
- Digital_environment_demo_v005.blend — remains pinned to accepted World v010 derivation
- Measurement_reveal_demo_v002.blend
- Waveform_demo_v015.blend

Surface/World review previews use Workbench for geometry and continuity inspection. They do not establish final film lighting, sea shading or geological provenance. Previous demo versions are archived without link maintenance.
''')
write(S/'README.md','''# Shared production library

- Assets: focused reusable components under Hardware, Environment and Effects.
- Demos: six linked review files. The connected Surface demo owns its S01-S02 reference timeline; shared masters contain no complete section scenes.
- Sources: supplied originals and provenance.
- Archive/2026-10-31: preserved prior versions, experiments and backups; historical links are not maintained.

Start with Assets/README.md. No production shot was automatically upgraded by the surface/World revision. Heavy native/media files remain local.
''')
replace(R/'04-Production/Records/Tasks/T-051/write_shared_catalog.py',[
    ('World_environment_v010.blend','World_environment_v011.blend'),('World_demo_v001.blend','World_demo_v002.blend'),
    ('Surface_descent_v005.blend','Surface_descent_v006.blend'),('Surface_demo_v001.blend','Surface_descent_demo_v002.blend'),
    ('Surface/subsea assembly and earth source.','Surface/subsea equipment and ocean; regional geology belongs to World v011.'),
    ('World_interface_v010.json describes coordinates/selection.','World_interface_v011.json describes coordinates/selection. World v010 remains pinned for accepted Digital and existing consumers.')])
for p,notice in [
    (R/'04-Production/Records/Tasks/T-051/report.md','Current surface/World revision: [31 October v006 review](../T-055/Revision_v006/report.md). Surface v006, World v011 and connected demo v002 supersede the surface/continuity package descriptions below. Pinned World v010 consumers remain unchanged.'),
    (R/'04-Production/Records/Tasks/T-055/report.md','Current revision: [Surface v006 / World v011](Revision_v006/report.md), authorized by Radzi on31October2026. Earlier implementation history below is retained; current paths are in the new review record.')]:
    txt=p.read_text(encoding='utf-8');a,b=txt.split('\n',1);write(p,a+'\n\n'+notice+'\n'+b)
paths=[A/'Environment/Surface/Surface_descent_v006.blend',A/'Environment/Borehole/World_environment_v011.blend',A/'Environment/Borehole/World_environment_v010.blend',S/'Demos/Surface_descent_demo_v002.blend',S/'Demos/World_demo_v002.blend',T/'Previews/Surface-to-wall_v006.mp4']
write(T/'artifact-manifest.json',json.dumps([{'path':p.relative_to(R).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p),'storage':'local only'} for p in paths],indent=2))
