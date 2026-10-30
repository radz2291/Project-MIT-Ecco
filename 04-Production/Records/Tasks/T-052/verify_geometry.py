import bpy,json,hashlib,struct
from pathlib import Path
R=Path(__file__).resolve().parents[4];T=Path(__file__).resolve().parent;A=R/'04-Production/Shared/Assets'
def snapshot(path):
    bpy.ops.wm.open_mainfile(filepath=str(path));out={}
    for o in bpy.data.objects:
        d={'type':o.type,'parent':o.parent.name if o.parent else None,'location':list(o.location),'rotation':list(o.rotation_euler),'scale':list(o.scale)}
        if o.type=='MESH':
            h=hashlib.sha256()
            for v in o.data.vertices:h.update(struct.pack('fff',*v.co))
            for p in o.data.polygons:h.update(struct.pack('I'*len(p.vertices),*p.vertices))
            d['geometry_sha256']=h.hexdigest()
        out[o.name]=d
    return out
records=[]
for old,new in [('ECCO/ECCO_film_v002.blend','ECCO/ECCO_film_v003.blend'),('BHA/BHA_film_v006.blend','BHA/BHA_core_satin_v001.blend'),('BHA/BHA_film_v007.blend','BHA/BHA_film_v008.blend')]:
    a=snapshot(A/old);b=snapshot(A/new);records.append({'baseline':old,'candidate':new,'equal':a==b,'baseline_count':len(a),'candidate_count':len(b),'differences':[k for k in a.keys()|b.keys() if a.get(k)!=b.get(k)]})
(T/'Evidence/geometry-preservation.json').write_text(json.dumps(records,indent=2));print(records)
