"""Mikrofon laptopa — capture 16kHz PCM → asyncio.Queue."""
import asyncio
import numpy as np
import sounddevice as sd

from config import MIC_SAMPLE_RATE, MIC_CHUNK_SIZE

audio_queue: asyncio.Queue = asyncio.Queue()
current_rms: float = 0.0
_loop: asyncio.AbstractEventLoop | None = None


def _callback(indata, frames, time, status) -> None:
    global current_rms
    current_rms = float(np.sqrt(np.mean(indata.astype(np.float32) ** 2)))
    if _loop:
        _loop.call_soon_threadsafe(audio_queue.put_nowait, bytes(indata))


def clear_queue() -> None:
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except asyncio.QueueEmpty:
            break


def start(loop: asyncio.AbstractEventLoop) -> sd.InputStream:
    global _loop
    _loop = loop
    stream = sd.InputStream(
        samplerate=MIC_SAMPLE_RATE,
        channels=1,
        dtype="int16",
        blocksize=MIC_CHUNK_SIZE,
        callback=_callback,
    )
    stream.start()
    print(f"[MIC] aktywny ({MIC_SAMPLE_RATE}Hz, chunk={MIC_CHUNK_SIZE})")
    return stream
