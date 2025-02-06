cd "$(dirname "$0")"

export PREFECT_HOME=$PWD

export PREFECT_API_URL=http://127.0.0.1:4200/api

uv run prefect server stop

uv run prefect server start -b

echo "Waiting 10 seconds for server before starting worker"

sleep 10

open http://127.0.0.1:4200

uv run prefect worker start --pool WorkPool 

uv run prefect server stop
