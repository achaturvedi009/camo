# Camoufox Antidetect Browser

A lightweight, login-free antidetect browser platform using Camoufox as the core engine. It supports unlimited, isolated browser profiles with unique device fingerprints, proxy configurations, and OS spoofing capabilities.

## Features

- **Multi-Profile Management**: Create, edit, and delete multiple isolated profiles without any login requirement.
- **Proxy Integration**: Each profile can have its own HTTP, HTTPS, SOCKS4, or SOCKS5 proxy configuration.
- **Device & OS Spoofing**: Built-in support for spoofing Windows, Linux, and Android fingerprints using Camoufox's powerful evasion tools.
- **Local-First**: All data is stored locally in `data/` directory as JSON files and browser configurations. No account, no API key, no server dependency.
- **Clean UI**: Simple local dashboard to manage profiles, launch browsers, and test proxy configurations.

## Architecture

- **Backend**: FastAPI (Python) running a local API server.
- **Frontend**: Vue.js + Tailwind CSS (Static files, loaded directly in the browser).
- **Core Browser Engine**: Camoufox (Playwright + Firefox modifications) ensuring state-of-the-art fingerprint evasion.

## Installation

1. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Playwright dependencies (optional depending on system, but recommended):
   ```bash
   playwright install-deps
   ```

## Usage

1. Start the API Server:
   ```bash
   python main.py
   ```
   (Alternatively: `uvicorn src.api.main:app --host 127.0.0.1 --port 8000`)

2. Open the UI:
   Just open `src/ui/index.html` in your favorite web browser (e.g., Chrome or regular Firefox).

3. Create a profile, set the desired OS and Proxy configurations, and hit **Start**.

## Folder Structure

- `data/`: All your profiles, preferences, and browser contexts are saved here.
- `src/api/`: FastAPI backend implementation.
- `src/core/`: Application logic, process management, Camoufox integration.
- `src/ui/`: The dashboard frontend.
