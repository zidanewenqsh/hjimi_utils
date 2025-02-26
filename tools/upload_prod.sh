#!/bin/bash
# Build package
python3 -m build

# Upload to PyPI
echo "Uploading to PyPI..."
if command -v python3 &> /dev/null; then
    # Linux/Mac
    python -m twine upload --repository pypi dist/*
else
    # Windows
    python -m twine upload --repository pypi dist/*
fi

echo "Upload to PyPI completed!" 