#!/bin/bash
echo "==================================="
echo "Starting String Transformer App in Production Mode"
echo "==================================="

# Navigate to app root directory
cd ../..

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Set environment variables for production
export FLASK_ENV=production
export DEBUG=False
export SECURE_COOKIES=True

# Check for gunicorn and install if needed
if ! pip show gunicorn > /dev/null; then
    echo "Installing gunicorn WSGI server..."
    pip install gunicorn
fi

# Run the app with gunicorn
echo "Starting production server with gunicorn..."
gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:application
