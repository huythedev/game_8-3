#!/bin/bash
echo "==================================="
echo "Setting up String Transformer App"
echo "==================================="

# Navigate to app root directory
cd ../..

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

echo "==================================="
echo "Setup complete! To run the app:"
echo "1. Use run.sh to start the application"
echo "2. Access the app at http://localhost:5000"
echo "==================================="

# Make run scripts executable
chmod +x quick_deploy/macos/run.sh
chmod +x quick_deploy/macos/run_production.sh
