# Render every slide of the deck to PNG with PowerPoint (Windows, Office installed) for review.
# The deck is opened read-only and closed without saving.
#   .\tools\report\render-deck.ps1                      # -> tools\report\.cache\deck-pages
param(
    [string]$Deck = (Join-Path $PSScriptRoot "..\..\report\the-shrewdies-technical-report.pptx"),
    [string]$OutDir = (Join-Path $PSScriptRoot ".cache\deck-pages"),
    [int]$Width = 1600
)
$ErrorActionPreference = "Stop"
$Deck = (Resolve-Path $Deck).Path
New-Item -ItemType Directory -Force $OutDir | Out-Null
Get-ChildItem $OutDir -Filter "slide-*.png" | Remove-Item -Force
$OutDir = (Resolve-Path $OutDir).Path

$app = New-Object -ComObject PowerPoint.Application
try {
    # Open(FileName, ReadOnly, Untitled, WithWindow)
    $pres = $app.Presentations.Open($Deck, -1, 0, 0)
    try {
        $height = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
        foreach ($slide in $pres.Slides) {
            $file = Join-Path $OutDir ("slide-{0:D2}.png" -f $slide.SlideIndex)
            $slide.Export($file, "PNG", $Width, $height)
        }
        "{0} slides -> {1}" -f $pres.Slides.Count, $OutDir
    } finally { $pres.Close() }
} finally { $app.Quit() }
