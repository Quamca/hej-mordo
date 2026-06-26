# Mordo — Stan Projektu

## Aktualna faza
Faza 1 — Hardware Mordo (ESP32-S3)

## Co jest zrobione
- Struktura projektu i agenci Claude Code
- ISSUE-006: Mikrofon ESP32-S3 Sense — firmware PDM działa
- ISSUE-007: Jakość mikrofonu — 16kHz, 16-bit, jakość dobra
- ISSUE-008: WiFi + WebSocket — ESP32 strumieniuje audio PCM do brain
- ISSUE-009: Pełna pętla audio — ESP32 mic → brain → Gemini → głośnik PC, multi-turn działa
- ISSUE-010: Streaming playback + barge-in + VAD 400ms/200ms — działa

## ISSUE-011 — w trakcie testowania
Głośnik MAX98357A podłączony (BCLK=D8, LRC=D7, DIN=D6).
Firmware i brain gotowe — czeka na test manualny:
- `python brain/test_speaker.py` → ESP32 podłącza się, gra gamę w pętli (test czy głośnik gra czysto)
- `python brain/main.py` → pełna pętla z Gemini przez wbudowany głośnik ESP32

Implementacja:
- firmware: I2S_NUM_1 dla głośnika, ring buffer 8KB, mic timeout 10ms
- brain/ws_server.py: outgoing_queue, sender task, enqueue_audio/stop
- brain/audio.py: zastąpiono sounddevice wysyłaniem przez WebSocket do ESP32

## Repo
https://github.com/Quamca/hej-mordo (publiczne)

## Ostatnia sesja
2026-06-26 — ISSUE-011 zaimplementowany (firmware + brain), test manualny do wykonania.
Dodano test_speaker.py do szybkiego sprawdzania głośnika bez uruchamiania main.py.
