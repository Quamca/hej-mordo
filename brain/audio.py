import numpy as np
import sounddevice as sd

from config import SPEAKER_SAMPLE_RATE


def play_audio(data: bytes) -> None:
    audio = np.frombuffer(data, dtype=np.int16)
    sd.play(audio, samplerate=SPEAKER_SAMPLE_RATE)
    sd.wait()
