cask "jarvis-term" do
  version "0.1.7"
  sha256 "86e33bfdce99a80ecda5734c51b299b6dfacd6a4aaec061cb83b66c8f5b002b4"

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
