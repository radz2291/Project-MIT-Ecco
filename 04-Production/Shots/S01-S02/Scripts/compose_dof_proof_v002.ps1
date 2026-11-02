$root=Split-Path -Parent $PSScriptRoot
$preview=Join-Path $root 'Previews/DOF-investigation-v002'
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
& $ffmpeg -hide_banner -loglevel error -y -i (Join-Path $preview 'separate_base.png') -i (Join-Path $preview 'separate_measurement.png') -filter_complex '[0:v][1:v]overlay=0:0:format=auto' -frames:v 1 (Join-Path $preview 'separate_composite.png')
if($LASTEXITCODE -ne 0){throw 'Diagnostic composite failed'}
# PNG feasibility proof only. Production compositing requires scene-linear,
# consistently premultiplied layers and animation/occlusion verification.
