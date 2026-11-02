$root=Split-Path -Parent $PSScriptRoot
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$record=Join-Path $root 'Notes/full_v016_render.json'
do {
 $job=Get-Content -Raw -LiteralPath $record | ConvertFrom-Json
 if($job.status -eq 'failed' -or $job.status -eq 'cancelled'){throw ($job | ConvertTo-Json -Depth 5)}
 if($job.status -ne 'complete'){Start-Sleep -Seconds 2}
} while($job.status -ne 'complete')
$frames=Join-Path $root 'Previews/Full-v016/frame_%04d.png'
$video=Join-Path $root 'Previews/Full-v016/S01-S02_full_v016.mp4'
& $ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i $frames -frames:v 756 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Encode failed'}
$progress=Join-Path $root 'Notes/full_v016_decode.txt'
& $ffmpeg -loglevel error -progress $progress -i $video -f null -
if($LASTEXITCODE -ne 0){throw 'Decode failed'}
Get-Content -LiteralPath $progress -Tail 12
Get-FileHash -LiteralPath $video -Algorithm SHA256 | Select-Object Hash
