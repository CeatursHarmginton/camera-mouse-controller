@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: ══════════════════════════════════════════════════
::  NonMouse - Camera Mouse Controller
::  Auto-setup & run script
:: ══════════════════════════════════════════════════

title NonMouse - Camera Mouse Controller

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║     🖐️  NonMouse - Camera Mouse Controller   ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: ──────────────────────────────────────────────────
::  Step 1: Check Python installation
:: ──────────────────────────────────────────────────
echo  [1/4] Checking Python installation...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo  ❌ ERROR: Python is not installed or not in PATH!
    echo.
    echo  Please install Python 3.8+ from:
    echo  https://www.python.org/downloads/
    echo.
    echo  ⚠️  Make sure to check "Add Python to PATH" during installation!
    echo.
    goto :error_exit
)

:: Get Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo        ✅ Python %PYVER% found

:: Check minimum version (3.8+)
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (
    set PYMAJOR=%%a
    set PYMINOR=%%b
)
if %PYMAJOR% LSS 3 (
    echo  ❌ ERROR: Python 3.8+ required, found %PYVER%
    goto :error_exit
)
if %PYMAJOR% EQU 3 if %PYMINOR% LSS 8 (
    echo  ❌ ERROR: Python 3.8+ required, found %PYVER%
    goto :error_exit
)

:: ──────────────────────────────────────────────────
::  Step 2: Check / Create virtual environment
:: ──────────────────────────────────────────────────
echo  [2/4] Checking virtual environment...

if not exist "venv\Scripts\activate.bat" (
    echo        ⏳ Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo  ❌ ERROR: Failed to create virtual environment!
        echo  Try: python -m pip install --upgrade pip virtualenv
        goto :error_exit
    )
    echo        ✅ Virtual environment created
    
    :: Force install on first run
    set NEED_INSTALL=1
) else (
    echo        ✅ Virtual environment exists
    set NEED_INSTALL=0
)

:: Activate venv
call venv\Scripts\activate.bat

:: ──────────────────────────────────────────────────
::  Step 3: Check / Install dependencies
:: ──────────────────────────────────────────────────
echo  [3/4] Checking dependencies...

:: Quick check: try importing critical packages
set MISSING=0

python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: opencv-python
    set MISSING=1
)

python -c "import mediapipe" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: mediapipe
    set MISSING=1
)

python -c "import numpy" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: numpy
    set MISSING=1
)

python -c "import keyboard" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: keyboard
    set MISSING=1
)

python -c "import pynput" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: pynput
    set MISSING=1
)

python -c "from PIL import Image" >nul 2>&1
if %errorlevel% neq 0 (
    echo        ⚠️  Missing: Pillow
    set MISSING=1
)

if %NEED_INSTALL% EQU 1 set MISSING=1

if %MISSING% EQU 1 (
    echo.
    echo        ⏳ Installing dependencies... (this may take a few minutes)
    echo        ───────────────────────────────────────────
    
    :: Upgrade pip first
    python -m pip install --upgrade pip >nul 2>&1
    
    :: Install all requirements
    pip install -r requirements.txt
    
    if %errorlevel% neq 0 (
        echo.
        echo  ❌ ERROR: Failed to install some dependencies!
        echo.
        echo  Common fixes:
        echo    1. pip install --upgrade pip setuptools wheel
        echo    2. Install Visual C++ Build Tools:
        echo       https://visualstudio.microsoft.com/visual-cpp-build-tools/
        echo    3. Try: pip install mediapipe --no-cache-dir
        echo.
        goto :error_exit
    )
    
    echo.
    echo        ✅ All dependencies installed successfully!
) else (
    echo        ✅ All dependencies are installed
)

:: ──────────────────────────────────────────────────
::  Step 4: Launch NonMouse
:: ──────────────────────────────────────────────────
echo  [4/4] Launching NonMouse...
echo.
echo  ═══════════════════════════════════════════════
echo   💡 Tips:
echo     • CapsLock ON  = Hand tracking ACTIVE
echo     • CapsLock OFF = Hand tracking PAUSED
echo     • Press ESC or close window to quit
echo  ═══════════════════════════════════════════════
echo.

python -m nonmouse
set EXIT_CODE=%errorlevel%

if %EXIT_CODE% neq 0 (
    echo.
    echo  ⚠️  NonMouse exited with error code %EXIT_CODE%
    echo.
    if %EXIT_CODE% EQU 1 (
        echo  Possible causes:
        echo    • No camera detected
        echo    • Camera is in use by another app
        echo    • Permission denied (try Run as Administrator)
    )
)

goto :clean_exit

:error_exit
echo.
echo  ══════════════════════════════════════════
echo   Setup failed. Please fix the errors above.
echo  ══════════════════════════════════════════

:clean_exit
echo.
echo  Press any key to exit...
pause >nul
endlocal
