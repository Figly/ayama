#!/usr/bin/env bash
set -efu
set -o pipefail

IMAGE="ayama"

BASE_DIR=$(pwd)

HASH=$(git rev-parse --short=8 HEAD)

DOCKERFILE=$BASE_DIR/Dockerfile

IMAGE_NAME=$IMAGE:$HASH

ENVIRONMENT=${1:-dev}

# Set the environment variables
. $BASE_DIR/scripts/_common.sh
# Set the common functions
. $BASE_DIR/scripts/_functions.sh

# Build image url for cloud source
if [[ -n "${PROJECT_ID}" ]]; then
  IMAGE_NAME=eu.gcr.io/${PROJECT_ID}/$IMAGE_NAME
fi

announce "Building $IMAGE_NAME :building_construction:"

# Actually build the image
docker build --pull -t "${IMAGE_NAME}" -f "${DOCKERFILE}" "${BASE_DIR}"

# If it is cloud hosted push it
if [[ -n "${PROJECT_ID}" ]]; then
  announce "Started pushing image ${IMAGE_NAME}"

  docker push ${IMAGE_NAME}

fi
announce "${IMAGE_NAME} successfully built. :tada:"
