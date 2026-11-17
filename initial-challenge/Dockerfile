# Runtime for the possession pipeline: CPython 3.11 with pinned numpy and pandas.
# Multi-arch (linux/arm64, linux/amd64). Source code and data are mounted at run time, never baked in.
#
#   docker build -t mtah2027:dev .
#
# If ./wheels contains the pinned wheels (scripts/fetch_wheels.*) the build is fully offline;
# otherwise the same pinned versions are installed from PyPI.
FROM python:3.11.11-slim-bookworm@sha256:081075da77b2b55c23c088251026fb69a7b2bf92471e491ff5fd75c192fd38e5

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# "wheel[s]" matches nothing when the folder is absent, so the copy never fails.
COPY requirements-solution.txt wheel[s] /tmp/build/
RUN set -eu; \
    if ls /tmp/build/*.whl >/dev/null 2>&1; then \
        pip install --no-index --no-deps --find-links /tmp/build -r /tmp/build/requirements-solution.txt; \
    else \
        pip install --no-deps --timeout 120 --retries 10 -r /tmp/build/requirements-solution.txt; \
    fi; \
    rm -rf /tmp/build; \
    python -c "import numpy, pandas; print('numpy', numpy.__version__, 'pandas', pandas.__version__)"

WORKDIR /work
