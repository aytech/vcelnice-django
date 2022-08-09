#!/usr/bin/env bash

(
  cd client && npm run build && (
    cd dist &&
      sed -i 's+styles.css+/assets/styles.css+g' index.html &&
      sed -i 's+runtime.js+/assets/runtime.js+g' index.html &&
      sed -i 's+polyfills.js+/assets/polyfills.js+g' index.html &&
      sed -i 's+scripts.js+/assets/scripts.js+g' index.html &&
      sed -i 's+main.js+/assets/main.js+g' index.html
  )
) && zip -r \
  --exclude=*node_modules* \
  --exclude=*.angular* \
  --exclude=*client/e2e* \
  --exclude=*client/src* \
  --exclude=*client/.editorconfig* \
  --exclude=*client/*.js* \
  --exclude=*client/*.json* \
  --exclude=*.venv* \
  --exclude=*.git* \
  --exclude=*.idea* \
  --exclude=*__pycache__* \
  --exclude=*build.sh* \
  --exclude=*vcelnice/logs* \
  --exclude=*vcelnice/media* \
  --exclude=*vcelnice/static_root* \
  --exclude=*resources.txt* \
  --exclude=*README.md* \
  build.zip .
