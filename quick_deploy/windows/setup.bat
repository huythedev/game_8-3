@echo off
echo ===================================
echo Setting up String Transformer App
echo ===================================

:: Create virtual environment if it doesn't exist
if not exist "..\..\venv" (
    echo Creating virtual environment...
    python -m venv ..\..\venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call ..\..\venv\Scripts\activate.bat

:: Install requirements
echo Installing dependencies...
pip install -r ..\..\requirements.txt

echo ===================================
echo Setup complete! To run the app:
echo 1. Use run.bat to start the application
echo 2. Access the app at http://localhost:5000
echo ===================================
