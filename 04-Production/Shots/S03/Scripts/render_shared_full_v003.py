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
scene.render.resolution_x = 640
scene.render.resolution_y = 360
scene.render.resolution_percentage = 100
scene.eevee.taa_render_samples = 8
scene.render.image_settings.file_format = "PNG"
temp = previews / "S03_v003_full_buffer.png"
clip = previews / "S03_shared-environment_v003_full.mp4"
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

frames = previews / "Full-v003"
frames.mkdir(exist_ok=True)
try:
    render(1)
    for frame in (1, 145, 217, 241, 337, 432):
        _, elapsed = render(frame)
        if elapsed >= 5:
            raise RuntimeError(f"Benchmark exceeds cap at {frame}: {elapsed}s")
    for frame in range(1, 433):
        output = frames / f"frame_{frame:04d}.png"
        if output.exists():
            continue
        _, elapsed = render(frame)
        if elapsed >= 5:
            raise RuntimeError(f"Frame {frame} exceeds cap: {elapsed}s")
        temp.replace(output)
    subprocess.run([str(ffmpeg), "-nostdin", "-v", "error", "-n", "-framerate", "24",
                    "-i", str(frames / "frame_%04d.png"), "-frames:v", "432",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(clip)], check=True)
finally:
    temp.unlink(missing_ok=True)
    (shot / "Notes/shared-environment-full_v003.json").write_text(
        json.dumps({"settings": "640x360 EEVEE 8 samples", "cold": timings[:1],
                    "benchmark": timings[1:7], "render": timings[7:]}, indent=2) + "\n")
