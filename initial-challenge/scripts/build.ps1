# Build the runtime image: offline when .\wheels holds the pinned wheels (fetch_wheels.ps1),
# from PyPI otherwise.
$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
docker build -t mtah2027:dev $repo 2>&1 | ForEach-Object { "$_" }
exit $LASTEXITCODE
