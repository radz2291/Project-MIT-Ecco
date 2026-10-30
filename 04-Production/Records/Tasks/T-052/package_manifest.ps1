$taskRoot = $PSScriptRoot
$repoRoot = (Resolve-Path (Join-Path $taskRoot '../../../..')).Path
$nativePaths = @('04-Production/Shared/Assets/ECCO/Satin_finish_v001.blend','04-Production/Shared/Assets/ECCO/ECCO_film_v003.blend','04-Production/Shared/Assets/BHA/BHA_core_satin_v001.blend','04-Production/Shared/Assets/BHA/BHA_film_v008.blend')
$nativePaths += Get-ChildItem -LiteralPath (Join-Path $taskRoot 'Consumers') -Filter '*.blend' | ForEach-Object { [IO.Path]::GetRelativePath($repoRoot,$_.FullName).Replace('\','/') }
$nativePaths += Get-ChildItem -LiteralPath (Join-Path $taskRoot 'Previews') -Filter '*.mp4' | ForEach-Object { [IO.Path]::GetRelativePath($repoRoot,$_.FullName).Replace('\','/') }
$hashes = foreach ($p in $nativePaths) { $f=Get-Item -LiteralPath (Join-Path $repoRoot $p); [ordered]@{path=$p;sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash.ToLower();bytes=$f.Length;storage='local-only; no new backup/upload claim'} }
$hashes | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'Evidence/native-manifest.json') -Encoding utf8
$published = Get-ChildItem -LiteralPath $taskRoot -File -Recurse | Where-Object { $_.Extension -in '.md','.py','.ps1','.json','.png' -and $_.FullName -notmatch '[\\/]Frames[\\/]' -and $_.Name -ne 'publication-files.json' } | ForEach-Object { [IO.Path]::GetRelativePath($repoRoot,$_.FullName).Replace('\','/') }
@{files=@($published);exclude='All .blend, .blend1, MP4 and raw frames remain local.'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $taskRoot 'publication-files.json') -Encoding utf8
