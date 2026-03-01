@echo off
setlocal

set VENV_DIR=.venv
set MAIN_SCRIPT=main.py

:: Mostrar ayuda si no hay parámetros
if "%~1"=="" (
    echo Usage: run.bat ^<URL^>
    echo Example: run.bat https://www.example.com
    exit /b 1
)

set URL=%~1

:: Comprobar si existe el entorno virtual
if not exist "%VENV_DIR%" (
    echo Error: Virtual environment not found. Please run install.sh first.
    exit /b 1
)

:: Activar el entorno virtual (Ruta de Windows)
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo Error: Activation script not found in %VENV_DIR%\Scripts.
    exit /b 1
)

:: Ejecutar el script
echo Starting extraction for: %URL%
python "%MAIN_SCRIPT%" "%URL%"

call deactivate
endlocal
