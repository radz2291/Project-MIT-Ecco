param([Parameter(Mandatory)][string]$Ffmpeg)

$ErrorActionPreference = 'Stop'
$shot = Split-Path -Parent $PSScriptRoot
$cache = Join-Path $shot 'Cache/v028/full-vulkan'
$output = Join-Path $shot 'Previews/S05_stretched-grid_v028_final.mp4'
$partial = [IO.Path]::ChangeExtension($output, '.encoding.mp4')
$verification = Join-Path $shot 'Notes/v028-full-delivery.json'
$state = Get-Content -LiteralPath (Join-Path $cache 'timings.json') -Raw | ConvertFrom-Json -AsHashtable
if (Test-Path -LiteralPath $output) { throw "Output already exists: $output" }
if ($state.frames.Count -ne 432) { throw 'Expected timings for all 432 frames.' }
foreach ($frame in 1..432) {
    $path = Join-Path $cache ('S05_{0:D4}.png' -f $frame)
    if (-not (Test-Path -LiteralPath $path -PathType Leaf) -or
        -not $state.frames.Contains([string]$frame) -or $state.frames[[string]$frame] -ge 5) {
        throw "Missing or over-budget source frame: $frame"
    }
}

$encodeArguments = @(
    '-nostdin', '-hide_banner', '-loglevel', 'error', '-xerror', '-y',
    '-framerate', '24', '-start_number', '1', '-i', (Join-Path $cache 'S05_%04d.png'),
    '-frames:v', '432', '-map', '0:v:0', '-an', '-sn', '-dn', '-c:v', 'libx264',
    '-preset', 'fast', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', $partial
)
& $Ffmpeg @encodeArguments
if ($LASTEXITCODE -ne 0) { throw 'Picture-only encode failed.' }

$frameHashes = Join-Path $cache 'decoded.framemd5'
$decode = & $Ffmpeg -nostdin -hide_banner -loglevel error -xerror -y -progress pipe:1 -i $partial -map 0 -f framemd5 $frameHashes
if ($LASTEXITCODE -ne 0 -or $decode -notcontains 'frame=432' -or
    $decode -notcontains 'out_time=00:00:18.000000' -or
    $decode -notcontains 'dup_frames=0' -or $decode -notcontains 'drop_frames=0') {
    throw 'Full MP4 decode failed.'
}
$decoded = Get-Content -LiteralPath $frameHashes
$mediaTypes = @($decoded | Where-Object { $_ -match '^#media_type' })
$records = @($decoded | Where-Object { $_ -match '^0\s*,' })
if ($mediaTypes.Count -ne 1 -or $mediaTypes[0] -ne '#media_type 0: video' -or
    $decoded -notcontains '#dimensions 0: 960x540' -or $decoded -notcontains '#tb 0: 1/24' -or
    $records.Count -ne 432) { throw 'Decoded stream does not match the delivery profile.' }
$hashes = @($records | ForEach-Object { ($_ -split ',')[-1].Trim() })
if (@($hashes | Sort-Object -Unique).Count -ne 432) { throw 'Duplicate decoded images found.' }
Move-Item -LiteralPath $partial -Destination $output

$times = $state.frames.Values | Measure-Object -Minimum -Maximum -Average -Sum
$bench = $state.benchmark.Values | Measure-Object -Maximum
$result = [ordered]@{
    output = [IO.Path]::GetFileName($output)
    sha256 = (Get-FileHash -LiteralPath $output).Hash.ToLowerInvariant()
    profile = $state.settings
    codec = 'H.264, yuv420p, CRF 17'
    duration_seconds = 18
    decoded_frames = 432
    distinct_decoded_images = 432
    audio_streams = 0
    benchmark_frames = $state.benchmark
    maximum_benchmark_seconds = $bench.Maximum
    render_mean_seconds = $times.Average
    render_maximum_seconds = $times.Maximum
    render_total_seconds = $times.Sum
    renderer_setup_seconds = $state.setup
    over_cap_attempts = $state.over_cap_attempts
}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $verification -Encoding utf8
$result | ConvertTo-Json -Depth 8
