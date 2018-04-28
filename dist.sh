#!/bin/bash

UPLOAD_PACKAGE=$1

# Build Source Distribution
python setup.py sdist

# Build universal package (--universal defaulted on setup.cfg)
python setup.py bdist_wheel

# Upload to Pypi
#if [ "$UPLOAD_PACKAGE" -eq '--upload-pypi' ]; then
#    twine upload dist/*
#fi