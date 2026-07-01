"""Mordo PC — wersja bez ESP32. Mikrofon i głośniki laptopa."""
import asyncio
import threading
import tkinter as tk

from config import GEMINI_API_KEY
from gemini_client import run
import mic_local
from speaker_local import player_open, player_write, player_stop, player_abort

_state = {"mode": "listen"}


def _on_state(state: str) -> None:
    _state["mode"] = state


class StatusWindow:
    MIC_MAX_RMS = 2500.0

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mordo")
        self.root.geometry("260x72")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#1a1a1a")

        mic_row = tk.Frame(self.root, bg="#1a1a1a")
        mic_row.pack(fill="x", padx=10, pady=(10, 3))
        tk.Label(mic_row, text="MIC", fg="#888", bg="#1a1a1a", width=5, anchor="w").pack(side="left")
        self._mic_cv = tk.Canvas(mic_row, height=16, bg="#333", highlightthickness=0)
        self._mic_cv.pack(side="left", fill="x", expand=True)
        self._mic_bar = self._mic_cv.create_rectangle(0, 0, 0, 16, fill="#00AA44", outline="")

        spk_row = tk.Frame(self.root, bg="#1a1a1a")
        spk_row.pack(fill="x", padx=10, pady=(3, 10))
        tk.Label(spk_row, text="SPEAK", fg="#888", bg="#1a1a1a", width=5, anchor="w").pack(side="left")
        self._spk_cv = tk.Canvas(spk_row, width=20, height=16, bg="#1a1a1a", highlightthickness=0)
        self._spk_cv.pack(side="left")
        self._spk_dot = self._spk_cv.create_oval(2, 2, 14, 14, fill="#444", outline="")

        self.root.after(100, self._tick)

    def _tick(self):
        # słupek mikrofonu
        w = self._mic_cv.winfo_width()
        level = min(1.0, mic_local.current_rms / self.MIC_MAX_RMS)
        self._mic_cv.coords(self._mic_bar, 0, 0, int(w * level), 16)

        # kółko głośnika
        color = "#00CC44" if _state["mode"] == "speak" else "#444"
        self._spk_cv.itemconfig(self._spk_dot, fill=color)

        self.root.after(100, self._tick)

    def run(self):
        self.root.mainloop()


def _run_async() -> None:
    async def _main():
        loop = asyncio.get_event_loop()
        mic_local.start(loop)
        await run(
            mic_local.audio_queue,
            mic_local.clear_queue,
            _on_state,
            player_open, player_write, player_stop, player_abort,
        )

    asyncio.run(_main())


def main() -> None:
    if not GEMINI_API_KEY:
        print("Błąd: ustaw zmienną środowiskową GEMINI_API_KEY")
        return

    print("Mordo PC startuje... (zamknij okno żeby zatrzymać)")
    t = threading.Thread(target=_run_async, daemon=True)
    t.start()

    StatusWindow().run()


if __name__ == "__main__":
    main()
