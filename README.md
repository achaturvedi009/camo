# Camoufox Antidetect Browser

A lightweight, login-free antidetect browser platform using Camoufox as the core engine. It supports unlimited, isolated browser profiles with unique device fingerprints, proxy configurations, and OS spoofing capabilities.

## Features

- **Multi-Profile Management**: Create, edit, clone, and delete multiple isolated profiles without any login requirement.
- **Fingerprint Engine**: Automatically generates realistic browser fingerprints (User-Agent, WebGL, Screen, Timezone, Languages, etc.) based on OS presets (Windows, Linux, Android).
- **Camoufox Version Manager**: Download and manage multiple versions of the Camoufox engine directly from PyPI. Assign specific engine versions to different profiles to ensure absolute isolation and testing flexibility.
- **Proxy Integration**: Each profile can have its own HTTP, HTTPS, SOCKS4, or SOCKS5 proxy configuration. Includes clipboard auto-paste for easy setup.
- **Local-First Storage**: All data is stored locally in an SQLite database (`data/profiles.db`). No account, no API key, no server dependency.
- **Clean UI**: Simple local dashboard (Vue.js + Tailwind CSS) to manage profiles, preview fingerprints, manage engine versions, and test proxy configurations.

## Architecture

- **Backend**: FastAPI (Python) running a local API server.
- **Database**: SQLite (SQLAlchemy ORM) for profile and version storage.
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
   *(Alternatively: `uvicorn src.api.main:app --host 127.0.0.1 --port 8000`)*

2. Open the UI:
   Just open `src/ui/index.html` in your favorite web browser (e.g., Chrome or regular Firefox).

3. Navigate the Dashboard:
   - **Profiles Tab**: Create a new profile, set the desired OS and Proxy configurations, preview the fingerprint, and hit **Start**.
   - **Settings Tab**: View installed Camoufox versions, set a default system version, or fetch and install older/newer versions directly from PyPI.

## Folder Structure

- `data/`: SQLite database (`profiles.db`) and isolated browser user-data directories.
- `src/api/`: FastAPI backend implementation and routes.
- `src/core/`: Application logic, fingerprint generator, database models, process management, and version manager.
- `src/ui/`: The Vue.js dashboard frontend.
- `~/.camo/camoufox_versions/`: Directory where downloaded Camoufox versions are stored for isolation.
