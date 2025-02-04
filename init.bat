@echo off

powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

uv venv

call .venv\Scripts\activate.bat

uv sync

pause