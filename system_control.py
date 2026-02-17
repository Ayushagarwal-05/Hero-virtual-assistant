import subprocess
import pyautogui

def open_any_app(app_name):
    pyautogui.press("win")
    pyautogui.write(app_name, interval=0.04)
    pyautogui.press("enter")

def close_app(app_name):
    import psutil
    app_name = app_name.lower()
    closed = False

    for proc in psutil.process_iter(["name"]):
        try:
            name = proc.info["name"]
            if name and app_name in name.lower():
                proc.kill()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return closed



