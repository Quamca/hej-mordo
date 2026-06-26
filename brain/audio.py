import numpy as np
import sounddevice as sd
from config import SPEAKER_SAMPLE_RATE

_player: sd.OutputStream | None = None


def player_open() -> None:
    global _player
    if _player:
        return
    _player = sd.OutputStream(
        samplerate=SPEAKER_SAMPLE_RATE, channels=1, dtype="int16", latency="low"
    )
    _player.start()


def player_write(data: bytes) -> None:
    if _player and _player.active:
        _player.write(np.frombuffer(data, dtype=np.int16))


def player_stop() -> None:
    """Opróżnij bufor do końca, potem zamknij."""
    global _player
    if _player:
        _player.stop()
        _player.close()
        _player = None


def player_abort() -> None:
    """Natychmiast przerwij, wyrzuć bufor."""
    global _player
    if _player:
        _player.abort()
        _player.close()
        _player = None
