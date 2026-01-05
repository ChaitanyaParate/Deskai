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

- Design of long-running user-level Linux daemons
- systemd user service configuration and lifecycle management
- Client–daemon IPC using UNIX domain sockets
- Token-level streaming pipelines with fault-tolerant client handling
- Local-first system design with zero cloud dependencies

---
## Architecture

DeskAI uses a daemon–client architecture with UNIX domain sockets to decouple long-running system state from short-lived CLI invocations.


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
Local LLM Runtime (Ollama)
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
| Display Server | X11 |
| LLM Runtime | Ollama |
| Ollama | v0.1+ |
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
Commands demonstrate intent routing and streaming execution rather than end-user features.

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
- Client lifecycle is fully decoupled from daemon state

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
│   └── executor/
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

- Cloud LLM clients exist but are currently unused and disabled; the system operates entirely in local-only mode.

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

- Linux systems using X11 only
- Requires systemd user sessions
- LLM latency depends on model size
- No sandboxing between intents
- No GUI feedback


## Future Work

- Optional cloud-backed inference path integrated behind the existing LLM runtime interface
- Lightweight GUI overlay as an alternate client to the existing daemon
- Plugin-based intent system with explicit isolation boundaries
- Multi-model routing within the daemon for heterogeneous workloads
- Persistent state storage decoupled from daemon process lifetime

## License

MIT License

---

## Author

Chaitanya Parate  
Built as a systems-level project focused on:

- systemd
- Linux services
- Streaming LLM inference
