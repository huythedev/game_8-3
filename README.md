# String Transformer Application

A Flask web application that transforms strings based on predefined patterns with access control and administrative features.

## Overview

The String Transformer application allows users to submit strings and receive transformed versions based on predefined patterns. Key features include:

- **One-Time Access**: Once a transformed string has been viewed, it cannot be accessed again
- **IP-Based Restrictions**: Prevents multiple views from the same IP address
- **Admin Dashboard**: Manage string patterns, users, and view access logs
- **Blueprint Architecture**: Modular code structure for better maintainability
- **Proxy Support**: Properly handles real client IP addresses when behind proxies like Nginx

## Installation

### Prerequisites

- Python 3.6+ 
- pip (Python package manager)
- Git (optional)

### Quick Setup

1. Clone the repository or download the source code:
   ```bash
   git clone https://github.com/yourusername/string-transformer.git
   cd string-transformer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/macOS: `source venv/bin/activate`

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file from the template:
   ```bash
   cp .env.example .env
   ```
   
6. Edit the `.env` file to configure your installation.

7. Run the application:
   ```bash
   python app.py
   ```

## Platform-Specific Quick Deploy

For easy deployment, use the scripts in the `quick_deploy` directory:

### Windows
```
cd quick_deploy\windows
setup.bat
run.bat
```

### Linux
```
cd quick_deploy/linux
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

### macOS
```
cd quick_deploy/macos
chmod +x setup.sh run.sh
./setup.sh
./run.sh
```

## Project Structure

```
game_8-3/
├── .env
├── .env.example
├── .gitattributes
├── app.py                 # Application entry point
├── config.py              # Configuration settings
├── fix_critical_templates.py # Script to fix critical templates
├── fix_database.py        # Script to fix database issues
├── fix_routes.py          # Script to fix route issues
├── generate_key.py        # Script to generate secret keys
├── middleware.py          # Proxy handling middleware
├── models.py              # Database models
├── quick_fix.py           # Script for quick fixes
├── README.md
├── requirements.txt       # Python dependencies
├── reset_database.py      # Script to reset the database
├── utils.py               # Utility functions
├── wsgi.py                # WSGI entry point for production
│
├── instance/              # Instance folder for SQLite database
│
├── logs/                  # Application logs directory
│
├── quick_deploy/          # Deployment scripts
│   ├── linux/
│   │   ├── run.sh
│   │   ├── run_production.sh
│   │   ├── run_systemd.sh
│   │   └── setup.sh
│   │
│   ├── macos/
│   │   ├── run.sh
│   │   └── setup.sh
│   │
│   └── windows/
│       ├── run.bat
│       ├── run_production.bat
│       └── setup.bat
│
├── routes/                # Route blueprints
│   ├── admin.py           # Admin routes
│   ├── errors.py          # Error handlers
│   └── main.py            # Main application routes
│
├── static/                # Static files (CSS, JS, images)
│   └── css/
│       ├── admin.css
│       └── style.css
│
└── templates/             # Jinja2 HTML templates
    ├── admin_dashboard.html
    ├── admin_login.html
    ├── error.html
    ├── index.html
    ├── no_match.html
    └── result.html
```

## Configuration

Configuration is managed through environment variables, which can be set in a `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Flask secret key for session security | Random generated |
| DATABASE_URI | SQLAlchemy database URI | sqlite:///strings.db |
| SECURE_COOKIES | Enable secure cookies | True |
| HOST | Host address to bind | 0.0.0.0 |
| PORT | Port number | 8000 |
| DEBUG | Flask debug mode | False |
| BEHIND_PROXY | Whether app is behind a proxy | False |

## Admin Access

After installation, you can access the admin interface at `/admin/login` with these default credentials:

- **Username**: admin
- **Password**: 123

*Important: Change this password immediately after first login!*

## Production Deployment

### Using Waitress (Windows)

```bash
python -m waitress --host=0.0.0.0 --port=8000 wsgi:application
```

### Nginx Configuration

When using Nginx as a reverse proxy, ensure you have the correct configuration to forward client IP addresses:

```nginx
location / {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

Also, set `BEHIND_PROXY=True` in your `.env` file.

## Troubleshooting

### URL Errors After Refactoring

If you encounter URL building errors after code updates, run the fix script:

```bash
python fix_routes.py
```

### Common Issues

- **Database Errors**: If you encounter database errors, delete the `strings.db` file and restart the application.
- **Permission Denied**: Ensure the directory has proper write permissions for log files.
- **Missing Templates**: Verify templates directory is properly installed.

## Development

### Virtual Environment

Always use a virtual environment for development:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### Installing Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### Running Tests

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Considerations

- The application restricts access to transformed strings based on IP addresses.
- Admin pages require authentication.
- Be cautious about exposing the application directly to the internet without proper security measures.
- Consider changing the default admin password immediately after installation.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
