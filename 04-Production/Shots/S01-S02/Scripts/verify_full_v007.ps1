$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$preview=Join-Path $root 'Previews/Full-v007'
$record=Get-Content (Join-Path $root 'Notes/full_v007_render.json') -Raw | ConvertFrom-Json
if($record.status -ne 'complete'){throw "Render status: $($record.status)"}
if($record.records.Count -ne 528){throw 'Expected528 timing records'}
foreach($frame in 1..528){
    $imagePath=Join-Path $preview ('frame_{0:D4}.png' -f $frame)
    if(!(Test-Path -LiteralPath $imagePath)){throw "Missing frame $frame"}
    if((Get-Item -LiteralPath $imagePath).Length -le 0){throw "Empty frame $frame"}
}
$timing=$record.records | Measure-Object seconds -Minimum -Maximum -Average
if($timing.Maximum -ge 5){throw 'Render cap violated'}
$video=Join-Path $preview 'S01-S02_full_1080_v007.mp4'
$encoder='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
& $encoder -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i (Join-Path $preview 'frame_%04d.png') -frames:v 528 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $video
if($LASTEXITCODE -ne 0){throw 'Video encoding failed'}
$decodeLog=Join-Path $root 'Notes/full_v007_decode.txt'
& $encoder -hide_banner -loglevel error -progress $decodeLog -nostats -i $video -f null -
if($LASTEXITCODE -ne 0){throw 'Video decode failed'}
if(!(Select-String -LiteralPath $decodeLog -Pattern '^frame=528$' -Quiet)){throw 'Decoded frame count is not528'}
$evidence=[ordered]@{frames=528;fps=24;duration_seconds=22;size=@(1920,1080);all_png_present=$true;decode_passed=$true;minimum_seconds=$timing.Minimum;maximum_seconds=$timing.Maximum;average_seconds=$timing.Average;export_elapsed_seconds=$record.elapsed_seconds;video=$video;video_sha256=(Get-FileHash -LiteralPath $video -Algorithm SHA256).Hash;local_only=$true}
$evidence | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $root 'Notes/full_v007_verification.json') -Encoding utf8
$evidence | ConvertTo-Json
