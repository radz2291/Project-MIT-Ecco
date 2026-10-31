"""Owner-authorized shared filesystem migration. Plan first; sole writer is master."""
from pathlib import Path
import json,hashlib,shutil,os
R=Path('C:/Users/RZ1/Desktop/RZ/261013-MIT-Ecco');S=R/'04-Production/Shared';A=S/'Assets';T=R/'04-Production/Records/Tasks/T-051/Reorganization';T.mkdir(parents=True,exist_ok=True)
ACTIVE={
 'ECCO/ECCO_film_v003.blend':'Hardware/ECCO/ECCO_film_v003.blend',
 'ECCO/Satin_finish_v001.blend':'Hardware/ECCO/Dependencies/Satin_finish_v001.blend',
 'BHA/BHA_film_v008.blend':'Hardware/BHA/BHA_film_v008.blend',
 'BHA/BHA_core_satin_v001.blend':'Hardware/BHA/Dependencies/BHA_core_satin_v001.blend',
 'WellAssembly/World_environment_v010.blend':'Environment/Borehole/World_environment_v010.blend',
 'WellAssembly/World_interface_v010.json':'Environment/Borehole/World_interface_v010.json',
 'WellAssembly/Scripts/world_interface_v010.py':'Environment/Borehole/Scripts/world_interface_v010.py',
 'WellAssembly/WellAssembly_variants_v003.blend':'Environment/Borehole/Dependencies/WellAssembly_variants_v003.blend',
 'WellAssembly/config_authorized_v003.json':'Environment/Borehole/Dependencies/config_authorized_v003.json',
 'WellAssembly/Scripts/compatibility_v001.py':'Environment/Borehole/Scripts/compatibility_v001.py',
 'Formation/Formation_context_v002.blend':'Environment/Borehole/Dependencies/Formation_context_v002.blend',
 'Formation/Formation_cased-section_v002.blend':'Environment/Borehole/Dependencies/Formation_cased-section_v002.blend',
 'CasedHole/CasedHole_v002.blend':'Environment/Borehole/Dependencies/CasedHole_v002.blend',
 'CasedHole/Scripts/cased_controls_v001.py':'Environment/Borehole/Scripts/cased_controls_v001.py',
 'CasedHole/Scripts/integrate_cased_v001.py':'Environment/Borehole/Scripts/integrate_cased_v001.py',
 'World/Scripts/formation_controls_v004.py':'Environment/Borehole/Scripts/formation_controls_v004.py',
 'World/Scripts/formation_controls_v003.py':'Environment/Borehole/Scripts/formation_controls_v003.py',
 'World/Scripts/world_controls.py':'Environment/Borehole/Scripts/world_controls.py',
 'World/Scripts/continuation_controls_v001.py':'Environment/Borehole/Scripts/continuation_controls_v001.py',
 'Surface/Surface_descent_v005.blend':'Environment/Surface/Surface_descent_v005.blend',
 'DigitalEnvironment/Digital_context_lines_v004.blend':'Effects/DigitalEnvironment/Digital_context_lines_v004.blend',
 'DigitalEnvironment/Digital_style_v001.blend':'Effects/DigitalEnvironment/Dependencies/Digital_style_v001.blend',
 'DigitalEnvironment/Digital_world_v001.blend':'Effects/DigitalEnvironment/Dependencies/Digital_world_v001.blend',
 'DigitalEnvironment/check_context_derivation_v004.py':'Effects/DigitalEnvironment/Scripts/check_context_derivation_v004.py',
 'DigitalEnvironment/Scripts/regenerate_context_lines.py':'Effects/DigitalEnvironment/Scripts/regenerate_context_lines.py',
 'DigitalEnvironment/CONTEXT_LINES_v004.md':'Effects/DigitalEnvironment/CONTEXT_LINES_v004.md',
 'MeasurementReveal/Measurement_reveal_v001.blend':'Effects/MeasurementReveal/Measurement_reveal_v001.blend',
 'Hydraulics/Hydraulics_v003.blend':'Effects/Hydraulics/Hydraulics_v003.blend',
 'Hydraulics/Scripts/hydraulics_controls_v001.py':'Effects/Hydraulics/Scripts/hydraulics_controls_v001.py',
 'Acoustics/Waveform_shared_v015/Waveform_shared_v015.blend':'Effects/Waveform/Waveform_shared_v015.blend',
}
DEMOS={
 'T-052/Demos/Hardware_demo_v001.blend':'Hardware_demo_v001.blend',
 'T-051/Demos/World_demo_v001.blend':'World_demo_v001.blend',
 'T-051/Demos/Surface_demo_v001.blend':'Surface_demo_v001.blend',
 'T-054/Demos/Digital_environment_demo_v005.blend':'Digital_environment_demo_v005.blend',
 'T-054/Demos/Measurement_reveal_demo_v002.blend':'Measurement_reveal_demo_v002.blend',
 'T-056/Demos/Waveform_demo_v015.blend':'Waveform_demo_v015.blend',
}
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def plan():
 rows=[]
 for p in sorted(A.rglob('*')):
  if not p.is_file():continue
  rel=p.relative_to(A).as_posix()
  if rel in ACTIVE:dst=A/ACTIVE[rel];kind='active'
  elif rel.startswith('ECCO/Originals/'):dst=S/'Sources/ECCO'/rel.removeprefix('ECCO/Originals/');kind='source'
  elif rel.startswith('Surface/Originals/'):dst=S/'Sources/Surface'/rel.removeprefix('Surface/Originals/');kind='source'
  else:dst=S/'Archive/2026-10-31/Assets'/rel;kind='archive'
  assert dst.resolve().is_relative_to(S.resolve()) and not dst.exists(),str(dst)
  rows.append({'old':p.relative_to(R).as_posix(),'new':dst.relative_to(R).as_posix(),'kind':kind,'bytes':p.stat().st_size,'sha256':sha(p)})
 for old,new in DEMOS.items():
  p=R/'04-Production/Records/Tasks'/old;dst=S/'Demos'/new;assert p.exists() and not dst.exists()
  rows.append({'old':p.relative_to(R).as_posix(),'new':dst.relative_to(R).as_posix(),'kind':'demo','bytes':p.stat().st_size,'sha256':sha(p)})
 assert len(set(x['new'] for x in rows))==len(rows)
 (T/'move-plan.json').write_text(json.dumps(rows,indent=2));print(json.dumps({'files':len(rows),'counts':{k:sum(x['kind']==k for x in rows) for k in ['active','archive','source','demo']},'bytes':sum(x['bytes'] for x in rows)}))
def move():
 rows=json.loads((T/'move-plan.json').read_text());done=[]
 for x in rows:
  p=R/x['old'];dst=R/x['new'];assert p.resolve().is_relative_to(R.resolve()) and dst.resolve().is_relative_to(S.resolve())
  assert p.exists() and sha(p)==x['sha256'] and not dst.exists(),x['old'];dst.parent.mkdir(parents=True,exist_ok=True);p.rename(dst);assert sha(dst)==x['sha256'];done.append(x)
  (T/'moves-completed.json').write_text(json.dumps(done,indent=2))
 # Only empty directories in the enumerated old asset tree; never recursive removal.
 for p in sorted(A.rglob('*'),key=lambda p:len(p.parts),reverse=True):
  if p.is_dir() and not any(p.iterdir()):p.rmdir()
 print('MOVED',len(done))
if __name__=='__main__':
 import sys
 {'plan':plan,'move':move}[sys.argv[-1]]()
