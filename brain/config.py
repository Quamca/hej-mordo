import os

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.1-flash-live-preview"

MIC_SAMPLE_RATE = 16000
MIC_CHANNELS = 1
MIC_CHUNK_SIZE = 1024

SPEAKER_SAMPLE_RATE = 24000

WS_HOST = "0.0.0.0"
WS_PORT = 8765

SYSTEM_PROMPT = """\
Jesteś Mordo — robot-asystent Igora. Rozmawiasz z Igorem. Mówisz wyłącznie po polsku.
Jesteś ciepły, bezpośredni i lekko dowcipny — jak dobry znajomy który chce pomóc.
Odpowiadasz bardzo krótko i naturalnie. Nie jesteś formalny.\
"""
