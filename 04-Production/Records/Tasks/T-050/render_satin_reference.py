"""One owner-requested S07 material-review still; never saves the source scene."""
import bpy, time, json, hashlib
from pathlib import Path

task = Path(__file__).resolve().parent
scene = bpy.context.scene
source = Path(bpy.data.filepath)
before = hashlib.sha256(source.read_bytes()).hexdigest()
folder = task/'Previews'
folder.mkdir(exist_ok=True)
scene.frame_set(90)
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = str(folder/'S07_satin-studio_f090.png')
start = time.perf_counter()
bpy.ops.render.render(write_still=True)
seconds = time.perf_counter()-start
record = {
    'source': str(source), 'source_sha256': before,
    'source_unchanged': hashlib.sha256(source.read_bytes()).hexdigest()==before,
    'frame':90, 'engine':scene.render.engine,
    'resolution':[scene.render.resolution_x,scene.render.resolution_y,scene.render.resolution_percentage],
    'samples':scene.eevee.taa_render_samples,
    'seconds':seconds, 'under_five_seconds':seconds<5,
    'output':scene.render.filepath,
    'purpose':'Owner-requested satin material reference under existing S07 studio lighting. Not material-only appearance.'
}
(task/'Evidence'/'satin-render.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print('SATIN_RENDER',json.dumps(record),flush=True)
