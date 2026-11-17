# Optional: download the pinned linux/arm64 CPython 3.11 wheels for an offline image build.
$ErrorActionPreference = 'Stop'
$repo = Split-Path -Parent $PSScriptRoot
python -I -m pip download --only-binary=:all: `
    --platform manylinux2014_aarch64 --platform manylinux_2_17_aarch64 --platform manylinux_2_28_aarch64 `
    --python-version 3.11 --implementation cp --abi cp311 --abi none --no-deps `
    --timeout 120 --retries 10 `
    -r (Join-Path $repo 'requirements-solution.txt') -d (Join-Path $repo 'wheels')
