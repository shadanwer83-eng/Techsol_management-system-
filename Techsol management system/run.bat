@echo off
title Techsol Student Management System
cd /d "%~dp0"

echo ============================================================
echo   Starting Techsol Student Management System...
echo ============================================================

:: Check for python in PATH
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    python main.py
    goto end
)

:: Check for py launcher
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    py main.py
    goto end
)

:: Check common AppData python path
if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    "%LOCALAPPDATA%\Python\bin\python.exe" main.py
    goto end
)

if exist "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" (
    "%LOCALAPPDATA%\Python\pythoncore-3.14-64\python.exe" main.py
    goto end
)

echo.
echo [ERROR] Python was not found on your system!
echo Please ensure Python 3 is installed and added to PATH.
pause

:end
