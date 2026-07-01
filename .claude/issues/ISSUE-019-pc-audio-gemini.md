---
title: "ISSUE-019: PC audio — rozmowa z Gemini przez mikrofon i głośniki laptopa"
status: planned
type: issue
faza: 0
epic: EPIC-1
created: 2026-07-01
updated: 2026-07-01
---

## Cel

Uruchamiasz `python brain/pc_mordo.py` i możesz rozmawiać z Gemini przez mikrofon i głośniki laptopa. Bez ESP32, bez WebSocket.

## Acceptance Criteria

- [ ] `pc_mordo.py` startuje i łączy się z Gemini Live
- [ ] Mikrofon laptopa (domyślne urządzenie systemowe) wysyła audio do Gemini
- [ ] Głośniki laptopa odtwarzają odpowiedź Gemini w czasie rzeczywistym
- [ ] Gemini nie przerywa sam siebie (barge-in działa — Igor może przerywać Gemini)
- [ ] Ctrl+C czysto kończy sesję

## Notatki

- Nowy punkt wejścia: `brain/pc_mordo.py`
- Nowy moduł: `brain/mic_local.py` — capture z laptopa przez `sounddevice` (16kHz, 16-bit, mono)
- Nowy moduł: `brain/speaker_local.py` — playback przez `sounddevice` (24kHz, 16-bit)
- `gemini_client.py` zostaje bez zmian — tylko źródło audio się zmienia
- `ws_server.py` i `audio.py` zostają nieruszone (wersja ESP32 nadal działa)
- Format audio do Gemini: PCM 16kHz (tak samo jak z ESP32)
- Format audio z Gemini: PCM 24kHz

## Test manualny

1. `cd brain && python pc_mordo.py`
2. Powiedz "cześć" → Gemini odpowiada głosem przez głośniki
3. Przerwij Gemini w połowie zdania → Gemini przestaje mówić, słucha dalej
4. Ctrl+C → program kończy bez błędów
