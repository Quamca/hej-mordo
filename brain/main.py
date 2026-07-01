import asyncio
import os
import sys

from config import GEMINI_API_KEY
from gemini_client import run_triggered
from ws_server import start as start_ws, frame_callbacks, photo_callbacks, audio_callbacks
import face
import wake_word


class _Tee:
    """Dubluje print() do konsoli i do pliku logu (nadpisywanego co start)."""

    def __init__(self, *streams) -> None:
        self._streams = streams

    def write(self, data) -> None:
        for s in self._streams:
            s.write(data)

    def flush(self) -> None:
        for s in self._streams:
            s.flush()


_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mordo.log")
_log_file = open(_log_path, "w", encoding="utf-8", buffering=1)
sys.stdout = _Tee(sys.stdout, _log_file)
sys.stderr = _Tee(sys.stderr, _log_file)


def main() -> None:
    if not GEMINI_API_KEY:
        print("Błąd: ustaw zmienną środowiskową GEMINI_API_KEY")
        return

    print("Mordo startuje... (Ctrl+C żeby zatrzymać)")

    async def _main():
        loop = asyncio.get_event_loop()
        frame_callbacks.append(face.put_frame)
        photo_callbacks.append(face.request_photo)
        audio_callbacks.append(wake_word.put_audio)
        face.start(loop)
        wake_word.start(loop)
        await asyncio.gather(start_ws(), run_triggered())

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print("\nMordo zatrzymany.")


if __name__ == "__main__":
    main()
