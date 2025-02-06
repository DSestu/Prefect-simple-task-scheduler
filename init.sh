#!/bin/bash

cd "$(dirname "$0")"

curl -LsSf https://astral.sh/uv/install.sh | sh

pkill python 

rm -rf .venv

uv venv

uv sync

uv pip install -e .