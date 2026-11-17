# Run the test suite in the container (no network, no match data).
$ErrorActionPreference = 'Continue'
$repo = Split-Path -Parent $PSScriptRoot
docker run --rm --network none -e PYTHONDONTWRITEBYTECODE=1 -v "${repo}:/work:ro" mtah2027:dev `
    python -m unittest discover -s possession/tests -t . -v 2>&1 | ForEach-Object { "$_" }
exit $LASTEXITCODE
