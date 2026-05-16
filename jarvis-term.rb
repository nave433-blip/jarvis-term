cask "jarvis-term" do
  version "0.1.7"
  sha256 "c52769a7beb395417d096869eb1c7cdc809078515d296c93797262655c6c694c"

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
