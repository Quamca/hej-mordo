"""Mordo PC — wersja bez ESP32. Mikrofon i głośniki laptopa."""
import asyncio

from config import GEMINI_API_KEY
from gemini_client import run
import mic_local
from speaker_local import player_open, player_write, player_stop, player_abort


def _on_state(state: str) -> None:
    labels = {"listen": "słucham", "speak": "mówię", "idle": "czekam"}
    print(f"[{labels.get(state, state).upper()}]")


def main() -> None:
    if not GEMINI_API_KEY:
        print("Błąd: ustaw zmienną środowiskową GEMINI_API_KEY")
        return

    print("Mordo PC startuje... (Ctrl+C żeby zatrzymać)")

    async def _main():
        loop = asyncio.get_event_loop()
        mic_local.start(loop)
        await run(
            mic_local.audio_queue,
            mic_local.clear_queue,
            _on_state,
            player_open, player_write, player_stop, player_abort,
        )

    try:
        asyncio.run(_main())
    except KeyboardInterrupt:
        print("\nMordo PC zatrzymany.")


if __name__ == "__main__":
    main()
