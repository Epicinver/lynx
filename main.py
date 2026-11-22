import os; 
if os.name != "nt": exit("Error: This program is only compatible with Windows. Please run it on a Windows system.")
import os
import sys
import json
import time
import tempfile
import subprocess
import urllib.request
from pathlib import Path
from packaging.version import Version
REPO = "epicinver/lynx"
CURRENT_VERSION = "1.0.0"
ASSET_NAME = "Installer.exe"
APP_PATH = Path(sys.executable).resolve()
APP_DIR = APP_PATH.parent
BACKUP_PATH = APP_DIR / "oldlynx.bak"
TEMP_DIR = Path(tempfile.gettempdir())
INSTALLER_PATH = TEMP_DIR / "install.exe"
BAT_PATH = TEMP_DIR / "update.bat"
from blessed import Terminal

term = Terminal()

def get_latest_release():
    url = f"https://api.github.com/repos/{REPO}/releases/latest"

    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "Lynx-Updater"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode())


def download_installer(release):
    asset = next(
        (a for a in release["assets"] if a["name"] == ASSET_NAME),
        None
    )

    if asset is None:
        raise Exception("Installer.exe not found in latest release")

    request = urllib.request.Request(
        asset["browser_download_url"],
        headers={"User-Agent": "Lynx-Updater"}
    )

    with urllib.request.urlopen(request, timeout=120) as response:
        INSTALLER_PATH.write_bytes(response.read())

    return INSTALLER_PATH


def launch_batch(installer):
    batch = f"""@echo off
setlocal

timeout /t 2 /nobreak >nul

set "APP={APP_PATH}"
set "BACKUP={BACKUP_PATH}"
set "INSTALLER={installer}"

if exist "%BACKUP%" del /f /q "%BACKUP%"

move /y "%APP%" "%BACKUP%" >nul
if errorlevel 1 goto rollback

"%INSTALLER%"
if errorlevel 1 goto rollback

if not exist "%APP%" goto rollback

del /f /q "%BACKUP%"
del /f /q "%INSTALLER%"
del /f /q "%~f0"
exit /b 0

:rollback
if exist "%APP%" del /f /q "%APP%"
if exist "%BACKUP%" move /y "%BACKUP%" "%APP%" >nul

del /f /q "%INSTALLER%"
del /f /q "%~f0"
exit /b 1
"""

    BAT_PATH.write_text(batch, encoding="utf-8")

    subprocess.Popen(
        ["cmd.exe", "/c", str(BAT_PATH)],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP |
                      subprocess.DETACHED_PROCESS,
        close_fds=True
    )

    sys.exit(0)


class menu:
    def __init__(self):
        term.clear()
        main()
# btw the art is 10 tabs/indents big so yh 
    art =  """

                                        \033[0;97m█\033[0;97;47m▀\033[0;97m▀▀▀▀█\033[0;90m▄\033[0;37m         \033[0;97m▄▄▄▄▄▄▄▄\033[0;37m▄\033[0;90m▄\033[0;97m▄▄▄▄▄▄▄▄\033[0;37m▄▄\033[0;90m▄\033[0;97m█\033[0;97;47m▀▀▀▀▀▀▀▀▀▀▄▄\033[0;90;47m▀\033[0;37m▄\033[0;90m▄\033[0;37m    \033[0;97m▄▄▄▄▄▄▄▄\033[0;37m▄\033[0;90m▄\033[0;37m  \033[0;97m▄▄▄▄\033[0;37m▄\033[0;90m▄\033[0;37m   \033[0m
                                        \033[0;97m█\033[0;37m█    \033[0;97m█\033[0;37m█\033[0;90m█\033[0;37m        \033[0;97m█\033[0;37m█▀▀▀▀▀\033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;37m█▀▀▀▀▀\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█      \033[0;93m■\033[0;37m \033[0;93m▄▄\033[0;37m \033[0;97m▀\033[0;97;47m▄\033[0;37m█\033[0;90;47m▀\033[0;90m▄\033[0;37m  \033[0;97m█\033[0;37m█▀▀▀▀▀\033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m▄\033[0;97;47m▀\033[0;37m█▀▀▀\033[0;97m▀\033[0;97;47m▄\033[0;37m█\033[0;90m█\033[0;37m \033[0m
                                        \033[0;97m█\033[0;37m█   \033[0;93m■\033[0;97m█\033[0;37m██\033[0;90m▄\033[0;37m       \033[0;97m█\033[0;37m█ \033[0;93m▄■\033[0;37m  \033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;37m█ \033[0;93m▄■\033[0;37m  \033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█ \033[0;32m░\033[0;37m        \033[0;93m▀▄\033[0;37m \033[0;97m█\033[0;37m█\033[0;90;47m▀\033[0;90m▄\033[0;37m \033[0;97m▐\033[0;97;47m▌\033[0;37m▌ \033[0;93m▄■·\033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;37m█ \033[0;93m▄■·\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0m
                                        \033[0;97m█\033[0;37m█ \033[0;93m▄▀\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m       \033[0;97m█\033[0;97;47m \033[0;93m▐\033[0;37m    \033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;97;47m \033[0;93m▐\033[0;37m    \033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█\033[0;32m░▒░░\033[0;37m \033[0;97m▄\033[0;97;47m▀\033[0;97m▄\033[0;37m▄ \033[0;32m░\033[0;37m \033[0;93m▌\033[0;97m▐\033[0;97;47m▌\033[0;37m█\033[0;90;47m▐\033[0;90m▌\033[0;97m▐\033[0;97;47m▌\033[0;37m▌\033[0;93m▐\033[0;37m   \033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m▐\033[0;97;47m▌\033[0;37m▌    \033[0;97m█\033[0;37m██\033[0;90m█\033[0m
                                        \033[0;97m█\033[0;37m█ \033[0;93m▌\033[0;37m  \033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m       \033[0;97m█\033[0;37m█ \033[0;32m▓▒░\033[0;37m \033[0;97m█\033[0;37m█\033[0;90;47m▀\033[0;97m█\033[0;37m█  \033[0;32m░▒\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█\033[0;32m▒▒▒▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;32m▐▒▒▒\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m \033[0;97m▀\033[0;97;47m▄\033[0;37m▄   \033[0;97m█\033[0;37m█\033[0;90;47m▀\033[0;97m█\033[0;37m█ \033[0;32m░▒▓\033[0;97m▐█\033[0;37m██\033[0;90m█\033[0m
                                        \033[0;97m█\033[0;37m█  \033[0;32m▓\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m       \033[0;97m█\033[0;37m█ \033[0;32m▀▓▒▄\033[0;97m▀▀▀▀\033[0;37m▀ \033[0;32m▒▓▓▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█\033[0;32m▐▓▓▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;32m▐▓▓▓▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m   \033[0;97m█\033[0;37m█\033[0;32m▐▄\033[0;37m▀\033[0;97m▀▀▀\033[0;37m \033[0;32m▄▒▓▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m \033[0m
                                        \033[0;97m█\033[0;37m█ \033[0;32;42m▒\033[0;32m█▄\033[0;97m▐\033[0;97;47m▌\033[0;37m█\033[0;90m█\033[0;37m        \033[0;97m▀\033[0;97;47m▄\033[0;97m▄\033[0;37m \033[0;32m▀▀▀▀▀▀▀▀\033[0;32;42m▒░\033[0;32m█▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;37m█\033[0;32m▐\033[0;32;42m░▒\033[0;32m▌\033[0;97m█\033[0;37m█\033[0;97;47m \033[0;90m█\033[0;97m█\033[0;32m▐███▌\033[0;97m█\033[0;97;47m \033[0;37m█\033[0;90m█\033[0;37m \033[0;97m▄\033[0;97;47m▀\033[0;37m \033[0;32m▄██▀▀▀▀█▒\033[0;32;42m▒\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m  \033[0m
                                        \033[0;97m█\033[0;37m█\033[0;32m▐▓\033[0;32;42m▒▓\033[0;32m▄\033[0;97m▀\033[0;97;47m▄▄\033[0;97m▀▀\033[0;97;47m▄\033[0;37m█\033[0;90;47m▀\033[0;90m▄\033[0;37m     \033[0;97m▀▀▀▀▀▀█\033[0;37m█ \033[0;32m██▒\033[0;37m \033[0;97m█\033[0;37m██\033[0;90m█\033[0;97;42m█\033[0;37m█\033[0;32m▐\033[0;32;42m░▒\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;32m▐█▓\033[0;32;42m▒\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m▐\033[0;97;47m▌\033[0;37m▌\033[0;32m▒█▒\033[0;37m \033[0;97;42m▄\033[0;97;47m▀▀▄\033[0;37m \033[0;32m▓██▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;37m \033[0m
                                        \033[0;97m▐\033[0;97;47m▌\033[0;37m▌\033[0;32m▓▓▓\033[0;32;42m▒░\033[0;32m▄▄█▄\033[0;97m▀\033[0;97;47m▄\033[0;37m█\033[0;90;47m▀\033[0;90m▄\033[0;97m█\033[0;97;47m▀\033[0;97m▀▀▀▀▀█▄▄\033[0;97;47m▀\033[0;90;47m▄\033[0;37m \033[0;32m▓▒\033[0;37m \033[0;97;42m▄\033[0;97;47m▀\033[0;37m██\033[0;90m█\033[0;97;42m█\033[0;37m█\033[0;32m▐\033[0;32;42m▒▓\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;32m▐\033[0;32;42m█▓▒\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m▐\033[0;97;47m▌\033[0;37m▌\033[0;32m▓▓▓▌\033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;37m█\033[0;32m▐▓▓▓\033[0;97m▐█\033[0;37m██\033[0;90m█\033[0m
                                        \033[0;37m \033[0;97m▀\033[0;97;47m▄\033[0;37m▄\033[0;32m▀▀\033[0;32;42m░\033[0;32m██▓▒▀\033[0;37m \033[0;97m█\033[0;97;47m  \033[0;90m█\033[0;97m█\033[0;97;47m \033[0;37m \033[0;32m███▄▄▄▄▄▄█▀\033[0;37m \033[0;97;42m▄\033[0;97;47m▀\033[0;37m█\033[0;90;47m▄\033[0;90m▀\033[0;37m \033[0;97;42m█\033[0;37m█\033[0;32m▐█\033[0;32;42m▓\033[0;32m▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;32m▐\033[0;32;42m▒░\033[0;32m█▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;97;47m \033[0;37m \033[0;32m▒▒▒\033[0;37m \033[0;97m█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;97;47m \033[0;37m \033[0;32m▒▒▒▌\033[0;97m█\033[0;37m██\033[0;90m█\033[0m
                                        \033[0;37m   \033[0;97m▀▀\033[0;97;47m▄\033[0;97m▄▄▄▄▄\033[0;97;47m▀▀\033[0;90;47m▄\033[0;37m▀\033[0;90m▀\033[0;37m \033[0;97m█\033[0;97;47m▄\033[0;97m▄▄▄▄▄▄▄▄▄▄▄\033[0;97;47m▀▀\033[0;37m█\033[0;90;47m▄\033[0;90m▀\033[0;37m   \033[0;97;42m█\033[0;97;47m▄\033[0;97;42m▄▄▄▄\033[0;97m█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;97;42m▄▄▄▄\033[0;97m▄█\033[0;37m██\033[0;90m█\033[0;97m█\033[0;97;47m▄\033[0;97m▄▄▄▄▄█\033[0;37m█\033[0;90m█\033[0;97m█\033[0;97;47m▄\033[0;97m▄▄▄▄▄█\033[0;37m██\033[0;90m█\033[0m

"""


class choices:
    def info():
        print(term.clear())
        print(menu.art)
        print("""
                                                                    Lynx version 1.0.0 (alpha)
                                                                   Release date: 21st Nov. 2026
                                                              I had CordTool installed. What happened?
                                        CordTool has been discontinued and rebranded as Lynx! We hope you enjoy the new project.
                                                                Telegram channel: t.me/cordtool
                                                                        Built by Parasocial
                                                                            TG: @jji6jo
                                                                             DC: @8p3s
                                                        You will be redirected to the home page in 2 seconds...
""")
        time.sleep(2)

    def update():
        print(term.clear())
        print(menu.art)
        print("""
                                                                             Updating... 
""")
        release = get_latest_release()
        latest_version = release["tag_name"].lstrip("v", "alpha", "beta", "a", "b")
        if Version(latest_version) <= Version(CURRENT_VERSION):
            print(term.clear())
            print(menu.art)
            print("""
                                                                             You are already on the latest version!
""")
            time.sleep(2)
            term.clear()
            return
        else:
            installer = download_installer(release)
            print("""
                                                                            Update downloaded. Launching installer...
                                                                This WILL wipe Lynx and redownload it. Make sure you back up your data!
""")
            print(term.clear())
            print("""
                                                                                        Updating in 5...
""")
            time.sleep(1)
            print(term.clear())
            print("""
                                                                                        Updating in 4...
""")
            time.sleep(1)
            print(term.clear())
            print("""
                                                                                        Updating in 3...
""")
            time.sleep(1)
            print(term.clear())
            print("""
                                                                                        Updating in 2...
""")
            time.sleep(1)
            print(term.clear())
            print("""
                                                                                        Updating in 1...
""")
            time.sleep(1)
            print(term.clear())
            print("""
                                                            Launching installer... please accept any UAC prompts and please wait...
""")
            launch_batch(installer)
        


def main():
    print(menu.art)
    print("""
                                                                             Loading...
""")
    time.sleep(0.8)
    term.clear()
    if os.name == "nt":
        os.system("cls")
    print(menu.art)
    print("""
                                                                 Telegram channel: t.me/cordtool
                                                                        Built by Parasocial
                                                                            TG: @jji6jo
                                                                             DC: @8p3s

""")
    time.sleep(1.4)
    with term.fullscreen(), term.cbreak():
        options = ["Update", "Info", "Exit"]
        selected = 0


        while True:
            print(term.move_yx(0, 0) + term.clear_eos())
            print(menu.art)
            
            for i, option in enumerate(options):
                if i == selected:
                    print("\033[1;32m                                                                      " + term.reverse(option))
                else:
                    print("\033[0;36m                                                                     " + option)

            key = term.inkey(timeout=0.1)

            if key.name == "KEY_UP":
                selected = (selected - 1) % len(options)
            elif key.name == "KEY_DOWN":
                selected = (selected + 1) % len(options)
            elif key.name == "KEY_ENTER" or key == "\n":
                if selected == 1:
                    term.clear()
                    choices.info()
                elif selected == 0:
                    term.clear()
                    choices.update()
                elif selected == 2:
                    quit(0)

def a(): # startup shit
    try:
        release = get_latest_release()
        latest_version = release["tag_name"].lstrip("v", "alpha", "beta", "a", "b")
        if Version(latest_version) <= Version(CURRENT_VERSION):
                    print("You are on the latest version of Lynx. Enjoy.")
                    time.sleep(2)
                    print(term.clear())
        else:
            print("A new version is avaliable! Would you like to update? (y/n)")
            choice = input().lower()
            if choice == "y":
                choices.update()
            else:
                print("You can update later through the menu.")
                time.sleep(4)
                print(term.clear())
    except:
        print("Failed to auto update. Check https://github.com/Epicinver/CordTool, https://t.me/cordtool or https://github.com/Epicinver/Lynx for more info.")

    time.sleep(2)
    print(term.clear())
    
    main()

if __name__ == "__main__":
   a()