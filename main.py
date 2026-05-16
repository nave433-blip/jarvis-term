import webview
from webview.menu import Menu, MenuItem, MenuSeparator
import pty
import os
import fcntl
import termios
import struct
import select
import threading
import json
import sys
from pathlib import Path
import webbrowser
import traceback

def term_repair_hook(exctype, value, tb):
    error_msg = "".join(traceback.format_exception(exctype, value, tb))
    print("\n--- JARVIS TERM CRITICAL ERROR ---")
    print(error_msg)
    with open("crash_log.txt", "w") as f:
        f.write(error_msg)
    print("Crash log saved to crash_log.txt")
    sys.__excepthook__(exctype, value, tb)

sys.excepthook = term_repair_hook

class Api:
    def __init__(self):
        self.ptys = {} # tab_id -> fd
        self.window = None
        self.config_path = Path.home() / ".jarvis" / "config.json"

    def set_window(self, window):
        self.window = window

    def start_terminal(self, tab_id, cwd, shell):
        if tab_id in self.ptys:
            os.close(self.ptys[tab_id])
            
        pid, fd = pty.fork()
        if pid == 0: # Child
            try:
                os.chdir(cwd)
            except Exception:
                os.chdir(os.path.expanduser("~"))
            os.environ['TERM'] = 'xterm-256color'
            os.environ['COLORTERM'] = 'truecolor'
            # Launch shell
            os.execv(shell, [shell])
        else: # Parent
            self.ptys[tab_id] = fd
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            threading.Thread(target=self.read_from_pty, args=(tab_id, fd), daemon=True).start()
            return True

    def read_from_pty(self, tab_id, fd):
        while True:
            if tab_id not in self.ptys: break
            r, _, _ = select.select([fd], [], [], 0.1)
            if fd in r:
                try:
                    data = os.read(fd, 4096).decode('utf-8', errors='replace')
                    if data and self.window:
                        self.window.evaluate_js(f"writeToTerminal('{tab_id}', {repr(data)})")
                except OSError:
                    break
        if tab_id in self.ptys:
            del self.ptys[tab_id]

    def write_to_pty(self, tab_id, data):
        fd = self.ptys.get(tab_id)
        if fd:
            os.write(fd, data.encode('utf-8'))

    def resize_pty(self, tab_id, cols, rows):
        fd = self.ptys.get(tab_id)
        if fd:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)

    def get_config(self):
        if self.config_path.exists():
            with open(self.config_path, "r") as f:
                return json.load(f)
        return {}

    def save_config(self, config):
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        return True

    def save_config_field(self, key, value):
        config = self.get_config()
        config[key] = value
        return self.save_config(config)

    def check_updates(self):
        try:
            sys.path.append(str(Path.home() / "jarvis-dev"))
            from core.update import check_for_updates, CURRENT_VERSION
            latest = check_for_updates()
            return {"current": CURRENT_VERSION, "latest": latest or CURRENT_VERSION}
        except:
            return {"current": "0.1.2", "latest": "0.1.2"}

    def run_update(self):
        try:
            sys.path.append(str(Path.home() / "jarvis-dev"))
            from core.update import apply_update
            return apply_update()
        except:
            return "Error: Update engine not found. Please update via CLI."

    def add_pinned_workspace(self, path):
        config = self.get_config()
        pinned = config.get("pinned_workspaces", [])
        if path not in pinned:
            pinned.append(path)
            config["pinned_workspaces"] = pinned
            self.save_config(config)
        return pinned

    def read_file(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return f.read()
            return "Error: File not found."
        except Exception as e:
            return f"Error reading file: {e}"

    def open_url(self, url):
        webbrowser.open(url)
        return True

    def get_cwd(self):
        return os.getcwd()

    # Menu Callbacks
    def menu_new_session(self):
        self.window.evaluate_js("createTab()")

    def menu_close_session(self):
        self.window.evaluate_js("closeActiveTab()")

    def menu_open_settings(self):
        self.window.evaluate_js("openSettings()")

    def menu_toggle_docs(self):
        self.window.evaluate_js("toggleSidePane()")

if __name__ == '__main__':
    api = Api()
    
    menu = [
        Menu('File', [
            MenuItem('New Session', api.menu_new_session, shortcut='meta+t'),
            MenuItem('Close Session', api.menu_close_session, shortcut='meta+w'),
            MenuSeparator(),
            MenuItem('Settings', api.menu_open_settings, shortcut='meta+,'),
            MenuItem('Quit Jarvis', sys.exit, shortcut='meta+q')
        ]),
        Menu('View', [
            MenuItem('Toggle Document Viewer', api.menu_toggle_docs, shortcut='meta+d'),
            MenuItem('Full Screen', lambda: api.window.toggle_fullscreen(), shortcut='meta+ctrl+f')
        ]),
        Menu('Help', [
            MenuItem('Visit GitHub', lambda: api.open_url('https://github.com/nave433-blip/jarvis-dev')),
            MenuItem('Get API Keys', lambda: api.window.evaluate_js('openKeysModal()'))
        ])
    ]

    window = webview.create_window(
        'Jarvis',
        'index.html',
        js_api=api,
        width=1200,
        height=800,
        background_color='#1E1E1E'
    )
    api.set_window(window)
    webview.start(debug=False, menu=menu)
