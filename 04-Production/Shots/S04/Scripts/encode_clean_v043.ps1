param(
    [Parameter(Mandatory)][string]$Ffmpeg,
    [Parameter(Mandatory)][string]$Frames,
    [Parameter(Mandatory)][string]$OutputVideo
)
$ErrorActionPreference = 'Stop'
$pngs = @(Get-ChildItem -LiteralPath $Frames -Filter 'S04_*.png' -File)
if ($pngs.Count -ne 432) { throw 'Expected 432 raw frames.' }
$partial = [IO.Path]::ChangeExtension($OutputVideo, '.encoding.mp4')
& $Ffmpeg -hide_banner -loglevel error -y -framerate 24 -start_number 1 -i (Join-Path $Frames 'S04_%04d.png') -frames:v 432 -an -c:v libx264 -preset fast -crf 17 -pix_fmt yuv420p -movflags +faststart $partial
if ($LASTEXITCODE -ne 0) { throw 'Clean export encode failed.' }
$decode = & $Ffmpeg -hide_banner -loglevel error -progress pipe:1 -i $partial -map '0:v:0' -f null -
if ($LASTEXITCODE -ne 0 -or $decode -notcontains 'frame=432' -or $decode -notcontains 'out_time=00:00:18.000000') {
    throw 'Clean export failed the full decode.'
}
Move-Item -LiteralPath $partial -Destination $OutputVideo -Force
$decode | Select-Object -Last 12
