"""WebSocket server odbierający chunki audio PCM z ESP32."""

import asyncio
import websockets
import websockets.exceptions

from config import WS_HOST, WS_PORT

audio_queue: asyncio.Queue = asyncio.Queue()


async def handle(websocket):
    addr = websocket.remote_address
    print(f"[WS] połączono: {addr}")
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
        print(f"\n[WS] rozłączono: {addr} (chunków: {chunks})")


async def start():
    print(f"[WS] serwer nasłuchuje na {WS_HOST}:{WS_PORT}")
    async with websockets.serve(handle, WS_HOST, WS_PORT):
        await asyncio.Future()


def clear_queue() -> None:
    while not audio_queue.empty():
        try:
            audio_queue.get_nowait()
        except asyncio.QueueEmpty:
            break


if __name__ == "__main__":
    asyncio.run(start())
