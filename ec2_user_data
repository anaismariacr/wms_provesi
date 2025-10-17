#!/bin/bash
# cloud-init / user-data for EC2 to prepare MonitoringApp (Ubuntu 24.04)
# Este script corre al inicio. Edita DB_HOST manualmente si tu DB está en otra instancia.
set -ex

# Update
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y git python3 python3-pip python3-venv build-essential

# Create app dir
cd /home/ubuntu
if [ ! -d MonitoringApp ]; then
  git clone https://github.com/ISIS2503/ISIS2503-MonitoringApp.git
fi
cd ISIS2503-MonitoringApp
git fetch --all
git checkout Load-Balancer || true

# Create venv and install
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
# --break-system-packages might be needed interactively; trying simple install
pip install -r requirements.txt || true

# NOTE: settings.py needs DB host adjustment. We'll leave migration to manual step. To run server at boot:
cat > /etc/systemd/system/monitoringapp.service <<'EOF'
[Unit]
Description=MonitoringApp Django service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/ISIS2503-MonitoringApp
Environment=PATH=/home/ubuntu/ISIS2503-MonitoringApp/venv/bin
ExecStart=/home/ubuntu/ISIS2503-MonitoringApp/venv/bin/python3 manage.py runserver 0.0.0.0:8080
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable service (won't run migrations; run migrations manually from one instance)
systemctl daemon-reload
systemctl enable monitoringapp.service
systemctl start monitoringapp.service || true

# For debugging, write a ready file
echo "ready" > /home/ubuntu/.monitoringapp_ready
chown ubuntu:ubuntu /home/ubuntu/.monitoringapp_ready
