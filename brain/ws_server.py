"""WebSocket server: odbiera audio mic i klatki kamery z ESP32, wysyła audio do ESP32."""

import asyncio
import os
import websockets
import websockets.exceptions

from config import WS_HOST, WS_PORT

_BRAIN_DIR = os.path.dirname(os.path.abspath(__file__))

CAM_HEADER = b'CAM\x00'

audio_queue: asyncio.Queue = asyncio.Queue()
frame_queue: asyncio.Queue = asyncio.Queue(maxsize=2)  # tylko najnowsze klatki
outgoing_queue: asyncio.Queue = asyncio.Queue()
frame_callbacks: list = []  # rejestrowane przez moduły (np. face.py)
_debug_frame_saved = False
_loop: asyncio.AbstractEventLoop | None = None


async def _sender(websocket) -> None:
    while True:
        data = await outgoing_queue.get()
        try:
            if isinstance(data, bytes):
                await websocket.send(data)
            else:
                await websocket.send(str(data))
        except Exception:
            break


async def handle(websocket):
    addr = websocket.remote_address
    print(f"[WS] połączono: {addr}")
    sender = asyncio.create_task(_sender(websocket))
    chunks = 0
    try:
        async for message in websocket:
            if isinstance(message, bytes):
                if message[:4] == CAM_HEADER:
                    frame = message[4:]
                    _handle_frame(frame)
                else:
                    await audio_queue.put(message)
                    chunks += 1
                    print(f"[WS] chunk #{chunks}: {len(message)}B", end="\r")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        sender.cancel()
        clear_outgoing()
        print(f"\n[WS] rozłączono: {addr} (chunków: {chunks})")


def _handle_frame(data: bytes) -> None:
    global _debug_frame_saved
    for cb in frame_callbacks:
        cb(data)
    if not _debug_frame_saved:
        try:
            path = os.path.join(_BRAIN_DIR, "frame_debug.jpg")
            with open(path, "wb") as f:
                f.write(data)
            print(f"[CAM] pierwsza klatka zapisana: {path}")
        except Exception:
            pass
        _debug_frame_saved = True
    # Nadpisz kolejkę najnowszą klatką (drop stare jeśli pełna)
    if frame_queue.full():
        try:
            frame_queue.get_nowait()
        except asyncio.QueueEmpty:
            pass
    try:
        frame_queue.put_nowait(data)
    except asyncio.QueueFull:
        pass


async def start():
    global _loop
    _loop = asyncio.get_running_loop()
    print(f"[WS] serwer nasłuchuje na {WS_HOST}:{WS_PORT}")
    async with websockets.serve(handle, WS_HOST, WS_PORT):
        await asyncio.Future()


def enqueue_audio(data: bytes) -> None:
    if _loop:
        _loop.call_soon_threadsafe(outgoing_queue.put_nowait, data)


def enqueue_stop() -> None:
    if _loop:
        _loop.call_soon_threadsafe(outgoing_queue.put_nowait, "STOP")


def enqueue_state(state: str) -> None:
    if _loop:
        _loop.call_soon_threadsafe(outgoing_queue.put_nowait, f"STATE:{state}")


def clear_queue() -> None:
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except asyncio.QueueEmpty:
            break


def clear_outgoing() -> None:
    while not outgoing_queue.empty():
        try:
            outgoing_queue.get_nowait()
        except asyncio.QueueEmpty:
            break


if __name__ == "__main__":
    asyncio.run(start())
