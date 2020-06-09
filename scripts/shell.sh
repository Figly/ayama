#!/usr/bin/env bash
set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")

# shellcheck source=_common.sh
. "${SCRIPTS_DIR}/_common.sh" "${1:-}"

get_pod "${2:-app}"
kubectl exec -it "${pod}" -- bash
