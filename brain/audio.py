from ws_server import enqueue_audio, enqueue_stop, clear_outgoing


def player_open() -> None:
    pass  # stream otwiera się przez I2S na ESP32


def player_write(data: bytes) -> None:
    enqueue_audio(data)


def player_stop() -> None:
    enqueue_stop()


def player_abort() -> None:
    clear_outgoing()
    enqueue_stop()
