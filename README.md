# Camoufox Antidetect Browser

A lightweight, login-free antidetect browser platform using Camoufox as the core engine. It supports unlimited, isolated browser profiles with unique device fingerprints, proxy configurations, and OS spoofing capabilities.

## Features

- **Multi-Profile Management**: Create, edit, clone, and delete multiple isolated profiles without any login requirement.
- **Fingerprint Engine**: Automatically generates realistic browser fingerprints (User-Agent, WebGL, Screen, Timezone, Languages, etc.) based on OS presets (Windows, Linux, Android). It supports variations within realistic data pools.
- **Camoufox Version Manager**: Download and manage multiple versions of the Camoufox engine directly from PyPI. Assign specific engine versions to different profiles to ensure absolute isolation and testing flexibility.
- **Proxy Integration**: Each profile can have its own HTTP, HTTPS, SOCKS4, or SOCKS5 proxy configuration. Includes clipboard auto-paste for easy setup.
- **Local-First Storage**: All data is stored locally in an SQLite database (`data/profiles.db`). No account, no API key, no server dependency.
- **Headless & Virtual Displays**: Auto-detects CI environments and falls back to virtual headless X11 servers using `Xvfb` if no physical display is found.
- **Clean UI**: Simple local dashboard (Vue.js + Tailwind CSS) to manage profiles, preview fingerprints, manage engine versions, and test proxy configurations.

## Architecture

- **Backend**: FastAPI (Python) running a local API server.
- **Database**: SQLite (SQLAlchemy ORM) for profile and version storage.
- **Frontend**: Vue.js + Tailwind CSS (Static files, loaded directly in the browser).
- **Core Browser Engine**: Camoufox (Playwright + Firefox modifications) ensuring state-of-the-art fingerprint evasion.

## Installation

1. Clone the repository and navigate into the folder.
2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Playwright system dependencies:
   Depending on your operating system, you may need additional libraries required by Playwright.
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

## Troubleshooting

- **Target closed / X11 Error**: If your browser instances crash immediately upon clicking "Start" on Linux, it may mean your environment lacks an X11 display. The application attempts to fall back to `virtual` mode, but ensure `Xvfb` is installed on your Linux distribution if running in a purely headless server environment.
- **Dependencies Missing**: Run `pip install -r requirements.txt` again to ensure `camoufox[geoip]` and `SQLAlchemy` are fully installed.

## Folder Structure

- `data/`: SQLite database (`profiles.db`) and isolated browser user-data directories. (Ignored from version control)
- `src/api/`: FastAPI backend implementation and routes.
- `src/core/`: Application logic, fingerprint generator, database models, process management, and version manager.
- `src/ui/`: The Vue.js dashboard frontend.
- `~/.camo/camoufox_versions/`: Directory where downloaded Camoufox versions are stored for isolation.

## Building Executables

You can package the FastAPI backend into a single executable file for your operating system using **PyInstaller**. This removes the need for Python or pip installations on the host machine.

### Prerequisites

First, install PyInstaller:
```bash
pip install pyinstaller
```

### Windows (.exe)

Run the following command from the repository root:
```bash
pyinstaller --name "Camoufox_Antidetect" --onefile main.py
```
This will generate `Camoufox_Antidetect.exe` inside the `dist/` folder.

### Linux (Executable)

Run the following command from the repository root:
```bash
pyinstaller --name "Camoufox_Antidetect" --onefile main.py
```
This will generate an executable named `Camoufox_Antidetect` inside the `dist/` folder.

### macOS (Executable / .app)

Run the following command from the repository root:
```bash
pyinstaller --name "Camoufox_Antidetect" --onefile main.py
```
This will generate an executable named `Camoufox_Antidetect` inside the `dist/` folder.

*Note: Since the UI is purely HTML/JS, you can distribute the `src/ui/` folder alongside your executable, and simply open `src/ui/index.html` in a web browser while the executable is running in the background.*
