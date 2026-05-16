# 🚀 Jarvis Term: The Ultimate AI Engineering Console

Jarvis Term is a high-performance, standalone terminal emulator built for the modern engineer. Inspired by **Warp** and powered by the **JARVIS AI Assistant**, it combines native speed with deep agentic intelligence. 

Designed for **macOS** and **Linux**, Jarvis Term transforms your terminal from a passive tool into a proactive engineering partner.

---

## 💎 Key Features

### ⚡️ Warp-Style Command Interface
*   **Intelligent Command Bar:** A dedicated, high-speed input bar at the bottom for commands, chat, and agent triggers.
*   **Multi-Session Power:** Launch and manage multiple independent workspaces (ZSH, BASH, or Python REPL) in a single tabbed window.
*   **Keyboard-First Focus:** Navigate the entire UI (Workspaces, Search, Terminal, Docs) using `Tab` and `Shift+Tab`.

### 🧠 Integrated JARVIS AI Agent
*   **Native Assistant:** Every new session automatically initializes the JARVIS CLI.
*   **Autonomous Debugging:** Launch repair loops directly from your console to research and fix bugs in your code.
*   **Multi-Model Selection:** Seamlessly switch between local AI (Ollama, LM Studio, GPT4All) and cloud giants (Gemini Pro, GPT-4o, Claude 3.5).

### 📑 Professional Workflow Tools
*   **Integrated Document Viewer:** A dedicated side-pane to read READMEs, logs, or source code side-by-side with your terminal.
*   **Drag-and-Drop Analysis:** Drop a file onto the terminal to instantly trigger a deep security and performance audit.
*   **Session Search:** High-speed search box to find anything in your terminal history or logs.

### 🏢 Native macOS Integration
*   **macOS Menu Bar:** Full support for native system menus and shortcuts (`Cmd+T` for New Tab, `Cmd+W` for Close).
*   **High-Contrast Theme:** Beautiful, vibrant Cyan/White theme optimized for deep-focus engineering on dark backgrounds.
*   **Universal Build:** Ships as a native `.app` for macOS and distributable `.AppImage` for Linux.

### 🛡 Safety & Self-Healing
*   **Auto-Update Engine:** One-click version checking and Git-based self-repair directly from the Settings menu.
*   **Safety Prompts:** Intelligent detection of potentially destructive commands with explicit user authorization required.
*   **Self-Healing Config:** Automated detection and configuration of local LLM servers (Ollama, etc.).

---

## 📦 Installation

### Method 1: Download Native Release
The easiest way to get started. Download the latest pre-packaged bundle from the **[Releases](https://github.com/nave433-blip/jarvis-term/releases)** tab.
*   **Mac:** Extract the `.zip` and move `JarvisTerm.app` to your `/Applications` folder.
*   **Linux:** Download and run the `.AppImage`.

### Method 2: Build from Source
If you want to contribute or build the latest cutting-edge features:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/nave433-blip/jarvis-term.git
    cd jarvis-term
    ```
2.  **Initialize Environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install pywebview pyinstaller
    ```
3.  **Build Native App:**
    ```bash
    python3 build.py
    ```
    The results will be available in the `dist/` directory.

---

## 🕹 Usage

1.  **Start a Session:** Click **+ New Session** or use `Cmd+T`.
2.  **Select Context:** Use the **Workspace** dropdown to jump into your project folders.
3.  **Chat with Jarvis:** Type `/chat "How do I optimize this?"` in the bottom command bar.
4.  **Auto-Fix:** Type `/fix bug_report.txt` and watch JARVIS handle the repair.
5.  **Docs View:** Click the 📄 icon to open the integrated viewer for easy file reading.

---

## 👨‍💻 Created By
**Nave433 (Evan Shipley)**

*Built for engineers who demand absolute technical truth and sovereign system access.*
