#!/usr/bin/env bash
set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
BASE_DIR=$(dirname "${SCRIPTS_DIR}")
POSTGRES_DIR="${BASE_DIR}/services/postgres"
POSTGRES_K8S_DIR="${BASE_DIR}/services/postgres/kubernetes"
POSTGRES_K8S_BUILD_DIR="${BASE_DIR}/services/postgres/kubernetes/build"

mkdir -p ${POSTGRES_K8S_BUILD_DIR}

. "${SCRIPTS_DIR}/_common.sh" "${1:-}"

set +f
rm -f "${POSTGRES_K8S_BUILD_DIR}"/*.yml
set -f

export IMAGE_URL
export HASH
export APP_NAME
export KUBECTL_CONTEXT

if [[ "${ENVIRONMENT}" = "dev" ]]; then
  set +e
  echo
  kubectl apply -f "${POSTGRES_K8S_DIR}/dev/"
  set -e
fi

jinja -D component=app "${POSTGRES_K8S_DIR}/deployment-base.yml.j2" > "${POSTGRES_K8S_BUILD_DIR}/deployments.yml"

if "${ANNOUNCE_ENABLED}"; then
  announce "Starting a deploy of Postgres image: ${IMAGE_URL}"
fi

# Config Maps
if [ -f "${POSTGRES_K8S_DIR}/configmaps/${ENVIRONMENT}.env" ]; then
  kubectl create configmap "${APP_NAME}-postgres-env" \
    --from-env-file="${POSTGRES_K8S_DIR}/configmaps/${ENVIRONMENT}.env" \
    --dry-run=client -oyaml | kubectl apply -f -
fi
# Secrets Maps
if [ -f "${POSTGRES_K8S_DIR}/secrets/${ENVIRONMENT}.env" ]; then
  kubectl create secret generic "${APP_NAME}-postgres-env" \
    --from-env-file="${POSTGRES_K8S_DIR}/secrets/${ENVIRONMENT}.env" \
    --dry-run=client -oyaml | kubectl apply -f -
fi

kubectl apply -f "${POSTGRES_K8S_BUILD_DIR}/"

check_all_deployments

echo "Deployment complete!"

if "${ANNOUNCE_ENABLED}";
then
  announce "Postgres image: ${IMAGE_URL} deploy complete! :tada:"
fi
