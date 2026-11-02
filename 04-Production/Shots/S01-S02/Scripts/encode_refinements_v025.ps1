$root=Split-Path -Parent $PSScriptRoot
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$record=Join-Path $root 'Notes/refinements_v025_motion.json'
do {
 $job=Get-Content -Raw -LiteralPath $record | ConvertFrom-Json
 if($job.status -eq 'failed'){throw $job.error}
 if($job.status -ne 'complete'){Start-Sleep -Seconds 2}
} while($job.status -ne 'complete')
$preview=Join-Path $root 'Previews/Fitted-contours-v025'
$video=Join-Path $preview 'fitted_contours_v025.mp4'
& $ffmpeg -hide_banner -loglevel error -y -framerate 12 -start_number 0 -i (Join-Path $preview 'preview_%04d.png') -frames:v 115 -c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Encode failed'}
$review=Join-Path $preview 'Decoded-review'
New-Item -ItemType Directory -Path $review -Force | Out-Null
& $ffmpeg -hide_banner -loglevel error -y -i $video -vf 'scale=320:180,tile=6x4' -fps_mode vfr (Join-Path $review 'review_%02d.png')
if($LASTEXITCODE -ne 0){throw 'Decode failed'}
$timings=@($job.rows | ForEach-Object {$_.seconds})
[pscustomobject]@{frames=$timings.Count;render_seconds=($timings | Measure-Object -Sum).Sum;average_seconds=($timings | Measure-Object -Average).Average;max_seconds=($timings | Measure-Object -Maximum).Maximum;wall_seconds=$job.wall_seconds;fps=12;duration_seconds=115/12;video=$video} | ConvertTo-Json | Set-Content (Join-Path $root 'Notes/refinements_v025_render_summary.json')
