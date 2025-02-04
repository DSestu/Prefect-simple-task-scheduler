@echo off

@cd /d "%~dp0"

REM fix for prefect relative path. Override path manually with a script and trash the temporary yaml afterwards
uv run update_prefect_path.py

uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

uv run prefect deploy --all

del prefect.yaml
