"""Głośniki laptopa — playback 24kHz PCM."""
import numpy as np
import sounddevice as sd

from config import SPEAKER_SAMPLE_RATE

_stream: sd.OutputStream | None = None


def player_open() -> None:
    global _stream
    _stream = sd.OutputStream(samplerate=SPEAKER_SAMPLE_RATE, channels=1, dtype="int16")
    _stream.start()


def player_write(data: bytes) -> None:
    if _stream and _stream.active:
        arr = np.frombuffer(data, dtype="int16")
        _stream.write(arr)


def player_stop() -> None:
    global _stream
    if _stream:
        _stream.stop()
        _stream.close()
        _stream = None


def player_abort() -> None:
    global _stream
    if _stream:
        _stream.abort()
        _stream.close()
        _stream = None
