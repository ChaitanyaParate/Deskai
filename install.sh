#!/usr/bin/env bash
set -e

echo "[deskai] Creating virtual environment..."
python3 -m venv desk

echo "[deskai] Activating desk..."
source desk/bin/activate

echo "[deskai] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[deskai] Installing user systemd service..."
mkdir -p ~/.config/systemd/user
sed "s|{{DESKAI_PATH}}|$PWD|g" deskai.service \
  > ~/.config/systemd/user/deskai.service

curl -fsSL https://ollama.com/install.sh | sh

ollama pull mistral

mkfifo /tmp/deskai_cmd

mkdir -p ~/.local/bin
mv deskai ~/.local/bin/


systemctl --user daemon-reload
systemctl --user enable deskai
systemctl --user start deskai

echo "[deskai] Installation complete."
