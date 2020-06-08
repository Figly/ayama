#!/usr/bin/env bash
set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
BASE_DIR=$(dirname "${SCRIPTS_DIR}")
KUBERNETES_DIR="${BASE_DIR}/kubernetes"
KUBERNETES_BUILD_DIR="$KUBERNETES_DIR/build"

mkdir -p ${KUBERNETES_BUILD_DIR}

. "${SCRIPTS_DIR}/_common.sh" "${1:-}"

set +f
rm -f "${KUBERNETES_BUILD_DIR}"/*.yml
set -f

export IMAGE_URL
export HASH
export APP_NAME
export KUBECTL_CONTEXT

if [[ "${ENVIRONMENT}" = "dev" ]]; then
  set +e
  echo
  echo "Ignore 'already exists' errors:"
  kubectl apply -f "${KUBERNETES_DIR}/dev/"
  set -e
fi

CRON_DIR=${BASE_DIR}/configs/crons
for f in $(find ${CRON_DIR} -name '*-cron.j2'); do
  cat ${BASE_DIR}/kubectl.yml $f | OVERRIDE=true jinja2 -D component=app "${KUBERNETES_DIR}/cron-jobs-base.yml.j2" > "${KUBERNETES_BUILD_DIR}/$(basename $f .j2).yml"
done

jinja2 -D component=app "${KUBERNETES_DIR}/deployment-base.yml.j2" > "${KUBERNETES_BUILD_DIR}/deployment.yml"

if "${ANNOUNCE_ENABLED}"; then
  announce "Starting a deploy of ${IMAGE_URL}"
fi

# Config Maps
create_configmap

# Secrets Maps
create_secret

kubectl apply -f "${KUBERNETES_BUILD_DIR}/"

check_all_deployments

echo "Deployment complete!"

if "${ANNOUNCE_ENABLED}";
then
  announce "${IMAGE_URL} deploy complete! :tada:"
fi
