cask "jarvis-term" do
  version "0.1.6"
  sha256 "60b6a0cc5bda27c2de95caa6babca045cea8443aeeae108cc0268e3ae6ccd9c9"

  url "https://github.com/nave433-blip/jarvis-term/releases/download/v#{version}/JarvisTerm-mac.zip"
  name "Jarvis Term"
  desc "Advanced AI Engineering Console & Terminal Emulator"
  homepage "https://github.com/nave433-blip/jarvis-term"

  app "JarvisTerm.app"

  binary "#{appdir}/JarvisTerm.app/Contents/MacOS/JarvisTerm", target: "jarvis-gui"

  zap trash: [
    "~/.jarvis",
    "~/Library/Application Support/JarvisTerm",
    "~/Library/Preferences/com.nave433.jarvisterm.plist",
  ]
end
