param(
    [Parameter(Mandatory)][string]$Ffmpeg,
    [Parameter(Mandatory)][string]$Frames,
    [Parameter(Mandatory)][string]$OriginalVideo,
    [Parameter(Mandatory)][string]$OutputVideo
)
$ErrorActionPreference = 'Stop'
$provenance = "drawbox=x=0:y=ih-21:w=iw:h=21:color=0x0A1419@0.745:t=fill,drawtext=fontfile='C\:/Windows/Fonts/segoeui.ttf':text='ILLUSTRATIVE GEOMETRY AND RESPONSE — NOT FIELD DATA':x=15:y=h-16:fontsize=9:fontcolor=0xCDDCE1"
$filter = "[0:v]trim=end_frame=62,setpts=PTS-STARTPTS,$provenance,format=yuv420p[entry];[1:v]trim=start_frame=62:end_frame=116,setpts=PTS-STARTPTS,scale=960:540:flags=lanczos,setsar=1[tail];[entry][tail]concat=n=2:v=1:a=0,settb=1/24,setpts=N[v]"
& $Ffmpeg -hide_banner -loglevel error -n -framerate 24 -start_number 1 -i (Join-Path $Frames 'frame_%04d.png') -i $OriginalVideo -filter_complex $filter -map '[v]' -an -r 24 -fps_mode cfr -video_track_timescale 24000 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $OutputVideo
if ($LASTEXITCODE -ne 0) { throw 'Opening camera encode failed.' }
$decode = & $Ffmpeg -hide_banner -loglevel error -progress pipe:1 -i $OutputVideo -map '0:v:0' -f null -
if ($LASTEXITCODE -ne 0 -or $decode -notcontains 'frame=116') { throw 'Opening preview failed full 116-frame decode.' }
$decode | Select-Object -Last 12
