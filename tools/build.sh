#!/bin/bash

python -m build
python -m twine upload dist/*
python -m twine upload --repository testpypi dist/* --verbose
python -m twine upload --repository pypi dist/*
