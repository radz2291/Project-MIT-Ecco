"""Fresh-open structural and motion self-checks for B201."""
import bpy,json,hashlib,math
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[3];R=ROOT/'Records/Tasks/T-007'
E=json.loads((R/'Evidence/build_v004.json').read_text());s=bpy.context.scene
checks=[]
def check(name,condition,details=None):
    checks.append(dict(name=name,pass_=bool(condition),details=details))
check('exact candidate hash',hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest()==E['scene_sha256'])
for rel,h in E['inputs'].items():check('accepted input unchanged: '+rel,hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h)
for lib in bpy.data.libraries:check('relative source library resolves',lib.filepath.startswith('//') and Path(bpy.path.abspath(lib.filepath)).is_file(),lib.filepath)
check('three 120-degree source references',len(E['sensor_references'])==3 and all(abs((math.atan2(E['sensor_references'][(i+1)%3]['position'][2],E['sensor_references'][(i+1)%3]['position'][1])-math.atan2(E['sensor_references'][i]['position'][2],E['sensor_references'][i]['position'][1]))%(2*math.pi)-2*math.pi/3)<1e-4 for i in range(3)))
section=bpy.data.objects['SECTION | ECCO_HOUSING_SOURCE_MESH']
check('section stays inside supplied tool OD (no Boolean complement)',max(abs(v.co.y) for v in section.data.vertices)<.153 and max(abs(v.co.z) for v in section.data.vertices)<.153,list(section.dimensions))
for e in E['events']:
    n=e['cycle'];origin=Vector(e['origin']);wall=Vector(e['wall'])
    for frame,name,expected in [(e['emit'],f'TX_{n}',origin),(e['contact'],f'TX_{n}',wall),(e['contact'],f'ECHO_{n}',wall),(e['receive'],f'ECHO_{n}',origin)]:
        s.frame_set(frame);bpy.context.view_layer.update();o=bpy.data.objects[name]
        check(f'ping {n} {name} endpoint f{frame}',(o.matrix_world.translation-expected).length<1e-6)
    check(f'ping {n} positive stand-off',e['illustrative_standoff_m']>.002)
    check(f'ping {n} equal outgoing/return diagram durations',e['contact']-e['emit']==e['receive']-e['contact'])
    check(f'ping {n} common schematic speed within half frame',abs(e['leg_frames']*.003-e['illustrative_standoff_m'])<=.0015)
    s.frame_set(e['start']+59);bpy.context.view_layer.update()
    r=bpy.data.objects['ASSEMBLY_CONTROL'];check(f'ping {n} whole-tool rotation control',abs(r['rotation_rad']-e['rotation_rad'])<1e-5)
    for other in E['events']:
        if other['cycle']!=n:check(f'ping {n} inactive emitter {other["cycle"]}',max(bpy.data.objects[f'EMITTER_REFERENCE_{other["cycle"]}'].scale)<1e-5)
check('T6 variation produces different arrival positions',len(set(e['leg_frames'] for e in E['events'][3:]))==3)
check('preview timeline',s.frame_start==1 and s.frame_end==432 and s.render.fps==24)
out={'kind':'implementation self-check, not independent MIT verification','checks':checks,'passed':all(c['pass_'] for c in checks),'count':len(checks)}
(R/'Evidence/verification_v004.json').write_text(json.dumps(out,indent=2))
assert out['passed'],[c for c in checks if not c['pass_']]
print('B201_VERIFY_PASS',len(checks))
