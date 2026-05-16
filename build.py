import os
import subprocess
import sys

def build():
    print("Building Jarvis Term with PyInstaller...")
    
    # We need to include the index.html
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onedir",
        "--windowed",
        "--add-data", "index.html:.",
        "--name", "JarvisTerm",
        "main.py"
    ]
    
    subprocess.run(cmd)
    
    print("\nBuild complete!")
    if sys.platform == 'darwin':
        print("macOS app bundle located in dist/JarvisTerm.app")
    elif sys.platform == 'linux':
        print("Linux executable located in dist/JarvisTerm")

if __name__ == "__main__":
    build()
