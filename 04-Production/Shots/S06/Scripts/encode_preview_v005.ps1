param(
    [Parameter(Mandatory)][string]$Ffmpeg,
    [string]$Cache,
    [string]$Video,
    [string]$Verification,
    [int]$FrameCount = 96
)

$ErrorActionPreference = 'Stop'
$shot = Split-Path -Parent $PSScriptRoot
$cache = if ($Cache) { $Cache } else { Join-Path $shot 'Cache/v005/preview' }
$state = Get-Content -LiteralPath (Join-Path $cache 'timings.json') -Raw | ConvertFrom-Json -AsHashtable
if ($state.frames.Count -ne $FrameCount -or ($state.frames.Values | Measure-Object -Maximum).Maximum -ge 5) {
    throw "The $FrameCount-frame source is incomplete or over budget."
}
$video = if ($Video) { $Video } else { Join-Path $shot 'Previews/S06_shared-reconstruction_v005_opening.mp4' }
$verification = if ($Verification) { $Verification } else { Join-Path $shot 'Notes/v005-preview-delivery.json' }
$seconds = $FrameCount / 24
$duration = [TimeSpan]::FromSeconds($seconds).ToString('hh\:mm\:ss\.ffffff')
$partial = [IO.Path]::ChangeExtension($video, '.encoding.mp4')
$encode = @(
    '-nostdin', '-hide_banner', '-loglevel', 'error', '-xerror', '-y',
    '-framerate', '24', '-start_number', '1', '-i', (Join-Path $cache 'S06_%04d.png'),
    '-frames:v', [string]$FrameCount, '-an', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
    '-pix_fmt', 'yuv420p', '-movflags', '+faststart', $partial
)
& $Ffmpeg @encode
if ($LASTEXITCODE -ne 0) { throw 'Preview encode failed.' }
$decode = & $Ffmpeg -nostdin -hide_banner -loglevel error -xerror -progress pipe:1 -i $partial -map 0:v:0 -f null NUL
if ($LASTEXITCODE -ne 0 -or $decode -notcontains "frame=$FrameCount" -or
    $decode -notcontains "out_time=$duration" -or
    $decode -notcontains 'drop_frames=0' -or $decode -notcontains 'dup_frames=0') {
    throw "The preview failed its $FrameCount-frame decode."
}
Move-Item -LiteralPath $partial -Destination $video -Force
$measure = $state.frames.Values | Measure-Object -Average -Maximum -Sum
$record = [ordered]@{
    video = [IO.Path]::GetFileName($video)
    sha256 = (Get-FileHash -LiteralPath $video).Hash.ToLowerInvariant()
    settings = $state.settings
    frames = @(1,$FrameCount)
    seconds = $seconds
    decoded_frames = $FrameCount
    relative_libraries = $state.relative_libraries
    benchmark = $state.benchmark
    setup_seconds = $state.setup
    max_seconds = $measure.Maximum
    mean_seconds = $measure.Average
    total_seconds = $measure.Sum
    retries = $state.over_cap_attempts
}
$record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $verification -Encoding utf8
$record | ConvertTo-Json -Depth 8
