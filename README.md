🤖 HERO — AI Desktop Assistant (Jarvis-Inspired)

HERO is an advanced voice-controlled AI desktop assistant inspired by Jarvis-style systems, designed to integrate real-world system control, AI reasoning, computer vision, and voice interaction into a single local application.

Unlike basic chatbot projects, HERO combines:

Voice commands

Real OS control

Camera-based object detection

Screen understanding (OCR)

Persistent memory

AI-powered conversation

The goal is to build the most realistic and technically achievable “Jarvis-like” assistant using modern AI and local automation.


✨ Features
🎤 Voice Control

Natural voice interaction

Wake-style commands (e.g. “Hello Hero”)

Speech recognition using SpeechRecognition


🔊 AI Voice Responses

Realistic TTS responses

Non-blocking speech system


🧠 AI Reasoning

OpenAI-powered intelligent responses

Context-aware conversation

System assistant behavior


💾 Persistent Memory

Hero can remember and forget information:

remember my name is Ayush
what is my name
forget my name


Memory is stored locally in:

hero_memory.json


🖥️ System Control
Open Applications
open chrome
open spotify


Uses Windows search automation.

Close Applications (Dynamic)
close chrome
close spotify


Uses process detection and termination.


📷 Computer Vision (Camera)

Real-time object detection using:

YOLOv8

OpenCV

Example:

what can you see


Hero analyzes the camera feed and identifies objects.


🖥️ Screen Understanding (OCR)

Hero can read visible text on your screen.

Example:

read my screen
what is on my screen


Uses:

Tesseract OCR

Screenshot capture


🎥 Recording System

Start and stop camera recording via voice:

start recording
stop recording


Recordings saved to:

/recordings


🏗️ Architecture
hero.py           → Main controller & intent routing
voice.py          → Text-to-speech system
listener.py       → Speech recognition input
brain.py          → AI reasoning (OpenAI)
memory.py         → Persistent memory system
system_control.py → OS automation
vision.py         → Camera + OCR + object detection
ui.py             → Desktop UI & status indicator


🧰 Tech Stack

Python 3.10+

OpenAI API

SpeechRecognition

OpenCV

Ultralytics YOLOv8

pytesseract (OCR)

PyGame (audio playback)

Threading (real-time async behavior)


⚙️ Installation
1. Clone Repository
git clone https://github.com/YOUR_USERNAME/HERO.git
cd HERO

2. Install Dependencies
pip install -r requirements.txt


If you don’t have a requirements file:

pip install openai speechrecognition pygame opencv-python ultralytics pytesseract pillow pyautogui psutil

3. Install Tesseract OCR

Download:

https://github.com/UB-Mannheim/tesseract/wiki

Verify installation:

tesseract --version

4. Set OpenAI API Key

Windows:

setx OPENAI_API_KEY "your_api_key_here"


Restart terminal after setting.


▶️ Running HERO
python hero.py


Example commands:

hello hero

open chrome

close spotify

what can you see

read my screen

remember my name is Ayush


⚠️ Known Considerations

Virtual audio devices (e.g., voice changers) may hijack microphone input.

Ensure correct microphone is set as Windows default.

Camera must not be used by another application.


🚀 Roadmap
Phase 6 (Upcoming)

Screen visual object recognition (YOLO on screenshots)

Context-aware analysis

Wake-word optimization

Advanced Jarvis-style interaction

Real-time environment awareness


📜 License

MIT License


🙌 Credits

Built as an experimental AI assistant project exploring realistic Jarvis-style systems using modern AI tooling.
