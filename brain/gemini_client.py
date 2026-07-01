import asyncio
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT

_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1alpha"},
)

_live_config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction=SYSTEM_PROMPT,
    realtime_input_config=types.RealtimeInputConfig(
        automatic_activity_detection=types.AutomaticActivityDetection(
            prefix_padding_ms=200,
            silence_duration_ms=400,
        )
    ),
)


async def _send_audio(session, audio_queue) -> None:
    while True:
        chunk = await audio_queue.get()
        await session.send_realtime_input(
            audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
        )


async def _receive_audio(session, clear_queue, on_state,
                         player_open, player_write, player_stop, player_abort) -> None:
    loop = asyncio.get_event_loop()
    while True:
        stream_open = False
        on_state("listen")
        async for response in session.receive():
            if not response.server_content:
                continue
            sc = response.server_content
            if sc.interrupted:
                await loop.run_in_executor(None, player_abort)
                clear_queue()
                on_state("listen")
                stream_open = False
                break
            if sc.model_turn:
                for part in sc.model_turn.parts:
                    if part.inline_data:
                        if not stream_open:
                            await loop.run_in_executor(None, player_open)
                            on_state("speak")
                            stream_open = True
                        await loop.run_in_executor(None, player_write, part.inline_data.data)
            if sc.turn_complete:
                await loop.run_in_executor(None, player_stop)
                clear_queue()
                on_state("listen")
                stream_open = False


async def run(audio_queue, clear_queue, on_state,
              player_open, player_write, player_stop, player_abort) -> None:
    while True:
        try:
            async with _client.aio.live.connect(model=GEMINI_MODEL, config=_live_config) as session:
                send_task = asyncio.create_task(_send_audio(session, audio_queue))
                recv_task = asyncio.create_task(_receive_audio(
                    session, clear_queue, on_state,
                    player_open, player_write, player_stop, player_abort,
                ))
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
