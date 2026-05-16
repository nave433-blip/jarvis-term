#!/bin/bash

# Jarvis Term: AppImage Builder Infrastructure
# This script must be run on a Linux environment to generate the final AppImage.

APP_NAME="JarvisTerm"
APP_DIR="${APP_NAME}.AppDir"

echo "Creating AppDir structure..."
mkdir -p "${APP_DIR}/usr/bin"
mkdir -p "${APP_DIR}/usr/share/icons/hicolor/512x512/apps"

# 1. Build the python executable (Assumes running on Linux)
# pip install pywebview pyinstaller
# pyinstaller --noconfirm --onedir --add-data "index.html:." main.py

# 2. Copy artifacts (Simulated layout)
# cp dist/main/* "${APP_DIR}/usr/bin/"
# cp assets/icon.png "${APP_DIR}/usr/share/icons/hicolor/512x512/apps/${APP_NAME}.png"

# 3. Create AppRun script
cat <<EOF > "${APP_DIR}/AppRun"
#!/bin/bash
HERE="\$(dirname "\$(readlink -f "\${0}")")"
export PATH="\${HERE}/usr/bin:\${PATH}"
exec "\${HERE}/usr/bin/main" "\$@"
EOF
chmod +x "${APP_DIR}/AppRun"

# 4. Create .desktop file
cat <<EOF > "${APP_DIR}/${APP_NAME}.desktop"
[Desktop Entry]
Type=Application
Name=Jarvis Term
Exec=AppRun
Icon=${APP_NAME}
Categories=Development;TerminalEmulator;
Comment=Advanced AI Engineering Console
EOF

echo "AppDir infrastructure ready."
echo "To generate the final AppImage on Linux, download appimagetool and run:"
echo "./appimagetool-x86_64.AppImage ${APP_DIR}"
