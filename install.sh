#!/usr/bin/env bash
set -e

PROJECT_DIR="$(pwd)"

echo "[deskai] Creating virtual environment..."
python3 -m venv desk

echo "[deskai] Installing dependencies..."
./desk/bin/pip install --upgrade pip
./desk/bin/pip install -r requirements.txt

echo "[deskai] Installing Ollama model..."
ollama pull phi3:mini

echo "[deskai] Installing systemd user service..."
mkdir -p ~/.config/systemd/user

sed "s|{{DESKAI_PATH}}|$PROJECT_DIR|g" deskai.service \
  > ~/.config/systemd/user/deskai.service

echo "[deskai] Installing CLI wrapper..."

mkdir -p ~/.local/bin
install -m 755 deskai.sh ~/.local/bin/deskai

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
fi


systemctl --user daemon-reload
systemctl --user enable deskai.service
systemctl --user restart deskai.service

echo "[deskai] Installation complete."
echo "[deskai] Check logs with: journalctl --user -u deskai -f"

