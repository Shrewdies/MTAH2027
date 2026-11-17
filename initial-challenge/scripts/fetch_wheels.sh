#!/usr/bin/env sh
# Optional: download the pinned wheels for an offline image build.
#   scripts/fetch_wheels.sh            # arm64 (Apple silicon, Graviton, Snapdragon)
#   scripts/fetch_wheels.sh x86_64     # amd64
set -eu
ARCH=${1:-aarch64}
REPO=$(cd "$(dirname "$0")/.." && pwd)
python3 -m pip download --only-binary=:all: \
  --platform "manylinux2014_${ARCH}" --platform "manylinux_2_17_${ARCH}" --platform "manylinux_2_28_${ARCH}" \
  --python-version 3.11 --implementation cp --abi cp311 --abi none --no-deps \
  -r "$REPO/requirements-solution.txt" -d "$REPO/wheels"
