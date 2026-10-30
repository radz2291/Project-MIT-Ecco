"""Read-only independent geometry and face-size check for the ribbon context proof."""
import bpy, pathlib, sys, json, hashlib, math
from mathutils import Vector
ROOT=pathlib.Path(__file__).resolve().parents[4]
args=sys.argv[sys.argv.index('--')+1:]
candidate=ROOT/args[0]
before=hashlib.sha256(candidate.read_bytes()).hexdigest()
bpy.ops.wm.open_mainfile(filepath=str(candidate),load_ui=False)
s=bpy.context.scene
event=json.loads((ROOT/'04-Production/Records/Tasks/T-056/event-projection.json').read_text())
a=Vector(event['frames']['300']['DW 1 SEND front0 core']['world'])
b=Vector(event['frames']['309']['DW 1 fixed native contact pin']['world'])
up=Vector((0,0,1)); lateral=(b-a).normalized().cross(up).normalized()
records=[]
for frame in [298,300,305,309,314,318,324]:
    s.frame_set(frame); dg=bpy.context.evaluated_depsgraph_get()
    objects=[o for o in s.objects if o.type=='MESH' and o.name.startswith('RIBBON_FIXED')]
    if not objects: raise RuntimeError('No fixed ribbon mesh found')
    points=[]
    for ob in objects:
        ev=ob.evaluated_get(dg); mesh=ev.to_mesh()
        points.extend(ev.matrix_world@v.co for v in mesh.vertices)
        ev.to_mesh_clear()
    payload=[[round(v,8) for v in p] for p in points]
    heights=[(p-a).dot(up) for p in points]; widths=[(p-a).dot(lateral) for p in points]
    records.append({'frame':frame,'geometry_sha256':hashlib.sha256(json.dumps(payload).encode()).hexdigest(),
                    'height_m':max(heights)-min(heights),'width_m':max(widths)-min(widths),
                    'vertical_center_offset_m':(max(heights)+min(heights))/2})
cap=None
for instance in dg.object_instances:
    if instance.object.name=='TEMP | Imaging port 2 | removable acoustic cap':
        cap=[instance.matrix_world@v.co for v in instance.object.data.vertices];break
if cap is None: raise RuntimeError('Visible cap not found')
height=max(p.dot(up) for p in cap)-min(p.dot(up) for p in cap)
width=max(p.dot(lateral) for p in cap)-min(p.dot(lateral) for p in cap)
checks={'fixed_evaluated_geometry':len({r['geometry_sha256'] for r in records})==1,
        'height_matches_face_within_1_percent':all(abs(r['height_m']/height-1)<.01 for r in records),
        'width_matches_face_within_1_percent':all(abs(r['width_m']/width-1)<.01 for r in records),
        'centered_within_half_mm':all(abs(r['vertical_center_offset_m'])<.0005 for r in records),
        'candidate_unchanged':hashlib.sha256(candidate.read_bytes()).hexdigest()==before}
result={'candidate':args[0],'sha256':before,'face_height_m':height,'face_width_m':width,
        'records':records,'checks':checks,'all_pass':all(checks.values())}
(ROOT/args[1]).write_text(json.dumps(result,indent=2))
print(json.dumps({'checks':checks,'face_height_m':height,'face_width_m':width}))
if not result['all_pass']: raise SystemExit(1)
