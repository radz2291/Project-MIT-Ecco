$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$production=Split-Path (Split-Path $root -Parent) -Parent
$preview=Join-Path $root 'Previews/Waveform-v009'
$fixture=Join-Path $production 'Shared/Demos/Previews/Waveform_v016'
$encoder='C:/Users/RZ1/.codex/tmp/ecco-media-runtime/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
$results=@()
function Encode-Sequence($pattern,$first,$count,$target){
 & $encoder -hide_banner -loglevel error -y -framerate 24 -start_number $first -i $pattern -frames:v $count -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $target
 if($LASTEXITCODE -ne 0){throw "Encode failed: $target"}
}
function Check-Video($target,$count,$name){
 $progress=Join-Path $root ('Notes/'+$name+'_decode.txt')
 & $encoder -hide_banner -loglevel error -nostats -progress $progress -i $target -f null -
 if($LASTEXITCODE -ne 0 -or !(Select-String -LiteralPath $progress -Pattern ('^frame='+$count+'$') -Quiet)){throw "Decode failed: $target"}
 return [pscustomobject][ordered]@{name=$name;path=$target;frames=$count;fps=24;decode_passed=$true;sha256=(Get-FileHash -LiteralPath $target).Hash}
}
$shot=Join-Path $preview 'S01-S02_waveform_v009.mp4'
Encode-Sequence (Join-Path $preview 'frame_%04d.png') 299 38 $shot
$results+=Check-Video $shot 38 'waveform_v009'
foreach($case in @(@('organic',1,96),@('open',70,27),@('cased',182,27))){
 $target=Join-Path $fixture ($case[0]+'_v016.mp4');Encode-Sequence (Join-Path $fixture ($case[0]+'_%04d.png')) $case[1] $case[2] $target
 $results+=Check-Video $target $case[2] ('waveform_v016_'+$case[0])
}
$comparison=Join-Path $preview 'compare_v007_left_v009_right.mp4'
$old=Join-Path $root 'Previews/Full-v007/S01-S02_full_1080_v007.mp4'
$filter='[0:v]trim=start_frame=298:end_frame=336,setpts=PTS-STARTPTS,scale=960:540[old];[1:v]scale=960:540[new];[old][new]hstack=inputs=2[v]'
& $encoder -hide_banner -loglevel error -y -i $old -i $shot -filter_complex $filter -map '[v]' -frames:v 38 -r 24 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $comparison
if($LASTEXITCODE -ne 0){throw 'Comparison encode failed'}
$results+=Check-Video $comparison 38 'waveform_v009_comparison'
$loop=Join-Path $preview 'compare_v007_left_v009_right_3x.mp4'
& $encoder -hide_banner -loglevel error -y -stream_loop 2 -i $comparison -frames:v 114 -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart $loop
if($LASTEXITCODE -ne 0){throw 'Loop encode failed'}
$results+=Check-Video $loop 114 'waveform_v009_comparison_3x'
$results | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $root 'Notes/waveform_v009_video_verification.json') -Encoding utf8
$results | Select-Object name,frames,decode_passed | ConvertTo-Json
