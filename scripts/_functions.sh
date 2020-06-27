#!/usr/bin/env bash
#
# Library of common repo-agnostic functions

set -efu
set -o pipefail

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
BASE_DIR=$(dirname "${SCRIPTS_DIR}")

announce () {
  # If announce is enabled push the message to slack, else show it locally.
  if [[ ${ANNOUNCE_ENABLED} = true ]]; then
    curl -X POST -H "Content-type: application/json" --data "{\"text\": \"*${ANNOUNCE_PREFIX}:* $1 ${ANNOUNCE_SUFFIX}\"}" ${SLACK_CHANNEL}
  else
    echo $1
  fi
}

get_pod () {
  PODS=$(kubectl get po -l app="${APP_NAME}" -o=jsonpath='{.items[*].metadata.name}')
  EXAMPLE_POD=$(echo "$PODS" | awk '{ print $1 }')

  PREFIX=${1:-}

  if [[ -z "$PREFIX" ]]; then
    echo 'Please provide a pod name or prefix'
    echo "e.g. ${EXAMPLE_POD}"
    exit 1
  fi

  echo "Looking for pods that match ${PREFIX}"

  for pod in $PODS; do
    if echo "${pod}" | grep -q "${PREFIX}"; then
      echo "Connecting to pod ${pod}"
      return
    fi
  done

  echo 'No pods found'
  exit 1
}

check_deployments() {
  deployments=( "$@" )
  for deployment in ${deployments[@]}; do
    (
      kubectl rollout status "${deployment}"
    ) &
  done
}

check_all_deployments () {
  DEPLOYMENTS=$(kubectl get deployments -o name -l "app=${APP_NAME}")
  check_deployments "${DEPLOYMENTS}"

  wait
}

create_configmap () {
  if [ -f "${KUBERNETES_DIR}/configmaps/${ENVIRONMENT}.env" ]; then
    kubectl create configmap "${APP_NAME}-env" \
      --from-env-file="${KUBERNETES_DIR}/configmaps/${ENVIRONMENT}.env" \
      --dry-run -oyaml | kubectl apply -f -
  fi
}

create_secret () {
  if [ -f "${KUBERNETES_DIR}/secrets/${ENVIRONMENT}.env" ]; then
    kubectl create secret generic "${APP_NAME}-env" \
      --from-env-file="${KUBERNETES_DIR}/secrets/${ENVIRONMENT}.env" \
      --dry-run -oyaml | kubectl apply -f -
  fi
}

git_status () {
  curl -u # TODO - REAUTH git to pull commit history -H "Content-Type: applicat
ion/json" -X POST -d "{
    \"state\": \"$1\",
    \"description\": \"$2\",
    \"context\": \"$3\"
  }"https://api.github.com/repos/Figly/$GIT_REPO_NAME/statuses/$(git rev-parse HEAD)" > /dev/null
}


jinja2 () {
  set -- --strict --format=yml -D environment="${ENVIRONMENT}" -D git_sha="${HASH}" -D image_url="${IMAGE_URL}" "$@"
  if [[ "${ENVIRONMENT}" == "dev" ]]; then
    set -- -D source_path="${SOURCE_PATH}" "$@"
  elif [[ "${ENVIRONMENT}" == "env" ]]; then
    set -- -D env_subdomain="${ENV_SUBDOMAIN}" -D kubectl_namespace="${KUBECTL_NAMESPACE}" "$@"
  elif [[ -n ${KUBECTL_NAMESPACE:-} ]] ; then
    set -- -D kubectl_namespace="${KUBECTL_NAMESPACE}" "$@"
  fi
  if [[ ! "${OVERRIDE:-}" == "true" ]]; then
    set -- "$@" "${BASE_DIR}/kubectl.yml"
  fi
  $(which jinja2) "$@"
}

kubectl () {
  if [[ -n ${KUBECTL_NAMESPACE:-} ]]; then
    set -- --namespace "${KUBECTL_NAMESPACE}" "$@"
  fi
  $(which kubectl) --context "${KUBECTL_CONTEXT}" "$@"
}

stern () {
  if [[ "${ENVIRONMENT}" == "env" ]]; then
    set -- --namespace "${KUBECTL_NAMESPACE}" "$@"
  fi
  $(which stern) --context "${KUBECTL_CONTEXT}" "$@"
}

jinja () {
  set -- --strict --format=yml -D environment="${ENVIRONMENT}" -D git_sha="${HASH}" -D image_url="${IMAGE_URL}" "$@"
  if [[ "${ENVIRONMENT}" == "dev" ]]; then
    set -- -D source_path="${SOURCE_PATH}" "$@"
  elif [[ "${ENVIRONMENT}" == "env" ]]; then
    set -- -D env_subdomain="${ENV_SUBDOMAIN}" -D kubectl_namespace="${KUBECTL_NAMESPACE}" "$@"
  elif [[ -n ${KUBECTL_NAMESPACE:-} ]] ; then
    set -- -D kubectl_namespace="${KUBECTL_NAMESPACE}" "$@"
  fi
  if [[ ! "${OVERRIDE:-}" == "true" ]]; then
    set -- "$@" "${BASE_DIR}/postctl.yml"
  fi
  $(which jinja2) "$@"
}

export announce
export check_all_deployments
export create_configmap
export create_secret
export get_pod
export git_status
export jinja2
export jinja
export kubectl
export stern
