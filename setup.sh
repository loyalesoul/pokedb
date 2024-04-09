#!/bin/bash

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null
then
    echo "pre-commit not found, installing..."
    pip install pre-commit
fi

# Install pre-commit hooks
pre-commit install

# Install dependencies from requirements.txt
pip install -r requirements.txt

echo "Setup completed successfully."

