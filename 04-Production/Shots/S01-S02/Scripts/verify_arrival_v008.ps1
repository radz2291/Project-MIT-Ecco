$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$preview=Join-Path $root 'Previews/Arrival-v008'
$record=Get-Content (Join-Path $root 'Notes/arrival_v008_render.json') -Raw | ConvertFrom-Json
if($record.status -ne 'complete' -or $record.records.Count -ne 137){throw 'Expected complete137-frame proof'}
foreach($frame in 128..264){
    $path=Join-Path $preview ('frame_{0:D4}.png' -f $frame)
    if(!(Test-Path -LiteralPath $path) -or (Get-Item -LiteralPath $path).Length -le 0){throw "Missing/empty frame $frame"}
}
$timing=$record.records | Measure-Object seconds -Minimum -Maximum -Average
if($timing.Maximum -ge 5){throw 'Render cap violated'}
$ffmpeg='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$video=Join-Path $preview 'S01-S02_product_arrival_v008.mp4'
& $ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 128 -i (Join-Path $preview 'frame_%04d.png') -frames:v 137 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Video encode failed'}
$progress=Join-Path $root 'Notes/arrival_v008_decode.txt'
& $ffmpeg -hide_banner -loglevel error -nostats -progress $progress -i $video -f null -
if($LASTEXITCODE -ne 0 -or !(Select-String -LiteralPath $progress -Pattern '^frame=137$' -Quiet)){throw 'Video decode failed'}
$old=Join-Path $root 'Previews/Full-v007/S01-S02_full_1080_v007.mp4'
$comparison=Join-Path $preview 'compare_v007_left_v008_right.mp4'
$filter='[0:v]trim=start_frame=127:end_frame=264,setpts=PTS-STARTPTS,scale=960:540[left];[1:v]scale=960:540[right];[left][right]hstack=inputs=2[v]'
& $ffmpeg -hide_banner -loglevel error -y -i $old -i $video -filter_complex $filter -map '[v]' -frames:v 137 -r 24 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $comparison
if($LASTEXITCODE -ne 0){throw 'Comparison encode failed'}
$compareProgress=Join-Path $root 'Notes/arrival_v008_compare_decode.txt'
& $ffmpeg -hide_banner -loglevel error -nostats -progress $compareProgress -i $comparison -f null -
if($LASTEXITCODE -ne 0 -or !(Select-String -LiteralPath $compareProgress -Pattern '^frame=137$' -Quiet)){throw 'Comparison decode failed'}
$out=[ordered]@{frames=137;source_range=@(128,264);fps=24;duration_seconds=(137/24);size=@(1920,1080);minimum_seconds=$timing.Minimum;maximum_seconds=$timing.Maximum;average_seconds=$timing.Average;video=$video;video_sha256=(Get-FileHash -LiteralPath $video).Hash;comparison=$comparison;both_decode_passed=$true;local_only=$true}
$out | ConvertTo-Json | Set-Content (Join-Path $root 'Notes/arrival_v008_verification.json') -Encoding utf8
$out | ConvertTo-Json
