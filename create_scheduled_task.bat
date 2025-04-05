@echo off
color 0F

:: Check for administrative privileges
net session >nul 2>&1
if %errorlevel% == 0 (
    echo Running with administrative privileges.
) else (
    echo Requesting administrative privileges...
    powershell -Command "Start-Process '%~f0' -Verb runAs"
    exit /b
)

set HOME_DIR=%~dp0

schtasks /create /tn Prefect /tr "cmd /c %HOME_DIR%start_prefect.vbs" /sc onlogon /ru "%username%"  /f

@echo off
color 0A
REM echo ***************************************
REM echo On task scheduler, go to the "Prefect" task and edit: 
REM echo Settings: Uncheck "Stop the task if it runs longer than"
REM echo If you don't want a cmd window to pop: General : Run wetheer the user is logged on or not
REM echo ***************************************
REM pause
