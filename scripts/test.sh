#!/usr/bin/env bash
set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
BASE_DIR=$(dirname "${SCRIPTS_DIR}")
KUBERNETES_DIR="${BASE_DIR}/kubernetes"
KUBERNETES_BUILD_DIR="${KUBERNETES_DIR}/build"

# shellcheck source=_build.sh
. "${SCRIPTS_DIR}/_build.sh" "${1:-}"

set +f
rm -f "${KUBERNETES_DIR}"/*.yml
set -f

POD_TEMPLATE="${KUBERNETES_BUILD_DIR}/pod-tests.yml"
jinja2 "${KUBERNETES_DIR}/pod-tests-base.yml.j2" > "${POD_TEMPLATE}"

POD_NAME="${APP_NAME}-tests"

if "${ANNOUNCE_ENABLED}"; then
  announce "Starting to run tests of ${IMAGE_URL}"
fi

echo "The pod might not exist:"
set +e
kubectl delete -f "${POD_TEMPLATE}"
set -e

echo "Waiting for pods to be cleaned up:"
while true; do
  if [[ ! "$(kubectl get -f "${POD_TEMPLATE}" -a -o=name)" ]] ; then
    break
  fi
done

# Config Maps
create_configmap

# Secrets Maps
create_secret

echo "Starting to run tests:"
kubectl create -f "${POD_TEMPLATE}"
git_status "pending" "Running tests" "tests/${ENVIRONMENT}-$(whoami)"

while true; do
  POD_STATUS=$(kubectl get -f "${POD_TEMPLATE}" -a -o=jsonpath='{.status.phase}')

  case $POD_STATUS in
    Succeeded)
      echo
      echo "Tests completed!"
      echo
      break
      ;;
    Failed)
      echo
      echo 'Tests seems to have failed'
      echo
      set +e
      kubectl logs "${POD_NAME}"
      set -e
      if "${ANNOUNCE_ENABLED}"; then
        git_status "failure" "Tests failed" "tests/${ENVIRONMENT}-$(whoami)"
        announce "Tests for ${IMAGE_URL} seemed to have failed... :disappointed:"
        set +e
        LOG_OUTPUT=$(kubectl logs "${POD_NAME}" | grep "Tests:" )
        announce "Tests output: ${LOG_OUTPUT}"
        set -e
      fi
      exit 1
      ;;
    Running)
      echo "*** ATTACHING TO POD DOING TESTS ***"
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


git_status "success" "Tests succeeded!" "tests/${ENVIRONMENT}-$(whoami)"
if "${ANNOUNCE_ENABLED}"; then
  announce "${IMAGE_URL} Tests complete! :tada:"
fi
