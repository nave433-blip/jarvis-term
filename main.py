import webview
import pty
import os
import fcntl
import termios
import struct
import select
import threading
import json
from pathlib import Path

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
                os.chdir("/")
            os.environ['TERM'] = 'xterm-256color'
            os.execv(shell, [shell])
        else: # Parent
            self.ptys[tab_id] = fd
            # Set non-blocking
            flags = fcntl.fcntl(fd, fcntl.F_GETFL)
            fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            
            # Start reading thread for this specific PTY
            threading.Thread(target=self.read_from_pty, args=(tab_id, fd), daemon=True).start()
            return True

    def read_from_pty(self, tab_id, fd):
        while True:
            if tab_id not in self.ptys: break
            r, _, _ = select.select([fd], [], [], 0.1)
            if fd in r:
                try:
                    data = os.read(fd, 1024).decode('utf-8', errors='replace')
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

    def save_config_field(self, key, value):
        config = self.get_config()
        config[key] = value
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=4)
        return True

    def add_pinned_workspace(self, path):
        config = self.get_config()
        pinned = config.get("pinned_workspaces", [])
        if path not in pinned:
            pinned.append(path)
            config["pinned_workspaces"] = pinned
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
        return pinned

    def remove_pinned_workspace(self, path):
        config = self.get_config()
        pinned = config.get("pinned_workspaces", [])
        if path in pinned:
            pinned.remove(path)
            config["pinned_workspaces"] = pinned
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=4)
        return pinned

    def read_file(self, file_path):
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    return f.read()
            return "Error: File not found."
        except Exception as e:
            return f"Error reading file: {e}"

    def list_dir_files(self, path):
        try:
            if os.path.exists(path):
                return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            return []
        except Exception:
            return []

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Jarvis Term - Warp Style',
        'index.html',
        js_api=api,
        width=1200,
        height=800,
        background_color='#1E1E1E'
    )
    api.set_window(window)
    webview.start(debug=False)
