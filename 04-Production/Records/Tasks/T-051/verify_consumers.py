"""Independent saved-file inspection; Blender background, no saves or renders.

Arguments after --: mapping JSON, output JSON. Mapping list entries contain
baseline/candidate repository-relative paths and optional frames.
"""
import bpy, pathlib, json, sys, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[4]

def digest(path):
    return hashlib.file_digest(open(path, 'rb'), 'sha256').hexdigest()

def inspect(relative, frames=None):
    path = ROOT / relative
    before = digest(path)
    bpy.ops.wm.open_mainfile(filepath=str(path), load_ui=False)
    s = bpy.context.scene
    frames = frames or sorted(set([s.frame_start, s.frame_end, (s.frame_start+s.frame_end)//2]))
    samples = []
    for frame in frames:
        s.frame_set(frame)
        cam = s.camera.evaluated_get(bpy.context.evaluated_depsgraph_get()) if s.camera else None
        samples.append({'frame':frame,'matrix':[round(v,7) for row in cam.matrix_world for v in row] if cam else None,
                        'lens':round(cam.data.lens,7) if cam else None,
                        'shift':[cam.data.shift_x,cam.data.shift_y] if cam else None})
    libraries = []
    for lib in bpy.data.libraries:
        resolved = pathlib.Path(bpy.path.abspath(lib.filepath))
        libraries.append({'path':lib.filepath,'resolved':str(resolved),'exists':resolved.is_file()})
    return {'path':relative,'sha256':before,'unchanged':digest(path)==before,
            'range':[s.frame_start,s.frame_end], 'fps':[s.render.fps,s.render.fps_base],
            'camera_samples':samples,'libraries':libraries,
            'objects':len(bpy.data.objects),'materials':len(bpy.data.materials)}

args = sys.argv[sys.argv.index('--')+1:]
results=[]
for entry in json.loads(pathlib.Path(args[0]).read_text(encoding='utf-8-sig')):
    baseline=inspect(entry['baseline'],entry.get('frames'))
    candidate=inspect(entry['candidate'],entry.get('frames'))
    checks={key:baseline[key]==candidate[key] for key in ['range','fps','camera_samples']}
    checks['source_files_unchanged']=baseline['unchanged'] and candidate['unchanged']
    checks['candidate_libraries_exist']=all(x['exists'] for x in candidate['libraries'])
    results.append({'baseline':baseline,'candidate':candidate,'checks':checks,'pass':all(checks.values())})
pathlib.Path(args[1]).write_text(json.dumps(results,indent=2),encoding='utf-8')
print(json.dumps([{'candidate':r['candidate']['path'],'checks':r['checks']} for r in results]))
