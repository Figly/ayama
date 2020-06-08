#!/usr/bin/env bash
set -efu
set -o pipefail

PROJECT_ZONE='europe-west1-d'
PRODUCTION_PROJECT='ayama-production'
STAGING_PROJECT='ayama-staging'

#gcloud --project "${PRODUCTION_PROJECT}" container clusters get-credentials "" --zone "${PROJECT_ZONE}"
gcloud --project "${STAGING_PROJECT}" container clusters get-credentials "carignan" --zone "${PROJECT_ZONE}"
