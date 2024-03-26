#! /bin/bash

source env/env.sh

yoyo-migrate apply --batch

cd clean_architecture_example/ || exit 1

gunicorn -c gunicorn.conf.py
