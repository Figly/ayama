#!/usr/bin/env bash
set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
BASE_DIR=$(dirname "${SCRIPTS_DIR}")
KUBERNETES_DIR="${BASE_DIR}/kubernetes"
KUBERNETES_BUILD_DIR="${KUBERNETES_DIR}/build"

. "${SCRIPTS_DIR}/_common.sh" "${1:-}"

set +f
rm -f "${KUBERNETES_DIR}"/*.yml
set -f

POD_TEMPLATE="${KUBERNETES_BUILD_DIR}/pod-migration.yml"
jinja2 "${KUBERNETES_DIR}/pod-migration-base.yml.j2" > "${POD_TEMPLATE}"

POD_NAME="${APP_NAME}-migration"

if "${ANNOUNCE_ENABLED}"; then
  announce "Starting to run migration of ${IMAGE_URL}"
fi

echo "The pod might not exist:"
set +e
kubectl delete -f "${POD_TEMPLATE}"
set -e

echo "Waiting for pods to be cleaned up:"
while true; do
  if [[ ! "$(kubectl get -f "${POD_TEMPLATE}" -o=name)" ]]; then
    break
  fi
done

# Config Maps
create_configmap

# Secrets Maps
create_secret

echo "Starting to run migration:"
kubectl apply -f "${POD_TEMPLATE}"

while true; do
  POD_STATUS=$(kubectl get -f "${POD_TEMPLATE}" -o=jsonpath='{.status.phase}')

  case $POD_STATUS in
    Succeeded)
      echo
      echo "Migration completed!"
      echo
      break
      ;;
    Failed)
      echo
      echo 'Migration seems to have failed'
      echo
      exit 1
      ;;
    Running)
      echo "*** ATTACHING TO POD DOING MIGRATION ***"
      set +e
      kubectl attach "${POD_NAME}"
      set -e
      ;;
    Pending)
      echo "Pod still pending..."
      ;;
  esac
done

echo 'Fetching all logs'
kubectl logs "${POD_NAME}"

mv "${POD_TEMPLATE}" "${POD_TEMPLATE}.bak"

if "${ANNOUNCE_ENABLED}"; then
  announce "${IMAGE_URL} Migration complete! :tada:"
fi
