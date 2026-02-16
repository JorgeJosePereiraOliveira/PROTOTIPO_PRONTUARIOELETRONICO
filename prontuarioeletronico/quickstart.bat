@echo off
REM Quick Start Guide for Windows - Prontuário Eletrônico

echo ================================================
echo Prontuario Eletronico - Quick Start (Windows)
echo ================================================
echo.

REM Check Python version
echo Checking Python installation...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Run tests
echo Running tests...
python -m pytest tests.py -v
echo.

REM Start development server
echo Starting development server...
echo API will be available at: http://localhost:8000
echo Swagger UI at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn src.infra.api.main:app --reload --host 0.0.0.0 --port 8000

pause
