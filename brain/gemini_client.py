import asyncio
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from audio import play_audio
from ws_server import audio_queue, clear_queue

_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1alpha"},
)

_live_config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction=SYSTEM_PROMPT,
)

_is_playing = False


async def _send_audio(session) -> None:
    while True:
        chunk = await audio_queue.get()
        if not _is_playing:
            await session.send_realtime_input(
                audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
            )


async def _receive_audio(session) -> None:
    global _is_playing
    loop = asyncio.get_event_loop()
    while True:
        audio_buffer = bytearray()
        async for response in session.receive():
            if response.server_content:
                if response.server_content.model_turn:
                    for part in response.server_content.model_turn.parts:
                        if part.inline_data:
                            audio_buffer.extend(part.inline_data.data)
                if response.server_content.turn_complete:
                    if audio_buffer:
                        _is_playing = True
                        await loop.run_in_executor(None, play_audio, bytes(audio_buffer))
                        _is_playing = False
                        audio_buffer = bytearray()
                        clear_queue()


async def run() -> None:
    while True:
        try:
            async with _client.aio.live.connect(model=GEMINI_MODEL, config=_live_config) as session:
                send_task = asyncio.create_task(_send_audio(session))
                recv_task = asyncio.create_task(_receive_audio(session))
                try:
                    done, pending = await asyncio.wait(
                        {send_task, recv_task},
                        return_when=asyncio.FIRST_COMPLETED,
                    )
                    for task in pending:
                        task.cancel()
                    for task in done:
                        if not task.cancelled() and task.exception():
                            raise task.exception()
                finally:
                    send_task.cancel()
                    recv_task.cancel()
        except Exception as e:
            print(f"\n[Gemini] sesja zakończona ({type(e).__name__}), ponawiam...")
        await asyncio.sleep(2)
