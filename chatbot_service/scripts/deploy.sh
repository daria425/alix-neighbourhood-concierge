#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: You forgot to set the GOOGLE_PROJECT_ID love 😕."
  echo "Usage: $0 <GOOGLE_PROJECT_ID>, not difficult"
  exit 1
fi

GOOGLE_PROJECT_ID="$1"

IMAGE_TAG="europe-west2-docker.pkg.dev/${GOOGLE_PROJECT_ID}/neighbourhood-concierge-chatbot/app:latest"
echo "Deployment of chatbot service starting 🌺"
echo "Check this"
echo "
          /\
         (  )
      .--.\/.--.
     (/`\_\/_/`\)
     '  {____}  '  
       ,_//\\_,
        '-\/-' 
          /\
         (  )
      .--.\/.--.
     (/`\_\/_/`\)
     '  {____}  '
       ,_//\\_,
        '-\/-'
"
gcloud builds submit --tag ${IMAGE_TAG}