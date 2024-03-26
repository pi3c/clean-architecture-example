#! /bin/bash

source env/.env

cd clean_architecture_example/ || exit 1

gunicorn -c gunicorn.conf.py
