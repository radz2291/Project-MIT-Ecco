"""Run in live Blender; frame evaluation through saved PNG must stay below5s.

Defaults benchmark1080p across the shot. Override test_frames/test_size/test_prefix
in the execution namespace for a bounded motion proof. Restore current frame.
"""
import bpy, time, json
from pathlib import Path

Q = Path(__file__).resolve().parents[1]
P = Q/'Previews/Render-feasibility-v005'
P.mkdir(exist_ok=True)
exec(bpy.data.texts['START HERE — pixel guides'].as_string())
module = bpy.app.driver_namespace['ecco_pixel_module']
scene = bpy.context.scene
original = scene.frame_current
frames = globals().get('test_frames', [1,80,95,106,123,157,318,432,528])
size = globals().get('test_size', (1920,1080))
prefix = globals().get('test_prefix', 'benchmark1080')
records = []
try:
    for frame in frames:
        started = time.perf_counter()
        scene.frame_set(frame)
        module.export(P/f'{prefix}_{frame:04}.png', *size)
        seconds = time.perf_counter()-started
        records.append({'frame':frame, 'seconds':seconds})
        (Q/'Notes'/f'{prefix}_timings.json').write_text(json.dumps(
            {'size':size,'fps':scene.render.fps,'timing':'frame evaluation through saved PNG',
             'method':'GPU viewport scene with fixed-pixel guides','records':records}, indent=2))
        if seconds >= 5:
            raise RuntimeError('Stopped: five-second render cap exceeded')
finally:
    scene.frame_set(original)
result = {'count':len(records),'max_seconds':max(x['seconds'] for x in records)}
