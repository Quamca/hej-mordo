"""Wake word 'Hej Mordo' — offline Vosk STT po polsku, lokalnie bez Gemini."""
import json
import os
import queue
import re
import threading

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))
_MODEL_PATH = os.path.join(_BRAIN_DIR, "data", "vosk-model-pl")
_SAMPLE_RATE = 16000
# "Mordo" bywa błędnie rozpoznawane fonetycznie (mordę, mordu, moor(e) do...)
_WAKE_PATTERN = re.compile(r"hej\W*(mor\w*|moor\w*)")

_audio_q: queue.Queue = queue.Queue()


def put_audio(data: bytes) -> None:
    _audio_q.put(data)


def _trigger_gemini() -> None:
    from gemini_client import signal_wake_word
    signal_wake_word()


def _wake_thread(loop) -> None:
    if not os.path.isdir(_MODEL_PATH):
        print(f"[WAKE] brak modelu Vosk w {_MODEL_PATH} — wake word wyłączony", flush=True)
        return

    from vosk import Model, KaldiRecognizer

    print("[WAKE] ładowanie modelu Vosk (polski)...", flush=True)
    model = Model(_MODEL_PATH)
    rec = KaldiRecognizer(model, _SAMPLE_RATE)
    print("[WAKE] nasłuch aktywny — powiedz 'Hej Mordo'", flush=True)

    while True:
        data = _audio_q.get()
        if rec.AcceptWaveform(data):
            text = json.loads(rec.Result()).get("text", "")
            if text and _WAKE_PATTERN.search(text):
                print(f"[WAKE] wykryto: '{text}'", flush=True)
                loop.call_soon_threadsafe(_trigger_gemini)


def start(loop) -> None:
    threading.Thread(target=_wake_thread, args=(loop,), daemon=True).start()
