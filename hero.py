from voice import speak, stop_speaking
from listener import listen
import system_control
import brain
import memory
import vision
import threading
import time
import os
from ui import start_ui, shutdown_event, ui_state

MODE_IDLE = "idle"
MODE_RECORDING = "recording"
current_mode = MODE_IDLE


def handle_task(command):
    global current_mode
    command = command.lower().strip()
    if not command:
        return

    # ========= MEMORY WRITE =========
    if command.startswith("remember "):
        phrase = command.replace("remember ", "").strip()
        if " is " in phrase:
            key, value = phrase.split(" is ", 1)
            key = key.replace("my ", "").strip()
            if key == "name":
                memory.set_fact("name", value.strip())
                speak(f"I will remember that your name is {value}.")
            else:
                memory.set_fact(key, value.strip())
                speak(f"I will remember that your {key} is {value}.")
        else:
            speak("Please say remember followed by a fact.")
        return

    # ========= MEMORY DELETE =========
    if command.startswith("forget "):
        key = command.replace("forget ", "").replace("my ", "").strip()
        if key == "name":
            memory.delete_fact("name")
            speak("I have forgotten your name.")
        else:
            memory.delete_fact(key)
            speak(f"I have forgotten your {key}.")
        return

    # ========= MEMORY READ =========
    if "what is my name" in command or "what's my name" in command:
        name = memory.get_fact("name")
        if name:
            speak(f"Your name is {name}.")
        else:
            speak("I do not know your name.")
        return

    # ========= EXIT =========
    if any(x in command for x in ["exit hero", "close hero", "quit hero"]):
        speak("Signing out.")
        shutdown_event.set()
        return

    # ========= STOP RECORDING =========
    if "stop recording" in command:
        if current_mode != MODE_RECORDING:
            speak("I am not recording.")
            return
        vision.stop_recording()
        current_mode = MODE_IDLE
        speak("Recording saved.")
        return

    # ========= START RECORDING =========
    if "start recording" in command:
        if current_mode == MODE_RECORDING:
            speak("I am already recording.")
            return
        os.makedirs("recordings", exist_ok=True)
        path = f"recordings/hero_record_{int(time.time())}.avi"
        if vision.start_recording(path):
            current_mode = MODE_RECORDING
            speak("Recording started.")
        else:
            speak("I could not start recording.")
        return

    # ========= VISION (ON COMMAND) =========
    if "what can you see" in command:
        objects = vision.detect_objects_once()
        if objects:
            speak("I can see " + ", ".join(objects[:5]) + ".")
        else:
            speak("I do not see anything clearly.")
        return

    # ========= READ SCREEN =========
    if "read my screen" in command or "what is on my screen" in command:
        speak("Reading your screen.")
        text = vision.extract_text_from_screen()
        if text:
            speak(text[:400])
        else:
            speak("I could not read any text on your screen.")
        return

    # ========= SYSTEM =========
    if command.startswith("open "):
        speak("Opening.")
        system_control.open_any_app(command.replace("open ", ""))
        return

    # ========= CLOSE APP =========
    if command.startswith("close "):
        app = command.replace("close ", "").strip()
        success = system_control.close_app(app)
        if success:
            speak(f"{app} closed.")
        else:
            speak(f"I could not find {app} running.")
        return

    # ========= FALLBACK =========
    response = brain.think(command)
    speak(response if response else "I heard you.")


def voice_loop():
    time.sleep(1)
    ui_state["status"] = "Listening"
    while not shutdown_event.is_set():
        cmd = listen()
        if cmd:
            ui_state["status"] = "Processing"
            handle_task(cmd)
            ui_state["status"] = "Listening"


if __name__ == "__main__":
    threading.Thread(target=voice_loop, daemon=True).start()
    start_ui()
