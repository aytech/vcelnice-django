#!/usr/bin/env bash

npm run build && cd dist \
    && sed -i 's+styles.css+/assets/styles.css+g' index.html \
    && sed -i 's+runtime.js+/assets/runtime.js+g' index.html \
    && sed -i 's+polyfills.js+/assets/polyfills.js+g' index.html \
    && sed -i 's+scripts.js+/assets/scripts.js+g' index.html \
    && sed -i 's+main.js+/assets/main.js+g' index.html \
    && zip -r ../build.zip .