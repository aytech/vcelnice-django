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
  --exclude=*client/angular.json* \
  --exclude=*client/karma.conf.js* \
  --exclude=*client/package.json* \
  --exclude=*client/package-lock.json* \
  --exclude=*client/protractor.conf.js* \
  --exclude=*client/proxy.conf.json* \
  --exclude=*client/README.md* \
  --exclude=*client/tsconfig.json* \
  --exclude=*client/tslint.json* \
  --exclude=*.venv* \
  --exclude=*.git* \
  --exclude=*.idea* \
  --exclude=*__pycache__* \
  --exclude=*build.sh* \
  --exclude=*db.sqlite3* \
  --exclude=*vcelnice/logs* \
  --exclude=*vcelnice/media* \
  --exclude=*vcelnice/static_root* \
  --exclude=*resources.txt* \
  --exclude=*README.md* \
  build.zip .
