param(
    [Parameter(Mandatory)][string]$Ffmpeg,
    [Parameter(Mandatory)][string]$Frames,
    [Parameter(Mandatory)][string]$OutputVideo
)
$ErrorActionPreference = 'Stop'
$caption = "drawtext=fontfile='C\:/Windows/Fonts/segoeui.ttf':text='ILLUSTRATIVE VISUALIZATION':x=18:y=h-22:fontsize=11:fontcolor=white@0.75"
& $Ffmpeg -hide_banner -loglevel error -n -framerate 24 -start_number 1 -i (Join-Path $Frames 'frame_%04d.png') -frames:v 153 -vf $caption -an -c:v libx264 -crf 17 -pix_fmt yuv420p -movflags +faststart $OutputVideo
if ($LASTEXITCODE -ne 0) { throw 'Intro encode failed.' }
$decode = & $Ffmpeg -hide_banner -loglevel error -progress pipe:1 -i $OutputVideo -map '0:v:0' -f null -
if ($LASTEXITCODE -ne 0 -or $decode -notcontains 'frame=153') { throw 'Intro failed full 153-frame decode.' }
$decode | Select-Object -Last 12
