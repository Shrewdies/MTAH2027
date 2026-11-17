# Generate the submission from the data bundle inside the container.
#
#   .\scripts\run_protected.ps1 -DataDir <bundle> [-Name submission] [-Profile macro] [-OutDir <dir>]
#
# -DataDir is the folder that contains tactical\BAR-ATH_tactical_atd.txt. The container has no
# network, the repository and data are mounted read-only and only -OutDir is writable.
param(
    [Parameter(Mandatory = $true)][string]$DataDir,
    [string]$OutDir = '',
    [string]$Name = 'submission',
    [ValidateSet('macro', 'balanced', 'spell', 'reasoned')]
    [string]$Profile = 'macro'
)
$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
# Default output folder: beside the repository, never inside it.
if (-not $OutDir) { $OutDir = Join-Path (Split-Path -Parent (Split-Path -Parent $repo)) 'protected_out' }
$DataDir = $DataDir.TrimEnd('\', '/')
$OutDir = $OutDir.TrimEnd('\', '/')

if (-not (docker version --format '{{.Server.Version}}' 2>$null)) {
    Write-Host "Docker engine is not running. Start Docker Desktop and retry."
    exit 1
}
if (-not (Test-Path (Join-Path $DataDir 'tactical\BAR-ATH_tactical_atd.txt'))) {
    Write-Host "Not found: $DataDir\tactical\BAR-ATH_tactical_atd.txt"
    exit 1
}
New-Item -ItemType Directory -Force $OutDir | Out-Null
# Docker reads a relative host path as a volume name, so mount absolute paths only.
$DataDir = (Resolve-Path -LiteralPath $DataDir).Path
$OutDir = (Resolve-Path -LiteralPath $OutDir).Path

docker run --rm --network none --read-only --tmpfs /tmp -e PYTHONDONTWRITEBYTECODE=1 `
    -e MTAH_DATA_DIR=/data `
    -v "${repo}:/work:ro" -v "${DataDir}:/data:ro" -v "${OutDir}:/out" `
    mtah2027:dev sh -c "python -m possession.run --profile $Profile --out /out/$Name.csv --diagnostics /out/$Name.diagnostics.json && python evaluation/validate_submission.py /out/$Name.csv" `
    2>&1 | ForEach-Object { "$_" }
exit $LASTEXITCODE
