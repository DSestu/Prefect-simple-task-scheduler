cd "$(dirname "$0")"

# fix for prefect relative path
uv run update_prefect_path.py

uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api

uv run prefect deploy --all

rm prefect.yaml

