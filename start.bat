@echo off
TITLE File Upload Server

REM Set the name for the virtual environment directory
SET VENV_NAME=venv

REM Check if the virtual environment directory exists
IF NOT EXIST "%VENV_NAME%" (
    echo --- Creating virtual environment...
    python -m venv "%VENV_NAME%"
    IF %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to create virtual environment.
        echo Please make sure Python is installed and in your PATH.
        pause
        exit /b
    )
)

REM Activate the virtual environment
echo --- Activating virtual environment...
call "%VENV_NAME%\Scripts\activate.bat"

REM Install required packages from requirements.txt
echo --- Installing/checking requirements...
pip install -r requirements.txt --quiet --disable-pip-version-check

REM Run the main Python application
echo --- Starting the server...
python server.py

echo.
echo Server has been shut down.
pause