#!/usr/bin/env bash
#
# Repo-specific config, that is used across other scripts and in _funcions.sh
#
# :treat:

set -efu
set -o pipefail

APP_NAME="ayama"
GIT_REPO_NAME="ayama"
PROJECT_ZONE=europe-west1-d
CURRENT_USER="$(USER)"
OS="$(uname -s)"

ENVIRONMENT=${1:-}

if [ -z "${ENVIRONMENT}" ]; then
  echo 'Please provide an environment when running this command'
  echo 'e.g. scripts/test.sh staging'
  exit 1;
fi

case "${ENVIRONMENT}" in
    production)
        CLUSTER="pangea"
        PROJECT_ID=figly-production
        KUBECTL_NAMESPACE="default"
        KUBECTL_CONTEXT="gke_${PROJECT_ID}_${PROJECT_ZONE}_${CLUSTER}"
        SLACK_CHANNEL="https://hooks.slack.com/services/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"
        ANNOUNCE_PREFIX=":rocket: production"
        ANNOUNCE_ENABLED=true
    ;;

    staging)
        CLUSTER="suburbia"
        PROJECT_ID=figly-staging
        KUBECTL_NAMESPACE="default"
        KUBECTL_CONTEXT="gke_${PROJECT_ID}_${PROJECT_ZONE}_${CLUSTER}"
        SLACK_CHANNEL="https://hooks.slack.com/services/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"
        ANNOUNCE_PREFIX=":construction: staging"
        ANNOUNCE_ENABLED=true
    ;;

    dev)
        CLUSTER=
        PROJECT_ID=
        KUBECTL_NAMESPACE=default
        KUBECTL_CONTEXT="minikube"
        SLACK_CHANNEL=""
        ANNOUNCE_PREFIX=""
        ANNOUNCE_ENABLED=false
    ;;

    *)
        echo "Try one of the following environments:"
        echo "   dev, staging, production"
        exit 1
    ;;
esac

if "${ANNOUNCE_ENABLED}"; then
  ANNOUNCE_PREFIX="${ANNOUNCE_PREFIX}/${APP_NAME}"
  ANNOUNCE_SUFFIX="(by *${CURRENT_USER}*)"
fi

case "$KUBECTL_CONTEXT" in
  "")
    echo "Not switching context, we're already there"
    ;;

  minikube)
    eval "$(minikube docker-env)"
    if [[ $(kubectl config use-context "${KUBECTL_CONTEXT}") ]]; then
      echo "Successfully changed context: ${KUBECTL_CONTEXT}"
    else
      echo "Looks like you aren't running minikube"
      exit 1
    fi
    ;;

  *)
    echo "Attempting to fetch context from gcloud: ${KUBECTL_CONTEXT}"
    gcloud --project "${PROJECT_ID}" container clusters get-credentials "${CLUSTER}" --zone "${PROJECT_ZONE}"
    kubectl config use-context "${KUBECTL_CONTEXT}"
    echo "Successfully changed context: ${KUBECTL_CONTEXT}"
    # We only switch context to check if the client has the necessary context in
    # their '~/.kube/config', as soon as we've written a CLI that reads that YAML
    # file we won't need to do this anymore.
    #
    # We explicitly set context for all 'kubectl' calls, so this is okay.
    if [[ "${USER}" != "jenkins" ]]; then
      set +e
      eval "$(minikube docker-env)"
      kubectl config use-context minikube
      set -e
    fi
    ;;
esac

SCRIPTS_DIR=$(dirname "$(python3 -c "import os; print(os.path.realpath('$0'))")")
echo "${SCRIPTS_DIR}"
BASE_DIR=$(dirname "${SCRIPTS_DIR}")
echo "${BASE_DIR}"

if [[ "${ENVIRONMENT}" == "dev" ]]; then
  SOURCE_PATH="${BASE_DIR}/src"
  export SOURCE_PATH
fi

HASH=$(git rev-parse --short=8 HEAD)

if [[ -z "$PROJECT_ID" ]]; then
  IMAGE_URL="${APP_NAME}:${HASH}"
else
  IMAGE_URL="eu.gcr.io/${PROJECT_ID}/${APP_NAME}:${HASH}"
fi

# shellcheck source=_functions.sh
. "${SCRIPTS_DIR}/_functions.sh"

export ANNOUNCE_ENABLED
export ANNOUNCE_PREFIX
export ANNOUNCE_SUFFIX
export APP_NAME
export CURRENT_USER
export ENVIRONMENT
export GIT_REPO_NAME
export IMAGE_URL
export KUBECTL_CONTEXT
export OS
export PROJECT_ID
export SLACK_CHANNEL
export announce
export check_all_deployments
export get_pod
export git_status
