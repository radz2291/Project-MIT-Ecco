import bpy,json,hashlib,math,struct
from pathlib import Path
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[4];BASE=ROOT/'04-Production/Mechanisms/B202';E=ROOT/'04-Production/Records/Tasks/T-008/Evidence'
build=json.loads((E/'build_v005.json').read_text());checks=[]
def check(name,value):
    checks.append({'check':name,'pass':bool(value)})
def signature(me):
    h=hashlib.sha256()
    for v in me.vertices:h.update(struct.pack('<3f',*v.co))
    for p in me.polygons:h.update(struct.pack('<I',len(p.vertices)));h.update(struct.pack('<'+'I'*len(p.vertices),*p.vertices))
    return h.hexdigest()
outputs=[]
for key in 'ABC':
    path=BASE/f'Scenes/B202_study_{key}_v005.blend';bpy.ops.wm.open_mainfile(filepath=str(path));s=bpy.context.scene
    check(key+' key-state',s['B202_key_state']==key)
    check(key+' camera',tuple(s.camera.location)==tuple(Vector(next(x for x in build['candidates'] if x['key']==key)['camera'])))
    libs=[{'path':l.filepath,'exists':Path(bpy.path.abspath(l.filepath)).exists()} for l in bpy.data.libraries]
    check(key+' relative linked sources',len(libs)>0 and all(l['exists'] and l['path'].startswith('//') for l in libs))
    pres=[o for o in s.objects if o.name.startswith('PRESENTATION_')]
    check(key+' source housing and nine closures',len(pres)==10)
    for o in pres:
        original=bpy.data.objects[o['source_object']]
        check(key+' unchanged mesh '+original.name,signature(o.data)==signature(original.data))
    hero=bpy.data.objects['Wall-registered section 03'];pts=[Vector(p.co[:3]) for p in hero.data.splines[0].points]
    check(key+' contour on sensor plane',all(abs(p.x-2.73)<1e-6 for p in pts))
    projections=[world_to_camera_view(s,s.camera,p) for p in pts]
    check(key+' contour inside image',all(.01<p.x<.99 and .01<p.y<.99 and p.z>0 for p in projections))
    refs=[bpy.data.objects[f'ECCO_SENSOR_REF_{i:02d}'].location for i in range(1,4)]
    angles=sorted(math.atan2(v.z,v.y) for v in refs)
    check(key+' common sensor plane',max(p.x for p in refs)-min(p.x for p in refs)<1e-6)
    check(key+' 120deg source references',all(abs((angles[(i+1)%3]-angles[i])%math.tau-math.tau/3)<1e-5 for i in range(3)))
    check(key+' no new animation',not any(o.animation_data for o in s.objects))
    image_path=BASE/f'Previews/Study_v005/B202_{key}_v005.png';im=bpy.data.images.load(str(image_path));check(key+' image size',tuple(im.size)==(960,540))
    check(key+' distinct visible image',max(im.pixels[:])-min(im.pixels[:])>.2)
    for p in (path,image_path):outputs.append({'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
for p,h in build['source_hashes'].items():check('source unchanged '+p,hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h)
result={'checks':checks,'passed':sum(c['pass'] for c in checks),'total':len(checks),'outputs':outputs,'source_hashes':build['source_hashes'],'limits':'Implementation self-checks; not independent engineering validation. Contour projection checks do not establish occlusion/readability or motion.'}
(E/'verification_v005.json').write_text(json.dumps(result,indent=2))
print(json.dumps({'passed':result['passed'],'total':result['total'],'failures':[c for c in checks if not c['pass']]}))
assert all(c['pass'] for c in checks)
