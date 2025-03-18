#!/bin/bash
echo "Setting up the local development environment..."
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Setup complete."
