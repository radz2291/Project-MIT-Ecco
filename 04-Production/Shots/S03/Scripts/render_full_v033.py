"""Render the full S03 proof after benchmarking and retain completed frames."""
import bpy
import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

shot = Path(__file__).resolve().parents[1]
previews = shot / "Previews"
ffmpeg = Path(sys.argv[sys.argv.index("--") + 1]).resolve()
if not ffmpeg.is_file():
    raise FileNotFoundError(ffmpeg)
scene = bpy.context.scene
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.render.use_compositing = False
scene.eevee.use_raytracing = False
scene.render.image_settings.file_format = "PNG"
temp = previews / "S03_v033_full_buffer.png"
clip = previews / "S03_nominal-fade-in_v033_full.mp4"
if clip.exists():
    raise FileExistsError(clip)
timings = []

def render(frame):
    start = perf_counter()
    scene.frame_set(frame)
    scene.camera.data.update_tag()
    bpy.context.view_layer.update()
    scene.render.filepath = str(temp)
    bpy.ops.render.render(write_still=True)
    elapsed = round(perf_counter() - start, 3)
    timings.append({"frame": frame, "seconds": elapsed})
    print("TIMING", frame, elapsed, flush=True)
    return temp.read_bytes(), elapsed

frames = previews / "Full-v033"
frames.mkdir(exist_ok=True)
try:
    render(1)  # Measure shader startup separately.
    for frame in (1, 15, 172, 222, 270, 337, 432, 552):
        for attempt in range(3):
            _, elapsed = render(frame)
            if elapsed < 5:
                break
        else:
            raise RuntimeError(f"Benchmark exceeds cap at {frame}: {elapsed}s")
    for frame in range(1, scene.frame_end + 1):
        output = frames / f"frame_{frame:04d}.png"
        if output.exists():
            continue
        for attempt in range(3):
            _, elapsed = render(frame)
            if elapsed < 5:
                break
        else:
            raise RuntimeError(f"Frame {frame} exceeds cap: {elapsed}s")
        temp.replace(output)
    subprocess.run([str(ffmpeg), "-nostdin", "-v", "error", "-n", "-framerate", "24",
                    "-i", str(frames / "frame_%04d.png"), "-frames:v", str(scene.frame_end),
                    "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(clip)], check=True)
finally:
    temp.unlink(missing_ok=True)
    (shot / "Notes/nominal-fade-in-full_v033.json").write_text(
        json.dumps({"settings": "960x540 EEVEE 8 samples, compositor and ray tracing off", "cold": timings[:1],
                    "benchmark": timings[1:9], "render": timings[9:]}, indent=2) + "\n")
