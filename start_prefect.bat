@REM @echo off

cd /d "%~dp0"
set PREFECT_HOME=%CD%


uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api 

call .venv\Scripts\activate.bat

prefect server stop

prefect server start -b 

prefect worker start --pool WorkPool 

prefect server stop