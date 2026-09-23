@echo off
title Navi Multitool
echo Loading Navi...

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto run_main
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto run_main
)

cls
color 0c
echo ======================================================
echo             ERROR: PYTHON NOT FOUND
echo ======================================================
echo.
echo Python is not installed or not in PATH (environment variable).
echo.
echo Solution:
echo 1. Download Python: https://www.python.org/downloads/
echo 2. Run the installer.
echo 3. IMPORTANT: Check the box at the bottom:
echo    "Add python.exe to PATH" (or "Add Python to PATH")
echo 4. Click "Install Now".
echo 5. Restart this file.
echo.
echo ======================================================
echo.
pause
exit /b

:run_main
%PYTHON_CMD% main.py
if %errorlevel% neq 0 (
    echo.
    echo [!] Navi crashed or exited with an error (Code: %errorlevel%)
    echo [!] Possible causes: Missing libraries, Python not in PATH, or code error.
    echo [!] Try running 'install.bat' to fix library issues.
    echo.
    pause
)


