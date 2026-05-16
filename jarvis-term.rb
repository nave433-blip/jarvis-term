cask "jarvis-term" do
  version "0.1.4"
  sha256 :no_check # Since we are pointing to a dynamic ZIP for now, or update with actual hash

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
