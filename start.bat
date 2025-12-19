@echo off
echo ============================================
echo   AUREA PRIME ELITE - Starting Services
echo   Powered by AlphaEngine
echo ============================================
echo.

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Check .env
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please run setup.bat first and configure .env
    pause
    exit /b 1
)

echo [1/3] Starting WebSocket Server...
start "WebSocket Server" cmd /k "python -m mt5.websocket_server"
timeout /t 2 /nobreak >nul

echo [2/3] Starting Telegram Bot...
start "Telegram Bot" cmd /k "python -m bot.telegram_bot"
timeout /t 2 /nobreak >nul

echo [3/3] Starting News Monitor...
start "News Monitor" cmd /k "python -m news.news_notifier"

echo.
echo ============================================
echo   All Services Started!
echo ============================================
echo.
echo Running services:
echo   - WebSocket Server (Port 8080)
echo   - Telegram Bot
echo   - News Monitor
echo.
echo To stop all services, run: stop.bat
echo.
pause