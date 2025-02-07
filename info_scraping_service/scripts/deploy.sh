#!/bin/bash

GOOGLE_PROJECT_ID="$1"

IMAGE_TAG="europe-west2-docker.pkg.dev/${GOOGLE_PROJECT_ID}/neighbourhood-concierge-scraper/app:latest"

gcloud builds submit --tag ${IMAGE_TAG}
