@echo off
echo ============================================
echo   AUREA PRIME ELITE - Setup Installer
echo   Powered by AlphaEngine
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.9+
    echo Download: https://python.org/downloads
    pause
    exit /b 1
)

echo [1/6] Creating directories...
if not exist "database" mkdir database
if not exist "models" mkdir models
if not exist "logs" mkdir logs
if not exist "data\cache" mkdir data\cache
echo       Done!

echo.
echo [2/6] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo       Virtual environment created!
) else (
    echo       Virtual environment already exists!
)

echo.
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [4/6] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo.
echo [5/6] Installing dependencies...
echo       This may take several minutes...
pip install -r requirements.txt --quiet
echo       Done!

echo.
echo [6/6] Setting up configuration...
if not exist ".env" (
    copy .env.example .env
    echo       .env file created from template!
    echo.
    echo [IMPORTANT] Please edit .env file with your credentials!
) else (
    echo       .env file already exists!
)

echo.
echo ============================================
echo   Setup Complete!
echo ============================================
echo.
echo Next steps:
echo   1. Edit .env file with your credentials
echo   2. Run: start.bat
echo.
pause