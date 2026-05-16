# Jarvis Term

Jarvis Term is a standalone, Warp-styled terminal emulator with deep Jarvis AI integration. It is built using Python, `pywebview`, and `xterm.js`, allowing it to be compiled into native desktop applications for macOS and Linux.

## Features

- **Warp-Style Interface:** Modern UI with dropdowns for your environment and working directory.
- **Deep Jarvis Integration:** Select the `JARVIS CLI` directly from the environment dropdown to chat and troubleshoot autonomously.
- **Multiple Shells:** Seamlessly switch between `zsh`, `bash`, and `jarvis`.
- **Standalone Packages:** Build into a `.app` for macOS or an executable for Linux.

## Installation

### Method 1: Download Release
Download the pre-packaged `.app` for Mac or `.AppImage` for Linux from the [GitHub Releases](https://github.com/nave433-blip/jarvis-term/releases) tab.

### Method 2: Build from Source
If you want to build the native desktop application yourself:

1. Clone the repository:
```bash
git clone https://github.com/nave433-blip/jarvis-term.git
cd jarvis-term
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pywebview pyinstaller
```

3. Build the Application:
```bash
python3 build.py
```

The macOS `.app` bundle or Linux executable will be located in the `dist/` folder.

## Usage
Simply launch the `JarvisTerm` application. Use the top bar to select your environment (`zsh`, `bash`, or `jarvis`) and your working directory, then click **Launch**.
