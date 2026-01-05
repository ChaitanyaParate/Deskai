# DeskAI

DeskAI is a **local-first desktop intelligence daemon** that continuously observes your active desktop context and allows you to interact with it using natural language via a lightweight CLI.  
It runs fully **offline**, powered by **local LLMs through Ollama**, and is designed to behave like a background system service rather than a typical app.

This project intentionally focuses on **systems-level engineering**: IPC, background services, streaming inference, and OS integration.

---

## Table of Contents
- Overview
- Why DeskAI
- Architecture
- Tech Stack
- Core Concepts
- Features
- Installation
- Usage
- Services & Startup
- Error Handling Philosophy
- Project Structure
- Development Notes
- Future Work
- License

---

## Overview

DeskAI runs as a **user-level daemon** that:
- Tracks desktop context (window under cursor, screen state, text signals)
- Routes user intents from a CLI
- Streams responses from a locally running LLM
- Automatically starts on login

The user interacts with DeskAI through the `deskai` command without worrying about starting servers or managing processes.

---

## Why DeskAI?

Most AI assistants:
- Depend on cloud APIs
- Have no awareness of your desktop
- Are UI-heavy and slow for developers

DeskAI is different:
- 100% local
- CLI-first
- Streaming responses
- Deep OS integration

It is meant to feel like a **system utility**, not an app.

---
## What this project demonstrates

- Daemon design
- IPC
- systemd
- Streaming systems

---
## Architecture

DeskAI uses a **daemon–client model** with UNIX sockets for IPC.

```
User Command
   |
   v
deskai CLI
   |
   | UNIX socket
   v
DeskAI Daemon
   |
   | subprocess
   v
Ollama LLM (phi3 / mistral)
```

### Runtime Flow

1. systemd starts DeskAI on login
2. Daemon initializes context loop
3. CLI connects via socket
4. Intent is inferred and routed
5. LLM streams tokens
6. Tokens are forwarded to CLI
7. Client exits, daemon stays alive

---

## Tech Stack

| Layer | Technology |
|-----|------------|
| Language | Python 3.10+ (tested on 3.10–3.12)|
| LLM Runtime | Ollama |
| Ollama | v0.1+ |
| Models | phi3:mini (default) |
| IPC | UNIX domain sockets |
| Service Manager | systemd (user) |
| Environment | Python venv |
| OS | Linux |

---

## Core Concepts

### Daemon State
A persistent global state tracks:
- Screen context
- Window Under Cursor
- Text streaks
- Last interaction metadata

### Streaming First
Responses are streamed token-by-token.  
No buffering. No waiting for full output.

### Local-Only
No HTTP APIs, no telemetry, no cloud calls.

---

## Features

- Background daemon
- Automatic startup on login
- Local LLM inference
- Streaming output
- Intent-based command routing
- CLI-first UX
- No hardcoded paths after install

---

## Installation

DeskAI is installed using **install.sh**, which configures everything correctly.

### Requirements
- Linux
- Python 3.10+
- systemd user sessions
- curl

### Install

```bash
git clone https://github.com/ChaitanyaParate/Deskai.git
cd Deskai
chmod +x install.sh
./install.sh
```
Clone inside Downloads folder

### What install.sh Does

- Creates Python venv (`desk/`)
- Installs dependencies
- Installs Ollama if missing
- Starts Ollama server
- Pulls required LLM model
- Installs systemd user services
- Enables auto-start
- Installs `deskai` CLI

---

## Commands & CLI Usage

#### deskai read
Reads the current ScreenContext.

### Run a Task

```bash

deskai stream summarize
deskai stream explain_error
deskai stream search

```

### Check Service

```bash
systemctl --user status deskai
```

### Restart and Stop

```bash
systemctl --user restart deskai
systemctl --user stop deskai
```

### Logs

```bash
journalctl --user -u deskai -f
```

---

## Services & Startup

DeskAI installs two user services:

- `deskai.service`
- `ollama.service`

They live in:
```
~/.config/systemd/user/
```

They are enabled automatically and start on login.

---

## Error Handling Philosophy

- `BrokenPipeError` is expected when clients exit early
- Daemon never crashes on client failure
- Restart handled by systemd
- Streaming errors are logged, not fatal

---

## Project Structure

```
deskai/
├── main.py          
├── client.py        
├── state.py         
│
├── capture/
│   ├── backend.py
│   ├── screen.py
│   └── windows.py
│
├── context_model/
│   ├── dataset.py
│   ├── infer.py
│   ├── model.py
│   ├── train.py
│   └── type.py
│
├── daemon/
│   └── loop.py

├── dataset/
│   └── data.json

├── intent/
│   ├── router/
│   │    └── router.py
│   │  
│   └── executo/
│       ├── handlers/
│       │   ├── explain_error.py
│       │   ├── summarize.py
│       │   └── search.py
│       │
│       └── executor.py
│
├── llm/
│   ├── factory.py
│   ├── local.py
│   └── openai_client.py
│
├── ocr/
│   ├── engine.py
│   ├── postprocess.py
│   └── types.py
│
├── deskai.sh        # CLI wrapper
├── install.sh       # Installer
├── deskai.service   # systemd service
├── ollama.service
└── requirements.txt
```

---

## Development Notes

This project intentionally avoids:
- Framework-heavy abstractions
- Cloud dependencies
- GUI complexity

It focuses on:
- OS-level correctness
- Robust streaming
- Process lifecycle management

---

## Known Limitations

- Linux using X11 only
- Requires systemd user sessions
- LLM latency depends on model size
- No sandboxing between intents yet
- No GUI feedback


## Future Work

- **Cloud LLM Integration**
  - Optional support for hosted LLM APIs such as OpenAI (ChatGPT), Azure OpenAI, Anthropic, and Gemini.
  - Runtime model selection between local (Ollama) and cloud providers based on latency, cost, or task complexity.
  - Secure API key management via environment variables or OS keyrings.

- **GUI Overlay**
  - Lightweight desktop overlay for displaying responses, context state, and streaming outputs.
  - Configurable hotkeys for invoking tasks without terminal interaction.

- **Plugin-Based Intent System**
  - Pluggable intent architecture allowing third-party extensions without modifying core logic.
  - Dynamic intent discovery and registration at runtime.

- **Multi-Model Routing**
  - Automatic routing between vision, text, and code-specialized models.
  - Confidence-based or cost-aware model selection.

- **Persistent Memory**
  - Long-term memory storage for user preferences, frequent workflows, and historical context.
  - Optional vector database backend for semantic recall across sessions.


## License

MIT License

---

## Author

Chaitanya Parate  
Built as a systems-level learning project focused on:

- systemd
- Linux services
- Streaming LLM inference
