import webview
import pty
import os
import fcntl
import termios
import struct
import select
import threading

class Api:
    def __init__(self):
        self.ptys = {} # tab_id -> fd
        self.window = None

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

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Jarvis Term - Warp Style',
        'index.html',
        js_api=api,
        width=1100,
        height=750,
        background_color='#1E1E1E'
    )
    api.set_window(window)
    webview.start(debug=False)
