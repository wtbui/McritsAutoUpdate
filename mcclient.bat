@echo off
REM ==========================================
REM  build.bat - multi-task version
REM ==========================================

IF "%1"=="" (
    GOTO usage
)

IF "%1"=="install" (
    GOTO install
)

IF "%1"=="run" (
    SHIFT
    GOTO run
)

IF "%1"=="shell" (
    GOTO shell
)

IF "%1"=="clean" (
    GOTO clean
)

:usage
echo Usage: build.bat install - run - shell - clean
echo
echo   install   Create venv (if missing) and install requirements
echo   run       Activate venv and run main.py (you can pass flags after run)
echo   shell     Activate venv, then drop into a new cmd shell
echo   clean     Remove the venv folder

REM Option A: Just pause so user can read it
pause
exit /b 0

REM Option B: Or open a new shell that stays open
REM cmd /k
REM exit /b 0


:install
echo == Installing ==
IF NOT exist venv (
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install --upgrade pip --user
pip install --user -r requirements.txt
pip install --user easyocr
exit /b 0

:run
echo == Running main.py ==

:: Activate the virtual environment
call venv\Scripts\activate.bat

:: Initialize an empty variable for new arguments
set "new_args="

:: Loop through all arguments, skipping the first one
setlocal enabledelayedexpansion
set i=0
for %%A in (%*) do (
    if !i! GTR 0 (
        set "new_args=!new_args! %%A"
    )
    set /a i+=1
)

:: Pass the new arguments to the Python script
python main %new_args%
exit /b 0


:shell
echo == Starting a shell with venv active ==
call venv\Scripts\activate.bat
cmd /k
exit /b 0


:clean
echo == Removing the venv folder ==
rmdir /s /q venv
exit /b 0