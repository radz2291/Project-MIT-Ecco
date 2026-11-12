"""Restore the selected S04 captions and encode the verified full frame sequence."""
from hashlib import sha256
import json
from pathlib import Path
import re
import statistics
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

cache, ffmpeg, output, record = [Path(arg).resolve() for arg in sys.argv[1:]]
timings = json.loads((cache / "timings.json").read_text())
profile = timings["settings"]
width, height = profile["resolution"]
fps = profile["fps"]
assert sorted(map(int, timings["frames"])) == list(range(1, 433))
assert max(timings["frames"].values()) < 5
scale = width / 1280
font_path = "C:/Windows/Fonts/segoeui.ttf"
font = ImageFont.truetype(font_path, round(21 * scale))
small = ImageFont.truetype(font_path, round(12 * scale))
partial = output.with_suffix(".encoding.mp4")
encode_log = cache / "encode.log"


def smooth(value):
    value = max(0, min(1, value))
    return value**3 * (10 + value * (-15 + 6 * value))


def caption(path, frame):
    with Image.open(path) as raw:
        base = raw.convert("RGBA")
    assert base.size == (width, height)
    layer = Image.new("RGBA", base.size)
    draw = ImageDraw.Draw(layer)
    for start, end, title in ((63, 141, "Supported backing"), (175, 261, "Reduced backing"),
                              (337, 450, "Inner-wall wear")):
        if start <= frame <= end:
            alpha = smooth((frame - start) / 8) * smooth((end - frame) / 8)
            right = draw.textbbox((0, 0), title, font=font)[2]
            draw.rounded_rectangle(
                (round(16*scale), round(17*scale), round(48*scale) + right, round(58*scale)),
                radius=max(1, round(5*scale)), fill=(12, 22, 28, round(145*alpha)),
            )
            draw.text((round(30*scale), round(25*scale)), title, font=font,
                      fill=(225, 235, 240, round(255*alpha)))
    if frame >= 336:
        draw.text((round(20*scale), round(669*scale)), "Wireframe tool: explanatory view",
                  font=small, fill=(185, 205, 215, 255))
    draw.rectangle((0, round(692*scale), width, height), fill=(10, 20, 25, 190))
    draw.text((round(20*scale), round(699*scale)), "ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA",
              font=small, fill=(205, 220, 225, 255))
    return Image.alpha_composite(base, layer).convert("RGB").tobytes()


with encode_log.open("wb") as log:
    command = [str(ffmpeg), "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
               "-pixel_format", "rgb24", "-video_size", f"{width}x{height}", "-framerate", str(fps),
               "-i", "-", "-frames:v", "432", "-an", "-c:v", "libx264", "-preset", "fast",
               "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(partial)]
    with subprocess.Popen(command, stdin=subprocess.PIPE, stderr=log) as process:
        for frame in range(1, 433):
            process.stdin.write(caption(cache / f"S04_{frame:04d}.png", frame))
        process.stdin.close()
        assert process.wait() == 0, encode_log

decoded = subprocess.run(
    [str(ffmpeg), "-hide_banner", "-loglevel", "error", "-progress", "pipe:1", "-i", str(partial),
     "-map", "0:v:0", "-f", "null", "-"], capture_output=True, check=True, text=True,
)
(cache / "decode.log").write_text(decoded.stdout)
assert re.findall(r"(?m)^frame=(\d+)\s*$", decoded.stdout)[-1] == "432"
assert "out_time=00:00:18.000000" in decoded.stdout
assert "dup_frames=0" in decoded.stdout and "drop_frames=0" in decoded.stdout
partial.replace(output)
values = list(timings["frames"].values())
delivery = {
    "video": output.name, "sha256": sha256(output.read_bytes()).hexdigest(), **profile,
    "frame_count": 432, "duration_seconds": 18, "all_frames_decoded": True,
    "render_mean_seconds": statistics.mean(values), "render_max_seconds": max(values),
    "render_total_seconds": sum(values), "renderer_setup_seconds": timings["setup_attempts"],
}
record.write_text(json.dumps(delivery, indent=2) + "\n")
print(json.dumps(delivery, indent=2))
