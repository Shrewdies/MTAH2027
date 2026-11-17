# Score a single submission against the public 5-minute window (alignment and format check).
#
#   .\scripts\public_check.ps1 -File submission.csv [-OutDir <dir>]
#
# The file is copied alone into its own folder so that exactly one submission is scored.
param(
    [Parameter(Mandatory = $true)][string]$File,
    [string]$OutDir = ''
)
$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
# Default output folder: beside the repository, never inside it.
if (-not $OutDir) { $OutDir = Join-Path (Split-Path -Parent (Split-Path -Parent $repo)) 'protected_out' }
$OutDir = $OutDir.TrimEnd('\', '/')
$check = Join-Path $OutDir 'public_check'
if (Test-Path $check) { Remove-Item -Recurse -Force $check }
New-Item -ItemType Directory -Force $check | Out-Null
# Docker reads a relative host path as a volume name, so mount an absolute path only.
$check = (Resolve-Path -LiteralPath $check).Path
Copy-Item (Join-Path $OutDir $File) $check

docker run --rm --network none --read-only --tmpfs /tmp -e PYTHONDONTWRITEBYTECODE=1 `
    -v "${repo}:/work:ro" -v "${check}:/check" mtah2027:dev `
    python evaluation/run_evaluation.py --gt public --results /check --out /check/reports --no-detail `
    2>&1 | ForEach-Object { "$_" }
exit $LASTEXITCODE
