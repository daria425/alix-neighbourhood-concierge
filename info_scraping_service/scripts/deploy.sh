#!/bin/bash

if [ -z "$1" ]; then
  echo "Error: You forgot to set the GOOGLE_PROJECT_ID love 😕."
  echo "Usage: $0 <GOOGLE_PROJECT_ID>, not difficult"
  exit 1
fi

GOOGLE_PROJECT_ID="$1"

IMAGE_TAG="europe-west2-docker.pkg.dev/${GOOGLE_PROJECT_ID}/neighbourhood-concierge-scraper/app:latest"
echo "Deployment of info scraping service starting ❤️‍🔥"
echo "Here is a cat to keep you company while you wait"
echo "       \`*-."
echo "        )  _\`-."
echo "       .  : \`. ."
echo "       : _   '  \\"
echo "       ; *\` _.   \`*-._"
echo "       \`-.-'          \`-."
echo "         ;       \`       \`."
echo "         :.       .        \\"
echo "         . \\  .   :   .-'   ."
echo "         '  \`+.;  ;  '      :"
echo "         :  '  |    ;       ;-."
echo "         ; '   : :\`-:     _.\`* ;"
echo "  .*' /  .*' ; .* \`- +'  \`*'"
echo "      \`*-*   \`*-*  \`*-*'"
gcloud builds submit --tag ${IMAGE_TAG}

