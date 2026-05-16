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
        self.fd = None
        self.window = None

    def set_window(self, window):
        self.window = window

    def start_terminal(self, cwd, shell):
        if self.fd is not None:
            os.close(self.fd)
            
        pid, self.fd = pty.fork()
        if pid == 0: # Child
            os.chdir(cwd)
            os.environ['TERM'] = 'xterm-256color'
            os.execv(shell, [shell])
        else: # Parent
            # Set non-blocking
            flags = fcntl.fcntl(self.fd, fcntl.F_GETFL)
            fcntl.fcntl(self.fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)
            
            # Start reading thread
            threading.Thread(target=self.read_from_pty, daemon=True).start()
            return True

    def read_from_pty(self):
        while True:
            r, _, _ = select.select([self.fd], [], [])
            if self.fd in r:
                try:
                    data = os.read(self.fd, 1024).decode('utf-8', errors='replace')
                    if data and self.window:
                        self.window.evaluate_js(f"writeToTerminal({repr(data)})")
                except OSError:
                    break

    def write_to_pty(self, data):
        if self.fd:
            os.write(self.fd, data.encode('utf-8'))

    def resize_pty(self, cols, rows):
        if self.fd:
            winsize = struct.pack("HHHH", rows, cols, 0, 0)
            fcntl.ioctl(self.fd, termios.TIOCSWINSZ, winsize)

    def get_directories(self, path):
        try:
            return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
        except Exception:
            return []

if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'Jarvis Term - Warp Style',
        'index.html',
        js_api=api,
        width=1000,
        height=700,
        background_color='#1E1E1E'
    )
    api.set_window(window)
    webview.start(debug=False)
