import asyncio
import threading
import os
import uuid
import pygame
import edge_tts
import time

pygame.mixer.init(frequency=44100, size=-16, channels=2)

_audio_lock = threading.Lock()
_stop_event = threading.Event()


def _cleanup():
    base = os.path.dirname(os.path.abspath(__file__))
    for f in os.listdir(base):
        if f.startswith("hero_voice_") and f.endswith(".mp3"):
            try:
                os.remove(os.path.join(base, f))
            except Exception:
                pass


_cleanup()


async def _tts_and_play(text, filename):
    if _stop_event.is_set():
        return

    communicate = edge_tts.Communicate(
        text,
        voice="en-GB-RyanNeural"
    )
    await communicate.save(filename)

    if _stop_event.is_set():
        return

    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        if _stop_event.is_set():
            pygame.mixer.music.stop()
            return
        await asyncio.sleep(0.05)


def speak(text):
    stop_speaking()

    def runner():
        with _audio_lock:
            _stop_event.clear()
            filename = f"hero_voice_{uuid.uuid4().hex}.mp3"
            try:
                asyncio.run(_tts_and_play(text, filename))
            finally:
                time.sleep(0.1)
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                except Exception:
                    pass

    threading.Thread(target=runner, daemon=True).start()


def stop_speaking():
    _stop_event.set()
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
