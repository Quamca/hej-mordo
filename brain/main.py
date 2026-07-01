import asyncio

from config import GEMINI_API_KEY
from gemini_client import run
from ws_server import start as start_ws, frame_callbacks, photo_callbacks
import face


def main() -> None:
    if not GEMINI_API_KEY:
        print("Błąd: ustaw zmienną środowiskową GEMINI_API_KEY")
        return

    print("Mordo startuje... (Ctrl+C żeby zatrzymać)")

    async def _main():
        loop = asyncio.get_event_loop()
        frame_callbacks.append(face.put_frame)
        photo_callbacks.append(face.request_photo)
        face.start(loop)
        await asyncio.gather(start_ws(), run())

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print("\nMordo zatrzymany.")


if __name__ == "__main__":
    main()
