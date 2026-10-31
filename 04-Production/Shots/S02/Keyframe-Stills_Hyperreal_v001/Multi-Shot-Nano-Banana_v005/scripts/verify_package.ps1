[CmdletBinding()]
param([string]$PackagePath = (Split-Path -Parent $PSScriptRoot))
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$manifest = Get-Content -LiteralPath (Join-Path $PackagePath 'manifest.json') -Raw | ConvertFrom-Json
$checked = @()
foreach ($item in (@($manifest.inputs) + @($manifest.stills) + @($manifest.selection))) {
    $path = Join-Path $PackagePath $item.file
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $item.sha256) { throw "Hash mismatch: $($item.file)" }
    $checked += $item.file
}
$shotMap = @(Get-Content -LiteralPath (Join-Path $PackagePath 'shot-map.json') -Raw | ConvertFrom-Json)
if ($shotMap.Count -ne 6) { throw 'Expected six individual-shot entries.' }
foreach ($shot in $shotMap) {
    foreach ($relativePath in @($shot.prompt, $shot.input_1, $shot.input_2, $shot.input_3)) {
        if (-not (Test-Path -LiteralPath (Join-Path $PackagePath $relativePath) -PathType Leaf)) {
            throw "Missing shot input/prompt: $relativePath"
        }
    }
}
$grid = [Drawing.Bitmap]::new((Join-Path $PackagePath $manifest.inputs[0].file))
$panelChecks = @()
try {
    if ($grid.Width -ne 2880 -or $grid.Height -ne 1080) { throw 'Grid dimensions changed.' }
    for ($i = 0; $i -lt 6; $i++) {
        $still = $manifest.stills[$i]
        $tile = [Drawing.Bitmap]::new((Join-Path $PackagePath $still.file))
        $crop = $null
        $streamCrop = $null
        $streamTile = $null
        try {
            if ($tile.Width -ne 960 -or $tile.Height -ne 540) { throw "Still dimensions changed: $($still.file)" }
            $x = ($i % 3) * 960
            $y = [int][Math]::Floor($i / 3) * 540
            $crop = $grid.Clone([Drawing.Rectangle]::new($x, $y, 960, 540), [Drawing.Imaging.PixelFormat]::Format32bppArgb)
            $rect = [Drawing.Rectangle]::new(0, 0, 960, 540)
            $cropData = $crop.LockBits($rect, [Drawing.Imaging.ImageLockMode]::ReadOnly, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
            $tileData = $tile.LockBits($rect, [Drawing.Imaging.ImageLockMode]::ReadOnly, [Drawing.Imaging.PixelFormat]::Format32bppArgb)
            try {
                if ($cropData.Stride -ne $tileData.Stride) { throw 'Unexpected pixel stride mismatch.' }
                $length = [Math]::Abs($cropData.Stride) * 540
                $cropBytes = [byte[]]::new($length)
                $tileBytes = [byte[]]::new($length)
                [Runtime.InteropServices.Marshal]::Copy($cropData.Scan0, $cropBytes, 0, $length)
                [Runtime.InteropServices.Marshal]::Copy($tileData.Scan0, $tileBytes, 0, $length)
                $hasher = [Security.Cryptography.SHA256]::Create()
                try {
                    $cropHash = [BitConverter]::ToString($hasher.ComputeHash($cropBytes))
                    $tileHash = [BitConverter]::ToString($hasher.ComputeHash($tileBytes))
                } finally { $hasher.Dispose() }
                if ($cropHash -ne $tileHash) { throw "Grid tile differs from selected still: $($still.file)" }
            } finally {
                $crop.UnlockBits($cropData)
                $tile.UnlockBits($tileData)
            }
            $panelChecks += [pscustomobject]@{id=$still.id;frame=$still.native_frame;position=$still.position;width=960;height=540;pixel_match=$true}
        } finally {
            if ($crop) { $crop.Dispose() }
            $tile.Dispose()
        }
    }
} finally { $grid.Dispose() }
$report = [ordered]@{
    package_checks_passed = $true
    sha256_verified_files = $checked
    grid = @{width=2880;height=1080;columns=3;rows=2;aspect='8:3';source_pixels_preserved=$true}
    panels = $panelChecks
    complete_individual_prompts = $shotMap.Count
    image_generation_run = $false
    source_blender_modified = $false
}
$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $PackagePath 'verification.json') -Encoding utf8
[pscustomobject]@{VerifiedHashes=$checked.Count;ExactGridPanels=$panelChecks.Count;IndividualPrompts=$shotMap.Count;Passed=$true}
