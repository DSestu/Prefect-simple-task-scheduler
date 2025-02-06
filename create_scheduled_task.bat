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

schtasks /create /tn Prefect /tr "cmd /k %HOME_DIR%\start_prefect.bat" /sc onlogon /ru "%username%"  /f

@echo off
color 0A
echo ***************************************
echo On task scheduler, go to the "Prefect" task and edit: 
echo Settings: Uncheck "Stop the task if it runs longer than"
echo If you don't want a cmd window to pop: General : Run wetheer the user is logged on or not
echo ***************************************
pause
