"""Test głośnika ESP32 — uruchom zamiast main.py, gra ciągłą gamę przez WebSocket."""

import asyncio
import math
import struct
import websockets

from config import WS_HOST, WS_PORT

SAMPLE_RATE = 24000
CHUNK_SAMPLES = 512
NOTES = [261.6, 293.7, 329.6, 349.2, 392.0, 440.0]
NOTE_SAMPLES = SAMPLE_RATE // 2   # 0.5s per nuta
PAUSE_SAMPLES = SAMPLE_RATE // 10  # 100ms pauza


def generate_note(freq: float, n_samples: int, start_phase: float = 0.0):
    inc = 2 * math.pi * freq / SAMPLE_RATE
    samples = []
    phase = start_phase
    for _ in range(n_samples):
        samples.append(int(math.sin(phase) * 6000))
        phase += inc
        if phase > 2 * math.pi:
            phase -= 2 * math.pi
    return struct.pack(f"<{n_samples}h", *samples), phase


def pcm_chunk(buf: list[int], start: int, size: int) -> bytes:
    end = min(start + size, len(buf))
    return struct.pack(f"<{end - start}h", *buf[start:end])


async def stream_audio(websocket):
    print(f"[test] ESP32 połączony, gram gamę w pętli — Ctrl+C żeby zakończyć")
    silence = struct.pack(f"<{CHUNK_SAMPLES}h", *([0] * CHUNK_SAMPLES))
    while True:
        for freq in NOTES:
            phase = 0.0
            for offset in range(0, NOTE_SAMPLES, CHUNK_SAMPLES):
                chunk_size = min(CHUNK_SAMPLES, NOTE_SAMPLES - offset)
                data, phase = generate_note(freq, chunk_size, phase)
                await websocket.send(data)
                await asyncio.sleep(chunk_size / SAMPLE_RATE * 0.9)
            for _ in range(0, PAUSE_SAMPLES, CHUNK_SAMPLES):
                await websocket.send(silence)
                await asyncio.sleep(CHUNK_SAMPLES / SAMPLE_RATE * 0.9)


async def handle(websocket):
    try:
        await stream_audio(websocket)
    except websockets.exceptions.ConnectionClosed:
        print("[test] ESP32 rozłączył się")


async def main():
    print(f"[test] serwer na {WS_HOST}:{WS_PORT} — czekam na ESP32...")
    async with websockets.serve(handle, WS_HOST, WS_PORT):
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[test] stop")
