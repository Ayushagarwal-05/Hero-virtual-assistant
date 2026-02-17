import cv2
import time
import threading
from ultralytics import YOLO
import torch
import pytesseract
import numpy as np
from PIL import ImageGrab

# ---------- YOLO ----------
MODEL = YOLO("yolov8n.pt")
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL.to(DEVICE)

# ---------- RECORDING STATE ----------
_recording = False
_stop_event = threading.Event()
_thread = None


def detect_objects(duration=2):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return []

    detected = set()
    start = time.time()

    while time.time() - start < duration:
        ret, frame = cap.read()
        if not ret:
            continue

        results = MODEL(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                label = MODEL.names.get(int(box.cls[0]), "unknown")
                detected.add(label)

    cap.release()
    return list(detected)


def _record_loop(path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = 20

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(path, fourcc, fps, (width, height))

    while not _stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()


def start_recording(path):
    global _recording, _thread

    if _recording:
        return False

    _stop_event.clear()
    _thread = threading.Thread(
        target=_record_loop, args=(path,), daemon=True
    )
    _thread.start()
    _recording = True
    return True


def stop_recording():
    global _recording

    if not _recording:
        return False

    _stop_event.set()
    _recording = False
    return True


def is_recording():
    return _recording


def extract_text_from_screen():
    img = ImageGrab.grab()
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(gray).strip()

def detect_objects_once(conf_threshold=0.6):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return []

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return []

    results = MODEL(frame, verbose=False)
    detected = []

    for r in results:
        for box in r.boxes:
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            label = MODEL.names.get(cls, "unknown")

            # confidence filter
            if conf < conf_threshold:
                continue

            # normalize glasses naming
            if label in ["glasses", "eyeglasses", "sunglasses"]:
                label = "glasses"

            detected.append(label)

    return detected

