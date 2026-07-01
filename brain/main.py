import asyncio

from config import GEMINI_API_KEY
from gemini_client import run
from ws_server import start as start_ws, frame_callbacks, audio_queue, clear_queue, enqueue_state
from audio import player_open, player_write, player_stop, player_abort
import face


def main() -> None:
    if not GEMINI_API_KEY:
        print("Błąd: ustaw zmienną środowiskową GEMINI_API_KEY")
        return

    print("Mordo startuje... (Ctrl+C żeby zatrzymać)")

    async def _main():
        loop = asyncio.get_event_loop()
        frame_callbacks.append(face.put_frame)
        face.start(loop)
        await asyncio.gather(
            start_ws(),
            run(audio_queue, clear_queue, enqueue_state,
                player_open, player_write, player_stop, player_abort),
        )

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print("\nMordo zatrzymany.")


if __name__ == "__main__":
    main()
