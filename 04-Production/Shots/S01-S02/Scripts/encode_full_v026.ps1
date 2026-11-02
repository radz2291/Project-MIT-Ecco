$root=Split-Path -Parent $PSScriptRoot
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$record=Join-Path $root 'Notes/full_v026_render.json'
do {
 $job=Get-Content -Raw -LiteralPath $record | ConvertFrom-Json
 if($job.status -eq 'failed' -or $job.status -eq 'cancelled'){throw ($job | Select-Object status,next,error | ConvertTo-Json)}
 if($job.status -ne 'complete'){Start-Sleep -Seconds 2}
} while($job.status -ne 'complete')
$preview=Join-Path $root 'Previews/Full-v026'
$video=Join-Path $preview 'S01-S02_full_v026.mp4'
& $ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i (Join-Path $preview 'frame_%04d.png') -frames:v 756 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Encode failed'}
$review=Join-Path $preview 'Decoded-review'
New-Item -ItemType Directory -Path $review -Force | Out-Null
& $ffmpeg -hide_banner -loglevel error -y -i $video -vf 'scale=240:135,tile=8x6' -fps_mode vfr (Join-Path $review 'review_%02d.png')
if($LASTEXITCODE -ne 0){throw 'Contact sheet decode failed'}
$progress=Join-Path $root 'Notes/full_v026_decode.txt'
& $ffmpeg -hide_banner -loglevel error -progress $progress -i $video -f null -
if($LASTEXITCODE -ne 0){throw 'Full video decode failed'}
& $ffmpeg -hide_banner -i $video -f null - 2> (Join-Path $root 'Notes/full_v026_media.txt')
if($LASTEXITCODE -ne 0){throw 'Media verification failed'}
$times=@($job.records | ForEach-Object {$_.seconds})
[pscustomobject]@{frames=$times.Count;size=$job.size;fps=24;duration_seconds=31.5;active_render_seconds=($times | Measure-Object -Sum).Sum;average_seconds=($times | Measure-Object -Average).Average;max_seconds=($times | Measure-Object -Maximum).Maximum;elapsed_seconds=$job.elapsed_seconds;video=$video;video_sha256=(Get-FileHash -LiteralPath $video -Algorithm SHA256).Hash;decode_completed=$true} | ConvertTo-Json | Set-Content (Join-Path $root 'Notes/full_v026_summary.json')
