import math,json,statistics
from pathlib import Path
B=Path(__file__).resolve().parents[1]
out={}
for version in ['v003','v004']:
 rows=json.loads((B.parent/f'Interaction-Proof_{version}/Records/tracks.json').read_text())
 cells=set();radii=[];anglebins=set();upsteps=[]
 for p in rows:
  if p['kind']!='fluid':continue
  for f,(x,y,z) in enumerate(p['heads']):
   if -.1<=z<.8:
    a=(math.atan2(y,x)+math.radians(5)*f/24)%math.tau
    cells.add((int((z+.1)/.1),int(a/(math.tau/12))));anglebins.add(int(a/(math.tau/12)));radii.append(math.hypot(x,y))
  upsteps.extend(b[2]-a[2] for a,b in zip(p['heads'],p['heads'][1:]) if b[2]-a[2]>-.5)
 out[version]={'occupied_10cm_by_30degree_cells':len(cells),'angular_sectors_visited':len(anglebins),'radius_range_m':[min(radii),max(radii)],'minimum_non_reset_upward_frame_step_m':min(upsteps),'cells':sorted(cells)}
out['meaning']='Diagnostic representative marker distribution in the tool reference frame across six seconds, axial range -0.1 to 0.8m. Not a physical flow fraction, uniformity metric, CFD or proof that every fluid parcel is shown.'
(B/'Records/coverage-comparison.json').write_text(json.dumps(out,indent=2))
print(json.dumps({k:{a:b for a,b in v.items() if a!='cells'} if isinstance(v,dict) else v for k,v in out.items()}))
