param(
    [Parameter(Mandatory)][string]$Ffmpeg,
    [Parameter(Mandatory)][string]$SourceVideo,
    [Parameter(Mandatory)][string]$OutputVideo
)
$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath $SourceVideo).Path
# Source frames 69–116 and 182–229 inclusive, with matching pulse lead-in.
$filter = '[0:v]trim=start_frame=68:end_frame=116,setpts=PTS-STARTPTS[s];[0:v]trim=start_frame=181:end_frame=229,setpts=PTS-STARTPTS[r];[s][r]concat=n=2:v=1:a=0,settb=1/24,setpts=N[v]'
& $Ffmpeg -hide_banner -loglevel error -n -i $source -filter_complex $filter -map '[v]' -an -r 24 -fps_mode cfr -video_track_timescale 24000 -c:v libx264 -crf 15 -pix_fmt yuv420p -movflags +faststart $OutputVideo
if ($LASTEXITCODE -ne 0) { throw 'Comparison encode failed.' }
$decode = & $Ffmpeg -hide_banner -loglevel error -progress pipe:1 -i $OutputVideo -map '0:v:0' -f null -
if ($LASTEXITCODE -ne 0 -or ($decode -notcontains 'frame=96')) {
    throw 'Comparison failed full 96-frame decode.'
}
$decode | Select-Object -Last 12
