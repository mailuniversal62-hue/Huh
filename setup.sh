#!/bin/bash
# phishkit setup — Kali

set -e

echo "[*] Updating pip..."
python3 -m pip install --upgrade pip

echo "[*] Installing dependencies..."
pip3 install -r requirements.txt

echo "[*] Creating directories..."
mkdir -p captured logs templates/google templates/microsoft \
         templates/instagram templates/facebook templates/generic static

echo "[*] Setting permissions..."
chmod +x phish.py

echo "[+] Setup complete."
echo "[+] Run: python3 phish.py --help"


# Serve Google template on port 8080
python3 phish.py -t google -p 8080

# Serve Microsoft on port 80
sudo python3 phish.py -t microsoft -p 80

# HTTPS with self-signed cert (generate cert first)
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
python3 phish.py -t google -p 443 --tls
