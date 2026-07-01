import asyncio
import time
from google import genai
from google.genai import types

from config import GEMINI_API_KEY, GEMINI_MODEL, SYSTEM_PROMPT
from audio import player_open, player_write, player_stop, player_abort
from ws_server import audio_queue as _ws_audio_queue, clear_queue as _ws_clear_queue, enqueue_state

_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1alpha"},
)

COOLDOWN_S = 30.0
_END_TOOL_NAME = "zakoncz_rozmowe"

_GREETING_PROMPT = (
    "\n\nIgor właśnie pojawił się przed kamerą. W SWOJEJ PIERWSZEJ wypowiedzi w tej sesji "
    "przywitaj go krótko i zapytaj czy możesz w czymś pomóc — zrób to TYLKO RAZ, na samym "
    "początku. W dalszej części rozmowy NIE witaj się ponownie i nie powtarzaj pytania — "
    "odpowiadaj normalnie na to co mówi Igor, jak w zwykłej rozmowie. "
    "Jeśli Igor da do zrozumienia że nie chce teraz rozmawiać "
    "(np. \"nie dzięki\", \"nie teraz\", \"spoko\", \"nic\") — pożegnaj się krótko "
    f"i wywołaj funkcję {_END_TOOL_NAME}."
)

_greeting_config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction=SYSTEM_PROMPT + _GREETING_PROMPT,
    tools=[types.Tool(function_declarations=[
        types.FunctionDeclaration(
            name=_END_TOOL_NAME,
            description="Wywołaj gdy Igor da do zrozumienia że nie chce teraz rozmawiać.",
        ),
    ])],
    realtime_input_config=types.RealtimeInputConfig(
        automatic_activity_detection=types.AutomaticActivityDetection(
            prefix_padding_ms=200,
            silence_duration_ms=400,
        )
    ),
)

_trigger_event: asyncio.Event | None = None
_last_dismiss_ts = 0.0


def init_trigger() -> asyncio.Event:
    global _trigger_event
    _trigger_event = asyncio.Event()
    return _trigger_event


def signal_igor_present() -> None:
    if _trigger_event:
        _trigger_event.set()


def signal_wake_word() -> None:
    """Świadoma komenda głosowa — pomija cooldown po dismissie."""
    global _last_dismiss_ts
    _last_dismiss_ts = 0.0
    if _trigger_event:
        _trigger_event.set()


async def _send_audio(session, audio_queue) -> None:
    while True:
        chunk = await audio_queue.get()
        await session.send_realtime_input(
            audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000")
        )


async def _receive_audio(session, clear_queue, on_state,
                         player_open, player_write, player_stop, player_abort) -> bool:
    """Zwraca True gdy Gemini wywoła zakończenie rozmowy (dismiss)."""
    loop = asyncio.get_event_loop()
    while True:
        stream_open = False
        on_state("listen")
        async for response in session.receive():
            if response.tool_call:
                for fc in response.tool_call.function_calls:
                    if fc.name == _END_TOOL_NAME:
                        await session.send_tool_response(
                            function_responses=[types.FunctionResponse(
                                id=fc.id, name=fc.name, response={"ok": True},
                            )]
                        )
                        return True
                continue
            if not response.server_content:
                continue
            sc = response.server_content
            if sc.interrupted:
                print("[Gemini] PRZERWANO (interrupted)", flush=True)
                await loop.run_in_executor(None, player_abort)
                clear_queue()
                on_state("listen")
                stream_open = False
                break
            if sc.model_turn:
                for part in sc.model_turn.parts:
                    if part.inline_data:
                        if not stream_open:
                            print("[Gemini] TURA START (model zaczyna mówić)", flush=True)
                            await loop.run_in_executor(None, player_open)
                            on_state("speak")
                            stream_open = True
                        await loop.run_in_executor(None, player_write, part.inline_data.data)
            if sc.turn_complete:
                print("[Gemini] TURA KONIEC (turn_complete)", flush=True)
                await loop.run_in_executor(None, player_stop)
                clear_queue()
                on_state("listen")
                stream_open = False
    return False


async def run_triggered(audio_queue=None, clear_queue=None, on_state=None,
                         player_open=player_open, player_write=player_write,
                         player_stop=player_stop, player_abort=player_abort) -> None:
    global _last_dismiss_ts
    audio_queue = audio_queue if audio_queue is not None else _ws_audio_queue
    clear_queue = clear_queue if clear_queue is not None else _ws_clear_queue
    on_state = on_state if on_state is not None else enqueue_state
    trigger = init_trigger()

    while True:
        await trigger.wait()
        trigger.clear()
        if time.time() - _last_dismiss_ts < COOLDOWN_S:
            continue

        print("[Gemini] Igor rozpoznany — sesja powitalna", flush=True)
        clear_queue()
        dismissed = False
        while not dismissed:
            try:
                async with _client.aio.live.connect(model=GEMINI_MODEL, config=_greeting_config) as session:
                    print("[Gemini] wysyłam wiadomość startową", flush=True)
                    await session.send_client_content(
                        turns=types.Content(
                            role="user",
                            parts=[types.Part(text="[Igor pojawił się przed kamerą — przywitaj się]")],
                        ),
                        turn_complete=True,
                    )
                    send_task = asyncio.create_task(_send_audio(session, audio_queue))
                    recv_task = asyncio.create_task(_receive_audio(
                        session, clear_queue, on_state,
                        player_open, player_write, player_stop, player_abort,
                    ))
                    done, pending = await asyncio.wait(
                        {send_task, recv_task}, return_when=asyncio.FIRST_COMPLETED,
                    )
                    for task in pending:
                        task.cancel()
                    for task in done:
                        if task is recv_task:
                            dismissed = task.result()
                        elif not task.cancelled() and task.exception():
                            raise task.exception()
            except Exception as e:
                print(f"[Gemini] sesja zakończona ({type(e).__name__}), ponawiam...", flush=True)
                await asyncio.sleep(2)

        _last_dismiss_ts = time.time()
        on_state("listen")
        print(f"[Gemini] dismiss — cooldown {COOLDOWN_S:.0f}s", flush=True)
