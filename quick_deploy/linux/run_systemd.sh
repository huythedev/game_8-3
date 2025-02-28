#!/bin/bash
echo "==================================="
echo "Creating systemd service for String Transformer App"
echo "==================================="

# Get absolute paths
APP_DIR=$(cd ../.. && pwd)
VENV_DIR="$APP_DIR/venv"

# Create a systemd service file
SERVICE_FILE="string_transformer.service"
cat > $SERVICE_FILE << EOL
[Unit]
Description=String Transformer Application
After=network.target

[Service]
User=$(whoami)
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="FLASK_ENV=production"
Environment="DEBUG=False"
Environment="SECURE_COOKIES=True"
ExecStart=$VENV_DIR/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOL

echo "Service file created: $SERVICE_FILE"
echo "To install as a system service:"
echo "1. sudo cp $SERVICE_FILE /etc/systemd/system/"
echo "2. sudo systemctl daemon-reload"
echo "3. sudo systemctl enable string_transformer"
echo "4. sudo systemctl start string_transformer"
