#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.local/share/deskai"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo "[deskai] Installing to $INSTALL_DIR"

mkdir -p "$INSTALL_DIR"
rsync -a --delete . "$INSTALL_DIR"

cd "$INSTALL_DIR"

sudo apt install git-lfs
git lfs install
git clone https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2

echo "[deskai] Creating virtual environment..."
python3 -m venv venv

echo "[deskai] Installing dependencies..."
"$INSTALL_DIR/venv/bin/pip" install --upgrade pip
"$INSTALL_DIR/venv/bin/pip" install -r requirements.txt

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

echo "[deskai] Installing systemd user services..."
mkdir -p "$SYSTEMD_USER_DIR"

sed "s|{{DESKAI_PATH}}|$INSTALL_DIR|g" deskai.service \
  > "$SYSTEMD_USER_DIR/deskai.service"

sed "s|{{DESKAI_PATH}}|$INSTALL_DIR|g" ollama.service \
  > "$SYSTEMD_USER_DIR/ollama.service"

echo "[deskai] Installing CLI wrapper..."
mkdir -p "$HOME/.local/bin"
install -m 755 deskai.sh "$HOME/.local/bin/deskai"

if ! echo "$PATH" | grep -q "$HOME/.local/bin"; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
fi

systemctl --user daemon-reload
systemctl --user enable deskai.service
systemctl --user restart deskai.service

echo "[deskai] Installation complete."
echo "[deskai] Logs: journalctl --user -u deskai -f"
