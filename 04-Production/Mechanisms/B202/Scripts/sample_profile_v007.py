"""Pure-Python wall lookup for T27. Values are illustrative scene geometry.

Return a world-fixed (source X metres) point, interpolated from saved T6/tight
mesh samples. Does not fire sensors, animate, correct eccentricity, or infer TOF.
"""
import json,math,bisect
from pathlib import Path
def load_tables(path=None):
    path=path or Path(__file__).resolve().parents[1]/'sampling_tables_v007.json'
    return json.loads(Path(path).read_text())
def sample_wall(table,profile,x,azimuth):
    rows={}
    for v in table[profile]['vertices']:rows.setdefault(v[0],[]).append(v)
    depths=sorted(rows)
    if not depths[0]<=x<=depths[-1]:raise ValueError('Outside retained source extent')
    idx=bisect.bisect_left(depths,x);lo=depths[max(0,idx-1)];hi=depths[min(idx,len(depths)-1)]
    def ring(depth):
        pts=sorted(rows[depth],key=lambda p:math.atan2(p[2],p[1])%math.tau)
        angles=[math.atan2(p[2],p[1])%math.tau for p in pts];a=azimuth%math.tau;j=bisect.bisect_right(angles,a)
        p=pts[(j-1)%len(pts)];q=pts[j%len(pts)];u=angles[(j-1)%len(pts)];v=angles[j%len(pts)]
        if j==0:u-=math.tau
        if j==len(pts):v+=math.tau
        t=(a-u)/(v-u)
        return tuple((1-t)*c+t*d for c,d in zip(p,q))
    a=ring(lo);b=ring(hi);t=0 if hi==lo else (x-lo)/(hi-lo)
    return (x,(1-t)*a[1]+t*b[1],(1-t)*a[2]+t*b[2])
