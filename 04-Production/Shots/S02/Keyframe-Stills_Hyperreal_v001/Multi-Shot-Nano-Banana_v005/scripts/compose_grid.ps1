<#
Creates a clean, unscaled grid from equal-sized opaque images on Windows.
Example: ./compose_grid.ps1 -ImagePaths $approvedPaths -Columns 3 -OutputPath ./reference-grid.png
Frame approval is a conversational prerequisite, not something this script grants.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string[]]$ImagePaths,
    [Parameter(Mandatory=$true)][ValidateRange(1,128)][int]$Columns,
    [Parameter(Mandatory=$true)][string]$OutputPath
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
if ($ImagePaths.Count -eq 0 -or $ImagePaths.Count % $Columns -ne 0) {
    throw 'Image count must fill every row exactly; confirm a suitable layout.'
}
$target = [IO.Path]::GetFullPath($OutputPath)
if ([IO.Path]::GetExtension($target) -ine '.png') { throw 'Output must use .png.' }
if (Test-Path -LiteralPath $target) { throw 'Output exists; choose a new versioned filename.' }
$images = [Collections.Generic.List[System.Drawing.Image]]::new()
$canvas = $null
$graphics = $null
$stream = $null
try {
    foreach ($path in $ImagePaths) {
        $images.Add([Drawing.Image]::FromFile([IO.Path]::GetFullPath($path)))
    }
    $tileWidth = $images[0].Width
    $tileHeight = $images[0].Height
    foreach ($im in $images) {
        if ($im.Width -ne $tileWidth -or $im.Height -ne $tileHeight) {
            throw 'All panels must have identical dimensions. Resolve resizing/cropping explicitly first.'
        }
    }
    $rows = [int]($images.Count / $Columns)
    $canvas = [Drawing.Bitmap]::new($Columns*$tileWidth, $rows*$tileHeight)
    $graphics = [Drawing.Graphics]::FromImage($canvas)
    $graphics.CompositingMode = [Drawing.Drawing2D.CompositingMode]::SourceCopy
    for ($i=0; $i -lt $images.Count; $i++) {
        $x = ($i % $Columns)*$tileWidth
        $y = [int][Math]::Floor($i / $Columns)*$tileHeight
        # Explicit pixel rectangles avoid DPI-dependent physical-size scaling.
        $destination = [Drawing.Rectangle]::new($x, $y, $tileWidth, $tileHeight)
        $graphics.DrawImage($images[$i], $destination, 0, 0, $tileWidth, $tileHeight, [Drawing.GraphicsUnit]::Pixel)
    }
    $parent = [IO.Path]::GetDirectoryName($target)
    [IO.Directory]::CreateDirectory($parent) | Out-Null
    $stream = [IO.File]::Open($target, [IO.FileMode]::CreateNew, [IO.FileAccess]::Write)
    $canvas.Save($stream, [Drawing.Imaging.ImageFormat]::Png)
    [pscustomobject]@{ Path=$target; Panels=$images.Count; Columns=$Columns; Rows=$rows; Width=$canvas.Width; Height=$canvas.Height }
} finally {
    if ($stream) { $stream.Dispose() }
    if ($graphics) { $graphics.Dispose() }
    if ($canvas) { $canvas.Dispose() }
    foreach ($im in $images) { $im.Dispose() }
}
