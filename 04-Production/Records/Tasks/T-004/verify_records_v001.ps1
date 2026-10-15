$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path
$settingsPath = Join-Path $repoRoot '04-Production/Records/preview-settings_v001.md'
$verificationPath = Join-Path $PSScriptRoot 'verification_v001.json'
$docs = @($settingsPath) + @(Get-ChildItem -LiteralPath $PSScriptRoot -Filter '*.md' | ForEach-Object FullName)
$links = @()
foreach ($doc in $docs) {
    $body = Get-Content -LiteralPath $doc -Raw
    foreach ($match in [regex]::Matches($body, '\[[^\]]+\]\(([^)]+)\)')) {
        $target = [uri]::UnescapeDataString($match.Groups[1].Value.Split('#')[0])
        if (!$target -or $target -match '^https?://') { continue }
        $resolved = [IO.Path]::GetFullPath((Join-Path (Split-Path $doc) $target))
        $exists = (Test-Path -LiteralPath $resolved) -or ($resolved -eq $verificationPath)
        $links += [ordered]@{ document=$doc.Substring($repoRoot.Length+1); target=$target; exists=$exists }
        if (!$exists) { throw "Broken link: $doc -> $target" }
    }
}
$allocations = @()
foreach ($match in [regex]::Matches((Get-Content -LiteralPath $settingsPath -Raw), '\| (S0[1-7]) \| (\d+)–(\d+) \| (\d+)–(\d+) \| (\d+) \|')) {
    $a = @($match.Groups | Select-Object -Skip 2 | ForEach-Object { [int]$_.Value })
    if (($a[1]-$a[0])*24 -ne $a[4] -or $a[3]-$a[2]+1 -ne $a[4]) { throw 'Invalid section allocation' }
    $allocations += [pscustomobject]@{section=$match.Groups[1].Value;start=$a[2];end=$a[3];frames=$a[4]}
}
if ($allocations.Count -ne 7 -or ($allocations | Measure-Object frames -Sum).Sum -ne 2160) { throw 'Invalid total' }
for ($i=1; $i -lt 7; $i++) { if ($allocations[$i].start -ne $allocations[$i-1].end+1) { throw 'Timeline gap/overlap' } }
$sources = @('AGENTS.md','04-Production/README.md','03-Context/README.md','03-Context/01_Foundation/01-PHASE_A_PRODUCTION_BRIEF.md','03-Context/01_Foundation/04-STORYBOARD_AND_SHOT_PLAN.md','03-Context/01_Foundation/05-PRODUCTION_WORKFLOW.md','03-Context/01_Foundation/06-DECISIONS_AND_READINESS.md','04-Production/Records/Tasks/T-002/Evidence/source-imported_v001.json','04-Production/Shared/Assets/PZ12-8301 Main Housing ENP3 _A_ Modified TFA _5_ Ready _TC.stp')
$hashes = foreach ($source in $sources) {
    $path = Join-Path $repoRoot $source
    [ordered]@{path=$source;bytes=(Get-Item -LiteralPath $path).Length;sha256=(Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash}
}
$external = 'C:\Users\RZ1\Desktop\RZ\261008-MIT-Ecco\04-Project\01-ECCO_First_Ping-Test\01-Blender\Source_Imported_ecco.blend'
$result = [ordered]@{
    checkedAtUtc=[DateTime]::UtcNow.ToString('o');kind='A04 records self-check';root=$repoRoot
    links=$links;sectionFrames=$allocations;totalFrames=2160;fpsProposed=24;durationSeconds=90
    sources=$hashes;externalCandidate=[ordered]@{path=$external;exists=(Test-Path -LiteralPath $external);sha256=(Get-FileHash -LiteralPath $external -Algorithm SHA256).Hash}
    limitations=@('No scene opened or modified','No render/playblast produced or visually verified','External candidate is not an approved master','A02/A03 outputs may change concurrently','Final delivery settings unconfirmed')
}
$result | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $verificationPath -Encoding utf8
if (!(Test-Path -LiteralPath $verificationPath)) { throw 'Verification evidence not saved' }
Write-Output "PASS: $($docs.Count) documents, $($links.Count) links, 7 contiguous sections, 2160 frames / 90 seconds."
