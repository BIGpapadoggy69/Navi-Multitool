@echo off
chcp 65001 >nul
title Navi Multitool - Installer
color 0b

echo ======================================================
echo           NAVI MULTITOOL INSTALLER
echo ======================================================
echo.

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
    goto python_found
)

py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=py
    goto python_found
)

color 0c
echo ======================================================
echo             ERROR: PYTHON NOT FOUND
echo ======================================================
echo.
echo Python is not installed or not in PATH.
echo.
echo 1. Download: https://www.python.org/downloads/
echo 2. Run the installer.
echo 3. Check "Add python.exe to PATH" at the bottom.
echo 4. Click "Install Now".
echo 5. Restart this installer.
echo.
pause
exit /b 1

:python_found
echo [+] Python found (%PYTHON_CMD%)
echo.

%PYTHON_CMD% -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Pip not found. Trying to restore...
    %PYTHON_CMD% -m ensurepip --default-pip >nul 2>&1
    %PYTHON_CMD% -m pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        color 0c
        echo ======================================================
        echo               ERROR: PIP NOT FOUND
        echo ======================================================
        echo.
        echo Run this manually to fix it:
        echo    %PYTHON_CMD% -m ensurepip --default-pip
        echo.
        pause
        exit /b 1
    )
)

echo [*] Installing dependencies from requirements.txt...
echo.
%PYTHON_CMD% -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    color 0c
    echo.
    echo [!] Some dependencies failed to install.
    echo [!] Check your internet connection or run as Administrator.
    echo.
    echo To retry manually:
    echo    %PYTHON_CMD% -m pip install -r requirements.txt
) else (
    color 0a
    echo.
    echo [+] Installation complete!
    echo [+] Run the tool with start.bat or main.py
)

echo.
pause
