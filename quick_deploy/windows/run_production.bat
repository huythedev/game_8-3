@echo off
echo ===================================
echo Starting String Transformer App in Production Mode
echo ===================================

:: Activate virtual environment
echo Activating virtual environment...
call ..\..\venv\Scripts\activate.bat

:: Set environment variables for production
set FLASK_ENV=production
set DEBUG=False
set SECURE_COOKIES=True

:: Run with waitress for production (install it if not present)
echo Checking for waitress WSGI server...
pip show waitress >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Installing waitress WSGI server...
    pip install waitress
)

:: Run the app with waitress
echo Starting production server with waitress...
cd ..\..
python -m waitress --host=0.0.0.0 --port=5000 wsgi:application

:: Deactivate when done
call venv\Scripts\deactivate.bat
