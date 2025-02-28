#!/bin/bash
echo "==================================="
echo "Starting String Transformer App"
echo "==================================="

# Navigate to app root directory
cd ../..

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Run the app
echo "Starting Flask application..."
python app.py
