"""Pure dimensional checks and source/provenance packet; no invented deployment."""
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
sys.dont_write_bytecode=True

ROOT=Path(__file__).resolve().parents[4]
TASK=ROOT/'Records/Tasks/T-006'
ASSET=ROOT/'Shared/Assets/WellAssembly'
REPO=ROOT.parent
spec=importlib.util.spec_from_file_location('compatibility',ASSET/'Scripts/compatibility_v001.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
evidence=json.loads((ROOT/'Records/Tasks/T-005/Evidence/build-evidence_v001.json').read_text())
# The independent Blender inspection supplies current v001 radial measurement.
inspection=json.loads((TASK/'Evidence/product-inspection_v001.json').read_text())
od=inspection['maximum_axis_diameter_m']
assert abs(od-.3048)<1e-6
assert abs(m.radial_clearance(.3048,12.3*m.INCH)-.00381)<1e-12
assert m.radial_clearance(od,8.5*m.INCH)<0
assert m.radial_clearance(od,9.625*m.INCH)<0
assert m.radial_clearance(od,7*m.INCH)<0
assert m.radial_clearance(od,12.3*m.INCH,.004)<0
bad_values=[(float('nan'),.4,0),(.3,.4,-1),(0,.4,0),(.3,float('inf'),0)]
for values in bad_values:
    try: m.radial_clearance(*values)
    except ValueError: pass
    else: raise AssertionError(values)
pending=json.loads((ASSET/'config_pending_v001.json').read_text())
gate=m.validate_config(pending,od)
assert not gate['ready'] and gate['clearances_m']=={}
for p in (ASSET/'Scripts').glob('*.py'):
    compile(p.read_text(),str(p),'exec')
pdf=REPO/'01-Brief/ECCO_ENP3_Datasheet-1.pdf'
pages=[p.extract_text() for p in PdfReader(pdf).pages]
(TASK/'Evidence/datasheet-text_v001.txt').write_text('\n\n'.join(f'PAGE {i+1}\n{t}' for i,t in enumerate(pages)),encoding='utf-8')
study=m.brief_fit_study(od)
result={'status':'independent preparation only; O05/BL02 blocks assembly construction',
        'tool_source':inspection,'fit_study':study,'pending_config_gate':gate,
        'checks':{'source_od_matches_12in':True,'unit_conversion':True,
                  'smaller_examples_rejected':True,'eccentric_contact_rejected':True,
                  'invalid_numeric_values_rejected':True,'missing_config_rejected':True,
                  'builder_syntax':True,'builder_scene_validation':False},
        'limit':'Centered straight envelope calculation only; no selected deployment, threads, shoe, deviation, BHA or replacement acceptance'}
(TASK/'Evidence/compatibility-checks_v001.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
# A source-based comparison image; no casing wall or invented cement thickness.
im=Image.new('RGB',(1440,900),'#101823');d=ImageDraw.Draw(im)
fontpath=Path('C:/Windows/Fonts/arial.ttf')
def f(s):return ImageFont.truetype(str(fontpath),s)
d.text((50,35),'T6 / ENP3 fit limits',font=f(36),fill='white')
d.text((50,90),'Source-based compatibility study - deployment configuration remains open',font=f(22),fill='#b9c7d5')
scale=1.5 # pixels per millimetre; both circles to same scale
cx,cy=320,420
rt=od*1000/2*scale;rc=12.3*m.INCH*1000/2*scale
d.ellipse((cx-rc,cy-rc,cx+rc,cy+rc),outline='#68cad1',width=3)
d.ellipse((cx-rt,cy-rt,cx+rt,cy+rt),fill='#596879',outline='#c4ced9',width=2)
d.text((190,390),'Inspected tool envelope',font=f(22),fill='white')
d.text((220,425),f'{od*1000:.3f} mm OD',font=f(22),fill='white')
d.text((80,690),'312.420 mm published minimum casing ID',font=f(22),fill='#68cad1')
d.text((80,725),f'{(12.3*m.INCH-od)*500:.3f} mm ideal centered radial gap',font=f(22),fill='white')
d.text((80,760),'Circle is the inner limit only; no wall thickness selected.',font=f(18),fill='#b9c7d5')
y=190
for s in study:
    gap=s['ideal_radial_gap_or_upper_bound_m']*1000
    d.text((640,y),f"{s['diameter_inches']:g} in {s['dimension_type']} / {gap:+.3f} mm radial gap" ,font=f(25),fill='#68cad1' if gap>0 else '#f0a795')
    d.text((640,y+37),s['source'],font=f(19),fill='white')
    # Manually wrap long notes to keep clear margins.
    import textwrap
    for k,line in enumerate(textwrap.wrap(s['disposition'],66)):
        d.text((640,y+65+k*23),line,font=f(18),fill='#b9c7d5')
    y+=122
d.text((50,845),'Not a complete BHA fit check. OD-only casing examples are upper bounds on possible clearance.',font=f(20),fill='#b9c7d5')
(TASK/'Previews').mkdir(exist_ok=True)
im.save(TASK/'Previews/compatibility-study_v001.png')
paths=[p for p in ASSET.rglob('*') if p.is_file()]+[p for p in TASK.rglob('*') if p.is_file() and p.name!='output-manifest_v001.json']
manifest=[{'path':str(p.relative_to(REPO)).replace('\\','/'),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths]
(TASK/'Evidence/output-manifest_v001.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(result['checks'],indent=2))
