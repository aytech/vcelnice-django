#!/usr/bin/env bash

rm --force vcelnice.zip &&
(
  cd client && npm install --force && npm run build && (
    cd dist &&
      sed -i 's+styles.css+/assets/styles.css+g' index.html &&
      sed -i 's+runtime.js+/assets/runtime.js+g' index.html &&
      sed -i 's+polyfills.js+/assets/polyfills.js+g' index.html &&
      sed -i 's+scripts.js+/assets/scripts.js+g' index.html &&
      sed -i 's+main.js+/assets/main.js+g' index.html
  )
) && python manage.py collectstatic --noinput \
  && zip -r \
    --exclude=*client/.angular* \
    --exclude=*client/dist* \
    --exclude=*client/e2e* \
    --exclude=*client/node_modules* \
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
    --exclude=*tests* \
    --exclude=*vcelnice/logs* \
    --exclude=*vcelnice/media* \
    --exclude=*vcelnice/common/credentials* \
    --exclude=*.venv* \
    --exclude=*.git* \
    --exclude=*.idea* \
    --exclude=*__pycache__* \
    --exclude=*db.sqlite3* \
    --exclude=*.env.tmpl* \
    --exclude=*.gitignore* \
    --exclude=*app.py* \
    --exclude=*build.sh* \
    --exclude=*builder.yml* \
    --exclude=*Dockerfile* \
    --exclude=*manage.py* \
    --exclude=*README.md* \
    --exclude=*requirements.txt* \
    --exclude=*resources.txt* \
    vcelnice.zip .
