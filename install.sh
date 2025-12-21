#!/usr/bin/env bash
set -e

echo "[deskai] Creating virtual environment..."
python3 -m venv venv

echo "[deskai] Activating venv..."
source venv/bin/activate

echo "[deskai] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[deskai] Installing user systemd service..."
mkdir -p ~/.config/systemd/user
sed "s|{{DESKAI_PATH}}|$PWD|g" deskai.service \
  > ~/.config/systemd/user/deskai.service

systemctl --user daemon-reload
systemctl --user enable deskai
systemctl --user start deskai

echo "[deskai] Installation complete."
