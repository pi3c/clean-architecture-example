#! /bin/bash

source scripts/env.sh

cd clean_architecture_example/ || exit 1

gunicorn -c gunicorn.conf.py
