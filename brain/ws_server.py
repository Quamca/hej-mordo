"""WebSocket server: odbiera audio mic z ESP32, wysyła audio głośnika do ESP32."""

import asyncio
import websockets
import websockets.exceptions

from config import WS_HOST, WS_PORT

audio_queue: asyncio.Queue = asyncio.Queue()
outgoing_queue: asyncio.Queue = asyncio.Queue()
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
                await audio_queue.put(message)
                chunks += 1
                print(f"[WS] chunk #{chunks}: {len(message)}B", end="\r")
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        sender.cancel()
        clear_outgoing()
        print(f"\n[WS] rozłączono: {addr} (chunków: {chunks})")


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
