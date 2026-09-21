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
