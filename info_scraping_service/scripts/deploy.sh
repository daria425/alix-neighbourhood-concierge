#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: You forgot to set the GOOGLE_PROJECT_ID love."
  echo "Usage: $0 <GOOGLE_PROJECT_ID>, not difficult"
  exit 1
fi

GOOGLE_PROJECT_ID="$1"

IMAGE_TAG="europe-west2-docker.pkg.dev/${GOOGLE_PROJECT_ID}/neighbourhood-concierge-scraper/app:latest"

gcloud builds submit --tag ${IMAGE_TAG}
