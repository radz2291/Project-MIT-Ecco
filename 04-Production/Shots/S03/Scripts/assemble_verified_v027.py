"""Reuse v024 frames outside the verified v027 orbit-entry patch."""
import bpy
import json
import subprocess
import sys
from pathlib import Path

shot = Path(__file__).resolve().parents[1]
ffmpeg = Path(sys.argv[sys.argv.index("--")+1])
outside = list(range(1,246)) + list(range(307,553))

def camera_samples():
    scene = bpy.context.scene
    samples = []
    for frame in outside:
        scene.frame_set(frame)
        camera = scene.camera
        samples.append((camera.matrix_world.copy(), camera.data.lens,
                        camera.data.shift_x, camera.data.shift_y))
    return samples

bpy.ops.wm.open_mainfile(filepath=str(shot/"Scenes/S03_subtle-titles_v024.blend"))
before = camera_samples()
bpy.ops.wm.open_mainfile(filepath=str(shot/"Scenes/S03_smooth-orbit-entry_v027.blend"))
after = camera_samples()
difference = max(max(abs(a-b) for x,y in zip(old[0],new[0]) for a,b in zip(x,y))
                 for old,new in zip(before,after))
assert difference < 1e-6, difference
assert all(old[1:] == new[1:] for old,new in zip(before,after))
previews = shot/"Previews"
clip = previews/"S03_smooth-orbit_v027_full.mp4"
frames = [previews/("Full-v027" if 246 <= f <= 306 else "Full-v024")/f"frame_{f:04d}.png"
          for f in range(1,553)]
assert all(path.is_file() for path in frames)
command = [str(ffmpeg),"-nostdin","-v","error","-n","-f","image2pipe","-framerate","24",
           "-vcodec","png","-i","pipe:0","-c:v","libx264","-pix_fmt","yuv420p",
           "-movflags","+faststart",str(clip)]
with subprocess.Popen(command,stdin=subprocess.PIPE) as encoder:
    for path in frames:
        encoder.stdin.write(path.read_bytes())
    encoder.stdin.close()
    assert encoder.wait() == 0
decode = subprocess.run([str(ffmpeg),"-v","error","-i",str(clip),"-progress","pipe:1",
                         "-f","null","-"],capture_output=True,text=True,check=True)
assert "frame=552" in decode.stdout.splitlines() and "progress=end" in decode.stdout.splitlines()
evidence = {"decoded_frames":552,"fps":24,"new_frames":[246,306],
            "reused_frames":len(outside),"max_unchanged_camera_matrix_delta":difference}
(shot/"Notes/assemble-verified_v027.json").write_text(json.dumps(evidence,indent=2)+"\n")
print("VERIFIED",evidence,flush=True)
