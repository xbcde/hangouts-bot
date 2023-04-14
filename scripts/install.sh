#!/bin/sh

python3 -m venv venv
. venv/bin/activate

python -m pip install --upgrade pip
pip install -r ./scripts/requirements.txt

pre-commit install
pre-commit install -t commit-msg
