#!/usr/bin/env sh
# Linux / macOS entry point.
#
#   scripts/run.sh build
#   scripts/run.sh test
#   scripts/run.sh submit <data_dir> [out_dir] [profile]
#   scripts/run.sh check <out_dir>/<file>.csv
#
# <data_dir> is the folder that contains tactical/BAR-ATH_tactical_atd.txt. [out_dir] defaults to
# the git-ignored outputs folder next to scripts, [profile] to macro.
set -eu

IMAGE=mtah2027:dev
REPO=$(cd "$(dirname "$0")/.." && pwd)

case "${1:-}" in
  build)
    docker build -t "$IMAGE" "$REPO"
    ;;
  test)
    docker run --rm --network none -v "$REPO:/work:ro" "$IMAGE" \
      python -m unittest discover -s possession/tests -t . -v
    ;;
  submit)
    DATA=$(cd "${2:?data dir}" && pwd)
    OUT=$(mkdir -p "${3:-$REPO/outputs}" && cd "${3:-$REPO/outputs}" && pwd)
    PROFILE=${4:-macro}
    docker run --rm --network none --read-only --tmpfs /tmp -e MTAH_DATA_DIR=/data \
      -v "$REPO:/work:ro" -v "$DATA:/data:ro" -v "$OUT:/out" "$IMAGE" \
      sh -c "python -m possession.run --profile $PROFILE --out /out/submission.csv \
             --diagnostics /out/diagnostics.json && python evaluation/validate_submission.py /out/submission.csv"
    ;;
  check)
    FILE=$(cd "$(dirname "${2:?csv}")" && pwd)/$(basename "$2")
    CHECK=$(mktemp -d)
    cp "$FILE" "$CHECK/"
    docker run --rm --network none -v "$REPO:/work:ro" -v "$CHECK:/check" "$IMAGE" \
      python evaluation/run_evaluation.py --gt public --results /check --out /check/reports --no-detail
    ;;
  *)
    sed -n '2,10p' "$0"
    exit 2
    ;;
esac
