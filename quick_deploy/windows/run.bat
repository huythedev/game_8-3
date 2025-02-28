@echo off
echo ===================================
echo Starting String Transformer App
echo ===================================

:: Activate virtual environment
echo Activating virtual environment...
call ..\..\venv\Scripts\activate.bat

:: Run the app
echo Starting Flask application...
cd ..\..
python app.py

:: Deactivate when done (this may not execute if app is terminated with Ctrl+C)
call venv\Scripts\deactivate.bat
