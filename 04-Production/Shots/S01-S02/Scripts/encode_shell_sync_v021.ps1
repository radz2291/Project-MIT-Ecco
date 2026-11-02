$root=Split-Path -Parent $PSScriptRoot
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$record=Join-Path $root 'Notes/shell_sync_v021_motion_final.json'
do {
 $job=Get-Content -Raw -LiteralPath $record | ConvertFrom-Json
 if($job.status -eq 'failed' -or $job.status -eq 'cancelled'){throw ($job | ConvertTo-Json -Depth 5)}
 if($job.status -ne 'complete'){Start-Sleep -Seconds 2}
} while($job.status -ne 'complete')
$frames=Join-Path $root 'Previews/Shell-sync-v021-final/preview_%04d.png'
$video=Join-Path $root 'Previews/Shell-sync-v021-final/camera_reveal_v021.mp4'
& $ffmpeg -hide_banner -loglevel error -y -framerate 8 -start_number 0 -i $frames -frames:v 95 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Encode failed'}
$progress=Join-Path $root 'Notes/shell_sync_v021_decode_final.txt'
& $ffmpeg -loglevel error -progress $progress -i $video -f null -
if($LASTEXITCODE -ne 0){throw 'Decode failed'}
Get-Content -LiteralPath $progress -Tail 12
Get-FileHash -LiteralPath $video -Algorithm SHA256 | Select-Object Hash


