#!/bin/bash
# build
py -m build

# upload
# linux script to upload the package to the testpypi repository
# This script will upload the package to the testpypi repository
python3 -m twine upload --repository testpypi dist/*
# This script will upload the package to the pypi repository
python3 -m twine upload --repository pypi dist/*
# windows script to upload the package to the testpypi repository
# This script will upload the package to the testpypi repository
py -m twine upload --repository testpypi dist/*
# This script will upload the package to the pypi repository
py -m twine upload --repository pypi dist/*
# set TWINE_PASSWORD
