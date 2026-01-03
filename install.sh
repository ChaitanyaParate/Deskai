#!/usr/bin/env bash
set -e

PROJECT_DIR="$(pwd)"

echo "[deskai] Creating virtual environment..."
python3 -m venv desk

echo "[deskai] Installing dependencies..."
./desk/bin/pip install --upgrade pip
./desk/bin/pip install -r requirements.txt

echo "[deskai] Checking for Ollama..."

if ! command -v ollama >/dev/null 2>&1; then
    echo "[deskai] Ollama not found. Installing..."

    OS="$(uname -s)"
    if [ "$OS" != "Linux" ]; then
        echo "[deskai] Unsupported OS: $OS"
        exit 1
    fi

    curl -fsSL https://ollama.com/install.sh | sh
fi

echo "[deskai] Ensuring Ollama server is running..."

if ! pgrep -f "ollama serve" >/dev/null; then
    nohup ollama serve >/tmp/ollama.log 2>&1 &
fi

echo "[deskai] Waiting for Ollama API..."

for i in {1..30}; do
    if curl -sf http://localhost:11434/api/tags >/dev/null; then
        echo "[deskai] Ollama is ready"
        break
    fi
    sleep 1
done

if ! curl -sf http://localhost:11434/api/tags >/dev/null; then
    echo "[deskai] Ollama failed to start"
    exit 1
fi

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
