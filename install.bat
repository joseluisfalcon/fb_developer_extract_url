@echo off
setlocal enabledelayedexpansion

set VENV_DIR=.venv
set CONFIG_FILE=config_facebook_developer.json
set SAMPLE_FILE=config_facebook_developer.json.sample

echo --- Facebook Developer URL Extractor Setup (Windows) ---

:: 0. Check Prerequisites
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Error: Python is not installed or not in PATH.
    exit /b 1
)

pip --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [!] Error: pip is not installed or not in PATH.
    exit /b 1
)
if not exist "%VENV_DIR%" (
    echo [*] Creating virtual environment...
    python -m venv "%VENV_DIR%"
) else (
    echo [✓] Virtual environment already exists.
)

:: 2. Activate Virtual Environment
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo [!] Error: Could not find activation script in %VENV_DIR%\Scripts.
    exit /b 1
)

:: 3. Install/Update Dependencies
echo [*] Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

:: 4. Check for Playwright
python -c "import playwright" 2>nul
if %ERRORLEVEL% neq 0 (
    echo [!] Playwright not found after installation. Something went wrong.
) else (
    echo [*] Ensuring Playwright browsers are installed...
    playwright install chromium
)

:: 5. Check for Config File
if not exist "%CONFIG_FILE%" (
    echo.
    echo [!] WARNING: %CONFIG_FILE% not found.
    echo     Please create it based on the sample file:
    echo     copy %SAMPLE_FILE% %CONFIG_FILE%
    echo     Then edit %CONFIG_FILE% with your credentials/cookies.
) else (
    echo [✓] Config file found.
)

echo.
echo --- Installation Complete ---
echo You can now run the tool using: run.bat ^<URL^>

call deactivate
endlocal
