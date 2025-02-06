#!/bin/bash

# Get current user and absolute path
CURRENT_USER=$USER
SCRIPT_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/start_prefect.sh"

# Remove existing service if it exists
sudo systemctl stop prefect 2>/dev/null
sudo systemctl disable prefect 2>/dev/null
sudo rm /etc/systemd/system/prefect.service 2>/dev/null

# Create new service file
sudo tee /etc/systemd/system/prefect.service << EOF
[Unit]
Description=Prefect Service
After=network.target

[Service]
Type=simple
User=${CURRENT_USER}
Environment=PATH=/home/${CURRENT_USER}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=${SCRIPT_PATH}
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable prefect
sudo systemctl start prefect
