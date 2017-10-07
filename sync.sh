#!/bin/bash

rsync -r \
    -avz \
    --progress \
    --exclude '.remote-sync.json' \
    --exclude '.git/**' \
    --exclude '.tox/**' \
    --exclude 'env/**' \
    --exclude '**.py[cod]' \
    --exclude '**.log*' \
    --exclude '**.env.ini' \
    --exclude '**.pem' \
    --exclude '**.crt' \
    --exclude '.vscode/**' \
    --exclude 'ignore/**' \
    --exclude '.gitbase' \
    --exclude '**_flymake.py' \
    --exclude '**node_modules**' \
    --exclude '**__pycache__**' \
    . $1
