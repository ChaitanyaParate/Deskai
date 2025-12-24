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

#curl -fsSL https://ollama.com/install.sh | sh

ollama pull mistral

if [[ ! -p /tmp/deskai_cmd ]]; then
  mkfifo /tmp/deskai_cmd
fi

mkdir -p ~/.local/bin
install -m 755 deskai.sh ~/.local/bin/deskai

echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc

systemctl --user daemon-reload
systemctl --user enable deskai
systemctl --user start deskai

echo "[deskai] Installation complete."
