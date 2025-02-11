#!/bin/bash
# Build package
python3 -m build

# Upload to TestPyPI
echo "Uploading to TestPyPI..."
if command -v python3 &> /dev/null; then
    # Linux/Mac
    python3 -m twine upload --repository testpypi dist/*
else
    # Windows
    py -m twine upload --repository testpypi dist/*
fi

echo "Upload to TestPyPI completed!"

