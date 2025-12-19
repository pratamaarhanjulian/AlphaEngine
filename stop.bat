@echo off
echo ============================================
echo   AUREA PRIME ELITE - Stopping Services
echo ============================================
echo.

echo Stopping all Python processes...
taskkill /f /im python.exe >nul 2>&1

echo.
echo All services stopped!
echo.
pause